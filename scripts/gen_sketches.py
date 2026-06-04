"""
Bosquejos REBEL LUXURY — trazos finos estilo lapiz de moda.
Genera: Air Force One, Ferrari, cadena, rosa, corona.
"""
import math, random, sys, io
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

ILLUS = Path(__file__).resolve().parent.parent / "assets" / "illustrations"
ILLUS.mkdir(parents=True, exist_ok=True)

INK  = (12, 12, 12)
WITE = (255, 255, 255)


def bezier3(p0, p1, p2, p3, n=40):
    pts = []
    for i in range(n + 1):
        t = i / n
        x = (1-t)**3*p0[0] + 3*(1-t)**2*t*p1[0] + 3*(1-t)*t**2*p2[0] + t**3*p3[0]
        y = (1-t)**3*p0[1] + 3*(1-t)**2*t*p1[1] + 3*(1-t)*t**2*p2[1] + t**3*p3[1]
        pts.append((int(x), int(y)))
    return pts


def bezier2(p0, p1, p2, n=25):
    pts = []
    for i in range(n + 1):
        t = i / n
        x = (1-t)**2*p0[0] + 2*(1-t)*t*p1[0] + t**2*p2[0]
        y = (1-t)**2*p0[1] + 2*(1-t)*t*p1[1] + t**2*p2[1]
        pts.append((int(x), int(y)))
    return pts


def to_transparent(img):
    arr = np.array(img.convert("RGBA"), dtype=np.float32)
    bright = (arr[:,:,0]+arr[:,:,1]+arr[:,:,2])/3
    alpha = np.clip((230 - bright)/190 * 255, 0, 255)
    arr[:,:,3] = alpha.astype(np.uint8)
    out = Image.fromarray(arr.astype(np.uint8), "RGBA")
    r,g,b,a = out.split()
    a = a.filter(ImageFilter.GaussianBlur(0.7))
    return Image.merge("RGBA", (r,g,b,a))


