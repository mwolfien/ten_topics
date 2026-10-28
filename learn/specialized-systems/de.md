---
title: "Spezialisierte klinische Systeme – vom Arbeitsplatz bis zur Biobank"
summary: "Was passiert innerhalb spezialisierter Systeme? Wir begleiten Herrn Krause von der Anordnung über das Tumorboard, die Operation und die erste Nacht auf der Intensivstation bis zur Biobank – und analysieren jedes System mit demselben 5-Fragen-Raster."
duration_minutes: 60
level: "Vertiefung"
audiences: [med, cs, clin, tech, pat]
order: 5
builds_on: [information-systems, therapy]
course: his
lecture: 3
author: "Markus Wolfien"
objectives:
  - "Die Rolle von klinischem Arbeitsplatz und CPOE für Anordnungen und Medikation erklären"
  - "Beschreiben, wie ein Tumorboard heterogene Daten zu einer dokumentierten Empfehlung zusammenführt"
  - "OP-Management als Planung knapper, voneinander abhängiger Ressourcen einordnen"
  - "Die Besonderheiten kontinuierlicher Daten im PDMS (Geräte, Zeitreihen, Alarme) erläutern"
  - "Erklären, wie Proben, Einwilligung und Pseudonymisierung Versorgung und Forschung verbinden"
  - "Beliebige klinische Informationssysteme mit dem 5-Fragen-Raster analysieren"
readings: [winter2023, bates1998, vandersijs2006, haynes2009, sendelbach2013]
related_topics: [ehr-cis, cdss, data-provenance, privacy-ethics, data-sharing, visualizations]
source: "Vorlesung 3 „Spezialisierte klinische Systeme vom Arbeitsplatz bis zur Biobank“, Informationssysteme im Gesundheitswesen (WiSe 2026/27), Markus Wolfien, IMB & ZMI"
---

> **Leitfrage:** Wie unterstützen spezialisierte klinische Systeme konkrete Arbeit, Entscheidungen und Therapieprozesse?

Im Modul [[information-systems]] haben Sie die Systemlandschaft eines Krankenhauses kennengelernt: wie KIS, LIS und RIS/PACS über ADT, Order/Result und den Kommunikationsserver zusammenhängen. Diese Infrastruktur setzen wir jetzt voraus und **zoomen hinein**: Was passiert *innerhalb* spezialisierter Systeme – und wie unterstützen sie die Arbeit am Patienten?

```persona med
Sie werden Anordnungen schreiben, Fälle im Tumorboard vorstellen und Patient:innen auf die Intensivstation übergeben. Dieses Modul zeigt, welches System dabei welche Arbeit übernimmt – und wo es Sie warnt, aufhält oder in die Irre führen kann.
```

```persona cs
Rollenbasierte Rechte, Regelwerke, Zustandsautomaten, Zeitreihen, Pseudonymisierung: Spezialisierte klinische Systeme sind angewandte Informatik. Spannend ist, wie diese Konzepte unter Zeitdruck und mit Patientensicherheit als Randbedingung funktionieren müssen.
```

```persona clin
Alert-Fatigue, Alarmmüdigkeit, fehlende Befunde im Board, kein Intensivbett: Vieles davon kennen Sie aus dem Alltag. Hier sehen Sie, welche Ursachen in der Gestaltung der Systeme liegen – und was sich daran ändern lässt.
```

```persona tech
Ein Geräte-Gateway am Kommunikationsserver vorbei, ein nächtlicher Export statt einer Live-Anbindung, eine Treuhandstelle als eigenes System: Das Modul zeigt, warum Integrations- und Betriebsentscheidungen direkt klinische Folgen haben.
```

```persona pat
Warum wird Ihr Armband vor jeder Medikamentengabe gescannt? Wer entscheidet im Tumorboard über Ihre Behandlung? Und was passiert mit Gewebe, das Sie für die Forschung spenden? Dieses Modul gibt Antworten – auch zu Ihrem Recht, eine Einwilligung zu widerrufen.
```

```case
**Herr Peter Krause, 62 Jahre** (*14.05.1964) – der Patient aus dem Modul [[therapy]]. Er raucht seit über 25 Jahren (ca. 30 Packungsjahre); im Niedrigdosis-CT des Lungenkrebs-Screenings zeigt sich ein **Rundherd von 2,6 cm im rechten Oberlappen**. Vorerkrankungen: Vorhofflimmern, Diabetes Typ 2, Hypertonie. Dauermedikation: **Apixaban**, Metformin, Ramipril.

Der Fall ist fiktiv und medizinisch vereinfacht. Uns interessiert, welches System welchen Teil seiner Daten verwaltet.
```

```timeline
title: "Herrn Krauses Weg durch die Systeme"
events:
  - when: "Woche 2"
    what: "Stationäre Abklärung: Bronchoskopie und Biopsie – **Arbeitsplatz & CPOE**"
  - when: "Woche 3"
    what: "Histologie: Adenokarzinom · Staging cT1c cN0 cM0"
  - when: "Woche 4"
    what: "Thorax-Tumorboard empfiehlt eine Lobektomie – **Tumorboard**"
  - when: "Woche 5"
    what: "Minimalinvasive Lobektomie rechts oben (VATS) – **OP-Management**"
  - when: "Woche 5"
    what: "Erste Nacht auf der Intensivstation – **PDMS**"
  - when: "Woche 5"
    what: "Tumorgewebe mit Einwilligung in die Biobank – **Biobank**"
```

### Das Werkzeug: das 5-Fragen-Raster

Statt Systeme auswendig zu lernen, stellen wir an jedes dieselben fünf Fragen. Wer das Raster beherrscht, kann auch Systeme analysieren, die hier nicht vorkommen – etwa Pathologie-, Notaufnahme- oder Pflegesysteme.

