import unreal, traceback
ROOT = "/5622d7d7-d1ca-438f-8a48-1286a48e2471"
BB = "/Game/Creative/Devices/Billboard/BP_Creative_Billboard.BP_Creative_Billboard_C"
BTN = "/CreativeCoreDevices/Device_Button_V2.Device_Button_V2_C"
HUD = "/CreativeCoreDevices/Device_HUDMessage_V2.Device_HUDMessage_V2_C"
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
V = lambda x, y, z: unreal.Vector(float(x), float(y), float(z))
L = []
def find(label):
    r = [a for a in eas.get_all_level_actors() if a.get_actor_label() == label]
    return r[0] if r else None
def spawn(cls, label, loc, yaw=0.0):
    a = find(label)
    if a: return a
    a = eas.spawn_actor_from_class(unreal.load_class(None, cls), loc, unreal.Rotator(0, 0, yaw))
    a.set_actor_label(label); a.set_folder_path("Zones/1v1/Extras")
    a.set_editor_property("is_spatially_loaded", False)
    return a
def bb(label, loc, text, size):
    a = spawn(BB, label, loc, 90.0)
    a.set_editor_property("text", text); a.set_editor_property("TextSize", size)
    return a
try:
    bb("ZONE_1v1X_Score", V(-20390, 256, 2330), "SCORE", 26)
    spawn(BTN, "ZONE_1v1X_HealthButton", V(-18700, 700, 1536), 90.0)
    bb("ZONE_1v1X_HealthBoard", V(-18700, 700, 1760), "HEALTH : 100 / 100", 20)
    spawn(BTN, "ZONE_1v1X_ResetScoreButton", V(-18700, -700, 1536), 90.0)
    bb("ZONE_1v1X_ResetScoreTitle", V(-18700, -700, 1760), "RESET SCORE", 20)
    spawn(HUD, "ZONE_1v1X_CountdownHUD", V(-18000, 1500, 1100), 0.0)
    d = find("ZONE_1v1X_Device")
    if not d:
        d = eas.spawn_actor_from_object(unreal.load_object(None, ROOT + "/_Verse.arena_extras"), V(-18000, 1300, 1100))
        d.set_actor_label("ZONE_1v1X_Device"); d.set_folder_path("Zones/1v1/Extras")
    eas.set_selected_level_actors([d])
    L.append("OK %s" % d)
    unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
except Exception:
    L.append(traceback.format_exc())
open(r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools\build_arena_extras_log.txt", "w").write("\n".join(L))
