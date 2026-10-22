from pathlib import Path
import wave
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs" / "blender-demo-v006" / "mechanical-temp-sound-v006.wav"
RATE = 48_000
DURATION = 16.0
N = int(RATE * DURATION)
t = np.arange(N, dtype=np.float64) / RATE
rng = np.random.default_rng(20261022)


def envelope(start, end, attack=0.08, release=0.12):
    env = np.zeros_like(t)
    active = (t >= start) & (t <= end)
    env[active] = 1.0
    if attack:
        mask = (t >= start) & (t < start + attack)
        env[mask] = (t[mask] - start) / attack
    if release:
        mask = (t > end - release) & (t <= end)
        env[mask] = (end - t[mask]) / release
    return np.clip(env, 0, 1)


sound = np.zeros(N, dtype=np.float64)
sound += 0.10 * np.sin(2 * np.pi * 58 * t) * envelope(0.0, 6.0, 0.4, 0.5)
sound += 0.035 * np.sin(2 * np.pi * 116 * t) * envelope(0.0, 6.0, 0.4, 0.5)
sound += 0.018 * rng.normal(size=N) * envelope(0.0, 6.0, 0.5, 0.6)

# Ram pressure rises until the platen reaches the bale contact plane at 9.67 s.
hyd = envelope(4.0, 9.8, 0.5, 0.3)
freq = 72 + 34 * np.clip((t - 4.0) / 5.8, 0, 1)
phase = 2 * np.pi * np.cumsum(freq) / RATE
sound += 0.12 * np.sin(phase) * hyd
sound += 0.025 * rng.normal(size=N) * hyd

# Contact stop, gate fully open, and start of the continued discharge stroke.
for when, frequency, amp, decay in [
    (9.67, 54, 0.42, 0.22),
    (11.33, 330, 0.22, 0.11),
    (12.00, 88, 0.30, 0.16),
]:
    local = np.maximum(t - when, 0)
    event = (t >= when) * np.sin(2 * np.pi * frequency * local) * np.exp(-local / decay)
    event += (t >= when) * 0.25 * rng.normal(size=N) * np.exp(-local / (decay * 0.65))
    sound += amp * event

push = envelope(12.0, 15.45, 0.18, 0.35)
sound += 0.085 * np.sin(2 * np.pi * 44 * t) * push
sound += 0.045 * rng.normal(size=N) * push

sound = np.tanh(sound * 1.4) * 0.72
delay = int(0.013 * RATE)
left = sound
right = np.roll(sound, delay) * 0.92
right[:delay] = 0
pcm = np.int16(np.clip(np.column_stack([left, right]), -1, 1) * 32767)

OUT.parent.mkdir(parents=True, exist_ok=True)
with wave.open(str(OUT), "wb") as handle:
    handle.setnchannels(2)
    handle.setsampwidth(2)
    handle.setframerate(RATE)
    handle.writeframes(pcm.tobytes())

print(OUT)
