from pathlib import Path


PROJECT = Path(r"C:\Users\76797\Desktop\chatgpt\cinematic-lab\projects\jenailv-promo-pilot")
source_path = PROJECT / "tools" / "blender-baler-demo-v006.py"
target_path = PROJECT / "tools" / "blender-baler-demo-v007.py"
source = source_path.read_text(encoding="utf-8")

source = source.replace('"blender-demo-v006"', '"blender-demo-v007"')
source = source.replace('v006-720x1280.mp4', 'v007-720x1280.mp4')
source = source.replace('v006.blend', 'v007.blend')
source = source.replace('scene.frame_end = 384', 'scene.frame_end = 576')
source = source.replace('point.co.x *= 1.6', 'point.co.x *= 2.4')
source = source.replace('point.handle_left.x *= 1.6', 'point.handle_left.x *= 2.4')
source = source.replace('point.handle_right.x *= 1.6', 'point.handle_right.x *= 2.4')
source = source.replace('"version": "v006"', '"version": "v007"')
source = source.replace('mechanism-interference-audit-v006.json', 'mechanism-interference-audit-v007.json')
source = source.replace('"timing_before_1_6_scale"', '"timing_before_2_4_scale"')

# Remove the bright floor grid that made v006 read as a showroom/display table.
grid_start = source.index('# Floor and framing grid.')
grid_end = source.index('# Deterministic factory volume:', grid_start)
factory_floor = '''# Full-scale factory floor without a glowing presentation grid.
floor = cube("Factory concrete floor", (0, 0, -0.3), (15, 9, 0.2), CONCRETE, bevel=0)

'''
source = source[:grid_start] + factory_floor + source[grid_end:]

# Add roof trusses and distant production silhouettes behind the action plane.
insert_at = source.index('def area_light')
factory_depth = '''# Long factory aisle: all columns remain behind the machine action plane.
for y in (5.7, 8.4):
    for x in (-9.0, -4.5, 0.0, 4.5, 9.0):
        cube(f"AisleColumn{x}_{y}", (x, y, 4.8), (0.18, 0.18, 5.0), FACTORY_STEEL, bevel=0.025)
for y in (5.7, 8.4):
    for z in (6.8, 9.3):
        cube(f"AisleBeam{y}_{z}", (0, y, z), (11.5, 0.14, 0.14), FACTORY_STEEL, bevel=0.02)
for n, x in enumerate((-7.5, -2.5, 2.5, 7.5)):
    cube(f"DistantLine{n}", (x, 8.0, 1.0), (1.35, 0.8, 1.0), DARK_BLUE, bevel=0.05)

'''
source = source[:insert_at] + factory_depth + source[insert_at:]

camera_start = source.index('# Camera:')
camera_end = source.index('# Smooth keyframes.', camera_start)
camera_block = '''# Four motivated cameras create a film sequence instead of a single demo orbit.
def make_camera(name, location, target, lens):
    bpy.ops.object.camera_add(location=location)
    cam = bpy.context.object
    cam.name = name
    cam.data.lens = lens
    look_at(cam, target)
    return cam


cam_feed = make_camera("CAM A material follow", (-8.8, -6.4, 4.1), (-5.4, 0, 2.5), 52)
key(cam_feed, 1, (-8.8, -6.4, 4.1))
look_at(cam_feed, (-5.4, 0, 2.5)); cam_feed.keyframe_insert("rotation_euler", frame=1)
key(cam_feed, 96, (-4.9, -8.2, 4.9))
look_at(cam_feed, (-2.2, 0, 2.7)); cam_feed.keyframe_insert("rotation_euler", frame=96)

cam_hero = make_camera("CAM B factory reveal", (5.0, -23.0, 10.5), (-0.8, 0, 2.5), 40)
key(cam_hero, 97, (5.0, -23.0, 10.5))
look_at(cam_hero, (-0.8, 0, 2.5)); cam_hero.keyframe_insert("rotation_euler", frame=97)
key(cam_hero, 168, (3.0, -19.5, 8.6))
look_at(cam_hero, (0.2, 0, 2.4)); cam_hero.keyframe_insert("rotation_euler", frame=168)

cam_press = make_camera("CAM C compression side", (7.2, -10.5, 5.8), (1.0, 0, 2.3), 58)
key(cam_press, 169, (7.2, -10.5, 5.8))
look_at(cam_press, (0.5, 0, 2.4)); cam_press.keyframe_insert("rotation_euler", frame=169)
key(cam_press, 408, (8.2, -9.7, 5.2))
look_at(cam_press, (2.2, 0, 2.25)); cam_press.keyframe_insert("rotation_euler", frame=408)

cam_exit = make_camera("CAM D discharge follow", (10.0, -15.8, 7.4), (3.3, 0, 2.2), 48)
key(cam_exit, 409, (10.0, -15.8, 7.4))
look_at(cam_exit, (3.3, 0, 2.2)); cam_exit.keyframe_insert("rotation_euler", frame=409)
key(cam_exit, 576, (16.0, -16.8, 8.0))
look_at(cam_exit, (6.0, 0, 2.1)); cam_exit.keyframe_insert("rotation_euler", frame=576)

scene.camera = cam_feed
for frame, camera in ((1, cam_feed), (97, cam_hero), (169, cam_press), (409, cam_exit)):
    marker = scene.timeline_markers.new(f"CUT {camera.name}", frame=frame)
    marker.camera = camera

'''
source = source[:camera_start] + camera_block + source[camera_end:]

# The audit must be written before animation scaling, exactly as in v006.
target_path.write_text(source, encoding="utf-8")
print(target_path)
