# Bouton "DOUBLE PUMP" dans la salle (contre le mur du fond a gauche, face au joueur) + petit texte
import unreal, traceback
exec(open(r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools\aim_lib.py", encoding="utf-8").read())
try:
    for a in eas.get_all_level_actors():
        if a.get_actor_label() in ("AIM_Pump_Button", "AIM_Pump_ButtonText"):
            eas.destroy_actor(a)
    # mur sud (derriere l'arrivee) : le joueur se retourne pour l'activer
    b = eas.spawn_actor_from_class(unreal.load_class(None, "/CreativeCoreDevices/Device_Button_V2.Device_Button_V2_C"),
                                   V(0, 60000 - 200, FLOOR), unreal.Rotator(roll=0, pitch=0, yaw=90.0))
    tag(b, "Pump_Button", "Pump")
    billboard("Pump_ButtonText", "Pump", V(0, 60000 - 241, FLOOR + 330), 90.0, "NO DELAY", 26)
    unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
    L.append("TERMINE")
except Exception:
    L.append(traceback.format_exc())
open(TOOLS + r"\pump_button_log.txt", "w").write("\n".join(L))
