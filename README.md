# verbietenreichtnicht.de

Website zum Buch „Verbieten reicht nicht – Handy weg, und dann?" von Sebastian Klatt.

## Wie die Seite online geht

Jeder Push auf `main`, der etwas unter `site/` ändert, lädt die Seite
automatisch per FTPS zu Web-Service4U hoch. Niemand muss Dateien von Hand
kopieren. Der Ablauf steht in `.github/workflows/deploy.yml`.

Ein Deploy lässt sich auch von Hand auslösen: Reiter **Actions** →
„Website veröffentlichen" → **Run workflow**.

## Was wo liegt

| Pfad | Inhalt |
|---|---|
| `site/` | die fertige Website – genau das, was hochgeladen wird |
| `site/.htaccess` | HTTPS-Zwang, www-Umleitung, Caching, Sicherheits-Header |
| `site/pdf/` | die drei Kopiervorlagen aus dem Buch |
| `tools/build_site.py` | erzeugt `site/` neu |
| `tools/vorlagen.py` | erzeugt die PDFs aus dem Buchsatz |

`site/` wird von `build_site.py` erzeugt. Änderungen am Inhalt gehören
deshalb in das Skript, nicht in die HTML-Dateien – sonst sind sie beim
nächsten Lauf weg.

## Benötigte Secrets

Unter **Settings → Secrets and variables → Actions**:

| Name | Inhalt |
|---|---|
| `FTP_SERVER` | FTP-Servername aus LiveConfig |
| `FTP_USERNAME` | FTP-Benutzer |
| `FTP_PASSWORD` | FTP-Passwort |

Die Zugangsdaten stehen nur hier. Sie gehören in keine Datei des
Repositorys und in keinen Chatverlauf.

## Noch offen

- Preise für Taschenbuch und Kindle
- die beiden Amazon-Links
- Erscheinungsdatum
- Kontaktadresse `kontakt@verbietenreichtnicht.de`
- Datum unter der Datenschutzerklärung

Diese Stellen sind auf der Seite als Platzhalter markiert und stehen
oben in `tools/build_site.py`.
