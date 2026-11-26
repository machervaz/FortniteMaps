import unreal, traceback
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
L = []
try:
    acts = eas.get_all_level_actors()
    sp = [a for a in acts if a.get_actor_label().startswith("ZONE_1v1_Arme")]
    for a in sorted(sp, key=lambda a: a.get_actor_label()):
        p = a.get_actor_location()
        L.append("%s %s (%.0f,%.0f,%.0f) folder=%s" % (a.get_actor_label(), a.get_class().get_name(), p.x, p.y, p.z, a.get_folder_path()))
    if len(sp) == 17:
        with unreal.ScopedEditorTransaction("1v1 : poseurs -> generateurs"):
            dead = [a for a in acts if a.get_actor_label() == "TEST_ItemSpawner"]
            dead += [a for a in acts if a.get_class().get_name() == "BP_ItemContainer_C" and -21000 < a.get_actor_location().x < -18000 and a.get_actor_label() != "Poseur d'objet29"]
            L.append("supprimes : %d" % sum(1 for a in dead if eas.destroy_actor(a)))
            for g in [a for a in acts if a.get_class().get_name() == "CP_Glass_Floor_C" and -22500 < a.get_actor_location().x < -17500]:
                c = g.get_component_by_class(unreal.StaticMeshComponent)
                n = eas.spawn_actor_from_class(unreal.FortStaticMeshActor, g.get_actor_location(), g.get_actor_rotation())
                nc = n.get_component_by_class(unreal.StaticMeshComponent)
                nc.set_static_mesh(c.static_mesh)
                for i in range(c.get_num_materials()):
                    nc.set_material(i, c.get_material(i))
                n.set_actor_scale3d(g.get_actor_scale3d())
                n.set_actor_label("ZONE_1v1_VitreArmes"); n.set_folder_path("Zones/1v1/Armes")
                n.set_editor_property("is_spatially_loaded", False)
                L.append("vitre remplacee : mesh=%s mats=%d ; ancienne supprimee=%s" % (c.static_mesh.get_name(), c.get_num_materials(), eas.destroy_actor(g)))
    unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
    L.append("TERMINE")
except Exception:
    L.append(traceback.format_exc())
open(r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools\swap_1v1_log.txt","w").write("\n".join(L))
