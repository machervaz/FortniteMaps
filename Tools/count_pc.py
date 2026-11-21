import unreal, collections
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
c = collections.Counter()
for a in eas.get_all_level_actors():
    p = a.get_actor_location()
    if 20000 < p.x < 34000 and -12500 < p.y < -500 and not a.get_actor_label().startswith("PCX_"):
        c[a.get_class().get_name()] += 1
open(r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools\count_pc_log.txt", "w").write("\n".join("%5d %s" % (n, k) for k, n in c.most_common()))
