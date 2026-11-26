import unreal, traceback
L = []
try:
    eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    ACT = {a.get_actor_label(): a for a in eas.get_all_level_actors()}
    s = ACT["LOBBY_Extras"].get_editor_property("Script")
    ORDER = ["TUN_FACILE", "TUN_MOYEN", "TUN_DIFFICILE", "TUN_IMPOSSIBLE", "PCX_Couloir1", "PCX_Couloir2", "PCX_Couloir3",
             "PCX_Montee1", "PCX_Montee2", "PCX_Montee3", "PCX_Montee4", "PCX_Descente1", "PCX_Descente2", "PCX_Descente3"]
    s.set_editor_property("__verse_0x7CD715DA_Courses", [ACT[n + "_Chrono"].get_editor_property("Script") for n in ORDER])
    BBW = unreal.load_class(None, "/CreativeCoreDevices/_Verse.billboard_device")
    boards = []
    for i in range(15):
        o = unreal.new_object(BBW, s); o.set_editor_property("SavedActor", ACT["LOBBY_Global%d" % i]); boards.append(o)
    s.set_editor_property("__verse_0xDEDB56CB_GlobalBoard", boards)
    s.get_editor_property("__verse_0x22A6ECF0_StatsButton").set_editor_property("SavedActor", ACT["LOBBY_StatsButton"])
    s.get_editor_property("__verse_0xBF6C10EF_StatsHUD").set_editor_property("SavedActor", ACT["LOBBY_StatsHUD"])
    L.append("courses %d boards %d" % (len(s.get_editor_property("__verse_0x7CD715DA_Courses")), len(s.get_editor_property("__verse_0xDEDB56CB_GlobalBoard"))))
    unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
    L.append("TERMINE")
except Exception:
    L.append(traceback.format_exc())
open(r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools\wire_lobby_extras_log.txt", "w").write("\n".join(L))
