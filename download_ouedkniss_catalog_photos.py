import os
import sys
import json
import time
import urllib.request
from PIL import Image

sys.stdout.reconfigure(encoding='utf-8')

catalog_data = {
    "paillasse_scolaire_eleve": {
        "id": "44297578",
        "title": "Paillasse scolaire pour élève / Table de classe scientifique",
        "category": "Mobilier scolaire et universitaire de laboratoire",
        "hashes": [
            "j7xxeOrUbcPtBiHIESb1Jz1LN6wJdRr1Ktxr5S27.jpg",
            "uBctXy0rsT5asolhTYrm0itzUe32YPIICFBrLSiV.jpg",
            "EC7mm5WCimxTvMH2KzvunHzWFEmI1YBj5957P4x1.jpg",
            "rbyyCcRo5GGtc2m05r8e4AIj57G8yGFk45kTMtDM.jpg",
            "asqhKKLKMl5scw7J8F7AtrHNB4mrsZwpuTVueOMG.jpg",
            "9k0Apd2iqcYDDmm3zvHKiLZbNKoHSwRcGxM3HsRp.jpg",
            "f2Ok1Cy5HkjRVyBGGkrBUnCYwwQmKGVlOeTxh5xD.jpg",
            "NzYu4I3KUoHzTvlc4VO1gtNBy0S1BIuJSOxM4l29.jpg"
        ]
    },
    "paillasse_scolaire_table_scientifique": {
        "id": "38711646",
        "title": "Paillasse scolaire / Table scientifique avec évier & robinetterie",
        "category": "Laboratoire scolaire, lycée, collège & université",
        "hashes": [
            "7ofNHzx1KfEOuDdzQk0rOt9wq6ZGqFGPI97LpZUa.jpg",
            "6WUrzh9808JJ8rpl5FrOhIopACMA0NLUHoJVtlMo.jpg",
            "qhK2DRGd0Jy5NJ177a2gGTn0SgzcVH1uqgrwclSJ.jpg",
            "v093aihAd2mwNsQYsEysnqvGwpzfqPO3AE2V5RJv.jpg",
            "Ge3acqo7xcM4L1NPCQyjpmuadJTAb3i7XpIvupsv.jpg",
            "gLSrEECyBDyv9HCH1YfficDrehQzehcQABi87nrd.jpg",
            "Gdoloogybv5SWr87PhI7PVOhxTT5y4SqDUbhBRp5.jpg",
            "HNGcv16cooG0sKxzm1mrN2XFZq4RL2ulDeMjIHvP.jpg",
            "O7Yp8dz6pk6bJclbwpIr9uiHAEO4Y1P8dZJZ4O15.jpg",
            "MTGNzvfPu2PpqSEKs7DInXHVeibMwGwJcKmEuBf5.jpg",
            "56Tbz3lb0UbG6BQO580o3IhWOt8UmW9fEtMq61FP.jpg",
            "drWthhG04pWjDs3Z85Kgifasjg744ewqjQRY6fvw.jpg"
        ]
    },
    "paillasse_laboratoire_bureautique": {
        "id": "45694867",
        "title": "Paillasse de laboratoire et bureautique technique sur mesure",
        "category": "Mobilier technique et paillasse informatique/bureautique",
        "hashes": [
            "tX2aot0bAvtqe5saYhNlPFXzu3AsqhdZAMVn5uNA.jpg",
            "iMewA4seooXrQfBasPrGHqCjZ6m7e4D4LJ2QAX0O.jpg",
            "5D2QEj4pXNp0yRf2qqUJwWiVBTK1FBy1f9p8ys05.jpg",
            "BnZ3MLEwtEqnl7Fkr1SOoZUIxDdSSR1FmQJYVzqd.jpg",
            "bFaj3xh485jmCQ3n7VH446oPROLTPJq9Rd6y6jvM.jpg",
            "HlScSgF0i9ROqA5W2DeASfHzRR9e2BuDHkudVPxt.jpg",
            "rgzFCCquWPmipet98vOjzHjcpIbVIp8ZXfY6V3SA.jpg",
            "lm0YUA3e5tyXEhfl00FqORjEoOfDd67bijMeCwU3.jpg",
            "pqVymT7fFtYAfmcTWDMImwDWwooCpus3WPwjBb2R.jpg",
            "KytcAmLJO02zjPZgTNWcALXa3V0AF7MTy6QtBRJ6.jpg",
            "yJTMcs83g3FwjpmfwLoOy5EJWVhW19s5xKljy3wN.jpg",
            "gB75I1gUfkW8fGu6O0NdAmSj4Mm7QWwCYgBHjqdk.jpg"
        ]
    },
    "paillasse_laboratoire_centrale_murale": {
        "id": "41275177",
        "title": "Paillasse de laboratoire centrale & murale professionnelle",
        "category": "Paillasses pour laboratoires d'analyse, contrôle qualité & R&D",
        "hashes": [
            "GPOUitknSrJJXFN31GPnmjL1k9eryJnSq53M2duP.jpg",
            "8fHerYuEbPF4c9T9Gf0HAtEitXm11tZKzeDhUc8z.jpg",
            "pvrJc0lVYEBaDpsD52FId9ogADO9CRX2TARc3apO.jpg",
            "vbGlvi45jLs1ZQ9XahsHeE3iQOL2XbjVxaiQEvpX.jpg",
            "4KONq7oyTCLZ6xXFoCXrApcG42FI30uqATklrNuG.jpg",
            "2CyEgMQ9Krien1k0ZTkHWC1zi801s1GNuCR3FuSG.jpg",
            "LZLA3xm9IXRXD9DBMiO2Bqd1lDdUfP6luiDreeOG.jpg",
            "NVzT4sbbDBMrv2PEpdnIzGD1votph95TM8RuPK9D.jpg",
            "HWVLD6wAyBw4idboqAlSj7Qn8IzhICLFzQ6G1IEF.jpg"
        ]
    },
    "armoire_securite_coupe_feu": {
        "id": "38700804",
        "title": "Armoire de sécurité coupe-feu pour produits inflammables",
        "category": "Sécurité et stockage produits dangereux & solvants",
        "hashes": [
            "OIhITHXG5sQOJoTtQAHHQ8e9n3giSsfjIE2CGoTQ.jpg",
            "bWTkaJdOapHO0tqRBNIGnevRVFhgARCcJ1DqIPao.jpg",
            "InbglCMdun30ITQeuMsxjlRYzc7nOBioHVxzy1g0.jpg",
            "Ti3rbE5l0gxnjpovmJi4znWKlyW5R8sTSiEWI2y7.jpg",
            "PC1gO4ItBzrAMFtq7gr0shuZyID3JTKp8Of91ION.jpg"
        ]
    },
    "armoire_ventilee_produits_chimiques": {
        "id": "38711544",
        "title": "Armoire ventilée / armoire de stockage produits chimiques & corrosifs",
        "category": "Armoires ventilées, acides, bases et toxiques",
        "hashes": [
            "y345mUcQBtm33SuEew2ytKPYDAxbwCZNOZkrRXUv.jpg",
            "xKBvATNhP0jrSP2UVctcgd13JV1m1yW3VzJm9MVf.jpg",
            "62wgHQHHaq0bM1odH3yVw64oDRrcCeatFU1sFFWp.jpg",
            "1ffoop9LwdBcbPXSmpw9wHbB0gP79NtHz7pjB1dO.jpg",
            "1EXDPrTcvANa3HLHpOU6uiRdJaVtapN8c9ebu3bf.jpg",
            "HfaNnuzAW9GYiYwueEt79SKW0BiV5NaSvXZkdOGp.jpg",
            "ec4t3eTDJFv985ACn8UCQR0fDaZfaNeK7UaWgiWx.jpg",
            "aSXaywYKXjkcfKUi4vbqUrSwf9AyJEUxIZVC2AUA.jpg",
            "Cbonz5LJz0dxjknyK1VsAuC0x49LUk6tnipxewzE.jpg",
            "u3EC5BFmLxpLU3ALTQgOvVcREicQpb6rtqdf7Cqh.jpg"
        ]
    }
}

