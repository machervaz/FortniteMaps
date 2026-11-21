# Relie les 4 sentinelles DOUBLE PUMP au device aim_trainer
import unreal, traceback
F = "__verse_0x9CF89422_PumpSentries"
W = "/CRD_SentryDevice/_Verse.sentry_device"
L = []
try:
    eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    ACT = {a.get_actor_label(): a for a in eas.get_all_level_actors()}
    s = ACT["AIM_Trainer"].get_editor_property("Script")
    objs = []
    for i in range(4):
        o = unreal.new_object(unreal.load_class(None, W), s)
        o.set_editor_property("SavedActor", ACT["AIM_Pump_Sentry%d" % i])
        objs.append(o)
    s.set_editor_property(F, objs)
    L.append("PumpSentries -> %s" % [x.get_editor_property("SavedActor").get_actor_label() for x in s.get_editor_property(F)])
    unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
    L.append("TERMINE")
except Exception:
    L.append(traceback.format_exc())
open(r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools\wire_pump_sentries_log.txt", "w").write("\n".join(L))
