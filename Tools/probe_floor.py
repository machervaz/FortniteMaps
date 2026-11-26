import unreal, collections
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
L = []; c = collections.Counter(); fl = collections.Counter()
for a in eas.get_all_level_actors():
    p = a.get_actor_location(); n = a.get_class().get_name()
    if -3200 < p.x < 3200 and -47700 < p.y < -22000 and 0 < p.z < 2000:
        c[(n, int(round(p.z)))] += 1
        if n.startswith("PBWA_W1_Floor") and p.z < 1300:
            fl[int(round(p.x/512.0))] += 1
for k, v in sorted(c.items(), key=lambda kv: kv[0][1]): L.append("%5d z=%d %s" % (v, k[1], k[0]))
L.append("sols bois z<1300 par colonne x/512 : %s" % sorted(fl.items()))
open(r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools\probe_floor_log.txt","w").write("\n".join(L))
