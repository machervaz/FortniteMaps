import unreal
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
u = [a for a in eas.get_all_level_actors() if a.get_actor_label() == "AIM_Glide_Umbrella"][0]
u.set_actor_scale3d(unreal.Vector(1.6, 1.6, 1.6))
unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
