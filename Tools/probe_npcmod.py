import unreal, traceback
L = []
try:
    ar = unreal.AssetRegistryHelpers.get_asset_registry()
    for ad in ar.get_assets_by_class(unreal.TopLevelAssetPath("/Script/Engine", "BlueprintGeneratedClass"), True):
        nm = str(ad.asset_name); low = nm.lower()
        if ("npc" in low or "modifier" in low or "characterdefinition" in low) and ("glid" in low or "skydiv" in low or "fly" in low or "movement" in low or "locomot" in low):
            L.append("BP %s | %s" % (nm, ad.package_name))
    for ad in ar.get_assets(unreal.ARFilter(package_paths=["/"], recursive_paths=True)):
        nm = str(ad.asset_name); low = nm.lower()
        if ("glid" in low and ("npc" in low or "ai" in low.split("_") or "modifier" in low or "component" in low)):
            L.append("A %s | %s | %s" % (nm, ad.package_name, ad.asset_class_path.asset_name))
    d = unreal.load_asset("/5622d7d7-d1ca-438f-8a48-1286a48e2471/Lobby/NPC/NPC_TrainingBot")
    L.append("DEF %s" % d)
    for p in dir(d):
        if not p.startswith("_") and not callable(getattr(d, p, None)):
            try: L.append("  %s = %s" % (p, str(d.get_editor_property(p))[:200]))
            except Exception: pass
except Exception:
    L.append(traceback.format_exc())
open(r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools\probe_npcmod_log.txt", "w").write("\n".join(L[:200]))
