# Salle DOUBLE PUMP : 4 Target Dummies (mannequins sur socle), un par coin, tournes vers le centre
import unreal, math, traceback
L = []
CLS = "/CreativeCoreDevices/Device_TargetDummy_V2.Device_TargetDummy_V2_C"
CX, CY, FLOOR, C = 0.0, 60000.0, 1270.0, 170.0
try:
    eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    for a in eas.get_all_level_actors():
        if a.get_actor_label().startswith("AIM_Pump_Dummy"):
            eas.destroy_actor(a)
    corners = [(-C, -C), (C, -C), (C, C), (-C, C)]
    for i, (dx, dy) in enumerate(corners):
        yaw = math.degrees(math.atan2(-dy, -dx))          # regarde le centre
        d = eas.spawn_actor_from_class(unreal.load_class(None, CLS), unreal.Vector(CX + dx, CY + dy, FLOOR), unreal.Rotator(roll=0, pitch=0, yaw=yaw))
        d.set_actor_label("AIM_Pump_Dummy%d" % i)
        d.set_folder_path("Zones/Aim/Pump")
        d.set_editor_property("is_spatially_loaded", False)
        o, e = d.get_actor_bounds(False)
        L.append("dummy %d bounds c=(%.0f,%.0f,%.0f) ext=(%.0f,%.0f,%.0f)" % (i, o.x, o.y, o.z, e.x, e.y, e.z))
    unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
    L.append("TERMINE")
except Exception:
    L.append(traceback.format_exc())
open(r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools\pump_dummies_log.txt", "w").write("\n".join(L))
