# Remet TOUTE la zone 1v1 au meme endroit (centre -20000, 0) :
#  1. rebuild_1v1.py : plateforme, anneau, rampes, lumieres + arrivee / retour lobby
#  2. explosif du RESET et ciel (Skydome) recentres sur l'arene
#  3. build_panel.py + wire_panel.py : panneau a cote des rampes
#  4. "toujours charge" pour tout ZONE_1v1*
import unreal, traceback
TOOLS = r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools"
CX, CY, FLOOR_Z = -20000.0, 0.0, 1270.0
L = []
def run(name):
    path = TOOLS + "\\" + name
    exec(compile(open(path, encoding="utf-8").read(), path, "exec"), {"__name__": "__main__", "__file__": path})
    L.append("execute " + name)
try:
    run("rebuild_1v1.py")
    eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    for a in eas.get_all_level_actors():
        lab = a.get_actor_label()
        if lab == "ZONE_1v1P_ResetExplosive":
            a.set_actor_location(unreal.Vector(CX, CY, FLOOR_Z + 300), False, False)
        elif lab == "ZONE_1v1P_Sky":
            a.set_actor_location(unreal.Vector(CX, CY, FLOOR_Z), False, False)
        elif lab.startswith("ZONE_1v1") and abs(a.get_actor_location().x - CX) > 15000:
            # devices restes a l'ancien emplacement (selecteurs, HUD...) : on les rapproche
            p = a.get_actor_location()
            a.set_actor_location(unreal.Vector(p.x + (35000 if p.x < CX else -35000), p.y, p.z), False, False)
            L.append("rapproche " + lab)
    run("build_panel.py")
    run("wire_panel.py")
    n = 0
    for a in eas.get_all_level_actors():
        if a.get_actor_label().startswith("ZONE_1v1") and a.get_editor_property("is_spatially_loaded"):
            a.set_editor_property("is_spatially_loaded", False); n += 1
    L.append("toujours charges : %d" % n)
    unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
    L.append("TERMINE")
except Exception:
    L.append(traceback.format_exc())
open(TOOLS + r"\fix_1v1_all_log.txt", "w").write("\n".join(L))
