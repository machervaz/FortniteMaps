# Monte l'arene 1v1 (disque, LEDs, rampes, panneau, retour lobby...) pour que le
# dessus du disque soit sur la grille de construction Fortnite (multiples de 384 cm) :
# 1270 -> 1536. Les constructions se posent alors pile sur le disque.
# Le sol colore (SkyFloor), la voute et les devices caches ne bougent pas.
# La zone de chute est recalee entre le sol et le dessous du disque.
import unreal, traceback
TOOLS = r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools"
OLD_TOP, NEW_TOP = 1270.0, 1536.0
D = NEW_TOP - OLD_TOP
KEEP = ("ZONE_1v1P_SkyFloor", "ZONE_1v1P_FallZone", "ZONE_1v1P_SkyVault", "ZONE_1v1P_PMTemplate")
EXTRA = ("ZONE_1v1_Arrival", "ZONE_1v1_ReturnHolo", "ZONE_1v1_ReturnSocle", "ZONE_1v1_ReturnTitle",
         "ZONE_1v1_ReturnZone", "ZONE_1v1_Title", "ZONE_1v1_Welcome")
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
L = []
try:
    ACT = {a.get_actor_label(): a for a in eas.get_all_level_actors()}
    disc = ACT["ZONE_1v1N_Disc"]
    o, e = disc.get_actor_bounds(False)
    if abs((o.z + e.z) - OLD_TOP) > 5:
        raise Exception("disque deja deplace ? dessus=%.0f" % (o.z + e.z))
    n = 0
    for lab, a in ACT.items():
        if (lab.startswith("ZONE_1v1N_") or lab.startswith("ZONE_1v1P_") or lab in EXTRA) and lab not in KEEP:
            p = a.get_actor_location()
            a.set_actor_location(unreal.Vector(p.x, p.y, p.z + D), False, False)
            n += 1
    L.append("%d acteurs montes de %.0f cm" % (n, D))
    o, e = disc.get_actor_bounds(False)
    L.append("disque z=[%.0f..%.0f]" % (o.z - e.z, o.z + e.z))
    # zone de chute : du sol (1200) jusqu'a 1450 (sous le disque a 1536)
    z = ACT["ZONE_1v1P_FallZone"]
    o, e = z.get_actor_bounds(False)
    s = z.get_actor_scale3d()
    lo, hi = 1190.0, 1450.0
    z.set_actor_scale3d(unreal.Vector(s.x * 17000.0 / e.x, s.y * 17000.0 / e.y, s.z * (hi - lo) / (2 * e.z)))
    o, e = z.get_actor_bounds(False)
    p = z.get_actor_location()
    z.set_actor_location(unreal.Vector(p.x - o.x + (-20000.0), p.y - o.y, p.z + lo - (o.z - e.z)), False, False)
    o, e = z.get_actor_bounds(False)
    L.append("zone de chute z=[%.0f..%.0f] r=%.0f" % (o.z - e.z, o.z + e.z, max(e.x, e.y)))
    unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
    L.append("TERMINE")
except Exception:
    L.append(traceback.format_exc())
open(TOOLS + r"\move_1v1_up_log.txt", "w").write("\n".join(L))
