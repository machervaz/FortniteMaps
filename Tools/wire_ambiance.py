import unreal, traceback
L = []
try:
    eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    ACT = {a.get_actor_label(): a for a in eas.get_all_level_actors()}
    s = ACT["LOBBY_Ambiance"].get_editor_property("Script")
    o = unreal.new_object(unreal.load_class(None, "/CreativeCoreDevices/_Verse.radio_device"), s)
    o.set_editor_property("SavedActor", ACT["LOBBY_Radio"])
    s.set_editor_property("__verse_0x0062E441_Radios", [o])
    s.get_editor_property("__verse_0x41B5EB93_MusicButton").set_editor_property("SavedActor", ACT["LOBBY_MusicButton"])
    s.get_editor_property("__verse_0x04FC474F_MusicHUD").set_editor_property("SavedActor", ACT["LOBBY_MusicHUD"])
    L.append("radios %d" % len(s.get_editor_property("__verse_0x0062E441_Radios")))
    eas.set_selected_level_actors([ACT["LOBBY_Radio"]])
    unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
    L.append("TERMINE")
except Exception:
    L.append(traceback.format_exc())
open(r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools\wire_ambiance_log.txt", "w").write("\n".join(L))
