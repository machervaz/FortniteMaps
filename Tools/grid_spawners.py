import unreal
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
X = -19400.0
ROWS = [  # (z de la base, armes de gauche a droite)
    (1790.0, [1, 4, 10, 11, 12, 14]),      # fusils d'assaut
    (1700.0, [16, 6, 2, 8, 9, 17]),        # fusil, pistolet, pompes speciaux
    (1610.0, [3, 5, 7, 13, 15]),           # pompes
]
by = {a.get_actor_label(): a for a in eas.get_all_level_actors()}
L = []
with unreal.ScopedEditorTransaction("1v1 : grille des armes"):
    for z, ids in ROWS:
        n = len(ids)
        for k, i in enumerate(ids):
            y = (k - (n - 1) / 2.0) * 115.0
            a = by["ZONE_1v1_Arme%d" % i]; a.modify()
            a.set_actor_location(unreal.Vector(X, y, z), False, False)
            L.append("Arme%d -> y=%.0f z=%.0f" % (i, y, z))
unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
open(r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools\grid_spawners_log.txt","w").write("\n".join(L))
v = by["ZONE_1v1_VitreArmes"]
with unreal.ScopedEditorTransaction("1v1 : vitre elargie"):
    v.modify()
    s = v.get_actor_scale3d()
    v.set_actor_scale3d(unreal.Vector(s.x, 700.0 / 100.0, 320.0 / 100.0))
    v.set_actor_location(unreal.Vector(-19456.0, 0.0, 1780.0), False, False)
o, e = v.get_actor_bounds(False)
L.append("vitre : y %.0f..%.0f z %.0f..%.0f" % (o.y - e.y, o.y + e.y, o.z - e.z, o.z + e.z))
unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
open(r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools\grid_spawners_log.txt","w").write("\n".join(L))
