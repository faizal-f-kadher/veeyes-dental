#!/usr/bin/env python3
"""Make the doctor photos uniform without touching faces.

For each original photo:
  1. cut the person out of their old background (rembg, isnet model)
  2. find the face (OpenCV) only to measure it
  3. scale and position so every face is the same size and sits at the same height
  4. place on one shared brand background (soft cool mist with a gentle light behind the head)
Pixels of the person are copied as-is: no retouching, smoothing, colour or shape changes.
"""
import os, sys, glob
import numpy as np
import cv2
from PIL import Image, ImageFilter
from rembg import remove, new_session

SRC = sys.argv[1] if len(sys.argv) > 1 else "originals"
OUT = sys.argv[2] if len(sys.argv) > 2 else "out"
os.makedirs(OUT, exist_ok=True)
SESSION = new_session("isnet-general-use")
FACE = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

BG_EDGE = (226, 236, 238)   # brand mist
BG_CENTRE = (244, 248, 248) # light behind the head

# (canvas w, h, face height as share of canvas height, face centre y as share of height)
FORMATS = {"square": (900, 900, .43, .41), "portrait": (900, 1125, .38, .41)}
LEADS = {"ramesh", "ranjana"}

def background(w, h, cx, cy):
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    d = np.sqrt(((xx - cx) / (w * .75)) ** 2 + ((yy - cy) / (h * .75)) ** 2)
    t = np.clip(d, 0, 1)[..., None]
    c0 = np.array(BG_CENTRE, np.float32); c1 = np.array(BG_EDGE, np.float32)
    return Image.fromarray((c0 * (1 - t) + c1 * t).astype(np.uint8), "RGB")

def find_face(rgb):
    g = cv2.cvtColor(np.array(rgb), cv2.COLOR_RGB2GRAY)
    faces = FACE.detectMultiScale(g, scaleFactor=1.08, minNeighbors=6, minSize=(g.shape[1] // 10, g.shape[1] // 10))
    if len(faces) == 0:
        return None
    return max(faces, key=lambda f: f[2] * f[3])  # x, y, w, h

def process(path):
    name = os.path.splitext(os.path.basename(path))[0]
    src = Image.open(path).convert("RGB")
    cut = remove(src, session=SESSION, post_process_mask=True)          # RGBA, person only
    alpha = np.array(cut.split()[-1])
    face = find_face(src)
    ys, xs = np.where(alpha > 128)
    if face is None:  # fall back to the head estimated from the mask
        top = ys.min(); width = xs.max() - xs.min()
        fh = int(width * .38); fx = int(np.median(xs[ys < top + fh])) - fh // 2
        face = (fx, top + int(fh * .15), fh, fh)
    fx, fy, fw, fh = face
    results = {}
    for fmt in (["portrait", "square"] if name in LEADS else ["square"]):
        W, H, share, cy_share = FORMATS[fmt]
        scale = (H * share) / fh
        person = cut.resize((round(cut.width * scale), round(cut.height * scale)), Image.LANCZOS)
        ox = round(W / 2 - (fx + fw / 2) * scale)
        oy = round(H * cy_share - (fy + fh / 2) * scale)
        canvas = background(W, H, W / 2, H * cy_share)
        # soft contact shadow so the cut-out sits on the background naturally
        sh = person.split()[-1].filter(ImageFilter.GaussianBlur(18)).point(lambda v: int(v * .18))
        shadow = Image.new("RGBA", person.size, (24, 56, 74, 0)); shadow.putalpha(sh)
        canvas = canvas.convert("RGBA")
        canvas.alpha_composite(shadow, (max(ox + 6, -10**6), oy + 10)) if ox + 6 >= 0 and oy + 10 >= 0 else canvas.paste(shadow, (ox + 6, oy + 10), shadow)
        if ox >= 0 and oy >= 0:
            canvas.alpha_composite(person, (ox, oy))
        else:
            canvas.paste(person, (ox, oy), person)
        # if the original photo stops above the frame bottom, fade the body out instead of a hard edge
        bottom = oy + person.height
        if bottom < H:
            fade = background(W, H, W / 2, H * cy_share).convert("RGBA")
            grad = np.zeros((H, W), np.uint8)
            start = max(0, bottom - int(H * .12))
            grad[start:bottom] = np.linspace(0, 255, bottom - start, dtype=np.uint8)[:, None]
            grad[bottom:] = 255
            fade.putalpha(Image.fromarray(grad))
            canvas.alpha_composite(fade)
        out = os.path.join(OUT, f"{name}-{fmt}.jpg")
        canvas.convert("RGB").save(out, "JPEG", quality=86, optimize=True, progressive=True)
        results[fmt] = out
    print(name, "face", tuple(int(v) for v in face), "->", list(results.values()))

if __name__ == "__main__":
    files = sorted(glob.glob(os.path.join(SRC, "*.*")))
    for f in files:
        process(f)
