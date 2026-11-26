import unreal
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
a = [a for a in eas.get_all_level_actors() if a.get_actor_label() == "CP_Glass_Floor3"][0]
L = []
for k in ("bIsInvulnerable", "is_invulnerable", "b_is_invulnerable", "bCanBeDamaged", "can_be_damaged", "b_can_be_damaged"):
    try: L.append("%s=%s" % (k, a.get_editor_property(k)))
    except Exception as e: L.append("%s ERR %s" % (k, str(e)[:80]))
try:
    a.set_editor_property("is_invulnerable", True); L.append("set is_invulnerable ok -> %s" % a.get_editor_property("is_invulnerable"))
except Exception as e: L.append("set ERR %s" % str(e)[:120])
L.append(str([p for p in dir(a) if "nvul" in p.lower() or "damage" in p.lower()]))
open(r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools\probe_inv_log.txt","w").write("\n".join(L))
