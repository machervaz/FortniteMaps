import unreal, traceback
ROOT = "/5622d7d7-d1ca-438f-8a48-1286a48e2471"
BB = "/Game/Creative/Devices/Billboard/BP_Creative_Billboard.BP_Creative_Billboard_C"
HUD = "/CreativeCoreDevices/Device_HUDMessage_V2.Device_HUDMessage_V2_C"
P = "/Game/Building/ActorBlueprints/Player/Wood/L1/%s.%s_C"
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
dls = unreal.get_editor_subsystem(unreal.DataLayerEditorSubsystem)
V = lambda x, y, z: unreal.Vector(float(x), float(y), float(z))
F = "Zones/Build"
L = []
ACT = {a.get_actor_label(): a for a in eas.get_all_level_actors()}
CUBE = unreal.EditorAssetLibrary.load_asset("/Engine/BasicShapes/Cube")
MAT = lambda n: unreal.EditorAssetLibrary.load_asset(ROOT + "/Lobby/Materials/" + n)


def reg(a, label, folder=F):
    a.set_actor_label(label)
    a.set_folder_path(folder)
    try:
        a.set_editor_property("is_spatially_loaded", False)
    except Exception:
        pass
    ACT[label] = a
    return a


def box(label, mat, c, size, coll=True, folder=F):
    if label in ACT:
        return ACT[label]
    a = eas.spawn_actor_from_class(unreal.FortStaticMeshActor, V(*c))
    cm = a.get_component_by_class(unreal.StaticMeshComponent)
    cm.set_static_mesh(CUBE)
    cm.set_material(0, mat)
    if not coll:
        cm.set_collision_profile_name("NoCollision")
        cm.set_editor_property("cast_shadow", False)
    a.set_actor_scale3d(V(size[0] / 100.0, size[1] / 100.0, size[2] / 100.0))
    return reg(a, label, folder)


def dup(src, label, loc=None, yaw=None, folder=F):
    if label in ACT:
        return ACT[label]
    s = ACT[src]
    a = eas.duplicate_actor(s, None, V(0, 0, 0))
    if loc is not None:
        a.set_actor_location(loc, False, False)
    if yaw is not None:
        r = s.get_actor_rotation()
        a.set_actor_rotation(unreal.Rotator(r.roll, r.pitch, yaw), False)
    return reg(a, label, folder)


def spawn(cls, label, loc, yaw=0.0, folder=F):
    if label in ACT:
        return ACT[label]
    a = eas.spawn_actor_from_class(unreal.load_class(None, cls), loc, unreal.Rotator(0, 0, yaw))
    return reg(a, label, folder)


def bb(label, loc, text, size, yaw=0.0, folder=F):
    a = spawn(BB, label, loc, yaw, folder)
    a.set_editor_property("text", text)
    a.set_editor_property("TextSize", size)
    return a


CH = {"start": "__verse_0x5CFF7AE4_StartTrigger", "finish": "__verse_0x16E5C556_FinishTrigger", "hud": "__verse_0xD5F0BE43_ResultHUD",
      "ret": "__verse_0xCB8B8794_ReturnPoint", "label": "__verse_0xBC955082_CourseLabel", "exp": "__verse_0xBEE4D5D5_ResetExplosives",
      "seq": "__verse_0x00B9F17C_ResetSequences"}
WR = {"prop": "/VerseDevices/_Verse/VNI/VerseDevices.Devices_creative_prop", "exp": "/CreativeCoreDevices/_Verse.explosive_device",
      "seq": "/CRD_CinematicSequence/_Verse.cinematic_sequence_device"}


def wrap(kind, outer, actor):
    o = unreal.new_object(unreal.load_class(None, WR[kind]), outer)
    o.set_editor_property("SavedActor", actor)
    return o


