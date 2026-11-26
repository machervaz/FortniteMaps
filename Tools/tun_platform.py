# Repose le sol noir brillant sous les 4 tunnels (TUN_Platform), dessus a z=1270, indestructible
import unreal, traceback
L = []
try:
    eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    old = [a for a in eas.get_all_level_actors() if a.get_actor_label() == "TUN_Platform"]
    L.append("deja present : %d" % len(old))
    if not old:
        MAT = unreal.EditorAssetLibrary.load_asset("/5622d7d7-d1ca-438f-8a48-1286a48e2471/Lobby/Materials/M_Lobby_BlackGloss")
        a = eas.spawn_actor_from_class(unreal.FortStaticMeshActor, unreal.Vector(0.0, -35200.0, 1245.0))
        c = a.get_component_by_class(unreal.StaticMeshComponent)
        c.set_static_mesh(unreal.EditorAssetLibrary.load_asset("/Engine/BasicShapes/Cube"))
        c.set_material(0, MAT)
        a.set_actor_scale3d(unreal.Vector(60.0, 244.0, 0.5))
        a.set_actor_label("TUN_Platform"); a.set_folder_path("Zones/Edit/Tunnels/Structure")
        a.set_editor_property("is_spatially_loaded", False)
        o, e = a.get_actor_bounds(False)
        L.append("pose : z %.0f..%.0f  y %.0f..%.0f  mat=%s" % (o.z-e.z, o.z+e.z, o.y-e.y, o.y+e.y, MAT))
    unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
    L.append("TERMINE")
except Exception:
    L.append(traceback.format_exc())
open(r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools\tun_platform_log.txt", "w").write("\n".join(L))
