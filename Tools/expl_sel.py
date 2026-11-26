import unreal
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
acts = eas.get_all_level_actors()
old = [a for a in acts if a.get_actor_label() in ("ZONE_1v1P_ResetExplosive", "ZONE_1v1P_ResetExplosive2", "ZONE_1v1P_ResetExplosive3")]
for a in old: eas.destroy_actor(a)
eas.set_selected_level_actors([a for a in eas.get_all_level_actors() if a.get_actor_label().startswith("ZONE_1v1P_ResetExp_G")])
