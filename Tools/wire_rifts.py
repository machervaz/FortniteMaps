# Rebranche les failles du hub/exercices (Rifts + RiftTargets) depuis build_aim_map.json
import unreal, json, traceback
TOOLS = r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools"
F = {"Rifts": ("__verse_0x9B3CE062_Rifts", "/CRD_VolumetricRegion/_Verse.mutator_zone_device"),
     "RiftTargets": ("__verse_0x42C6EFD9_RiftTargets", "/VerseDevices/_Verse/VNI/VerseDevices.Devices_creative_prop")}
L = []
try:
    MAP = json.load(open(TOOLS + r"\build_aim_map.json"))
    eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    ACT = {a.get_actor_label(): a for a in eas.get_all_level_actors()}
    s = ACT["AIM_Trainer"].get_editor_property("Script")
    for key, labels in (("Rifts", MAP["rifts"]), ("RiftTargets", MAP["targets"])):
        field, cls = F[key]
        objs = []
        for l in labels:
            o = unreal.new_object(unreal.load_class(None, cls), s)
            o.set_editor_property("SavedActor", ACT[l])
            objs.append(o)
        s.set_editor_property(field, objs)
        L.append("%s : %d (dernier : %s)" % (key, len(objs), labels[-1]))
    unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
    L.append("TERMINE")
except Exception:
    L.append(traceback.format_exc())
open(TOOLS + r"\wire_rifts_log.txt", "w").write("\n".join(L))
