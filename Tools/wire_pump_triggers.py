# Relie les triggers des mannequins DOUBLE PUMP au device aim_trainer
import unreal, traceback
F = {"PumpUp": "__verse_0x9BD7867C_PumpUp", "PumpDown": "__verse_0x3575C8C6_PumpDown"}
W = "/CreativeCoreDevices/_Verse.trigger_device"
L = []
try:
    eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    ACT = {a.get_actor_label(): a for a in eas.get_all_level_actors()}
    s = ACT["AIM_Trainer"].get_editor_property("Script")
    for field, kind in (("PumpUp", "Up"), ("PumpDown", "Down")):
        objs = []
        for i in range(4):
            o = unreal.new_object(unreal.load_class(None, W), s)
            o.set_editor_property("SavedActor", ACT["AIM_Pump_%s%d" % (kind, i)])
            objs.append(o)
        s.set_editor_property(F[field], objs)
        L.append("%s -> %s" % (field, [x.get_editor_property("SavedActor").get_actor_label() for x in s.get_editor_property(F[field])]))
    unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
    L.append("TERMINE")
except Exception:
    L.append(traceback.format_exc())
open(r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools\wire_pump_triggers_log.txt", "w").write("\n".join(L))
