# ============================================================================
#  wire_manager.py - pose et relie training_hub_manager + chrono_course
#  (a lancer apres build_lobby.py et build_zones.py)
#  Les champs @editable Verse sont stockes dans le sous-objet "Script" du
#  VerseDevice, sous des noms encodes (__verse_0x<hash>_<Nom>). Une reference
#  vers un acteur est un sous-objet "wrapper" dont la propriete SavedActor
#  pointe sur l'acteur.
# ============================================================================
import unreal, json, traceback

ROOT = "/5622d7d7-d1ca-438f-8a48-1286a48e2471"
TOOLS = r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools"
LOG_FILE = TOOLS + r"\wire_manager_log.txt"
MAP = json.load(open(TOOLS + r"\build_zones_map.json", encoding="utf-8"))

F = {  # noms encodes des champs Verse
    "Portals": "__verse_0xB4A62D8E_Portals",
    "ReturnZones": "__verse_0x95E6B777_ReturnZones",
    "LobbyPoint": "__verse_0x204CC60D_LobbyPoint",
    "DefaultClass": "__verse_0xBD0AF838_DefaultClass",
    "SpeedOptions": "__verse_0x29D62964_SpeedOptions",
    "Holograms": "__verse_0x4F6B1541_Holograms",
    "EntryZone": "__verse_0xC40A24B1_EntryZone",
    "Destination": "__verse_0x96EC8CCE_Destination",
    "Loadouts": "__verse_0xC1C983CE_Loadouts",
    "WelcomeMessages": "__verse_0x6647C83C_WelcomeMessages",
    "ClassOnEnter": "__verse_0x5D0E3A5E_ClassOnEnter",
    "Button": "__verse_0x8F004746_Button",
    "ClassSelector": "__verse_0xB53F160E_ClassSelector",
}
W = {  # classes "wrapper" Verse des devices
    "mutator": "/CRD_VolumetricRegion/_Verse.mutator_zone_device",
    "prop": "/VerseDevices/_Verse/VNI/VerseDevices.Devices_creative_prop",
    "granter": "/CreativeCoreDevices/_Verse.item_granter_device",
    "hud": "/CreativeCoreDevices/_Verse.hud_message_device",
    "selector": "/CreativeCoreDevices/_Verse.class_and_team_selector_device",
    "button": "/CreativeCoreDevices/_Verse.button_device",
    "hub_portal": ROOT + "/_Verse.hub_portal",
    "speed_option": ROOT + "/_Verse.speed_option",
}
# lobby : portail -> mutator zone du cylindre
LOBBY_ZONES = {"PieceControl": "LOBBY_Zone_PieceControl", "Edit": "LOBBY_Zone_Edit",
               "Aim": "LOBBY_Zone_Aim", "1v1": "LOBBY_Zone_1v1"}

lines = []
def log(*a):
    lines.append(" ".join(str(x) for x in a))

eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
ACT = {a.get_actor_label(): a for a in eas.get_all_level_actors()}

def actor(label):
    a = ACT.get(label)
    if not a:
        log("ACTEUR INTROUVABLE", label)
    return a

_wcls = {}
def wcls(key):
    if key not in _wcls:
        _wcls[key] = unreal.load_class(None, W[key])
        log("classe", key, _wcls[key])
    return _wcls[key]

def ref(key, outer, label):
    """Cree un wrapper Verse pointant sur l'acteur 'label'."""
    a = actor(label)
    if not a:
        return None
    o = unreal.new_object(wcls(key), outer)
    o.set_editor_property("SavedActor", a)
    return o

def set_single(obj, field, label):
    """Champ simple (deja present comme sous-objet) -> SavedActor."""
    a = actor(label)
    if not a:
        return
    sub = obj.get_editor_property(F[field])
    sub.set_editor_property("SavedActor", a)

def get_or_spawn_verse_device(cls_path, label, loc):
    if label in ACT:
        return ACT[label]
    a = eas.spawn_actor_from_object(unreal.load_object(None, cls_path), loc)
    a.set_actor_label(label)
    a.set_folder_path("Zones/Manager")
    ACT[label] = a
    return a

try:
    # ---- manager ----
    m = ACT.get("ZONE_TrainingHubManager") or ACT.get("ZONE_TrainingHubManager_TEST")
    if not m:
        m = get_or_spawn_verse_device(ROOT + "/_Verse.training_hub_manager", "ZONE_TrainingHubManager", unreal.Vector(0, 0, 870))
    m.set_actor_label("ZONE_TrainingHubManager")
    m.set_folder_path("Zones/Manager")
    s = m.get_editor_property("Script")
    log("script", s)

    set_single(s, "LobbyPoint", MAP["lobby_point"])

    portals = []
    for key in ["PieceControl", "Edit", "Aim", "1v1"]:
        z = MAP[key]
        p = unreal.new_object(wcls("hub_portal"), s)
        p.get_editor_property(F["EntryZone"]).set_editor_property("SavedActor", actor(LOBBY_ZONES[key]))
        p.get_editor_property(F["Destination"]).set_editor_property("SavedActor", actor(z["arrival"]))
        p.set_editor_property(F["Loadouts"], [ref("granter", p, z["granter"])])
        p.set_editor_property(F["WelcomeMessages"], [ref("hud", p, z["hud"])])
        if key == "1v1":
            p.set_editor_property(F["ClassOnEnter"], [ref("selector", p, MAP["speed"][0]["selector"])])
        else:
            p.set_editor_property(F["ClassOnEnter"], [])
        portals.append(p)
        log("portail ok", key)
    s.set_editor_property(F["Portals"], portals)

    s.set_editor_property(F["ReturnZones"], [ref("mutator", s, MAP[k]["return_zone"]) for k in ["PieceControl", "Edit", "Aim", "1v1"]])
    s.set_editor_property(F["DefaultClass"], [ref("selector", s, MAP["speed"][0]["selector"])])

    opts = []
    for sp in MAP["speed"]:
        o = unreal.new_object(wcls("speed_option"), s)
        o.get_editor_property(F["Button"]).set_editor_property("SavedActor", actor(sp["button"]))
        o.get_editor_property(F["ClassSelector"]).set_editor_property("SavedActor", actor(sp["selector"]))
        opts.append(o)
    s.set_editor_property(F["SpeedOptions"], opts)
    s.set_editor_property(F["Holograms"], [])
    log("manager relie")

    # ---- chrono_course : un device par parcours ----
    for c in MAP["chronos"]:
        lbl = c["start"].replace("_ChronoStart", "_Chrono")
        st = actor(c["start"])
        loc = st.get_actor_location() if st else unreal.Vector(0, 0, 870)
        d = get_or_spawn_verse_device(ROOT + "/_Verse.chrono_course", lbl, loc + unreal.Vector(0, -600, 0))
        log("chrono pose", lbl, d)

    unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
    log("TERMINE")
except Exception:
    log("ERREUR", traceback.format_exc())

open(LOG_FILE, "w", encoding="utf-8").write("\n".join(lines))
