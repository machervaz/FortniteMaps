import unreal, traceback
L = []
try:
    ar = unreal.AssetRegistryHelpers.get_asset_registry()
    for ad in ar.get_assets(unreal.ARFilter(package_paths=["/CRD_AISpawner"], recursive_paths=True)):
        L.append("%s | %s | %s" % (ad.asset_name, ad.package_name, ad.asset_class_path.asset_name))
    cls = unreal.load_class(None, "/CRD_AISpawner/SpawnDefinitions/Modifiers/CharacterModifier_Movement.CharacterModifier_Movement_C")
    cdo = unreal.get_default_object(cls)
    L.append("== CDO %s" % cdo)
    for p in sorted(dir(cdo)):
        if p.startswith("_"): continue
        try:
            v = cdo.get_editor_property(p)
            L.append("  %s = %s" % (p, str(v)[:150]))
        except Exception:
            pass
except Exception:
    L.append(traceback.format_exc())
open(r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools\probe_npcmod2_log.txt", "w").write("\n".join(L[:300]))
