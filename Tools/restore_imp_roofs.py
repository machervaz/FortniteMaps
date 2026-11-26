# Repose les toits (cones/pentes) du tunnel IMPOSSIBLE releves le 19/11 qui ont disparu
import unreal, traceback
TOOLS = r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools"
P = "/Game/Building/ActorBlueprints/Player/Wood/L1/%s.%s"
L = []
try:
    eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    dls = unreal.get_editor_subsystem(unreal.DataLayerEditorSubsystem)
    dl = unreal.load_asset("/5622d7d7-d1ca-438f-8a48-1286a48e2471/Tunnels/DL_TunnelBuilds")
    inst = [i for i in dls.get_all_data_layers() if i.get_asset() == dl][0]
    roofs = [(a.get_actor_location(), a.get_actor_label()) for a in eas.get_all_level_actors() if a.get_class().get_name().startswith("PBWA_W1_Roof")]
    new = []
    for line in open(TOOLS + r"\imp_roofs_ref.csv"):
        lab, cls, x, y, z, yaw = line.strip().split(";")
        x, y, z, yaw = float(x), float(y), float(z), float(yaw)
        if any(abs(p.x - x) < 60 and abs(p.y - y) < 60 and abs(p.z - z) < 60 for p, l in roofs):
            continue
        base = cls[:-2]  # PBWA_W1_RoofC
        a = eas.spawn_actor_from_class(unreal.load_class(None, P % (base, cls)), unreal.Vector(x, y, z), unreal.Rotator(roll=0, pitch=0, yaw=yaw))
        a.set_actor_label(lab); a.set_folder_path("Zones/Edit/Tunnels/Impossible/Builds")
        a.set_editor_property("is_spatially_loaded", False)
        a.set_editor_property("forcibly_structurally_supported", True)
        new.append(a); roofs.append((unreal.Vector(x, y, z), lab))
        L.append("repose %s %s (%.0f,%.0f,%.0f) yaw %.0f" % (lab, cls, x, y, z, yaw))
    if new:
        L.append("ajout au reset : %s" % dls.add_actors_to_data_layer(new, inst))
    unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
    L.append("TERMINE : %d toits reposes" % len(new))
except Exception:
    L.append(traceback.format_exc())
open(TOOLS + r"\restore_imp_roofs_log.txt", "w").write("\n".join(L))
