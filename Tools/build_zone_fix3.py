import unreal
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
ACT = {a.get_actor_label(): a for a in eas.get_all_level_actors()}
L = []
with unreal.ScopedEditorTransaction("Zone BUILD : rebords des rampes"):
    for lab in ("BUILD_RampEdge-1", "BUILD_RampEdge1"):
        a = ACT[lab]
        a.modify()
        p = a.get_actor_location()
        a.set_actor_location(unreal.Vector(p.x, p.y - 512.0, p.z), False, False)
        o, e = a.get_actor_bounds(False)
        L.append("%s : y %.0f..%.0f" % (lab, o.y - e.y, o.y + e.y))
unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
open(r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools\build_zone_fix3_log.txt", "w").write("\n".join(L))
