import unreal, traceback
ROOT = "/5622d7d7-d1ca-438f-8a48-1286a48e2471"
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
V = lambda x, y, z: unreal.Vector(float(x), float(y), float(z))
L = []
ACT = {a.get_actor_label(): a for a in eas.get_all_level_actors()}


def spawn(cls, label, loc, yaw=0.0):
    if label in ACT:
        return ACT[label]
    a = eas.spawn_actor_from_class(unreal.load_class(None, cls), loc, unreal.Rotator(0, 0, yaw))
    a.set_actor_label(label)
    a.set_folder_path("Lobby/Extras/Music")
    a.set_editor_property("is_spatially_loaded", False)
    ACT[label] = a
    return a


try:
    spawn("/CreativeCoreDevices/Device_Radio_V2.Device_Radio_V2_C", "LOBBY_Radio", V(0, 600, 870))
    spawn("/CreativeCoreDevices/Device_Button_V2.Device_Button_V2_C", "LOBBY_MusicButton", V(-1700, 1100, 1270), 180.0)
    t = spawn("/Game/Creative/Devices/Billboard/BP_Creative_Billboard.BP_Creative_Billboard_C", "LOBBY_MusicTitle", V(-1700, 1165, 1560), 0.0)
    t.set_editor_property("text", "MUSIC ON / OFF")
    t.set_editor_property("TextSize", 24)
    spawn("/CreativeCoreDevices/Device_HUDMessage_V2.Device_HUDMessage_V2_C", "LOBBY_MusicHUD", V(-1700, 900, 870))
    d = ACT.get("LOBBY_Ambiance")
    if not d:
        d = eas.spawn_actor_from_object(unreal.load_object(None, ROOT + "/_Verse.ambiance"), V(0, 800, 870))
        d.set_actor_label("LOBBY_Ambiance")
        d.set_folder_path("Lobby/Extras/Music")
    eas.set_selected_level_actors([d])
    unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
    L.append("OK")
except Exception:
    L.append(traceback.format_exc())
open(r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools\build_ambiance_log.txt", "w").write("\n".join(L))
