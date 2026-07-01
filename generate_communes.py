import re
import unicodedata
from pathlib import Path
from urllib.request import urlopen
from html import unescape

ROOT = Path(__file__).resolve().parent
OUT_DIR = ROOT / 'communes'
OUT_DIR.mkdir(exist_ok=True)

URL = 'https://fr.wikipedia.org/wiki/Liste_des_communes_d%27Ille-et-Vilaine'


def slugify(text: str) -> str:
    text = unescape(text).strip()
    text = unicodedata.normalize('NFKD', text)
    text = text.encode('ascii', 'ignore').decode('ascii')
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    text = re.sub(r'-+', '-', text).strip('-')
    return text or 'commune'


def clean_name(raw: str) -> str:
    name = unescape(raw).strip()
    name = re.sub(r'<[^>]+>', '', name)
    name = name.replace('&nbsp;', ' ')
    name = name.replace('&#160;', ' ')
    name = re.sub(r'\s+', ' ', name)
    name = name.replace('  ', ' ').strip()
    name = re.sub(r'\s*\(.*?\)\s*$', '', name)
    if name.lower().startswith('modifier') or name.lower().startswith('voir'):
        return ''
    if name.startswith('|'):
        return ''
    return name.strip()


html = urlopen(URL, timeout=30).read().decode('utf-8', errors='ignore')
raw_matches = re.findall(r'\|\s*([^|]+?)\s*\|\s*\d{5}\s*\|', html)

names = []
for item in raw_matches:
    cleaned = clean_name(item)
    if not cleaned:
        continue
    if cleaned.lower() in {'modifier les données', 'modifier', 'commune', 'communes'}:
        continue
    if cleaned not in names:
        names.append(cleaned)

# Keep the communes list and remove obvious non-commune rows
filtered = []
for name in names:
    if 'modifier' in name.lower() or 'voir aussi' in name.lower():
        continue
    if re.fullmatch(r'[^A-Za-zÀ-ÿ\- ]+', name):
        continue
    if name.startswith('Rennes') and len(filtered) == 0:
        filtered.append(name)
        continue
    if name.lower().startswith('liste'):
        continue
    filtered.append(name)

# Deduplicate again and keep the 332 commune entries from the source page.
final_names = []
for name in filtered:
    if name and name not in final_names:
        final_names.append(name)

final_names = final_names[:332]

if len(final_names) < 300:
    raise RuntimeError(f'Only {len(final_names)} communes extracted; expected at least 300')

print(f'Extracted {len(final_names)} communes from Wikipedia')

