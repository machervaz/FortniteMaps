import unreal
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
for a in eas.get_all_level_actors():
    if a.get_actor_label() == "AIM_Glide_Guard":
        eas.destroy_actor(a)
g = eas.spawn_actor_from_class(unreal.load_class(None, "/CRD_HenchmanSpawner/Device_GuardSpawner_V2.Device_GuardSpawner_V2_C"), unreal.Vector(3300, 71300, 1270))
g.set_actor_label("AIM_Glide_Guard"); g.set_folder_path("Zones/Aim/Glide")
g.set_editor_property("is_spatially_loaded", False)
unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
eas.set_selected_level_actors([g])