| | Frage |
|---|---|
| **USER** | Wer arbeitet mit dem System und in welcher Rolle? |
| **DATA** | Welche Daten entstehen, welche werden gebraucht? |
| **WORKFLOW** | Welchen Arbeitsablauf bildet das System ab? |
| **INTERFACES** | Mit welchen Systemen muss es Daten austauschen? |
| **RISK** | Was kann schiefgehen – und mit welchen Folgen? |

## 1 · Klinischer Arbeitsplatz & CPOE: von der Entscheidung zum Auftrag

Für die Nutzer:innen ist „das KIS“ kein Kasten im Architekturbild, sondern ein **Arbeitsplatz**. Dieselbe Akte erscheint je nach Rolle anders:

| Rolle | sieht und bearbeitet vor allem |
|---|---|
| Ärztin / Arzt | Befunde, Anordnungen, Verlauf, Arztbrief |
| Pflege | Kurve, Maßnahmen, Vitalzeichen, Pflegeplanung |
| Apotheke | Medikationsprüfung, Interaktionen, Unit-Dose |
| Stationsleitung | Belegung, Personal, offene Aufgaben |

Rollen bestimmen auch **Rechte**: Wer darf anordnen, wer freigeben? Technisch ist das ein **rollenbasiertes Berechtigungskonzept** (*Role-Based Access Control*, RBAC): Rechte hängen nicht an Personen, sondern an Rollen, und Personen erhalten Rollen. Der Kopfbalken mit Name, Geburtsdatum und Station ist der ADT-Kontext aus der letzten Vorlesung – sichtbar auf jedem Bildschirm, damit niemand in der falschen Akte arbeitet. Mehr dazu im Thema [[topic:ehr-cis]].

**CPOE** (*Computerized Physician Order Entry*) heißt: Die Ärztin ordnet direkt und **strukturiert** im System an – nicht auf Papier und nicht mündlich an die Pflege, die es dann abtippt. Eine Anordnung ist ein Objekt mit Feldern: *was, für wen, wann, wie dringlich, warum*. Deshalb kann das System prüfen, bevor der Auftrag an die Leistungsstelle geht; was danach passiert, ist das Order/Result-Muster aus [[information-systems]].

```case
Herrn Krauses Anordnungen am Aufnahmetag: **Bronchoskopie mit EBUS-Biopsie** (dringlich, Fragestellung: Histologie Rundherd rechts) · **Lungenfunktion** inkl. Diffusion vor möglicher Resektion · **Labor**: Blutbild, Gerinnung, Kreatinin vor dem Eingriff · **Apixaban pausieren**, 48 h vor der Biopsie (nach lokaler SOP).
```

```quiz
question: "Um wie viel sanken nicht abgefangene schwere Medikationsfehler in der klassischen Studie nach Einführung von CPOE?"
options: ["um etwa 15 %", "um etwa 55 %", "um etwa 95 %", "gar nicht – nur die Dokumentation wurde schneller"]
answer: "um etwa 55 %"
explain: "Von 10,7 auf 4,86 pro 1000 Patiententage [@bates1998]. CPOE wirkt vor allem durch **Struktur und Prüfungen**, nicht durch das Tippen an sich."
```

### Medikation als geschlossener Kreislauf

Medikation ist der wichtigste Anwendungsfall von CPOE. Geschlossen ist der Kreislauf nur, wenn alle Schritte digital **über dieselben IDs** verbunden sind – dieselbe Logik wie der Barcode im Labor. Jeder Medienbruch (abschreiben, umrechnen, stellen) ist eine Fehlerquelle. Bei der Gabe prüft die Pflege die **5 R**: richtige Patient:in, richtiges Arzneimittel, richtige Dosis, richtiger Applikationsweg, richtiger Zeitpunkt – der Scan von Armband und Arzneimittel unterstützt sie technisch. In Deutschland wurde digitales Medikationsmanagement u. a. über das Krankenhauszukunftsgesetz (KHZG) gefördert.

```include medication-loop-de.svg
```

### Entscheidungsunterstützung und ihre Kehrseite

Strukturierte Anordnungen ermöglichen Entscheidungsunterstützung ([[topic:cdss]]): **Hinweise**, **Warnungen** und **harte Stopps**. Bei Herrn Krause etwa: Biopsie in zwei Tagen geplant – Apixaban pausieren? Kontrastmittel-CT angefordert – unter Metformin die Nierenfunktion prüfen. Ein zweites Antikoagulans ausgewählt – Doppelverordnung.

```quiz
question: "In wie vielen Fällen werden Arzneimittelwarnungen im CPOE laut einem Review übergangen?"
options: ["in 5–10 %", "in 20–30 %", "in 49–96 %"]
answer: "in 49–96 %"
shuffle: false  # options in a natural order
explain: "So das Review von van der Sijs et al. [@vandersijs2006] – oft zu Recht, weil die Warnung unspezifisch war. Ein System, das ständig warnt, wird ignoriert – auch dann, wenn es ausnahmsweise recht hat. Das ist **Alert-Fatigue**."
```

Gute Alerts sind **spezifisch** für diese Patientin oder diesen Patienten, **handlungsleitend** (was soll ich tun?), kommen **zum richtigen Zeitpunkt** im Arbeitsablauf und sind **nach Schwere abgestuft**.

