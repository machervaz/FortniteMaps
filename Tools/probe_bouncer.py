import unreal, traceback
TOOLS = r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools"
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
L = []
C = ["/CRD_Bouncer/SetupAssets/Classic_Bouncer/BP_Device_ClassicBouncer", "/CRD_Bouncer/SetupAssets/Mushroom_Bouncer/BP_Device_MushroomBouncer",
     "/Figment_Trap_Floor_Player_Launch_Pad_Athena/Items/Trap/Trap_Floor_Player_LaunchPad_Figment", "/CRD_Bouncer/BP_Device_Bouncer"]
try:
    for a in eas.get_all_level_actors():
        if a.get_actor_label().startswith("PROBE_"):
            eas.destroy_actor(a)
    for i, p in enumerate(C):
        nm = p.split("/")[-1]
        try:
            cls = unreal.load_class(None, p + "." + nm + "_C")
            a = eas.spawn_actor_from_class(cls, unreal.Vector(900 - i * 600, 19400, 1270))
            a.set_actor_label("PROBE_B%d" % i)
            o, e = a.get_actor_bounds(False)
            L.append("%d %s c=(%.0f,%.0f,%.0f) e=(%.0f,%.0f,%.0f)" % (i, nm, o.x, o.y, o.z, e.x, e.y, e.z))
        except Exception as ex:
            L.append("%d %s ERR %s" % (i, nm, ex))
    unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).set_level_viewport_camera_info(unreal.Vector(0, 18500, 1700), unreal.Rotator(roll=0, pitch=-15, yaw=90))
except Exception:
    L.append(traceback.format_exc())
open(TOOLS + r"\probe_bouncer_log.txt", "w").write("\n".join(L))
