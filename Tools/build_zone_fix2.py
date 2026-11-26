# Zone BUILD : portail de retour remis dans la zone (il etait dans le hub Aim) + rampes calees
# sur la grille (decalage d'une demi-case en Y).
import unreal, traceback
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
V = lambda x, y, z: unreal.Vector(float(x), float(y), float(z))
L = []
try:
    ACT = {a.get_actor_label(): a for a in eas.get_all_level_actors()}
    with unreal.ScopedEditorTransaction("Zone BUILD : retour + rampes"):
        # retour : a gauche de l'arrivee (x 19968 - 1536), meme hauteur
        for part in ("Holo", "Socle", "Title", "Zone"):
            a = ACT["BUILD_Return" + part]
            a.modify()
            p = a.get_actor_location()
            a.set_actor_location(V(p.x - 1468.0 + 18432.0, p.y, p.z), False, False)
            L.append("%s -> x %.0f" % (a.get_actor_label(), a.get_actor_location().x))
        # rampes : bords sur les lignes de la grille (256 + 512k)
        for lab in ("BUILD_Ramp-1", "BUILD_Ramp1", "BUILD_RampEdge-1", "BUILD_RampEdge1"):
            a = ACT[lab]
            a.modify()
            o, e = a.get_actor_bounds(False)
            lo = o.y - e.y
            k = round((lo - 256.0) / 512.0)
            dy = (256.0 + 512.0 * k) - lo if "Edge" not in lab else 0.0
            if "Edge" in lab:
                # le rebord suit sa rampe
                dy = 256.0
            p = a.get_actor_location()
            a.set_actor_location(V(p.x, p.y + dy, p.z), False, False)
            o, e = a.get_actor_bounds(False)
            L.append("%s : y %.0f..%.0f z %.0f..%.0f" % (lab, o.y - e.y, o.y + e.y, o.z - e.z, o.z + e.z))
    unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
    L.append("OK")
except Exception:
    L.append(traceback.format_exc())
open(r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools\build_zone_fix2_log.txt", "w").write("\n".join(L))