# ══════════════════════════════════════════════════════════════════
#  AIR FORCE ONE  —  vista lateral correcta
# ══════════════════════════════════════════════════════════════════
def gen_af1(S=1000):
    W, H = S, int(S * 0.62)
    img = Image.new("RGB", (W,H), WITE)
    d   = ImageDraw.Draw(img)

    # helper: fraction → pixel
    def x(r): return int(r * W)
    def y(r): return int(r * H)

    T3 = max(3, S//150)   # thick
    T2 = max(2, S//260)   # medium
    T1 = max(1, S//500)   # thin

    # ── SOLE (goma inferior) ──────────────────────────────────────
    # Bottom rubber sole: flat rectangle with rounded front toe
    # Outer sole outline
    sole = (
        bezier2((x(.07),y(.80)), (x(.07),y(.97)), (x(.20),y(.97)), 15) +
        [(x(.78),y(.97))] +
        bezier2((x(.78),y(.97)), (x(.93),y(.97)), (x(.93),y(.82)), 15) +
        [(x(.93),y(.73))]
    )
    d.line(sole, fill=INK, width=T3)
    d.line([(x(.07),y(.80)), (x(.93),y(.80))], fill=INK, width=T2)  # midsole top
    # Midsole texture lines
    for fy in (.84, .87, .90, .93):
        d.line([(x(.08),y(fy)), (x(.92),y(fy))], fill=INK, width=T1)
    # Air unit oval at heel
    d.ellipse([x(.12),y(.85), x(.28),y(.93)], outline=INK, width=T1)

    # ── UPPER BODY ────────────────────────────────────────────────
    # Back of shoe (heel counter) — vertical with slight curve
    heel_back = bezier2((x(.07),y(.80)), (x(.05),y(.50)), (x(.08),y(.28)), 20)
    d.line(heel_back, fill=INK, width=T3)

    # Top of shoe from heel to tongue opening
    # AF1: heel drops steeply then rises into the ankle collar, then slopes down to toe
    top_curve = (
        bezier3((x(.08),y(.28)), (x(.12),y(.18)), (x(.25),y(.12)), (x(.38),y(.10)), 25) +
        bezier3((x(.38),y(.10)), (x(.48),y(.08)), (x(.58),y(.10)), (x(.65),y(.16)), 20)
    )
    d.line(top_curve, fill=INK, width=T2)

    # Ankle collar opening (oval cut)
    collar_open = bezier3((x(.08),y(.28)), (x(.15),y(.22)), (x(.28),y(.18)), (x(.38),y(.10)), 20)
    d.line(collar_open, fill=INK, width=T2)

    # Toe box — rounded bulbous nose (AF1 signature)
    toe = (
        bezier3((x(.65),y(.16)), (x(.78),y(.18)), (x(.88),y(.32)), (x(.91),y(.52)), 25) +
        bezier2((x(.91),y(.52)), (x(.93),y(.68)), (x(.93),y(.80)), 15)
    )
    d.line(toe, fill=INK, width=T3)

    # Bottom of upper / vamp line
    vamp = bezier3((x(.07),y(.80)), (x(.25),y(.77)), (x(.60),y(.75)), (x(.93),y(.80)), 30)
    d.line(vamp, fill=INK, width=T2)

    # Toe cap seam
    toe_seam = bezier3((x(.72),y(.20)), (x(.80),y(.35)), (x(.84),y(.56)), (x(.84),y(.75)), 20)
    d.line(toe_seam, fill=INK, width=T1)

    # Vamp panel seam (from collar to mid-toe)
    vamp_seam = bezier3((x(.22),y(.30)), (x(.40),y(.26)), (x(.58),y(.26)), (x(.72),y(.30)), 20)
    d.line(vamp_seam, fill=INK, width=T1)

    # ── TONGUE ────────────────────────────────────────────────────
    tongue_l = bezier2((x(.36),y(.10)), (x(.34),y(.00)), (x(.42),y(-.04)), 15)
    tongue_r = bezier2((x(.60),y(.10)), (x(.62),y(.00)), (x(.54),y(-.04)), 15)
    d.line(tongue_l, fill=INK, width=T2)
    d.line(tongue_r, fill=INK, width=T2)
    # Tongue tip (off top of image is fine — creates bleed effect)

    # ── SWOOSH ────────────────────────────────────────────────────
    # AF1 swoosh: starts thin at back-low, sweeps up-forward, ends thin
    sw_pts = bezier3((x(.16),y(.68)), (x(.28),y(.44)), (x(.52),y(.32)), (x(.68),y(.24)), 40)
    sw_back = bezier3((x(.68),y(.24)), (x(.60),y(.30)), (x(.36),y(.46)), (x(.18),y(.64)), 40)

    # Variable width swoosh
    n = len(sw_pts)
    for i in range(n-1):
        t = i/(n-1)
        w = max(T1, int(T1 + (T3*3.0-T1) * math.sin(math.pi * t * 0.85)))
        d.line([sw_pts[i], sw_pts[i+1]], fill=INK, width=w)
    d.line(sw_back, fill=INK, width=T1)

    # ── LACE HOLES + LACES ───────────────────────────────────────
    lace_xs = [.38, .43, .48, .53, .58, .63]
    lace_ys = [.14, .13, .12, .11, .13, .15]
    for i in range(len(lace_xs)):
        ex = x(lace_xs[i]); ey = y(lace_ys[i]); r=max(4,S//120)
        d.ellipse([ex-r,ey-r,ex+r,ey+r], outline=INK, width=T1)
    # Cross laces
    for i in range(len(lace_xs)-1):
        d.line([(x(lace_xs[i]),y(lace_ys[i])), (x(lace_xs[i+1]),y(lace_ys[i+1]))],
               fill=INK, width=T1)

    # ── HEEL TAB ─────────────────────────────────────────────────
    d.line([(x(.07),y(.36)), (x(.04),y(.36)), (x(.04),y(.50)), (x(.07),y(.50))],
           fill=INK, width=T2)

    # Save
    dst = ILLUS / "illus_af1.png"
    to_transparent(img).save(dst, "PNG")
    return dst


# ══════════════════════════════════════════════════════════════════
#  FERRARI 488 / F40  —  vista lateral
# ══════════════════════════════════════════════════════════════════
def gen_ferrari(S=1000):
    W, H = S, int(S * 0.52)
    img = Image.new("RGB", (W,H), WITE)
    d   = ImageDraw.Draw(img)

    def x(r): return int(r*W)
    def y(r): return int(r*H)
    T3 = max(3, S//150); T2 = max(2, S//280); T1 = max(1, S//500)

    # Ground line
    d.line([(x(.04),y(.88)), (x(.96),y(.88))], fill=INK, width=T1)

    # ── WHEELS ───────────────────────────────────────────────────
    for cx_r, cy_r, wr in [(0.18,0.80,0.11), (0.76,0.80,0.11)]:
        cx=x(cx_r); cy=y(cy_r); R=int(wr*H)
        r_inner = int(R*0.62); r_hub = int(R*0.18)
        # Tire
        d.ellipse([cx-R,cy-R,cx+R,cy+R], outline=INK, width=T3)
        # Rim
        d.ellipse([cx-r_inner,cy-r_inner,cx+r_inner,cy+r_inner], outline=INK, width=T2)
        # Hub
        d.ellipse([cx-r_hub,cy-r_hub,cx+r_hub,cy+r_hub], fill=INK)
        # Spokes (5)
        for a in range(0, 360, 72):
            rad = math.radians(a)
            x1=cx+int(r_hub*1.3*math.cos(rad)); y1=cy+int(r_hub*1.3*math.sin(rad))
            x2=cx+int(r_inner*0.9*math.cos(rad)); y2=cy+int(r_inner*0.9*math.sin(rad))
            d.line([(x1,y1),(x2,y2)], fill=INK, width=T2)

    # ── BODY SILHOUETTE ──────────────────────────────────────────
    # Front bumper to windshield base
    front = bezier3((x(.04),y(.70)), (x(.04),y(.58)), (x(.06),y(.46)), (x(.14),y(.40)), 25)
    # Hood slope (low, aggressive)
    hood = bezier3((x(.14),y(.40)), (x(.22),y(.36)), (x(.30),y(.30)), (x(.38),y(.26)), 20)
    # A-pillar + roof
    roof = bezier3((x(.38),y(.26)), (x(.44),y(.18)), (x(.56),y(.16)), (x(.64),y(.22)), 25)
    # C-pillar + rear
    rear_top = bezier3((x(.64),y(.22)), (x(.70),y(.26)), (x(.78),y(.32)), (x(.86),y(.40)), 20)
    # Rear deck + bumper
    rear = bezier3((x(.86),y(.40)), (x(.92),y(.48)), (x(.94),y(.60)), (x(.94),y(.70)), 20)

    full_body = front + hood + roof + rear_top + rear
    d.line(full_body, fill=INK, width=T3)

    # Rocker / sill line (underside of body)
    sill = bezier3((x(.08),y(.70)), (x(.30),y(.68)), (x(.60),y(.68)), (x(.90),y(.70)), 30)
    d.line(sill, fill=INK, width=T2)

    # Close front + rear verticals
    d.line([(x(.04),y(.70)), (x(.08),y(.70))], fill=INK, width=T2)
    d.line([(x(.94),y(.70)), (x(.90),y(.70))], fill=INK, width=T2)

    # ── WINDSHIELD ───────────────────────────────────────────────
    # A-pillar interior
    d.line([x(.38),y(.26), x(.40),y(.40)], fill=INK, width=T2)
    d.line([x(.64),y(.22), x(.63),y(.38)], fill=INK, width=T2)
    # Dashboard line
    d.line([(x(.40),y(.40)), (x(.63),y(.38))], fill=INK, width=T1)

    # ── BODY LINES / CREASE ──────────────────────────────────────
    # Main crease from front wheel arch to rear
    crease = bezier3((x(.14),y(.52)), (x(.30),y(.48)), (x(.60),y(.48)), (x(.86),y(.52)), 30)
    d.line(crease, fill=INK, width=T1)

    # ── WHEEL ARCHES ─────────────────────────────────────────────
    for cx_r in (0.18, 0.76):
        cx=x(cx_r); cy=y(.68); R=int(.12*H)
        # Arch cutout
        pts = []
        for a in range(180, 361, 6):
            rad = math.radians(a)
            pts.append((cx+int(R*math.cos(rad)), cy+int(R*math.sin(rad))))
        # Just draw top arch
        arch_pts = []
        for a in range(200, 340, 5):
            rad = math.radians(a)
            arch_pts.append((cx+int(R*math.cos(rad)), cy+int(R*0.85*math.sin(rad))))
        d.line(arch_pts, fill=INK, width=T2)

    # ── DOOR LINE ────────────────────────────────────────────────
    door_curve = bezier3((x(.40),y(.40)), (x(.42),y(.38)), (x(.60),y(.38)), (x(.62),y(.40)), 15)
    d.line(door_curve, fill=INK, width=T1)
    d.line([(x(.42),y(.40)), (x(.42),y(.68))], fill=INK, width=T1)
    d.line([(x(.62),y(.40)), (x(.62),y(.68))], fill=INK, width=T1)
    # Door handle
    d.rectangle([x(.52),y(.50), x(.58),y(.53)], outline=INK, width=T1)

    # ── AIR INTAKE (side) ─────────────────────────────────────────
    air_pts = [
        (x(.68),y(.44)), (x(.72),y(.42)), (x(.78),y(.44)),
        (x(.78),y(.54)), (x(.68),y(.56)), (x(.68),y(.44))
    ]
    d.line(air_pts, fill=INK, width=T1)
    # Slats inside
    for fy in (.46, .49, .52):
        d.line([(x(.69),y(fy)), (x(.77),y(fy))], fill=INK, width=T1)

    # ── HEADLIGHT ────────────────────────────────────────────────
    d.line([(x(.06),y(.46)), (x(.13),y(.44)), (x(.13),y(.52)), (x(.06),y(.54))], fill=INK, width=T1)

    # ── TAILLIGHT ────────────────────────────────────────────────
    d.line([(x(.90),y(.44)), (x(.93),y(.46)), (x(.93),y(.56)), (x(.90),y(.58))], fill=INK, width=T1)

    # ── EXHAUST ──────────────────────────────────────────────────
    d.ellipse([x(.87),y(.63), x(.91),y(.67)], outline=INK, width=T2)
    d.ellipse([x(.90),y(.62), x(.94),y(.66)], outline=INK, width=T2)

    # Save
    dst = ILLUS / "illus_ferrari.png"
    to_transparent(img).save(dst, "PNG")
    return dst


# ══════════════════════════════════════════════════════════════════
#  CADENA CUBANA  —  joya de lujo urbano
# ══════════════════════════════════════════════════════════════════
def gen_chain(S=700):
    W, H = S, S
    img = Image.new("RGB", (W,H), WITE)
    d   = ImageDraw.Draw(img)

    cx, cy = W//2, H//2
    T3 = max(4, S//100); T1 = max(1, S//350)
    n_links = 11
    lw = int(S*.075); lh = int(S*.045)
    gap = int(S*.058)
    ang = math.radians(-30)

    total = n_links * gap
    sx = cx - int(total/2*math.cos(ang))
    sy = cy - int(total/2*math.sin(ang))

    for i in range(n_links):
        lx = sx + int(i*gap*math.cos(ang))
        ly = sy + int(i*gap*math.sin(ang))
        a = ang if i%2==0 else ang + math.pi/2
        pts = []
        for deg in range(0, 361, 8):
            t = math.radians(deg)
            ex = lx + int(lw/2*math.cos(t)*math.cos(a) - lh/2*math.sin(t)*math.sin(a))
            ey = ly + int(lw/2*math.cos(t)*math.sin(a) + lh/2*math.sin(t)*math.cos(a))
            pts.append((ex,ey))
        d.line(pts+[pts[0]], fill=INK, width=T3)
        # Highlight
        hi = pts[3:7]
        if len(hi) > 1:
            d.line(hi, fill=(160,160,160), width=T1)

    # Colgante: estrella de 5 puntas
    star_cx = lx + int(gap*1.2*math.cos(ang))
    star_cy = ly + int(gap*1.2*math.sin(ang))
    R_out = int(S*.07); R_in = int(S*.03)
    star_pts = []
    for k in range(10):
        r = R_out if k%2==0 else R_in
        a2 = math.radians(k*36 - 90)
        star_pts.append((star_cx + int(r*math.cos(a2)), star_cy + int(r*math.sin(a2))))
    d.polygon(star_pts, outline=INK, fill=None)
    d.line(star_pts + [star_pts[0]], fill=INK, width=T3)

    dst = ILLUS / "illus_chain.png"
    to_transparent(img).save(dst, "PNG")
    return dst


# ══════════════════════════════════════════════════════════════════
#  RUN
# ══════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    print("Generando bosquejos REBEL LUXURY...")
    a = gen_af1(1000);       print(f"  AF1:     {a.name} ({a.stat().st_size//1024}KB)")
    f = gen_ferrari(1000);   print(f"  Ferrari: {f.name} ({f.stat().st_size//1024}KB)")
    c = gen_chain(700);      print(f"  Chain:   {c.name} ({c.stat().st_size//1024}KB)")
    print("LISTO")
