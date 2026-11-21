import unreal, traceback
L = []
try:
    eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    n = 0
    with unreal.ScopedEditorTransaction("PC zones sans VFX"):
        for a in eas.get_all_level_actors():
            lab = a.get_actor_label()
            if lab.startswith("PCX_") and (lab.endswith("_Start") or lab.endswith("_Finish")):
                a.modify()
                for pn, v in (("EnableVFX", False), ("ZoneVisibleDuringGame", False)):
                    try:
                        a.set_editor_property(pn, v)
                    except Exception as ex:
                        L.append("%s %s : %s" % (lab, pn, ex))
                n += 1
    unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
    L.append("zones : %d" % n)
except Exception:
    L.append(traceback.format_exc())
open(r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools\pc_zone_vfx_log.txt", "w").write("\n".join(L[:20]))