```match
question: "Aktivierung: Stopp, Hinweis oder gar kein Alert?"
options: ["Stopp", "Hinweis", "kein Alert"]
items:
  - item: "Penicillin-Allergie mit Anaphylaxie dokumentiert – Amoxicillin (ein Penicillin-Derivat) wird verordnet."
    answer: "Stopp"
  - item: "Paracetamol mit einer verordneten Tagesdosis von 8 g"
    answer: "Stopp"
  - item: "Ramipril-Verordnung, Kalium aktuell 5,3 mmol/l (leicht erhöht)"
    answer: "Hinweis"
  - item: "Bei jeder Metformin-Verordnung „Nierenfunktion beachten“ – die eGFR ist normal."
    answer: "kein Alert"
explain: "Die Allergie und die doppelte Tageshöchstdosis (ein typischer Eingabefehler, etwa Einzel- und Tagesdosis verwechselt) verlangen einen Stopp, ggf. mit dokumentierter Begründung. Das Kalium ist klinisch relevant, die Abwägung liegt bei der Ärztin. Eine Dauerwarnung bei normaler Nierenfunktion ist Rauschen und trainiert das Wegklicken. **Die Kunst liegt darin, Fall 4 zu vermeiden, damit Fall 1 wahrgenommen wird.**"
```

```match
question: "Raster für Arbeitsplatz & CPOE: Zu welcher Frage gehört die Antwort?"
options: ["USER", "DATA", "WORKFLOW", "INTERFACES", "RISK"]
items:
  - item: "Ärzt:innen, Pflege, Apotheke, Stationsleitung – mit unterschiedlichen Sichten und Rechten"
    answer: "USER"
  - item: "Anordnungen, Medikation, Allergien, Laborwerte, Wissensbasis für Interaktionen"
    answer: "DATA"
  - item: "Entscheidung → Verordnung → Prüfung → Bereitstellung → Gabe → Monitoring"
    answer: "WORKFLOW"
  - item: "KIS/ADT, LIS, RIS, Apothekensystem, Leistungsstellen (Order/Result)"
    answer: "INTERFACES"
  - item: "Alert-Fatigue, falsche Auswahl im Dropdown, Copy & Paste, Workarounds bei schlechter Usability"
    answer: "RISK"
explain: "Schlechte Usability – lange Klickpfade, Pflichtfelder, Alert-Flut – führt zu Workarounds wie Zetteln oder Sammeleingaben."
```

## 2 · Tumordokumentation & Tumorboard: viele Quellen, eine Empfehlung

Die Biopsie zeigt ein **Adenokarzinom**. Jetzt braucht es eine interdisziplinäre Therapieentscheidung. Im **Tumorboard** (auch Tumorkonferenz) sitzen alle Disziplinen, die dazu beitragen – bei Herrn Krause Pneumologie, Thoraxchirurgie, Onkologie, Strahlentherapie, Radiologie, Nuklearmedizin und Pathologie. In zertifizierten Krebszentren der Deutschen Krebsgesellschaft ist die Vorstellung bestimmter Fälle Pflicht; das molekulare Tumorboard aus [[therapy]] ist eine Spezialform. Informationstechnisch wichtig: **Das Ergebnis ist kein Gespräch, sondern eine dokumentierte Empfehlung.**

```timeline
title: "Der Tumorboard-Workflow"
events:
  - when: "1 · Anmeldung"
    what: "Fall, Fragestellung, Frist – Formular mit Pflichtfeldern"
  - when: "2 · Vorbereitung"
    what: "Daten zusammenführen, Bilder vorladen, Befunde prüfen"
  - when: "3 · Besprechung"
    what: "Fallansicht, Bilddemonstration, ggf. Video – oft nur wenige Minuten pro Fall"
  - when: "4 · Empfehlung"
    what: "Strukturiertes Protokoll, Freigabe durch den Vorsitz"
  - when: "5 · Umsetzung"
    what: "Aufgaben, Termine, Arztbrief, Kontrolle der Umsetzung – und ggf. Wiedervorstellung"
```

Die meiste Arbeit passiert **vor und nach** der Besprechung: Daten suchen, Empfehlungen umsetzen, Wiedervorstellungen nachhalten.

```match
question: "Herrn Krauses Fall auf einem Bildschirm: Aus welchem System kommt die Information?"
options: ["KIS", "PACS", "Pathologie-System", "Molekularpathologie", "Funktionsdiagnostik", "LIS", "Gesprächsnotiz"]
items:
  - item: "Klinik, Raucherstatus, Allgemeinzustand ECOG 0"
    answer: "KIS"
  - item: "Niedrigdosis-CT und PET-CT"
    answer: "PACS"
  - item: "Histologie: Adenokarzinom"
    answer: "Pathologie-System"
  - item: "EGFR, ALK, PD-L1"
    answer: "Molekularpathologie"
  - item: "Lungenfunktion: FEV1 78 %"
    answer: "Funktionsdiagnostik"
  - item: "Blutbild, Gerinnung, Kreatinin"
    answer: "LIS"
  - item: "Wunsch: „operieren, wenn möglich“"
    answer: "Gesprächsnotiz"
explain: "Mindestens sieben Quellen – in vielen Häusern noch als PDF, Freitext oder Screenshot manuell zusammengesucht. Das Tumorboard ist ein **Integrationsproblem in Reinform**, und die Fallansicht eine Frage guter [[topic:visualizations]]."
```

### Die Timeline – und welcher Stand sichtbar ist

Therapieentscheidungen beruhen auf **Verläufen**, nicht auf Einzelbefunden. Eine Timeline ordnet Ereignisse aus ganz unterschiedlichen Systemen auf einer Zeitachse:

```timeline
title: "Herrn Krauses Verlauf aus sieben Systemen"
events:
  - when: "Woche 0"
    what: "Niedrigdosis-CT: Rundherd (PACS)"
  - when: "Woche 2"
    what: "Aufnahme Pneumologie (KIS); Bronchoskopie und EBUS-Biopsie (Endoskopie); Histologie: Adenokarzinom (Pathologie)"
  - when: "Woche 3"
    what: "PET-CT: cN0 cM0 (PACS); Lungenfunktion FEV1 78 % (Funktionsdiagnostik)"
  - when: "Woche 4 · Mo 18:00"
    what: "**Export der Fallansicht** für das Tumorboard"
  - when: "Woche 4 · Di 11:00"
    what: "Molekularbefund freigegeben (Molekularpathologie)"
  - when: "Woche 4 · Di 14:00"
    what: "Tumorboard (Tumordokumentation)"
```

