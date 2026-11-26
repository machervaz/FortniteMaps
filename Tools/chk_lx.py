import unreal
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
L = []
for a in eas.get_all_level_actors():
    if a.get_actor_label() == "LOBBY_Extras" or a.get_class().get_name() in ("VerseDevice_C", "lobby_extras", "lobby_extras_C"):
        s = None
        try: s = a.get_editor_property("Script")
        except Exception: pass
        L.append("%s | %s | %s | %s" % (a.get_actor_label(), a.get_class().get_name(), s.get_class().get_name() if s else None, a.get_folder_path()))
open(r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools\chk_lx_log.txt","w").write("\n".join(L))
