import unreal, collections
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
L = []; c = collections.Counter()
for a in eas.get_all_level_actors():
    if a.get_class().get_name().startswith("PBWA_"):
        p = a.get_actor_location()
        if -3500 < p.x < 3500 and -48000 < p.y < -22000:
            c[a.get_class().get_name()] += 1
            if len(L) < 15: L.append("%s %s (%.0f,%.0f,%.0f) valide=%s" % (a.get_actor_label(), a.get_class().get_name(), p.x, p.y, p.z, unreal.SystemLibrary.is_valid(a)))
L.append(str(dict(c)))
open(r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools\probe_left_log.txt", "w").write("\n".join(L))
