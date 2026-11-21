import unreal, traceback
TOOLS = r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools"
L = []
try:
    L.append("classes unreal : " + ", ".join(n for n in dir(unreal) if "CharacterDefinition" in n or "NPCSpawner" in n or "NpcSpawner" in n or "NPCCharacter" in n))
    ar = unreal.AssetRegistryHelpers.get_asset_registry()
    flt = unreal.ARFilter(class_paths=[unreal.TopLevelAssetPath("/Script/Engine", "BlueprintGeneratedClass")], recursive_classes=True)
    for a in ar.get_assets(flt):
        n = str(a.asset_name).lower()
        p = str(a.package_name)
        if ("npcspawner" in n or "npc_spawner" in n or ("device" in n and "npc" in n)) and not p.startswith("/Game"):
            L.append("dev " + p)
    for a in ar.get_assets_by_path("/", recursive=False):
        pass
except Exception:
    L.append(traceback.format_exc())
open(TOOLS + r"\find_npc_log.txt", "w").write("\n".join(L))
