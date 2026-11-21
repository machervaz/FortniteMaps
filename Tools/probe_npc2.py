import unreal, traceback
L = []
try:
    eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    sp = [a for a in eas.get_all_level_actors() if a.get_actor_label() == "PROBE_NPCSpawner"][0]
    comp = sp.get_component_by_class(unreal.NPCCharacterDefinitionComponent)
    L.append("comp %s" % comp)
    L.append("comp dir: " + ", ".join(n for n in dir(comp) if not n.startswith("_") and "_" in n and not n.startswith(("get_", "set_", "k2_", "is_", "add_", "remove_", "on_", "can_", "has_", "call_", "cast_", "modify", "reset_", "post_", "pre_", "export", "import", "rename", "static_", "find_"))))
    d = unreal.load_asset("/5622d7d7-d1ca-438f-8a48-1286a48e2471/Lobby/NPC/NPC_TrainingBot")
    L.append("def dir: " + ", ".join(n for n in dir(d) if not n.startswith("_") and not n.startswith(("get_", "set_", "k2_", "is_", "call_", "cast_", "modify", "rename", "static_", "export", "import", "find_", "can_", "has_"))))
    L.append("actor dir: " + ", ".join(n for n in dir(sp) if "npc" in n.lower() or "definition" in n.lower() or "spawn" in n.lower()))
except Exception:
    L.append(traceback.format_exc())
open(r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools\probe_npc2_log.txt", "w").write("\n".join(L))
