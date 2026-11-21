# Remet toute la zone 1v1 (ZONE_1v1*) a son emplacement d'origine (centre -20000, 0).
# Les acteurs restes vers -55000 sont decales de +35000 en X ; le panneau suit
# l'arene et reste a cote des rampes.
import unreal, os, traceback
TOOLS = r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools"
DX = 35000.0
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
L = []
try:
    n = 0
    for a in eas.get_all_level_actors():
        if a.get_actor_label().startswith("ZONE_1v1"):
            p = a.get_actor_location()
            if p.x < -40000:
                a.set_actor_location(unreal.Vector(p.x + DX, p.y, p.z), False, False)
                n += 1
    L.append("acteurs remis a l'origine : %d" % n)
    if os.path.exists(TOOLS + r"\move_1v1_done.txt"):
        os.remove(TOOLS + r"\move_1v1_done.txt")
    unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
except Exception:
    L.append(traceback.format_exc())
open(TOOLS + r"\move_1v1_back_log.txt", "w").write("\n".join(L))
