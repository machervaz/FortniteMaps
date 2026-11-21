# Remet les lignes de depart des tunnels au niveau du sol (elles n'avaient pas ete remontees : z 1153 -> sol 1270)
import unreal, traceback
L = []
try:
    eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    with unreal.ScopedEditorTransaction("Lignes de depart"):
        for a in eas.get_all_level_actors():
            if a.get_actor_label().endswith("_EntryLine") and a.get_actor_label().startswith("TUN_"):
                a.modify()
                for c in a.get_components_by_class(unreal.SceneComponent):
                    c.modify()
                p = a.get_actor_location()
                a.set_actor_location(unreal.Vector(p.x, p.y, 1271.0), False, False)
                L.append("%s : %.0f -> 1271" % (a.get_actor_label(), p.z))
    unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
    L.append("TERMINE")
except Exception:
    L.append(traceback.format_exc())
open(r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools\tun_entry_lines_log.txt", "w").write("\n".join(L))
