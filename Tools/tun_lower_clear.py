# Tunnels d'edit : supprime toutes les pieces en bois, puis redescend les tunnels de 118
# (sol 1270 -> 1152 : sur la grille de construction) pour construire au telephone.
# (Remonter ensuite avec tun_raise_keep.py : +118, pieces ajoutees au reset)
import unreal, traceback
TOOLS = r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools"
DZ = -118.0
BOX = (-3200, 3200, -47700, -23000)
L = []
try:
    eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    n = 0
    for a in eas.get_all_level_actors():
        if a.get_class().get_name().startswith("PBWA_"):
            p = a.get_actor_location()
            if -3500 < p.x < 3500 and -48000 < p.y < -22000:
                eas.destroy_actor(a); n += 1
    L.append("pieces en bois supprimees : %d" % n)
    moved = 0
    with unreal.ScopedEditorTransaction("Tunnels redescendus"):
        for a in eas.get_all_level_actors():
            lab = a.get_actor_label()
            p = a.get_actor_location()
            if lab.startswith("ZONE_") or not (BOX[0] < p.x < BOX[1] and BOX[2] < p.y < BOX[3]):
                continue
            if isinstance(a, unreal.WorldSettings) or a.get_class().get_name() in ("WorldDataLayers", "LevelBounds"):
                continue
            a.modify()
            for c in a.get_components_by_class(unreal.SceneComponent):
                c.modify()
            a.set_actor_location(unreal.Vector(p.x, p.y, p.z + DZ), False, False)
            moved += 1
    L.append("acteurs redescendus : %d" % moved)
    unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
    L.append("TERMINE")
except Exception:
    L.append(traceback.format_exc())
open(TOOLS + r"\tun_lower_clear_log.txt", "w").write("\n".join(L))
