"""Render every frame from two cameras and build the critic's review images.

For each animation and iteration it writes, under work/<anim>/iter_N/:
  frames/fNNN.png      the 3/4 view and the side view side by side, with the frame number
  review/sheet_K.png   numbered contact sheets, 20 frames each (4 columns x 5 rows)
  review/onion.png     side-view onion skin of every 2nd frame (shows arcs and spacing)
  review/curves.png    graph-editor style plot of every animated channel, with key markers
  preview.gif          a real-time (30 fps) preview
"""
import os

import bpy
from PIL import Image, ImageChops, ImageDraw, ImageFont

from pipeline import curves

CELL = 220
SHEET_COLS, SHEET_ROWS = 4, 5


def _font(size=14):
    for path in ("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
                 "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"):
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def render_frames(out_dir):
    scene = bpy.context.scene
    fdir = os.path.join(out_dir, "frames")
    tmp = os.path.join(out_dir, "_tmp")
    os.makedirs(fdir, exist_ok=True)
    os.makedirs(tmp, exist_ok=True)
    font = _font(15)
    paths = []
    for f in range(scene.frame_start, scene.frame_end + 1):
        scene.frame_set(f)
        views = []
        for cam in ("Cam34", "CamSide"):
            scene.camera = bpy.data.objects[cam]
            scene.render.filepath = os.path.join(tmp, f"{cam}.png")
            bpy.ops.render.render(write_still=True)
            views.append(Image.open(scene.render.filepath).convert("RGB"))
        combo = Image.new("RGB", (CELL * 2, CELL), "white")
        combo.paste(views[0], (0, 0))
        combo.paste(views[1], (CELL, 0))
        d = ImageDraw.Draw(combo)
        d.rectangle([0, 0, 58, 20], fill=(20, 20, 24))
        d.text((4, 2), f"F{f:03d}", fill=(255, 255, 255), font=font)
        d.line([(CELL, 0), (CELL, CELL)], fill=(255, 255, 255), width=2)
        p = os.path.join(fdir, f"f{f:03d}.png")
        combo.save(p)
        paths.append(p)
    return paths


def contact_sheets(frame_paths, out_dir, title):
    rdir = os.path.join(out_dir, "review")
    os.makedirs(rdir, exist_ok=True)
    per = SHEET_COLS * SHEET_ROWS
    font = _font(18)
    sheets = []
    for si in range(0, len(frame_paths), per):
        chunk = frame_paths[si:si + per]
        w, h = CELL * 2, CELL
        sheet = Image.new("RGB", (SHEET_COLS * w + (SHEET_COLS - 1) * 6, SHEET_ROWS * h + (SHEET_ROWS - 1) * 6 + 30), (40, 40, 46))
        d = ImageDraw.Draw(sheet)
        first = int(os.path.basename(chunk[0])[1:4])
        last = int(os.path.basename(chunk[-1])[1:4])
        d.text((8, 5), f"{title}  frames {first}-{last}   (left: 3/4 front view | right: side view, character faces right)",
               fill=(255, 255, 255), font=font)
        for i, p in enumerate(chunk):
            r, c = divmod(i, SHEET_COLS)
            sheet.paste(Image.open(p), (c * (w + 6), 30 + r * (h + 6)))
        sp = os.path.join(rdir, f"sheet_{si // per + 1}.png")
        sheet.save(sp)
        sheets.append(sp)
    return sheets


def onion_skin(frame_paths, out_dir, step=2):
    """Darken-blend the side views, so all poses overlap with older frames lighter."""
    side = [Image.open(p).crop((CELL, 0, CELL * 2, CELL)) for p in frame_paths[::step]]
    base = Image.new("RGB", (CELL, CELL), (255, 255, 255))
    n = len(side)
    for i, im in enumerate(side):
        fade = 0.25 + 0.75 * (i + 1) / n
        faded = Image.blend(Image.new("RGB", im.size, (255, 255, 255)), im, fade)
        base = ImageChops.darker(base, faded)
    base = base.resize((CELL * 3, CELL * 3), Image.LANCZOS)
    d = ImageDraw.Draw(base)
    d.text((8, 6), f"side-view onion skin, every {step} frames (darker = later)", fill=(0, 0, 0), font=_font(16))
    p = os.path.join(out_dir, "review", "onion.png")
    base.save(p)
    return p


def curve_plot(out_dir, title):
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    scene = bpy.context.scene
    fmap = curves.fcurve_map()
    frames, data = curves.sample_all(scene.frame_start, scene.frame_end, step=0.5)
    bones = sorted({b for b, _ in fmap})
    ncols = 3
    nrows = (len(bones) + ncols - 1) // ncols
    fig, axes = plt.subplots(nrows, ncols, figsize=(15, 2.3 * nrows), squeeze=False)
    colors = {"rx": "#d62728", "ry": "#2ca02c", "rz": "#1f77b4", "lx": "#ff7f0e", "ly": "#9467bd", "lz": "#8c564b"}
    for ax, bone in zip(axes.flat, bones):
        for (b, ch), fc in sorted(fmap.items()):
            if b != bone:
                continue
            vals = data[(b, ch)]
            scale = 100.0 if ch.startswith("l") else 1.0
            label = f"{ch} (studs x100)" if scale != 1 else ch
            ax.plot(frames, [v * scale for v in vals], color=colors[ch], lw=1.4, label=label)
            kx = [kp.co[0] for kp in fc.keyframe_points]
            ky = [curves.to_display(ch, kp.co[1]) * scale for kp in fc.keyframe_points]
            ax.plot(kx, ky, "o", color=colors[ch], ms=3.5)
        ax.set_title(bone, fontsize=9)
        ax.grid(alpha=0.3)
        ax.tick_params(labelsize=7)
        ax.set_xlim(scene.frame_start, scene.frame_end)
        ax.legend(fontsize=6, loc="upper right")
    for ax in list(axes.flat)[len(bones):]:
        ax.axis("off")
    fig.suptitle(f"{title}: F-curves (degrees; dots = keys; x axis = frame)", fontsize=12)
    fig.tight_layout()
    p = os.path.join(out_dir, "review", "curves.png")
    fig.savefig(p, dpi=80)
    plt.close(fig)
    return p


def gif(frame_paths, out_path, fps=30):
    ims = [Image.open(p).convert("P", palette=Image.ADAPTIVE, colors=128) for p in frame_paths]
    ims[0].save(out_path, save_all=True, append_images=ims[1:], duration=int(1000 / fps), loop=0, optimize=True)
    return out_path


def render_review(out_dir, title):
    frames = render_frames(out_dir)
    sheets = contact_sheets(frames, out_dir, title)
    onion = onion_skin(frames, out_dir)
    plot = curve_plot(out_dir, title)
    g = gif(frames, os.path.join(out_dir, "preview.gif"))
    return {"sheets": sheets, "onion": onion, "curves": plot, "gif": g, "frames": frames}
