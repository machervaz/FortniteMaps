import unreal, traceback
ROOT = "/5622d7d7-d1ca-438f-8a48-1286a48e2471"
BB = "/Game/Creative/Devices/Billboard/BP_Creative_Billboard.BP_Creative_Billboard_C"
BTN = "/CreativeCoreDevices/Device_Button_V2.Device_Button_V2_C"
HUD = "/CreativeCoreDevices/Device_HUDMessage_V2.Device_HUDMessage_V2_C"
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
V = lambda x, y, z: unreal.Vector(float(x), float(y), float(z))
L = []
def spawn(cls, label, folder, loc, yaw=0.0):
    old = [a for a in eas.get_all_level_actors() if a.get_actor_label() == label]
    if old:
        return old[0]
    a = eas.spawn_actor_from_class(unreal.load_class(None, cls), loc, unreal.Rotator(0, 0, yaw))
    a.set_actor_label(label); a.set_folder_path(folder)
    a.set_editor_property("is_spatially_loaded", False)
    return a
def bb(label, folder, loc, yaw, text, size):
    a = spawn(BB, label, folder, loc, yaw)
    a.set_editor_property("text", text); a.set_editor_property("TextSize", size)
    return a
try:
    RULES = ["HOW TO PLAY",
             "EDIT  -  piece control courses : beat your time",
             "EDIT RACE  -  4 edit tunnels, from Easy to Impossible",
             "AIM  -  Launch, Bounce, Circuit, Double Pump, Tracking, Flicks",
             "1V1  -  buildfight : shoot the panel for speed, health, sky, RESET",
             "BUILD  -  90s / ramp rush and retakes against the clock",
             "Your records and stats are saved, even after you leave !"]
    for i, t in enumerate(RULES):
        bb("LOBBY_Rules%d" % i, "Lobby/Extras/Rules", V(-600, 1165, 2060 - i * 80 - (20 if i else 0)), 0.0, t, 30 if i == 0 else 18)
    bb("LOBBY_Global0", "Lobby/Extras/Global", V(-400, -1165, 2080), 180.0, "WORLD RECORDS", 22)
    for k in range(14):
        col, row = divmod(k, 7)
        bb("LOBBY_Global%d" % (k + 1), "Lobby/Extras/Global", V(-1100 + col * 1400, -1165, 1990 - row * 70), 180.0, "---", 16)
    spawn(BTN, "LOBBY_StatsButton", "Lobby/Extras/Stats", V(-1700, -1100, 1270), 0.0)
    bb("LOBBY_StatsTitle", "Lobby/Extras/Stats", V(-1700, -1165, 1560), 180.0, "MY STATS", 24)
    spawn(HUD, "LOBBY_StatsHUD", "Lobby/Extras/Stats", V(-1700, -900, 870), 0.0)
    if not [a for a in eas.get_all_level_actors() if a.get_actor_label() == "LOBBY_Extras"]:
        d = eas.spawn_actor_from_object(unreal.load_object(None, ROOT + "/_Verse.lobby_extras"), V(0, -600, 870))
        d.set_actor_label("LOBBY_Extras"); d.set_folder_path("Lobby/Extras")
    L.append("OK")
    unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
except Exception:
    L.append(traceback.format_exc())
open(r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools\build_lobby_extras_log.txt", "w").write("\n".join(L))
