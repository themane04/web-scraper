# Modul 122 - Teil 2

## Zweck des Skriptes

Das Skript dient dazu, Daten von verschiedenen Nachrichtenwebseiten zu extrahieren und in eine PostgreSQL-Datenbank zu
speichern. Es ermöglicht die semi-automatische Sammlung von Artikeldaten, einschliesslich Titel, Text,
Veröffentlichungsdatum und Autor.

## Ziele und Anforderungen

Bis zum Zeitpunkt der Abgabe am 18.06.2024 um 14:00 UHR. soll...

* Semi-Automatisches (also manuell bestätigt und ausgeführt) Scraping von Nachrichtenartikeln von verschiedenen
  Webseiten möglich sein.
* Speicherung der gesammelten Daten in einer PostgreSQL-Datenbank möglich sein.
* Robustes Fehlerhandling (keine unerwarteten Fehler) und effiziente Datenspeicherung (Keine unbenutzten oder unnötigen
  Columns oder Filetypes) implementiert sein.

## Vorgehen

* Entwicklung einer Database-Klasse zur Verwaltung der PostgreSQL-Datenbank.
* Entwicklung einer Scraper-Klasse zum Abrufen und Parsen von HTML-Inhalten.
* Implementierung von spezifischen Parsing-Methoden für verschiedene Nachrichtenwebseiten.
* Verwendung einer switch-case-Struktur, um den passenden Scraper basierend auf der URL auszuwählen.

## Diagramme und Video

### Video

Das Video finden Sie [hier](Praxisarbeit_LB2/02_Marjan/webScraper.mp4).

### PAP / Flussdiagramm / Struktogramm

<br>
<img src="Praxisarbeit_LB2/01_Leonid/m122_lb2_diagram.drawio.png" width="300">
<br>

Beschreibung: Das Diagramm zeigt den Ablauf des Skripts von der URL-Eingabe über das Scraping und Parsen der Daten bis
hin zur Speicherung in der Datenbank.

### Test Case

<br>
<img src="Praxisarbeit_LB2/01_Leonid/m122_lb2_testcase.drawio.png" width="300">
<br>

Beschreibung: Das Diagramm zeigt, wie das Skript in verschiedenen Testfällen reagiert, einschliesslich erfolgreicher und
fehlerhafter Szenarien.

### Use Case

<br>
<img src="Praxisarbeit_LB2/01_Leonid/m122_lb2_usecase.drawio.png" width="300">
<br>

Beschreibung: Die drei Diagramme zeigen den Ablauf des Skripts in verschiedenen normalen Szenarien, einschliesslich
Eingabe, Scraping und Speicherung der Daten.

## Skript/Programm

### Technologie

* Python
* PostgreSQL
* Bibliotheken: requests, BeautifulSoup, psycopg2

### Ein- und Ausgabe

* Eingabe: URLs der Nachrichtenwebseiten über CLI oder File
* Ausgabe: Gespeicherte Artikeldaten in der PostgreSQL-Datenbank, und im CLI

### Kontrollstrukturen

* try-except-Blöcke für Fehlerbehandlung bei HTTP-Anfragen
* switch-case-Struktur zur Auswahl des passenden Scrapers
* Schleifen zur Verarbeitung mehrerer URLs

## Bedienung

### Installation

#### 1. Die Umgebung (.venv) installieren:

```bash
python -m venv venv
```

#### 2. Die Umgebung aktivieren:

```bash
# Windows
.venv\Scripts\activate.ps1
```

```bash
# Linux
. venv/bin/activate
```

#### 3. Die benötigten Bibliotheken installieren:

```bash
pip install -r requirements.txt
```

#### 4. Das Skript ausführen:

```bash
python main.py
```

## Error-Handling

* Nutzung von try-except-Blöcken zur Behandlung von HTTP-Fehlern und Datenbankfehlern.
* Validierung der HTML-Inhalte vor der Verarbeitung.
* Sicherstellung der Datenintegrität durch Verwendung von ON CONFLICT DO NOTHING bei der Datenbankeinfügung.

## Testfälle

* Erfolgreiches Scraping: Daten werden korrekt von der Webseite extrahiert und in der Datenbank gespeichert.
* HTTP-Fehler: Umgang mit Seiten, die nicht geladen werden können.
* Fehlende Elemente: Behandlung von Artikeln, bei denen Titel, Veröffentlichungsdatum oder Autor fehlen.

### Liste der Haupttestfälle oder Verweise auf Testdokumentation.

* Testfall 1: Scraping einer funktionierenden Webseite.
* Testfall 2: Umgang mit einer nicht erreichbaren Webseite.
* Testfall 3: Verarbeitung einer Webseite mit fehlenden Artikeldetails.

## Integration und Sicherheit ##

### Implementierung

* Integration des Scrapers mit einer PostgreSQL-Datenbank zur Speicherung der gesammelten Daten.
* Modulare Struktur zur einfachen Erweiterung um zusätzliche Webseiten.

### Sicherheit

* Absicherung der Datenbankverbindung durch sichere Speicherung der Zugangsdaten.
* Robustheit gegenüber ungültigen oder unerwarteten HTML-Inhalten.

## Reflexion ##

### Ergebnis ###

Das Skript ermöglicht die effiziente und automatische Sammlung von Artikeldaten von verschiedenen Nachrichtenwebseiten
und deren Speicherung in einer PostgreSQL-Datenbank.

### Zusammenarbeit ###

Die Entwicklung des Skripts erfolgte durch laufende Verbesserungen und die Integration von Feedback.

Auch geholfen hat, dass wir direkt am Anfang, einen klaren Ablauf für das Script entworfen haben, bei dem alle Kriterien
erfüllt wurden.

### Fazit ###

Es war ein lehrreiches Projekt, bei dem viel über Datenbanken und deren Anwendung innerhalb der Skripte gelernt wurde.
Auch in Bezug auf die OOP-Methode wurden wertvolle Erkenntnisse gewonnen. Die Zusammenarbeit war gut, und es hat Spass
gemacht, mit solch kompetenten Menschen zusammenarbeiten zu dürfen.

## Anhang

* Weitere Ressourcen und Quellcode: https://git.gibb.ch/urs.dummermuth/inf-122-23n-sg2 