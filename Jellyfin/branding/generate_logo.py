import math
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen

font = TTFont('bebas.ttf')
glyphset = font.getGlyphSet()
cmap = font.getBestCmap()

text = 'OMIFLIX'
tracking = -15  # slightly tight tracking like Netflix

glyphs_data = []
curr_x = 0.0
for char in text:
    gname = cmap[ord(char)]
    glyph = glyphset[gname]
    pen = RecordingPen()
    glyph.draw(pen)
    glyphs_data.append((char, gname, curr_x, pen.value))
    curr_x += glyph.width + tracking

total_w = curr_x - tracking
cap_h = 700.0
arch_h = 95.0  # Netflix characteristic bottom curve (~13.5% of cap height)

def warp_point(x, y):
    u = x / total_w
    u = max(0.0, min(1.0, u))
    # parabolic arc: 0 at edges (u=0, u=1), arch_h in middle (u=0.5)
    y_base = 4.0 * arch_h * u * (1.0 - u)
    factor = (cap_h - y_base) / cap_h
    new_y = y_base + y * factor
    return x, new_y

def subdivide_line(p0, p1, max_len=15.0):
    dx = p1[0] - p0[0]
    dy = p1[1] - p0[1]
    dist = math.hypot(dx, dy)
    if dist <= max_len:
        return [p1]
    n = int(math.ceil(dist / max_len))
    pts = []
    for i in range(1, n + 1):
        t = i / n
        pts.append((p0[0] + dx * t, p0[1] + dy * t))
    return pts

def subdivide_quad(p0, p1, p2):
    pts = []
    n = 8
    for i in range(1, n + 1):
        t = i / n
        omt = 1.0 - t
        qx = omt*omt*p0[0] + 2*omt*t*p1[0] + t*t*p2[0]
        qy = omt*omt*p0[1] + 2*omt*t*p1[1] + t*t*p2[1]
        pts.append((qx, qy))
    return pts

svg_d = []
for char, gname, offset_x, ops in glyphs_data:
    curr_pt = (0.0, 0.0)
    for op, args in ops:
        if op == 'moveTo':
            pt = (args[0][0] + offset_x, args[0][1])
            curr_pt = pt
            wpt = warp_point(*pt)
            svg_d.append(f'M {wpt[0]:.1f} {cap_h - wpt[1]:.1f}')
        elif op == 'lineTo':
            pt = (args[0][0] + offset_x, args[0][1])
            sub_pts = subdivide_line(curr_pt, pt)
            for sp in sub_pts:
                wpt = warp_point(*sp)
                svg_d.append(f'L {wpt[0]:.1f} {cap_h - wpt[1]:.1f}')
            curr_pt = pt
        elif op == 'qCurveTo':
            pts = [(p[0] + offset_x, p[1]) for p in args]
            if len(pts) == 2:
                sub_pts = subdivide_quad(curr_pt, pts[0], pts[1])
            else:
                sub_pts = subdivide_quad(curr_pt, pts[0], pts[-1])
            for sp in sub_pts:
                wpt = warp_point(*sp)
                svg_d.append(f'L {wpt[0]:.1f} {cap_h - wpt[1]:.1f}')
            curr_pt = pts[-1]
        elif op == 'closePath':
            svg_d.append('Z')

path_str = ' '.join(svg_d)
aspect_ratio = total_w / cap_h

svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {int(total_w)} {int(cap_h)}">
  <path fill="#e50914" d="{path_str}"/>
</svg>'''

with open('omiflix-logo.svg', 'w', encoding='utf-8') as f:
    f.write(svg_content)

print(f"Generated omiflix-logo.svg successfully!")
print(f"Total Width: {total_w}, Height: {cap_h}, Aspect Ratio: {aspect_ratio:.4f}")
