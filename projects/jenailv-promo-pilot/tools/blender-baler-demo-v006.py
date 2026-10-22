import bpy
import math
import json
from pathlib import Path
from mathutils import Vector


PROJECT = Path(r"C:\Users\76797\Desktop\chatgpt\cinematic-lab\projects\jenailv-promo-pilot")
OUT = PROJECT / "outputs" / "blender-demo-v006"
OUT.mkdir(parents=True, exist_ok=True)

bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.frame_start = 1
scene.frame_end = 384
scene.render.fps = 24
scene.render.resolution_x = 720
scene.render.resolution_y = 1280
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = 'FFMPEG'
scene.render.ffmpeg.format = 'MPEG4'
scene.render.ffmpeg.codec = 'H264'
scene.render.ffmpeg.constant_rate_factor = 'MEDIUM'
scene.render.ffmpeg.ffmpeg_preset = 'GOOD'
scene.render.filepath = str(OUT / "jenailv-baler-concept-v006-720x1280.mp4")
scene.render.engine = 'BLENDER_EEVEE_NEXT'
scene.render.image_settings.color_mode = 'RGB'
scene.render.resolution_percentage = 100
scene.render.film_transparent = False
scene.render.image_settings.color_mode = 'RGB'
scene.view_settings.look = 'AgX - Medium High Contrast'
scene.world = bpy.data.worlds.new("Industrial World")
scene.world.color = (0.012, 0.025, 0.045)


def mat(name, color, metallic=0.0, roughness=0.45):
    material = bpy.data.materials.new(name)
    material.diffuse_color = (*color, 1.0)
    material.use_nodes = True
    bsdf = material.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = (*color, 1.0)
    bsdf.inputs["Metallic"].default_value = metallic
    bsdf.inputs["Roughness"].default_value = roughness
    return material


BLUE = mat("JNL Blue", (0.018, 0.16, 0.50), metallic=0.55, roughness=0.28)
DARK_BLUE = mat("Structure", (0.012, 0.035, 0.075), metallic=0.65, roughness=0.34)
YELLOW = mat("Safety", (0.92, 0.48, 0.025), metallic=0.28, roughness=0.30)
STEEL = mat("Steel", (0.28, 0.34, 0.40), metallic=0.90, roughness=0.24)
LIGHT_STEEL = mat("Rod", (0.62, 0.69, 0.76), metallic=0.98, roughness=0.12)
GREEN = mat("Flow", (0.10, 0.50, 0.22), metallic=0.05, roughness=0.55)
BALE = mat("Bale", (0.43, 0.28, 0.12), metallic=0.0, roughness=0.88)
WASTE_COLORS = [
    mat("Waste Blue", (0.025, 0.25, 0.68), roughness=0.42),
    mat("Waste White", (0.76, 0.80, 0.82), roughness=0.30),
    mat("Waste Kraft", (0.46, 0.27, 0.10), roughness=0.92),
    mat("Waste Red", (0.60, 0.035, 0.025), roughness=0.48),
]
CONCRETE = mat("Concrete", (0.09, 0.105, 0.12), metallic=0.0, roughness=0.82)
FACTORY_STEEL = mat("Factory Steel", (0.07, 0.085, 0.10), metallic=0.78, roughness=0.38)

# Procedural fiber breakup gives the deterministic bale a non-plastic surface.
bale_nodes = BALE.node_tree.nodes
bale_links = BALE.node_tree.links
bale_noise = bale_nodes.new("ShaderNodeTexNoise")
bale_noise.inputs["Scale"].default_value = 7.0
bale_noise.inputs["Detail"].default_value = 4.0
bale_noise.inputs["Roughness"].default_value = 0.72
bale_bump = bale_nodes.new("ShaderNodeBump")
bale_bump.inputs["Strength"].default_value = 0.32
bale_bump.inputs["Distance"].default_value = 0.12
bale_links.new(bale_noise.outputs["Fac"], bale_bump.inputs["Height"])
bale_links.new(bale_bump.outputs["Normal"], bale_nodes["Principled BSDF"].inputs["Normal"])


