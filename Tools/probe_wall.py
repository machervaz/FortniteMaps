import unreal, collections
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
c = collections.Counter(); L = []
for a in eas.get_all_level_actors():
    p = a.get_actor_location()
    if -22500 < p.x < -17500 and -2500 < p.y < 2500 and 1000 < p.z < 3500 and not a.get_actor_label().startswith("ZONE_"):
        n = a.get_class().get_name()
        inv = "?"
        try: inv = a.get_editor_property("bIsInvulnerable")
        except Exception: pass
        c[(n, isinstance(a, unreal.BuildingActor), inv)] += 1
for k, v in sorted(c.items()): L.append("%4d %s buildingactor=%s invuln=%s" % (v, k[0], k[1], k[2]))
open(r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools\probe_wall_log.txt","w").write("\n".join(L))
