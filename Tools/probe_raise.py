import unreal, collections
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
zs = collections.Counter(); bad = []
for a in eas.get_all_level_actors():
    p = a.get_actor_location(); n = a.get_class().get_name()
    if -3200 < p.x < 3200 and -47700 < p.y < -23000 and n.startswith("PBWA_") and p.z > -10000:
        zs[int(round(p.z))] += 1
        try:
            if not a.get_editor_property("forcibly_structurally_supported"): bad.append(a.get_actor_label())
        except Exception: pass
open(r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools\probe_raise_log.txt","w").write("z: %s\nnon supportees: %d\nmin z: %s" % (sorted(zs.items())[:12], len(bad), min(zs) if zs else None))
