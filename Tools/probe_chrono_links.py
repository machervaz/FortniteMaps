import unreal, traceback
L = []
F = {"start": "__verse_0x5CFF7AE4_StartTrigger", "finish": "__verse_0x16E5C556_FinishTrigger", "label": "__verse_0xBC955082_CourseLabel", "board": "__verse_0xD0A1761B_Leaderboard"}
try:
    eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    for a in eas.get_all_level_actors():
        lab = a.get_actor_label()
        if lab.endswith("_Chrono") or "Chrono" in lab and lab.startswith("PCX_"):
            try:
                s = a.get_editor_property("Script")
            except Exception:
                continue
            if s is None: continue
            try:
                st = s.get_editor_property(F["start"]).get_editor_property("SavedActor")
                fi = s.get_editor_property(F["finish"]).get_editor_property("SavedActor")
                L.append("%s label=%s start=%s finish=%s boards=%d" % (lab, s.get_editor_property(F["label"]), st.get_actor_label() if st else None, fi.get_actor_label() if fi else None, len(s.get_editor_property(F["board"]))))
            except Exception as ex:
                L.append("%s : %s" % (lab, ex))
except Exception:
    L.append(traceback.format_exc())
open(r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools\probe_chrono_links_log.txt", "w").write("\n".join(L))
