import unreal
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
L = []
for a in eas.get_all_level_actors():
    lab = a.get_actor_label()
    if lab.startswith("AIM_Hub_RiftPump") or lab.startswith("ZONE_AimWall") or lab.startswith("AIM_HubWall") or lab.startswith("ZONE_Aim_") or lab.startswith("AIM_Hub_RiftLaunch") or lab.startswith("AIM_Pump_Arrival") or lab.startswith("AIM_Pump_Wall") or lab.startswith("AIM_Pump_Floor") or lab.startswith("AIM_Pump_Roof"):
        o, e = a.get_actor_bounds(False); r = a.get_actor_rotation()
        L.append("%-32s %-30s c(%.0f,%.0f,%.0f) ext(%.0f,%.0f,%.0f) yaw%.0f %s" % (lab[:32], a.get_class().get_name()[:30], o.x, o.y, o.z, e.x, e.y, e.z, r.yaw, a.get_folder_path()))
open(r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools\probe_hub_log.txt","w").write("\n".join(sorted(L)))
