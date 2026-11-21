# GLIDE : arene plus haute (4000 -> 8000) + zone de chute libre dans le haut de l'arene
import unreal, traceback
L = []
FLOOR, DZ = 1270.0, 4000.0
try:
    eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    ar = unreal.AssetRegistryHelpers.get_asset_registry()
    cls = None
    for ad in ar.get_assets_by_class(unreal.TopLevelAssetPath("/Script/Engine", "BlueprintGeneratedClass"), True):
        nm = str(ad.asset_name)
        if "skydive" in nm.lower() and nm.startswith("Device_"):
            L.append("classe : %s.%s" % (ad.package_name, nm))
            cls = cls or "%s.%s" % (ad.package_name, nm)
    ACT = {a.get_actor_label(): a for a in eas.get_all_level_actors()}
    if ACT["AIM_Glide_WallN"].get_actor_scale3d().z < 50:
        with unreal.ScopedEditorTransaction("Glide plus haut"):
            for s in "NSEW":
                a = ACT["AIM_Glide_Wall" + s]; a.modify()
                sc = a.get_actor_scale3d(); hh = sc.z * 100 + DZ; p = a.get_actor_location()
                a.set_actor_location(unreal.Vector(p.x, p.y, FLOOR + hh / 2), False, False)
                a.set_actor_scale3d(unreal.Vector(sc.x, sc.y, hh / 100))
            for lab in ["AIM_Glide_Roof"] + ["AIM_Glide_TopLed" + s for s in "NSEW"] + ["AIM_Glide_Light%d" % i for i in range(4)]:
                a = ACT[lab]; a.modify(); p = a.get_actor_location()
                a.set_actor_location(unreal.Vector(p.x, p.y, p.z + DZ), False, False)
        L.append("arene remontee de %d" % DZ)
    for lab, a in ACT.items():
        if lab == "AIM_Glide_Skydive":
            eas.destroy_actor(a)
    v = eas.spawn_actor_from_class(unreal.load_class(None, cls), unreal.Vector(0, 68500, FLOOR + 3000))
    v.set_actor_label("AIM_Glide_Skydive"); v.set_folder_path("Zones/Aim/Glide")
    v.set_editor_property("is_spatially_loaded", False)
    o, e = v.get_actor_bounds(False); s = v.get_actor_scale3d()
    L.append("volume de base : ext=(%.0f,%.0f,%.0f) scale=%s" % (e.x, e.y, e.z, s))
    # couvre x -3500..3500, y 65800..71300, z FLOOR+3000..FLOOR+7900
    tx, ty, tz = 7000.0, 5500.0, 4900.0
    v.set_actor_scale3d(unreal.Vector(s.x * tx / (2 * e.x), s.y * ty / (2 * e.y), s.z * tz / (2 * e.z)))
    o, e = v.get_actor_bounds(False); p = v.get_actor_location()
    v.set_actor_location(unreal.Vector(p.x + 0 - o.x, p.y + 68550 - o.y, p.z + (FLOOR + 3000 + tz / 2) - o.z), False, False)
    o, e = v.get_actor_bounds(False)
    L.append("volume : c=(%.0f,%.0f,%.0f) ext=(%.0f,%.0f,%.0f)" % (o.x, o.y, o.z, e.x, e.y, e.z))
    unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
    L.append("TERMINE")
except Exception:
    L.append(traceback.format_exc())
open(r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools\glide_skydive_log.txt", "w").write("\n".join(L))
