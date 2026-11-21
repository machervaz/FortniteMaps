# Relie le device arena_panel (apres build_panel.py) : formes a tirer
import unreal, json, traceback
TOOLS = r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools"
MAP = json.load(open(TOOLS + r"\build_panel_map.json"))
F = {"down": "__verse_0x53ED515C_SpeedDownShape", "up": "__verse_0x668A10D1_SpeedUpShape",
     "display": "__verse_0xA9A9005C_SpeedDisplay", "selectors": "__verse_0xF6F415C1_SpeedSelectors",
     "reset": "__verse_0x003E7750_ResetShape", "explosives": "__verse_0xBEE4D5D5_ResetExplosives",
     "sky_shapes": "__verse_0x9D623D14_SkyShapes", "sky_vault": "__verse_0x305F1501_SkyVault",
     "shape_props": "__verse_0x112222C4_ShapeProps",
     "sky_floor": "__verse_0xEEEB52A5_SkyFloor", "fall_zone": "__verse_0x9ABFD34F_FallZone",
     "respawn": "__verse_0x6838D131_RespawnPoint"}
W = {"pm": "/CRD_PropManipulationDevice/_Verse.prop_manipulator_device",
     "prop": "/VerseDevices/_Verse/VNI/VerseDevices.Devices_creative_prop",
     "selector": "/CreativeCoreDevices/_Verse.class_and_team_selector_device",
     "dome": "/CRD_SkydomeDevice/_Verse.day_sequence_device",
     "explosive": "/CreativeCoreDevices/_Verse.explosive_device"}
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
L = []
try:
    ACT = {a.get_actor_label(): a for a in eas.get_all_level_actors()}
    s = ACT[MAP["panel"]].get_editor_property("Script")
    def single(field, label):
        s.get_editor_property(F[field]).set_editor_property("SavedActor", ACT[label])
    def wrap(kind, label):
        o = unreal.new_object(unreal.load_class(None, W[kind]), s)
        o.set_editor_property("SavedActor", ACT[label])
        return o
    for k in ("down", "up", "display", "reset"):
        single(k, MAP[k])
    s.set_editor_property(F["explosives"], [wrap("explosive", l) for l in MAP["explosives"]])
    single("sky_vault", MAP["sky_vault"])
    for k in ("sky_floor", "fall_zone", "respawn"):
        single(k, MAP[k])
    s.set_editor_property(F["selectors"], [wrap("selector", l) for l in MAP["selectors"]])
    s.set_editor_property(F["sky_shapes"], [wrap("pm", l) for l in MAP["sky_shapes"]])
    shapes = sorted(l for l in ACT if l.startswith("ZONE_1v1P_Shape"))
    s.set_editor_property(F["shape_props"], [wrap("prop", l) for l in shapes])
    L.append("formes : %s" % shapes)
    unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
    L.append("ok")
except Exception:
    L.append(traceback.format_exc())
open(TOOLS + r"\wire_panel_log.txt", "w").write("\n".join(L))
