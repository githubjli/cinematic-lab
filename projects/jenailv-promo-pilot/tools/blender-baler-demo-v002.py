import bpy
import math
from pathlib import Path
from mathutils import Vector


PROJECT = Path(r"C:\Users\76797\Desktop\chatgpt\cinematic-lab\projects\jenailv-promo-pilot")
OUT = PROJECT / "outputs" / "blender-demo-v002"
OUT.mkdir(parents=True, exist_ok=True)

bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.frame_start = 1
scene.frame_end = 240
scene.render.fps = 24
scene.render.resolution_x = 720
scene.render.resolution_y = 1280
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = 'FFMPEG'
scene.render.ffmpeg.format = 'MPEG4'
scene.render.ffmpeg.codec = 'H264'
scene.render.ffmpeg.constant_rate_factor = 'MEDIUM'
scene.render.ffmpeg.ffmpeg_preset = 'GOOD'
scene.render.filepath = str(OUT / "jenailv-baler-concept-v002-720x1280.mp4")
scene.render.engine = 'BLENDER_WORKBENCH'
scene.display.shading.light = 'STUDIO'
scene.display.shading.studio_light = 'rim.sl'
scene.display.shading.color_type = 'MATERIAL'
scene.display.shading.show_shadows = True
scene.display.shading.show_cavity = True
scene.display.shading.cavity_type = 'BOTH'
scene.display.shading.curvature_ridge_factor = 1.7
scene.display.shading.curvature_valley_factor = 1.2
scene.render.film_transparent = False
scene.world = bpy.data.worlds.new("Industrial World")
scene.world.color = (0.012, 0.025, 0.045)


def mat(name, color):
    material = bpy.data.materials.new(name)
    material.diffuse_color = (*color, 1.0)
    return material


BLUE = mat("JNL Blue", (0.025, 0.22, 0.62))
DARK_BLUE = mat("Structure", (0.018, 0.07, 0.16))
YELLOW = mat("Safety", (0.95, 0.57, 0.04))
STEEL = mat("Steel", (0.34, 0.39, 0.45))
LIGHT_STEEL = mat("Rod", (0.68, 0.73, 0.78))
GREEN = mat("Flow", (0.25, 0.78, 0.36))
BALE = mat("Bale", (0.56, 0.46, 0.28))
WASTE_COLORS = [
    mat("Waste Blue", (0.08, 0.42, 0.82)),
    mat("Waste White", (0.78, 0.82, 0.85)),
    mat("Waste Kraft", (0.56, 0.36, 0.16)),
    mat("Waste Red", (0.72, 0.08, 0.06)),
]


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
cube("Floor", (0, 0, -0.3), (11, 7, 0.2), DARK_BLUE, bevel=0)
for x in range(-10, 11, 2):
    cube(f"GridX{x}", (x, 0, -0.08), (0.015, 7, 0.015), STEEL, bevel=0)
for y in range(-6, 7, 2):
    cube(f"GridY{y}", (0, y, -0.08), (11, 0.015, 0.015), STEEL, bevel=0)

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

# Hydraulic cylinder, rod, and platen. Near side stays open for cutaway view.
cylinder("Cylinder body", (-4.2, 0, 2.5), 0.54, 2.6, STEEL, (0, math.radians(90), 0))
rod = cylinder("Cylinder rod", (-2.4, 0, 2.5), 0.26, 2.8, LIGHT_STEEL, (0, math.radians(90), 0))
platen = cube("Compression platen", (-1.0, 0, 2.45), (0.24, 1.7, 1.45), YELLOW)
key(rod, 72, (-2.4, 0, 2.5), (1, 1, 1))
key(rod, 150, (0.0, 0, 2.5), (1.0, 1.0, 2.65))
key(platen, 72, (-1.0, 0, 2.45))
key(platen, 150, (2.15, 0, 2.45))

# Sliding exit gate.
gate = cube("Exit gate", (3.65, 0, 2.35), (0.18, 1.78, 1.5), BLUE)
key(gate, 125, (3.65, 0, 2.35))
key(gate, 165, (3.65, 0, 5.8))

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
    key(piece, 150, compact_loc, (0.22, 0.9, 0.85))
    key(piece, 156, compact_loc, (0.01, 0.01, 0.01))
    waste.append(piece)

# Finished bale emerges after compression.
bale = cube("Finished bale", (2.75, 0, 2.05), (0.95, 1.55, 1.12), BALE, bevel=0.04)
key(bale, 1, (2.75, 0, 2.05), (0.01, 0.01, 0.01))
key(bale, 150, (2.75, 0, 2.05), (0.01, 0.01, 0.01))
key(bale, 158, (2.75, 0, 2.05), (1, 1, 1))
key(bale, 222, (6.35, 0, 2.05), (1, 1, 1))
for offset in (-0.62, 0, 0.62):
    strap = cube(f"Strap{offset}", (2.75 + offset, -1.57, 2.05), (0.035, 0.035, 1.14), LIGHT_STEEL, bevel=0.01)
    key(strap, 1, (2.75 + offset, -1.57, 2.05), (0.01, 0.01, 0.01))
    key(strap, 158, (2.75 + offset, -1.57, 2.05), (1, 1, 1))
    key(strap, 222, (6.35 + offset, -1.57, 2.05), (1, 1, 1))

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

# Save the editable source and render the 10-second vertical proxy.
bpy.ops.wm.save_as_mainfile(filepath=str(OUT / "jenailv-baler-concept-v002.blend"))
bpy.ops.render.render(animation=True)
