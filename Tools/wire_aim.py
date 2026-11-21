# Relie le device aim_trainer (apres build_aim.py) - bots = NPC Spawners
import unreal, json, traceback
TOOLS = r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools"
MAP = json.load(open(TOOLS + r"\build_aim_map.json"))
F = {"Rifts": "__verse_0x9B3CE062_Rifts", "RiftTargets": "__verse_0x42C6EFD9_RiftTargets",
     "LaunchSpawner": "__verse_0xB9EC6450_LaunchSpawner", "LaunchPads": "__verse_0x54B8477C_LaunchPads",
     "BounceSpawner": "__verse_0x812F24DF_BounceSpawner", "BouncePads": "__verse_0xC4187C5C_BouncePads",
     "CircuitSpawner": "__verse_0x7DAED292_CircuitSpawner", "CircuitPath": "__verse_0xD59DD1A9_CircuitPath"}
W = {"mutator": "/CRD_VolumetricRegion/_Verse.mutator_zone_device",
     "prop": "/VerseDevices/_Verse/VNI/VerseDevices.Devices_creative_prop"}
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
L = []
try:
    ACT = {a.get_actor_label(): a for a in eas.get_all_level_actors()}
    dev = ACT[MAP["device"]]
    s = dev.get_editor_property("Script")
    def single(field, label):
        s.get_editor_property(F[field]).set_editor_property("SavedActor", ACT[label])
    def arr(field, kind, labels):
        objs = []
        for l in labels:
            o = unreal.new_object(unreal.load_class(None, W[kind]), s)
            o.set_editor_property("SavedActor", ACT[l])
            objs.append(o)
        s.set_editor_property(F[field], objs)
        L.append("%s : %d" % (field, len(objs)))
    arr("Rifts", "mutator", MAP["rifts"])
    arr("RiftTargets", "prop", MAP["targets"])
    single("LaunchSpawner", MAP["launch"]["spawner"]); arr("LaunchPads", "prop", MAP["launch"]["pads"])
    single("BounceSpawner", MAP["bounce"]["spawner"]); arr("BouncePads", "prop", MAP["bounce"]["pads"])
    single("CircuitSpawner", MAP["circuit"]["spawner"]); arr("CircuitPath", "prop", MAP["circuit"]["path"])
    unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
    L.append("ok")
except Exception:
    L.append(traceback.format_exc())
open(TOOLS + r"\wire_aim_log.txt", "w").write("\n".join(L))
