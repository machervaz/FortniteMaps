import unreal, traceback
L = []
try:
    eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    seen = set()
    for a in eas.get_all_level_actors():
        n = a.get_class().get_name()
        p = a.get_actor_location()
        if n in seen or not (20000 < p.x < 34000 and -12500 < p.y < -500):
            continue
        if n.startswith(("BrickSimple", "SM_FORT_Floors", "Pueblo", "PBWA")):
            seen.add(n)
            L.append("%s : %s" % (n, ", ".join(x for x in dir(a) if any(k in x.lower() for k in ("invul", "damage", "health", "destruct", "indestruct")))))
            for pn in ("bIsInvulnerable", "is_invulnerable", "b_is_invulnerable", "invulnerable", "CanBeDamaged", "can_be_damaged", "bCanBeDamaged"):
                try:
                    L.append("    %s = %s" % (pn, a.get_editor_property(pn)))
                except Exception:
                    pass
except Exception:
    L.append(traceback.format_exc())
open(r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools\probe_invul_log.txt", "w").write("\n".join(L))