base_template = '''<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Peintre à {name} | Zindeco Peinture</title>
  <meta name="description" content="Artisan peintre à {name} pour la peinture intérieure, extérieure et rénovation. Devis gratuit dans toute la commune de {name} et autour du 35." />
  <link rel="stylesheet" href="../style.css" />
</head>
<body>
  <header>
    <div class="container">
      <a href="../index.html" class="logo">
        <span class="logo-icon"><i class="fas fa-paint-roller"></i></span>
        <div><h1>ZINDECO</h1><p>PEINTURE</p></div>
      </a>
      <nav class="nav-links">
        <ul>
          <li><a href="../index.html">Accueil</a></li>
          <li><a href="../peinture-interieur.html">Peinture intérieure</a></li>
          <li><a href="../peinture-exterieur.html">Peinture extérieure</a></li>
          <li><a href="../renovation.html">Rénovation</a></li>
          <li><a href="../index.html#contact">Contact</a></li>
        </ul>
      </nav>
    </div>
  </header>
  <section class="hero page-hero" style="background:linear-gradient(rgba(5,20,40,.72),rgba(5,20,40,.72)),url('https://images.unsplash.com/photo-1504307651254-35680f356dfd?auto=format&fit=crop&w=1600&q=80') center/cover;">
    <div class="container hero-container">
      <div class="hero-left">
        <span class="section-subtitle">{name}</span>
        <h2>Peintre professionnel à {name}</h2>
        <p>Entreprise de peinture à {name} pour les maisons, appartements, façades et chantiers de rénovation. Devis gratuit et intervention rapide dans le département 35.</p>
        <div class="hero-buttons">
          <a href="tel:0766718175" class="btn-primary">Nous appeler</a>
          <a href="../index.html#contact" class="btn-dark">Demander un devis</a>
        </div>
      </div>
    </div>
  </section>
  <section class="about">
    <div class="container about-grid">
      <div class="about-content">
        <span class="section-subtitle">Peinture à {name}</span>
        <h2>Peinture intérieure, extérieure et rénovation à {name}</h2>
        <p>Nous intervenons à {name} avec un service de proximité, une préparation soignée du support et des finitions propres. Nous accompagnons les particuliers et les professionnels sur leurs projets de peinture et de rénovation.</p>
        <ul class="check-list">
          <li><i class="fas fa-check-circle"></i> Peinture intérieure : murs, plafonds, cuisines, salles de bain</li>
          <li><i class="fas fa-check-circle"></i> Peinture extérieure : façades, volets, portails, clôtures</li>
          <li><i class="fas fa-check-circle"></i> Rénovation : rebouchage, ponçage et finitions</li>
        </ul>
      </div>
      <div class="about-image">
        <img src="https://images.unsplash.com/photo-1484154218962-a197022b5858?auto=format&fit=crop&w=1000&q=80" alt="Peinture à {name}" />
      </div>
    </div>
  </section>
  <section class="services">
    <div class="container">
      <div class="section-title">
        <span>Nos prestations</span>
        <h2>Un artisan peintre à {name} et dans tout le 35</h2>
      </div>
      <div class="services-grid">
        <div class="service-card"><div class="icon"><i class="fas fa-paint-roller"></i></div><h3>Peinture intérieure</h3><p>Interventions rapides pour appartements, maisons et locaux professionnels.</p></div>
        <div class="service-card"><div class="icon"><i class="fas fa-house"></i></div><h3>Peinture extérieure</h3><p>Façades, murs extérieurs, volets, portails et clôtures.</p></div>
        <div class="service-card"><div class="icon"><i class="fas fa-hammer"></i></div><h3>Rénovation</h3><p>Préparation du support, rebouchage et finitions de qualité.</p></div>
      </div>
    </div>
  </section>
  <section class="contact" id="contact">
    <div class="container">
      <div class="section-title">
        <span>Contact</span>
        <h2>Demandez votre devis gratuit à {name}</h2>
      </div>
      <div class="contact-grid">
        <div class="contact-info">
          <div class="contact-card"><i class="fas fa-phone-alt"></i><h3>Téléphone</h3><a href="tel:0766718175">07 66 71 81 75</a></div>
          <div class="contact-card"><i class="fas fa-map-marker-alt"></i><h3>Zone d’intervention</h3><p>{name}, Rennes, Saint-Malo, Vitré, Redon et tout le département 35.</p></div>
        </div>
        <div class="contact-form">
          <form action="../contact.php" method="POST">
            <input type="text" name="nom" placeholder="Votre nom" required />
            <input type="tel" name="telephone" placeholder="Votre téléphone" required />
            <input type="email" name="email" placeholder="Votre e-mail" required />
            <input type="text" name="ville" value="{name}" />
            <select name="service"><option>Peinture intérieure</option><option>Peinture extérieure</option><option>Rénovation</option></select>
            <textarea name="message" rows="6" placeholder="Décrivez votre projet..." required></textarea>
            <button type="submit"><i class="fas fa-paper-plane"></i>Envoyer ma demande</button>
          </form>
        </div>
      </div>
    </div>
  </section>
  <footer class="footer">
    <div class="container">
      <div class="footer-grid">
        <div class="footer-col">
          <h3>ZINDECO PEINTURE</h3>
          <p>Artisan peintre dans le 35 pour les projets de peinture intérieure, extérieure et rénovation.</p>
          <a href="tel:0766718175" class="footer-phone">📞 07 66 71 81 75</a>
        </div>
        <div class="footer-col">
          <h3>Navigation</h3>
          <ul>
            <li><a href="../index.html">Accueil</a></li>
            <li><a href="index.html">Toutes les communes</a></li>
            <li><a href="../peinture-interieur.html">Peinture intérieure</a></li>
            <li><a href="../peinture-exterieur.html">Peinture extérieure</a></li>
          </ul>
        </div>
      </div>
    </div>
  </footer>
  <script src="../script.js"></script>
</body>
</html>
'''

for name in final_names:
    slug = slugify(name)
    path = OUT_DIR / f'{slug}.html'
    content = base_template.format(name=name)
    path.write_text(content, encoding='utf-8')

