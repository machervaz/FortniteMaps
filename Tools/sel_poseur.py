import unreal
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
eas.set_selected_level_actors([a for a in eas.get_all_level_actors() if a.get_actor_label().startswith("ZONE_1v1_Arme")])
