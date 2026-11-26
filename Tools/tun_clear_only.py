# Tunnels d'edit : supprime toutes les pieces en bois (les tunnels restent en bas, sur la grille)
import unreal, traceback
L = []
try:
    eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    n = 0
    for a in eas.get_all_level_actors():
        if a.get_class().get_name().startswith("PBWA_"):
            p = a.get_actor_location()
            if -3500 < p.x < 3500 and -48000 < p.y < -22000:
                eas.destroy_actor(a); n += 1
    unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
    left = sum(1 for a in eas.get_all_level_actors() if a.get_class().get_name().startswith("PBWA_") and -3500 < a.get_actor_location().x < 3500 and -48000 < a.get_actor_location().y < -22000)
    L.append("supprimees : %d, restantes : %d" % (n, left))
except Exception:
    L.append(traceback.format_exc())
open(r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools\tun_clear_only_log.txt", "w").write("\n".join(L))
