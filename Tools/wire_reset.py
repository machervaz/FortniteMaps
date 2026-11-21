# Relie le device tunnel_reset : bouton, explosifs, sequence (apres edit_zone_v2.py)
import unreal, json, traceback
TOOLS = r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools"
TMAP = json.load(open(TOOLS + r"\build_tunnels_map.json", encoding="utf-8"))
F = {"buttons": "__verse_0x644B73CD_Buttons", "explosives": "__verse_0xDD942CDF_Explosives",
     "seq": "__verse_0x85E523EB_ReloadSequence"}
W = {"button": "/CreativeCoreDevices/_Verse.button_device", "explosive": "/CreativeCoreDevices/_Verse.explosive_device"}
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
ACT = {a.get_actor_label(): a for a in eas.get_all_level_actors()}
L = []
def wrap(key, outer, label):
    o = unreal.new_object(unreal.load_class(None, W[key]), outer)
    o.set_editor_property("SavedActor", ACT[label])
    return o
try:
    s = ACT["TUN_ResetDevice"].get_editor_property("Script")
    s.set_editor_property(F["buttons"], [wrap("button", s, "TUN_ResetButton")])
    s.set_editor_property(F["explosives"], [wrap("explosive", s, n) for n in TMAP["explosives"]])
    s.get_editor_property(F["seq"]).set_editor_property("SavedActor", ACT["TUN_ReloadSequence"])
    L.append("ok reset : %d explosifs" % len(TMAP["explosives"]))
    unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
except Exception:
    L.append(traceback.format_exc())
open(TOOLS + r"\wire_reset_log.txt", "w").write("\n".join(L))
