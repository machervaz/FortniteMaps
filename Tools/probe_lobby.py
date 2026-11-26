import unreal
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
L = []
for a in eas.get_all_level_actors():
    p = a.get_actor_location()
    if abs(p.x) < 2600 and abs(p.y) < 2600 and 1000 < p.z < 3500:
        o, e = a.get_actor_bounds(False); r = a.get_actor_rotation()
        L.append("%-34s %-34s c(%.0f,%.0f,%.0f) ext(%.0f,%.0f,%.0f) yaw%.0f" % (a.get_actor_label()[:34], a.get_class().get_name()[:34], o.x, o.y, o.z, e.x, e.y, e.z, r.yaw))
open(r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools\probe_lobby_log.txt","w").write("\n".join(sorted(L)))
