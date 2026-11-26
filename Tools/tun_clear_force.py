import unreal, traceback
L = []
try:
    eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    dls = unreal.get_editor_subsystem(unreal.DataLayerEditorSubsystem)
    left = [a for a in eas.get_all_level_actors() if a.get_class().get_name().startswith("PBWA_") and -3500 < a.get_actor_location().x < 3500 and -48000 < a.get_actor_location().y < -22000]
    L.append("a supprimer : %d" % len(left))
    try:
        L.append("retire des data layers : %s" % dls.remove_actors_from_all_data_layers(left))
    except Exception as ex:
        L.append("data layers : %s" % ex)
    ok = 0
    for a in left:
        try:
            a.set_editor_property("forcibly_structurally_supported", False)
        except Exception:
            pass
        if eas.destroy_actor(a):
            ok += 1
    L.append("destroy ok : %d" % ok)
    if ok < len(left):
        rest = [a for a in left if unreal.SystemLibrary.is_valid(a)]
        L.append("destroy_actors groupe : %s" % eas.destroy_actors(rest))
    unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
    after = sum(1 for a in eas.get_all_level_actors() if a.get_class().get_name().startswith("PBWA_") and -3500 < a.get_actor_location().x < 3500 and -48000 < a.get_actor_location().y < -22000)
    L.append("restantes : %d" % after)
except Exception:
    L.append(traceback.format_exc())
open(r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools\tun_clear_force_log.txt", "w").write("\n".join(L))
