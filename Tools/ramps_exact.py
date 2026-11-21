# Rampes 1v1 : la SURFACE va exactement d'un bord de case a l'autre, comme une
# rampe construite : (y=0, z=1536) -> (y=+/-512, z=1920), largeur 512 (case x -20224..-19712).
# Dalle de 24 cm sous la surface. Rebord LED (sans collision) juste sous l'arete du haut.
import unreal, traceback
TOOLS = r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools"
X0, X1 = -20224.0, -19712.0
Z0, RUN, RISE, T = 1536.0, 512.0, 384.0, 24.0
SLOPE = (RISE ** 2 + RUN ** 2) ** 0.5          # 640
SN, CS = RISE / SLOPE, RUN / SLOPE               # 0.6 / 0.8
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
L = []
try:
    ACT = {a.get_actor_label(): a for a in eas.get_all_level_actors()}
    with unreal.ScopedEditorTransaction("Rampes 1v1 exactes"):
        for side in (1, -1):
            r = ACT["ZONE_1v1N_Ramp%d" % side]
            e = ACT["ZONE_1v1N_RampEdge%d" % side]
            for a in (r, e):
                a.modify()
                for c in a.get_components_by_class(unreal.SceneComponent):
                    c.modify()
            # centre de la surface (side*256, 1728) ; centre de la dalle = surface - normale*T/2
            # normale vers le haut de la surface montant vers side*y : (-side*SN, CS)
            cy = side * RUN / 2 + side * SN * T / 2
            cz = Z0 + RISE / 2 - CS * T / 2
            r.set_actor_location(unreal.Vector((X0 + X1) / 2, cy, cz), False, False)
            r.set_actor_scale3d(unreal.Vector((X1 - X0) / 100.0, SLOPE / 100.0, T / 100.0))
            e.set_actor_location(unreal.Vector((X0 + X1) / 2, side * (RUN - 8), Z0 + RISE - 8), False, False)
            e.set_actor_scale3d(unreal.Vector((X1 - X0) / 100.0, 0.16, 0.16))
            for c in e.get_components_by_class(unreal.PrimitiveComponent):
                c.set_collision_profile_name("NoCollision")
            # verification : coins de la face du haut
            comp = r.get_component_by_class(unreal.StaticMeshComponent)
            T_ = comp.get_world_transform()
            pts = [T_.transform_location(unreal.Vector(x, y, 50)) for x in (-50, 50) for y in (-50, 50)]
            L.append("%s rot=%s surface : %s" % (r.get_actor_label(), r.get_actor_rotation(),
                     ["(%.1f,%.1f,%.1f)" % (p.x, p.y, p.z) for p in pts]))
    unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
    L.append("TERMINE")
except Exception:
    L.append(traceback.format_exc())
open(TOOLS + r"\ramps_exact_log.txt", "w").write("\n".join(L))
