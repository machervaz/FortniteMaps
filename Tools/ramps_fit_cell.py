# Rampes 1v1 : tiennent entierement DANS leur case de grille (aucun debord sur les
# cases voisines, ou les constructions du joueur se poseraient), surface inchangee
# (1536 -> 1920 sur 512 cm). Rebords LED sans collision et a l'interieur de la case.
import unreal, traceback
TOOLS = r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools"
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
L = []
try:
    ACT = {a.get_actor_label(): a for a in eas.get_all_level_actors()}
    with unreal.ScopedEditorTransaction("Rampes 1v1 dans leur case"):
        for side in (1, -1):
            r = ACT["ZONE_1v1N_Ramp%d" % side]
            e = ACT["ZONE_1v1N_RampEdge%d" % side]
            for a in (r, e):
                a.modify()
                for c in a.get_components_by_class(unreal.SceneComponent):
                    c.modify()
            # longueur 640 -> 610, largeur 512 -> 500 (centre et pente inchanges)
            r.set_actor_scale3d(unreal.Vector(5.0, 6.10, 0.24))
            p = e.get_actor_location()
            e.set_actor_location(unreal.Vector(p.x, side * 503.0, p.z), False, False)
            e.set_actor_scale3d(unreal.Vector(5.0, 0.14, 0.16))
            for c in e.get_components_by_class(unreal.PrimitiveComponent):
                c.set_collision_profile_name("NoCollision")
            for a in (r, e):
                o, x = a.get_actor_bounds(False)
                L.append("%s x=[%.0f..%.0f] y=[%.0f..%.0f] z=[%.0f..%.0f]" % (a.get_actor_label(),
                         o.x - x.x, o.x + x.x, o.y - x.y, o.y + x.y, o.z - x.z, o.z + x.z))
    unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
    L.append("TERMINE")
except Exception:
    L.append(traceback.format_exc())
open(TOOLS + r"\ramps_fit_cell_log.txt", "w").write("\n".join(L))