def cube(name, loc, scale, material, bevel=0.08):
    bpy.ops.mesh.primitive_cube_add(location=loc)
    obj = bpy.context.object
    obj.name = name
    obj.scale = scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if bevel:
        modifier = obj.modifiers.new("Edge bevel", 'BEVEL')
        modifier.width = bevel
        modifier.segments = 2
    obj.data.materials.append(material)
    return obj


def cylinder(name, loc, radius, depth, material, rotation=(0, 0, 0)):
    bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=radius, depth=depth, location=loc, rotation=rotation)
    obj = bpy.context.object
    obj.name = name
    obj.data.materials.append(material)
    return obj


def key(obj, frame, location=None, scale=None, rotation=None):
    if location is not None:
        obj.location = location
        obj.keyframe_insert("location", frame=frame)
    if scale is not None:
        obj.scale = scale
        obj.keyframe_insert("scale", frame=frame)
    if rotation is not None:
        obj.rotation_euler = rotation
        obj.keyframe_insert("rotation_euler", frame=frame)


def look_at(obj, point):
    direction = Vector(point) - obj.location
    obj.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()


def label(text, loc, size=0.62):
    bpy.ops.object.text_add(location=loc, rotation=(math.radians(90), 0, 0))
    obj = bpy.context.object
    obj.data.body = text
    obj.data.align_x = 'CENTER'
    obj.data.size = size
    obj.data.extrude = 0.018
    obj.data.materials.append(GREEN)
    return obj


# Floor and framing grid.
cube("Floor", (0, 0, -0.3), (11, 7, 0.2), CONCRETE, bevel=0)
for x in range(-10, 11, 2):
    cube(f"GridX{x}", (x, 0, -0.08), (0.015, 7, 0.015), STEEL, bevel=0)
for y in range(-6, 7, 2):
    cube(f"GridY{y}", (0, y, -0.08), (11, 0.015, 0.015), STEEL, bevel=0)

# Deterministic factory volume: columns and overhead beams establish vertical scale.
for x in (-9.0, -4.5, 0.0, 4.5, 9.0):
    cube(f"ColumnNear{x}", (x, 5.7, 4.8), (0.22, 0.22, 5.0), FACTORY_STEEL, bevel=0.03)
for z in (4.0, 7.8, 9.4):
    cube(f"BeamNear{z}", (0, 5.7, z), (10.0, 0.18, 0.18), FACTORY_STEEL, bevel=0.02)


def area_light(name, location, energy, color, size):
    bpy.ops.object.light_add(type='AREA', location=location)
    light = bpy.context.object
    light.name = name
    light.data.energy = energy
    light.data.color = color
    light.data.shape = 'DISK'
    light.data.size = size
    look_at(light, (0, 0, 2.0))
    return light


area_light("Cool roof key", (-4.0, -2.0, 11.0), 1700, (0.58, 0.72, 1.0), 6.0)
area_light("Warm practical", (5.0, -3.0, 8.0), 1200, (1.0, 0.47, 0.18), 4.0)
area_light("Machine rim", (2.5, 4.5, 6.5), 1350, (0.35, 0.55, 1.0), 3.0)

# Machine base and open cutaway chamber.
cube("Base", (0.5, 0, 0.35), (4.7, 2.2, 0.32), BLUE)
cube("Far wall", (0.8, 1.95, 2.3), (4.4, 0.14, 1.95), BLUE)
cube("Chamber floor", (0.8, 0, 0.95), (4.2, 1.9, 0.16), BLUE)
cube("Top rail", (0.8, 1.6, 4.3), (4.2, 0.22, 0.22), BLUE)
for x in (-3.2, -1.0, 1.2, 3.4):
    cube(f"Rib{x}", (x, 1.72, 2.5), (0.12, 0.18, 1.75), STEEL)

