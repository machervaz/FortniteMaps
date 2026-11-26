import unreal
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
sel = [a for a in eas.get_all_level_actors() if a.get_class().get_name().startswith("PBWA_") and -3500 < a.get_actor_location().x < 3500 and -48000 < a.get_actor_location().y < -22000]
eas.set_selected_level_actors(sel)
print("SELECTION", len(sel))
