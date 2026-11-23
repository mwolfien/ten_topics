---
title: "Clinical Decision Support & KI – von Regeln zu lernenden Systemen"
summary: "Wie wird aus klinischen Daten eine Empfehlung – und wie prüfen wir, ob sie zuverlässig, nützlich und sicher genug für die Versorgung ist? Regeln, Scores und Pathways, Integration in den Arbeitsplatz, Validierung, echte Systeme und Regulierung am Fall Maria K."
duration_minutes: 75
level: "Vertiefung"
audiences: [med, cs, clin, tech, pat]
order: 7
builds_on: [specialized-systems, communication-standards]
course: his
lecture: 6
author: "Markus Wolfien"
objectives:
  - "Regelbasierte CDSS erklären und Regeln, Leitlinien und Pathways unterscheiden"
  - "Die Integration von CDSS in KIS und klinischen Arbeitsplatz beschreiben"
  - "CDSS mit geeigneten Kennzahlen bewerten – Sensitivität, PPV, Threshold, Kalibrierung"
  - "Regelbasierte und lernende Systeme vergleichen und typische Fehlerquellen erkennen"
  - "Die Grundlogik von MDR und AI Act für CDSS einordnen"
readings: [wong2021, adams2022, zech2018, agniel2018, finlayson2021, singer2016, evans2021, collins2024, vasey2022, vandersijs2006]
related_topics: [cdss, data-quality, privacy-ethics, fhir, ehr-cis]
source: "Vorlesung 6 „Clinical Decision Support & KI – von Regeln zu lernenden Systemen“, Informationssysteme im Gesundheitswesen (WiSe 2026/27), Markus Wolfien, IMB & ZMI"
---

> **Leitfrage:** Wie wird aus klinischen Daten eine Empfehlung – und wie prüfen wir, ob sie zuverlässig, nützlich und sicher genug für die Versorgung ist?

Bisher haben unsere Systeme Informationen **bereitgestellt**: KIS und Subsysteme ([[information-systems]]), Arbeitsplatz, CPOE und Workflows ([[specialized-systems]]), Standards ([[communication-standards]]). Jetzt beginnen sie, daraus **Vorschläge abzuleiten**. Was KI ist und wie Training, Test und Generalisierung funktionieren, setzen wir voraus; hier geht es eine Ebene näher an das klinische System: Wie entsteht eine Empfehlung, wie gelangt sie zur Nutzerin, wie wird sie validiert – und wann wird daraus regulierte Software? In der begleitenden Übung bauen Sie diese Kette selbst.

```persona med
Sie werden Scores lesen, Warnungen bekommen und Risiken angezeigt sehen. Dieses Modul zeigt, was hinter „Risiko 78 %“ steckt, warum viele Alerts Fehlalarme sind – und warum die Entscheidung trotzdem bei Ihnen bleibt.
```

```persona cs
IF–THEN-Regeln mit Unit-Tests, logistische Regression mit Threshold, Konfusionsmatrix, Kalibrierung, Data Leakage, Dataset Shift: Hier treffen Ihre Werkzeuge auf klinische Wirklichkeit – und auf die Frage, wann aus Code ein Medizinprodukt wird.
```

```persona clin
Warum warnt das System ständig – und manchmal gerade dann nicht, wenn es darauf ankommt? Sie lernen, welche Fragen Sie einem CDSS vor der Einführung stellen sollten und wer über Eskalationsstufen entscheiden sollte.
```

```persona tech
CDS Hooks, FHIR Subscriptions, Scheduler, Wissensbasen mit Versionierung und Regressionstests, Monitoring nach dem Go-live: Ein CDSS ist Betrieb, nicht nur ein Modell.
```

```persona pat
Immer mehr Software unterstützt Ärzt:innen bei Entscheidungen. Dieses Modul zeigt, wie sie funktioniert, wie man prüft, ob sie wirklich hilft – und welche Regeln dafür in der EU gelten.
```

```case
**Maria K., 62 Jahre** – die Patientin aus der Datenschutz-Vorlesung. Vorgeschichte: Diabetes Typ 2, chronische Niereninsuffizienz. Jetzt: Dyspnoe, Fieber, Verdacht auf Pneumonie.

**Vitalwerte:** Temperatur 39,1 °C · Herzfrequenz 112/min · Atemfrequenz 26/min · RR systolisch 96 mmHg · SpO₂ 91 % (Raumluft) · Bewusstsein orientiert

**Labor:** Kreatinin 1,6 mg/dl · eGFR 38 · CRP 186 mg/l

Das **KIS** sieht viele einzelne Werte, jeden in seinem eigenen Feld. Die **Ärztin** sieht eine möglicherweise kritisch kranke Patientin. Und ein **CDSS**? Das hängt davon ab, wie wir es bauen. (Werte fiktiv, didaktisch gewählt. Merken Sie sich: **Laktat ist nicht gemessen.**)
```

```reflect
question: "Aktivierung: Soll das System warnen? (A) „RR 96 mmHg – außerhalb des Normbereichs“, (B) „Pneumonie + Tachypnoe + Hypotonie → erhöhte Aufmerksamkeit“, (C) „Risiko für Verschlechterung: 78 %“ oder (D) gar nichts? Alle vier lassen sich technisch korrekt implementieren – aber sind sie klinisch gleich sinnvoll?"
intro: "Die vier Optionen stehen für vier Arten von Entscheidungsunterstützung:"
answers:
  - "**A** ist eine einfache **Grenzwertprüfung** – isoliert, ohne Kontext."
  - "**B** ist eine **Regel** bzw. ein **Score** – sie verknüpft mehrere Werte mit Wissen."
  - "**C** ist die Ausgabe eines **lernenden Modells** – ohne Threshold und Kalibrierung schwer zu interpretieren."
  - "**D** – nicht zu warnen – ist ebenfalls eine **Designentscheidung**, und manchmal die richtige."
```

