# Repose les pieces d'origine des tunnels qui ont disparu (plan de build_tunnels.py, sol remonte a 1270).
# Ne pose rien si une piece de la meme famille est deja a cet endroit. Ajout au reset + support force.
import unreal, collections, traceback
TOOLS = r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools"
FLOOR, CELL, LH, Y0 = 1270.0, 512.0, 384.0, -23296.0
def rep(b, n): return b * n
TUNNELS = [
    ("FACILE", -1536.0, ["W", "", "U", "W", "", "C", "W", "D", "", "W", "U", "S", "W", "", "WD", "W", "C", "W", "", ""]),
    ("MOYEN", -512.0, ["W", "W", "U", "WC", "WU", "W", "S", "WD", "W", "C", "WU", "W", "S", "WC", "WD", "W", "WD",
                       "W", "C", "WS", "WU", "W", "WD", "C", "W", "S", "W", ""]),
    ("DIFFICILE", 512.0, rep(["WS", "WU", "WC", "WS", "WD", "WC", "WU", "WS", "WD"], 4)),
    ("IMPOSSIBLE", 1536.0, rep(["WS", "WU", "WC", "WU", "WS", "WD", "WC", "WD", "WC", "WU", "WD"], 4)),
]
P = "/Game/Building/ActorBlueprints/Player/Wood/L1/%s.%s_C"
CLS = {"W": P % ("PBWA_W1_Solid", "PBWA_W1_Solid"), "S": P % ("PBWA_W1_StairW", "PBWA_W1_StairW"),
       "C": P % ("PBWA_W1_RoofC", "PBWA_W1_RoofC"), "F": P % ("PBWA_W1_Floor", "PBWA_W1_Floor")}
def family(clsname):
    n = clsname.replace("PBWA_W1_", "")
    if n.startswith("Roof"): return "C"
    if n.startswith("Stair"): return "S"
    if n.startswith("Floor"): return "F"
    return "W"            # murs et murs edites (fenetres, portes...)
L = []
try:
    eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    dls = unreal.get_editor_subsystem(unreal.DataLayerEditorSubsystem)
    dl = unreal.load_asset("/5622d7d7-d1ca-438f-8a48-1286a48e2471/Tunnels/DL_TunnelBuilds")
    inst = [i for i in dls.get_all_data_layers() if i.get_asset() == dl][0]
    actors = eas.get_all_level_actors()
    labels = set(a.get_actor_label() for a in actors)
    wood = [(a.get_actor_location(), family(a.get_class().get_name())) for a in actors if a.get_class().get_name().startswith("PBWA_")]
    def occupied(fam, x, y, z):
        return any(f == fam and abs(p.x - x) < 60 and abs(p.y - y) < 60 and abs(p.z - z) < 60 for p, f in wood)
    new = []; stats = collections.Counter()
    for name, X, seq in TUNNELS:
        cells = seq + ["#"]
        lvl, levels = 0, []
        for tok in cells:
            levels.append(lvl)
            lvl += 1 if "U" in tok else (-1 if "D" in tok else 0)
        yf = lambda k: Y0 - k * CELL
        folder = "Zones/Edit/Tunnels/%s/Builds" % name.capitalize()
        for k, tok in enumerate(cells):
            z = FLOOR + levels[k] * LH
            want = []
            if "W" in tok: want.append(("W", "%s_Wall%d" % (name, k), yf(k)))
            if "S" in tok or "U" in tok: want.append(("S", "%s_%s%d" % (name, "Ramp" if "U" in tok else "Stair", k), yf(k + 1)))
            if "C" in tok: want.append(("C", "%s_Cone%d" % (name, k), yf(k + 1)))
            if "D" in tok: want.append(("F", "%s_Hole%d" % (name, k), yf(k + 1)))
            for fam, lab, y in want:
                lab = "TUN_" + lab
                if lab in labels:
                    stats[(name, "deja la")] += 1; continue
                if occupied(fam, X, y, z):
                    stats[(name, "place prise")] += 1; continue
                a = eas.spawn_actor_from_class(unreal.load_class(None, CLS[fam]), unreal.Vector(X, y, z))
                a.set_actor_label(lab); a.set_folder_path(folder)
                a.set_editor_property("is_spatially_loaded", False)
                a.set_editor_property("forcibly_structurally_supported", True)
                new.append(a); wood.append((unreal.Vector(X, y, z), fam))
                stats[(name, "reposee")] += 1
    if new:
        L.append("ajout au reset : %s" % dls.add_actors_to_data_layer(new, inst))
    for k in sorted(stats):
        L.append("%s %s : %d" % (k[0], k[1], stats[k]))
    L.append("TOTAL reposees : %d" % len(new))
    unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
    L.append("TERMINE")
except Exception:
    L.append(traceback.format_exc())
open(TOOLS + r"\restore_tunnels_log.txt", "w").write("\n".join(L))
