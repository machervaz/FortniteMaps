import unreal, traceback
TOOLS = r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools"
L = []
try:
    eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    a = [x for x in eas.get_all_level_actors() if x.get_actor_label() == "ZONE_1v1P_PanelDevice"][0]
    s = a.get_editor_property("Script")
    for base in ("SkyFloor", "FallZone", "RespawnPoint"):
        L.append(base + " : " + str([p for p in dir(s) if base.lower() in p.lower()]))
    try:
        t = unreal.EditorAssetLibrary  # export text as fallback
        L.append(unreal.ObjectTools if False else "")
    except Exception:
        pass
except Exception:
    L.append(traceback.format_exc())
open(TOOLS + r"\list_panel_fields_log.txt", "w").write("\n".join(L))
