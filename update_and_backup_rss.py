#!/usr/bin/env python3
import os, time, subprocess

# --- Config ---
AUDIO_DIRS = [
    "/Users/xavierangle/mr-x-podcast/MrX_normalized",
    "/Users/xavierangle/mr-x-podcast/MrX_downloads"
]
OUTPUT_FILE = "feed.xml"   # ⚡ On génère feed.xml désormais
BACKUP_DIR = "backups"

AUTHOR = "Patrick Pesnot"
OWNER_NAME = "MrX Podcast"
OWNER_EMAIL = "ton.email@example.com"   # ⚠️ remplace par ton email réel
COVER_URL = "https://angles974-tech.github.io/mr-x-podcast/assets/mr_x_cover.jpg"

# --- Fonction pour récupérer la durée avec ffprobe ---
def get_duration(file_path):
    try:
        result = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "default=noprint_wrappers=1:nokey=1", file_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        seconds = float(result.stdout.strip())
        h = int(seconds // 3600)
        m = int((seconds % 3600) // 60)
        s = int(seconds % 60)
        return f"{h:02}:{m:02}:{s:02}"
    except:
        return "00:00:00"

# --- Prépare la liste des fichiers ---
files = []
for d in AUDIO_DIRS:
    if os.path.exists(d):
        for f in os.listdir(d):
            if f.endswith(".mp3"):
                files.append(os.path.join(d, f))
files.sort()

# --- Création dossier backups ---
os.makedirs(BACKUP_DIR, exist_ok=True)

# --- Génération du XML ---
rss = []
rss.append('<?xml version="1.0" encoding="UTF-8"?>')
rss.append('<rss xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd" version="2.0">')
rss.append("<channel>")
rss.append("<title>Rendez-vous avec Mr X</title>")
rss.append("<link>https://archive.org/details/rendezvous-avec-mr-x</link>")
rss.append("<description>Podcast complet de Rendez-vous avec Mr X</description>")
rss.append("<language>fr-FR</language>")
rss.append("<copyright>© 2025 MrX Podcast</copyright>")
rss.append(f"<itunes:author>{AUTHOR}</itunes:author>")
rss.append("<itunes:summary>Tous les épisodes de Rendez-vous avec Mr X, émission culte de France Inter (1997–2015).</itunes:summary>")
rss.append("<itunes:explicit>no</itunes:explicit>")
rss.append("<itunes:subtitle>Rendez-vous avec Mr X</itunes:subtitle>")
rss.append("<itunes:type>episodic</itunes:type>")
rss.append(f"<itunes:owner><itunes:name>{OWNER_NAME}</itunes:name><itunes:email>{OWNER_EMAIL}</itunes:email></itunes:owner>")
rss.append(f'<itunes:image href="{COVER_URL}"/>')
rss.append('<itunes:category text="History"/>')
rss.append(time.strftime("<lastBuildDate>%a, %d %b %Y %H:%M:%S GMT</lastBuildDate>", time.gmtime()))

# --- Ajout des items ---
for f in files:
    basename = os.path.basename(f)
    title = basename.replace(".mp3", "").replace("_", " ")
    url = f"https://archive.org/download/rendezvous-avec-mr-x/{basename}"
    size = os.path.getsize(f)
    pubdate = time.strftime("%a, %d %b %Y %H:%M:%S GMT", time.gmtime(os.path.getmtime(f)))
    duration = get_duration(f)

    rss.append("  <item>")
    rss.append(f"    <title>{title}</title>")
    rss.append(f"    <link>{url}</link>")
    rss.append(f"    <description>{title} — épisode de Rendez-vous avec Mr X.</description>")
    rss.append(f'    <enclosure url="{url}" length="{size}" type="audio/mpeg"/>')
    rss.append(f"    <guid>{url}</guid>")
    rss.append(f"    <pubDate>{pubdate}</pubDate>")
    rss.append(f"    <itunes:author>{AUTHOR}</itunes:author>")
    rss.append("    <itunes:explicit>no</itunes:explicit>")
    rss.append(f"    <itunes:summary>{title}</itunes:summary>")
    rss.append(f"    <itunes:duration>{duration}</itunes:duration>")
    rss.append("  </item>")

rss.append("</channel>")
rss.append("</rss>")

# --- Sauvegarde ---
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write("\n".join(rss))

backup_name = os.path.join(BACKUP_DIR, f"feed_{time.strftime('%Y%m%d_%H%M%S')}.xml")
with open(backup_name, "w", encoding="utf-8") as f:
    f.write("\n".join(rss))

print(f"✅ {len(files)} fichiers audio trouvés")
print(f"🚀 Flux RSS généré : {os.path.abspath(OUTPUT_FILE)}")
print(f"💾 Backup créé : {backup_name}")

