import unreal, json
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
YAW = json.load(open(r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools\yaw_fix.json"))
L = []
with unreal.ScopedEditorTransaction("1v1 : orientation armes"):
    for a in eas.get_all_level_actors():
        lab = a.get_actor_label()
        if lab in YAW:
            a.modify(); r = YAW[lab]
            a.set_actor_rotation(unreal.Rotator(r[0], r[1], r[2]), False)
            L.append("%s %s" % (lab, r))
unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
open(r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools\yaw_fix_log.txt","w").write("\n".join(L))
