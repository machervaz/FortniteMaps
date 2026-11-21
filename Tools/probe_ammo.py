import unreal, traceback
L = []
try:
    eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    for a in eas.get_all_level_actors():
        n = a.get_class().get_name()
        if any(k in n for k in ("IslandSettings", "MinigameSettings", "PlaysetSettings", "Settings")) and "Billboard" not in n:
            L.append("== %s | %s" % (a.get_actor_label(), n))
    # options du donneur de pompes
    g = [a for a in eas.get_all_level_actors() if a.get_actor_label() == "AIM_Pump_Loadout"][0]
    for c in g.get_components_by_class(unreal.ActorComponent):
        if c.get_name() == "ToyOptionsComponent":
            L.append(str(c.get_editor_property("PlayerOptionData"))[:1500])
except Exception:
    L.append(traceback.format_exc())
open(r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools\probe_ammo_log.txt", "w").write("\n".join(L))
