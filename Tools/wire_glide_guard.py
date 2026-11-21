import unreal, traceback
L = []
try:
    eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    ACT = {a.get_actor_label(): a for a in eas.get_all_level_actors()}
    s = ACT["AIM_Trainer"].get_editor_property("Script")
    s.get_editor_property("__verse_0x1567AB0E_GlideGuards").set_editor_property("SavedActor", ACT["AIM_Glide_Guard"])
    L.append("GlideGuards -> %s" % s.get_editor_property("__verse_0x1567AB0E_GlideGuards").get_editor_property("SavedActor").get_actor_label())
    unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
    L.append("TERMINE")
except Exception:
    L.append(traceback.format_exc())
open(r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools\wire_glide_guard_log.txt", "w").write("\n".join(L))
