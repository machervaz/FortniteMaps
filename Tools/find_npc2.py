import unreal, traceback
L = []
try:
    ar = unreal.AssetRegistryHelpers.get_asset_registry()
    flt = unreal.ARFilter(class_paths=[unreal.TopLevelAssetPath("/Script/Engine", "BlueprintGeneratedClass")], recursive_classes=True)
    for a in ar.get_assets(flt):
        n = str(a.asset_name).lower()
        if "npcspawn" in n or "npc_spawn" in n or "characterspawner" in n:
            L.append(str(a.package_name) + "." + str(a.asset_name))
except Exception:
    L.append(traceback.format_exc())
open(r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools\find_npc2_log.txt", "w").write("\n".join(L[:80]))
