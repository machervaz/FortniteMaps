# Relie les 2 devices chrono_course a leurs triggers / HUD (apres wire_manager.py)
import unreal, json, traceback
TOOLS = r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools"
MAP = json.load(open(TOOLS + r"\build_zones_map.json", encoding="utf-8"))
F = {"start": "__verse_0x5CFF7AE4_StartTrigger", "finish": "__verse_0x16E5C556_FinishTrigger", "hud": "__verse_0xD5F0BE43_ResultHUD"}
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
ACT = {a.get_actor_label(): a for a in eas.get_all_level_actors()}
L = []
try:
    for c in MAP["chronos"]:
        dev = ACT.get(c["start"].replace("_ChronoStart", "_Chrono"))
        if not dev:
            continue   # chrono supprime (ancienne partie Edit)
        s = dev.get_editor_property("Script")
        for k in ("start", "finish", "hud"):
            s.get_editor_property(F[k]).set_editor_property("SavedActor", ACT[c[k]])
        L.append("ok " + dev.get_actor_label())
    unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
except Exception:
    L.append(traceback.format_exc())
open(TOOLS + r"\wire_chrono_log.txt", "w").write("\n".join(L))
