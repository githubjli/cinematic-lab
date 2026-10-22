from pathlib import Path
import wave
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs" / "blender-demo-v004" / "mechanical-temp-sound-v001.wav"
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

# Conveyor and motor bed.
sound += 0.10 * np.sin(2 * np.pi * 58 * t) * envelope(0.0, 6.0, 0.4, 0.5)
sound += 0.035 * np.sin(2 * np.pi * 116 * t) * envelope(0.0, 6.0, 0.4, 0.5)
sound += 0.018 * rng.normal(size=N) * envelope(0.0, 6.0, 0.5, 0.6)

# Hydraulic pressure rises through compression.
hyd = envelope(4.0, 10.6, 0.5, 0.3)
freq = 72 + 34 * np.clip((t - 4.0) / 6.6, 0, 1)
phase = 2 * np.pi * np.cumsum(freq) / RATE
sound += 0.12 * np.sin(phase) * hyd
sound += 0.025 * rng.normal(size=N) * hyd

# Short mechanical events: compression stop, gate release, ejector contact.
for when, frequency, amp, decay in [
    (10.45, 54, 0.42, 0.22),
    (11.15, 330, 0.22, 0.11),
    (12.05, 88, 0.30, 0.16),
]:
    local = np.maximum(t - when, 0)
    event = (t >= when) * np.sin(2 * np.pi * frequency * local) * np.exp(-local / decay)
    event += (t >= when) * 0.25 * rng.normal(size=N) * np.exp(-local / (decay * 0.65))
    sound += amp * event

# Ejector and bale friction bed.
push = envelope(12.0, 15.7, 0.18, 0.35)
sound += 0.085 * np.sin(2 * np.pi * 44 * t) * push
sound += 0.045 * rng.normal(size=N) * push

# Gentle limiter and stereo room offset.
sound = np.tanh(sound * 1.4) * 0.72
delay = int(0.013 * RATE)
left = sound
right = np.roll(sound, delay) * 0.92
right[:delay] = 0
stereo = np.column_stack([left, right])
pcm = np.int16(np.clip(stereo, -1, 1) * 32767)

OUT.parent.mkdir(parents=True, exist_ok=True)
with wave.open(str(OUT), "wb") as handle:
    handle.setnchannels(2)
    handle.setsampwidth(2)
    handle.setframerate(RATE)
    handle.writeframes(pcm.tobytes())

print(OUT)
