# 8 triggers (sous la salle, hors d'atteinte) : Up_i -> fait se lever le mannequin i,
# Down_i <- declenche quand le mannequin i est abattu (Verse ecoute)
import unreal, traceback
L = []
CLS = "/CreativeCoreDevices/Device_Trigger_V2.Device_Trigger_V2_C"
try:
    eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    for a in eas.get_all_level_actors():
        if a.get_actor_label().startswith(("AIM_Pump_Up", "AIM_Pump_Down")):
            eas.destroy_actor(a)
    for i in range(4):
        for k, kind in enumerate(("Up", "Down")):
            t = eas.spawn_actor_from_class(unreal.load_class(None, CLS), unreal.Vector(-300 + i * 200, 60000 + k * 200, 300))
            t.set_actor_label("AIM_Pump_%s%d" % (kind, i))
            t.set_folder_path("Zones/Aim/Pump/Triggers")
            t.set_editor_property("is_spatially_loaded", False)
    unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
    L.append("TERMINE")
except Exception:
    L.append(traceback.format_exc())
open(r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools\pump_triggers_log.txt", "w").write("\n".join(L))
