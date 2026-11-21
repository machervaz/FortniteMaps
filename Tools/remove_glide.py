# Supprime l'exercice GLIDE (arene, faille du hub, spawners) et remet 4 failles espacees
import unreal, json, traceback
TOOLS = r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools"
HUBX = {"Circuit": -2100.0, "Bounce": -700.0, "Launch": 700.0, "Pump": 2100.0}
L = []
try:
    eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    n = 0
    for a in eas.get_all_level_actors():
        if a.get_actor_label().startswith(("AIM_Glide", "AIM_Hub_RiftGlide")):
            eas.destroy_actor(a); n += 1
    L.append("supprimes : %d" % n)
    ACT = {a.get_actor_label(): a for a in eas.get_all_level_actors()}
    with unreal.ScopedEditorTransaction("Failles 4"):
        for key, nx in HUBX.items():
            dx = nx - ACT["AIM_Hub_Rift%s_Zone" % key].get_actor_location().x
            if abs(dx) < 1: continue
            for part in ("Core", "Edge", "Glow", "Title", "Zone"):
                a = ACT["AIM_Hub_Rift%s_%s" % (key, part)]; a.modify()
                for c in a.get_components_by_class(unreal.SceneComponent):
                    c.modify()
                p = a.get_actor_location()
                a.set_actor_location(unreal.Vector(p.x + dx, p.y, p.z), False, False)
    MAP = json.load(open(TOOLS + r"\build_aim_map.json"))
    keep = [(r, t) for r, t in zip(MAP["rifts"], MAP["targets"]) if "Glide" not in r]
    MAP["rifts"] = [r for r, t in keep]; MAP["targets"] = [t for r, t in keep]
    json.dump(MAP, open(TOOLS + r"\build_aim_map.json", "w"), indent=1)
    L.append("failles : %d" % len(MAP["rifts"]))
    unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
    L.append("TERMINE")
except Exception:
    L.append(traceback.format_exc())
open(TOOLS + r"\remove_glide_log.txt", "w").write("\n".join(L))
