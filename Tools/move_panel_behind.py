# Panneau 1v1 (ciel / RESET / vitesse) : recule derriere les rampes, au milieu du V
# (y=256), monte de 2,5 m pour depasser du haut des rampes, poteaux allonges jusqu'au disque.
# Textes : justification centree, centres sur leur forme et DEVANT les plaques de couleur.
# Transaction editeur (sinon le deplacement ne part pas dans la session).
import unreal, traceback
TOOLS = r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools"
DX, DY, DZ = -850.0, 256.0, 250.0
DISC_TOP = 1536.0
WIDGET_DZ = 82.0      # centre du texte = acteur billboard + 82 en z
WIDGET_DX = 9.0       # face du texte = acteur billboard + 9 en x
PARTS = ("Board", "Frame", "Post-1", "Post1", "SecSpeed")
TXT = {"ZONE_1v1P_TxtReset": ["ZONE_1v1P_SkinReset"], "ZONE_1v1P_TxtDown": ["ZONE_1v1P_SkinSpeedDown"],
       "ZONE_1v1P_TxtUp": ["ZONE_1v1P_SkinSpeedUp"],
       "ZONE_1v1P_SpeedDisplay": ["ZONE_1v1P_SkinSpeedDown", "ZONE_1v1P_SkinSpeedUp"]}
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
L = []

def touch(a):
    a.modify()
    for c in a.get_components_by_class(unreal.SceneComponent):
        c.modify()

try:
    ACT = {a.get_actor_label(): a for a in eas.get_all_level_actors()}
    board = ACT["ZONE_1v1P_Board"]
    if abs(board.get_actor_location().x - (-19550.0)) > 2:
        raise Exception("panneau deja deplace ? x=%.0f" % board.get_actor_location().x)
    moved = [ACT["ZONE_1v1P_" + p] for p in PARTS]
    moved += [a for l, a in ACT.items() if l.startswith(("ZONE_1v1P_Shape", "ZONE_1v1P_Skin", "ZONE_1v1P_SkyFrame"))]
    moved += [ACT[t] for t in TXT]
    with unreal.ScopedEditorTransaction("Panneau 1v1 derriere les rampes"):
        for a in moved:
            touch(a)
            p = a.get_actor_location()
            a.set_actor_location(unreal.Vector(p.x + DX, p.y + DY, p.z + DZ), False, False)
        L.append("%d acteurs deplaces" % len(moved))
        # poteaux : du disque jusque sous le cadre
        fo, fe = ACT["ZONE_1v1P_Frame"].get_actor_bounds(False)
        top = fo.z - fe.z + 5
        for p in ("Post-1", "Post1"):
            a = ACT["ZONE_1v1P_" + p]
            s = a.get_actor_scale3d()
            loc = a.get_actor_location()
            a.set_actor_scale3d(unreal.Vector(s.x, s.y, (top - DISC_TOP) / 100.0))
            a.set_actor_location(unreal.Vector(loc.x, loc.y, (top + DISC_TOP) / 2), False, False)
        # textes centres
        for t, skins in TXT.items():
            a = ACT[t]
            sk = [ACT[s].get_actor_location() for s in skins]
            ty = sum(v.y for v in sk) / len(sk)
            tz = sum(v.z for v in sk) / len(sk)
            tx = max(v.x for v in sk) + 2 + 4          # 4 cm devant la plaque
            a.set_actor_location(unreal.Vector(tx - WIDGET_DX, ty, tz - WIDGET_DZ), False, False)
            ok = None
            for val in (getattr(getattr(unreal, "TextJustify", None), "CENTER", None), "Center", 1):
                if val is None:
                    continue
                try:
                    a.set_editor_property("TextJustification", val)
                    ok = val
                    break
                except Exception as ex:
                    L.append("   %s justif %r : %s" % (t, val, ex))
            L.append("%s -> (%.0f,%.0f,%.0f) justif=%s" % (t, tx, ty, tz, ok))
    o, e = board.get_actor_bounds(False)
    L.append("tableau x=[%.0f..%.0f] y=[%.0f..%.0f] z=[%.0f..%.0f]" % (o.x - e.x, o.x + e.x, o.y - e.y, o.y + e.y, o.z - e.z, o.z + e.z))
    unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
    L.append("TERMINE")
except Exception:
    L.append(traceback.format_exc())
open(TOOLS + r"\move_panel_behind_log.txt", "w").write("\n".join(L))