## 1 · Was ist Clinical Decision Support?

```timeline
title: "Von Daten zur Handlung"
events:
  - when: "Daten"
    what: "RR 96"
  - when: "Information"
    what: "Hypotonie"
  - when: "Wissen"
    what: "Hypotonie + Infektion kann kritisch sein"
  - when: "Decision Support"
    what: "„Bitte klinisch prüfen“"
  - when: "Entscheidung"
    what: "ärztliche Bewertung – **hier entscheidet der Mensch**"
  - when: "Handlung"
    what: "Diagnostik / Therapie"
```

> **Arbeitsdefinition:** Ein Clinical Decision Support System verknüpft **patientenspezifische Daten** mit **medizinischem Wissen oder einem Modell** und liefert daraus **kontextbezogene** Unterstützung für klinische Entscheidungen. **Ein CDSS ist keine automatische Entscheidung.**

### Zwei Raster, ein Zoom

Im Modul [[specialized-systems]] haben wir Systeme mit dem Raster USER, DATA, WORKFLOW, INTERFACES, RISK analysiert. Ein CDSS ist ein spezieller informationsverarbeitender Workflow, in den wir hineinzoomen – das neue Raster ersetzt das alte nicht:

```include chain-de.svg
```

```match
question: "Welches Glied der CDSS-Kette ist bei Maria gemeint?"
options: ["DATA", "TRIGGER", "LOGIC", "OUTPUT", "ACTION", "FEEDBACK"]
items:
  - item: "Atemfrequenz 26, RR 96, SpO₂ 91 %"
    answer: "DATA"
  - item: "Neue Vitalwerte werden dokumentiert."
    answer: "TRIGGER"
  - item: "Eine Regel oder ein Modell bewertet die Werte."
    answer: "LOGIC"
  - item: "Ein Hinweis erscheint am Arbeitsplatz."
    answer: "OUTPUT"
  - item: "Die Ärztin prüft Maria klinisch."
    answer: "ACTION"
  - item: "Die Ärztin bestätigt oder verwirft den Hinweis."
    answer: "FEEDBACK"
```

### Welche Arten von Decision Support gibt es?

| Art | Beispiel | Wissen |
|---|---|---|
| Reminder | „Thromboseprophylaxe prüfen“ | explizit – von Menschen formuliert |
| Plausibilitätsprüfung | „Dosis zu hoch“ | explizit |
| Regel | IF A AND B THEN C | explizit |
| Score | qSOFA 2 Punkte, NEWS2 12 Punkte | explizit |
| leitlinienbasiert | „passt zu Empfehlung X“ | explizit |
| prädiktives Modell | „Risiko 78 %“ | gelernt – aus Daten abgeleitet |
| generativ / agentisch | Fall zusammenfassen, Optionen vorbereiten | gelernt |

**Nicht alles davon ist KI.** Viele etablierte CDSS im Krankenhaus sind regelbasiert – und das ist kein Makel. Mehr dazu im Thema [[topic:cdss]].

## 2 · Regeln, Leitlinien, Pathways

Die einfachste Form eines CDSS ist eine **IF–THEN-Regel** (didaktisch vereinfacht, kein klinisches Protokoll):

```text
IF   Infektionsverdacht
AND  Atemfrequenz >= 22
AND  systolischer RR <= 100
THEN „klinische Reevaluation“

# Python-Brücke
if atemfrequenz >= 22 and rr_systolisch <= 100:
    create_alert("klinische Reevaluation")
```

Die Regel ist im Kern **qSOFA** aus der Sepsis-3-Definition [@singer2016]: Atemfrequenz ≥ 22/min, systolischer Blutdruck ≤ 100 mmHg, veränderte Bewusstseinslage – je ein Punkt, ab 2 Punkten auffällig. Der **NEWS2** (Royal College of Physicians) bewertet sieben Parameter.

```quiz
question: "Wie viele qSOFA-Punkte hat Maria?"
options: ["0", "1", "2", "3"]
answer: "2"
shuffle: false  # options in a natural order
explain: "Atemfrequenz 26 ≥ 22 → 1, RR 96 ≤ 100 → 1, Bewusstsein orientiert → 0. Also 2 von 3 – auffällig."
```

```quiz
question: "Und im NEWS2 (Raumluft)? Atemfrequenz 26 → 3, SpO₂ 91 % → 3, RR 96 → 2, Herzfrequenz 112 → 2, Temperatur 39,1 °C → 2, wach und Raumluft → 0."
options: ["6", "9", "12", "15"]
answer: "12"
shuffle: false  # options in a natural order
explain: "12 Punkte – hohe Dringlichkeit."
```

```quiz
question: "Gleiche Patientin, verschiedene Scores. Was folgt daraus?"
options:
  - "Einer der beiden Scores ist falsch berechnet."
  - "Ein Score ist nur interpretierbar, wenn klar ist, welches Outcome er vorhersagen soll."
  - "Man sollte immer den Score mit der höheren Punktzahl verwenden."
answer: "Ein Score ist nur interpretierbar, wenn klar ist, welches Outcome er vorhersagen soll."
explain: "qSOFA prognostiziert schlechte Verläufe bei vermuteter Infektion, NEWS2 allgemeine klinische Verschlechterung. Die Surviving Sepsis Campaign 2021 rät davon ab, qSOFA im Vergleich zu SIRS, NEWS oder MEWS als alleiniges Sepsis-Screening zu verwenden [@evans2021] – in der Übung sehen Sie: hohe Spezifität, niedrige Sensitivität."
```

### Bausteine einer Regel – und ihr Kontext

Eine Regel besteht aus **Variable** (`egfr`), **Operator** (`<`), **Schwelle** (`60`), **Logik** (AND / OR / NOT) und **Aktion** (`create_alert()`). Mehrere Regeln werden oft als **Entscheidungstabelle** gepflegt – hier für ein renal eliminiertes Antibiotikum (didaktisch vereinfacht; die echten Grenzen stehen in der Fachinformation):

