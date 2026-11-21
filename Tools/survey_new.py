# Repere les ajouts du joueur : zones d'alteration dans les arenes Aim, composants dans Piece Control
import unreal, traceback, collections
TOOLS = r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools"
MINE = ("ZONE_", "LOBBY_", "TUN_", "AIM_", "PCX_", "PROBE_")
ARENAS = {"Launch": (-5500, 5500, 28500, 39500), "Bounce": (-4500, 4500, 39500, 48300), "Circuit": (-4000, 4000, 48300, 56000)}
PC = (20000, 34000, -12500, -500)
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
L = []
try:
    pc_classes = collections.Counter()
    for a in eas.get_all_level_actors():
        lab = a.get_actor_label()
        if lab.startswith(MINE):
            continue
        p = a.get_actor_location()
        n = a.get_class().get_name()
        for k, (x0, x1, y0, y1) in ARENAS.items():
            if x0 < p.x < x1 and y0 < p.y < y1:
                o, e = a.get_actor_bounds(False)
                L.append("AIM %s : %s (%s) loc=(%.0f,%.0f,%.0f) z=[%.0f..%.0f] taille=(%.0f,%.0f)" % (k, lab, n, p.x, p.y, p.z, o.z - e.z, o.z + e.z, 2 * e.x, 2 * e.y))
        if PC[0] < p.x < PC[1] and PC[2] < p.y < PC[3]:
            pc_classes[n] += 1
    L.append("== Piece Control, classes :")
    for n, c in pc_classes.most_common():
        L.append("   %5d %s" % (c, n))
except Exception:
    L.append(traceback.format_exc())
open(TOOLS + r"\survey_new_log.txt", "w").write("\n".join(L))