try:
    with unreal.ScopedEditorTransaction("Zone BUILD"):
        GLOSS, LED = MAT("M_Lobby_BlackGloss"), MAT("M_Lobby_LedBlue")
        CX, CY, Z0 = 20000.0, 25000.0, 1270.0
        box("BUILD_Floor", GLOSS, (CX, CY, Z0 - 25), (13000, 7000, 50))
        for sx in (-1, 1):
            box("BUILD_LedX%d" % sx, LED, (CX + sx * 6490, CY, Z0 + 1), (20, 7000, 2), False)
            box("BUILD_LedY%d" % sx, LED, (CX, CY + sx * 3490, Z0 + 1), (13000, 20, 2), False)
        tun_start = ACT["TUN_FACILE_Chrono"].get_editor_property("Script").get_editor_property(CH["start"]).get_editor_property("SavedActor")
        dup("ZONE_Aim_Arrival", "BUILD_Arrival", V(CX, 22300, 1275))
        dup("ZONE_Aim_Arrival", "LOBBY_BuildReturnPoint", V(0, 0, 1275), folder="Lobby/Extras")
        for part in ("Holo", "Socle", "Title", "Zone"):
            s = ACT["ZONE_Aim_Return" + part]
            p = s.get_actor_location()
            dup("ZONE_Aim_Return" + part, "BUILD_Return" + part, V(p.x + 900 + 1500, p.y - 17600 + 22300, p.z))
        ACT["BUILD_ReturnTitle"].set_editor_property("text", "LOBBY")
        bb("BUILD_Title", V(CX, 22000, 2300), "BUILD", 60, 0.0)
        LANES = [("Rush", 15, 16000.0, 10), ("Nineties", 16, 20000.0, 10), ("Retake", 17, 24000.0, 3)]
        TEXT = {"Rush": "RAMP RUSH  -  build ramps up to the blue line",
                "Nineties": "90s  -  climb with 90s up to the blue line",
                "Retake": "RETAKE  -  take the top of the wooden box"}
        for key, label, X, levels in LANES:
            fold = F + "/" + key
            pad = dup("ZONE_Aim_Arrival", "BUILD_%s_Pad" % key, V(X, 23400, 1275), folder=fold)
            st = dup(tun_start.get_actor_label(), "BUILD_%s_Start" % key, V(X, 23400, Z0 + 300), folder=fold)
            st.set_actor_scale3d(V(0.35, 0.35, 1.0))
            goal = Z0 + levels * 384.0
            fin = dup(tun_start.get_actor_label(), "BUILD_%s_Finish" % key, folder=fold)
            if key == "Retake":
                fin.set_actor_location(V(X, 25000, goal + 200), False, False)
                fin.set_actor_scale3d(V(0.6, 0.6, 0.6))
            else:
                fin.set_actor_location(V(X, 25300, goal + 150), False, False)
                fin.set_actor_scale3d(V(3.4, 5.0, 0.5))
                for sx in (-1, 1):
                    box("BUILD_%s_GoalX%d" % (key, sx), LED, (X + sx * 1300, 25300, goal), (20, 3800, 20), False, fold)
                    box("BUILD_%s_GoalY%d" % (key, sx), LED, (X, 25300 + sx * 1900, goal), (2600, 20, 20), False, fold)
            bb("BUILD_%s_Title" % key, V(X, 23900, 1900), TEXT[key], 22, 0.0, fold)
            hud = spawn(HUD, "BUILD_%s_HUD" % key, V(X, 23000, 900), 0.0, fold)
            exp = dup("ZONE_1v1P_ResetExp_G0_PX", "BUILD_%s_Exp" % key, V(X, 25300, 2200 if key == "Retake" else 3300), folder=fold)
            exp.set_editor_property("Blast Radius", 4.0 if key == "Retake" else 6.0)
            ch = ACT.get("BUILD_%s_Chrono" % key)
            if not ch:
                ch = eas.spawn_actor_from_object(unreal.load_object(None, ROOT + "/_Verse.chrono_course"), V(X, 23000, 870))
                reg(ch, "BUILD_%s_Chrono" % key, fold)
            s = ch.get_editor_property("Script")
            s.set_editor_property(CH["label"], label)
            s.get_editor_property(CH["start"]).set_editor_property("SavedActor", st)
            s.get_editor_property(CH["finish"]).set_editor_property("SavedActor", fin)
            s.get_editor_property(CH["hud"]).set_editor_property("SavedActor", hud)
            s.set_editor_property(CH["ret"], [wrap("prop", s, pad)])
            s.set_editor_property(CH["exp"], [wrap("exp", s, exp)])
            if key == "Retake":
                s.set_editor_property(CH["seq"], [wrap("seq", s, ACT["PCX_ReloadSequence"])])
            L.append("piste %s ok" % key)
        # tour en bois a reprendre (rechargee par la sequence du Piece Control)
        dl = unreal.load_asset(ROOT + "/Lobby/PieceControl/DL_PieceControlBuilds")
        inst = [i for i in dls.get_all_data_layers() if i.get_asset() == dl][0]
        Xc, Yb = 24000.0, 24744.0
        pieces = []

        def piece(kind, label, loc, yaw):
            if label in ACT:
                return
            a = eas.spawn_actor_from_class(unreal.load_class(None, P % (kind, kind)), loc, unreal.Rotator(0, 0, yaw))
            reg(a, label, F + "/Retake/Box")
            a.set_editor_property("forcibly_structurally_supported", True)
            pieces.append(a)

        for lv in range(3):
            z = Z0 + lv * 384.0
            piece("PBWA_W1_Solid", "BUILD_Retake_WallS%d" % lv, V(Xc, Yb, z), 0)
            piece("PBWA_W1_Solid", "BUILD_Retake_WallN%d" % lv, V(Xc, Yb + 512, z), 0)
            piece("PBWA_W1_Solid", "BUILD_Retake_WallW%d" % lv, V(Xc - 256, Yb + 256, z), 90)
            piece("PBWA_W1_Solid", "BUILD_Retake_WallE%d" % lv, V(Xc + 256, Yb + 256, z), 90)
            piece("PBWA_W1_Floor", "BUILD_Retake_Floor%d" % (lv + 1), V(Xc, Yb, z + 384), 0)
        if pieces:
            L.append("tour : %d pieces, reset %s" % (len(pieces), dls.add_actors_to_data_layer(pieces, inst)))
        # portail BUILD dans le lobby : copie miroir du portail 1V1
        for lab in list(ACT.keys()):
            if lab.startswith("LOBBY_Portal_1v1_") and "Icon" not in lab:
                s = ACT[lab]
                p = s.get_actor_location()
                r = s.get_actor_rotation()
                dup(lab, lab.replace("_1v1_", "_Build_"), V(-p.x, p.y, p.z), r.yaw + 180.0, "Lobby/Portals/Build")
        s = ACT["LOBBY_Zone_1v1"]
        p = s.get_actor_location()
        dup("LOBBY_Zone_1v1", "LOBBY_Zone_Build", V(-p.x, p.y, p.z), folder="Lobby/Portals/Build")
        ACT["LOBBY_Portal_Build_Title"].set_editor_property("text", "BUILD")
        # lignes 15-17 du classement global
        for k, (col, row) in zip(range(15, 18), ((0, 7), (1, 7), (0, 8))):
            bb("LOBBY_Global%d" % k, V(-1100 + col * 1400, -1165, 1990 - row * 70), "---", 16, 180.0, "Lobby/Extras/Global")
        d = ACT.get("BUILD_Device")
        if not d:
            d = eas.spawn_actor_from_object(unreal.load_object(None, ROOT + "/_Verse.build_zone"), V(CX, 22500, 870))
            reg(d, "BUILD_Device")
        eas.set_selected_level_actors([d])
    unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
    L.append("OK")
except Exception:
    L.append(traceback.format_exc())
open(r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools\build_buildzone_log.txt", "w").write("\n".join(L))
