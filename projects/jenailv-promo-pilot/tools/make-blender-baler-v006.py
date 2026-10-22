from pathlib import Path


PROJECT = Path(r"C:\Users\76797\Desktop\chatgpt\cinematic-lab\projects\jenailv-promo-pilot")
source_path = PROJECT / "tools" / "blender-baler-demo-v005.py"
target_path = PROJECT / "tools" / "blender-baler-demo-v006.py"

source = source_path.read_text(encoding="utf-8")
source = source.replace('import math\n', 'import math\nimport json\n')
source = source.replace('"blender-demo-v005"', '"blender-demo-v006"')
source = source.replace('v005-720x1280.mp4', 'v006-720x1280.mp4')
source = source.replace('v005.blend', 'v006.blend')

old_ram = '''# Hydraulic cylinder, rod, and platen. Near side stays open for cutaway view.
cylinder("Cylinder body", (-4.2, 0, 2.5), 0.54, 2.6, STEEL, (0, math.radians(90), 0))
rod = cylinder("Cylinder rod", (-2.4, 0, 2.5), 0.26, 2.8, LIGHT_STEEL, (0, math.radians(90), 0))
platen = cube("Compression platen", (-1.0, 0, 2.45), (0.24, 1.7, 1.45), YELLOW)
key(rod, 72, (-2.4, 0, 2.5), (1, 1, 1))
key(rod, 150, (0.0, 0, 2.5), (1.0, 1.0, 2.65))
key(platen, 72, (-1.0, 0, 2.45))
key(platen, 150, (2.15, 0, 2.45))
'''
new_ram = '''# One continuous hydraulic ram performs compression and the later discharge stroke.
# The yellow platen stops 30 mm before the proxy bale envelope, then remains in
# contact while both objects translate by the same amount. This avoids the v005
# overlap and removes the mechanically ambiguous second yellow ejector plate.
cylinder("Cylinder body", (-4.2, 0, 2.5), 0.54, 2.6, STEEL, (0, math.radians(90), 0))
rod = cylinder("Cylinder rod", (-2.07, 0, 2.5), 0.26, 1.66, LIGHT_STEEL, (0, math.radians(90), 0))
platen = cube("Compression and discharge platen", (-1.0, 0, 2.45), (0.24, 1.7, 1.45), YELLOW)
key(rod, 72, (-2.07, 0, 2.5), (1, 1, 1))
key(rod, 145, (-0.805, 0, 2.5), (1.0, 1.0, 2.524))
key(rod, 180, (-0.805, 0, 2.5), (1.0, 1.0, 2.524))
key(rod, 230, (0.995, 0, 2.5), (1.0, 1.0, 4.693))
key(platen, 72, (-1.0, 0, 2.45))
key(platen, 145, (1.53, 0, 2.45))
key(platen, 180, (1.53, 0, 2.45))
key(platen, 230, (5.13, 0, 2.45))
'''
if old_ram not in source:
    raise RuntimeError("v005 ram block was not found")
source = source.replace(old_ram, new_ram)

source = source.replace('key(bale, 176, (2.75, 0, 2.05), (1, 1, 1))\nkey(bale, 226, (6.35, 0, 2.05), (1, 1, 1))',
                        'key(bale, 180, (2.75, 0, 2.05), (1, 1, 1))\nkey(bale, 230, (6.35, 0, 2.05), (1, 1, 1))')
source = source.replace('key(strap, 176, (2.75 + offset, -1.57, 2.05), (1, 1, 1))\n    key(strap, 226, (6.35 + offset, -1.57, 2.05), (1, 1, 1))',
                        'key(strap, 180, (2.75 + offset, -1.57, 2.05), (1, 1, 1))\n    key(strap, 230, (6.35 + offset, -1.57, 2.05), (1, 1, 1))')

start = source.index('# Explicit ejector:')
end = source.index('# Material identity markers')
source = source[:start] + '''# The separate v005 ejector was removed. A single ram now exposes the causal sequence.\n''' + source[end:]

source = source.replace('key(patch, 176, loc, (1, 1, 1))\n    key(patch, 226, (loc[0] + 3.6, loc[1], loc[2]), (1, 1, 1))',
                        'key(patch, 180, loc, (1, 1, 1))\n    key(patch, 230, (loc[0] + 3.6, loc[1], loc[2]), (1, 1, 1))')

audit_marker = '# Save the editable source and render the 16-second vertical proxy.\n'
audit_block = '''# Deterministic one-dimensional interference audit for the contact surfaces.
bale_half_x = 0.95
platen_half_x = 0.24
contact_gap = (2.75 - bale_half_x) - (1.53 + platen_half_x)
push_start_gap = contact_gap
push_end_gap = ((6.35 - bale_half_x) - (5.13 + platen_half_x))
assert contact_gap >= 0.0, "Platen intersects bale at compression stop"
assert abs(push_end_gap - push_start_gap) < 1e-6, "Platen and bale lose contact spacing during discharge"
audit = {
    "version": "v006",
    "status": "motion proxy; real machine internals unverified",
    "removed_component": "separate v005 ejector plate",
    "sequence": ["feed", "compress", "form_bale", "open_exit_gate", "continue_ram_stroke_to_discharge"],
    "proxy_units": "Blender units",
    "bale_initial_x_interval": [1.8, 3.7],
    "platen_compression_stop_x_interval": [1.29, 1.77],
    "surface_gap_at_compression_stop": round(contact_gap, 6),
    "surface_gap_at_discharge_end": round(push_end_gap, 6),
    "timing_before_1_6_scale": {"contact": 145, "gate_open": 170, "discharge_start": 180, "discharge_end": 230},
}
(OUT / "mechanism-interference-audit-v006.json").write_text(json.dumps(audit, indent=2), encoding="utf-8")

'''
if audit_marker not in source:
    raise RuntimeError("render marker was not found")
source = source.replace(audit_marker, audit_block + audit_marker)
target_path.write_text(source, encoding="utf-8")
print(target_path)
