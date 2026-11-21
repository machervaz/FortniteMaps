# Zone Piece Control (dans le ciel) : 4 vrais murs + toit + liseres LED + lumieres
# (StaticMesh : ni constructibles ni destructibles, le reset ne les touche pas)
import unreal, traceback
TOOLS = r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools"
MAT_DIR = "/5622d7d7-d1ca-438f-8a48-1286a48e2471/Lobby/Materials"
X0, X1, Y0, Y1 = 20700.0, 33600.0, -12050.0, -750.0
Z0, Z1, T = 4700.0, 15600.0, 60.0
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
eal = unreal.EditorAssetLibrary
CUBE = eal.load_asset("/Engine/BasicShapes/Cube")
V = lambda x, y, z: unreal.Vector(float(x), float(y), float(z))
L = []

def box(label, m, c, s, collision=True):
    a = eas.spawn_actor_from_class(unreal.FortStaticMeshActor, c)
    comp = a.get_component_by_class(unreal.StaticMeshComponent)
    comp.set_static_mesh(CUBE); comp.set_material(0, m)
    a.set_actor_scale3d(V(s.x / 100, s.y / 100, s.z / 100))
    if not collision:
        comp.set_collision_profile_name("NoCollision")
        comp.set_editor_property("cast_shadow", False)
    a.set_actor_label("ZONE_PCWall_" + label)
    a.set_folder_path("Zones/PieceControl/Enclosure")
    a.set_editor_property("is_spatially_loaded", False)
    return a

try:
    for a in eas.get_all_level_actors():
        if a.get_actor_label().startswith("ZONE_PCWall_"):
            eas.destroy_actor(a)
    wall = eal.load_asset(MAT_DIR + "/M_Aim_ArenaWall")
    led = eal.load_asset(MAT_DIR + "/M_Lobby_LedDeepBlue")
    W, D, H = X1 - X0, Y1 - Y0, Z1 - Z0
    cx, cy, cz = (X0 + X1) / 2, (Y0 + Y1) / 2, (Z0 + Z1) / 2
    box("N", wall, V(cx, Y1 + T / 2, cz), V(W + 2 * T, T, H))
    box("S", wall, V(cx, Y0 - T / 2, cz), V(W + 2 * T, T, H))
    box("E", wall, V(X1 + T / 2, cy, cz), V(T, D, H))
    box("W", wall, V(X0 - T / 2, cy, cz), V(T, D, H))
    box("Roof", wall, V(cx, cy, Z1 + T / 2), V(W + 2 * T, D + 2 * T, T))
    for nm, c, s in (("LedN", V(cx, Y1 - 6, Z1 - 12), V(W, 12, 24)), ("LedS", V(cx, Y0 + 6, Z1 - 12), V(W, 12, 24)),
                     ("LedE", V(X1 - 6, cy, Z1 - 12), V(12, D, 24)), ("LedW", V(X0 + 6, cy, Z1 - 12), V(12, D, 24))):
        box(nm, led, c, s, False)
    k = 0
    for fx in (0.2, 0.5, 0.8):
        for fy in (0.25, 0.75):
            pl = eas.spawn_actor_from_class(unreal.PointLight, V(X0 + fx * W, Y0 + fy * D, Z1 - 300))
            lc = pl.get_component_by_class(unreal.PointLightComponent)
            lc.set_light_color(unreal.LinearColor(0.85, 0.9, 1.0, 1)); lc.set_intensity(60.0); lc.set_attenuation_radius(9000.0)
            lc.set_editor_property("cast_shadows", False)
            pl.set_actor_label("ZONE_PCWall_Light%d" % k); pl.set_folder_path("Zones/PieceControl/Enclosure")
            pl.set_editor_property("is_spatially_loaded", False)
            k += 1
    unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
    L.append("TERMINE : murs %d x %d, hauteur %d (z %d -> %d)" % (W, D, H, Z0, Z1))
except Exception:
    L.append(traceback.format_exc())
open(TOOLS + r"\pc_walls_log.txt", "w").write("\n".join(L))
