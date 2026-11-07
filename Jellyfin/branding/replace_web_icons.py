from PIL import Image
import os
import shutil

src_img_path = r"d:\Ai Session\omiflix-clean.png"
base_img = Image.open(src_img_path).convert('RGBA')

web_dir = r"C:\Program Files\Jellyfin\Server\jellyfin-web"
server_dir = r"C:\Program Files\Jellyfin\Server"
backup_dir = r"d:\Ai Session\icons_backup"

os.makedirs(backup_dir, exist_ok=True)

# 1. Server icon.ico
ico_sizes = [(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)]
server_ico = os.path.join(server_dir, "icon.ico")
if os.path.exists(server_ico):
    shutil.copy2(server_ico, os.path.join(backup_dir, "server_icon.ico"))
base_img.save(server_ico, format='ICO', sizes=ico_sizes)
print("Updated server icon.ico")

# 2. Web favicon.ico (find exact file name)
for fname in os.listdir(web_dir):
    if fname.startswith("favicon.") and fname.endswith(".ico"):
        target = os.path.join(web_dir, fname)
        shutil.copy2(target, os.path.join(backup_dir, fname))
        base_img.save(target, format='ICO', sizes=[(64, 64), (48, 48), (32, 32), (16, 16)])
        print(f"Updated {fname}")

# 3. Web root touchicon and icon-transparent files
for fname in os.listdir(web_dir):
    full_path = os.path.join(web_dir, fname)
    if not os.path.isfile(full_path):
        continue
    
    if fname.startswith("touchicon.") and fname.endswith(".png"):
        shutil.copy2(full_path, os.path.join(backup_dir, fname))
        base_img.resize((180, 180), Image.Resampling.LANCZOS).save(full_path)
        print(f"Updated {fname} (180x180)")
    elif fname.startswith("touchicon144.") and fname.endswith(".png"):
        shutil.copy2(full_path, os.path.join(backup_dir, fname))
        base_img.resize((144, 144), Image.Resampling.LANCZOS).save(full_path)
        print(f"Updated {fname} (144x144)")
    elif fname.startswith("icon-transparent.") and fname.endswith(".png"):
        shutil.copy2(full_path, os.path.join(backup_dir, fname))
        base_img.resize((512, 512), Image.Resampling.LANCZOS).save(full_path)
        print(f"Updated {fname} (512x512)")
    elif fname.startswith("notificationicon.") and fname.endswith(".png"):
        shutil.copy2(full_path, os.path.join(backup_dir, fname))
        base_img.resize((512, 512), Image.Resampling.LANCZOS).save(full_path)
        print(f"Updated {fname} (512x512)")

# 4. favicons/ directory
favicons_dir = os.path.join(web_dir, "favicons")
if os.path.exists(favicons_dir):
    size_map = {
        "touchicon.png": (192, 192),
        "touchicon72.png": (72, 72),
        "touchicon114.png": (114, 114),
        "touchicon144.png": (144, 144),
        "touchicon512.png": (512, 512),
    }
    for fname, (w, h) in size_map.items():
        fpath = os.path.join(favicons_dir, fname)
        if os.path.exists(fpath):
            shutil.copy2(fpath, os.path.join(backup_dir, f"favicons_{fname}"))
        base_img.resize((w, h), Image.Resampling.LANCZOS).save(fpath)
        print(f"Updated favicons/{fname} ({w}x{h})")

with open(r"d:\Ai Session\replace_success.txt", "w") as f:
    f.write("SUCCESS")

print("All web icons replaced successfully!")
