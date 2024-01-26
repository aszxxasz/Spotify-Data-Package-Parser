import zipfile
import os
import sys
import shutil
import json
import csv
import pandas as pd
from utilities import cprint, alert, success, info, warn

if os.path.exists("./temp"):
    warn("Removing old temp directory...")
    shutil.rmtree("./temp")

if len(sys.argv) < 2:
    info("Usage: python main.py <zip file>")
    exit(1)

zip_file = sys.argv[1]
if not os.path.exists(zip_file):
    alert("File not found!")
    exit(1)

info("Attempting to open zip file...")
try:
    zipFile = zipfile.ZipFile(zip_file)
except Exception as e:
    alert("Error opening zip file!")
    cprint("red", str(e))
    exit(1)

info("Attempting to extract zip file...")

try:
    if not os.path.exists("./temp"):
        os.mkdir("./temp")

    zipFile.extractall("./temp")
except Exception as e:
    alert("Error extracting zip file!")
    cprint("red", str(e))
    exit(1)

artists = {}
albums = {}
songs = {}

def process_data(data):
    for stream in data:
        artist = stream["master_metadata_album_artist_name"]
        album = stream["master_metadata_album_album_name"]
        song = stream["master_metadata_track_name"]

        if artist not in artists:
            artists[artist] = {"streams": 0, "hours": 0}

        artists[artist]["streams"] += 1
        artists[artist]["hours"] += stream["ms_played"] / 1000 / 60 / 60

        if album not in albums:
            albums[album] = {"streams": 0, "hours": 0}

        albums[album]["streams"] += 1
        albums[album]["hours"] += stream["ms_played"] / 1000 / 60 / 60

        if song not in songs:
            songs[song] = {"streams": 0, "hours": 0}

        songs[song]["streams"] += 1
        songs[song]["hours"] += stream["ms_played"] / 1000 / 60 / 60

def write_csv(file_name, data_dict, header):
    with open(file_name, "w", newline="", encoding='utf-8-sig') as f:
        writer = csv.writer(f, delimiter=",")
        writer.writerow(header)

        for key, values in data_dict.items():
            key_name = str(key).encode("utf-8", "replace").decode("utf-8", "replace")
            writer.writerow([key_name, values["streams"], values["hours"]])

for root, dirs, files in os.walk("./temp/Spotify Extended Streaming History"):
    for file in files:
        if file.endswith(".json"):
            file_path = os.path.join(root, file)
            info("Processing " + file_path + "...")
            
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                process_data(data)

if not os.path.exists("./output"):
    os.mkdir("./output")

if not os.path.exists("./output/csv"):
    os.mkdir("./output/csv")

if not os.path.exists("./output/html"):
    os.mkdir("./output/html")

write_csv("output/csv/artists.csv", artists, ["artist", "streams", "hours"])
write_csv("output/csv/albums.csv", albums, ["album", "streams", "hours"])
write_csv("output/csv/songs.csv", songs, ["song", "streams", "hours"])

for file in os.listdir("./output/csv"):
    if file.endswith(".csv"):
        df = pd.read_csv("./output/csv/" + file)
        df.to_html("./output/html/" + file.replace(".csv", ".html"), index=False)

write_csv("output/csv/artists_sorted.csv", dict(sorted(artists.items(), key=lambda x: x[1]["streams"], reverse=True)), ["artist", "streams", "hours"])
write_csv("output/csv/albums_sorted.csv", dict(sorted(albums.items(), key=lambda x: x[1]["streams"], reverse=True)), ["album", "streams", "hours"])
write_csv("output/csv/songs_sorted.csv", dict(sorted(songs.items(), key=lambda x: x[1]["streams"], reverse=True)), ["song", "streams", "hours"])

for file in os.listdir("./output/csv"):
    if file.endswith("_sorted.csv"):
        df = pd.read_csv("./output/csv/" + file)
        df.to_html("./output/html/" + file.replace("_sorted.csv", "_sorted.html"), index=False)

success("Data parsed successfully and written to output directory!")