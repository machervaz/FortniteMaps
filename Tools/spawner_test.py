import unreal
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
cls = unreal.load_class(None, "/CreativeCoreDevices/Device_ItemSpawner_V3.Device_ItemSpawner_V3_C")
a = eas.spawn_actor_from_class(cls, unreal.Vector(-54000, 0, 770))
a.set_actor_label("TEST_ItemSpawner")
eas.set_selected_level_actors([a])
