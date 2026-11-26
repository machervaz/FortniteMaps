import unreal
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
ACT = {a.get_actor_label(): a for a in eas.get_all_level_actors()}
if "AIM_ScoreHUD" not in ACT:
    a = eas.spawn_actor_from_class(unreal.load_class(None, "/CreativeCoreDevices/Device_HUDMessage_V2.Device_HUDMessage_V2_C"), unreal.Vector(1400, 17300, 870))
    a.set_actor_label("AIM_ScoreHUD"); a.set_folder_path("Zones/Aim/Devices"); a.set_editor_property("is_spatially_loaded", False)
eas.set_selected_level_actors([ACT["AIM_Trainer"]])
