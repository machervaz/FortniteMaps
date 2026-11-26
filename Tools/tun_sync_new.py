# Nouvelles pieces dans les tunnels : support force, toujours chargees, bois -> reset
import unreal, traceback
L = []
try:
    eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    dls = unreal.get_editor_subsystem(unreal.DataLayerEditorSubsystem)
    dl = unreal.load_asset("/5622d7d7-d1ca-438f-8a48-1286a48e2471/Tunnels/DL_TunnelBuilds")
    inst = [i for i in dls.get_all_data_layers() if i.get_asset() == dl][0]
    wood = []
    for a in eas.get_all_level_actors():
        p = a.get_actor_location()
        if a.get_class().get_name().startswith("PBWA_") and -3200 < p.x < 3200 and -47700 < p.y < -16000 and p.z > -10000:
            a.modify()
            a.set_editor_property("forcibly_structurally_supported", True)
            a.set_editor_property("is_spatially_loaded", False)
            wood.append(a)
    L.append("bois tunnels : %d, ajout reset : %s" % (len(wood), dls.add_actors_to_data_layer(wood, inst)))
    unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
    L.append("TERMINE")
except Exception:
    L.append(traceback.format_exc())
open(r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools\tun_sync_new_log.txt", "w").write("\n".join(L))
