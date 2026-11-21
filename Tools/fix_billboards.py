import unreal, traceback
OUT = r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools\fix_billboards_out.txt"
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
lines = []
for a in eas.get_all_level_actors():
    lab = a.get_actor_label()
    if not lab.startswith("LOBBY_Billboard_"):
        continue
    try:
        r = a.get_actor_rotation()
        a.set_actor_rotation(unreal.Rotator(roll=r.roll, pitch=r.pitch, yaw=r.yaw + 90.0), False)
        o, e = a.get_actor_bounds(False)
        lines.append("%s rot=%s ext=%s" % (lab, a.get_actor_rotation(), e))
        for p in ["text_size", "TextSize", "font_size"]:
            try:
                a.set_editor_property(p, 40); lines.append("  size via " + p); break
            except Exception:
                pass
        props = [n for n in dir(a) if "text" in n.lower() or "align" in n.lower()]
        lines.append("  props " + str(props[:40]))
    except Exception:
        lines.append(traceback.format_exc())
unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
with open(OUT, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))
