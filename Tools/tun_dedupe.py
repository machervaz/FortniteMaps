# Tunnels : supprime les pieces en bois en double (meme classe, meme position, meme rotation).
# Garde de preference la piece posee au telephone (sinon la premiere).
import unreal, traceback, collections
TOOLS = r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools"
DRY = False
L = []
try:
    eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    groups = collections.defaultdict(list)
    for a in eas.get_all_level_actors():
        n = a.get_class().get_name()
        if not n.startswith("PBWA_"): continue
        p = a.get_actor_location()
        if not (-3500 < p.x < 3500 and -48000 < p.y < -22000): continue
        r = a.get_actor_rotation()
        key = (n, round(p.x / 16), round(p.y / 16), round(p.z / 16), round(((r.yaw % 360) + 360) % 360 / 10) % 36)
        groups[key].append(a)
    gone = collections.Counter()
    for key, lst in groups.items():
        if len(lst) < 2: continue
        lst.sort(key=lambda a: a.get_actor_label().startswith("TUN_"))   # pieces du joueur d'abord
        keep = lst[0]
        for a in lst[1:]:
            L.append("doublon : %s (garde %s) a (%d,%d,%d)" % (a.get_actor_label(), keep.get_actor_label(), key[1]*16, key[2]*16, key[3]*16))
            t = "IMPOSSIBLE" if key[1]*16 > 1000 else "DIFFICILE" if key[1]*16 > 0 else "MOYEN" if key[1]*16 > -1000 else "FACILE"
            gone[(t, key[0])] += 1
            if not DRY: eas.destroy_actor(a)
    L.append("resume : " + str(dict(gone)))
    if not DRY: unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
    L.append("TERMINE")
except Exception:
    L.append(traceback.format_exc())
open(TOOLS + r"\tun_dedupe_log.txt", "w").write("\n".join(L))
