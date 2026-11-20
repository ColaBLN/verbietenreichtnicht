"""Baut die Website verbietenreichtnicht.de als statische Seiten."""
import os, pathlib, html

S = pathlib.Path("/home/claude/site")
DOMAIN = "https://verbietenreichtnicht.de"

NAV = [("/", "Das Buch"), ("/material/", "Material"), ("/vortraege/", "Vorträge"),
       ("/ueber-mich/", "Über mich")]

CHECK = ('<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2.4" '
         'aria-hidden="true"><path d="M3 8.5l3 3 7-7"/></svg>')
HTACCESS = """# verbietenreichtnicht.de - Apache-Konfiguration
# Erzeugt von tools/build_site.py - nicht von Hand aendern.

AddDefaultCharset UTF-8
DirectoryIndex index.html
Options -Indexes

<IfModule mod_rewrite.c>
  RewriteEngine On

  # 1. Immer HTTPS. Beide Bedingungen zusammen verhindern eine Endlosschleife,
  #    falls TLS vor dem Webserver endet.
  RewriteCond %{HTTPS} !=on
  RewriteCond %{HTTP:X-Forwarded-Proto} !=https
  RewriteRule ^ https://%{HTTP_HOST}%{REQUEST_URI} [R=301,L]

  # 2. www auf die Hauptadresse umleiten.
  RewriteCond %{HTTP_HOST} ^www\\.(.+)$ [NC]
  RewriteRule ^ https://%1%{REQUEST_URI} [R=301,L]
</IfModule>

<IfModule mod_headers.c>
  Header always set X-Content-Type-Options "nosniff"
  Header always set Referrer-Policy "strict-origin-when-cross-origin"
  Header always set X-Frame-Options "SAMEORIGIN"
</IfModule>

<IfModule mod_expires.c>
  ExpiresActive On
  ExpiresDefault "access plus 1 hour"
  ExpiresByType text/html "access plus 0 seconds"
  ExpiresByType text/css "access plus 7 days"
  ExpiresByType image/jpeg "access plus 30 days"
  ExpiresByType image/png "access plus 30 days"
  ExpiresByType image/svg+xml "access plus 30 days"
  ExpiresByType application/pdf "access plus 7 days"
  ExpiresByType font/woff2 "access plus 1 year"
</IfModule>

# Schriften liegen unter einem festen Namen und aendern sich nie.
<FilesMatch "\\.woff2$">
  <IfModule mod_headers.c>
    Header set Cache-Control "public, max-age=31536000, immutable"
  </IfModule>
</FilesMatch>

<IfModule mod_deflate.c>
  AddOutputFilterByType DEFLATE text/html text/css text/plain
  AddOutputFilterByType DEFLATE application/xml image/svg+xml
</IfModule>
"""

PH = '<span class="ph">%s</span>'
MAIL = ('<a href="mailto:kontakt@verbietenreichtnicht.de">'
        'kontakt@verbietenreichtnicht.de</a>')
PREIS_TB = PH % "[0,00 €]"
PREIS_EB = "19,95 €"
# Kein Platzhalter-Markup: dieser Wert landet in einem href-Attribut.
AMAZON = "#"
AMAZON_EB = "https://www.amazon.de/dp/B0HSCFY8J3"
DATUM = PH % "[TT.MM.2026]"


def page(path, title, desc, body, depth, active, extra_head=""):
    up = "../" * depth
    links = "".join(
        f'<a href="{href}"{" aria-current=page" if href == active else ""}>{txt}</a>'
        for href, txt in NAV)
    doc = f"""<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{html.escape(desc, quote=True)}">
<link rel="canonical" href="{DOMAIN}{active if active != '/' else '/'}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Verbieten reicht nicht">
<meta property="og:locale" content="de_DE">
<meta property="og:title" content="{html.escape(title, quote=True)}">
<meta property="og:description" content="{html.escape(desc, quote=True)}">
<meta property="og:url" content="{DOMAIN}{active if active != '/' else '/'}">
<meta property="og:image" content="{DOMAIN}/assets/img/vorschau.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="stylesheet" href="{up}assets/css/site.css">
<link rel="preload" href="{up}assets/fonts/manrope-latin-800-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{up}assets/fonts/fraunces-latin-400-italic.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{up}assets/fonts/manrope-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>
{extra_head}</head>
<body>
<a class="skip" href="#inhalt">Zum Inhalt springen</a>
<div class="sheet">
  <nav class="main" aria-label="Hauptnavigation">
    <a class="brand" href="/"><span class="mark" aria-hidden="true"></span>/ Verbieten reicht nicht</a>
    <div class="links">{links}</div>
    <div class="nav-cta">
      <a class="btn btn-ghost" href="/#kaufen">Jetzt kaufen</a>
    </div>
  </nav>
<main id="inhalt">
{body}
</main>
  <footer class="main">
    <span>© 2026 Sebastian Klatt · Verbieten reicht nicht</span>
    <nav aria-label="Rechtliches">
      <a href="/material/">Material</a>
      <a href="/vortraege/">Vorträge</a>
      <a href="/impressum/">Impressum</a>
      <a href="/datenschutz/">Datenschutz</a>
    </nav>
  </footer>
</div>
</body>
</html>
"""
    out = S / path
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(doc, encoding="utf8")
    return out


