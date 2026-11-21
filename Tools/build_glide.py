# Exercice aim 5 : GLIDE (bots qui planent) - arene (0, 68000), plateforme de depart au sud,
# 5e faille dans le hub (les 4 autres sont respacees), faille de retour, spawner (copie de LANCER)
import unreal, json, traceback
exec(open(r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools\aim_lib.py", encoding="utf-8").read())
CX, CY, SIZE, H = 0.0, 68000.0, 8000.0, 4000.0
HUBX = {"Circuit": -2400.0, "Bounce": -1200.0, "Launch": 0.0, "Pump": 1200.0}
try:
    ACT = {a.get_actor_label(): a for a in eas.get_all_level_actors()}
    for lab, a in list(ACT.items()):
        if lab.startswith(("AIM_Glide", "AIM_Hub_RiftGlide")):
            eas.destroy_actor(a)
    M = {"gloss": eal.load_asset(MAT_DIR + "/M_Lobby_BlackGloss"), "led": eal.load_asset(MAT_DIR + "/M_Lobby_LedDeepBlue"),
         "arenawall": eal.load_asset(MAT_DIR + "/M_Aim_ArenaWall")}
    # hub : 5 failles espacees de 12 m
    with unreal.ScopedEditorTransaction("Failles respacees"):
        for key, nx in HUBX.items():
            cur = ACT["AIM_Hub_Rift%s_Zone" % key].get_actor_location().x
            dx = nx - cur
            if abs(dx) < 1: continue
            for part in ("Core", "Edge", "Glow", "Title", "Zone"):
                a = ACT["AIM_Hub_Rift%s_%s" % (key, part)]
                a.modify()
                for c in a.get_components_by_class(unreal.SceneComponent):
                    c.modify()
                p = a.get_actor_location()
                a.set_actor_location(V(p.x + dx, p.y, p.z), False, False)
    rift("Hub_RiftGlide", "Hub", 2400, 20800, -90.0, (1.0, 0.8, 0.1), "GLIDE", M)
    # arene
    arena_floor("Glide", CX, CY, SIZE, M, "GLIDE", (CX, CY + SIZE / 2 - 400), 900)
    enclosure("Glide", M, CX, CY, SIZE, H)
    top = platform("Glide_Platform", "Glide", M, 0, CY - SIZE / 2 + 700)
    arrival("Glide_Arrival", "Glide", 0, CY - SIZE / 2 + 850, 90.0, top)
    rift("Glide_Return", "Glide", 0, CY - SIZE / 2 + 400, 90.0, (0.2, 0.6, 1.0), "BACK TO AIM", M, top)
    # spawner : copie de celui de LANCER (deja regle sans reapparition automatique)
    sp = eas.duplicate_actor(ACT["AIM_Launch_Spawner"])
    sp.set_actor_location(V(SIZE / 2 - 500, CY + SIZE / 2 - 500, FLOOR), False, False)
    sp.set_actor_label("AIM_Glide_Spawner"); sp.set_folder_path("Zones/Aim/Glide")
    ACT2 = {a.get_actor_label(): a for a in eas.get_all_level_actors()}
    for lab in ("AIM_Hub_RiftGlide_Title", "AIM_Glide_Return_Title"):
        ACT2[lab].set_editor_property("TextSize", 32)
    MAP = json.load(open(TOOLS + r"\build_aim_map.json"))
    for z, t in (("AIM_Hub_RiftGlide_Zone", "AIM_Glide_Arrival"), ("AIM_Glide_Return_Zone", "ZONE_Aim_Arrival")):
        if z not in MAP["rifts"]:
            MAP["rifts"].append(z); MAP["targets"].append(t)
    json.dump(MAP, open(TOOLS + r"\build_aim_map.json", "w"), indent=1)
    unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
    L.append("TERMINE (plateforme z=%d)" % top)
except Exception:
    L.append(traceback.format_exc())
open(TOOLS + r"\build_glide_log.txt", "w").write("\n".join(L))
