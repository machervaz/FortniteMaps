import unreal
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
L = []
xs = []
for a in eas.get_all_level_actors():
    l = a.get_actor_label()
    if l.startswith("ZONE_1v1"):
        p = a.get_actor_location()
        xs.append((round(p.x / 5000) * 5000, l))
        if any(k in l for k in ("Disc", "Ramp1", "Arrival", "ReturnSocle", "ReturnZone", "Board", "ResetExplosive", "1v1P_Sky", "Loadout", "Welcome")):
            L.append("%s (%.0f, %.0f, %.0f)" % (l, p.x, p.y, p.z))
from collections import Counter
L.append("repartition X : %s" % Counter(x for x, _ in xs))
L.append("loin : %s" % [l for x, l in xs if abs(x + 20000) > 10000])
open(r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools\diag_1v1_out.txt", "w").write("\n".join(sorted(L)))
