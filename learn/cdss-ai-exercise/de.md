---
title: "Übung: Ein CDSS selbst bauen – und prüfen"
summary: "Selbstständige Python-Übung zur Vorlesung Clinical Decision Support & KI: Sie implementieren eine Regel mit Tests, trainieren ein Modell, wählen einen Threshold, entdecken Leakage und prüfen das System in einer zweiten Klinik – direkt im Browser oder lokal in Jupyter."
duration_minutes: 90
level: "Übung · Python"
audiences: [med, cs, clin, tech]
order: 8
builds_on: [cdss-ai]
course: his
lecture: 6
kind: exercise
author: "Markus Wolfien"
objectives:
  - "Eine qSOFA-artige Regel als Funktion implementieren und mit Referenz-, Grenzwert- und Regressionstests prüfen"
  - "Eine logistische Regression trainieren und mit der AUC bewerten"
  - "Einen Threshold unter einer realistischen Alert-Vorgabe wählen und begründen"
  - "Eine Leakage-Variable erkennen"
  - "Ein Modell extern validieren und Diskrimination von Kalibrierung unterscheiden"
  - "Erklären, wie fehlende Werte Dokumentationsverhalten abbilden können"
  - "Die CDSS-Kette und die Zweckbestimmung für das eigene System beschreiben"
readings: [collins2024, finlayson2021, agniel2018]
related_topics: [cdss, data-quality]
source: "Übung zu Vorlesung 6 „Clinical Decision Support & KI – von Regeln zu lernenden Systemen“, Informationssysteme im Gesundheitswesen (WiSe 2026/27), Markus Wolfien, IMB & ZMI"
---

> **Worum es geht:** Im Modul [[cdss-ai]] haben Sie die CDSS-Kette kennengelernt: **DATA → TRIGGER → LOGIC → OUTPUT → ACTION → FEEDBACK**. Jetzt bauen Sie den mittleren Teil selbst – eine **Regel**, ein **Modell**, einen **Threshold** – und prüfen, ob das Ganze in einer zweiten Klinik noch funktioniert.

## So starten Sie

<div class="launch">
<a class="primary" href="../../../lab/lab/index.html?path=cdss-ai-exercise/Uebung_VL6_CDSS_Aufgaben.ipynb">▶ Notebook im Browser öffnen</a>
<a href="../notebook.zip" download>⬇ Notebook und Daten herunterladen (ZIP)</a>
</div>

**Im Browser (empfohlen):** Das Notebook läuft vollständig in Ihrem Browser (JupyterLite mit Pyodide) – ohne Installation, ohne Konto, ohne Server; die Daten verlassen Ihr Gerät nicht.

- Beim ersten Start lädt der Browser Python und die Bibliotheken; das dauert je nach Verbindung **etwa eine Minute**. Die erste Code-Zelle dauert ebenfalls etwas länger.
- Nutzen Sie ein **normales Browserfenster** (Chrome, Edge, Firefox, Safari) – im privaten Modus, besonders in Firefox, findet das Notebook die CSV-Dateien nicht.
- Ihre Änderungen bleiben **nur in diesem Browser** gespeichert. Sichern Sie Ihr Notebook zwischendurch über *File → Download*.

**Lokal:** Entpacken Sie die ZIP-Datei und öffnen Sie `Uebung_VL6_CDSS_Aufgaben.ipynb` in Jupyter (z. B. JupyterLab oder VS Code). Sie brauchen Python ≥ 3.10 mit `numpy`, `pandas`, `scikit-learn` und `matplotlib` (für den Bonus in Teil 6 zusätzlich `scipy`). Die CSV-Dateien müssen im selben Ordner wie das Notebook liegen.

> ⚠️ Der Datensatz ist **vollständig synthetisch** (Klinik A: 2.000, Klinik B: 1.500 Patient:innen). Das Outcome `verschlechterung_6h` ist eine didaktisch definierte Verschlechterung innerhalb von 6 Stunden – **keine Sepsisdiagnose**. Was Sie bauen, ist ein **Lehrprototyp** ohne medizinische Zweckbestimmung.

## Ablauf

