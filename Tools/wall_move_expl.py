import unreal, traceback
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
L = []
DX = 500.0
try:
    acts = eas.get_all_level_actors()
    with unreal.ScopedEditorTransaction("1v1 : mur d'armes eloigne + explosifs"):
        for a in acts:
            p = a.get_actor_location(); lab = a.get_actor_label()
            if lab == "ZONE_1v1_VitreArmes" or (a.get_class().get_name() == "BP_ItemContainer_C" and -19500 < p.x < -19400 and abs(p.y) < 300):
                a.modify(); a.set_actor_location(unreal.Vector(p.x + DX, p.y, p.z), False, False)
                for c in a.get_components_by_class(unreal.SceneComponent): c.modify()
                L.append("deplace %s -> x=%.0f" % (lab, p.x + DX))
        src = [a for a in acts if a.get_actor_label() == "ZONE_1v1P_ResetExplosive"][0]
        WX, WZ = -19440.0 + DX, 1780.0
        R = 12 * 512.0
        SPOTS = {"PX": (WX + R + 300, 0, WZ), "NX": (WX - R - 300, 0, WZ),
                 "PY": (WX, 256 + R + 300, WZ), "NY": (WX, -256 - R - 300, WZ),
                 "PZ": (WX, 0, 1920 + R + 300), "NZ": (WX, 0, 1642 - R - 300)}
        for g in range(3):
            for k, (x, y, z) in SPOTS.items():
                lab = "ZONE_1v1P_ResetExp_G%d_%s" % (g, k)
                if any(a.get_actor_label() == lab for a in acts):
                    continue
                n = eas.duplicate_actor(src, None, unreal.Vector(0, 0, 0))
                n.set_actor_location(unreal.Vector(x, y, z), False, False)
                n.set_actor_label(lab); n.set_folder_path("Zones/1v1/Panel/Reset")
                L.append("cree %s (%.0f,%.0f,%.0f)" % (lab, x, y, z))
    unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
    L.append("TERMINE")
except Exception:
    L.append(traceback.format_exc())
open(r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools\wall_move_expl_log.txt","w").write("\n".join(L))
