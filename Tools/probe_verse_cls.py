import unreal
R = "/5622d7d7-d1ca-438f-8a48-1286a48e2471"
L = []
for p in (R + "/_Verse.aim_trainer", R + "/_Verse.arena_panel", R + "/_Verse.aim_trainer_C"):
    try:
        o = unreal.load_object(None, p)
        L.append("%s -> %s" % (p, o))
    except Exception as ex:
        L.append("%s -> ERR %s" % (p, ex))
open(r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools\probe_verse_cls_log.txt", "w").write("\n".join(L))
