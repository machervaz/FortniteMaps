import unreal
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
L = []
def find():
    return [a for a in eas.get_all_level_actors() if a.get_outermost().get_name().endswith("HE0T9U4QKIJQ6XY1AYGH8O")]
f = find(); L.append("avant : %d %s" % (len(f), [a.get_path_name() for a in f]))
if f:
    a = f[0]
    L.append("locked=%s editable=%s" % (a.is_actor_label_editable() if hasattr(a, "is_actor_label_editable") else "?", "?"))
    r = eas.destroy_actor(a)
    L.append("destroy -> %s ; valide apres=%s" % (r, unreal.SystemLibrary.is_valid(a)))
f = find(); L.append("apres : %d %s" % (len(f), [a.get_path_name() for a in f]))
open(r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools\probe_destroy_one_log.txt", "w").write("\n".join(L))