# ---------------------------------------------------------------- Startseite
START = f"""
  <header class="hero" id="top">
    <div>
      <div class="badge">
        <div class="q" aria-hidden="true">&bdquo;</div>
        <div><b>Band 1 von Sebastian Klatt</b>
          <span>Erschienen am {DATUM} · <a href="#leseprobe">Leseprobe lesen</a></span></div>
      </div>
      <h1><span class="strike">Verbieten</span><br>reicht nicht</h1>
      <p class="subtitle">Handy weg – und dann?</p>
      <div class="lede">
        <p>„Nur noch fünf Minuten.“ Dann die Tränen, dann die Tür. Und hinterher die Frage,
        die bleibt: War das jetzt richtig?</p>
        <div class="meta">
          <span><b>200 Seiten</b> · Taschenbuch &amp; Kindle</span>
          <span aria-hidden="true">/</span>
          <span>Medienkompetenz in der Grundschule</span>
        </div>
      </div>
      <div class="hero-ctas">
        <a class="btn btn-dark" href="#kaufen">Buch bestellen <small>— bei Amazon</small></a>
        <a class="textlink" href="/material/">Kopiervorlagen gratis ↗</a>
      </div>
    </div>
    <div class="stage" aria-label="Buchcover und Eckdaten">
      <div class="block" aria-hidden="true"></div>
      <div class="book"><img src="assets/img/cover.jpg" width="560" height="784"
        alt="Buchcover: Verbieten reicht nicht – Handy weg, und dann?"></div>
      <div class="chip c1"><i>{CHECK}</i>Zwölf Projekte zum Nachmachen</div>
      <div class="chip c2"><i>{CHECK}</i>16 Bundesländer im Vergleich</div>
      <div class="glass stat">
        <div class="k">— Eigenes Smartphone</div>
        <div class="v">63&thinsp;%</div>
        <div class="d">der Zehn- bis Elf&shy;jährigen. Der Sprung passiert in der Grundschule.</div>
      </div>
      <div class="glass price">
        <div class="fmt">Taschenbuch · sofort lieferbar</div>
        <div class="p">{PREIS_TB}</div>
        <a class="btn btn-accent" href="#kaufen">Bei Amazon bestellen</a>
      </div>
    </div>
  </header>

  <div class="facts">
    <span class="lbl">Auf einen Blick</span>
    <span class="f">200 Seiten</span>
    <span class="f">17 Kapitel</span>
    <span class="f">12 Projekte</span>
    <span class="f">21 Grafiken</span>
    <span class="f">3 Kopiervorlagen</span>
  </div>

  <section class="s" id="buch">
    <div class="split">
      <div>
        <p class="eyebrow">Worum es geht</p>
        <h2>Handy weg ist schnell gesagt. Aber was kommt danach?</h2>
      </div>
      <div class="prose">
        <p class="big">Dieses Buch ist für Eltern und Lehrkräfte, die mehr wollen als Verbote –
        und die keine Zeit haben für Patentrezepte, die im Alltag nicht funktionieren.</p>
        <p>Es zeigt, was Kinder zwischen sechs und zehn Jahren wirklich mit Medien tun. Nicht,
        was wir vermuten. Es zeigt, was Handyverbote leisten und wo sie aufhören zu wirken –
        in Europa und in allen 16 Bundesländern. Und es zeigt, wie aus einem Verbot Begleitung
        wird: mit zwölf erprobten Projekten für Klassenzimmer und Küchentisch.</p>
        <p>Geschrieben hat es ein Vater, dessen Sohn gerade in genau diesem Alter ist, mit dem
        Blick eines Mediengestalters und dem Berliner Schulalltag als Prüfstein. Berlin ist dabei
        Beispiel, nicht Maßstab: Die Methoden und Projekte sind an kein Bundesland gebunden.</p>
      </div>
    </div>
    <div class="theses">
      <div class="thesis"><h3>Verbote schaffen Ruhe</h3><p>Sie sind sinnvoll, und sie geben
      Grundschulkindern Zeit. Aber sie erklären nicht, warum die Grenze gilt.</p></div>
      <div class="thesis"><h3>Wissen gibt Sicherheit</h3><p>Wer versteht, wie Medien funktionieren,
      entscheidet auf der Grundlage von Fakten – auch dann, wenn niemand hinschaut.</p></div>
      <div class="thesis"><h3>Begleitung statt Angst</h3><p>Kinder lernen den Umgang mit Medien
      nicht von allein. Sie lernen ihn an der Seite von Erwachsenen.</p></div>
    </div>
  </section>

  <section class="s" id="inhalt-buch">
    <div class="split">
      <div>
        <p class="eyebrow">Was Sie mitnehmen</p>
        <h2>Vier Fragen, auf die das Buch antwortet.</h2>
        <a class="btn btn-dark" href="#kaufen">Buch bestellen</a>
      </div>
      <ul class="learn">
        <li><span class="x">{CHECK}</span><div><b>Was machen Grundschulkinder wirklich mit Medien?</b>
        <span>Zahlen statt Bauchgefühl: was Kinder nutzen, ab wann und wie lange.</span></div></li>
        <li><span class="x">{CHECK}</span><div><b>Bringen Handyverbote an Schulen etwas?</b>
        <span>Von Frankreich bis Schweden – und was in Ihrem Bundesland gilt.</span></div></li>
        <li><span class="x">{CHECK}</span><div><b>Wie erkläre ich einem Achtjährigen Werbung, KI und Datenschutz?</b>
        <span>Zwölf Projekte mit Zeitplan, Material und Lernzielen.</span></div></li>
        <li><span class="x">{CHECK}</span><div><b>Was tue ich im Ernstfall?</b>
        <span>Cybermobbing, Abzocke, ungeeignete Inhalte: erste Schritte und wo es Hilfe gibt.</span></div></li>
      </ul>
    </div>
  </section>

  <section class="s" id="leseprobe">
    <figure class="excerpt">
      <blockquote>Ein Buch, das keine Angst macht, sondern Mut. Denn Wissen gibt Sicherheit.</blockquote>
      <figcaption>Aus dem Vorwort</figcaption>
      <div class="acts">
        <a class="btn btn-ghost" href="{AMAZON_EB}">Leseprobe bei Amazon ↗</a>
      </div>
    </figure>
    <div class="quotes">
      <blockquote class="quote"><p>Ein Kind, das an Zauberei glaubt, ist nicht naiv, sondern sieben.</p><cite>Kapitel 2</cite></blockquote>
      <blockquote class="quote"><p>Eine Regel, die ein Erstklässler wiedergeben kann, ist eine gute Regel.</p><cite>Kapitel 5</cite></blockquote>
      <blockquote class="quote"><p>Ein Kind, das ein Tablet flink entsperren und eine App öffnen kann, ist noch nicht medienkompetent.</p><cite>Kapitel 10</cite></blockquote>
      <blockquote class="quote"><p>Kinder, die sich kontrolliert fühlen, suchen Wege, die Kontrolle zu umgehen.</p><cite>Kapitel 14</cite></blockquote>
    </div>
  </section>

  <section class="s" id="material-teaser">
    <div class="split">
      <div>
        <p class="eyebrow">Für Familie und Schule</p>
        <h2>Material, das Sie sofort benutzen dürfen.</h2>
        <a class="btn btn-dark" href="/material/">Zu den Kopiervorlagen</a>
      </div>
      <div class="prose">
        <p class="big">Drei Kopiervorlagen aus dem Buch gibt es hier kostenlos als PDF – auch
        ohne das Buch.</p>
        <p>Der Mediennutzungsvertrag für die Familie, Regeln für den Klassenchat und ein
        Elternbrief, mit dem Schulen ihre Handyregel erklären. Kopieren für Familie, Schule und
        Elternarbeit ist ausdrücklich erlaubt.</p>
      </div>
    </div>
  </section>

  <section class="s" id="kaufen">
    <p class="eyebrow">Jetzt bestellen</p>
    <h2>Wählen Sie Ihre Ausgabe.</h2>
    <div class="cards">
      <div class="card main">
        <p class="kicker">Taschenbuch</p>
        <div class="p">{PREIS_TB}</div>
        <p>200 Seiten, 15 × 21 cm. Mit Kopiervorlagen zum Heraustrennen und Kopieren.</p>
        <div class="acts"><a class="btn btn-accent" href="{AMAZON}">Bei Amazon bestellen</a></div>
        <span class="note">ISBN 9798165446795</span>
      </div>
      <div class="card">
        <p class="kicker">Kindle</p>
        <div class="p">{PREIS_EB}</div>
        <p>Für Kindle-Geräte und die Kindle-App. Schriftgröße frei wählbar.</p>
        <div class="acts"><a class="btn btn-dark" href="{AMAZON_EB}">E-Book kaufen</a></div>
        <span class="note">Sofort verfügbar</span>
      </div>
      <div class="card">
        <p class="kicker">Für Schule und Verein</p>
        <div class="p">Vortrag</div>
        <p>Ein Abend für Elternvertretung, Förderverein oder Kollegium.</p>
        <div class="acts"><a class="btn btn-dark" href="/vortraege/">Mehr erfahren</a></div>
        <span class="note">Berlin und Umgebung</span>
      </div>
    </div>
  </section>

  <section class="s" id="kontakt">
    <div class="contact">
      <div>
        <h2>Vortrag, Elternabend oder Interview?</h2>
        <p>Für Veranstaltungen an Schulen, Presseanfragen und Rezensionsexemplare.</p>
      </div>
      <div class="mail">
        <code>{MAIL}</code>
      </div>
    </div>
  </section>
"""

