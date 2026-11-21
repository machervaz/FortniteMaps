# Builds infinis + munitions infinies sur les 4 classes de la zone 1v1
# (le joueur recoit la classe 100 % en arrivant, puis 75/50/25 % via le panneau)
import unreal, traceback
OUT = r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools\infinite_1v1_log.txt"
PROPS = {"bInfiniteBuildingResources_Override": True, "bInfiniteBuildingResources": True,
         "bInfiniteAmmo_Override": True, "bInfiniteAmmo": True}
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
L = []
try:
    for a in eas.get_all_level_actors():
        lab = a.get_actor_label()
        if not (lab.startswith("ZONE_1v1_Speed") and lab.endswith("_ClassDesigner")):
            continue
        done = []
        for h in [a] + list(a.get_components_by_class(unreal.ActorComponent)):
            for k, v in PROPS.items():
                if k in done:
                    continue
                try:
                    h.set_editor_property(k, v); done.append(k)
                except Exception:
                    pass
        L.append("%s : %s" % (lab, done))
    unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
except Exception:
    L.append(traceback.format_exc())
open(OUT, "w").write("\n".join(L))
