# Zone BUILD v2 : on vide les pistes (rush / 90s / retake), on pose 2 rampes comme en 1v1,
# un spawner de bots, un bouton RESET + explosif, et le device build_air_bots.
import unreal, traceback
ROOT = "/5622d7d7-d1ca-438f-8a48-1286a48e2471"
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
V = lambda x, y, z: unreal.Vector(float(x), float(y), float(z))
F = "Zones/Build"
L = []
KEEP = ("BUILD_Arrival", "BUILD_Floor", "BUILD_Title", "BUILD_Device")
try:
    ACT = {a.get_actor_label(): a for a in eas.get_all_level_actors()}
    with unreal.ScopedEditorTransaction("Zone BUILD v2"):
        # 1. on retire les pistes du classement global
        x = ACT["LOBBY_Extras"].get_editor_property("Script")
        courses = [c for c in x.get_editor_property("__verse_0x7CD715DA_Courses")
                   if not any(c == ACT[n].get_editor_property("Script") for n in ("BUILD_Rush_Chrono", "BUILD_Nineties_Chrono", "BUILD_Retake_Chrono") if n in ACT)]
        x.set_editor_property("__verse_0x7CD715DA_Courses", courses)
        W = unreal.load_class(None, "/CreativeCoreDevices/_Verse.billboard_device")
        boards = []
        for i in range(15):
            o = unreal.new_object(W, x)
            o.set_editor_property("SavedActor", ACT["LOBBY_Global%d" % i])
            boards.append(o)
        x.set_editor_property("__verse_0xDEDB56CB_GlobalBoard", boards)
        L.append("classement : %d parcours" % len(courses))
        # 2. suppression
        dead = [a for lab, a in ACT.items()
                if (lab.startswith("BUILD_") and lab not in KEEP and not lab.startswith("BUILD_Return") and not lab.startswith("BUILD_Led"))
                or lab in ("LOBBY_Global15", "LOBBY_Global16", "LOBBY_Global17")]
        n = sum(1 for a in dead if eas.destroy_actor(a))
        L.append("supprimes : %d / %d" % (n, len(dead)))
        ACT = {a.get_actor_label(): a for a in eas.get_all_level_actors()}
        # 3. deux rampes comme en 1v1 (copie, decalee sur le sol de la zone)
        DX, DY, DZ = 20000.0 + 19968.0, 25000.0 - 256.0, 1270.0 - 1536.0
        for lab in ("ZONE_1v1N_Ramp-1", "ZONE_1v1N_Ramp1", "ZONE_1v1N_RampEdge-1", "ZONE_1v1N_RampEdge1"):
            new = lab.replace("ZONE_1v1N_", "BUILD_")
            if new in ACT:
                continue
            s = ACT[lab]
            p = s.get_actor_location()
            a = eas.duplicate_actor(s, None, V(0, 0, 0))
            a.set_actor_location(V(p.x + DX, p.y + DY, p.z + DZ), False, False)
            a.set_actor_label(new)
            a.set_folder_path(F)
        # 4. spawner de bots, bouton reset, explosif
        if "BUILD_BotSpawner" not in ACT:
            a = eas.duplicate_actor(ACT["AIM_Launch_Spawner"], None, V(0, 0, 0))
            a.set_actor_location(V(20000, 28200, 1270), False, False)
            a.set_actor_label("BUILD_BotSpawner")
            a.set_folder_path(F)
        if "BUILD_ResetButton" not in ACT:
            a = eas.spawn_actor_from_class(unreal.load_class(None, "/CreativeCoreDevices/Device_Button_V2.Device_Button_V2_C"), V(21000, 22300, 1270), unreal.Rotator(0, 0, 0))
            a.set_actor_label("BUILD_ResetButton")
            a.set_folder_path(F)
            a.set_editor_property("is_spatially_loaded", False)
        if "BUILD_ResetTitle" not in ACT:
            a = eas.spawn_actor_from_class(unreal.load_class(None, "/Game/Creative/Devices/Billboard/BP_Creative_Billboard.BP_Creative_Billboard_C"), V(21000, 22350, 1560), unreal.Rotator(0, 0, 0))
            a.set_actor_label("BUILD_ResetTitle")
            a.set_folder_path(F)
            a.set_editor_property("text", "RESET BUILDS")
            a.set_editor_property("TextSize", 22)
        if "BUILD_ResetExp" not in ACT:
            a = eas.duplicate_actor(ACT["ZONE_1v1P_ResetExp_G0_PX"], None, V(0, 0, 0))
            a.set_actor_location(V(20000, 25000, 3000), False, False)
            a.set_actor_label("BUILD_ResetExp")
            a.set_folder_path(F)
        ACT["BUILD_Title"].set_editor_property("text", "BUILD  -  full piece the bots in the air")
        ACT["BUILD_Title"].set_editor_property("TextSize", 30)
        ACT["LOBBY_Rules5"].set_editor_property("text", "BUILD  -  full piece the bots floating above the ramps")
        # 5. device
        d = ACT.get("BUILD_AirBots")
        if not d:
            d = eas.spawn_actor_from_object(unreal.load_object(None, ROOT + "/_Verse.build_air_bots"), V(20000, 22600, 870))
            d.set_actor_label("BUILD_AirBots")
            d.set_folder_path(F)
        eas.set_selected_level_actors([d])
    unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
    L.append("OK")
except Exception:
    L.append(traceback.format_exc())
open(r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools\build_zone_v2_log.txt", "w").write("\n".join(L))
