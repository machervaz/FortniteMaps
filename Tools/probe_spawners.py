import unreal, traceback
L = []
try:
    eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    for a in eas.get_all_level_actors():
        if a.get_actor_label() in ("AIM_Launch_Spawner", "AIM_Pump_Spawner", "AIM_Bounce_Spawner"):
            c = a.get_component_by_class(unreal.NPCCharacterDefinitionComponent)
            L.append("%s loc=%s def=%s spatial=%s" % (a.get_actor_label(), a.get_actor_location(), c.get_editor_property("NPCCharacterDefinition") if c else None, a.get_editor_property("is_spatially_loaded")))
except Exception:
    L.append(traceback.format_exc())
open(r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools\probe_spawners_log.txt", "w").write("\n".join(L))
