import unreal, traceback
L = []
try:
    eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    ACT = {a.get_actor_label(): a for a in eas.get_all_level_actors()}
    s = ACT["BUILD_Device"].get_editor_property("Script")
    for f, lab in (("__verse_0xC40A24B1_EntryZone", "LOBBY_Zone_Build"), ("__verse_0x2E1810D5_Arrival", "BUILD_Arrival"),
                   ("__verse_0x11C253F9_ReturnZone", "BUILD_ReturnZone"), ("__verse_0x204CC60D_LobbyPoint", "LOBBY_BuildReturnPoint"),
                   ("__verse_0xC08A223F_BuildClass", "ZONE_1v1_Speed0_ClassSelector")):
        s.get_editor_property(f).set_editor_property("SavedActor", ACT[lab])
        L.append("%s -> %s" % (f, lab))
    # classement global : 3 parcours de plus
    x = ACT["LOBBY_Extras"].get_editor_property("Script")
    courses = list(x.get_editor_property("__verse_0x7CD715DA_Courses"))
    have = set(c.get_outer().get_actor_label() if hasattr(c.get_outer(), "get_actor_label") else "" for c in courses)
    for n in ("BUILD_Rush_Chrono", "BUILD_Nineties_Chrono", "BUILD_Retake_Chrono"):
        if n not in have:
            courses.append(ACT[n].get_editor_property("Script"))
    x.set_editor_property("__verse_0x7CD715DA_Courses", courses)
    W = unreal.load_class(None, "/CreativeCoreDevices/_Verse.billboard_device")
    boards = []
    for i in range(18):
        o = unreal.new_object(W, x)
        o.set_editor_property("SavedActor", ACT["LOBBY_Global%d" % i])
        boards.append(o)
    x.set_editor_property("__verse_0xDEDB56CB_GlobalBoard", boards)
    L.append("courses %d boards %d" % (len(x.get_editor_property("__verse_0x7CD715DA_Courses")), len(boards)))
    unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
    L.append("TERMINE")
except Exception:
    L.append(traceback.format_exc())
open(r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools\wire_buildzone_log.txt", "w").write("\n".join(L))