# ---------------------------------------------------------------- Material
VORLAGEN = [
    ("Unser Mediennutzungsvertrag", "Unser_Mediennutzungsvertrag.pdf",
     "Für Familien mit Grundschulkindern. Gemeinsam ausfüllen, gut sichtbar aufhängen und nach "
     "einigen Wochen überprüfen. Mit Feldern für eigene Regeln und Platz für Unterschriften.",
     "Eine Seite, A4"),
    ("Unsere Klassenchat-Regeln", "Unsere_Klassenchat-Regeln.pdf",
     "Zehn Regeln, aus denen eine Klasse ihre wichtigsten auswählt und eigene ergänzt. Zum "
     "Aushängen, Unterschreiben und nach ein paar Wochen gemeinsam Überprüfen.",
     "Eine Seite, A4"),
    ("Elternbrief zur Handyregel", "Elternbrief_zur_Handyregel.pdf",
     "Ein Muster für Schulen, die ihre Handyregel erklären möchten: Regel, Ausnahmen, "
     "Erreichbarkeit im Notfall und Medien im Unterricht. Die eckigen Klammern anpassen, fertig.",
     "Eine Seite, A4"),
]
MATERIAL = """
  <header class="pagehead">
    <p class="eyebrow">Für Familie und Schule</p>
    <h1>Material</h1>
    <p class="lead">Drei Kopiervorlagen aus dem Buch, kostenlos als PDF. Das Kopieren für
    Familie, Schule und Elternarbeit ist ausdrücklich erlaubt – ohne Anmeldung, ohne
    E-Mail-Adresse.</p>
  </header>
  <section class="s">
    <div class="cards">
""" + "".join(f"""      <div class="card">
        <h3>{t}</h3>
        <p>{d}</p>
        <div class="acts"><a class="btn btn-dark" href="/pdf/{f}" download>PDF herunterladen</a></div>
        <span class="note">{n} · PDF</span>
      </div>
""" for t, f, d, n in VORLAGEN) + """    </div>
  </section>
  <section class="s">
    <div class="split">
      <div>
        <p class="eyebrow">Und im Buch</p>
        <h2>Zwölf Projekte für Klassenzimmer und Küchentisch.</h2>
      </div>
      <div class="prose">
        <p class="big">Die Kopiervorlagen sind der Anhang. Der praktische Teil des Buches sind
        zwölf ausgearbeitete Projekte für die Klassen 1 bis 6.</p>
        <p>Jedes mit Zeitplan, Materialliste, Lernziel und zwei Reflexionsfragen für die Kinder:
        von der Geräuschejagd im Schulhaus über die Werbedetektive bis zu der Frage, warum eine
        KI sich irrt. Zugeordnet zum Berliner Basiscurriculum Medienbildung und zu den
        Kompetenzbereichen der Kultusministerkonferenz.</p>
        <p><a class="btn btn-dark" href="/#kaufen">Buch bestellen</a></p>
      </div>
    </div>
  </section>
"""

