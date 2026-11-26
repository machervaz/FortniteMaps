import unreal, traceback
F = "__verse_0xBEE4D5D5_ResetExplosives"
W = "/CreativeCoreDevices/_Verse.explosive_device"
L = []
try:
    eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    ACT = {a.get_actor_label(): a for a in eas.get_all_level_actors()}
    s = ACT["ZONE_1v1P_PanelDevice"].get_editor_property("Script")
    objs = []
    for g in range(3):
        for k in ("PX", "NX", "PY", "NY", "PZ", "NZ"):
            o = unreal.new_object(unreal.load_class(None, W), s)
            o.set_editor_property("SavedActor", ACT["ZONE_1v1P_ResetExp_G%d_%s" % (g, k)])
            objs.append(o)
    s.set_editor_property(F, objs)
    L.append("ResetExplosives -> %s" % [x.get_editor_property("SavedActor").get_actor_label() for x in s.get_editor_property(F)])
    unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
    L.append("TERMINE")
except Exception:
    L.append(traceback.format_exc())
open(r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools\wire_reset_exp_log.txt", "w").write("\n".join(L))
