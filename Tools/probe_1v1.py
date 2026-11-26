import unreal, collections
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
L = []; c = collections.Counter()
for a in eas.get_all_level_actors():
    n = a.get_class().get_name(); lab = a.get_actor_label(); f = str(a.get_folder_path())
    if "1v1" in lab or "1v1" in f or "Spawner" in n or "Weapon" in n or "Item" in n:
        p = a.get_actor_location()
        L.append("%s | %s | %s | %.0f %.0f %.0f" % (lab, n, f, p.x, p.y, p.z))
open(r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools\probe_1v1_log.txt","w").write("\n".join(sorted(L, key=lambda s: s.split(' | ')[1])))
