#!/bin/python3

import requests
import argparse
import os
from concurrent.futures import ThreadPoolExecutor

headers = {"Content-Type": "application/json"}
data = {"streamCtag": None}

def main():
    parser = argparse.ArgumentParser(description="Download iCloud shared album photos.")
    parser.add_argument("-url", "-u", required=True, help="The URL of the iCloud shared album.")
    args = parser.parse_args()

    url = args.url
    album_id = url.split("#")[-1]
    api_url = f"https://p153-sharedstreams.icloud.com/{album_id}/sharedstreams"
    print(f"[+] Album ID: {album_id}")
    stream_resp = requests.post(f"{api_url}/webstream", headers=headers, json=data)
    #print(stream_resp.text) 
    stream_data = stream_resp.json()

    photos = stream_data.get("photos", [])
    if not photos:
        print("[-] No photos found in the album.")
        exit(1)
        return
    checksums = []
    photo_guids = []
    for photo in photos:
        derivatives = photo.get("derivatives", {})
        if not derivatives:
            continue
        largest = max(derivatives.values(), key=lambda d: int(d.get("fileSize", 0)))
        checksum = largest.get("checksum")
        if checksum:
            checksums.append(checksum)
        photo_guid = photo.get("photoGuid")
        if photo_guid:
            photo_guids.append(photo_guid)

    if not photo_guids:
        print("[-] No valid photo GUIDs found.")
        return

    # Fetch asset URLs
    asset_urls_resp = requests.post(
        f"{api_url}/webasseturls",
        headers=headers,
        json={"photoGuids": photo_guids}
    )
    asset_urls_data = asset_urls_resp.json()
    items = asset_urls_data.get("items", {})

    download_list = []
    for key, value in items.items():
        url_path = value.get("url_path", "")
        url_location = value.get("url_location", "")
        full_url = f"https://{url_location}{url_path}&{key}"

        if "." in url_path:
            ext = url_path.split("?")[0].split(".")[-1]
            ext = ext.lower()
        else:
            ext = ""  # fallback extension if none found

        for checksum in checksums:
            if checksum in full_url:
                download_list.append((full_url, checksum, ext))
                break 

    print(f"[+] Found {len(download_list)} downloadable items.")
    os.makedirs("downloads", exist_ok=True)
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [
            executor.submit(download_file, url, checksum, ext)
            for url, checksum, ext in download_list
        ]
        for future in futures:
            try:
                future.result()
            except Exception as e:
                print(f"[!] Error downloading file: {e}")

def download_file(url, checksum, ext):
    response = requests.get(url, stream=True)
    response.raise_for_status()
    filename = os.path.join("downloads", f"{checksum}.{ext}")

    with open(filename, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)

    print(f"[+] Downloaded: {filename}")

if __name__ == "__main__":
    main()