# ---------------------------------------------------------------- Vorträge
VORTRAEGE = f"""
  <header class="pagehead">
    <p class="eyebrow">Für Schulen, Fördervereine und Elternvertretungen</p>
    <h1>Vorträge und Elternabende</h1>
    <p class="lead">Ein Abend über Medien in der Grundschule: was die Forschung sagt, was
    Handyverbote leisten – und was Sie am nächsten Morgen tun können.</p>
  </header>

  <section class="s">
    <div class="split">
      <div>
        <p class="eyebrow">Worum es geht</p>
        <h2>Kein Vortrag über Gefahren. Ein Abend über Handlungsmöglichkeiten.</h2>
      </div>
      <div class="prose">
        <p class="big">Elternabende zum Thema Medien enden oft mit mehr Sorge als vorher. Das
        muss nicht sein.</p>
        <p>Ich erzähle, was Kinder zwischen sechs und zehn wirklich mit Medien tun, was
        Handyverbote in Europa und in den Bundesländern bewirkt haben und wo sie aufhören zu
        wirken. Vor allem aber geht es um das, was danach kommt: wie Familien zu Regeln kommen,
        die im Alltag halten, und wie Schulen Medienbildung unterbringen, ohne ein neues Fach
        zu erfinden.</p>
        <p>Dabei spreche ich als Vater eines Grundschulkindes, nicht als jemand, bei dem zu
        Hause alles glattläuft. Die ehrlichen Baustellen gehören dazu.</p>
      </div>
    </div>
    <div class="theses">
      <div class="thesis"><h3>Elternabend</h3><p>Rund 60 Minuten plus Fragen. Für eine Klasse,
      eine Jahrgangsstufe oder die ganze Schule.</p></div>
      <div class="thesis"><h3>Kollegium</h3><p>Für Studientage und Fachkonferenzen: Methoden,
      Projekte und der Rahmen Ihres Bundeslandes.</p></div>
      <div class="thesis"><h3>Förderverein</h3><p>Ein Abend für Mitglieder und Interessierte,
      gern verbunden mit einer Diskussion über die Regeln an Ihrer Schule.</p></div>
    </div>
  </section>

  <section class="s">
    <div class="split">
      <div>
        <p class="eyebrow">Praktisches</p>
        <h2>Was Sie wissen müssen.</h2>
      </div>
      <div class="prose">
        <p><b>Wo:</b> Berlin und Umgebung, ohne Reisekosten. Darüber hinaus auf Anfrage, auch
        online.</p>
        <p><b>Was es kostet:</b> Für Schulen, Fördervereine und Elternvertretungen in Berlin
        mache ich das in der Regel ohne Honorar. Es geht mir um das Thema, nicht um den Abend.</p>
        <p><b>Was Sie brauchen:</b> einen Raum, einen Beamer und jemanden, der den Abend
        moderiert. Mehr nicht.</p>
        <p><b>Vorlauf:</b> Vier bis sechs Wochen sind angenehm, kurzfristiger geht oft auch.</p>
      </div>
    </div>
  </section>

  <section class="s">
    <div class="contact">
      <div>
        <h2>Termin anfragen</h2>
        <p>Schreiben Sie kurz, für wen der Abend gedacht ist und wann er stattfinden soll.
        Ich melde mich innerhalb weniger Tage.</p>
      </div>
      <div class="mail"><code>{MAIL}</code></div>
    </div>
  </section>
"""

