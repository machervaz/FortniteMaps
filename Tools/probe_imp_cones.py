import unreal, traceback, collections
L = []
try:
    eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    rows = []
    for a in eas.get_all_level_actors():
        n = a.get_class().get_name()
        if not n.startswith("PBWA_W1_Roof"): continue
        p = a.get_actor_location()
        if 1000 < p.x < 2100 and -48000 < p.y < -22000:
            rows.append((p.y, p.z, p.x, a.get_actor_rotation().yaw, a.get_actor_label(), n))
    rows.sort(key=lambda r: (-r[0], r[1]))
    for r in rows:
        L.append("y=%.0f z=%.0f x=%.0f yaw=%.0f %s %s" % r)
    # paires proches (moins d'une case)
    L.append("--- chevauchements")
    for i in range(len(rows)):
        for j in range(i + 1, len(rows)):
            a, b = rows[i], rows[j]
            if abs(a[0] - b[0]) < 300 and abs(a[1] - b[1]) < 300 and abs(a[2] - b[2]) < 300:
                L.append("%s  <->  %s  (dy=%.0f dz=%.0f dx=%.0f)" % (a[4], b[4], b[0] - a[0], b[1] - a[1], b[2] - a[2]))
except Exception:
    L.append(traceback.format_exc())
open(r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools\probe_imp_cones_log.txt", "w").write("\n".join(L))
