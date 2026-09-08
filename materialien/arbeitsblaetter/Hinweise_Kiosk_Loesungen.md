# Kiosk und Lösungspaket · Fassung 3

Schritt 6 abgeschlossen · 8. September 2026

## Im Raum

Der Kiosk gehört auf den Klassenraum-Laptop. Kinder wählen „Tipp“ oder „Lösung“, geben Blatt 1–24 mit Tastatur oder Bildschirm-Zahlenfeld ein und wählen „Anzeigen“ (oder Enter). Am Ergebnis kann zwischen Tipp und Lösung gewechselt werden. Freiwillige Zusätze öffnen sich erst beim Anklicken. Danach „Zurück zum Start“ wählen.

Während des Lesens gibt es keine Zeitbegrenzung. Bei der Nummerneingabe führt eine Pause von drei Minuten zum Start. Escape führt ebenfalls zum Start, Backspace löscht eine Ziffer und Delete die Eingabe. Der Vollbildknopf nutzt den Browser-Vollbildmodus, ersatzweise F11. Die HTML-Datei enthält alle Inhalte und benötigt nach dem Speichern keine Internetverbindung. Es werden keine Kinderdaten gespeichert.

Die Datei `apps/kontroll-kiosk/index.html` als vollständige HTML-Datei auf dem Laptop speichern und im Browser öffnen. Vor dem Unterricht einmal Tipp, Lösung und Vollbild am tatsächlichen Gerät ausprobieren. Der Kiosk ist für Maus/Touchpad, Tastatur und Touch bedienbar. Bei Leseproblemen kann ein Partnerkind oder eine Lehrkraft vorlesen.

## Rückmeldung und Grenzen

Die Lösungen passen zu den Arbeitsblättern in Fassung 3. Geschlossene Aufgaben erhalten ihre konkrete Antwort, offene Aufgaben Vergleichsbeispiele und Kriterien. Plausible Alternativen sind besonders bei Zuständigkeiten, Wünschen, Anreden, Gründen und Reflexionen zulässig. Kein wortgleiches Abschreiben verlangen. Die Kiosktexte sind Orientierung, keine automatische Bewertung.

Blatt 21 enthält keinen Musterbrief zur Probearbeit. Für den ersten Versuch gelten die festgelegten Hilfen; zusätzliche Unterstützung wird notiert. Der Kiosk gehört nicht zu den regulären Prüfungshilfen. Nach der Probearbeit erfolgt die Rückmeldung mit der Lehrkraft. Die angeglichenen Prüfungsunterlagen enthalten bereits beide erlaubten Hilfeseiten; siehe [Durchführungshinweise](../lernerfolgskontrolle/Hinweise_Pruefungen_Fassung3.md).

Der Kiosk deckt Blatt 1–24 ab. Die neuen freiwilligen Projekte und Vertiefungen haben eigene Einsatz- und Lösungshinweise im Projektordner. Keine Projektzahl in den Kiosk eingeben.

## Gedruckte Fassung

Das Lösungspaket enthält 24 DIN-A5-Seiten mit 14-Punkt-Grundschrift: Tipp, Lösung beziehungsweise Vergleich, freiwilliger Zusatz und Lehrkrafthinweis. DOCX und PDF stehen bereit. Bei Ausgabe an Kinder die Lehrkrafthinweise berücksichtigen; die Kioskfassung enthält diese nicht.

## Gemeinsame Datenquelle

`loesungen_inhalte.json` enthält die geprüften Texte. `tools/generate_loesungen.py` erzeugt daraus die Daten im eigenständig nutzbaren Kiosk und die DOCX. Die PDF wird anschließend aus der DOCX gerendert. Der Generator prüft Blattnummern und Titel gegen `arbeitsblaetter_inhalte.json`. Nach Änderungen alle betroffenen Seiten prüfen und DOCX, PDF und Kiosk gemeinsam aktualisieren.

`tools/check_kiosk.cjs` prüft mit Playwright alle 48 Tipp-/Lösungsansichten, Offlinebetrieb, Tastatur und Zahlenfeld, Fehlermeldungen, Moduswechsel, freiwillige Zusätze, Zeitverhalten und schmale Ansichten. Ein eigener Browserpfad kann über `KIOSK_BROWSER` angegeben werden.

`tools/check_kiosk_logic.cjs` prüft dieselben Kernfälle ohne Browser in einer DOM-Simulation. Ein bestandener Logiktest ersetzt keine Sichtprüfung am Browser.
