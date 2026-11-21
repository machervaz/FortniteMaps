# Salle DOUBLE PUMP : 4 sentinelles (Sentry device), une par coin, a la place des Target Dummies
import unreal, math, traceback
L = []
CX, CY, FLOOR, C = 0.0, 60000.0, 1270.0, 170.0
try:
    ar = unreal.AssetRegistryHelpers.get_asset_registry()
    cls_path = "/CRD_SentryDevice/Actors/Device_Sentry_Prop_V2.Device_Sentry_Prop_V2_C"
    for path in ():
        for ad in ar.get_assets(unreal.ARFilter(package_paths=[path], recursive_paths=True)):
            nm = str(ad.asset_name)
            if "sentry" in nm.lower() and nm.startswith("Device_") and str(ad.asset_class_path.asset_name) == "BlueprintGeneratedClass":
                L.append("classe trouvee : %s.%s" % (ad.package_name, nm))
                cls_path = cls_path or "%s.%s" % (ad.package_name, nm)
    eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    for a in eas.get_all_level_actors():
        if a.get_actor_label().startswith(("AIM_Pump_Dummy", "AIM_Pump_Up", "AIM_Pump_Down", "AIM_Pump_Sentry")):
            eas.destroy_actor(a)
    for i, (dx, dy) in enumerate([(-C, -C), (C, -C), (C, C), (-C, C)]):
        yaw = math.degrees(math.atan2(-dy, -dx))
        s = eas.spawn_actor_from_class(unreal.load_class(None, cls_path), unreal.Vector(CX + dx, CY + dy, FLOOR), unreal.Rotator(roll=0, pitch=0, yaw=yaw))
        s.set_actor_label("AIM_Pump_Sentry%d" % i)
        s.set_folder_path("Zones/Aim/Pump")
        s.set_editor_property("is_spatially_loaded", False)
    unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
    L.append("TERMINE")
except Exception:
    L.append(traceback.format_exc())
open(r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools\pump_sentries_log.txt", "w").write("\n".join(L))
