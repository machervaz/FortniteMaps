import unreal, traceback
L = []
try:
    eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    a = [x for x in eas.get_all_level_actors() if x.get_actor_label() == "ZONE_Aim_Loadout"][0]
    objs = [a] + list(a.get_components_by_class(unreal.ActorComponent))
    for o in objs:
        L.append("== %s (%s)" % (o.get_name(), o.get_class().get_name()))
        for name in dir(o):
            if name.startswith("_"): continue
            try:
                v = o.get_editor_property(name)
            except Exception:
                continue
            s = str(v)
            if any(k in name.lower() for k in ("item", "grant", "weapon", "clear", "equip", "inventory", "count", "ammo")) or "WID_" in s:
                L.append("   %s = %s" % (name, s[:400]))
except Exception:
    L.append(traceback.format_exc())
open(r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools\probe_granter_log.txt", "w").write("\n".join(L))
