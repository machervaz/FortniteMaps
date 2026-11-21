import unreal, traceback
L = []
try:
    eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    sp = [a for a in eas.get_all_level_actors() if a.get_actor_label() == "PROBE_NPCSpawner"][0]
    comp = sp.get_component_by_class(unreal.NPCCharacterDefinitionComponent)
    d = unreal.load_asset("/5622d7d7-d1ca-438f-8a48-1286a48e2471/Lobby/NPC/NPC_TrainingBot")
    for obj, nm in ((sp, "actor"), (comp, "comp")):
        for p in ("NPCCharacterDefinition", "CharacterDefinition", "NPC Character Definition", "NPCDefinition", "Definition", "CharacterDefinitionToUse", "NPC_CharacterDefinition"):
            try:
                v = obj.get_editor_property(p)
                L.append("%s.%s = %s" % (nm, p, v))
                obj.set_editor_property(p, d)
                L.append("   -> set ok : %s" % obj.get_editor_property(p))
            except Exception as ex:
                pass
    for p in ("CharacterType", "character_type", "Character Type", "Health", "MaxHealth"):
        try:
            L.append("def.%s = %s" % (p, d.get_editor_property(p)))
        except Exception:
            pass
except Exception:
    L.append(traceback.format_exc())
open(r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools\probe_npc3_log.txt", "w").write("\n".join(L) or "rien")