# Index page listing the generated communes
list_html = '''<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Toutes les communes du 35 | Zindeco Peinture</title>
  <meta name="description" content="Découvrez toutes les communes du département 35 pour lesquelles Zindeco propose des services de peinture et rénovation. Devis gratuit." />
  <link rel="stylesheet" href="../style.css" />
</head>
<body>
  <header>
    <div class="container">
      <a href="../index.html" class="logo">
        <span class="logo-icon"><i class="fas fa-paint-roller"></i></span>
        <div><h1>ZINDECO</h1><p>PEINTURE</p></div>
      </a>
      <nav class="nav-links">
        <ul>
          <li><a href="../index.html">Accueil</a></li>
          <li><a href="../peinture-interieur.html">Peinture intérieure</a></li>
          <li><a href="../peinture-exterieur.html">Peinture extérieure</a></li>
          <li><a href="../renovation.html">Rénovation</a></li>
        </ul>
      </nav>
    </div>
  </header>
  <section class="hero page-hero" style="background:linear-gradient(rgba(5,20,40,.72),rgba(5,20,40,.72)),url('https://images.unsplash.com/photo-1460317442991-0ec209397118?auto=format&fit=crop&w=1600&q=80') center/cover;">
    <div class="container hero-container">
      <div class="hero-left">
        <span class="section-subtitle">Département 35</span>
        <h2>Toutes les communes du 35</h2>
        <p>Découvrez notre couverture SEO locale sur l’ensemble du département d’Ille-et-Vilaine avec des pages dédiées à chaque commune.</p>
        <div class="hero-buttons">
          <a href="../index.html#contact" class="btn-primary">Demander un devis</a>
          <a href="tel:0766718175" class="btn-dark">Nous appeler</a>
        </div>
      </div>
    </div>
  </section>
  <section class="about">
    <div class="container">
      <div class="section-title">
        <span>Couverture locale</span>
        <h2>Des pages dédiées pour chaque commune du 35</h2>
      </div>
      <div class="services-grid" style="grid-template-columns:repeat(auto-fit,minmax(240px,1fr));">
'''

for name in final_names:
    slug = slugify(name)
    list_html += f'        <a class="service-card" href="{slug}.html" style="display:block;"><h3>{name}</h3><p>Peinture intérieure, extérieure et rénovation à {name}. Demander un devis gratuit.</p></a>\n'

list_html += '''      </div>
    </div>
  </section>
  <footer class="footer">
    <div class="container">
      <div class="footer-grid">
        <div class="footer-col">
          <h3>ZINDECO PEINTURE</h3>
          <p>Artisan peintre sur tout le département 35.</p>
          <a href="tel:0766718175" class="footer-phone">📞 07 66 71 81 75</a>
        </div>
        <div class="footer-col">
          <h3>Navigation</h3>
          <ul>
            <li><a href="../index.html">Accueil</a></li>
            <li><a href="../peinture-interieur.html">Peinture intérieure</a></li>
            <li><a href="../peinture-exterieur.html">Peinture extérieure</a></li>
          </ul>
        </div>
      </div>
    </div>
  </footer>
  <script src="../script.js"></script>
</body>
</html>
'''

(OUT_DIR / 'index.html').write_text(list_html, encoding='utf-8')

sitemap_path = ROOT / 'sitemap.xml'
sitemap_text = sitemap_path.read_text(encoding='utf-8')
if '</urlset>' not in sitemap_text:
    sitemap_text += '\n</urlset>'
if 'communes/index.html' not in sitemap_text:
    sitemap_text = sitemap_text.replace('</urlset>', '  <url>\n    <loc>https://zindeco-peinture-rennes.fr/communes/index.html</loc>\n    <priority>0.90</priority>\n    <changefreq>monthly</changefreq>\n  </url>\n</urlset>')
for name in final_names:
    slug = slugify(name)
    entry = f'  <url>\n    <loc>https://zindeco-peinture-rennes.fr/communes/{slug}.html</loc>\n    <priority>0.85</priority>\n    <changefreq>monthly</changefreq>\n  </url>\n'
    if f'/communes/{slug}.html' not in sitemap_text:
        sitemap_text = sitemap_text.replace('</urlset>', entry + '</urlset>')

sitemap_path.write_text(sitemap_text, encoding='utf-8')
print(f'Wrote {len(final_names)} commune pages to {OUT_DIR}')
