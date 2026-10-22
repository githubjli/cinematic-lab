"""Submit one project-local ComfyUI API workflow to the isolated server."""
import argparse
import hashlib
import json
import subprocess
import time
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument("workflow", type=Path)
parser.add_argument("--url", default="http://127.0.0.1:8189")
args = parser.parse_args()


def request(path, payload=None):
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(args.url + path, data=data, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as response:
        return json.load(response)


workflow_path = args.workflow.resolve()
prompt = json.loads(workflow_path.read_text(encoding="utf-8"))
workflow_hash = hashlib.sha256(workflow_path.read_bytes()).hexdigest().upper()
started = time.monotonic()
reply = request("/prompt", {"prompt": prompt})
prompt_id = reply["prompt_id"]
print("Queued", prompt_id, flush=True)

log_dir = ROOT / "runtime" / "comfyui" / "logs"
log_dir.mkdir(parents=True, exist_ok=True)
stamp = time.strftime("%Y%m%d-%H%M%S")
record_path = log_dir / f"wan-control-{stamp}.json"
record = {"prompt_id": prompt_id, "workflow": str(workflow_path), "workflow_sha256": workflow_hash, "state": "running"}
record_path.write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding="utf-8")

peak_gpu_mib = 0
while True:
    gpu = subprocess.run(
        ["nvidia-smi", "--query-gpu=memory.used", "--format=csv,noheader,nounits"],
        capture_output=True,
        text=True,
    )
    if gpu.returncode == 0 and gpu.stdout.strip():
        peak_gpu_mib = max(peak_gpu_mib, int(gpu.stdout.strip().splitlines()[0]))
    history = request("/history/" + prompt_id)
    if prompt_id in history:
        result = history[prompt_id]
        state = result["status"]["status_str"]
        record.update(
            state=state,
            elapsed_seconds=round(time.monotonic() - started, 2),
            sampled_peak_total_gpu_mib=peak_gpu_mib,
            history=result,
        )
        record_path.write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding="utf-8")
        print("Result", state, "seconds", record["elapsed_seconds"], "record", record_path, flush=True)
        print(json.dumps(result.get("outputs", {}), ensure_ascii=False), flush=True)
        raise SystemExit(0 if state == "success" else 1)
    time.sleep(3)
