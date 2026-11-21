import unreal
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
for a in eas.get_all_level_actors():
    if a.get_actor_label() == "AIM_Glide_GuardTest":
        eas.destroy_actor(a)
g = eas.spawn_actor_from_class(unreal.load_class(None, "/CRD_HenchmanSpawner/Device_GuardSpawner_V2.Device_GuardSpawner_V2_C"), unreal.Vector(3000, 71000, 1270))
g.set_actor_label("AIM_Glide_GuardTest"); g.set_folder_path("Zones/Aim/Glide")
eas.set_selected_level_actors([g])
