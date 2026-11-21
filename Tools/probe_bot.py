import unreal, traceback
TOOLS = r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools"
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
L = []
def chain(cls):
    out = []
    c = cls
    for _ in range(12):
        if not c:
            break
        out.append(c.get_name())
        try:
            c = c.get_super_class() if hasattr(c, "get_super_class") else None
        except Exception:
            break
    return out
try:
    for a in eas.get_all_level_actors():
        if a.get_actor_label().startswith("PROBE_BOT"):
            eas.destroy_actor(a)
    dojo = unreal.load_class(None, "/Game/Environments/Asteria/Props/Dojo/Dojo_TargetDummy_A/Blueprints/Asteria_Dojo_TargetDummy_A.Asteria_Dojo_TargetDummy_A_C")
    L.append("dojo class %s" % dojo)
    L.append("is BuildingProp: %s" % (unreal.BuildingProp in unreal.BuildingProp.__mro__ and isinstance(unreal.get_default_object(dojo), unreal.BuildingProp)))
    a = eas.spawn_actor_from_class(dojo, unreal.Vector(0, 21000, 1270))
    a.set_actor_label("PROBE_BOT_Dojo")
    o, e = a.get_actor_bounds(False)
    L.append("dojo bounds c=%s e=%s class=%s" % (o, e, a.get_class().get_name()))
    L.append("dojo isinstance BuildingProp=%s" % isinstance(a, unreal.BuildingProp))
    # CP prop + mesh du mannequin
    cp = unreal.load_class(None, "/CRG_Props/SetupAssets/Blueprints/TechPrimitives/CP_L_T_Primitive_Squared_Cube_Flat.CP_L_T_Primitive_Squared_Cube_Flat_C")
    b = eas.spawn_actor_from_class(cp, unreal.Vector(300, 21000, 1270))
    b.set_actor_label("PROBE_BOT_Mesh")
    mesh = unreal.load_asset("/Game/Creative/Devices/Mannequin/Meshes/CP_Device_Mannequin_01")
    for c in b.get_components_by_class(unreal.StaticMeshComponent):
        L.append("  comp %s mesh avant=%s" % (c.get_name(), c.static_mesh))
        c.set_static_mesh(mesh)
    o, e = b.get_actor_bounds(False)
    L.append("mesh-prop bounds c=%s e=%s" % (o, e))
    unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).set_level_viewport_camera_info(unreal.Vector(150, 20400, 1450), unreal.Rotator(roll=0, pitch=-5, yaw=90))
except Exception:
    L.append(traceback.format_exc())
open(TOOLS + r"\probe_bot_log.txt", "w").write("\n".join(L))
