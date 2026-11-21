# Exercice aim 4 : DOUBLE PUMP
#  - 4e faille dans le hub (les 3 autres sont decalees pour faire de la place)
#  - salle fermee (0, 60000) : sol, murs, toit, LED, titre, texte "emote -> lobby"
#  - Mutator Zone qui couvre la salle (entree = donne les 2 pompes, emote = retour lobby)
#  - NPC spawner (mannequins), donneur d'objets (2 pompes, reglage manuel)
import unreal, json, traceback
exec(open(r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools\aim_lib.py", encoding="utf-8").read())
CX, CY, SIZE, H = 0.0, 60000.0, 3000.0, 1000.0
SHIFT = {"Circuit": -700.0, "Bounce": -700.0, "Launch": -700.0}     # -1400/0/1400 -> -2100/-700/700
try:
    ACT = {a.get_actor_label(): a for a in eas.get_all_level_actors()}
    for lab, a in list(ACT.items()):
        if lab.startswith("AIM_Pump_") or lab.startswith("AIM_Hub_RiftPump"):
            eas.destroy_actor(a)
    M = {"gloss": eal.load_asset(MAT_DIR + "/M_Lobby_BlackGloss"),
         "led": eal.load_asset(MAT_DIR + "/M_Lobby_LedDeepBlue"),
         "arenawall": mat("M_Aim_ArenaWall", LC(0.06, 0.09, 0.16), None, 0.5)}
    # --- hub : decale les 3 failles existantes ---
    if abs(ACT["AIM_Hub_RiftBounce_Zone"].get_actor_location().x) < 50:
        with unreal.ScopedEditorTransaction("Failles decalees"):
            for key, dx in SHIFT.items():
                for part in ("Core", "Edge", "Glow", "Title", "Zone"):
                    a = ACT["AIM_Hub_Rift%s_%s" % (key, part)]
                    a.modify()
                    for c in a.get_components_by_class(unreal.SceneComponent):
                        c.modify()
                    p = a.get_actor_location()
                    a.set_actor_location(V(p.x + dx, p.y, p.z), False, False)
        L.append("failles decalees")
    rz = rift("Hub_RiftPump", "Hub", 2100, 20800, -90.0, (1.0, 0.12, 0.12), "DOUBLE PUMP", M)
    ACT2 = {a.get_actor_label(): a for a in eas.get_all_level_actors()}
    ACT2["AIM_Hub_RiftPump_Title"].set_editor_property("TextSize", 30)
    # --- salle ---
    arena_floor("Pump", CX, CY, SIZE, M, "DOUBLE PUMP", (CX, CY + SIZE / 2 - 60), 700)
    enclosure("Pump", M, CX, CY, SIZE, H)
    arr = arrival("Pump_Arrival", "Pump", CX, CY - 900, 90.0)
    billboard("Pump_Emote1", "Pump", V(CX, CY + SIZE / 2 - 60, FLOOR + 480), -90.0, "DO AN EMOTE", 30)
    billboard("Pump_Emote2", "Pump", V(CX, CY + SIZE / 2 - 60, FLOOR + 420), -90.0, "TO RETURN TO LOBBY", 24)
    # zone de la salle
    z = spawn("mutator", "Pump_Room", "Pump", V(CX, CY, FLOOR))
    z.set_actor_rotation(unreal.Rotator(0, 0, 0), False)
    o, e = z.get_actor_bounds(False); s = z.get_actor_scale3d()
    z.set_actor_scale3d(V(s.x * (SIZE - 40) / (2 * e.x), s.y * (SIZE - 40) / (2 * e.y), s.z * (H - 40) / (2 * e.z)))
    o, e = z.get_actor_bounds(False); p = z.get_actor_location()
    z.set_actor_location(V(p.x + CX - o.x, p.y + CY - o.y, p.z + FLOOR + 10 - (o.z - e.z)), False, False)
    # bots + armes
    sp = npc_spawner("Pump_Spawner", "Pump", V(CX + SIZE / 2 + 600, CY, FLOOR), eal.load_asset(NPC_DEF))
    g = eas.spawn_actor_from_class(unreal.load_class(None, "/CreativeCoreDevices/Device_ItemGranter_V2.Device_ItemGranter_V2_C"), V(CX + SIZE / 2 + 600, CY + 400, FLOOR))
    tag(g, "Pump_Loadout", "Pump")
    unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
    L.append("TERMINE")
except Exception:
    L.append(traceback.format_exc())
open(TOOLS + r"\build_pump_log.txt", "w").write("\n".join(L))