os.makedirs('assets/products', exist_ok=True)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
}

def try_download_image(img_hash, target_path):
    cdns = ['cdn.ouedkniss.com', 'cdn7.ouedkniss.com', 'cdn8.ouedkniss.com', 'cdn9.ouedkniss.com']
    sizes = ['1600', '800', '400', '']
    
    for size in sizes:
        for cdn in cdns:
            if size:
                url = f"https://{cdn}/{size}/medias/announcements/images/0gMPZX/{img_hash}"
            else:
                url = f"https://{cdn}/medias/announcements/images/0gMPZX/{img_hash}"
            
            try:
                req = urllib.request.Request(url, headers=headers)
                with urllib.request.urlopen(req, timeout=5) as resp:
                    data = resp.read()
                    if len(data) > 1000:
                        with open(target_path, 'wb') as f:
                            f.write(data)
                        return url, len(data)
            except Exception:
                continue
    return None, 0

print("Downloading full HD product photos...")
download_summary = {}

for prod_key, prod_info in catalog_data.items():
    print(f"\nProcessing {prod_key} ({len(prod_info['hashes'])} photos)...")
    download_summary[prod_key] = []
    
    for idx, h in enumerate(prod_info['hashes']):
        dest_filename = f"{prod_key}_{idx+1:02d}.jpg"
        dest_path = os.path.join('assets/products', dest_filename)
        
        # If already downloaded and valid, check
        if os.path.exists(dest_path) and os.path.getsize(dest_path) > 10000:
            im = Image.open(dest_path)
            download_summary[prod_key].append({
                'file': dest_filename,
                'resolution': f"{im.size[0]}x{im.size[1]}",
                'size_kb': os.path.getsize(dest_path) // 1024
            })
            print(f"  [Existing] {dest_filename} ({im.size[0]}x{im.size[1]})")
            continue
            
        success_url, size_bytes = try_download_image(h, dest_path)
        if success_url:
            im = Image.open(dest_path)
            download_summary[prod_key].append({
                'file': dest_filename,
                'resolution': f"{im.size[0]}x{im.size[1]}",
                'size_kb': size_bytes // 1024,
                'source_url': success_url
            })
            print(f"  [Downloaded] {dest_filename} ({im.size[0]}x{im.size[1]}, {size_bytes//1024} KB)")
        else:
            print(f"  [Failed] hash {h}")

with open('catalog_images_summary.json', 'w', encoding='utf-8') as f:
    json.dump(download_summary, f, indent=2)

print("\nDone downloading catalog images!")
