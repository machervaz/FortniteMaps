# Les explosifs du RESET 1v1 detruisaient aussi les formes du panneau (props a
# 32 000 PV) : degats aux structures 100 000 dans 40 cases. On passe a 2 000
# (casse tous les builds joueurs, pas les formes) et 12 cases (~60 m).
import unreal, traceback
OUT = r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools\fix_reset_explosives_log.txt"
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
L = []
try:
    for a in eas.get_all_level_actors():
        lab = a.get_actor_label()
        if not lab.startswith("ZONE_1v1P_ResetExplosive"):
            continue
        for k, v in (("Structure Damage", 2000.0), ("Blast Radius", 12.0)):
            try:
                a.set_editor_property(k, v)
                L.append("%s %s=%s" % (lab, k, a.get_editor_property(k)))
            except Exception as e:
                L.append("%s %s ECHEC %s" % (lab, k, e))
    unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
except Exception:
    L.append(traceback.format_exc())
open(OUT, "w").write("\n".join(L))
