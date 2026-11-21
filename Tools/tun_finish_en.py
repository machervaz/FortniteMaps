# Apres la reconstruction des tunnels (build_tunnels -> edit_zone_v2 -> wire_tunnels) :
#  - explosifs des tunnels regles (invisibles, 0 degat joueur, rayon 40, gros degats structures)
#  - plus de bouton RESET : chaque chrono de tunnel remet les pieces a zero a l'arrivee
#    (explosifs + sequence de rechargement), nom anglais via CourseLabel (11..14)
#  - tous les panneaux de la map traduits en anglais
import unreal, json, traceback
TOOLS = r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools"
CH = {"label": "__verse_0xBC955082_CourseLabel", "exp": "__verse_0xBEE4D5D5_ResetExplosives",
      "seq": "__verse_0x00B9F17C_ResetSequences", "ret": "__verse_0xCB8B8794_ReturnPoint"}
WR = {"prop": "/VerseDevices/_Verse/VNI/VerseDevices.Devices_creative_prop",
      "exp": "/CreativeCoreDevices/_Verse.explosive_device", "seq": "/CRD_CinematicSequence/_Verse.cinematic_sequence_device"}
LABELS = {"FACILE": 11, "MOYEN": 12, "DIFFICILE": 13, "IMPOSSIBLE": 14}
EN = {"ARRIVEE": "FINISH", "RETOUR AIM": "BACK TO AIM", "RETOUR LOBBY": "BACK TO LOBBY", "FACILE": "EASY",
      "MOYEN": "MEDIUM", "DIFFICILE": "HARD", "TUNNELS D'EDIT": "EDIT TUNNELS", "REBOND": "BOUNCE",
      "LANCER": "LAUNCH", "PARCOURS CHRONO": "TIMED RUN"}
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
L = []
try:
    ACT = {a.get_actor_label(): a for a in eas.get_all_level_actors()}
    for lab in ("TUN_ResetButton", "TUN_ResetTitle", "TUN_ResetDevice"):
        if lab in ACT:
            eas.destroy_actor(ACT.pop(lab)); L.append("supprime " + lab)
    exps = sorted(l for l in ACT if l.startswith("TUN_Explosive"))
    for l in exps:
        e = ACT[l]
        for pn, v in (("Blast Radius", 40.0), ("Structure Damage", 100000.0), ("Player Damage", 0.0), ("Visible During Game", False)):
            try:
                e.set_editor_property(pn, v)
            except Exception as ex:
                L.append("%s %s : %s" % (l, pn, ex))
    L.append("explosifs tunnels : %s" % exps)
    for l, a in ACT.items():
        if l.startswith("TUN_"):
            try:
                a.set_editor_property("is_spatially_loaded", False)
            except Exception:
                pass
    def wrap(kind, outer, label):
        o = unreal.new_object(unreal.load_class(None, WR[kind]), outer)
        o.set_editor_property("SavedActor", ACT[label])
        return o
    for name, num in LABELS.items():
        s = ACT["TUN_%s_Chrono" % name].get_editor_property("Script")
        s.set_editor_property(CH["label"], num)
        s.set_editor_property(CH["exp"], [wrap("exp", s, e) for e in exps])
        s.set_editor_property(CH["seq"], [wrap("seq", s, "TUN_ReloadSequence")])
        s.set_editor_property(CH["ret"], [wrap("prop", s, "TUN_ReturnPad")])
        L.append("chrono %s -> %d" % (name, num))
    n = 0
    for a in eas.get_all_level_actors():
        if "Billboard" in a.get_class().get_name():
            try:
                t = str(a.get_editor_property("text"))
            except Exception:
                continue
            if t in EN:
                a.set_editor_property("text", EN[t]); n += 1
    L.append("panneaux traduits : %d" % n)
    unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
    L.append("TERMINE")
except Exception:
    L.append(traceback.format_exc())
open(TOOLS + r"\tun_finish_en_log.txt", "w").write("\n".join(L))
