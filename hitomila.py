import requests
import json
import os
from bs4 import BeautifulSoup
import re

"""
    https://ltn.hitomi.la/common.js
    HitomiDownloader(galleryid)のオブジェクトつくって、
    hd.download_manga()呼び出すだけ
"""

number_of_frontends = 3
class HitomiDownloader:

    def __init__(self, gallery_id, save_dir="./hitomi/"):
        self.gallery_id   = gallery_id
        self.download_root_url = "https://{}hitomi.la/galleries/{}"
        self.save_dir = save_dir + "{}/"
        self.session_headers = {"Referer": "https://hitomi.la/reader/{gallery_id}.html"}
        self.title = self._get_manga_title()

    def _subdomain_from_galleryid(self):
        
        offset = int(str(self.gallery_id)[-1]) % number_of_frontends
        return chr(97 + offset) + "a."

    def _get_image_names(self):
        url = "https://ltn.hitomi.la/" + f"galleries/{self.gallery_id}.js"
        response = requests.get(url)
        response.raise_for_status()
        preText = response.text
        jsonText = preText[preText.find("["): preText.rfind("]") + 1]
        list_json = json.loads(jsonText)
        return [file_info["name"] for file_info in list_json]
    
    def _get_manga_title(self):
        url = f"https://hitomi.la/reader/{self.gallery_id}.html"
        r = requests.get(url)
        soup = BeautifulSoup(r.text, features="html.parser")
        title = str(soup.find("title"))
        return title[title.find(">") + 1:title.rfind(" |")]
    
    def _download_image(self, subdomain, filename):
        url = self.download_root_url.format(subdomain, f"{self.gallery_id}/"+filename)
        res = requests.get(url, headers=self.session_headers)
        path = self.save_dir.format(self.title) + filename
        with open(path, "wb") as f:
            f.write(res.content)

    def download_manga(self):
        subdomain = self._subdomain_from_galleryid()
        save_dir = self.save_dir.format(self.title)

        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        for filename in self._get_image_names():
            self._download_image(subdomain, filename)
