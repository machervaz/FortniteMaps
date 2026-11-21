# Le joueur apparait tourne vers -X avec le spawner a 0 deg : on le tourne de 180 deg
# pour arriver face aux 4 portails (mur +X). Transaction -> envoye a la session.
import unreal, traceback
L = []
try:
    eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    with unreal.ScopedEditorTransaction("Spawn face aux portails"):
        for a in eas.get_all_level_actors():
            if a.get_actor_label() == "LOBBY_PlayerSpawner":
                a.modify()
                for c in a.get_components_by_class(unreal.SceneComponent):
                    c.modify()
                a.set_actor_rotation(unreal.Rotator(roll=0.0, pitch=0.0, yaw=180.0), False)
                L.append("spawner rot=%s" % a.get_actor_rotation())
    unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
    L.append("TERMINE")
except Exception:
    L.append(traceback.format_exc())
open(r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools\spawn_face_portals_log.txt", "w").write("\n".join(L))