# ---------------------------------------------------------------- Über mich
UEBER = f"""
  <header class="pagehead">
    <p class="eyebrow">Über mich</p>
    <h1>Sebastian Klatt</h1>
    <p class="lead">Vater eines Grundschulkindes, Mediengestalter, und seit diesem Jahr Autor
    eines Buches, das ich selbst gebraucht hätte.</p>
  </header>

  <section class="s">
    <div class="author">
      <img class="portrait" src="/assets/img/sebastian-klatt.jpg" width="720" height="900"
        alt="Sebastian Klatt, Autor von „Verbieten reicht nicht“" loading="lazy">
      <div class="prose">
        <p class="big">Der größte Auslöser für dieses Buch ist mein Sohn.</p>
        <p>Er ist sieben Jahre alt, und bei ihm, bei seinen Freundinnen und Freunden, bei seinen
        Mitschülerinnen und Mitschülern nimmt die Mediennutzung stetig zu. Erst die Tonie-Box und
        die Musikbox, dann der Fernseher am Wochenende, inzwischen eine Smartwatch. Irgendwann
        wird das erste Smartphone kommen.</p>
        <p>Beruflich komme ich aus der Medienproduktion. Ich bin ausgebildeter Mediengestalter
        Bild und Ton und arbeite seit über 20 Jahren mit Medien, als Videograf, Fotograf, Editor,
        Motion Designer und Creative Director. Ich weiß, wie Licht, Farben, Musik und Dramaturgie
        Gefühle erzeugen, und wie schwer es selbst für Erwachsene ist, das zu durchschauen.
        Dieses Wissen möchte ich weitergeben. Außerdem engagiere ich mich im Förderverein der
        Grundschule unseres Sohnes.</p>

        <h3>Warum dieses Buch</h3>
        <p>Ich habe mir ein Buch gewünscht, von dem alle etwas haben: eine Fibel zum
        Nachschlagen, zum Lesen, zum Informieren und zum Sensibilisieren. Ein Buch, das keine
        Angst macht, sondern Mut. Denn Wissen gibt Sicherheit: Wer versteht, wie Medien
        funktionieren, kann auf der Grundlage von Fakten selbst entscheiden.</p>
        <p>Und ich sage ganz offen: Auch wir Eltern wissen nicht alles. Wir müssen uns ständig
        und immer wieder neu mit diesen Themen auseinandersetzen. In den persönlichen Kästen des
        Buches erzähle ich deshalb, wie wir es als Familie machen. Ehrlich, auch dort, wo bei uns
        selbst noch eine Baustelle ist.</p>

        <h3>Warum Berlin</h3>
        <p>Das Buch schaut immer wieder besonders auf Berlin. Ich schreibe als Vater eines
        Berliner Grundschulkindes und kenne die Schule hier aus eigener Anschauung. In Berlin und
        Brandenburg dauert die Grundschule sechs Jahre, die Zeit des ersten Smartphones liegt
        hier also noch in der Grundschulzeit. Und Berlin verzichtet auf ein landesweites
        Handyverbot, überlässt die Regeln also den Schulen. Daran lässt sich gut zeigen, wie viel
        an der einzelnen Schule entschieden wird.</p>
        <p>Berlin ist dabei Beispiel, nicht Maßstab. Bildung ist Ländersache, und das Buch
        vergleicht alle 16 Länder.</p>

        <h3>Für die Presse</h3>
        <p>Rezensionsexemplare, Interviews und Bildmaterial auf Anfrage. Die Übersicht über die
        Handyregeln und die Verankerung von Medienbildung in allen 16 Bundesländern (Stand
        Oktober 2026) stelle ich Redaktionen gern zur Verfügung.</p>
      </div>
    </div>
  </section>

  <section class="s">
    <div class="contact">
      <div>
        <h2>Kontakt</h2>
        <p>Für Anfragen von Schulen, Vereinen, Redaktionen – und für ehrliche Rückmeldungen
        zum Buch.</p>
      </div>
      <div class="mail"><code>{MAIL}</code></div>
    </div>
  </section>
"""