| eGFR (ml/min/1,73 m²) | Situation | Output |
|---|---|---|
| ≥ 60 | Standarddosis | kein Alert |
| 30–59 | Dosis anpassen | Hinweis |
| 15–29 | deutlich reduzieren | Warnung |
| < 15 / Dialyse | nur nach Rücksprache | Hard Stop mit Begründung |

```quiz
question: "Maria hat eine eGFR von 38. Was gibt die Entscheidungstabelle aus?"
options: ["kein Alert", "Hinweis: Dosis anpassen", "Warnung: deutlich reduzieren", "Hard Stop"]
answer: "Hinweis: Dosis anpassen"
shuffle: false  # options in a natural order
```

```reflect
question: "Und plötzlich braucht die Regel mehr. Welche Fragen muss sie beantworten, bevor sie bei Maria sicher läuft?"
answers:
  - "**Welcher Wert?** Der Kreatininwert von heute oder von vor drei Tagen?"
  - "**Akutsituation?** Bei einer akuten Nierenschädigung ist die eGFR-Formel unzuverlässig."
  - "**Geplantes?** Ist ein Kontrastmittel-CT geplant?"
  - "**Fehlender Wert?** Was tut die Regel, wenn kein Kreatinin vorliegt?"
  - "Merke: **Regel = Daten + Operatoren + Aktion – plus Kontext.**"
```

**Arzneimittelprüfung im CPOE** ist das häufigste CDSS im Krankenhaus: Eine Anordnung wird beim Signieren mit dem Patientenkontext (Allergien, eGFR 38, Metformin, Ramipril, Alter 62) und einer Wissensbasis (Interaktionen, Kontraindikationen, Dosisregeln nach Nierenfunktion) abgeglichen – in Deutschland typischerweise einer kommerziell gepflegten Arzneimitteldatenbank. Das CDSS sitzt **zwischen Verordnung und Ausführung**. Aus [[specialized-systems]] kennen Sie die Kehrseite: 49–96 % der Arzneimittelwarnungen werden übergangen [@vandersijs2006]. Die Qualität hängt weniger an der Technik als an der Wissensbasis und der Abstufung.

### Regelwerk ≠ Leitlinie: das Problem der Formalisierung

```match
question: "Leitlinie oder ausführbare Regel?"
options: ["Leitlinie", "Regel"]
items:
  - item: "narrative Evidenz"
    answer: "Leitlinie"
  - item: "Empfehlungsgrade und Ausnahmen"
    answer: "Leitlinie"
  - item: "Raum für klinische Interpretation"
    answer: "Leitlinie"
  - item: "formal und eindeutig"
    answer: "Regel"
  - item: "maschinenlesbar"
    answer: "Regel"
  - item: "testbar"
    answer: "Regel"
explain: "Damit ein System eine Leitlinie ausführen kann, muss sie **formalisiert** werden – Übersetzungsarbeit mit Interpretationsspielraum."
```

Für ausführbares Wissen gibt es eigene Sprachen: **Arden Syntax** ist der Klassiker (HL7-Standard seit den 1990ern), mit *Medical Logic Modules* aus Trigger, Logik und Aktion – fast unsere CDSS-Kette. Heute wichtiger ist **CQL** (*Clinical Quality Language*, HL7): menschenlesbar, maschinell ausführbar, für CDS und Qualitätsindikatoren, eng mit [[topic:fhir]] verbunden.

### Von der Leitlinie zum Clinical Pathway

Ein **Clinical Pathway** übersetzt eine Leitlinie in einen lokalen Behandlungspfad – über vier Ebenen: die **narrative Leitlinie** (z. B. die S3-Leitlinie zur ambulant erworbenen Pneumonie), **Entscheidungspunkte** (Schweregrad? Risiko?), **ausführbare Regeln** (z. B. mit dem CRB-65-Score) und einen **Workflow** mit Aufgaben, Terminen und Zuständigkeiten im KIS.

```timeline
title: "Pneumonie-Pfad für Maria (vereinfacht)"
events:
  - when: "1"
    what: "Verdacht"
  - when: "2"
    what: "Schweregrad"
  - when: "3"
    what: "Diagnostik"
  - when: "4"
    what: "Therapie"
  - when: "5"
    what: "Reevaluation"
```

```reflect
question: "Was heißt das für die Implementierung? Welche Fragen muss das Team klären, bevor der Pfad im KIS läuft?"
answers:
  - "Was heißt „schwer“ – welcher Score, welcher Grenzwert?"
  - "Welcher Wert, wie aktuell?"
  - "Was passiert bei einem fehlenden Wert?"
  - "Was bei einer begründeten Abweichung – und wie wird sie dokumentiert?"
  - "Ein Pathway ist **Leitlinie + lokaler Prozess**. Jede Ebene verliert Nuancen – und gewinnt Ausführbarkeit."
```

## 3 · Integration in KIS und Arbeitsplatz

Ein CDSS schwebt nicht im luftleeren Raum: Es braucht Daten aus KIS/ADT, PDMS, LIS und CPOE, muss den Patientenkontext kennen, verknüpft ihn in einer **CDSS-Engine** mit Wissensbasis oder Modell und liefert einen Output an den Arbeitsplatz. Entscheidend ist der **Trigger** – wann das System läuft. Die abstrakten Trigger unserer Kette haben reale Interoperabilitätsstandards (siehe [[communication-standards]]):

| Trigger | Beispiel bei Maria | Standard / Technik |
|---|---|---|
| nutzerausgelöst | Ärztin öffnet Marias Akte | CDS Hooks: `patient-view` |
| anordnungsausgelöst | Antibiotikum wird ausgewählt bzw. signiert | CDS Hooks: `order-select` / `order-sign` |
| ereignisausgelöst | neuer Vital- oder Laborwert | HL7-v2-Nachricht, FHIR Subscription |
| zeitausgelöst | Reevaluation nach 6 Stunden | Scheduler, Aufgabe im Workflow |

