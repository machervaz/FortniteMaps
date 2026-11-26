import unreal, traceback
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
L = []
try:
    a = [x for x in eas.get_all_level_actors() if x.get_actor_label() == "ZONE_1v1_VitreArmes"][0]
    o, e = a.get_actor_bounds(False)
    c = a.get_component_by_class(unreal.StaticMeshComponent)
    mat = c.get_material(0)
    L.append("avant : centre %s ext %s mat %s" % (o, e, mat.get_path_name() if mat else None))
    with unreal.ScopedEditorTransaction("1v1 : vitre en cube"):
        a.modify(); c.modify()
        c.set_static_mesh(unreal.EditorAssetLibrary.load_asset("/Engine/BasicShapes/Cube"))
        if mat: c.set_material(0, mat)
        a.set_actor_rotation(unreal.Rotator(0, 0, 0), False)
        a.set_actor_scale3d(unreal.Vector(max(e.x, 2) / 50.0, max(e.y, 2) / 50.0, max(e.z, 2) / 50.0))
        a.set_actor_location(o, False, False)
    o2, e2 = a.get_actor_bounds(False)
    L.append("apres : centre %s ext %s" % (o2, e2))
    unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
    L.append("TERMINE")
except Exception:
    L.append(traceback.format_exc())
open(r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools\fix_vitre_log.txt","w").write("\n".join(L))
