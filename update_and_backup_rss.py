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

# Email Apple Podcasts (⚠️ à remplacer par ton vrai email)
OWNER_NAME = "MrX"
OWNER_EMAIL = "ton.email@exemple.com"

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
<rss xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd" version="2.0"
     xmlns:atom="http://www.w3.org/2005/Atom">

  <channel>
    <title>Rendez-vous avec Mr X</title>
    <link>https://archive.org/details/rendezvous-avec-mr-x</link>
    <language>fr-FR</language>
    <copyright>© 2025 MrX Podcast</copyright>
    <atom:link href="https://angles974-tech.github.io/mr-x-podcast/mr_x.xml"
               rel="self" type="application/rss+xml"/>

    <itunes:author>MrX</itunes:author>
    <itunes:summary>Un podcast unique avec 700+ épisodes archivés.</itunes:summary>
    <itunes:explicit>no</itunes:explicit>
    <itunes:subtitle>Rendez-vous avec MrX</itunes:subtitle>
    <itunes:type>episodic</itunes:type>
    <itunes:owner>
        <itunes:name>{OWNER_NAME}</itunes:name>
        <itunes:email>{OWNER_EMAIL}</itunes:email>
    </itunes:owner>
    <itunes:image href="{COVER_URL}"/>
    <itunes:category text="Society & Culture"/>
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
      <description>{title} — épisode de Rendez-vous avec Mr X.</description>
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

