# Scripts
this repo contains script that i wrote and use on daily basis hope they help you sometime :)

### Icloud_shared_albums_downloader.py
A command-line tool to download all photos from an iCloud shared album coz apple share sucks :)

**Usage:**
```sh
python3 Icloud_shared_albums_downloader.py -u <iCloud_shared_album_url>
```

### Rename.py
renames every file in pwd 1...n with thier extensions eg 0001.jpg,0002.mp4,0003.heic,etc

**Usage:**
```sh
python3 rename.py
```

### ip.sh
returns json for ip address for adapters (if tun exists it will return tun ip) 

**Usage:**
```sh
bash ip.sh
```
### discordupdate.sh
updates the version of discord in the specified file so that i dont have to convert .deb to .zst every time i update discord

**Usage:**
```sh
sudo ./discordupdate.sh
```
---
#### the script may or may not require venv but here the step to create one

```sh
python3 -m venv venv && source venv/bin/activate
```