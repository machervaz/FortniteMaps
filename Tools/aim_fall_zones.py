# Zones d'alteration posees par le joueur au sol des arenes Aim : tomber dedans -> retour
# sur la plateforme de depart de l'exercice (ajoutees aux failles du device aim_trainer).
import unreal, json, traceback
TOOLS = r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools"
ARENAS = {"AIM_Launch_Arrival": (28500, 39500), "AIM_Bounce_Arrival": (39500, 48300), "AIM_Circuit_Arrival": (48300, 56000)}
L = []
try:
    eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    m = json.load(open(TOOLS + r"\build_aim_map.json"))
    base_r, base_t = m["rifts"][:6], m["targets"][:6]
    with unreal.ScopedEditorTransaction("Aim : zones de chute"):
        for a in eas.get_all_level_actors():
            if a.get_class().get_name() != "Device_MutatorVolume_V2_C" or a.get_actor_label().startswith(("ZONE_", "LOBBY_", "TUN_", "AIM_", "PCX_")):
                continue
            p = a.get_actor_location()
            for target, (y0, y1) in ARENAS.items():
                if y0 < p.y < y1 and abs(p.x) < 6000:
                    a.modify()
                    a.set_editor_property("is_spatially_loaded", False)
                    base_r.append(a.get_actor_label()); base_t.append(target)
                    L.append("%s -> %s" % (a.get_actor_label(), target))
    m["rifts"], m["targets"] = base_r, base_t
    json.dump(m, open(TOOLS + r"\build_aim_map.json", "w"), indent=1)
    unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
    L.append("TERMINE")
except Exception:
    L.append(traceback.format_exc())
open(TOOLS + r"\aim_fall_zones_log.txt", "w").write("\n".join(L))