### Die „Five Rights“ und die Eskalationsstufe

Der Standardrahmen für die Integration sind die **Five Rights of CDS** (Osheroff et al. 2012): die richtige **Information** an die richtige **Person** im richtigen **Format** über den richtigen **Kanal** zum richtigen **Zeitpunkt**.

```match
question: "Welches „Right“ ist bei Marias Dosiswarnung gemeint?"
options: ["Information", "Person", "Format", "Kanal", "Zeitpunkt"]
items:
  - item: "eGFR 38 → Dosis anpassen"
    answer: "Information"
  - item: "die verordnende Ärztin – nicht alle"
    answer: "Person"
  - item: "Hinweis mit Begründung und Dosisvorschlag"
    answer: "Format"
  - item: "im CPOE-Dialog, nicht per E-Mail"
    answer: "Kanal"
  - item: "beim Auswählen, nicht beim Entlassbrief"
    answer: "Zeitpunkt"
```

Dann die **Eskalationsstufe**: *Info* („Kreatinin erhöht.“), *Warnung* („Dosisanpassung prüfen.“), *Empfehlung* („Aufgrund von X und Y Dosis Z erwägen.“), *Hard Stop* (die Anordnung kann nicht abgeschlossen werden). CDS Hooks bildet das mit dem Card-Indikator `info`, `warning`, `critical` ab. **Gleiche Logik, unterschiedliche Wirkung:** Die Eskalationsstufe ist eine **Governance-Entscheidung** (z. B. Arzneimittelkommission, CDS-Gremium mit Klinik, Pharmazie und Informatik), nicht nur eine technische.

```match
question: "Aktivierung: Wann und wie eingreifen? Welcher Trigger und welche Stufe passen?"
options:
  - "order-select · Hinweis/Warnung mit Dosisvorschlag"
  - "Ereignis (neues Laborergebnis) · Warnung an das zuständige Team"
  - "order-sign · Hard Stop, Übersteuern nur mit Begründung"
  - "patient-view bzw. Aufnahmeworkflow · Info/Reminder"
items:
  - item: "Für Maria wird ein renal eliminiertes Antibiotikum ausgewählt, eGFR 38."
    answer: "order-select · Hinweis/Warnung mit Dosisvorschlag"
  - item: "Bei Maria trifft ein neuer Laktatwert von 4,2 mmol/l ein."
    answer: "Ereignis (neues Laborergebnis) · Warnung an das zuständige Team"
  - item: "Penicillin-Allergie mit Anaphylaxie dokumentiert – Amoxicillin wird signiert."
    answer: "order-sign · Hard Stop, Übersteuern nur mit Begründung"
  - item: "Bei Aufnahme ist keine Thromboseprophylaxe verordnet."
    answer: "patient-view bzw. Aufnahmeworkflow · Info/Reminder"
explain: "Im Modul [[specialized-systems]] ging es um die Stufe – jetzt zusätzlich um Logik und Zeitpunkt. Ein Laktat über 4 mmol/l ist klinisch relevant; die Warnung gehört an das zuständige Team, nicht an alle."
```

## 4 · Qualität und Validierung

Ein CDSS kann auf **zwei Arten** falsch sein:

| | Patient:in verschlechtert sich | bleibt stabil |
|---|---|---|
| **Alert** | **TP** richtig positiv – Alert, und Maria wird tatsächlich kritisch | **FP** falsch positiv – unnötige Unterbrechung, Alarmmüdigkeit |
| **kein Alert** | **FN** falsch negativ – kritischer Verlauf übersehen | **TN** richtig negativ – kein Alert, stabil: der Normalfall |

```reflect
question: "Bei einem Screening auf Verschlechterung: Welchen Fehler würden Sie eher akzeptieren – und gilt das auch bei 30 Fehlalarmen pro Schicht?"
answers:
  - "Meist lautet die erste Antwort: lieber falsch positiv als einen kritischen Verlauf übersehen."
  - "Bei 30 Fehlalarmen pro Schicht kippt das: Alarmmüdigkeit führt dazu, dass auch echte Alarme übersehen werden."
  - "Es gibt **keine pauschale Antwort** – sie hängt von den Folgen des Übersehens und von den Ressourcen ab. **Jede Entscheidung für weniger FN kauft man mit mehr FP – und umgekehrt.**"
```

### Sensitivität, Spezifität, PPV an 100 Patient:innen

20 von 100 Patient:innen verschlechtern sich. Das System erkennt 18 (TP), übersieht 2 (FN), alarmiert bei 8 Stabilen (FP) und lässt 72 in Ruhe (TN).

```match
question: "Ordnen Sie Kennzahl, Frage und Ergebnis zu."
options: ["Sensitivität = 18/20 = 90 %", "Spezifität = 72/80 = 90 %", "PPV = 18/26 = 69 %"]
items:
  - item: "Wie viele Kranke findet das System? TP / (TP + FN)"
    answer: "Sensitivität = 18/20 = 90 %"
  - item: "Wie viele Gesunde lässt es in Ruhe? TN / (TN + FP)"
    answer: "Spezifität = 72/80 = 90 %"
  - item: "Wie oft stimmt ein Alert? TP / (TP + FP)"
    answer: "PPV = 18/26 = 69 %"
explain: "Für die Station zählt der **PPV**: Wie viele Alerts lohnen sich?"
```

```quiz
question: "Gleiches System (Sensitivität 90 %, Spezifität 90 %), aber nur 2 % Prävalenz: 1.000 Patient:innen, 20 verschlechtern sich. Wie hoch ist der PPV?"
options: ["etwa 16 %", "etwa 50 %", "etwa 69 %", "etwa 90 %"]
answer: "etwa 16 %"
shuffle: false  # options in a natural order
explain: "18 richtige Alerts (90 % von 20) und 98 Fehlalarme (10 % von 980): 18 / 116 ≈ 16 %. Fünf von sechs Alerts sind Fehlalarme. Bei seltenen Ereignissen sind die meisten Alerts Fehlalarme – **Alert-Fatigue ist auch Mathematik.** Deshalb muss ein CDSS immer in der Zielpopulation bewertet werden."
```

