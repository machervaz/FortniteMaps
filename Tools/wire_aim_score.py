import unreal
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
ACT = {a.get_actor_label(): a for a in eas.get_all_level_actors()}
s = ACT["AIM_Trainer"].get_editor_property("Script")
s.get_editor_property("__verse_0x7DEAE3A3_ScoreHUD").set_editor_property("SavedActor", ACT["AIM_ScoreHUD"])
unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
open(r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools\wire_aim_score_log.txt","w").write(s.get_editor_property("__verse_0x7DEAE3A3_ScoreHUD").get_editor_property("SavedActor").get_actor_label())