```quiz
question: "Was fällt an dieser Timeline auf?"
options:
  - "Das PET-CT kam zu spät für das Tumorboard."
  - "Der Molekularbefund wurde nach dem Datenstand der Fallansicht, aber vor dem Board freigegeben."
  - "Die Lungenfunktion fehlt in der Fallansicht."
answer: "Der Molekularbefund wurde nach dem Datenstand der Fallansicht, aber vor dem Board freigegeben."
explain: "Im Pathologiesystem ist der Befund da, in der Fallansicht nicht. Zeit ist in klinischen Systemen nicht nur eine Achse, sondern auch eine Frage: **Welcher Stand ist gerade sichtbar?** Eine gute Fallansicht zeigt deshalb ihren Datenstand."
```

### Tumordokumentation: einmal erfassen, mehrfach nutzen

Tumordokumentation ist spezialisierte, stark strukturierte Dokumentation:

| Feld | bei Herrn Krause |
|---|---|
| Diagnose | ICD-10-GM C34.1 · Oberlappen (Bronchus) |
| Morphologie | ICD-O-3 8140/3 · Adenokarzinom |
| Klinisches TNM | cT1c cN0 cM0 (UICC, 9. Auflage) |
| Stadium | UICC IA3 |
| Allgemeinzustand | ECOG 0 |
| Tumorboard | Datum, Empfehlung, Leitlinienbezug |

Klassifikationen sind **versioniert**: Seit dem 1. Januar 2026 empfiehlt die UICC die 9. Auflage der TNM-Klassifikation. Für Herrn Krause ändert sich nichts, aber die Version muss mitdokumentiert werden.

```match
question: "Wer nutzt dieselben Tumordaten wofür?"
options: ["Behandlung", "Klinisches Krebsregister", "Zentrumszertifizierung", "Forschung"]
items:
  - item: "Arztbrief, Therapieplanung, Nachsorge"
    answer: "Behandlung"
  - item: "Gesetzliche Meldung nach § 65c SGB V im einheitlichen onkologischen Basisdatensatz (oBDS)"
    answer: "Klinisches Krebsregister"
  - item: "Kennzahlen und Qualitätsindikatoren"
    answer: "Zentrumszertifizierung"
  - item: "Kohorten, Register, Studienrekrutierung"
    answer: "Forschung"
explain: "Ohne strukturierte Erfassung steht dieselbe Information in KIS, Tumordoku, Registermeldung, Zentrumsbogen und Studien-CRF – **Mehrfachdokumentation**. Das Ziel: einmal strukturiert erfassen, mehrfach nutzen."
```

### Die Empfehlung – und woher sie kommt

```case
**Tumorkonferenz Thorax · Woche 4, Di 14:00.** *Empfehlung:* anatomische Lobektomie rechts oben (VATS) mit systematischer Lymphknotendissektion. *Begründung:* cT1c cN0 cM0, UICC IA3, funktionell operabel (FEV1 78 %, ECOG 0). *Leitlinie:* S3-Leitlinie Lungenkarzinom, konform. *Weiteres:* Wiedervorstellung postoperativ mit pTNM und Molekularbefund. *Datenbasis:* Fallansicht, Stand Mo 18:00 – **Molekularbefund nicht berücksichtigt**. *Freigabe:* Vorsitz, Di 15:10, 7 Disziplinen anwesend.
```

**Provenance** heißt Herkunftsnachweis ([[topic:data-provenance]]). An jede Empfehlung lassen sich fünf Fragen stellen: Wer hat empfohlen? Auf welcher Datenbasis? Mit welcher Leitlinie – oder bewusst abweichend? Welche Information fehlte? Wurde die Empfehlung umgesetzt? **Ohne Datenbasis ist eine Empfehlung nicht nachvollziehbar** – für die Haftung, die Qualitätssicherung und die Forschung.

```reflect
question: "Aktivierung: Di 14:20 – Herr Krause wird besprochen. Eine Pathologin erwähnt: „Der Molekularbefund ist seit heute Vormittag freigegeben.“ In der Fallansicht fehlt er. (A) Empfehlung ohne Molekularbefund aussprechen, (B) Fall auf nächste Woche vertagen oder (C) Befund live öffnen, einbeziehen und den Datenstand dokumentieren? Und wie verhindert man, dass das wieder passiert?"
intro: "Meist **C** – oder A mit dokumentierter Wiedervorstellung: Für die OP-Entscheidung in einem frühen Stadium ist der Molekularbefund wohl nicht ausschlaggebend, für eine mögliche perioperative oder adjuvante Systemtherapie aber sehr wohl. Damit es nicht wieder passiert:"
answers:
  - "**System:** Live-Anbindung statt nächtlichem Export; ein Ereignis „neuer Befund freigegeben“ an die Tumorboard-Liste; sichtbarer Datenstand in der Fallansicht"
  - "**Prozess:** Checkliste „ausstehende Befunde“ bei der Anmeldung"
  - "**Organisation:** Anmeldefristen und klare Zuständigkeit für die Vorbereitung"
  - "Kernaussage: **Ein veralteter Datenstand ist ein typisches Risiko jeder zusammengeführten Ansicht.**"
```

## 3 · OP-Management: ein Ressourcenpuzzle

