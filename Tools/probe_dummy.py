import unreal, traceback
L = []
try:
    ar = unreal.AssetRegistryHelpers.get_asset_registry()
    seen = set()
    for path in ("/Game/Creative", "/Game/Athena/Items/Gameplay", "/CreativeCoreDevices", "/Game"):
        flt = unreal.ARFilter(package_paths=[path], recursive_paths=True)
        for ad in ar.get_assets(flt):
            nm = str(ad.asset_name)
            low = nm.lower()
            if ("dummy" in low or "mannequin" in low or "targetpractice" in low or "trainingtarget" in low) and str(ad.package_name) not in seen:
                seen.add(str(ad.package_name))
                L.append("%s | %s | %s" % (nm, ad.package_name, ad.asset_class_path.asset_name))
    # devices exposes en Verse
    D = r"C:\Users\marca\AppData\Local\UnrealEditorFortnite\Saved\VerseProject\testMoudon01\Digests\BuiltIn\Fortnite\Fortnite.digest.verse"
    for line in open(D, encoding="utf-8"):
        l = line.lower()
        if ("dummy" in l or "mannequin" in l) and ":=" in line:
            L.append("VERSE " + line.strip())
except Exception:
    L.append(traceback.format_exc())
open(r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools\probe_dummy_log.txt", "w", encoding="utf-8").write("\n".join(L[:300]))
