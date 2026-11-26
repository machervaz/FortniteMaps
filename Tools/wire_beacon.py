import unreal
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
ACT = {a.get_actor_label(): a for a in eas.get_all_level_actors()}
s = ACT["BUILD_AirBots"].get_editor_property("Script")
s.get_editor_property("__verse_0x099B0D77_Indicator").set_editor_property("SavedActor", ACT["BUILD_BotBeacon"])
eas.set_selected_level_actors([ACT["BUILD_BotBeacon"]])
unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
open(r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools\wire_beacon_log.txt", "w").write(
    s.get_editor_property("__verse_0x099B0D77_Indicator").get_editor_property("SavedActor").get_actor_label())
