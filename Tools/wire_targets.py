import unreal, traceback
L = []
try:
    eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    ACT = {a.get_actor_label(): a for a in eas.get_all_level_actors()}
    s = ACT["AIM_Targets_Device"].get_editor_property("Script")
    W = unreal.load_class(None, "/CreativeCoreDevices/_Verse.shooting_range_target_device")
    objs = []
    for i in range(8):
        o = unreal.new_object(W, s); o.set_editor_property("SavedActor", ACT["AIM_Targets_Flick%d" % i]); objs.append(o)
    s.set_editor_property("__verse_0x19791D5E_FlickTargets", objs)
    for f, lab in (("__verse_0x40857CF0_FlickButton", "AIM_Targets_FlickButton"), ("__verse_0x582B71C0_TrackButton", "AIM_Targets_TrackButton"),
                   ("__verse_0xA01A74CD_Track", "AIM_Targets_Track"), ("__verse_0x74718EAE_Board", "AIM_Targets_Board"), ("__verse_0xA9350A44_HUD", "AIM_Targets_HUD")):
        s.get_editor_property(f).set_editor_property("SavedActor", ACT[lab])
        L.append("%s -> %s" % (f, lab))
    L.append("flicks %d" % len(s.get_editor_property("__verse_0x19791D5E_FlickTargets")))
    unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
    L.append("TERMINE")
except Exception:
    L.append(traceback.format_exc())
open(r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools\wire_targets_log.txt", "w").write("\n".join(L))
