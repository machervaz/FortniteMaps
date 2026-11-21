# Repose les pieces des tunnels disparues (positions lues dans les autosaves UEFN de 20h05,
# avant la remontee de +118) : meme classe/position/rotation, + reset (Data Layer) + support force.
import unreal, traceback
TOOLS = r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools"
DZ = 118.0
CLS = "/Game/Building/ActorBlueprints/Player/Wood/L1/%s.%s_C"
FOLD = {"FACILE": "Facile", "MOYEN": "Moyen", "DIFFICILE": "Difficile", "IMPOSSIBLE": "Impossible"}
L = []
try:
    eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    dls = unreal.get_editor_subsystem(unreal.DataLayerEditorSubsystem)
    dl = unreal.load_asset("/5622d7d7-d1ca-438f-8a48-1286a48e2471/Tunnels/DL_TunnelBuilds")
    inst = [i for i in dls.get_all_data_layers() if i.get_asset() == dl][0]
    actors = eas.get_all_level_actors()
    labels = set(a.get_actor_label() for a in actors)
    wood = [(a.get_actor_location(), a.get_actor_label()) for a in actors if a.get_class().get_name().startswith(("PBWA_W1_Roof", "PBWA_W1_Stair"))]
    new = []
    for line in open(TOOLS + r"\lost_pieces.csv"):
        f = line.strip().split(";")
        if len(f) < 7 or not f[0].startswith("TUN_"):
            continue
        lab, cls = f[0], f[1]
        x, y, z, yaw = [float(v.replace(",", ".")) for v in f[2:6]]
        z += DZ
        if lab in labels:
            L.append("existe deja : " + lab); continue
        occ = [l for p, l in wood if abs(p.x - x) < 60 and abs(p.y - y) < 60 and abs(p.z - z) < 60]
        if occ:
            L.append("place occupee pour %s par %s" % (lab, occ[0])); continue
        a = eas.spawn_actor_from_class(unreal.load_class(None, CLS % (cls, cls)), unreal.Vector(x, y, z), unreal.Rotator(roll=0, pitch=0, yaw=yaw))
        a.set_actor_label(lab)
        a.set_folder_path("Zones/Edit/Tunnels/%s/Builds" % FOLD[lab.split("_")[1]])
        a.set_editor_property("is_spatially_loaded", False)
        a.set_editor_property("forcibly_structurally_supported", True)
        new.append(a)
        L.append("repose : %s (%.0f,%.0f,%.0f)" % (lab, x, y, z))
    if new:
        L.append("data layer : %s" % dls.add_actors_to_data_layer(new, inst))
    unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
    L.append("TERMINE : %d pieces reposees" % len(new))
except Exception:
    L.append(traceback.format_exc())
open(TOOLS + r"\restore_lost_log.txt", "w").write("\n".join(L))
