# HB Industry Group - Site Web & Showroom Virtuel

Site web interactif haute performance pour **HB Industry Group**, intégrant une animation 3D immersive au défilement (scroll animation) à 60 FPS basée sur Nuxt.js et un Web Worker de rendu Canvas.

---

## 🚀 Fonctionnalités Clés

- **Animation au Scroll 60 FPS :** Défilement fluide synchronisé sur une séquence de 410 images WebP haute définition (1920x1080 Desktop / 960x540 Mobile).
- **Web Worker Dédié :** Chargement asynchrone et décodage multithreadé des images (`video-sequence.worker-B5BJOqje.js`).
- **Showroom Industriel & Laboratoire :** Présentation immersive des équipements de pointe HBIG (Sorbonnes de laboratoire, paillasses techniques, douches de sécurité, unités de stockage).
- **Architecture Statique Déployable :** Prêt pour hébergement sur GitHub Pages, Vercel, Netlify ou serveur Nginx/Apache.

---

## 🛠️ Lancement Local

Pour tester le site en local :

```bash
# 1. Démarrer le serveur HTTP local
python -m http.server 8080

# 2. Ouvrir le navigateur
http://localhost:8080/
```

> **Astuce :** Utilisez **Ctrl + F5** pour forcer le rechargement et rafraîchir le cache des frames d'animation.

---

## 🎬 Mise à Jour de la Vidéo d'Animation

Pour intégrer une nouvelle vidéo de scroll :

1. Placer votre fichier vidéo MP4 à la racine sous le nom `user_new_video.mp4`.
2. Exécuter le script d'échantillonnage automatique :
   ```bash
   python convert_new_video_to_frames.py
   ```
3. Le script génère automatiquement les 410 images Desktop (`static/frames/home/desktop/webp/`) et Mobile (`static/frames/home/mobile/webp/`) avec interpolation et compression WebP optimisée.

---

## 📁 Structure du Projet

```text
├── _nuxt/                                # Bundles JavaScript & CSS Nuxt compilés
├── static/
│   └── frames/home/
│       ├── desktop/webp/                 # Séquence d'images Desktop (1920x1080)
│       └── mobile/webp/                  # Séquence d'images Mobile (960x540)
├── fiches_produits_commerciales/         # Documentation & fiches techniques
├── user_new_video.mp4                    # Vidéo source Full HD
├── convert_new_video_to_frames.py        # Script d'extraction multithread
├── index.html                            # Page d'accueil principale
└── README.md
```

---

© 2026 HB Industry Group. Tous droits réservés.
