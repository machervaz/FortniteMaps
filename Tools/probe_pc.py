import unreal, traceback, collections
L = []
try:
    eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    mn = [1e9]*3; mx = [-1e9]*3
    cnt = collections.Counter()
    for a in eas.get_all_level_actors():
        p = a.get_actor_location()
        if not (15000 < p.x < 40000 and -16000 < p.y < 3000): continue
        lab = a.get_actor_label(); n = a.get_class().get_name()
        cnt[n[:30]] += 1
        o, e = a.get_actor_bounds(False)
        if e.x > 20000 or e.y > 20000: 
            L.append("GRAND : %s %s c=(%.0f,%.0f,%.0f) ext=(%.0f,%.0f,%.0f)" % (lab, n, o.x, o.y, o.z, e.x, e.y, e.z)); continue
        for i, (c, ex) in enumerate(((o.x, e.x), (o.y, e.y), (o.z, e.z))):
            mn[i] = min(mn[i], c - ex); mx[i] = max(mx[i], c + ex)
        if lab.startswith("ZONE_PieceControl") or "Floor" in lab or "Wall" in lab or "Roof" in lab or (e.x > 1500 or e.y > 1500):
            L.append("%s | %s | c=(%.0f,%.0f,%.0f) ext=(%.0f,%.0f,%.0f)" % (lab, n, o.x, o.y, o.z, e.x, e.y, e.z))
    L.append("BOITE min=%s max=%s" % ([round(v) for v in mn], [round(v) for v in mx]))
    L.append(str(cnt.most_common(15)))
except Exception:
    L.append(traceback.format_exc())
open(r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools\probe_pc_log.txt", "w").write("\n".join(L))
