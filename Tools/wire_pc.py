# Relie les 9 chronos et le RESET de la zone Piece Control du joueur (apres build_pc.py)
import unreal, json, traceback
TOOLS = r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools"
MAP = json.load(open(TOOLS + r"\build_pc_map.json"))
C = {"start": "__verse_0x5CFF7AE4_StartTrigger", "finish": "__verse_0x16E5C556_FinishTrigger",
     "hud": "__verse_0xD5F0BE43_ResultHUD", "ret": "__verse_0xCB8B8794_ReturnPoint", "label": "__verse_0xBC955082_CourseLabel"}
R = {"buttons": "__verse_0x644B73CD_Buttons", "explosives": "__verse_0xDD942CDF_Explosives", "seq": "__verse_0x85E523EB_ReloadSequence"}
W = {"prop": "/VerseDevices/_Verse/VNI/VerseDevices.Devices_creative_prop",
     "button": "/CreativeCoreDevices/_Verse.button_device", "explosive": "/CreativeCoreDevices/_Verse.explosive_device"}
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
L = []
try:
    ACT = {a.get_actor_label(): a for a in eas.get_all_level_actors()}
    def wrap(kind, outer, label):
        o = unreal.new_object(unreal.load_class(None, W[kind]), outer)
        o.set_editor_property("SavedActor", ACT[label])
        return o
    for c in MAP["courses"]:
        s = ACT[c["chrono"]].get_editor_property("Script")
        for k in ("start", "finish", "hud"):
            s.get_editor_property(C[k]).set_editor_property("SavedActor", ACT[c[k]])
        s.set_editor_property(C["ret"], [wrap("prop", s, MAP["arrival"])])
        s.set_editor_property(C["label"], c["label"])
        L.append("chrono %s -> %d" % (c["name"], s.get_editor_property(C["label"])))
    s = ACT[MAP["reset"]].get_editor_property("Script")
    s.set_editor_property(R["buttons"], [wrap("button", s, MAP["button"])])
    s.set_editor_property(R["explosives"], [wrap("explosive", s, MAP["explosive"])])
    s.get_editor_property(R["seq"]).set_editor_property("SavedActor", ACT[MAP["seq"]])
    L.append("reset ok")
    unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
    L.append("TERMINE")
except Exception:
    L.append(traceback.format_exc())
open(TOOLS + r"\wire_pc_log.txt", "w").write("\n".join(L))
