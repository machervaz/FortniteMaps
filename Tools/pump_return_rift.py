# Salle DOUBLE PUMP : portail "BACK TO AIM" (zone d'alteration) contre le mur est -> hall aim
# (l'emote n'est pas signalee par Fortnite ici) ; retire les textes "emote"
import unreal, json, traceback
exec(open(r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools\aim_lib.py", encoding="utf-8").read())
try:
    for a in eas.get_all_level_actors():
        lab = a.get_actor_label()
        if lab.startswith("AIM_Pump_Return") or lab in ("AIM_Pump_Emote1", "AIM_Pump_Emote2"):
            eas.destroy_actor(a)
    M = {}
    z = rift("Pump_Return", "Pump", 220, 60000, 180.0, (0.2, 0.6, 1.0), "BACK TO AIM", M)
    for a in eas.get_all_level_actors():
        if a.get_actor_label() == "AIM_Pump_Return_Title":
            a.set_editor_property("TextSize", 30)
    MAP = json.load(open(TOOLS + r"\build_aim_map.json"))
    if "AIM_Pump_Return_Zone" not in MAP["rifts"]:
        MAP["rifts"].append("AIM_Pump_Return_Zone"); MAP["targets"].append("ZONE_Aim_Arrival")
        json.dump(MAP, open(TOOLS + r"\build_aim_map.json", "w"), indent=1)
    unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
    L.append("TERMINE")
except Exception:
    L.append(traceback.format_exc())
open(TOOLS + r"\pump_return_rift_log.txt", "w").write("\n".join(L))
