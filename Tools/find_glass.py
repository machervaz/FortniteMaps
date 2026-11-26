import unreal
ar = unreal.AssetRegistryHelpers.get_asset_registry()
L = [str(d.package_name) for d in ar.get_all_assets() if "GlassGallery" in str(d.asset_name) or str(d.asset_name).startswith("MI_CP_Glass")]
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
a = [x for x in eas.get_all_level_actors() if x.get_actor_label() == "ZONE_1v1_VitreArmes"][0]
m = a.get_component_by_class(unreal.StaticMeshComponent).get_material(0)
try: L.append("parent: " + m.get_editor_property("parent").get_path_name())
except Exception as e: L.append(str(e))
open(r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools\find_glass_log.txt","w").write("\n".join(L))
