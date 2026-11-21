# Zone Edit : mur avant (cote tunnels) pour qu'on ne puisse pas sortir entre / au-dessus des
# tunnels. Du sol au toit, de mur lateral a mur lateral, avec seulement l'ouverture de chaque tunnel.
import unreal, traceback
TOOLS = r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools"
MAT_DIR = "/5622d7d7-d1ca-438f-8a48-1286a48e2471/Lobby/Materials"
FLOOR, ROOF = 1270.0, 2270.0          # tunnels remontes (sol 1270)
Y, T = -23321.0, 50.0                  # v3 : entree des tunnels a y = -23296
XL, XR = -2950.0, 2950.0               # faces interieures des murs lateraux
TUN_X, HALF, OPEN_H = [-1536.0, -512.0, 512.0, 1536.0], 256.0, 384.0
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
eal = unreal.EditorAssetLibrary
CUBE = eal.load_asset("/Engine/BasicShapes/Cube")
L = []

def box(label, m, x0, x1, z0, z1, y=Y, t=T, collision=True):
    a = eas.spawn_actor_from_class(unreal.FortStaticMeshActor, unreal.Vector((x0 + x1) / 2, y, (z0 + z1) / 2))
    c = a.get_component_by_class(unreal.StaticMeshComponent)
    c.set_static_mesh(CUBE); c.set_material(0, m)
    a.set_actor_scale3d(unreal.Vector((x1 - x0) / 100, t / 100, (z1 - z0) / 100))
    if not collision:
        c.set_collision_profile_name("NoCollision")
        c.set_editor_property("cast_shadow", False)
    a.set_actor_label("ZONE_EditWall_Front" + label)
    a.set_folder_path("Zones/Edit/Walls")
    a.set_editor_property("is_spatially_loaded", False)
    return a

try:
    for a in eas.get_all_level_actors():
        if a.get_actor_label().startswith("ZONE_EditWall_Front"):
            eas.destroy_actor(a)
    black = eal.load_asset(MAT_DIR + "/M_Lobby_BlackMatte")
    blue = eal.load_asset(MAT_DIR + "/M_Lobby_LedBlue")
    # bande du haut : au-dessus des ouvertures, jusqu'au toit
    box("Top", black, XL, XR, FLOOR + OPEN_H, ROOF)
    # morceaux entre les ouvertures
    edges = [XL]
    for x in TUN_X:
        edges += [x - HALF, x + HALF]
    edges.append(XR)
    for i in range(0, len(edges), 2):
        if edges[i + 1] - edges[i] > 1:
            box("Low%d" % (i // 2), black, edges[i], edges[i + 1], FLOOR, FLOOR + OPEN_H)
    # liseres LED cote interieur (comme les autres murs de la zone)
    yi = Y + T / 2 + 3
    box("LedHigh", blue, XL + 30, XR - 30, ROOF - 40, ROOF - 20, yi, 6, False)
    box("LedMid", blue, XL + 30, XR - 30, FLOOR + OPEN_H + 70, FLOOR + OPEN_H + 90, yi, 6, False)
    unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
    L.append("TERMINE : %d morceaux" % sum(1 for a in eas.get_all_level_actors() if a.get_actor_label().startswith("ZONE_EditWall_Front")))
except Exception:
    L.append(traceback.format_exc())
open(TOOLS + r"\edit_front_wall_log.txt", "w").write("\n".join(L))