### Der Threshold verändert das System

Ein Modell liefert ein Risiko zwischen 0 und 1 – erst der **Threshold** macht daraus einen Alert. Die Zahlen stammen aus dem synthetischen Übungsdatensatz (Klinik A, Testdaten, n = 600, logistische Regression):

| Threshold | Charakter | Sensitivität | PPV | Alerts pro 100 Pat. |
|---|---|---|---|---|
| 0,2 | viele Alerts, wenig übersehen | 68 % | 39 % | 30 |
| 0,5 | Kompromiss | 27 % | 60 % | 8 |
| 0,8 | wenige Alerts, viel übersehen | 7 % | 70 % | 2 |

```quiz
question: "Wer sollte über den Threshold entscheiden?"
options:
  - "Die Data Scientists – er ist eine rein mathematische Optimierung."
  - "Klinik, Pflege, Qualitätsmanagement und Informatik gemeinsam – er hängt davon ab, wie viele Alerts eine Station bewältigt und was ein übersehener Fall kostet."
  - "Der Hersteller – er ist im Produkt fest eingestellt."
answer: "Klinik, Pflege, Qualitätsmanagement und Informatik gemeinsam – er hängt davon ab, wie viele Alerts eine Station bewältigt und was ein übersehener Fall kostet."
explain: "Der Threshold ist keine rein mathematische Entscheidung, sondern eine klinische und organisatorische. Genau das üben Sie in der Übung."
```

### Diskrimination und Kalibrierung

```match
question: "Diskrimination oder Kalibrierung?"
options: ["Diskrimination (AUC)", "Kalibrierung"]
items:
  - item: "Ordnet das Modell Patient:innen mit Ereignis höher ein als solche ohne?"
    answer: "Diskrimination (AUC)"
  - item: "Bedeutet ein angezeigtes Risiko von 30 % wirklich, dass 3 von 10 solcher Patient:innen das Ereignis haben?"
    answer: "Kalibrierung"
  - item: "misst die Rangfolge"
    answer: "Diskrimination (AUC)"
  - item: "vergleicht vorhergesagte mit beobachteten Risiken"
    answer: "Kalibrierung"
explain: "In den Übungsdaten hat das in Klinik A trainierte Modell in A und B je eine AUC von 0,80 – in B werden aber im Mittel 19,7 % vorhergesagt und nur 8,6 % beobachtet. **Die Rangfolge stimmt, die Zahl nicht.** Für eine Ärztin, die „40 %“ liest, ist das ein großer Unterschied."
```

### Auch eine Regel kann falsch sein

Validierung ist nicht nur ein ML-Thema. Regelbasierte CDSS werden validiert **wie Software – plus Pflege der Wissensbasis**:

```text
# Referenzfälle
assert cds_alert(af=26, rr=96) == True
assert cds_alert(af=18, rr=125) == False
# Grenzwert
assert cds_alert(af=22, rr=100) == True
```

**Regressionstest:** Ändere ich Regel B, darf Regel A nicht still kaputtgehen – alle Tests laufen bei jeder Änderung der Wissensbasis erneut.

```match
question: "Auf welcher Ebene wird die Regel geprüft?"
options: ["Logik korrekt?", "Wissen korrekt?", "Wissen aktuell?", "Im Workflow sinnvoll?"]
items:
  - item: "Unit-Tests und Referenzfälle"
    answer: "Logik korrekt?"
  - item: "Abgleich mit Leitlinie, Fachinformation, Score-Definition"
    answer: "Wissen korrekt?"
  - item: "Versionierung, Update-Prozess, benannte Verantwortliche"
    answer: "Wissen aktuell?"
  - item: "Override-Rate, Alert-Frequenz, Akzeptanz"
    answer: "Im Workflow sinnvoll?"
```

### Von interner zu externer Validierung – und weiter

Generalisierung kennen Sie aus der KI-Einführung; klinisch wird daraus eine Stufenfolge. Die meisten publizierten Modelle kommen nie über Stufe 2 hinaus.

```timeline
title: "Validierungsstufen (Beispiel)"
events:
  - when: "1 · Training"
    what: "z. B. Dresden"
  - when: "2 · Interne Validierung"
    what: "Dresden, neue Patient:innen"
  - when: "3 · Externe Validierung"
    what: "ein anderes Haus, z. B. Leipzig"
  - when: "4 · Prospektive Evaluation"
    what: "im realen Workflow"
  - when: "5 · Klinischer Nutzen"
    what: "Verbessert sich die Versorgung?"
```

```match
question: "Welche Berichtsleitlinie gilt wofür?"
options: ["TRIPOD+AI (2024)", "DECIDE-AI (2022)", "CONSORT-AI (2020)"]
items:
  - item: "Entwicklung und Validierung von Vorhersagemodellen, auch mit Machine Learning"
    answer: "TRIPOD+AI (2024)"
  - item: "frühe klinische Evaluation KI-basierter Entscheidungsunterstützung"
    answer: "DECIDE-AI (2022)"
  - item: "randomisierte Studien mit einer KI-Intervention"
    answer: "CONSORT-AI (2020)"
explain: "Siehe [@collins2024] und [@vasey2022]."
```

