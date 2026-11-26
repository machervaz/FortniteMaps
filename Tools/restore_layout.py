import unreal
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
POS = [
    ('ZONE_1v1_Arme1', -19440.000000, -160.000000, 1750.000),
    ('ZONE_1v1_Arme2', -19440.000117, 192.000000, 1642.000),
    ('ZONE_1v1_Arme3', -19440.000000, 0.000117, 1690.000),
    ('ZONE_1v1_Arme4', -19440.000000, -112.000117, 1594.000),
    ('ZONE_1v1_Arme5', -19440.000000, -80.000116, 1690.000),
    ('ZONE_1v1_Arme6', -19440.000117, 192.000000, 1690.000),
    ('ZONE_1v1_Arme7', -19440.000117, -192.000000, 1642.000),
    ('ZONE_1v1_Arme8', -19439.999883, 96.000000, 1594.000),
    ('ZONE_1v1_Arme9', -19440.000117, -16.000000, 1594.000),
    ('ZONE_1v1_Arme10', -19440.000000, 0.000000, 1642.000),
    ('ZONE_1v1_Arme11', -19440.000117, -208.000000, 1594.000),
    ('ZONE_1v1_Arme12', -19440.000117, -208.000000, 1690.000),
    ('ZONE_1v1_Arme13', -19439.999883, 144.000000, 1750.000),
    ('ZONE_1v1_Arme14', -19440.000117, 208.000000, 1594.000),
    ('ZONE_1v1_Arme15', -19440.000001, 96.000000, 1690.000),
    ('ZONE_1v1_Arme16', -19440.000117, -96.000000, 1642.000),
    ('ZONE_1v1_Arme17', -19440.000000, 96.000000, 1642.000),
]
by = {a.get_actor_label(): a for a in eas.get_all_level_actors()}
L = []
with unreal.ScopedEditorTransaction("1v1 : armes a la place d'origine"):
    for lab, x, y, z in POS:
        a = by[lab]; a.modify()
        a.set_actor_location(unreal.Vector(x, y, z), False, False)
        yaw = 0 if lab in ("ZONE_1v1_Arme10", "ZONE_1v1_Arme6") else 90
        a.set_actor_rotation(unreal.Rotator(0, 0, yaw), False)
        L.append("%s (%.0f,%.0f,%.0f) yaw=%d" % (lab, x, y, z, yaw))
    v = by["ZONE_1v1_VitreArmes"]; v.modify()
    s = v.get_actor_scale3d()
    v.set_actor_scale3d(unreal.Vector(s.x, 512.0 / 100.0, 256.0 / 100.0))
    v.set_actor_location(unreal.Vector(-19456.0, 0.0, 1792.0), False, False)
o, e = v.get_actor_bounds(False)
L.append("vitre : y %.0f..%.0f z %.0f..%.0f" % (o.y - e.y, o.y + e.y, o.z - e.z, o.z + e.z))
unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
open(r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools\restore_layout_log.txt","w").write("\n".join(L))
