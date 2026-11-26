import unreal, traceback
L = []
try:
    eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    ACT = {a.get_actor_label(): a for a in eas.get_all_level_actors()}
    s = ACT["ZONE_1v1X_Device"].get_editor_property("Script")
    for f, lab in (("__verse_0xBB2BEDDA_ScoreBoard", "ZONE_1v1X_Score"), ("__verse_0xAF5B3348_ResetScoreButton", "ZONE_1v1X_ResetScoreButton"),
                   ("__verse_0x3EC300EF_HealthButton", "ZONE_1v1X_HealthButton"), ("__verse_0x46878924_HealthBoard", "ZONE_1v1X_HealthBoard"),
                   ("__verse_0xCE13F6CA_ArrivalPoint", "ZONE_1v1_Arrival"), ("__verse_0x5060C149_CountdownHUD", "ZONE_1v1X_CountdownHUD")):
        s.get_editor_property(f).set_editor_property("SavedActor", ACT[lab])
        L.append("%s -> %s" % (f, s.get_editor_property(f).get_editor_property("SavedActor").get_actor_label()))
    unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
    L.append("TERMINE")
except Exception:
    L.append(traceback.format_exc())
open(r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools\wire_arena_extras_log.txt", "w").write("\n".join(L))
