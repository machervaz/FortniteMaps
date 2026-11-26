# Builds poses au telephone dans la salle devant les tunnels (zone Edit) : support force,
# toujours charges, bois -> reset des tunnels ; autres pieces de construction -> indestructibles
import unreal, collections, traceback
L = []
BOX = (-3200, 3200, -23000, -16000)
try:
    eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    dls = unreal.get_editor_subsystem(unreal.DataLayerEditorSubsystem)
    dl = unreal.load_asset("/5622d7d7-d1ca-438f-8a48-1286a48e2471/Tunnels/DL_TunnelBuilds")
    inst = [i for i in dls.get_all_data_layers() if i.get_asset() == dl][0]
    wood, other = [], collections.Counter()
    with unreal.ScopedEditorTransaction("Zone Edit : builds"):
        for a in eas.get_all_level_actors():
            p = a.get_actor_location(); n = a.get_class().get_name()
            if not (BOX[0] < p.x < BOX[1] and BOX[2] < p.y < BOX[3]) or not isinstance(a, unreal.BuildingActor) or "Device" in n:
                continue
            a.modify()
            try:
                a.set_editor_property("forcibly_structurally_supported", True)
                a.set_editor_property("is_spatially_loaded", False)
            except Exception:
                pass
            if n.startswith("PBWA_"):
                wood.append(a)
            else:
                try:
                    a.set_editor_property("bIsInvulnerable", True); a.set_editor_property("bCanBeDamaged", False)
                except Exception:
                    pass
                other[n] += 1
    if wood:
        L.append("bois de la salle ajoute au reset : %s" % dls.add_actors_to_data_layer(wood, inst))
    L.append("salle Edit : %d bois, autres %s" % (len(wood), dict(other)))
    unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
    L.append("TERMINE")
except Exception:
    L.append(traceback.format_exc())
open(r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools\edit_hall_sync_log.txt", "w").write("\n".join(L))