# ---------------------------------------------------------------- Impressum
IMPRESSUM = f"""
  <header class="pagehead">
    <h1>Impressum</h1>
    <p class="lead">Angaben gemäß § 5 Digitale-Dienste-Gesetz (DDG).</p>
  </header>
  <section class="s">
    <div class="prose">
      <h3>Diensteanbieter</h3>
      <p>Sebastian Klatt<br>Britzer Straße 58a<br>12109 Berlin<br>Deutschland</p>

      <h3>Kontakt</h3>
      <p>E-Mail: {MAIL}</p>

      <h3>Verantwortlich für den Inhalt nach § 18 Abs. 2 MStV</h3>
      <p>Sebastian Klatt, Anschrift wie oben.</p>

      <h3>Umsatzsteuer</h3>
      <p>{PH % "[Umsatzsteuer-Identifikationsnummer, falls vorhanden – sonst diesen Abschnitt löschen]"}</p>

      <h3>Hinweis auf Partnerlinks</h3>
      <p>{PH % "[Nur nötig, wenn Sie Amazon-Partnerlinks verwenden. Dann hier kennzeichnen.]"}</p>

      <h3>Streitbeilegung</h3>
      <p>Ich bin nicht bereit und nicht verpflichtet, an Streitbeilegungsverfahren vor einer
      Verbraucherschlichtungsstelle teilzunehmen.</p>

      <h3>Haftung für Inhalte und Links</h3>
      <p>Die Inhalte dieser Seiten wurden mit Sorgfalt erstellt. Für die Richtigkeit,
      Vollständigkeit und Aktualität der Inhalte kann ich keine Gewähr übernehmen. Diese Website
      enthält Links zu externen Websites Dritter, auf deren Inhalte ich keinen Einfluss habe.
      Für die Inhalte der verlinkten Seiten ist stets der jeweilige Anbieter verantwortlich. Zum
      Zeitpunkt der Verlinkung waren keine Rechtsverstöße erkennbar. Bei Bekanntwerden von
      Rechtsverletzungen entferne ich solche Links umgehend.</p>

      <h3>Urheberrecht</h3>
      <p>Die auf dieser Website veröffentlichten Inhalte unterliegen dem deutschen Urheberrecht.
      Ausgenommen sind die hier bereitgestellten Kopiervorlagen: Sie dürfen für den Gebrauch in
      Familie, Schule und Elternarbeit kopiert und weitergegeben werden.</p>
    </div>
  </section>
"""

