import unreal, traceback, itertools
TOOLS = r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools"
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
L = []
try:
    for a in eas.get_all_level_actors():
        lab = a.get_actor_label()
        if not (lab.startswith("ZONE_1v1N_Ramp")):
            continue
        c = a.get_component_by_class(unreal.StaticMeshComponent)
        mesh = c.static_mesh
        bb = mesh.get_bounding_box()
        T = c.get_world_transform()
        L.append("%s mesh=%s loc=%s rot=%s scale=%s local=[%s .. %s]" % (lab, mesh.get_name(), a.get_actor_location(),
                 a.get_actor_rotation(), a.get_actor_scale3d(), bb.min, bb.max))
        for ix, iy, iz in itertools.product((0, 1), repeat=3):
            v = unreal.Vector(bb.max.x if ix else bb.min.x, bb.max.y if iy else bb.min.y, bb.max.z if iz else bb.min.z)
            w = T.transform_location(v)
            L.append("   %d%d%d -> (%.1f, %.1f, %.1f)" % (ix, iy, iz, w.x, w.y, w.z))
except Exception:
    L.append(traceback.format_exc())
open(TOOLS + r"\ramp_info_log.txt", "w").write("\n".join(L))
