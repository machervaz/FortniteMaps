# ============================================================================
#  wire_tunnels.py - pose un chrono_course par tunnel et le relie
#  (apres build_tunnels.py). Champs Verse encodes : voir wire_manager.py
# ============================================================================
import unreal, json, traceback

ROOT = "/5622d7d7-d1ca-438f-8a48-1286a48e2471"
TOOLS = r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools"
MAP = json.load(open(TOOLS + r"\build_tunnels_map.json", encoding="utf-8"))
FLOOR_Z = 1270.0

F = {
    "start": "__verse_0x5CFF7AE4_StartTrigger",
    "finish": "__verse_0x16E5C556_FinishTrigger",
    "hud": "__verse_0xD5F0BE43_ResultHUD",
    "name": None,      # rempli plus bas si connu
    "ret": None,
}
try:
    F.update(json.load(open(TOOLS + r"\chrono_fields.json", encoding="utf-8")))
except Exception:
    pass

eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
ACT = {a.get_actor_label(): a for a in eas.get_all_level_actors()}
L = []
try:
    prop_cls = unreal.load_class(None, "/VerseDevices/_Verse/VNI/VerseDevices.Devices_creative_prop")
    for t in MAP["tunnels"]:
        lbl = "TUN_%s_Chrono" % t["name"]
        d = ACT.get(lbl)
        if not d:
            d = eas.spawn_actor_from_object(unreal.load_object(None, ROOT + "/_Verse.chrono_course"),
                                            unreal.Vector(t["x"], -23000, FLOOR_Z - 400))
            d.set_actor_label(lbl)
            d.set_folder_path("Zones/Edit/Tunnels/" + t["name"].capitalize() + "/Chrono")
        s = d.get_editor_property("Script")
        s.get_editor_property(F["start"]).set_editor_property("SavedActor", ACT[t["start"]])
        s.get_editor_property(F["finish"]).set_editor_property("SavedActor", ACT[t["finish"]])
        s.get_editor_property(F["hud"]).set_editor_property("SavedActor", ACT[t["hud"]])
        # CourseName (chaine Verse) : non modifiable en Python -> a saisir dans Details
        if F["ret"]:
            w = unreal.new_object(prop_cls, s)
            w.set_editor_property("SavedActor", ACT[MAP["return_pad"]])
            s.set_editor_property(F["ret"], [w])
        L.append("ok " + lbl)
    # device de remise a zero (ses 2 champs se reglent dans Details :
    # Buttons = TUN_ResetButton, RoundSettings = TUN_RoundSettings)
    if "TUN_ResetDevice" not in ACT:
        r = eas.spawn_actor_from_object(unreal.load_object(None, ROOT + "/_Verse.tunnel_reset"),
                                        unreal.Vector(-700, -22300, FLOOR_Z - 400))
        r.set_actor_label("TUN_ResetDevice")
        r.set_folder_path("Zones/Edit/Tunnels/Structure")
        L.append("reset device pose")
    unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
except Exception:
    L.append(traceback.format_exc())
open(TOOLS + r"\wire_tunnels_log.txt", "w", encoding="utf-8").write("\n".join(L))
