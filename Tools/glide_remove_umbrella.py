import unreal
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
for a in eas.get_all_level_actors():
    if a.get_actor_label() == "AIM_Glide_Umbrella":
        eas.destroy_actor(a)
unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