**Gute Performance ist noch kein klinischer Nutzen.** Vier Stufen, jede braucht eine andere Studie: **Modell-Performance** (erkennt das Modell Muster? AUC, Sensitivität, PPV), **klinische Validität** (ist der Zusammenhang plausibel – richtige Zielgröße, keine Leakage?), **klinischer Nutzen** (verändert es Entscheidungen sinnvoll – Workflow, Akzeptanz, Reaktionszeit?) und **Patienten-Outcome** (geht es Patient:innen besser – Mortalität, Komplikationen, Liegedauer?). Auch die Evidenz hat Stufen: **Modell-Evaluation ≠ Impact-Evaluation ≠ kausale Evidenz.** Ein Modell kann statistisch hervorragend und klinisch nutzlos sein. Siehe auch [[topic:data-quality]].

## 5 · Was bei echten Systemen passiert

| | Regel | Machine Learning |
|---|---|---|
| Entscheidungsfunktion | Mensch definiert f(x): `AF >= 22 AND RR <= 100` | Modell lernt f(x) aus Beispielen: `model.fit(X, y)` |
| Wissen | explizit | aus Daten gelernt |
| Nachvollziehbarkeit | meist hoch | variabel |
| Anpassung | manuell, versioniert | Retraining, Rekalibrierung |
| Datenbedarf | gering | hoch |
| außerhalb bekannter Fälle | starr | flexibler, aber unsicher |

Nicht „alt gegen modern“, sondern unterschiedliche Werkzeuge – **viele gute Systeme sind hybrid**.

```match
question: "Aktivierung: Regel, ML oder beides?"
options: ["Regel", "ML", "Kombination"]
items:
  - item: "bekannte Arzneimittelallergie prüfen"
    answer: "Regel"
  - item: "Lungenrundherd im CT detektieren"
    answer: "ML"
  - item: "Tageshöchstdosis überwachen"
    answer: "Regel"
  - item: "Verschlechterungsrisiko aus 40 zeitabhängigen Variablen"
    answer: "Kombination"
explain: "Allergie und Höchstdosis sind eindeutiges, explizites Wissen. Ein Rundherd im CT ist hochdimensionale Eingabe, schwer als Regel formulierbar. Für das Verschlechterungsrisiko liefert meist ein Modell das Risiko, Regeln übernehmen Plausibilität, harte Ausschlüsse und die Alert-Logik – genau so bauen Sie es in der Übung."
```

### Breit implementiert – ist es damit validiert?

```case
**Epic Sepsis Model:** ein proprietäres Sepsis-Vorhersagemodell eines großen EHR-Herstellers, in Hunderten US-Kliniken im Einsatz. Externe Validierung an Michigan Medicine: 38.455 Hospitalisierungen, 7 % mit Sepsis [@wong2021].
```

```match
question: "Was ergab die externe Validierung?"
options: ["0,63", "18 %", "67 %"]
items:
  - item: "AUC in der externen Validierung"
    answer: "0,63"
  - item: "Anteil aller Hospitalisierungen, die einen Alert auslösten"
    answer: "18 %"
  - item: "Anteil der Sepsisfälle, die trotzdem nicht erkannt wurden"
    answer: "67 %"
explain: "**Verbreitung ist keine Evidenz.** Interne Herstellerzahlen ersetzen keine unabhängige externe Validierung. Hier kommt alles aus dem Validierungsblock zusammen: Diskrimination, PPV, Alert-Last, externe Validierung."
```

**TREWS** ist das Gegenbeispiel: ein ML-basiertes Frühwarnsystem, prospektiv an fünf Kliniken im realen Betrieb untersucht – 590.736 überwachte Patient:innen, Analyse von 6.877 Sepsisfällen, bei denen der Alert vor der Antibiotikagabe auslöste [@adams2022].

```quiz
question: "Wurde der TREWS-Alert innerhalb von 3 Stunden ärztlich bestätigt, war die Krankenhaussterblichkeit adjustiert um 3,3 Prozentpunkte niedriger. Welche Formulierung ist korrekt?"
options:
  - "„TREWS senkte die Sterblichkeit um 3,3 Prozentpunkte.“"
  - "„Eine rasche Bestätigung des TREWS-Alerts war mit einer um 3,3 Prozentpunkte niedrigeren Sterblichkeit assoziiert.“"
  - "„TREWS ist kausal wirksam, weil 590.736 Patient:innen untersucht wurden.“"
answer: "„Eine rasche Bestätigung des TREWS-Alerts war mit einer um 3,3 Prozentpunkte niedrigeren Sterblichkeit assoziiert.“"
explain: "Eine **Kohortenstudie** zeigt einen Zusammenhang, keinen kausalen Effekt. TREWS liegt zwischen Modell-Evaluation und kausaler Evidenz (RCT): bei der Impact-Evaluation."
```

### Bilddiagnostik: Was hat das Modell eigentlich gelernt?

Zech et al. trainierten Pneumonie-Klassifikatoren (CNN) auf 158.323 Thorax-Röntgenaufnahmen aus drei Kliniksystemen [@zech2018]. Das CNN konnte die **Herkunftsklinik** fast perfekt erkennen – bei NIH-Aufnahmen zu 99,95 %. Da die Pneumonie-Prävalenz zwischen den Kliniken extrem verschieden war (34 % gegenüber rund 1 %), erreichte **schon das Sortieren nach Klinik eine AUC von 0,86** – ohne die Lunge anzuschauen.

```quiz
question: "Wie nennt man dieses Phänomen?"
options: ["Overfitting auf das Rauschen", "Shortcut Learning", "Automation Bias"]
answer: "Shortcut Learning"
explain: "Das Modell nutzt Merkmale, die mit dem Label korrelieren – Gerät, Marker, Klinik –, aber nicht die Krankheit selbst. **Das Modell lernt etwas – aber vielleicht nicht das, was wir glauben.** Folge: in der eigenen Klinik gut, in der nächsten deutlich schlechter. Eine Form von Dataset Shift."
```

### Sechs bekannte Fehlerquellen

