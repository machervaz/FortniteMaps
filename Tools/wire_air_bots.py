import unreal, traceback
L = []
try:
    eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    ACT = {a.get_actor_label(): a for a in eas.get_all_level_actors()}
    s = ACT["BUILD_AirBots"].get_editor_property("Script")
    s.get_editor_property("__verse_0x45644DA3_Spawner").set_editor_property("SavedActor", ACT["BUILD_BotSpawner"])
    s.get_editor_property("__verse_0xDE5A3C79_ResetButton").set_editor_property("SavedActor", ACT["BUILD_ResetButton"])
    o = unreal.new_object(unreal.load_class(None, "/CreativeCoreDevices/_Verse.explosive_device"), s)
    o.set_editor_property("SavedActor", ACT["BUILD_ResetExp"])
    s.set_editor_property("__verse_0xBEE4D5D5_ResetExplosives", [o])
    L.append("spawner %s" % s.get_editor_property("__verse_0x45644DA3_Spawner").get_editor_property("SavedActor").get_actor_label())
    L.append("explosifs %d" % len(s.get_editor_property("__verse_0xBEE4D5D5_ResetExplosives")))
    left = [l for l in ACT if l.startswith("BUILD_")]
    L.append("restants BUILD_* : %s" % sorted(left))
    eas.set_selected_level_actors([ACT["LOBBY_Radio"]])
    unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
    L.append("TERMINE")
except Exception:
    L.append(traceback.format_exc())
open(r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools\wire_air_bots_log.txt", "w").write("\n".join(L))
