# Les deplacements faits par set_actor_location sans transaction ne partent pas
# dans la session. On re-applique la position de chaque acteur de l'arene 1v1
# dans une transaction editeur (modify + petit aller-retour) pour qu'ils soient envoyes.
import unreal, traceback
TOOLS = r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools"
EXTRA = ("ZONE_1v1_Arrival", "ZONE_1v1_ReturnHolo", "ZONE_1v1_ReturnSocle", "ZONE_1v1_ReturnTitle",
         "ZONE_1v1_ReturnZone", "ZONE_1v1_Title", "ZONE_1v1_Welcome")
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
L = []
try:
    acts = [a for a in eas.get_all_level_actors()
            if a.get_actor_label().startswith(("ZONE_1v1N_", "ZONE_1v1P_")) or a.get_actor_label() in EXTRA]
    with unreal.ScopedEditorTransaction("Monter arene 1v1") as t:
        for a in acts:
            a.modify()
            p = a.get_actor_location()
            a.set_actor_location(unreal.Vector(p.x, p.y, p.z + 1.0), False, False)
            a.set_actor_location(p, False, False)
            for c in a.get_components_by_class(unreal.SceneComponent):
                c.modify()
    eas.set_selected_level_actors(acts)
    L.append("%d acteurs touches" % len(acts))
    unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
    L.append("TERMINE")
except Exception:
    L.append(traceback.format_exc())
open(TOOLS + r"\touch_1v1_log.txt", "w").write("\n".join(L))