| Teil | Thema | Bezug zur Vorlesung | Zeit |
|---|---|---|---:|
| 0 | Setup | | 5 min |
| 1 | Daten kennenlernen | DATA | 10 min |
| 2 | Eine Regel als Funktion – mit Tests | „Auch eine Regel kann falsch sein“ | 15 min |
| 3 | Ein Modell trainieren | Regel vs. gelernte Funktion | 10 min |
| 4 | Den Threshold wählen | „Der Threshold verändert das System“ | 15 min |
| 5 | Eine verdächtig gute Variable | Fehlerquellen | 8 min |
| 6 | Externe Validierung: Klinik B | Diskrimination vs. Kalibrierung, Monitoring | 15 min |
| 7 | Was bedeutet ein fehlender Wert? | Fehlerquellen | 7 min |
| 8 | Vom Modell zum CDSS | Synthese, Regulierung | 5 min |
| | **Gesamt** | | **90 min** |

Die Programmieraufgaben (mit `TODO` markiert) bearbeiten Sie im Notebook; meist genügen ein bis drei Zeilen. Solange eine Aufgabe offen ist, meldet die Zelle, was noch fehlt. Die **Fragen** unten finden Sie auch im Notebook – notieren Sie Ihre Antworten dort oder hier; hier bleiben sie in Ihrem Browser gespeichert und lassen sich am Ende herunterladen, z. B. für die Besprechung.

## Fragen zu den Teilen

```reflect
question: "**Teil 1b:** Gehen Sie die Spalten durch. Welche Information wäre zum Vorhersagezeitpunkt **tatsächlich verfügbar** – und bei welcher sind Sie unsicher?"
```

```reflect
question: "**Teil 2c:** Eine Kollegin schlägt vor, die Atemfrequenz-Schwelle auf `> 22` zu ändern. Welcher Test schlägt fehl – und was lernen Sie daraus?"
```

```reflect
question: "**Teil 2d:** Die Spezifität der Regel ist hoch, die Sensitivität niedrig. Passt das zur Aussage, dass qSOFA nicht als alleiniges Screening-Instrument empfohlen wird?"
```

```reflect
question: "**Teil 3:** Die AUC sagt, wie gut das Modell Patient:innen mit und ohne Ereignis *ordnet*. Kann man mit einer AUC allein schon einen Alert auslösen? Was fehlt noch?"
```

```reflect
question: "**Teil 4b:** Die Station sagt: „Mehr als 15 Alerts pro 100 Patient:innen schauen wir uns nicht mehr ernsthaft an.“ Welchen Threshold wählen Sie? Wie hoch sind dann Sensitivität und PPV? Und wer sollte diese Entscheidung eigentlich treffen?"
```

```reflect
question: "**Teil 5b:** Mit `antibiotikum_gegeben` wird das Modell deutlich „besser“. Würden Sie es so ausrollen? **Wann war diese Information verfügbar?**"
```

```reflect
question: "**Teil 6:** Die AUC ist in Klinik B fast gleich. Was bedeutet es für die Ärztin in Klinik B, wenn das System „Risiko 40 %“ anzeigt?"
```

```reflect
question: "**Teil 7b:** Welches Vorzeichen hat der Koeffizient von `laktat_fehlt` – und was hat das Modell damit eigentlich gelernt? Wäre dieses Wissen auf Klinik A übertragbar?"
```

```reflect
question: "**Teil 8:** Füllen Sie die CDSS-Kette für Ihr System aus, in Stichworten: **DATA** (welche Daten, wie aktuell?), **TRIGGER** (wann läuft es?), **LOGIC** (Regel, Modell oder beides? welcher Threshold?), **OUTPUT** (Info, Warnung, Hard Stop? an wen?), **ACTION** (was soll die Person konkret tun?), **FEEDBACK** (welche Kennzahlen überwachen Sie nach dem Go-live?)."
rows: 7
```

```reflect
question: "**Abschlussfrage:** Ihr Notebook ist ein Lehrprototyp. Was müsste sich ändern, damit es zu einem Medizinprodukt wird – und welche Rolle spielt dabei die **Zweckbestimmung**?"
```
