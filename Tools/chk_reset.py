import unreal
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
a = [x for x in eas.get_all_level_actors() if x.get_actor_label() == "ZONE_1v1P_PanelDevice"][0]
v = a.get_editor_property("Script").get_editor_property("__verse_0xBEE4D5D5_ResetExplosives")
unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
open(r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools\chk_reset_log.txt","w").write("%d %s" % (len(v), [x.get_editor_property("SavedActor").get_actor_label() if x.get_editor_property("SavedActor") else None for x in v][:3]))