# Hopper and conveyor proxy.
cube("Conveyor bed", (-5.9, 0, 2.5), (3.4, 1.45, 0.18), STEEL)
conveyor = bpy.context.object
conveyor.rotation_euler[1] = math.radians(-12)
for index in range(8):
    roller = cylinder(f"Roller{index}", (-8.6 + index * 0.78, 0, 2.95 - index * 0.16), 0.12, 2.8, LIGHT_STEEL, (math.radians(90), 0, 0))
cube("Hopper back", (-2.55, 1.35, 4.25), (1.1, 0.12, 1.55), BLUE)
cube("Hopper left", (-2.55, 0.0, 4.15), (1.1, 0.12, 1.5), BLUE).rotation_euler[2] = math.radians(90)

# One continuous hydraulic ram performs compression and the later discharge stroke.
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

# Sliding exit gate.
gate = cube("Exit gate", (3.65, 0, 2.35), (0.18, 1.78, 1.5), BLUE)
key(gate, 145, (3.65, 0, 2.35))
key(gate, 170, (3.65, 0, 5.8))

# Loose material moves into the chamber and compresses.
waste = []
for index in range(14):
    x0 = -8.2 + (index % 7) * 0.75
    y0 = -0.9 + (index % 4) * 0.55
    z0 = 3.2 + (index % 3) * 0.34
    size = (0.32 + (index % 2) * 0.1, 0.28 + (index % 3) * 0.07, 0.22 + (index % 2) * 0.08)
    piece = cube(f"Waste{index:02d}", (x0, y0, z0), size, WASTE_COLORS[index % len(WASTE_COLORS)], bevel=0.04)
    key(piece, 1 + index * 2, (x0, y0, z0), (1, 1, 1), (0.2 * index, 0.13 * index, 0.09 * index))
    chamber_loc = (-0.1 + (index % 4) * 0.62, -0.9 + (index % 4) * 0.55, 1.5 + (index // 4) * 0.58)
    key(piece, 65 + index, chamber_loc, (1, 1, 1), (0.1 * index, 0.05 * index, 0.08 * index))
    compact_loc = (2.55 + (index % 2) * 0.13, -0.82 + (index % 4) * 0.52, 1.4 + (index // 4) * 0.52)
    mid_loc = (1.15 + (index % 3) * 0.35, -0.9 + (index % 4) * 0.55, 1.48 + (index // 4) * 0.55)
    key(piece, 105, mid_loc, (0.75, 1.0, 0.95))
    key(piece, 132, compact_loc, (0.42, 0.95, 0.9))
    key(piece, 154, compact_loc, (0.18, 0.9, 0.85))
    key(piece, 164, compact_loc, (0.01, 0.01, 0.01))
    waste.append(piece)

# Finished bale emerges after compression.
bale = cube("Finished bale", (2.75, 0, 2.05), (0.95, 1.55, 1.12), BALE, bevel=0.04)
key(bale, 1, (2.75, 0, 2.05), (0.01, 0.01, 0.01))
key(bale, 126, (2.75, 0, 2.05), (0.12, 0.82, 0.72))
key(bale, 154, (2.75, 0, 2.05), (0.82, 1.0, 0.96))
key(bale, 164, (2.75, 0, 2.05), (1, 1, 1))
key(bale, 180, (2.75, 0, 2.05), (1, 1, 1))
key(bale, 230, (6.35, 0, 2.05), (1, 1, 1))
for offset in (-0.62, 0, 0.62):
    strap = cube(f"Strap{offset}", (2.75 + offset, -1.57, 2.05), (0.035, 0.035, 1.14), LIGHT_STEEL, bevel=0.01)
    key(strap, 1, (2.75 + offset, -1.57, 2.05), (0.01, 0.01, 0.01))
    key(strap, 164, (2.75 + offset, -1.57, 2.05), (1, 1, 1))
    key(strap, 180, (2.75 + offset, -1.57, 2.05), (1, 1, 1))
    key(strap, 230, (6.35 + offset, -1.57, 2.05), (1, 1, 1))

# The separate v005 ejector was removed. A single ram now exposes the causal sequence.
# Material identity markers remain attached visually to the same finished bale.
# They match the kraft / white plastic / cobalt blue / sparse red fingerprint from S01-S02.
identity_patches = [
    ("WhitePatchA", (2.48, -1.585, 2.42), (0.22, 0.025, 0.24), WASTE_COLORS[1]),
    ("WhitePatchB", (2.92, -1.585, 1.78), (0.28, 0.025, 0.18), WASTE_COLORS[1]),
    ("BlueIdentityPatch", (2.48, -1.59, 1.42), (0.24, 0.026, 0.20), WASTE_COLORS[0]),
    ("RedIdentityPatch", (3.34, -1.59, 2.18), (0.16, 0.026, 0.15), WASTE_COLORS[3]),
]
for name, loc, size, material in identity_patches:
    patch = cube(name, loc, size, material, bevel=0.025)
    key(patch, 1, loc, (0.01, 0.01, 0.01))
    key(patch, 154, loc, (0.82, 1.0, 0.96))
    key(patch, 164, loc, (1, 1, 1))
    key(patch, 180, loc, (1, 1, 1))
    key(patch, 230, (loc[0] + 3.6, loc[1], loc[2]), (1, 1, 1))
# Direction markers stay abstract so the vertical frame is not crowded with labels.
for x in (-6.8, -5.7, -4.6, -0.2, 0.9, 2.0, 4.7, 5.8):
    cube(f"Flow{x}", (x, -2.0, 0.08), (0.38, 0.06, 0.035), GREEN, bevel=0.02)

# Camera: continuous approach, cutaway orbit, then follow the bale.
bpy.ops.object.camera_add(location=(-8.0, -14.0, 7.5))
camera = bpy.context.object
camera.name = "Vertical camera"
camera.data.lens = 48
scene.camera = camera
key(camera, 1, (-8.0, -14.0, 7.5))
look_at(camera, (-5.0, 0, 2.5)); camera.keyframe_insert("rotation_euler", frame=1)
key(camera, 60, (5.8, -15.5, 8.5))
look_at(camera, (-0.8, 0, 2.45)); camera.keyframe_insert("rotation_euler", frame=60)
key(camera, 120, (7.3, -10.8, 6.3))
look_at(camera, (1.0, 0, 2.4)); camera.keyframe_insert("rotation_euler", frame=120)
key(camera, 180, (8.8, -13.0, 7.0))
look_at(camera, (3.2, 0, 2.2)); camera.keyframe_insert("rotation_euler", frame=180)
key(camera, 240, (10.8, -14.5, 7.8))
look_at(camera, (5.1, 0, 2.15)); camera.keyframe_insert("rotation_euler", frame=240)

# Smooth keyframes.
for obj in bpy.context.scene.objects:
    if obj.animation_data and obj.animation_data.action:
        for curve in obj.animation_data.action.fcurves:
            for point in curve.keyframe_points:
                point.interpolation = 'BEZIER'

# Stretch the established 10-second action contract to a 16-second review sample.
for animated in bpy.context.scene.objects:
    if animated.animation_data and animated.animation_data.action:
        for curve in animated.animation_data.action.fcurves:
            for point in curve.keyframe_points:
                point.co.x *= 1.6
                point.handle_left.x *= 1.6
                point.handle_right.x *= 1.6

# Deterministic one-dimensional interference audit for the contact surfaces.
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

# Save the editable source and render the 16-second vertical proxy.
bpy.ops.wm.save_as_mainfile(filepath=str(OUT / "jenailv-baler-concept-v006.blend"))
bpy.ops.render.render(animation=True)