```match
question: "Welche Fehlerquelle ist es?"
options: ["Sampling Bias", "Label Bias", "Data Leakage", "Missingness", "Dataset Shift", "Automation Bias"]
items:
  - item: "trainiert an einer Uniklinik, eingesetzt im Kreiskrankenhaus"
    answer: "Sampling Bias"
  - item: "„Sepsis“ ist als abgerechneter Code definiert statt über den klinischen Verlauf"
    answer: "Label Bias"
  - item: "„Antibiotikum gegeben“ wird als Prädiktor verwendet"
    answer: "Data Leakage"
  - item: "„Laktat nicht gemessen“ bedeutet für das Modell: vermutlich gesund"
    answer: "Missingness"
  - item: "Klinik B hat eine andere Population, andere Geräte, andere Prozesse und eine andere Prävalenz"
    answer: "Dataset Shift"
  - item: "„Das System hat nicht gewarnt, also ist alles gut.“"
    answer: "Automation Bias"
explain: "Real belegt: Schon die Tatsache, dass ein Labortest angeordnet wurde, war bei 86 % von 272 Tests mit dem Überleben assoziiert [@agniel2018] – ein Modell kann Dokumentationsverhalten lernen statt Krankheit. Zum Dataset Shift siehe [@finlayson2021]. Leakage und Missingness finden Sie in der Übung wieder – erinnern Sie sich an Marias fehlendes Laktat."
```

### Wenn ein Modell scheinbar weiter funktioniert

Das gefährlichste Szenario ist kein Absturz, sondern ein Modell, das **scheinbar weiter funktioniert** (Werte illustrativ): 2026 AUC 0,88, kalibriert, PPV 40 %; 2028 AUC 0,87 – aber die Population hat sich verändert, die Risiken werden überschätzt, der PPV liegt bei 22 %.

```reflect
question: "Ist das Modell 2028 noch gut? Was sollte nach dem Go-live überwacht werden?"
answers:
  - "**Nein** – die AUC ist fast gleich, aber die Risiken stimmen nicht mehr, der PPV sinkt, die Alert-Last steigt."
  - "**Performance:** Sensitivität und PPV gegen spätere Outcomes"
  - "**Kalibrierung:** vorhergesagt vs. beobachtet"
  - "**Daten-Drift:** Verteilungen der Eingangsdaten"
  - "**Alert-Frequenz** (pro Patient:in und Schicht) und **Override-Rate**"
  - "**Outcomes:** Geht es Patient:innen besser?"
  - "Ein CDSS ist nach dem Go-live nicht fertig – **FEEDBACK ist ein Dauerprozess.**"
```

## 6 · Regulierung: MDR und AI Act

Regulierung ist kein juristischer Anhang, sondern die logische letzte Frage: Wer legt fest, welche Evidenz, Qualitätssicherung und Kontrolle nötig sind? Die entscheidende Frage lautet **nicht „Ist es KI?“, sondern: Wofür ist die Software bestimmt?** – die **Zweckbestimmung** durch den Hersteller (siehe auch [[topic:privacy-ethics]]).

```match
question: "Medizinprodukt-Software (MDSW) oder nicht?"
options: ["kein medizinischer Zweck", "reine Informationsverwaltung – meist kein Medizinprodukt", "bei medizinischer Zweckbestimmung MDSW"]
items:
  - item: "Terminverwaltung, Abrechnung"
    answer: "kein medizinischer Zweck"
  - item: "Medikationsliste anzeigen"
    answer: "reine Informationsverwaltung – meist kein Medizinprodukt"
  - item: "Dosisprüfung, Risikoscore, Sepsis-Alert"
    answer: "bei medizinischer Zweckbestimmung MDSW"
```

Für MDSW greift typischerweise **Regel 11 der MDR** (Anhang VIII; vgl. MDCG 2019-11): grundsätzlich **Klasse IIa**; **IIb**, wenn eine falsche Information zu einer schwerwiegenden Verschlechterung oder einem chirurgischen Eingriff führen kann; **III** bei möglichem Tod oder irreversibler Verschlechterung. Software zur Überwachung von Vitalparametern mit unmittelbarer Gefahr ist IIb, sonstige Software Klasse I. Ab Klasse IIa ist eine **Benannte Stelle** beteiligt. **Funktion + Zweck + potenzieller Schaden bestimmen die Klassifikation.**

```match
question: "Welche Klasse nach MDR-Regel 11?"
options: ["IIa", "IIb", "III"]
items:
  - item: "Grundfall: Software liefert Informationen für diagnostische oder therapeutische Entscheidungen"
    answer: "IIa"
  - item: "Eine falsche Information kann zu einer schwerwiegenden Verschlechterung oder einem chirurgischen Eingriff führen"
    answer: "IIb"
  - item: "Eine falsche Information kann zum Tod oder einer irreversiblen Verschlechterung führen"
    answer: "III"
```

**MDR und AI Act sind zwei Achsen.** Die MDR fragt nach dem **medizinischen Zweck** und der Gefahr durch falsche Information (→ Klasse, Konformitätsbewertung, klinische Bewertung). Der AI Act fragt, ob es ein **KI-System** ist und in welche **Risikokategorie** es fällt (→ u. a. Datenqualität, Dokumentation, menschliche Aufsicht). KI in Medizinprodukten, die eine Benannte Stelle brauchen, gilt als Hochrisiko-KI (Art. 6 Abs. 1).

```timeline
title: "Zeitplan des AI Act (Stand November 2026, geändert durch das Digital Omnibus on AI)"
events:
  - when: "01.08.2024"
    what: "Inkrafttreten"
  - when: "02.02.2025"
    what: "Verbote"
  - when: "02.08.2025"
    what: "Pflichten für General-Purpose-AI-Modelle"
  - when: "02.08.2026"
    what: "allgemeine Anwendung"
  - when: "02.12.2027"
    what: "Hochrisiko-KI nach Anhang III"
  - when: "02.08.2028"
    what: "Hochrisiko-KI nach Anhang I – u. a. Medizinprodukte"
```

