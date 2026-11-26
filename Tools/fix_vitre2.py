import unreal
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
a = [x for x in eas.get_all_level_actors() if x.get_actor_label() == "ZONE_1v1_VitreArmes"][0]
c = a.get_component_by_class(unreal.StaticMeshComponent)
with unreal.ScopedEditorTransaction("1v1 : vitre materiau"):
    c.modify()
    c.set_material(0, unreal.EditorAssetLibrary.load_asset("/Game/Creative/Environments/Meshes/Glass/Materials/MI_CP_GlassGallery"))
unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
open(r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools\fix_vitre2_log.txt","w").write(c.get_material(0).get_path_name())
