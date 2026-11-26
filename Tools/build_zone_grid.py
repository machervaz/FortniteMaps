# Zone BUILD sur la grille de construction : sol a 1152 (3 etages de 384), centre sur une case
# (19968, 25088 = multiples de 512), sol de 25 x 13 cases. + balise chevron rouge pour les bots.
import unreal, traceback
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
V = lambda x, y, z: unreal.Vector(float(x), float(y), float(z))
L = []
try:
    ACT = {a.get_actor_label(): a for a in eas.get_all_level_actors()}
    DX, DY, DZ = 19968.0 - 20000.0, 25088.0 - 25000.0, 1152.0 - 1270.0
    with unreal.ScopedEditorTransaction("Zone BUILD sur la grille"):
        if ACT["BUILD_Floor"].get_actor_location().z > 1140:
            for lab, a in ACT.items():
                if lab.startswith("BUILD_"):
                    a.modify()
                    p = a.get_actor_location()
                    a.set_actor_location(V(p.x + DX, p.y + DY, p.z + DZ), False, False)
            L.append("zone decalee")
        CX, CY, TOP = 19968.0, 25088.0, 1152.0
        W, H = 25 * 512.0, 13 * 512.0
        f = ACT["BUILD_Floor"]
        f.set_actor_location(V(CX, CY, TOP - 25), False, False)
        f.set_actor_scale3d(V(W / 100.0, H / 100.0, 0.5))
        for sx in (-1, 1):
            ACT["BUILD_LedX%d" % sx].set_actor_location(V(CX + sx * (W / 2 - 10), CY, TOP + 1), False, False)
            ACT["BUILD_LedX%d" % sx].set_actor_scale3d(V(0.2, H / 100.0, 0.02))
            ACT["BUILD_LedY%d" % sx].set_actor_location(V(CX, CY + sx * (H / 2 - 10), TOP + 1), False, False)
            ACT["BUILD_LedY%d" % sx].set_actor_scale3d(V(W / 100.0, 0.2, 0.02))
        if "BUILD_BotBeacon" not in ACT:
            b = eas.spawn_actor_from_class(unreal.load_class(None, "/CreativeCoreDevices/AlwaysCook/Device_Beacon_V2_Chevron_Red.Device_Beacon_V2_Chevron_Red_C"),
                                           V(CX, CY, 3000), unreal.Rotator(0, 0, 0))
            b.set_actor_label("BUILD_BotBeacon")
            b.set_folder_path("Zones/Build")
            b.set_editor_property("is_spatially_loaded", False)
            ACT["BUILD_BotBeacon"] = b
        o, e = f.get_actor_bounds(False)
        L.append("sol : x %.0f..%.0f  y %.0f..%.0f  dessus %.0f" % (o.x - e.x, o.x + e.x, o.y - e.y, o.y + e.y, o.z + e.z))
        eas.set_selected_level_actors([ACT["BUILD_AirBots"]])
    unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
    L.append("OK")
except Exception:
    L.append(traceback.format_exc())
open(r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools\build_zone_grid_log.txt", "w").write("\n".join(L))
