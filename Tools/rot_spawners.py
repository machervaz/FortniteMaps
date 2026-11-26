import unreal
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
L = []
with unreal.ScopedEditorTransaction("1v1 : armes alignees au mur"):
    for a in eas.get_all_level_actors():
        if a.get_actor_label().startswith("ZONE_1v1_Arme"):
            a.modify()
            a.set_actor_rotation(unreal.Rotator(0, 0, 90), False)
            r = a.get_actor_rotation(); L.append("%s yaw=%.0f" % (a.get_actor_label(), r.yaw))
unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
open(r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools\rot_spawners_log.txt","w").write("\n".join(L))