Die Empfehlung lautet Lobektomie. Eine Operation findet nur statt, wenn **alle Ressourcen gleichzeitig verfügbar** sind: Saal, Thoraxchirurgie, Anästhesie, OP-Pflege, Instrumente und Sterilgut (VATS-Turm, Siebe), Blutprodukte, ein Intensivbett für danach – und ein vorbereiteter Patient. „Patient bereit“ heißt bei Herrn Krause: aufgeklärt und eingewilligt, nüchtern, **Apixaban rechtzeitig pausiert**, Labor und Blutgruppe aktuell, OP-Seite markiert. Hier schließt sich der Kreis zu CPOE: Ohne die Medikationsanordnung von vorhin wäre die OP gefährlich oder würde abgesagt.

Der OP-Plan zeigt die Säle auf einer Zeitachse; Planung ist immer **Re-Planung**, etwa wenn ein Notfall eingeschoben wird. Das Statusboard zeigt, wo jeder Fall steht. Technisch ist das ein **Zustandsmodell**: *geplant → vorbereitet → eingeschleust → in OP → beendet → verlegt*. Ereignisse lösen die Übergänge aus, jedes erzeugt einen Zeitstempel – und kann eine Nachricht an andere Systeme auslösen.

```match
question: "Welcher Zustand ist nach dem Ereignis erreicht?"
options: ["vorbereitet", "eingeschleust", "in OP", "beendet", "verlegt"]
items:
  - item: "Aufklärung unterschrieben, nüchtern, Apixaban pausiert, Seite markiert"
    answer: "vorbereitet"
  - item: "07:05 – Herr Krause kommt im OP-Bereich an"
    answer: "eingeschleust"
  - item: "07:58 – Schnitt"
    answer: "in OP"
  - item: "10:31 – Naht"
    answer: "beendet"
  - item: "11:15 – Übergabe an die Intensivstation"
    answer: "verlegt"
explain: "Aus den Zeitstempeln entstehen Schnitt-Naht-Zeit, Wechselzeiten, Saalauslastung, OP-Bericht und die OPS-Kodierung für die Abrechnung. Klinische Workflows werden sehr oft als Zustandsmodell abgebildet."
```

### Sicherheit als Workflow: die WHO-Checkliste

Die WHO Surgical Safety Checklist strukturiert drei Momente. Digital werden die Checkpunkte zu **Pflichtschritten** im OP-System, mit Zeitstempel und Namen – der nächste Status ist erst erreichbar, wenn der Checkpunkt dokumentiert ist.

```match
question: "Wann wird der Punkt geprüft?"
options: ["Sign In – vor der Narkose", "Team Time Out – vor dem Schnitt", "Sign Out – vor Verlassen des Saals"]
items:
  - item: "Identität, Eingriff und Seite bestätigt; Einwilligung liegt vor"
    answer: "Sign In – vor der Narkose"
  - item: "Allergien, Atemweg, erwarteter Blutverlust"
    answer: "Sign In – vor der Narkose"
  - item: "Das Team stellt sich vor; Patient, Eingriff und Seite werden laut bestätigt"
    answer: "Team Time Out – vor dem Schnitt"
  - item: "Erwartete kritische Ereignisse werden besprochen"
    answer: "Team Time Out – vor dem Schnitt"
  - item: "Instrumente und Tücher gezählt"
    answer: "Sign Out – vor Verlassen des Saals"
  - item: "Präparate korrekt beschriftet"
    answer: "Sign Out – vor Verlassen des Saals"
explain: "Der letzte Punkt führt direkt zur Pathologie – und später zur Biobank."
```

```quiz
question: "Was zeigte die Studie in acht Kliniken nach Einführung der Checkliste?"
options:
  - "keinen messbaren Effekt"
  - "weniger Komplikationen, aber keine geringere Sterblichkeit"
  - "Sterblichkeit von 1,5 % auf 0,8 % und Komplikationen von 11,0 % auf 7,0 % gesunken"
answer: "Sterblichkeit von 1,5 % auf 0,8 % und Komplikationen von 11,0 % auf 7,0 % gesunken"
explain: "7.688 Patient:innen in acht Kliniken weltweit [@haynes2009]. Aber Vorsicht: Ein abgehaktes Feld ist nicht dasselbe wie ein gelebtes Time Out – ein sozio-technisches Thema."
```

```reflect
question: "Aktivierung: Do, 06:45 – die Intensivstation meldet: „Vor 14 Uhr haben wir kein Intensivbett.“ Herr Krause ist seit 22 Uhr nüchtern, Apixaban seit zwei Tagen pausiert, Saal 3 ab 07:30 für ihn geplant. Was passiert jetzt mit ihm und Saal 3? Wer muss informiert werden – über welches System? Was hätte das System früher sichtbar machen können?"
answers:
  - "**Optionen:** Reihenfolge in Saal 3 tauschen (eine Mediastinoskopie vorziehen, die kein Intensivbett braucht); Herrn Krause auf den Nachmittag schieben – dann Nüchternheit und Antikoagulationspause klären; IMC statt Intensiv prüfen; im schlimmsten Fall absetzen."
  - "**Informieren:** OP-Koordination, Anästhesie, Station, Patient, Intensivstation, ggf. Blutbank."
  - "**System:** Das OP-System sollte die Intensivbett-Belegung kennen – idealerweise schon am Vortag mit der Warnung „postoperatives Intensivbett nicht gesichert“. Diese Schnittstelle zwischen OP-Planung und Bettenmanagement gibt es in vielen Häusern nur telefonisch."
```

## 4 · PDMS Intensivmedizin: wenn Daten kontinuierlich entstehen

Herr Krause kommt um 11:15 auf die Intensivstation – und die Art der Daten ändert sich grundlegend.

