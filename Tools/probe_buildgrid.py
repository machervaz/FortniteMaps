import unreal
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
L = []
for a in eas.get_all_level_actors():
    lab = a.get_actor_label()
    p = a.get_actor_location()
    if lab.startswith("BUILD_") or (a.get_class().get_name().startswith("PBWA_") and 13000 < p.x < 27000 and 21000 < p.y < 29000):
        o, e = a.get_actor_bounds(False)
        r = a.get_actor_rotation()
        L.append("%-22s %-22s loc(%.0f,%.0f,%.0f) x %.0f..%.0f y %.0f..%.0f z %.0f..%.0f rot(p%.0f y%.0f r%.0f)" % (
            lab[:22], a.get_class().get_name()[:22], p.x, p.y, p.z, o.x - e.x, o.x + e.x, o.y - e.y, o.y + e.y, o.z - e.z, o.z + e.z, r.pitch, r.yaw, r.roll))
open(r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools\probe_buildgrid_log.txt", "w").write("\n".join(sorted(L)))
