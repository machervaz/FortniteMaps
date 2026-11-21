# Piece Control du joueur - corrections :
#  - montees recentrees sur les vraies colonnes (entre les murs) et une 4e montee
#  - zones de depart / arrivee invisibles en jeu
#  - pieces qui ne sont pas en bois (briques noires, dalles, escaliers Pueblo...) :
#    aucun degat (bCanBeDamaged = False + invulnerables) -> le reset ne casse que le bois
#  - recablage de tous les chronos (zones, HUD, retour, numero, reset a l'arrivee)
import unreal, json, traceback
TOOLS = r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools"
src = open(TOOLS + r"\build_pc.py", encoding="utf-8").read()
exec(src[:src.index("try:\n    ACT")])            # helpers et constantes de build_pc.py
MONTEES = [(22528.0, -1280.0, 4), (23040.0, -1280.0, 5), (24064.0, -1536.0, 6), (25088.0, -1792.0, 10)]
CH = {"start": "__verse_0x5CFF7AE4_StartTrigger", "finish": "__verse_0x16E5C556_FinishTrigger",
      "hud": "__verse_0xD5F0BE43_ResultHUD", "ret": "__verse_0xCB8B8794_ReturnPoint", "label": "__verse_0xBC955082_CourseLabel",
      "exp": "__verse_0xBEE4D5D5_ResetExplosives", "seq": "__verse_0x00B9F17C_ResetSequences"}
WR = {"prop": "/VerseDevices/_Verse/VNI/VerseDevices.Devices_creative_prop",
      "exp": "/CreativeCoreDevices/_Verse.explosive_device", "seq": "/CRD_CinematicSequence/_Verse.cinematic_sequence_device"}
L = []
try:
    MAP = json.load(open(TOOLS + r"\build_pc_map.json"))
    ACT = {a.get_actor_label(): a for a in eas.get_all_level_actors()}
    n = 0
    for lab, a in list(ACT.items()):
        if lab.startswith("PCX_Montee"):
            eas.destroy_actor(a); n += 1
    L.append("anciennes montees supprimees : %d" % n)
    white = eal.load_asset(MAT_DIR + "/M_Lobby_LedWhite")
    led = eal.load_asset(MAT_DIR + "/M_Lobby_DiscBlue")
    rgb = (0.2, 1.0, 0.3)
    holo = holo_mat("M_PC_Holo_%d_%d_%d" % tuple(int(c * 100) for c in rgb), rgb)
    courses = [c for c in MAP["courses"] if not c["name"].startswith("Montee")]
    with unreal.ScopedEditorTransaction("Piece Control : montees + degats"):
        for i, (x, yf, label) in enumerate(MONTEES):
            name = "Montee%d" % (i + 1)
            f = "Courses/" + name
            sz = zone(name + "_Start", f, x, -6400, HUBZ, 460, 500, 900)
            fz = zone(name + "_Finish", f, x, yf, 14216, 440, 440, 700)
            cyl(name + "_FinSocle", f, led, V(x, yf, 14216 + 3), V(420, 420, 6))
            cyl(name + "_FinRing", f, white, V(x, yf, 14216 + 2), V(470, 470, 3))
            cyl(name + "_FinHolo", f, holo, V(x, yf, 14216 + 15 + 170), V(330, 330, 340))
            billboard(name + "_FinTitle", f, V(x, yf, 14216 + 300), "ARRIVEE", 30)
            pl = eas.spawn_actor_from_class(unreal.PointLight, V(x, yf, 14216 + 250))
            lc = pl.get_component_by_class(unreal.PointLightComponent)
            lc.set_light_color(unreal.LinearColor(rgb[0], rgb[1], rgb[2], 1)); lc.set_intensity(40.0); lc.set_attenuation_radius(700.0)
            tag(pl, name + "_FinLight", f)
            hud = spawn("hud", name + "_HUD", f, V(23000, -11000 + i * 150, HUBZ - 600))
            ch = eas.spawn_actor_from_object(unreal.load_object(None, ROOT + "/_Verse.chrono_course"), V(23300, -11000 + i * 150, HUBZ - 600))
            tag(ch, name + "_Chrono", f)
            courses.append({"name": name, "label": label, "chrono": ch.get_actor_label(), "start": sz.get_actor_label(),
                            "finish": fz.get_actor_label(), "hud": hud.get_actor_label()})
        MAP["courses"] = courses
        ACT = {a.get_actor_label(): a for a in eas.get_all_level_actors()}
        # zones invisibles en jeu
        hidden = 0
        for c in courses:
            for k in ("start", "finish"):
                z = ACT[c[k]]
                for pn in ("VisibleDuringGame", "Visible During Game", "bVisibleDuringGame"):
                    try:
                        z.set_editor_property(pn, False); hidden += 1; break
                    except Exception:
                        pass
        L.append("zones rendues invisibles : %d" % hidden)
        # pieces non-bois : aucun degat
        nd = 0
        for a in eas.get_all_level_actors():
            p = a.get_actor_location()
            if not (USER_BOX[0] < p.x < USER_BOX[1] and USER_BOX[2] < p.y < USER_BOX[3]):
                continue
            if not isinstance(a, unreal.BuildingActor) or a.get_class().get_name().startswith("PBWA_"):
                continue
            a.modify()
            a.set_editor_property("bIsInvulnerable", True)
            a.set_editor_property("bCanBeDamaged", False)
            nd += 1
        L.append("pieces non-bois sans degats : %d" % nd)
    # cablage de tous les chronos
    def wrap(kind, outer, label):
        o = unreal.new_object(unreal.load_class(None, WR[kind]), outer)
        o.set_editor_property("SavedActor", ACT[label])
        return o
    for c in courses:
        s = ACT[c["chrono"]].get_editor_property("Script")
        for k in ("start", "finish", "hud"):
            s.get_editor_property(CH[k]).set_editor_property("SavedActor", ACT[c[k]])
        s.set_editor_property(CH["ret"], [wrap("prop", s, MAP["arrival"])])
        s.set_editor_property(CH["label"], c["label"])
        s.set_editor_property(CH["exp"], [wrap("exp", s, e) for e in MAP["explosives"]])
        s.set_editor_property(CH["seq"], [wrap("seq", s, MAP["seq"])])
    L.append("chronos cables : %d" % len(courses))
    json.dump(MAP, open(TOOLS + r"\build_pc_map.json", "w"), indent=1)
    unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
    L.append("TERMINE")
except Exception:
    L.append(traceback.format_exc())
open(TOOLS + r"\pc_fix2_log.txt", "w").write("\n".join(L))
