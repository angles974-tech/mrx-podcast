#!/usr/bin/env python3
import os
import datetime

# --- CONFIGURATION ---
BASE_DIR = "/Users/xavierangle/mr-x-podcast"
AUDIO_DIRS = [
    os.path.join(BASE_DIR, "MrX_normalized"),
    os.path.join(BASE_DIR, "MrX_downloads"),
]

BACKUP_DIR = os.path.join(BASE_DIR, "backups")
OUTPUT_FILE = os.path.join(BASE_DIR, "mr_x.xml")
ARCHIVE_URL = "https://archive.org/download/rendezvous-avec-mr-x/"

# Jaquette hébergée sur GitHub Pages
COVER_URL = "https://angles974-tech.github.io/mr-x-podcast/assets/mr_x_cover.jpg"

# --- CREATION DOSSIER BACKUP ---
os.makedirs(BACKUP_DIR, exist_ok=True)

# --- RECUPERATION DES MP3 ---
files = []
for d in AUDIO_DIRS:
    if os.path.exists(d):
        files.extend([os.path.join(d, f) for f in os.listdir(d) if f.endswith(".mp3")])

files.sort()
print(f"✅ {len(files)} fichiers audio trouvés pour génération RSS")

# --- GENERATION RSS ---
rss_header = f'''<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0"
     xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd"
     xmlns:atom="http://www.w3.org/2005/Atom">

  <channel>
    <title>Rendez-vous avec Mr X</title>
    <link>https://archive.org/details/rendezvous-avec-mr-x</link>
    <language>fr</language>
    <copyright>© France Inter / Diffusion à but non lucratif</copyright>
    <atom:link href="https://angles974-tech.github.io/mr-x-podcast/mr_x.xml"
               rel="self" type="application/rss+xml"/>

    <itunes:author>Rendez-vous avec Mr X</itunes:author>
    <itunes:subtitle>Un podcast culte de France Inter (1997–2015).</itunes:subtitle>
    <itunes:summary>Rendez-vous avec Mr X, émission mythique animée par Patrick Pesnot sur France Inter. 
Redécouvrez les enquêtes, mystères et grandes affaires qui ont marqué l’histoire.</itunes:summary>
    <itunes:explicit>no</itunes:explicit>
    <itunes:category text="History"/>
    <itunes:image href="{COVER_URL}"/>
    <lastBuildDate>{datetime.datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")}</lastBuildDate>
'''

rss_items = ""
for path in files:
    fname = os.path.basename(path)
    title = os.path.splitext(fname)[0].replace("_", " ")
    url = ARCHIVE_URL + fname
    length = os.path.getsize(path) if os.path.exists(path) else 0

    rss_items += f'''
    <item>
      <title>{title}</title>
      <link>https://archive.org/details/rendezvous-avec-mr-x</link>
      <itunes:subtitle>{title}</itunes:subtitle>
      <itunes:summary>{title} — épisode de Rendez-vous avec Mr X.</itunes:summary>
      <enclosure url="{url}" type="audio/mpeg" length="{length}"/>
      <guid>{url}</guid>
      <pubDate>{datetime.datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")}</pubDate>
      <itunes:explicit>no</itunes:explicit>
    </item>
    '''

rss_footer = '''
  </channel>
</rss>
'''

xml_string = rss_header + rss_items + rss_footer

# --- SAUVEGARDE EN UTF-8 ---
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write(xml_string)

backup_name = os.path.join(
    BACKUP_DIR, f"mr_x_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.xml"
)
with open(backup_name, "w", encoding="utf-8") as f:
    f.write(xml_string)

print(f"🚀 Flux RSS généré : {OUTPUT_FILE}")
print(f"💾 Backup créé : {backup_name}")

