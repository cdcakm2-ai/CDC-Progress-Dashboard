import os
import shutil

dist_dir = 'dist'
files_to_sync = [
    'index.html',
    'data_version.json',
    'css/glassmorphism.css',
    'css/responsive.css',
    'css/style.css',
    'js/app.js',
    'js/charts.js',
    'js/data.js',
    'js/sheets-service.js'
]

for rel_path in files_to_sync:
    src = rel_path
    dst = os.path.join(dist_dir, rel_path)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.copy2(src, dst)
    print(f"Synced: {src} -> {dst} ({os.path.getsize(dst)} bytes)")

print("\nDist bundle is fully synchronized!")