```quiz
question: "Auf der Normalstation werden Vitalzeichen etwa dreimal täglich erhoben. Wie viele Messwerte entstehen auf der Intensivstation pro Parameter und Tag, wenn der Monitor einen Wert pro Sekunde liefert?"
options: ["24", "1.440", "86.400", "über 1 Million"]
answer: "86.400"
shuffle: false  # options in a natural order
explain: "24 × 60 × 60 = 86.400. Ein PDMS speichert davon typischerweise verdichtete Werte, etwa minütlich, und zeigt sie als **Kurve**."
```

Das **PDMS** (Patientendatenmanagementsystem) übernimmt Gerätedaten automatisch, zeigt alles auf einer Zeitachse, verwaltet Anordnungen und Perfusoren, berechnet Bilanzen und Scores und dokumentiert Pflege und Visiten. Scores wie SAPS II und TISS gehen auch in die Abrechnung der intensivmedizinischen Komplexbehandlung ein (OPS 8-980).

**Geräteintegration:** Monitor, Beatmung, Spritzenpumpen und Blutgasanalyse sprechen meist nicht direkt mit dem PDMS, sondern über ein **Geräte-Gateway** – historisch herstellerspezifisch, häufig HL7 v2, zunehmend der offene Standard ISO/IEEE 11073 SDC. Kennen Sie das? Es ist die **Direktverbindung am Kommunikationsserver vorbei** aus [[information-systems]]. Und: **Ein Messwert ist nicht gleich ein dokumentierter Wert.** In vielen Häusern übernimmt die Pflege die Werte aktiv und verwirft Artefakte – die Verantwortung bleibt beim Menschen.

```timeline
title: "Herrn Krauses erste Nacht in der Kurve"
events:
  - when: "02:10"
    what: "Alarm: Herzfrequenz über 130/min, Blutdruck fällt"
  - when: "02:15"
    what: "Ärztin am Bett, EKG: Vorhofflimmern – nach Lungenresektionen häufig, und Herr Krause hat eine Vorgeschichte"
  - when: "02:25"
    what: "Medikation im PDMS angeordnet und gegeben"
  - when: "03:40"
    what: "Frequenz wieder normal"
```

Die Kurve verbindet **Messwerte, Anordnungen und Handlungen** über die Zeit – das ist ihr eigentlicher Wert. Es ist derselbe Medikationskreislauf wie im CPOE, nur in Minuten statt Tagen.

### Alarme: zwischen Sicherheit und Alarmmüdigkeit

```quiz
question: "Welcher Anteil der klinischen Alarme sind laut einer Übersichtsarbeit Fehlalarme?"
options: ["5–10 %", "25–40 %", "72–99 %"]
answer: "72–99 %"
shuffle: false  # options in a natural order
explain: "Nach Sendelbach und Funk [@sendelbach2013]. Die Folge ist **Alarmmüdigkeit**: Desensibilisierung, echte Alarme werden überhört oder zu spät beachtet – wie die Alert-Fatigue im CPOE, nur akustisch und rund um die Uhr."
```

```match
question: "Aktivierung: Welcher Wert ist echt? Alarm auslösen und in die Akte übernehmen?"
options: ["Artefakt – prüfen, nicht übernehmen", "echt – handeln und dokumentieren"]
items:
  - item: "SpO₂ fällt kurz ab – 14:06, Herr Krause wird von der Pflege umgelagert"
    answer: "Artefakt – prüfen, nicht übernehmen"
  - item: "Arterieller Mitteldruck erst bei 8, dann bei 250 mmHg – 14:07, Blutentnahme aus dem arteriellen Zugang, danach Spülung"
    answer: "Artefakt – prüfen, nicht übernehmen"
  - item: "Anhaltend hohe Herzfrequenz – keine Manipulation, Patient wach, spürt Herzklopfen"
    answer: "echt – handeln und dokumentieren"
explain: "Ob ein Wert echt ist, entscheidet der **Kontext** – und der steht nicht im Messwert selbst. Deshalb validiert die Pflege, und deshalb sind Alarme ohne Kontext so oft falsch. Der dritte Fall ist eine zweite Episode von Herrn Krauses Vorhofflimmern. Mehr zur Frage, wann Daten verlässlich sind, im Thema [[topic:data-quality]]."
```

Gegenmaßnahmen sind teils technisch, teils organisatorisch: **individuelle Grenzwerte** pro Patient:in statt Werkseinstellung, **Verzögerung und Priorisierung** (kurze Ausreißer abwarten, Schweregrade unterscheiden), **gezielte Weiterleitung** an die zuständige Pflegekraft statt an alle und **„Smart Alarms“**, die mehrere Parameter kombinieren. Das Ziel ist nicht „weniger Alarme“, sondern **die richtigen Alarme bei der richtigen Person**.

```match
question: "Raster für das PDMS: Zu welcher Frage gehört die Antwort?"
options: ["USER", "DATA", "WORKFLOW", "INTERFACES", "RISK"]
items:
  - item: "Intensivpflege, Intensivmedizin, Physiotherapie, Apotheke – rund um die Uhr"
    answer: "USER"
  - item: "Zeitreihen der Vitalparameter, Beatmung, Perfusoren, Bilanzen, Scores"
    answer: "DATA"
  - item: "Messen → validieren → bewerten → handeln → dokumentieren, in Minuten statt Tagen"
    answer: "WORKFLOW"
  - item: "Medizingeräte über Gateway, KIS/ADT, LIS (Blutgasanalyse), Apotheke, Abrechnung"
    answer: "INTERFACES"
  - item: "Alarmmüdigkeit, Artefakte als Messwerte, Ausfall des Gateways, Datenflut"
    answer: "RISK"
```

## 5 · Biobank: von der Versorgung zur Forschung

