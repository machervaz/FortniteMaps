import unreal, traceback
L = []
try:
    eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    dls = unreal.get_editor_subsystem(unreal.DataLayerEditorSubsystem)
    left = [a for a in eas.get_all_level_actors() if a.get_class().get_name().startswith("PBWA_") and -3500 < a.get_actor_location().x < 3500 and -48000 < a.get_actor_location().y < -22000]
    dls.remove_actors_from_all_data_layers(left)
    with unreal.ScopedEditorTransaction("Pieces enterrees"):
        for a in left:
            a.modify()
            for c in a.get_components_by_class(unreal.SceneComponent):
                c.modify()
            p = a.get_actor_location()
            a.set_actor_location(unreal.Vector(p.x, p.y, -50000.0), False, False)
            a.set_actor_hidden_in_game(True)
            a.set_folder_path("Zones/Edit/Tunnels/Enterrees")
    unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
    after = sum(1 for a in eas.get_all_level_actors() if a.get_class().get_name().startswith("PBWA_") and -3500 < a.get_actor_location().x < 3500 and -48000 < a.get_actor_location().y < -22000 and a.get_actor_location().z > -1000)
    L.append("enterrees : %d, restantes dans les tunnels : %d" % (len(left), after))
except Exception:
    L.append(traceback.format_exc())
open(r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools\tun_bury_left_log.txt", "w").write("\n".join(L))
