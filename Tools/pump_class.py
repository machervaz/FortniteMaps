# Classe "double pump" : copie du concepteur + selecteur de classe normaux (Speed0), places pres de la salle
import unreal, traceback
L = []
try:
    eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    ACT = {a.get_actor_label(): a for a in eas.get_all_level_actors()}
    for lab in ("AIM_Pump_ClassDesigner", "AIM_Pump_ClassSelector"):
        if lab in ACT:
            eas.destroy_actor(ACT[lab])
    for src, lab, pos in (("ZONE_1v1_Speed0_ClassDesigner", "AIM_Pump_ClassDesigner", (2100, 60800, 1270)),
                          ("ZONE_1v1_Speed0_ClassSelector", "AIM_Pump_ClassSelector", (2100, 61200, 1270))):
        d = eas.duplicate_actor(ACT[src])
        d.set_actor_location(unreal.Vector(*pos), False, False)
        d.set_actor_label(lab)
        d.set_folder_path("Zones/Aim/Pump/Class")
        d.set_editor_property("is_spatially_loaded", False)
        L.append("copie %s -> %s" % (src, lab))
    unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
    L.append("TERMINE")
except Exception:
    L.append(traceback.format_exc())
open(r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools\pump_class_log.txt", "w").write("\n".join(L))