# ---------------------------------------------------------------- Datenschutz
DATENSCHUTZ = f"""
  <header class="pagehead">
    <h1>Datenschutzerklärung</h1>
    <p class="lead">Diese Website kommt ohne Cookies, ohne Tracking und ohne Werbenetzwerke aus.
    Sie können sie lesen und die Kopiervorlagen herunterladen, ohne Daten anzugeben.</p>
  </header>
  <section class="s">
    <div class="prose">
      <h3>Verantwortlicher</h3>
      <p>Sebastian Klatt, Britzer Straße 58a, 12109 Berlin, Deutschland.<br>
      E-Mail: {MAIL}</p>

      <h3>Hosting</h3>
      <p>Diese Website wird gehostet von IT-Service Reiko Kretzschmar (Web-Service4U),
      Verbindungsweg 4, 17309 Pasewalk, Deutschland. Beim Aufruf der Seiten verarbeitet der
      Hoster technisch notwendige Daten, insbesondere IP-Adresse, Datum und Uhrzeit des
      Zugriffs, aufgerufene Seite, übertragene Datenmenge sowie Browser- und
      Betriebssysteminformationen. Rechtsgrundlage ist Art. 6 Abs. 1 lit. f DSGVO; das
      berechtigte Interesse liegt in einem sicheren und zuverlässigen Betrieb der Website.
      Mit dem Hoster besteht ein Vertrag über die Auftragsverarbeitung nach Art. 28 DSGVO.
      Die Server stehen in Deutschland; eine Übermittlung in Drittländer findet nicht statt.</p>

      <h3>Keine Cookies, keine Analyse</h3>
      <p>Diese Website setzt keine Cookies und bindet keine Analyse-, Werbe- oder
      Social-Media-Dienste ein. Es gibt deshalb auch keinen Cookie-Banner.</p>

      <h3>Schriften</h3>
      <p>Die verwendeten Schriftarten werden von diesem Server ausgeliefert. Es besteht keine
      Verbindung zu Google Fonts oder einem anderen externen Anbieter, und es werden dabei keine
      Daten an Dritte übertragen.</p>

      <h3>Downloads</h3>
      <p>Die Kopiervorlagen können ohne Anmeldung und ohne Angabe einer E-Mail-Adresse
      heruntergeladen werden. Es findet keine Registrierung statt.</p>

      <h3>Kontaktaufnahme per E-Mail</h3>
      <p>Wenn Sie mir schreiben, verarbeite ich Ihre Angaben zur Bearbeitung Ihrer Anfrage und
      für mögliche Anschlussfragen. Rechtsgrundlage ist Art. 6 Abs. 1 lit. b DSGVO, sofern Ihre
      Anfrage auf einen Vertrag zielt, sonst Art. 6 Abs. 1 lit. f DSGVO. Ich lösche die Daten,
      sobald sie nicht mehr erforderlich sind, und prüfe das regelmäßig; gesetzliche
      Aufbewahrungspflichten bleiben unberührt.</p>

      <h3>Externe Links</h3>
      <p>Diese Website verlinkt auf externe Angebote, insbesondere auf Amazon. Beim Anklicken
      eines solchen Links verlassen Sie diese Website; es gelten dann die
      Datenschutzbestimmungen des jeweiligen Anbieters. Vor dem Klick werden keine Daten an
      diese Anbieter übertragen.</p>

      <h3>Ihre Rechte</h3>
      <p>Sie haben das Recht auf Auskunft (Art. 15 DSGVO), Berichtigung (Art. 16), Löschung
      (Art. 17), Einschränkung der Verarbeitung (Art. 18), Datenübertragbarkeit (Art. 20) sowie
      ein Widerspruchsrecht gegen Verarbeitungen auf Grundlage berechtigter Interessen
      (Art. 21). Wenden Sie sich dafür an die oben genannte Adresse. Außerdem steht Ihnen ein
      Beschwerderecht bei einer Aufsichtsbehörde zu, für Berlin bei der Berliner Beauftragten
      für Datenschutz und Informationsfreiheit.</p>

      <h3>Stand</h3>
      <p>{PH % "[Datum der Veröffentlichung eintragen]"}</p>
    </div>
  </section>
"""

