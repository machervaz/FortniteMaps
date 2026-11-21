# Relie l'exercice DOUBLE PUMP au device aim_trainer (+ 4e faille du hub)
import unreal, json, traceback
TOOLS = r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools"
F = {"PumpRoom": "__verse_0x3FA795CE_PumpRoom", "PumpSpawner": "__verse_0x4464509C_PumpSpawner",
     "PumpLoadout": "__verse_0x2F724D1F_PumpLoadout", "LobbyPoint": "__verse_0x204CC60D_LobbyPoint",
     "Rifts": "__verse_0x9B3CE062_Rifts", "RiftTargets": "__verse_0x42C6EFD9_RiftTargets"}
W = {"mutator": "/CRD_VolumetricRegion/_Verse.mutator_zone_device",
     "prop": "/VerseDevices/_Verse/VNI/VerseDevices.Devices_creative_prop"}
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
L = []
try:
    ACT = {a.get_actor_label(): a for a in eas.get_all_level_actors()}
    s = ACT["AIM_Trainer"].get_editor_property("Script")
    # point d'arrivee du lobby : celui du device du hub
    lobby = None
    for a in ACT.values():
        if a.get_actor_label() == "AIM_Trainer": continue
        try:
            sc = a.get_editor_property("Script")
            lobby = sc.get_editor_property(F["LobbyPoint"]).get_editor_property("SavedActor")
            if lobby: L.append("lobby point (de %s) : %s" % (a.get_actor_label(), lobby.get_actor_label())); break
        except Exception:
            pass
    for field, lab in (("PumpRoom", "AIM_Pump_Room"), ("PumpSpawner", "AIM_Pump_Spawner"), ("PumpLoadout", "AIM_Pump_Loadout")):
        s.get_editor_property(F[field]).set_editor_property("SavedActor", ACT[lab])
    s.get_editor_property(F["LobbyPoint"]).set_editor_property("SavedActor", lobby)
    # faille du hub : ajoutee a la fin des listes
    MAP = json.load(open(TOOLS + r"\build_aim_map.json"))
    if "AIM_Hub_RiftPump_Zone" not in MAP["rifts"]:
        MAP["rifts"].append("AIM_Hub_RiftPump_Zone"); MAP["targets"].append("AIM_Pump_Arrival")
        json.dump(MAP, open(TOOLS + r"\build_aim_map.json", "w"), indent=1)
    for field, kind, labels in (("Rifts", "mutator", MAP["rifts"]), ("RiftTargets", "prop", MAP["targets"])):
        objs = []
        for l in labels:
            o = unreal.new_object(unreal.load_class(None, W[kind]), s)
            o.set_editor_property("SavedActor", ACT[l])
            objs.append(o)
        s.set_editor_property(F[field], objs)
        L.append("%s : %d" % (field, len(objs)))
    for k in F:
        v = s.get_editor_property(F[k])
        if isinstance(v, unreal.Array) or isinstance(v, list):
            L.append("%s -> %s" % (k, [x.get_editor_property("SavedActor").get_actor_label() if x.get_editor_property("SavedActor") else None for x in v][-2:]))
        else:
            sa = v.get_editor_property("SavedActor")
            L.append("%s -> %s" % (k, sa.get_actor_label() if sa else None))
    unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
    L.append("TERMINE")
except Exception:
    L.append(traceback.format_exc())
open(TOOLS + r"\wire_pump_log.txt", "w").write("\n".join(L))
