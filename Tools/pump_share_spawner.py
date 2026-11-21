# Limite de PNJ : le 4e NPC spawner ne fait rien apparaitre -> la salle DOUBLE PUMP
# utilise le spawner de l'exercice REBOND (les bots n'existent que si un joueur est dans l'arene)
import unreal, traceback
L = []
try:
    eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    ACT = {a.get_actor_label(): a for a in eas.get_all_level_actors()}
    s = ACT["AIM_Trainer"].get_editor_property("Script")
    w = s.get_editor_property("__verse_0x4464509C_PumpSpawner")
    w.set_editor_property("SavedActor", ACT["AIM_Bounce_Spawner"])
    L.append("PumpSpawner -> %s" % s.get_editor_property("__verse_0x4464509C_PumpSpawner").get_editor_property("SavedActor").get_actor_label())
    for lab in ("AIM_Pump_Spawner", "AIM_Pump_Staging"):
        if lab in ACT:
            eas.destroy_actor(ACT[lab]); L.append("supprime " + lab)
    n = sum(1 for a in eas.get_all_level_actors() if a.get_class().get_name() == "Device_CharacterSpawner_C")
    L.append("NPC spawners restants : %d" % n)
    unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
    L.append("TERMINE")
except Exception:
    L.append(traceback.format_exc())
open(r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools\pump_share_spawner_log.txt", "w").write("\n".join(L))
