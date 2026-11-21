import unreal, traceback
TOOLS = r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools"
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
L = []
C = ["/Desert_Assets/SetupAssets/Blueprints/FNEC_DesertCity_WaxStatue_D", "/Desert_Assets/SetupAssets/Blueprints/FNEC_DesertCity_WaxStatue_E",
     "/Desert_Assets/SetupAssets/Blueprints/FNEC_DesertCity_WaxStatue_F", "/Desert_Assets/SetupAssets/Blueprints/FNEC_DesertCity_WaxStatue_G",
     "/CRG_Minerva/SetupAssets/Blueprints/CP_Minerva_Statue_01", "/CRG_Modular/SetupAssets/Blueprints/Statues/CP_Savepoint_Statue"]
try:
    for a in eas.get_all_level_actors():
        if a.get_actor_label().startswith("PROBE_"):
            eas.destroy_actor(a)
    for i, p in enumerate(C):
        nm = p.split("/")[-1]
        cls = unreal.load_class(None, p + "." + nm + "_C")
        a = eas.spawn_actor_from_class(cls, unreal.Vector(-1500 + i * 600, 19500, 1270), unreal.Rotator(0, 0, -90))
        a.set_actor_label("PROBE_ST%d" % i)
        o, e = a.get_actor_bounds(False)
        L.append("%d %s prop=%s e=(%.0f,%.0f,%.0f)" % (i, nm, isinstance(a, unreal.BuildingProp), e.x, e.y, e.z))
    unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).set_level_viewport_camera_info(unreal.Vector(0, 18200, 1500), unreal.Rotator(roll=0, pitch=-3, yaw=90))
except Exception:
    L.append(traceback.format_exc())
open(TOOLS + r"\probe_statues_log.txt", "w").write("\n".join(L))