```quiz
question: "Ein KI-basiertes Medizinprodukt braucht eine Benannte Stelle. Was gilt?"
options:
  - "Nur die MDR – der AI Act gilt nicht für Medizinprodukte."
  - "Nur der AI Act – er ersetzt die MDR für KI."
  - "Beide: die MDR-Pflichten unverändert, die Hochrisiko-Pflichten des AI Act ab dem 2. August 2028."
answer: "Beide: die MDR-Pflichten unverändert, die Hochrisiko-Pflichten des AI Act ab dem 2. August 2028."
explain: "**MDR fragt nach dem medizinischen Produkt. AI Act fragt nach dem KI-Risiko.**"
```

### Eigenherstellung – und das CDSS aus der Übung

Für die Universitätsmedizin besonders relevant: Nach **Art. 5 Abs. 5 MDR** dürfen Gesundheitseinrichtungen Produkte selbst herstellen und intern verwenden – u. a. wenn keine Weitergabe an eine andere juristische Person erfolgt, ein angemessenes Qualitätsmanagementsystem besteht, begründet ist, dass kein gleichwertiges Marktprodukt den Bedarf deckt, die grundlegenden Sicherheits- und Leistungsanforderungen erfüllt sind und Dokumentation, eine öffentliche Erklärung sowie die Auswertung der Erfahrungen vorliegen.

```reflect
question: "In der Übung bauen Sie ein CDSS in einem Jupyter-Notebook. Ist das ein Medizinprodukt? Und wann müsste man die Frage neu stellen?"
answers:
  - "**Nein** – das Notebook dient ausschließlich Lehre und Forschung und hat **keine medizinische Zweckbestimmung**. Eine logistische Regression zu schreiben, macht noch kein Medizinprodukt."
  - "**Sobald** Software vom Hersteller für einen medizinischen Zweck bestimmt wird, muss ihre regulatorische Einordnung geklärt werden – **bevor** sie klinisch eingesetzt wird."
  - "Viele CDSS entstehen im eigenen Haus: Eigenherstellung ist **keine Ausnahme von Qualität, sondern ein eigener Rahmen dafür**."
```

## Synthese: Ein CDSS ist mehr als ein Algorithmus

```match
question: "Welche Prüffrage gehört zu welchem Glied der Kette?"
options: ["DATA", "TRIGGER", "LOGIC", "OUTPUT", "ACTION", "FEEDBACK"]
items:
  - item: "Sind die Daten richtig, aktuell und zum Zeitpunkt verfügbar?"
    answer: "DATA"
  - item: "Wird das System im richtigen Moment aktiv?"
    answer: "TRIGGER"
  - item: "Ist die Regel bzw. das Modell valide und kalibriert?"
    answer: "LOGIC"
  - item: "Ist die Empfehlung verständlich und richtig abgestuft?"
    answer: "OUTPUT"
  - item: "Kann die Nutzerin sinnvoll reagieren?"
    answer: "ACTION"
  - item: "Wissen wir, ob das System geholfen hat?"
    answer: "FEEDBACK"
```

> **Ein Algorithmus wird erst durch Daten, Workflow, Validierung, Nutzerinteraktion und Governance zu einem klinischen Entscheidungsunterstützungssystem.**

## Take-home Messages

1. **Ein CDSS verknüpft Patientendaten mit Wissen oder einem Modell.** Nicht alles ist KI – viele etablierte klinische CDSS sind regelbasiert.
2. **Integration entscheidet über die Wirkung:** richtige Information, Person, Format, Kanal, Zeitpunkt.
3. **Validierung heißt mehr als AUC:** PPV, Threshold, Kalibrierung, externe und prospektive Evaluation.
4. **Echte Systeme scheitern an Daten und Betrieb:** Leakage, Shift, Missingness, Automation Bias – Monitoring ist Pflicht.
5. **Zweckbestimmung und Risiko bestimmen die Regulierung:** MDR Regel 11; AI-Act-Hochrisiko für Medizinprodukte ab 2. August 2028.

## Ausblick: die Übung

In der Übung bauen Sie die Kette selbst: eine qSOFA-artige **Regel** mit `assert`-Tests, eine **logistische Regression** mit `predict_proba()`, die Wahl eines **Thresholds** unter einer realistischen Alert-Grenze, die **Konfusionsmatrix**, eine verdächtig gute Variable (**Leakage**) und fehlendes Laktat (**Missingness**), den externen Test in **Klinik B** mit Kalibrierungskurve – und am Ende die CDSS-Kette und die Zweckbestimmung für Ihr System. Der Datensatz ist vollständig synthetisch; das Outcome ist eine didaktisch definierte Verschlechterung innerhalb von 6 Stunden, keine Sepsisdiagnose.

## Selbsttest

```quiz
question: "Ein System hat 90 % Sensitivität und 90 % Spezifität. Warum können trotzdem die meisten Alerts Fehlalarme sein?"
options:
  - "Weil die Sensitivität falsch berechnet ist"
  - "Weil der PPV von der Prävalenz abhängt – bei seltenen Ereignissen überwiegen Fehlalarme"
  - "Weil die Spezifität nur für gesunde Patient:innen gilt"
answer: "Weil der PPV von der Prävalenz abhängt – bei seltenen Ereignissen überwiegen Fehlalarme"
```

```quiz
question: "Ein Modell hat in Klinik B dieselbe AUC wie in Klinik A, überschätzt aber jedes Risiko. Was ist das Problem?"
options: ["die Diskrimination", "die Kalibrierung", "die Sensitivität"]
answer: "die Kalibrierung"
```

```quiz
question: "Was entscheidet darüber, ob eine CDSS-Software ein Medizinprodukt ist?"
options:
  - "ob sie KI verwendet"
  - "ihre Zweckbestimmung durch den Hersteller"
  - "wie viele Patient:innen sie nutzen"
answer: "ihre Zweckbestimmung durch den Hersteller"
```
