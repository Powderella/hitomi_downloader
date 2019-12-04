# hitomi.la downloader

[hitomi.la](https://hitomi.la/)のダウンローダ.
HitomiDownloader(galleryid)のオブジェクトつくって,hd.download_manga()呼び出すだけ.

## example
```Python
import hitomila

if __name__ = "__main__":
    hd = hitomila.HitomiDownloader(galleryid)
    hd.dowload_manga()
```