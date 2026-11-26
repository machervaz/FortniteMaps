import unreal, traceback
L = []
FLOOR, CELL, LH, Y0 = 1270.0, 512.0, 384.0, -23296.0
def rep(b, n): return b * n
TUNNELS = [
    ("FACILE", -1536.0, ["W", "", "U", "W", "", "C", "W", "D", "", "W", "U", "S", "W", "", "WD", "W", "C", "W", "", ""]),
    ("MOYEN", -512.0, ["W", "W", "U", "WC", "WU", "W", "S", "WD", "W", "C", "WU", "W", "S", "WC", "WD", "W", "WD",
                       "W", "C", "WS", "WU", "W", "WD", "C", "W", "S", "W", ""]),
    ("DIFFICILE", 512.0, rep(["WS", "WU", "WC", "WS", "WD", "WC", "WU", "WS", "WD"], 4)),
    ("IMPOSSIBLE", 1536.0, rep(["WS", "WU", "WC", "WU", "WS", "WD", "WC", "WD", "WC", "WU", "WD"], 4)),
]
try:
    eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    ACT = {a.get_actor_label(): a for a in eas.get_all_level_actors()}
    W = unreal.load_class(None, "/CRD_VolumetricRegion/_Verse.mutator_zone_device")
    with unreal.ScopedEditorTransaction("Tunnels : temps intermediaires"):
        for name, X, seq in TUNNELS:
            s = ACT["TUN_%s_Chrono" % name].get_editor_property("Script")
            src = s.get_editor_property("__verse_0x5CFF7AE4_StartTrigger").get_editor_property("SavedActor")
            lvl, levels = 0, []
            for tok in seq:
                levels.append(lvl)
                lvl += 1 if "U" in tok else (-1 if "D" in tok else 0)
            n = len(seq)
            objs = []
            for j, k in enumerate((n // 3, (2 * n) // 3)):
                lab = "TUN_%s_Split%d" % (name, j + 1)
                a = ACT.get(lab)
                if not a:
                    a = eas.duplicate_actor(src, None, unreal.Vector(0, 0, 0))
                    a.set_actor_label(lab); a.set_folder_path("Zones/Edit/Tunnels/%s/Chrono" % name.capitalize())
                a.set_actor_scale3d(unreal.Vector(0.65, 0.6, 1.5))
                a.set_actor_location(unreal.Vector(X, Y0 - k * CELL - CELL / 2, FLOOR + levels[k] * LH + 432), False, False)
                o = unreal.new_object(W, s); o.set_editor_property("SavedActor", a); objs.append(o)
                L.append("%s cellule %d niveau %d" % (lab, k, levels[k]))
            s.set_editor_property("__verse_0xFA6B308F_Checkpoints", objs)
    unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
    L.append("TERMINE")
except Exception:
    L.append(traceback.format_exc())
open(r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools\tun_splits_log.txt", "w").write("\n".join(L))