Während Herr Krause auf der Intensivstation liegt, ist sein Tumorgewebe längst unterwegs.

```timeline
title: "Der Weg der Probe"
events:
  - when: "09:42 · OP"
    what: "Resektat entnommen"
  - when: "09:58 · Pathologie"
    what: "Die Diagnostik hat Vorrang: Die Pathologie entscheidet, welches Material für die Diagnose gebraucht wird; nur Überschussmaterial geht in die Biobank."
  - when: "10:15 · Asservierung"
    what: "Tumor, Normalgewebe, Plasma – eingefroren"
  - when: "10:30 · Biobank-IS"
    what: "Proben-ID, Aliquote, Lagerort (z. B. −80 °C oder Gasphase über Flüssigstickstoff)"
  - when: "später"
    what: "Herausgabe nach genehmigtem Antrag"
```

```quiz
question: "Wie lang war die kalte Ischämiezeit von Herrn Krauses Tumorgewebe (vom Entfernen bis zum Einfrieren)?"
options: ["16 min", "33 min", "48 min", "73 min"]
answer: "33 min"
shuffle: false  # options in a natural order
explain: "09:42 → 10:15. Die Zeit wird mit der Probe dokumentiert, denn sie beeinflusst, ob sich RNA oder Proteine später verlässlich messen lassen – **Präanalytik zählt**, genau wie im Labor."
```

Damit aus Versorgungsmaterial eine Forschungsressource wird, braucht es zwei Voraussetzungen ([[topic:privacy-ethics]]):

1. **Einwilligung:** In der Universitätsmedizin wird zunehmend der **Broad Consent der Medizininformatik-Initiative** (MII) genutzt – ein bundesweit einheitlicher Mustertext für die Nutzung von Daten und Proben in künftiger, noch nicht festgelegter Forschung, jederzeit widerrufbar.
2. **Pseudonymisierung über eine Treuhandstelle:** Die Klinik kennt die Identität; die Zuordnung zum Pseudonym und den Einwilligungsstatus verwaltet getrennt davon die Treuhandstelle; Biobank und Forschende arbeiten mit pseudonymisierten Daten. Die Architektur ist lokal unterschiedlich – das Prinzip der Trennung ist überall gleich.

```include trust-center-de.svg
```

```match
question: "Wer kennt was?"
options: ["Klinik", "Treuhandstelle", "Biobank & Forschung"]
items:
  - item: "Name und Geburtsdatum zusammen mit der Patienten-ID 4711-K"
    answer: "Klinik"
  - item: "Die Zuordnung 4711-K ↔ PSN-7Q2K-91XD und den Einwilligungsstatus"
    answer: "Treuhandstelle"
  - item: "Proben und klinische Daten unter PSN-7Q2K-91XD"
    answer: "Biobank & Forschung"
explain: "Die Treuhandstelle ist also auch ein Informationssystem – mit sehr speziellem USER und sehr speziellem RISK."
```

**Ohne klinischen Kontext keine Forschung:** Eine Probe ist wissenschaftlich nur so viel wert wie ihr Kontext – sonst ist sie nur gefrorenes Gewebe. Dazu gehören das endgültige Stadium (pT1c pN0 (0/18) R0, aus der Tumordokumentation), Histologie und Molekularbefund (Pathologie), Raucherstatus und Vorerkrankungen (KIS), Therapie und Verlauf sowie Nachsorge, Rezidiv und Überleben (Krebsregister). Diese Daten werden über das Pseudonym verknüpft: In der MII führen die **Datenintegrationszentren** sie standardisiert zusammen, Forschende stellen Anträge über das **Forschungsdatenportal für Gesundheit** und erhalten nach Prüfung pseudonymisierte Daten und Proben (siehe [[topic:data-sharing]]). Provenance verfolgt jede Probe von der Entnahme bis zum Verbrauch: *Wer hat wann was mit der Probe gemacht – und mit welcher Einwilligung?* Das ist dieselbe Frage wie beim Tumorboard.

```reflect
question: "Aktivierung: Zwei Jahre später widerruft Herr Krause seine Einwilligung. Seine Proben lagern in der Biobank, seine Daten wurden in zwei Projekten genutzt, eines ist publiziert. Wo überall sind seine Proben und Daten? Was muss jetzt passieren – in welchem System? Was lässt sich nicht mehr zurückholen?"
intro: "Merke: **Einwilligung ist ein Status, der sich ändern kann – kein Formular, das einmal abgeheftet wird.**"
answers:
  - "**Wo:** Proben im Biobank-Informationssystem (Lagerort, Aliquote, ggf. schon an Projekte herausgegeben), Daten im Datenintegrationszentrum und in den Projektdatensätzen, der Einwilligungsstatus in der Treuhandstelle."
  - "**Was passieren muss:** Status in der Treuhandstelle ändern, das Ereignis an Biobank und Datenintegrationszentrum weitergeben, Proben vernichten oder – je nach Einwilligung und Rechtslage – anonymisieren, Daten löschen oder sperren."
  - "**Nicht zurückholbar:** Ergebnisse bereits abgeschlossener Analysen und Publikationen."
  - "Der Widerruf ist ein Ereignis, das durch mehrere Systeme laufen muss – wie eine ADT-Nachricht. Und was passiert, wenn diese Nachricht in einer Queue hängen bleibt? (Siehe die Übung [[his-exercise]].)"
```

## Synthese: ein Raster, fünf Systeme

