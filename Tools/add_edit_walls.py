# Murs noirs + LED sur les cotes (et le fond, cote lobby) de la zone Edit, sous le toit.
# Le cote des tunnels reste ouvert. Relancable (supprime ZONE_EditWall*).
import unreal, traceback
OUT = r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools\add_edit_walls_log.txt"
ROOT = "/5622d7d7-d1ca-438f-8a48-1286a48e2471"
MAT_DIR = ROOT + "/Lobby/Materials"
FLOOR_Z, H = 1270.0, 1000.0          # le toit est a FLOOR_Z + 1000
X0, X1 = -2975.0, 2975.0             # murs lateraux (sur le bord du sol de la zone)
Y_BACK, Y_FRONT = -17025.0, -23800.0  # fond (cote lobby) -> bout du toit (cote tunnels)
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
eal = unreal.EditorAssetLibrary
CUBE = eal.load_asset("/Engine/BasicShapes/Cube")
BLACK, BLUE, WHITE = [eal.load_asset(MAT_DIR + "/" + n) for n in ("M_Lobby_BlackMatte", "M_Lobby_LedBlue", "M_Lobby_LedWhite")]
L = []

def box(label, mat, cx, cy, cz, sx, sy, sz, collision=True):
    a = eas.spawn_actor_from_class(unreal.FortStaticMeshActor, unreal.Vector(cx, cy, cz))
    c = a.get_component_by_class(unreal.StaticMeshComponent)
    c.set_static_mesh(CUBE)
    c.set_material(0, mat)
    a.set_actor_scale3d(unreal.Vector(sx / 100, sy / 100, sz / 100))
    if not collision:
        c.set_collision_profile_name("NoCollision")
        c.set_editor_property("cast_shadow", False)
    a.set_actor_label(label)
    a.set_folder_path("Zones/Edit/Walls")
    return a

try:
    for a in eas.get_all_level_actors():
        if a.get_actor_label().startswith("ZONE_EditWall"):
            eas.destroy_actor(a)
    length = abs(Y_FRONT - Y_BACK)
    yc = (Y_FRONT + Y_BACK) / 2
    # murs lateraux
    for sx, x in ((-1, X0), (1, X1)):
        box("ZONE_EditWall_Side%d" % sx, BLACK, x, yc, FLOOR_Z + H / 2, 50, length, H)
        xi = x - sx * 28                         # face interieure
        box("ZONE_EditWall_LedLow%d" % sx, BLUE, xi, yc, FLOOR_Z + 20, 6, length, 20, False)
        box("ZONE_EditWall_LedHigh%d" % sx, BLUE, xi, yc, FLOOR_Z + H - 30, 6, length, 20, False)
        for i in range(1, 6):
            y = Y_BACK - length * i / 6
            box("ZONE_EditWall_LedV%d_%d" % (sx, i), WHITE, xi, y, FLOOR_Z + H / 2, 6, 20, H - 100, False)
    # mur du fond (cote lobby)
    W = X1 - X0 + 50
    box("ZONE_EditWall_Back", BLACK, 0, Y_BACK, FLOOR_Z + H / 2, W, 50, H)
    box("ZONE_EditWall_BackLedLow", BLUE, 0, Y_BACK - 28, FLOOR_Z + 20, W - 60, 6, 20, False)
    box("ZONE_EditWall_BackLedHigh", BLUE, 0, Y_BACK - 28, FLOOR_Z + H - 30, W - 60, 6, 20, False)
    for i in range(1, 5):
        x = X0 + (X1 - X0) * i / 5
        box("ZONE_EditWall_BackLedV%d" % i, WHITE, x, Y_BACK - 28, FLOOR_Z + H / 2, 20, 6, H - 100, False)
    unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
    L.append("ok")
except Exception:
    L.append(traceback.format_exc())
open(OUT, "w").write("\n".join(L))
