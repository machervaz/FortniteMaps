import unreal, traceback
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
L = []
try:
    with unreal.ScopedEditorTransaction("1v1 : mur d'armes indestructible"):
        for a in eas.get_all_level_actors():
            p = a.get_actor_location(); n = a.get_class().get_name()
            if -22500 < p.x < -17500 and -2500 < p.y < 2500 and 1000 < p.z < 3500 and n in ("BP_ItemContainer_C", "CP_Glass_Floor_C"):
                a.modify()
                a.set_editor_property("bIsInvulnerable", True)
                a.set_editor_property("bCanBeDamaged", False)
                L.append("%s %s -> %s" % (a.get_actor_label(), n, a.get_editor_property("bIsInvulnerable")))
    unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
    L.append("TERMINE")
except Exception:
    L.append(traceback.format_exc())
open(r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools\wall_invuln_log.txt","w").write("\n".join(L))
