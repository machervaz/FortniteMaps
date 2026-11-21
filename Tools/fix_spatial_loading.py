# Corrige les erreurs MapCheck "Acteur non charge dynamiquement ... se refere a
# Acteur charge dynamiquement" : les devices Verse sont toujours charges, donc
# tout ce qu'ils referencent (pads de teleport, zones, HUD, boutons...) doit
# l'etre aussi. Sinon la teleport vise un pad pas encore charge -> sous la map.
# On rend toujours charges tous les acteurs LOBBY_ / ZONE_ / TUN_ (sauf les
# pieces de construction des tunnels, gerees par le Data Layer).
import unreal, traceback
OUT = r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools\fix_spatial_loading_log.txt"
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
L, n, skip = [], 0, 0
try:
    for a in eas.get_all_level_actors():
        lab = a.get_actor_label()
        if not lab.startswith(("LOBBY_", "ZONE_", "TUN_")):
            continue
        if a.get_class().get_name().startswith("PBWA_"):
            skip += 1
            continue
        try:
            if a.get_editor_property("is_spatially_loaded"):
                a.set_editor_property("is_spatially_loaded", False)
                n += 1
        except Exception as e:
            L.append("echec %s : %s" % (lab, e))
    L.append("acteurs passes en 'toujours charges' : %d (pieces des tunnels ignorees : %d)" % (n, skip))
    unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
except Exception:
    L.append(traceback.format_exc())
open(OUT, "w").write("\n".join(L))
