import unreal, traceback
TOOLS = r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools"
DIR = "/5622d7d7-d1ca-438f-8a48-1286a48e2471/Lobby/NPC"
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
eal = unreal.EditorAssetLibrary
L = []
try:
    path = DIR + "/NPC_TrainingBot"
    if eal.does_asset_exist(path):
        d = eal.load_asset(path)
    else:
        d = unreal.AssetToolsHelpers.get_asset_tools().create_asset("NPC_TrainingBot", DIR, unreal.NPCCharacterDefinition, unreal.NPCCharacterDefinitionFactory())
        eal.save_loaded_asset(d)
    L.append("definition : %s" % d)
    for p in dir(d):
        if not p.startswith("_") and p.islower():
            pass
    try:
        L.append("props : " + str([p for p in d.get_editor_property("character_modifiers")]) )
    except Exception as ex:
        L.append("modifiers : %s" % ex)
    for a in eas.get_all_level_actors():
        if a.get_actor_label().startswith("PROBE_"):
            eas.destroy_actor(a)
    sp = eas.spawn_actor_from_class(unreal.load_class(None, "/CRD_AISpawner/Device_CharacterSpawner.Device_CharacterSpawner_C"), unreal.Vector(0, 19000, 1270))
    sp.set_actor_label("PROBE_NPCSpawner")
    eas.set_selected_level_actors([sp])
    L.append("spawner ok")
except Exception:
    L.append(traceback.format_exc())
open(TOOLS + r"\probe_npc_log.txt", "w").write("\n".join(L))
