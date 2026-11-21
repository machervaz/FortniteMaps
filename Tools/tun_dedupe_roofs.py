# Tunnels : un seul toit (cone/pente) par emplacement. Si plusieurs toits ont le meme pivot,
# on garde le cone (RoofC) s'il y en a un, sinon la piece posee en premier ; on supprime les autres.
import unreal, traceback, collections, re
TOOLS = r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools"
L = []
def num(a):
    m = re.search(r"(\d+)$", a.get_actor_label())
    return int(m.group(1)) if m else 0
try:
    eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    groups = collections.defaultdict(list)
    for a in eas.get_all_level_actors():
        n = a.get_class().get_name()
        if not n.startswith("PBWA_W1_Roof"): continue
        p = a.get_actor_location()
        if not (-3500 < p.x < 3500 and -48000 < p.y < -22000): continue
        groups[(round(p.x / 16), round(p.y / 16), round(p.z / 16))].append(a)
    n_del = 0
    for key, lst in groups.items():
        if len(lst) < 2: continue
        lst.sort(key=lambda a: (not a.get_class().get_name().startswith("PBWA_W1_RoofC"), num(a)))
        keep = lst[0]
        for a in lst[1:]:
            L.append("supprime %s (garde %s) a (%d,%d,%d)" % (a.get_actor_label(), keep.get_actor_label(), key[0]*16, key[1]*16, key[2]*16))
            eas.destroy_actor(a); n_del += 1
    unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
    L.append("TERMINE : %d supprimes" % n_del)
except Exception:
    L.append(traceback.format_exc())
open(TOOLS + r"\tun_dedupe_roofs_log.txt", "w").write("\n".join(L))
