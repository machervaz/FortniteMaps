# Tunnel EASY (FACILE) : ajoute un mur editable a l'entree et un cone editable sur une montee.
# Memes positions/rotations que build_tunnels.py (W au bord avant de la case, C au bord arriere),
# ajoutes au Data Layer du reset + support force. Ne pose rien si une piece est deja la.
import unreal, traceback
TOOLS = r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools"
X, Y0, CELL, FLOOR = -1536.0, -23296.0, 512.0, 1270.0
CLS = {"W": "/Game/Building/ActorBlueprints/Player/Wood/L1/PBWA_W1_Solid.PBWA_W1_Solid_C",
       "C": "/Game/Building/ActorBlueprints/Player/Wood/L1/PBWA_W1_RoofC.PBWA_W1_RoofC_C"}
yf = lambda k: Y0 - k * CELL
# FACILE : case 0 = entree (niveau 0), case 2 = premiere montee "U" (niveau 0 -> 1)
WANT = [("W", "TUN_FACILE_EntryWall", (X, yf(0), FLOOR)), ("C", "TUN_FACILE_ConeUp2", (X, yf(3), FLOOR))]
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
dls = unreal.get_editor_subsystem(unreal.DataLayerEditorSubsystem)
L = []
try:
    dl = unreal.load_asset("/5622d7d7-d1ca-438f-8a48-1286a48e2471/Tunnels/DL_TunnelBuilds")
    inst = [i for i in dls.get_all_data_layers() if i.get_asset() == dl][0]
    near = lambda p, q: abs(p.x - q[0]) < 60 and abs(p.y - q[1]) < 60 and abs(p.z - q[2]) < 60
    # ce qu'il y a deja autour
    for a in eas.get_all_level_actors():
        p = a.get_actor_location()
        if abs(p.x - X) < 400 and -25500 < p.y < -23000 and a.get_class().get_name().startswith("PBWA_"):
            L.append("existant : %s %s (%.0f,%.0f,%.0f) rot=%.0f" % (a.get_actor_label(), a.get_class().get_name(), p.x, p.y, p.z, a.get_actor_rotation().yaw))
    new = []
    for key, label, pos in WANT:
        cls_name = CLS[key].split(".")[-1]
        dup = [a for a in eas.get_all_level_actors() if a.get_class().get_name() == cls_name and near(a.get_actor_location(), pos)]
        if dup:
            L.append("deja present a %s : %s" % (str(pos), dup[0].get_actor_label()))
            continue
        a = eas.spawn_actor_from_class(unreal.load_class(None, CLS[key]), unreal.Vector(*pos))
        a.set_actor_label(label)
        a.set_folder_path("Zones/Edit/Tunnels/Facile/Builds")
        a.set_editor_property("is_spatially_loaded", False)
        a.set_editor_property("forcibly_structurally_supported", True)
        new.append(a)
        L.append("pose : %s a %s" % (label, str(pos)))
    if new:
        L.append("data layer : %s" % dls.add_actors_to_data_layer(new, inst))
    unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
    L.append("TERMINE")
except Exception:
    L.append(traceback.format_exc())
open(TOOLS + r"\easy_add_pieces_log.txt", "w").write("\n".join(L))
