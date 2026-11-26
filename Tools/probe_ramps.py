import unreal
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
L = []
for a in eas.get_all_level_actors():
    lab = a.get_actor_label(); p = a.get_actor_location()
    if lab.startswith("ZONE_1v1N_Ramp") or lab in ("ZONE_1v1P_Board", "ZONE_1v1_VitreArmes", "ZONE_1v1P_Post1", "ZONE_1v1P_Post-1", "ZONE_1v1N_Disc", "ZONE_1v1_Arrival") or (a.get_class().get_name() == "BP_ItemContainer_C" and -21000 < p.x < -18000):
        o, e = a.get_actor_bounds(False); r = a.get_actor_rotation(); s = a.get_actor_scale3d()
        L.append("%s | loc (%.0f,%.0f,%.0f) rot (p%.0f y%.0f r%.0f) scale (%.2f,%.2f,%.2f) | x %.0f..%.0f y %.0f..%.0f z %.0f..%.0f" % (lab, p.x, p.y, p.z, r.pitch, r.yaw, r.roll, s.x, s.y, s.z, o.x-e.x, o.x+e.x, o.y-e.y, o.y+e.y, o.z-e.z, o.z+e.z))
open(r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools\probe_ramps_log.txt","w").write("\n".join(sorted(L)))