PAGES = [
    ("index.html", "Verbieten reicht nicht – Handy weg, und dann? | Sebastian Klatt",
     "Medienkompetenz in der Grundschule: Was Kinder wirklich mit Medien tun, was Handyverbote "
     "leisten und zwölf Projekte für Klassenzimmer und Küchentisch. Ein Wegweiser für Eltern "
     "und Lehrkräfte.", START, 0, "/"),
    ("material/index.html", "Material und Kopiervorlagen | Verbieten reicht nicht",
     "Mediennutzungsvertrag, Klassenchat-Regeln und Elternbrief zur Handyregel: drei "
     "Kopiervorlagen aus dem Buch, kostenlos als PDF.", MATERIAL, 1, "/material/"),
    ("vortraege/index.html", "Vorträge und Elternabende | Verbieten reicht nicht",
     "Ein Abend über Medien in der Grundschule für Schulen, Fördervereine und "
     "Elternvertretungen in Berlin und Umgebung.", VORTRAEGE, 1, "/vortraege/"),
    ("ueber-mich/index.html", "Über mich – Sebastian Klatt | Verbieten reicht nicht",
     "Vater eines Grundschulkindes, Mediengestalter Bild und Ton, Autor von „Verbieten reicht "
     "nicht“. Warum dieses Buch entstanden ist.", UEBER, 1, "/ueber-mich/"),
    ("impressum/index.html", "Impressum | Verbieten reicht nicht",
     "Impressum nach § 5 DDG.", IMPRESSUM, 1, "/impressum/"),
    ("datenschutz/index.html", "Datenschutzerklärung | Verbieten reicht nicht",
     "Diese Website kommt ohne Cookies, ohne Tracking und ohne externe Schriften aus.",
     DATENSCHUTZ, 1, "/datenschutz/"),
]


def main():
    for path, title, desc, body, depth, active in PAGES:
        p = page(path, title, desc, body, depth, active)
        print(p.relative_to(S), len(p.read_text(encoding="utf8")) // 1024, "KB")
    (S / "robots.txt").write_text(
        f"User-agent: *\nAllow: /\n\nSitemap: {DOMAIN}/sitemap.xml\n", encoding="utf8")
    urls = "".join(f"  <url><loc>{DOMAIN}{a}</loc></url>\n" for *_, a in PAGES)
    (S / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + urls + "</urlset>\n",
        encoding="utf8")
    (S / ".htaccess").write_text(HTACCESS, encoding="utf8")
    print("robots.txt, sitemap.xml, .htaccess")


if __name__ == "__main__":
    main()
