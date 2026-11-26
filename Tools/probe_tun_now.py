import unreal, collections
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
c = collections.Counter(); sp = collections.Counter(); outside = 0
for a in eas.get_all_level_actors():
    n = a.get_class().get_name()
    if not n.startswith("PBWA_"): continue
    p = a.get_actor_location()
    if -3500 < p.x < 3500 and -48000 < p.y < -22000:
        t = "FACILE" if p.x < -1000 else "MOYEN" if p.x < 0 else "DIFFICILE" if p.x < 1000 else "IMPOSSIBLE"
        c[t] += 1
        sp[a.get_editor_property("is_spatially_loaded")] += 1
open(r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools\probe_tun_now_log.txt", "w").write("%s\nspatial: %s\ntotal acteurs charges: %d" % (dict(c), dict(sp), len(eas.get_all_level_actors())))