| | Arbeitsplatz & CPOE | Tumorboard | OP-Management | PDMS | Biobank |
|---|---|---|---|---|---|
| **USER** | Ärzt:innen, Pflege, Apotheke | interdisziplinäres Board | OP-Team, Koordination | Intensivpflege und -medizin | Pathologie, Forschende, Patient:in |
| **DATA** | Anordnungen, Medikation | Befunde aus 7+ Quellen, TNM | Plan, Ressourcen, Zeitstempel | Zeitreihen, Alarme, Scores | Proben, Consent, Pseudonyme |
| **WORKFLOW** | verordnen → prüfen → geben | anmelden → beraten → empfehlen | planen → operieren → umplanen | messen → validieren → handeln | einwilligen → lagern → herausgeben |
| **INTERFACES** | LIS, RIS, Apotheke | PACS, Pathologie, Krebsregister | Betten, Blutbank, Pathologie | Medizingeräte, LIS | Treuhandstelle, DIZ |
| **RISK** | Alert-Fatigue | veralteter Datenstand | Ressourcenkonflikt | Alarmmüdigkeit, Artefakte | Widerruf, Re-Identifizierung |

```match
question: "Zu welchem System gehört das typische Risiko?"
options: ["Arbeitsplatz & CPOE", "Tumorboard", "OP-Management", "PDMS", "Biobank"]
items:
  - item: "Warnungen werden reflexhaft weggeklickt"
    answer: "Arbeitsplatz & CPOE"
  - item: "Die Fallansicht zeigt einen Stand von gestern Abend"
    answer: "Tumorboard"
  - item: "Saal, Team und Patient sind bereit – das Intensivbett fehlt"
    answer: "OP-Management"
  - item: "Ein Spülvorgang steht als Blutdruck von 250 mmHg in der Akte"
    answer: "PDMS"
  - item: "Ein Widerruf erreicht nicht alle Systeme"
    answer: "Biobank"
```

Lesen Sie die Tabelle zeilenweise: Die Systeme sind sehr verschieden, aber sie teilen **Grundmuster**. Alle brauchen den **Patientenkontext** aus ADT. Alle arbeiten mit **Zeit** – als Verordnungszeitpunkt, Datenstand, Zeitstempel, Zeitreihe oder Einwilligungsdatum. Alle bilden **Status** ab. Alle brauchen **Provenance**. Und in jeder INTERFACES-Zeile stehen andere Systeme.

## Take-home Messages

1. **Spezialisierte Systeme unterstützen Arbeit – nicht nur Datenhaltung.** Rollen, Sichten, Regeln und Status prägen, wie klinisch gearbeitet wird.
2. **CPOE macht Anordnungen strukturiert und damit prüfbar.** Gute Entscheidungsunterstützung ist spezifisch – sonst entsteht Alert-Fatigue.
3. **Therapieentscheidungen brauchen integrierte Daten** – mit sichtbarem Datenstand und nachvollziehbarer Herkunft (Provenance).
4. **Zeit ist die zentrale Dimension** – als OP-Plan und Zeitstempel oder als kontinuierliche Zeitreihe im PDMS.
5. **Aus Versorgung wird Forschung nur mit Einwilligung, Pseudonym und Kontext.** Das 5-Fragen-Raster funktioniert für jedes dieser Systeme – und für jedes neue.

## Ausblick: von spezialisierten Systemen zu Standards

Heute ging es darum, **was** die Systeme leisten müssen; in der nächsten Vorlesung geht es darum, **wie** wir sie dazu bringen, miteinander zu sprechen: HL7 v2 (ADT, ORU), CDA für strukturierte Dokumente wie den Arztbrief, DICOM, IHE-Profile, xDT im ambulanten Bereich und die Kommunikationsmuster Push, Pull und Publish–Subscribe. Einen Ausblick auf den modernen Standard bietet das Thema [[topic:fhir]].

## Selbsttest

```quiz
question: "Warum kann CPOE eine Anordnung prüfen, eine Papieranordnung aber nicht?"
options:
  - "Weil sie schneller geschrieben ist"
  - "Weil sie als strukturiertes Objekt mit Feldern vorliegt (was, für wen, wann, wie dringlich, warum)"
  - "Weil die Apotheke sie früher sieht"
answer: "Weil sie als strukturiertes Objekt mit Feldern vorliegt (was, für wen, wann, wie dringlich, warum)"
```

```quiz
question: "Was gehört zu einer nachvollziehbaren Tumorboard-Empfehlung unbedingt dazu?"
options: ["die Datenbasis mit ihrem Stand", "die Zahl der Teilnehmenden", "die Dauer der Besprechung"]
answer: "die Datenbasis mit ihrem Stand"
```

```quiz
question: "Was macht eine Biobank-Probe wissenschaftlich wertvoll?"
options:
  - "eine möglichst große Gewebemenge"
  - "Einwilligung, Pseudonym, Präanalytik-Daten und klinischer Kontext"
  - "eine möglichst lange Lagerung"
answer: "Einwilligung, Pseudonym, Präanalytik-Daten und klinischer Kontext"
```

```reflect
question: "Transfer: Wenden Sie das 5-Fragen-Raster auf ein System an, das hier nicht vorkam – etwa ein Notaufnahme-, Pathologie- oder Pflegedokumentationssystem – und vergleichen Sie es mit der Synthesetabelle."
answers:
  - "Beispiel **Notaufnahmesystem** – USER: Triage-Pflege, ZNA-Ärzt:innen, Rettungsdienst-Übergabe; DATA: Triagestufe, Vitalzeichen, Wartezeiten, vorläufige Identität; WORKFLOW: Ankunft → Triage → Behandlung → Disposition (Aufnahme oder Entlassung); INTERFACES: KIS/ADT, LIS, RIS, Bettenmanagement, Rettungsdienst; RISK: unbekannte Identität, Überfüllung, Patient:innen „verschwinden“ im Wartebereich."
  - "Gemeinsam mit den fünf Systemen: Patientenkontext, Zeit (Wartezeiten), Status (Triagestufe, Behandlungsstand) und Provenance."
```
