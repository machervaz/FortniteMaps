# Relie bouton + selecteurs de classe de la salle DOUBLE PUMP au device aim_trainer
import unreal, traceback
F = {"PumpButton": ("__verse_0x5D268A97_PumpButton", "AIM_Pump_Button"),
     "PumpClassOn": ("__verse_0x645E9077_PumpClassOn", "AIM_Pump_ClassSelector"),
     "PumpClassOff": ("__verse_0x1D61AA81_PumpClassOff", "ZONE_1v1_Speed0_ClassSelector")}
L = []
try:
    eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    ACT = {a.get_actor_label(): a for a in eas.get_all_level_actors()}
    s = ACT["AIM_Trainer"].get_editor_property("Script")
    for k, (field, lab) in F.items():
        s.get_editor_property(field).set_editor_property("SavedActor", ACT[lab])
        L.append("%s -> %s" % (k, s.get_editor_property(field).get_editor_property("SavedActor").get_actor_label()))
    unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
    L.append("TERMINE")
except Exception:
    L.append(traceback.format_exc())
open(r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools\wire_pump_class_log.txt", "w").write("\n".join(L))
