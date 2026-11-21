# Relie le reset a l'arrivee : chaque chrono Piece Control -> 7 explosifs + sequence de rechargement
import unreal, json, traceback
TOOLS = r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools"
MAP = json.load(open(TOOLS + r"\build_pc_map.json"))
F = {"exp": "__verse_0xBEE4D5D5_ResetExplosives", "seq": "__verse_0x00B9F17C_ResetSequences"}
W = {"exp": "/CreativeCoreDevices/_Verse.explosive_device", "seq": "/CRD_CinematicSequence/_Verse.cinematic_sequence_device"}
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
        s.set_editor_property(F["exp"], [wrap("exp", s, n) for n in MAP["explosives"]])
        s.set_editor_property(F["seq"], [wrap("seq", s, MAP["seq"])])
        L.append("ok " + c["name"])
    unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
    L.append("TERMINE")
except Exception:
    L.append(traceback.format_exc())
open(TOOLS + r"\wire_pc_reset_log.txt", "w").write("\n".join(L))
