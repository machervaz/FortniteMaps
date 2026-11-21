# Emote dans la salle DOUBLE PUMP -> hall aim principal (et plus le lobby) + texte du mur
import unreal, traceback
L = []
try:
    eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    ACT = {a.get_actor_label(): a for a in eas.get_all_level_actors()}
    s = ACT["AIM_Trainer"].get_editor_property("Script")
    w = s.get_editor_property("__verse_0x204CC60D_LobbyPoint")
    w.set_editor_property("SavedActor", ACT["ZONE_Aim_Arrival"])
    L.append("retour emote -> %s" % s.get_editor_property("__verse_0x204CC60D_LobbyPoint").get_editor_property("SavedActor").get_actor_label())
    b = ACT["AIM_Pump_Emote2"]
    with unreal.ScopedEditorTransaction("Texte emote"):
        b.modify()
        b.set_editor_property("text", "TO GO BACK TO AIM")
    L.append("texte : %s" % b.get_editor_property("text"))
    unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
    L.append("TERMINE")
except Exception:
    L.append(traceback.format_exc())
open(r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools\pump_emote_hub_log.txt", "w").write("\n".join(L))
