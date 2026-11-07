import urllib.parse
import re

with open('omiflix-logo.svg', 'r', encoding='utf-8') as f:
    svg_raw = f.read()

# Minify svg
svg_min = re.sub(r'\s+', ' ', svg_raw).strip()
encoded_svg = urllib.parse.quote(svg_min)
data_uri = f"data:image/svg+xml,{encoded_svg}"

# Calculate aspect ratio
m = re.search(r'viewBox="0 0 (\d+) (\d+)"', svg_min)
w, h = float(m.group(1)), float(m.group(2))
ratio = round(w / h, 4)

css = f"""@import url("https://cdn.jsdelivr.net/gh/ahza-code/Netflin@latest/Theme/Netflin.min.css");
@import url("https://cdn.jsdelivr.net/gh/ahza-code/Netflin@latest/Theme/add-ons/media-covers.min.css");
@import url("https://cdn.jsdelivr.net/gh/Druidblack/jellyfin-icon-metadata@main/public-icon.css");
@import url("https://cdn.jsdelivr.net/gh/KartoffelChipss/Jellyfin-Lucide@main/theme/jellyfin-lucide.css");

:root {{
  --nf-radius: 12px;
  --nf-wordmark-omiflix: url("{data_uri}");
  --nf-wordmark-ratio-omiflix: {ratio};
}}

/* Netflix Curved Wordmark: OMIFLIX */
.MuiAppBar-root :is(.MuiStack-root, .dashboard-appBar) > .MuiButton-root:has(.MuiButton-startIcon > img)::before,
.MuiDrawer-paper > .MuiBox-root > .MuiList-root:first-child > li:first-child > a::before {{
    content: "" !important;
    height: 1.59rem !important;
    aspect-ratio: var(--nf-wordmark-ratio-omiflix) !important;
    background: var(--nf-wordmark-omiflix) center / contain no-repeat !important;
    display: inline-block !important;
}}

/* Hide Back and Forward navigation buttons */
button[title="Back"],
button[title="Forward"],
button[aria-label="Back"],
button[aria-label="Forward"] {{
    display: none !important;
}}"""

# Write to branding.xml
branding_path = r"C:\ProgramData\Jellyfin\Server\config\branding.xml"
with open(branding_path, 'r', encoding='utf-8') as f:
    branding_content = f.read()

# Replace CustomCss
updated_branding = re.sub(
    r'<CustomCss>.*?</CustomCss>',
    f'<CustomCss>{css}</CustomCss>',
    branding_content,
    flags=re.DOTALL
)

with open(branding_path, 'w', encoding='utf-8') as f:
    f.write(updated_branding)

print("branding.xml successfully updated with curved OMIFLIX wordmark!")
print(f"Aspect ratio: {ratio}")
