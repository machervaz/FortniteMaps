import unreal, traceback, json
ROOT = "/5622d7d7-d1ca-438f-8a48-1286a48e2471"
BB = "/Game/Creative/Devices/Billboard/BP_Creative_Billboard.BP_Creative_Billboard_C"
BTN = "/CreativeCoreDevices/Device_Button_V2.Device_Button_V2_C"
HUD = "/CreativeCoreDevices/Device_HUDMessage_V2.Device_HUDMessage_V2_C"
TGT = "/Game/Creative/Devices/ShootingTargets/B_ShootingTarget_Master.B_ShootingTarget_Master_C"
TRK = "/Game/Creative/Devices/ShootingTargets/B_TargetTrack.B_TargetTrack_C"
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
V = lambda x, y, z: unreal.Vector(float(x), float(y), float(z))
F = "Zones/Aim/Targets"
L = []
ACT = {a.get_actor_label(): a for a in eas.get_all_level_actors()}
def mat_of(label):
    return ACT[label].get_component_by_class(unreal.StaticMeshComponent).get_material(0)
CUBE = unreal.EditorAssetLibrary.load_asset("/Engine/BasicShapes/Cube")
def box(label, mat, c, size, coll=True):
    if label in ACT: return ACT[label]
    a = eas.spawn_actor_from_class(unreal.FortStaticMeshActor, V(*c))
    cm = a.get_component_by_class(unreal.StaticMeshComponent); cm.set_static_mesh(CUBE); cm.set_material(0, mat)
    if not coll: cm.set_collision_profile_name("NoCollision")
    a.set_actor_scale3d(V(size[0] / 100.0, size[1] / 100.0, size[2] / 100.0))
    a.set_actor_label(label); a.set_folder_path(F); a.set_editor_property("is_spatially_loaded", False)
    ACT[label] = a
    return a
def spawn(cls, label, loc, yaw=0.0):
    if label in ACT: return ACT[label]
    a = eas.spawn_actor_from_class(unreal.load_class(None, cls), loc, unreal.Rotator(0, 0, yaw))
    a.set_actor_label(label); a.set_folder_path(F); a.set_editor_property("is_spatially_loaded", False)
    ACT[label] = a
    return a
def dup(src, label, dx, dy, dz=0.0):
    if label in ACT: return ACT[label]
    s = ACT[src]
    a = eas.duplicate_actor(s, None, V(0, 0, 0))
    p = s.get_actor_location(); a.set_actor_location(V(p.x + dx, p.y + dy, p.z + dz), False, False)
    a.set_actor_label(label); a.set_folder_path(F)
    ACT[label] = a
    return a
try:
    with unreal.ScopedEditorTransaction("Aim : salle TARGETS"):
        WALL, FLOOR, ROOF = mat_of("AIM_Pump_WallN"), mat_of("AIM_Pump_Floor"), mat_of("AIM_Pump_Roof")
        CX, CY, Z0, S, H = 0.0, 64000.0, 1270.0, 2400.0, 1100.0
        box("AIM_Targets_Floor", FLOOR, (CX, CY, Z0 - 25), (S + 120, S + 120, 50))
        box("AIM_Targets_Roof", ROOF, (CX, CY, Z0 + H + 30), (S + 120, S + 120, 60))
        box("AIM_Targets_WallN", WALL, (CX, CY + S / 2 + 30, Z0 + H / 2), (S + 120, 60, H))
        box("AIM_Targets_WallS", WALL, (CX, CY - S / 2 - 30, Z0 + H / 2), (S + 120, 60, H))
        box("AIM_Targets_WallE", WALL, (CX + S / 2 + 30, CY, Z0 + H / 2), (60, S, H))
        box("AIM_Targets_WallW", WALL, (CX - S / 2 - 30, CY, Z0 + H / 2), (60, S, H))
        arr = dup("AIM_Pump_Arrival", "AIM_Targets_Arrival", 0, CY - 1000 - 60000)
        # retour au hub : copie du cylindre "retour" de l'aim
        for part in ("Holo", "Socle", "Title", "Zone"):
            dup("ZONE_Aim_Return" + part, "AIM_Targets_Return" + part, 0, (CY - 700) - 17600)
        ACT["AIM_Targets_ReturnTitle"].set_editor_property("text", "BACK")
        # faille dans le hub (copie de la faille DOUBLE PUMP)
        for part in ("Core", "Edge", "Glow", "Title", "Zone"):
            dup("AIM_Hub_RiftPump_" + part, "AIM_Hub_RiftTargets_" + part, -2100, 1500)
        ACT["AIM_Hub_RiftTargets_Title"].set_editor_property("text", "TARGETS")
        # boutons + panneaux
        spawn(BTN, "AIM_Targets_FlickButton", V(-500, CY - 900, Z0), 0.0)
        bb = spawn(BB, "AIM_Targets_FlickTitle", V(-500, CY - 900, Z0 + 260), 180.0); bb.set_editor_property("text", "FLICKS (30 s)"); bb.set_editor_property("TextSize", 22)
        spawn(BTN, "AIM_Targets_TrackButton", V(500, CY - 900, Z0), 0.0)
        bb = spawn(BB, "AIM_Targets_TrackTitle", V(500, CY - 900, Z0 + 260), 180.0); bb.set_editor_property("text", "TRACKING (20 s)"); bb.set_editor_property("TextSize", 22)
        bb = spawn(BB, "AIM_Targets_Board", V(0, CY + S / 2 - 10, Z0 + 950), 0.0); bb.set_editor_property("text", "TARGETS"); bb.set_editor_property("TextSize", 26)
        spawn(HUD, "AIM_Targets_HUD", V(0, CY - 1100, Z0 - 300), 0.0)
        # cibles flicks : arc devant le joueur, hauteurs variees
        SPOTS = [(-1000, 64700, 1300), (-650, 65000, 1700), (-300, 64600, 1450), (0, 65050, 1900),
                 (300, 64650, 1350), (650, 64950, 1650), (1000, 64700, 1500), (0, 64300, 1300)]
        for i, (x, y, z) in enumerate(SPOTS):
            spawn(TGT, "AIM_Targets_Flick%d" % i, V(x, y, z), 0.0)
        spawn(TRK, "AIM_Targets_Track", V(-900, 64800, 1400), 0.0)
        d = ACT.get("AIM_Targets_Device")
        if not d:
            d = eas.spawn_actor_from_object(unreal.load_object(None, ROOT + "/_Verse.aim_targets"), V(0, CY - 1100, Z0 - 400))
            d.set_actor_label("AIM_Targets_Device"); d.set_folder_path(F)
    # failles : hub -> salle, retour -> hub
    M = json.load(open(r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools\build_aim_map.json"))
    for z, t in (("AIM_Hub_RiftTargets_Zone", "AIM_Targets_Arrival"), ("AIM_Targets_ReturnZone", "ZONE_Aim_Arrival")):
        if z not in M["rifts"]:
            M["rifts"].append(z); M["targets"].append(t)
    json.dump(M, open(r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools\build_aim_map.json", "w"), indent=1)
    unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
    L.append("OK")
except Exception:
    L.append(traceback.format_exc())
open(r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools\build_targets_log.txt", "w").write("\n".join(L))
