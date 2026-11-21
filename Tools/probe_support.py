import unreal, traceback
TOOLS = r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools"
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
L = []
KEYS = ("support", "collapse", "structur", "anchor", "ground", "unsupport", "integrity", "destroy", "physics")
try:
    pb = None
    isl = None
    brick = None
    for a in eas.get_all_level_actors():
        n = a.get_class().get_name()
        p = a.get_actor_location()
        if n.startswith("PBWA_W1_Solid") and p.z > 9000 and pb is None:
            pb = a
        if n.startswith("BrickSimple") and brick is None:
            brick = a
        if "ExperienceSettings" in n or "IslandSettings" in n:
            isl = a
    for nm, obj in (("PBWA", pb), ("Brick", brick), ("Island", isl)):
        if obj is None:
            L.append("%s : absent" % nm); continue
        L.append("%s : %s (%s)" % (nm, obj.get_actor_label(), obj.get_class().get_name()))
        L.append("   py : " + ", ".join(x for x in dir(obj) if any(k in x.lower() for k in KEYS)))
except Exception:
    L.append(traceback.format_exc())
open(TOOLS + r"\probe_support_log.txt", "w").write("\n".join(L))
