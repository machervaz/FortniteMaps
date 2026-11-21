import unreal
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
a = [x for x in eas.get_all_level_actors() if x.get_actor_label() == "ZONE_Aim_Title"][0]
with unreal.ScopedEditorTransaction("Titre AIM plus haut"):
    a.modify()
    for c in a.get_components_by_class(unreal.SceneComponent):
        c.modify()
    p = a.get_actor_location()
    a.set_actor_location(unreal.Vector(p.x, p.y, 2150.0), False, False)
unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
