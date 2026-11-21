import unreal, traceback
L = []
try:
    for n in ("GuardSpawn", "Physics", "WildlifeSpawn", "Navigation"):
        cls = unreal.load_class(None, "/CRD_AISpawner/SpawnDefinitions/Modifiers/CharacterModifier_%s.CharacterModifier_%s_C" % (n, n))
        cdo = unreal.get_default_object(cls)
        L.append("== %s" % n)
        for p in sorted(dir(cdo)):
            if p.startswith("_"): continue
            try:
                v = cdo.get_editor_property(p)
                if callable(v): continue
                L.append("  %s = %s" % (p, str(v)[:160]))
            except Exception:
                pass
except Exception:
    L.append(traceback.format_exc())
open(r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools\probe_npcmod3_log.txt", "w").write("\n".join(L))
