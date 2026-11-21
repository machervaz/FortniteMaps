# Liste les acteurs que je n'ai pas crees (sans mes prefixes) pour trouver la zone du joueur
import unreal, traceback, collections
TOOLS = r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools"
MINE = ("ZONE_", "LOBBY_", "TUN_", "AIM_", "PROBE_")
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
L = []
try:
    groups = collections.defaultdict(list)
    for a in eas.get_all_level_actors():
        lab = a.get_actor_label()
        if lab.startswith(MINE):
            continue
        p = a.get_actor_location()
        key = (int(p.x // 10000), int(p.y // 10000))
        groups[key].append((a.get_class().get_name(), lab, p))
    for key, items in sorted(groups.items(), key=lambda kv: -len(kv[1])):
        cnt = collections.Counter(c for c, _, _ in items)
        xs = [p.x for _, _, p in items]; ys = [p.y for _, _, p in items]; zs = [p.z for _, _, p in items]
        L.append("case %s : %d acteurs  x[%.0f..%.0f] y[%.0f..%.0f] z[%.0f..%.0f]" % (key, len(items), min(xs), max(xs), min(ys), max(ys), min(zs), max(zs)))
        for c, n in cnt.most_common(12):
            L.append("     %4d  %s" % (n, c))
except Exception:
    L.append(traceback.format_exc())
open(TOOLS + r"\survey_user_log.txt", "w").write("\n".join(L))
