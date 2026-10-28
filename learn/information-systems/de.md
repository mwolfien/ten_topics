---
title: "KIS, LIS und RIS/PACS – Zusammenspiel klinischer Informationssysteme"
summary: "Wie KIS, Labor- und Radiologiesysteme als gemeinsames Informationssystem zusammenarbeiten – und warum ihre Integration so schwierig ist. Wir folgen einer Patientin und ihren Daten durch die Systemlandschaft eines Krankenhauses."
duration_minutes: 50
level: "Vertiefung"
audiences: [med, cs, clin, tech, pat]
order: 3
builds_on: [history]
course: his
lecture: 2
author: "Eveline Prochaska, Markus Wolfien"
objectives:
  - "Typische Architekturen klinischer Systemlandschaften (All-in-One, Best-of-Breed, Spaghetti, Stern) unterscheiden und bewerten"
  - "Die Rolle von ADT für Patientenidentität und Versorgungskontext erklären"
  - "Das Order/Result-Muster als gemeinsame Logik diagnostischer Systeme beschreiben"
  - "Den Laborworkflow von der Anforderung bis zum validierten Befund nachvollziehen"
  - "Den radiologischen Workflow mit RIS, PACS und DICOM erläutern"
  - "Schnittstellen, Redundanzen und Ausfallrisiken in einem Patientenfall identifizieren"
readings: [winter2023, carraro2007, sittig2010]
related_topics: [ehr-cis, fhir, data-quality]
source: "Vorlesung 2 „KIS, LIS und RIS/PACS – Zusammenspiel klinischer Informationssysteme“, Informationssysteme im Gesundheitswesen (WiSe 2026/27), Eveline Prochaska und Markus Wolfien, IMB & ZMI"
---

> **Leitfrage:** Wie arbeiten KIS, LIS und RIS/PACS als gemeinsames Informationssystem zusammen – und warum ist ihre Integration so schwierig?

Im Modul [[history]] haben Sie gesehen, *warum* KIS, LIS und PACS entstanden sind: als Antwort auf unterschiedliche Datentypen und Prozesslogiken. *Subsysteme sind Ausdruck fachlicher Spezialisierung, nicht nur technischer Fragmentierung.* Jetzt fragen wir, **wie** diese Systeme technisch und prozessual zusammenarbeiten. Dabei gehen wir nicht System für System vor, sondern folgen einem Informationsfluss – einer Patientin, einem Fall und ihrem Weg durch die Systemlandschaft.

```persona med
Sie werden täglich Aufträge anlegen, Befunde lesen und Patient:innen verlegen. Dieses Modul zeigt, was dabei im Hintergrund passiert – und an welchen Stellen ein Befund verloren gehen kann.
```

```persona cs
Vieles hier kennen Sie unter anderen Namen: Order/Result ist ein Request-Response-Muster mit Korrelations-IDs, ADT ist ein Event-Stream, der Kommunikationsserver ein Message Broker. Neu ist, was ein verlorenes Ereignis hier bedeutet.
```

```persona clin
Ein Befund gilt erst als angekommen, wenn ihn jemand gesehen und gehandelt hat. Das Modul zeigt, warum Verlegungen, Dubletten und kritische Werte dabei besondere Aufmerksamkeit brauchen.
```

```persona tech
Spaghetti gegen Stern ist Punkt-zu-Punkt gegen Hub-and-Spoke. Spannend wird es bei der Frage, welche Direktverbindungen am Monitoring vorbeilaufen – und wer nachts zuständig ist.
```

```persona pat
Warum werden Sie im Krankenhaus immer wieder nach Name und Geburtsdatum gefragt, und warum tragen Sie ein Armband mit Barcode? Dieses Modul erklärt, wie viel davon abhängt.
```

```case
**Frau Erika Müller, 68 Jahre** (*12.03.1958). Dienstag, 14:05 Uhr, Zentrale Notaufnahme (ZNA): Temperatur 39,2 °C, SpO₂ 89 %, Atemfrequenz 28/min, reduzierter Allgemeinzustand. Arbeitsdiagnose: Verdacht auf ambulant erworbene Pneumonie.

In den nächsten Stunden folgen Aufnahme und Fallanlage, Labor inklusive Blutgasanalyse und Blutkulturen, ein Röntgen-Thorax und am Folgetag ein CT. Frau Müller verschlechtert sich und wird auf die Intensivstation verlegt. **Wir verfolgen nicht die Medizin, sondern die Daten.**
```

```quiz
question: "Aktivierung: Wie viele Systeme berührt Frau Müller in den ersten 24 Stunden ihres Aufenthalts?"
options:
  - "1–2 – „Das KIS macht doch alles.“"
  - "3–5 – KIS plus Labor und Radiologie"
  - "6–9 – ein paar Spezialsysteme mehr"
  - "10 oder mehr – eine ganze Landschaft"
answer: "10 oder mehr – eine ganze Landschaft"
shuffle: false  # options in a natural order
explain: "KIS mit Aufnahme/ADT, Order Entry und klinischer Dokumentation, Kommunikationsserver, LIS Klinische Chemie, LIS Mikrobiologie, POCT-Middleware für die Blutgasanalyse, RIS, Modalität (Röntgen/CT), PACS, PDMS auf der Intensivstation, Abrechnung/DRG – je nach Haus noch deutlich mehr. **Jedes dieser Systeme braucht denselben Kontext: Wer ist die Patientin? Zu welchem Fall gehört das? Wo ist sie gerade?**"
```

> **Integration ist kein Sonderfall, sondern Alltag** – schon bei einer „normalen“ Routine-Aufnahme.

## 1 · Architekturen: Wie sind klinische Systemlandschaften aufgebaut?

An jede Systemlandschaft lassen sich zwei Fragen stellen – und die Antworten sind **unabhängig voneinander** ([@winter2023]):

1. **Wie viele Anwendungen?** (fachlich-logische Ebene) Eine integrierte Suite eines Herstellers – *All-in-One* – oder für jeden Bereich das fachlich stärkste Spezialsystem – *Best-of-Breed*?
2. **Wie kommunizieren sie?** (technische Ebene) Viele direkte Punkt-zu-Punkt-Verbindungen – *Spaghetti* – oder Kommunikation über eine zentrale Integrationsschicht – *Stern*?

| | All-in-One | Best-of-Breed |
|---|---|---|
| Idee | möglichst viele Funktionen aus einer Suite | pro Bereich das fachlich stärkste System |
| Stärken | einheitliche Oberfläche und Datenbasis, wenige interne Schnittstellen, ein Vertragspartner | fachlich passgenaue Systeme, Komponenten austauschbar, Innovation pro Fachbereich |
| Schwächen | Herstellerabhängigkeit (Lock-in), einzelne Module fachlich schwächer, Spezialprozesse schwer abbildbar | viele Schnittstellen, hoher Integrationsaufwand, redundante Stammdaten, uneinheitliche Bedienung, viele Verträge |

In der Realität – auch am UKDD – findet man meist **Mischformen**: ein Kern-KIS plus spezialisierte Subsysteme (LIS, RIS/PACS, PDMS …). Spezialisierung ist fachlich sinnvoll, sie verschiebt aber Komplexität in die Integration.

```match
question: "All-in-One oder Best-of-Breed? Ordnen Sie die Eigenschaft zu."
options: ["All-in-One", "Best-of-Breed"]
items:
  - item: "ein Vertragspartner"
    answer: "All-in-One"
  - item: "einzelne Komponenten sind austauschbar"
    answer: "Best-of-Breed"
  - item: "Abhängigkeit vom Hersteller (Lock-in)"
    answer: "All-in-One"
  - item: "redundante Stammdaten in vielen Systemen"
    answer: "Best-of-Breed"
  - item: "einheitliche Oberfläche und Datenbasis"
    answer: "All-in-One"
  - item: "Innovation pro Fachbereich"
    answer: "Best-of-Breed"
```

### Spaghetti oder Stern?

Im **Spaghetti**-Muster spricht jedes System direkt mit jedem anderen. Im ungünstigsten Fall wächst die Zahl der Schnittstellen quadratisch: **n · (n − 1) / 2**. Jede davon muss gebaut, getestet, bei jedem Update geprüft und überwacht werden. Im **Stern**-Muster hat jedes System genau eine Verbindung zum Kommunikationsserver – das wächst linear: **n**. Bei 6 Systemen sind das 15 gegenüber 6 Verbindungen.

```quiz
question: "Ein Haus hat 30 Systeme. Wie viele Schnittstellen wären es im Spaghetti-Muster im ungünstigsten Fall?"
options: ["30", "60", "435", "900"]
answer: "435"
shuffle: false  # options in a natural order
explain: "30 · 29 / 2 = 435 – im Stern wären es 30. Die Rechnung ist ein Worst Case, denn nicht jedes System muss mit jedem sprechen. Das Prinzip bleibt: Direktverbindungen skalieren schlecht."
```

Der **Kommunikationsserver** (auch Integration Engine, Interface Engine, KOM-Server) ist mehr als ein Verteiler. Er übernimmt vier Aufgaben – und ist zugleich ein *Single Point of Failure*, der Hochverfügbarkeit, Monitoring und klare Zuständigkeiten braucht.

```match
question: "Welche Aufgabe des Kommunikationsservers ist jeweils gefragt?"
options: ["Routing", "Transformation & Mapping", "Pufferung (Queueing)", "Monitoring & Protokoll"]
items:
  - item: "Jede Verlegung soll an LIS, RIS und PDMS gehen."
    answer: "Routing"
  - item: "Das KIS sendet HL7 v2.3, das LIS erwartet v2.5 und andere Stationskürzel."
    answer: "Transformation & Mapping"
  - item: "Das LIS ist nach einem Update kurz nicht erreichbar; keine Nachricht soll verloren gehen."
    answer: "Pufferung (Queueing)"
  - item: "Eine Nachricht kam nicht an und soll nachverfolgt und erneut gesendet werden."
    answer: "Monitoring & Protokoll"
explain: "Merken Sie sich die Pufferung: Im Fehlerszenario am Ende spielt eine hängende Queue die Hauptrolle."
```

| | All-in-One | Best-of-Breed |
|---|---|---|
| **Stern** | integrierte Suite, Fremdsysteme sauber über den Kommunikationsserver angebunden | viele Spezialsysteme, konsequent über den Kommunikationsserver integriert |
| **Spaghetti** | Suite, aber Zusatzsysteme direkt „angeflanscht“ | gewachsene Landschaft mit vielen Direktschnittstellen |

*Best-of-Breed ist nicht automatisch Spaghetti, und All-in-One ist nicht automatisch interoperabel.* Intern integriert heißt nicht: nach außen standardisiert – etwa für Einweiser, ePA oder Forschung. Unten rechts steht der historisch gewachsene Zustand aus [[history]]: *eher gewachsen als entworfen*.

```include landscape-de.svg
```

```reflect
question: "Aktivierung: All-in-One, Best-of-Breed, Stern oder Spaghetti – was sehen Sie in dieser Landschaft? Und wo würden Sie bei einer Störung zuerst suchen?"
intro: "Es ist ein **Hybrid**:"
answers:
  - "Die KIS-Suite ist intern All-in-One (sechs Module, ein Hersteller)."
  - "Mit LIS, RIS, PDMS und OP-System verschiedener Hersteller ist die Gesamtlandschaft Best-of-Breed."
  - "Kommunikativ überwiegend ein Stern über den Kommunikationsserver – aber mit Direktverbindungen: RIS ↔ PACS, LIS ↔ POCT-Middleware, PDMS ↔ Medizingeräte und der Bildlink KIS → PACS."
  - "Direktverbindungen sind oft fachlich gut begründet (Datenvolumen, Echtzeit, Herstellerkopplung), laufen aber am Monitoring des Kommunikationsservers vorbei. Bei einer Störung sucht man zuerst am Server – die Direktverbindungen werden gern vergessen."
```

## 2 · ADT: das organisatorische Rückgrat

**ADT** steht für *Admission, Discharge, Transfer* – Aufnahme, Entlassung, Verlegung – und beantwortet drei Fragen: **Wer ist die Patientin, in welchem Fall, und wo ist sie gerade?** Das klingt nach Verwaltung, ist aber der unterschätzte Schlüssel für alles, was danach kommt.

```timeline
title: "Frau Müllers Aufenthalt als ADT-Ereignisse"
events:
  - when: "Di 14:05 · A01"
    what: "Aufnahme in der ZNA"
  - when: "Di 18:40 · A02"
    what: "Verlegung auf die Intensivstation"
  - when: "Fr 10:15 · A02"
    what: "Verlegung auf die Pneumologie (Station P3)"
  - when: "Tag 9, 11:00 · A03"
    what: "Entlassung nach Hause"
```

Jede Bewegung ändert den Kontext, in dem alle anderen Systeme arbeiten. Drei Ebenen muss man dabei auseinanderhalten:

| Ebene | Bedeutung | bei Frau Müller |
|---|---|---|
| **Patient:in** | die Person: Stammdaten wie Name, Geburtsdatum, Geschlecht, Versicherung; die Patienten-ID bleibt im Haus dauerhaft gleich | ID 4711 |
| **Fall** | eine Behandlungsepisode: Klammer für Dokumentation, Leistungen und Abrechnung (DRG) | F2024-0312 (Hüft-OP, abgeschlossen) und F2026-0815 (Pneumonie, aktuell) |
| **Bewegung** | wo und wann innerhalb des Falls: Station, Bett, Fachabteilung, Zeitraum | ZNA → Intensiv → P3 |

Die Begriffe variieren je Hersteller; in HL7 v2 heißt die Fallebene *Visit* (PV1-Segment), in FHIR *Encounter*.

```match
question: "Auf welche Ebene schaut das System jeweils?"
options: ["Patient:in", "Fall", "Bewegung"]
items:
  - item: "Das LIS sucht die Vorwerte von Frau Müller."
    answer: "Patient:in"
  - item: "Die Abrechnung gruppiert die DRG."
    answer: "Fall"
  - item: "Das PDMS zeigt Frau Müller auf der Stationsliste der Intensivstation."
    answer: "Bewegung"
  - item: "Das PACS findet die Bilder der Hüft-OP von 2024 als Vorbilder."
    answer: "Patient:in"
```

Fast jedes System hält eine **Kopie des ADT-Kontexts**: das LIS (für Probenzuordnung, Vorwerte, Befundrouting und alters- und geschlechtsspezifische Referenzbereiche), RIS/PACS (für die Zuordnung von Bildern und Vorbildern), das PDMS (für die Stationsliste und Monitordaten), die Abrechnung (für die DRG und die Datenübermittlung an die Krankenkasse nach § 301 SGB V) und sogar Betten- und Küchenplanung. **Diese Kopien müssen aktuell bleiben.**

### Ereignisse statt Abfragen

Die Systeme fragen nicht ständig beim KIS nach. Stattdessen meldet das KIS jedes Ereignis, und der Kommunikationsserver verteilt es an alle Abonnenten. Die Folge: **Geht ein Ereignis verloren, ist die Kopie veraltet – oft unbemerkt.**

```match
question: "Welcher HL7-v2-Ereignistyp passt?"
options: ["A01", "A02", "A03", "A08", "A11", "A40"]
items:
  - item: "Frau Müller wird in der ZNA aufgenommen."
    answer: "A01"
  - item: "Sie wird auf die Intensivstation verlegt."
    answer: "A02"
  - item: "Sie wird nach Hause entlassen."
    answer: "A03"
  - item: "Ihre Adresse wird korrigiert."
    answer: "A08"
  - item: "Eine versehentlich angelegte Aufnahme wird zurückgenommen."
    answer: "A11"
  - item: "Zwei Akten derselben Person werden zusammengeführt."
    answer: "A40"
explain: "Gerade die Korrekturen – Stornos (A11) und Zusammenführungen (A40) – sind fehleranfällig, weil alle Empfänger sie korrekt nachvollziehen müssen."
```

So sieht die Verlegung als (vereinfachte) HL7-v2-Nachricht aus. Jede Zeile ist ein Segment, `|` trennt Felder, `^` trennt Komponenten:

```text
MSH|^~\&|KIS|KLINIKUM|LIS|LABOR|202610131840||ADT^A02|MSG0471|P|2.5
EVN|A02|202610131840
PID|1||4711^^^KLINIKUM^PI||Müller^Erika||19580312|F
PV1|1|I|ITS^01^B|||ZNA^03^A|||||||||||||F2026-0815
```

`MSH` ist der Kopf (Sender, Empfänger, Typ), `EVN` das Ereignis, `PID` die Patientin, `PV1` der Aufenthalt bzw. Fall. Die vielen leeren Felder sind normal: HL7 v2 ist ein Baukasten, aus dem jede Einrichtung nur einen Teil nutzt – Stärke und Schwäche zugleich.

```match
question: "Lesen Sie mit: Was steht wo in der Nachricht?"
options: ["Patienten-ID (wer?)", "neuer Ort (Station^Zimmer^Bett)", "vorheriger Ort", "Fallnummer (welcher Fall?)", "Nachrichtentyp und Ereignis"]
items:
  - item: "`ADT^A02`"
    answer: "Nachrichtentyp und Ereignis"
  - item: "`4711`"
    answer: "Patienten-ID (wer?)"
  - item: "`ITS^01^B`"
    answer: "neuer Ort (Station^Zimmer^Bett)"
  - item: "`ZNA^03^A`"
    answer: "vorheriger Ort"
  - item: "`F2026-0815`"
    answer: "Fallnummer (welcher Fall?)"
```

### Patientenidentität: Dubletten und Verwechslungen

| | Dublette: eine Person, zwei IDs | Verwechslung: zwei Personen, eine ID |
|---|---|---|
| Beispiel | ID 4711 Erika Müller und ID 8823 Erika Mueller, beide *12.03.1958 | ID 4711 Erika Müller *12.03.1958 und *07.11.1961 |
| Risiko | Befunde verteilen sich auf zwei Akten, Vorwerte und Vorbilder fehlen | Befunde der falschen Person → falsche Therapieentscheidung |
| Gegenmaßnahme | Zusammenführen (A40), Master Patient Index, Dublettenprüfung | zweites Identifikationsmerkmal, Patientenarmband mit Barcode |

> **Patientenidentifikation ist keine Verwaltungsfrage, sondern Patientensicherheit.**

```match
question: "Dublette oder Verwechslung?"
options: ["Dublette", "Verwechslung"]
items:
  - item: "Der Delta-Check findet keinen Vorwert, obwohl Frau Müller schon oft im Haus war."
    answer: "Dublette"
  - item: "In der Akte steht ein Laborwert, der zu einer anderen Patientin gehört."
    answer: "Verwechslung"
  - item: "„Müller“ und „Mueller“ mit gleichem Geburtsdatum unter zwei IDs"
    answer: "Dublette"
  - item: "Zwei Patientinnen gleichen Namens werden unter derselben ID geführt."
    answer: "Verwechslung"
explain: "Die Dublette ist häufig und eher lästig als akut gefährlich; die Verwechslung ist seltener, aber gefährlich. Deshalb gelten in der Klinik immer zwei Identifikationsmerkmale."
```

## 3 · Orders & Results: Was soll passieren – und was kam dabei heraus?

**ADT** sagt: *Wer? Welcher Fall? Wo?* **Order/Result** sagt: *Was soll passieren – und was kam dabei heraus?* Bildlich ist ADT die Schiene, an der viele Auftragskreisläufe hängen: Labor (Blutbild, CRP, PCT), Radiologie (Röntgen-Thorax), Mikrobiologie (Blutkulturen), Konsile. Jeder Kreislauf erbt den Kontext von der Schiene – **ist die Schiene falsch, ist auch jeder Kreislauf falsch adressiert.**

```include loop-de.svg
```

Ein Auftrag durchläuft die Status *angefordert → angenommen → in Bearbeitung → vorläufig → endgültig*, dazu die Sonderzustände *storniert* und *korrigiert*, die ebenfalls übermittelt werden müssen. Vorläufige und korrigierte Befunde sind keine Sonderfälle, sondern Alltag – etwa in der Mikrobiologie.

```quiz
question: "Wann ist der Auftragskreislauf geschlossen?"
options:
  - "Wenn das LIS den Befund technisch an das KIS gesendet hat"
  - "Wenn der Befund im KIS gespeichert ist"
  - "Wenn jemand das Ergebnis gesehen und gehandelt hat"
answer: "Wenn jemand das Ergebnis gesehen und gehandelt hat"
explain: "Der Kreislauf endet nicht mit dem technischen Versand, sondern erst mit der Kenntnisnahme. Nicht beachtete Befunde („Test Result Follow-up“) sind ein bekanntes Patientensicherheitsthema."
```

**Placer und Filler:** Das KIS als Auftraggeber (*Placer*) vergibt eine Auftragsnummer (z. B. A-77812), das LIS als Leistungserbringer (*Filler*) eine eigene Labor- bzw. Probennummer (z. B. L-55301). Beide Nummern reisen in jeder Nachricht mit – so findet das Ergebnis zu seinem Auftrag zurück. Zwei typische Störungen fallen nur auf, wenn jemand **offene Aufträge aktiv überwacht**: *Ergebnis ohne Auftrag* (z. B. Nachforderung direkt im Labor, Notfallprobe ohne elektronische Anforderung) und *Auftrag ohne Ergebnis* (Probe nie angekommen, Nachricht verloren, Untersuchung abgesagt).

Aktivierung: Bringen Sie die Schritte in die richtige Reihenfolge.

```match
question: "Order/Result-Puzzle, Labor: Welcher Schritt kommt an welcher Stelle?"
options: ["1", "2", "3", "4", "5", "6", "7"]
items:
  - item: "Technische Validation"
    answer: "5"
  - item: "Anforderung im KIS"
    answer: "1"
  - item: "Probeneingang und Barcode-Scan"
    answer: "3"
  - item: "Befund im KIS sichtbar"
    answer: "7"
  - item: "Messung am Analysegerät"
    answer: "4"
  - item: "Medizinische Validation"
    answer: "6"
  - item: "Blutentnahme mit Etikett"
    answer: "2"
explain: "Die technische Validation kommt vor der medizinischen."
```

```match
question: "Order/Result-Puzzle, Radiologie: Welcher Schritt kommt an welcher Stelle?"
options: ["1", "2", "3", "4", "5", "6", "7"]
items:
  - item: "Bilder ans PACS"
    answer: "5"
  - item: "Anforderung im KIS"
    answer: "1"
  - item: "Befundung am Befundungsplatz"
    answer: "6"
  - item: "Termin und rechtfertigende Indikation im RIS"
    answer: "2"
  - item: "Befund und Bildlink im KIS"
    answer: "7"
  - item: "Patientendaten per Worklist an die Modalität"
    answer: "3"
  - item: "Untersuchung am CT"
    answer: "4"
explain: "Oft vergessen: Die rechtfertigende Indikation wird *vor* der Untersuchung gestellt."
```

| | Order | Vorbereitung | Durchführung | Prüfung / Befundung | Result |
|---|---|---|---|---|---|
| **Labor** | Anforderung im KIS | Etikett, Entnahme, Probeneingang | Messung | technische und medizinische Validation | Befund im KIS |
| **Radiologie** | Anforderung im KIS | Termin, Indikation, Worklist | Untersuchung, Bilder ins PACS | Befundung | Befund und Bildlink im KIS |

> **Ein gemeinsames Informationsmuster – nicht zwei isolierte Systeme.** Wer es verstanden hat, versteht auch Pathologie, Kardiologie oder Konsile.

## 4 · LIS im Detail: von der Anforderung bis zum validierten Befund

Das LIS steuert drei Phasen. Die eigentliche Messung im Gerät ist nur der mittlere Teil:

| Präanalytik | Analytik | Postanalytik |
|---|---|---|
| Anforderung, Etikettierung, Blutentnahme, Transport, Probeneingang | Probenverteilung, Messung am Gerät, Qualitätskontrolle | technische und medizinische Validation, Befundübermittlung, Archivierung |

```quiz
question: "In welcher Phase lag in einer Studie eines Notfalllabors der größte Anteil der bestätigten Laborfehler?"
options: ["Präanalytik", "Analytik", "Postanalytik"]
answer: "Präanalytik"
shuffle: false  # options in a natural order
explain: "Von 160 bestätigten Fehlern lagen 61,9 % in der Präanalytik, 15,0 % in der Analytik und 23,1 % in der Postanalytik [@carraro2007]. Die meisten Fehler passieren nicht im Analysegerät, sondern an den Übergängen – Identifikation, Etikett, Transport, Übermittlung. Genau dort können Informationssysteme ansetzen."
```

```case
Ein ärztlicher Auftrag, drei Geschwindigkeiten: Die **Blutgasanalyse** läuft als Point-of-Care-Test direkt in der ZNA (das Gerät hängt über eine POCT-Middleware am LIS). **Blutbild, CRP, PCT und Laktat** kommen aus Klinischer Chemie und Hämatologie. Die **Blutkulturen** gehen in die Mikrobiologie, oft ein eigenes Subsystem – mit Vorbefund (z. B. Gramfärbung bei positiver Kultur) und erst nach Tagen dem endgültigen Befund mit Resistenztestung.
```

```match
question: "Wann ist welches Ergebnis ungefähr verfügbar? (Zeitangaben beispielhaft)"
options: ["nach Minuten", "nach ca. 1 Stunde", "nach mehreren Tagen, mit Vorbefund"]
items:
  - item: "Blutgasanalyse am POCT-Gerät"
    answer: "nach Minuten"
  - item: "Blutbild, CRP, PCT, Laktat"
    answer: "nach ca. 1 Stunde"
  - item: "Blutkulturen in der Mikrobiologie"
    answer: "nach mehreren Tagen, mit Vorbefund"
explain: "Für das KIS heißt das: mehrere Teilergebnisse, mehrere Subsysteme, vorläufige und endgültige Befunde – und alle zum selben Auftrag und Fall. Genau diese spät eintreffenden Befunde werden im Fehlerszenario wichtig."
```

**Der Barcode als Brücke:** Er verbindet physische Probe und digitalen Auftrag – Armband scannen, Auftrag im KIS, Etikett mit Auftrags- und Probennummer drucken, sofort am Bett aufkleben; das Analysegerät liest den Barcode und holt sich den Auftrag. Typische präanalytische Fehler sind vertauschte Etiketten oder falsche Röhrchen, hämolysierte Proben oder falsches Material, Proben, die nie ankommen, und falsche Abnahmezeitpunkte (z. B. bei Medikamentenspiegeln). Etiketten „auf Vorrat“ im Stationszimmer sind eine klassische Verwechslungsquelle.

Im Labor verteilt häufig eine **Middleware** die Aufträge an die Analysegeräte und sammelt die Messwerte. Dann folgen drei Prüfstufen: (1) **technische Validation** – Gerät in Ordnung, Qualitätskontrolle im Sollbereich, Messung formal plausibel? (2) **regelbasierte Prüfung** – Referenzbereich, Delta-Check (Abweichung zum Vorwert), Plausibilität zwischen Parametern; (3) **medizinische Validation** – passt das Gesamtbild zur Patientin? **Kritische Werte** werden zusätzlich aktiv, z. B. telefonisch, an das behandelnde Team gemeldet; hier genügt eine Nachricht allein nicht.

```quiz
question: "Der Delta-Check vergleicht einen Messwert mit dem Vorwert. Was setzt er voraus?"
options:
  - "Ein besonders genaues Analysegerät"
  - "Eine korrekte Patientenidentität über alle Aufenthalte"
  - "Einen vorläufigen Befund"
answer: "Eine korrekte Patientenidentität über alle Aufenthalte"
explain: "Bei einer Dublette findet der Delta-Check keinen Vorwert, bei einer Verwechslung vergleicht er mit den Werten einer anderen Person. Hier schließt sich der Kreis zu ADT."
```

Das Ergebnis geht als HL7-v2-Nachricht `ORU^R01` zurück ins KIS (vereinfacht; `OBR` = Auftrag, `OBX` = einzelner Messwert):

```text
MSH|^~\&|LIS|LABOR|KIS|KLINIKUM|202610131512||ORU^R01|MSG0533|P|2.5
PID|1||4711^^^KLINIKUM^PI||Müller^Erika||19580312|F
OBR|1|A-77812|L-55301|ENTZ^Entzündungsparameter|||202610131420
OBX|1|NM|1988-5^CRP^LN||182|mg/L|<5|H|||F
OBX|2|NM|6690-2^Leukozyten^LN||15.8|10*3/uL|3.9-10.2|H|||F
```

```match
question: "Was bedeuten die markierten Teile der Ergebnisnachricht?"
options: ["Placer- und Filler-Nummer", "LOINC-Code: was genau gemessen wurde", "Wert, Einheit, Referenzbereich", "Flag: oberhalb des Referenzbereichs", "Status: endgültig"]
items:
  - item: "`A-77812|L-55301`"
    answer: "Placer- und Filler-Nummer"
  - item: "`1988-5^CRP^LN`"
    answer: "LOINC-Code: was genau gemessen wurde"
  - item: "`182|mg/L|<5`"
    answer: "Wert, Einheit, Referenzbereich"
  - item: "`H`"
    answer: "Flag: oberhalb des Referenzbereichs"
  - item: "`F` am Zeilenende"
    answer: "Status: endgültig"
explain: "Der LOINC-Code macht international eindeutig, was gemessen wurde – unabhängig vom lokalen Kürzel: semantische Interoperabilität. Ein vorläufiger Mikrobiologie-Befund hätte den Status P, eine Korrektur C. Das Flag H heißt „oberhalb des Referenzbereichs“, aber noch nicht automatisch „kritisch“."
```

## 5 · RIS/PACS und DICOM: vom Bildgebungsauftrag zum Befund mit Bildern

```timeline
title: "Der Röntgen-Thorax von Frau Müller in sieben Schritten"
events:
  - when: "1 · KIS"
    what: "Anforderung: Die Ärztin fordert einen Röntgen-Thorax an."
  - when: "2 · RIS"
    what: "Indikation und Termin: Die Radiologie prüft, plant Gerät und Zeit."
  - when: "3 · RIS → Modalität"
    what: "Worklist: Die Patientendaten gehen ans Gerät."
  - when: "4 · Modalität"
    what: "Untersuchung: Röntgen oder CT erzeugt Bilder."
  - when: "5 · PACS"
    what: "Bilder speichern, archivieren, verteilen."
  - when: "6 · PACS + RIS"
    what: "Befundung: Bilder ansehen, Befund diktieren."
  - when: "7 · KIS"
    what: "Befund und Bildlink im klinischen Kontext."
```

**Rechtfertigende Indikation:** Vor jeder Röntgen- oder CT-Untersuchung stellt eine fachkundige Ärztin oder ein fachkundiger Arzt fest, dass der Nutzen das Strahlenrisiko überwiegt (§ 83 StrlSchG) – ein Prozessschritt, den das RIS dokumentiert. Im Vergleich zum Labor folgt die Radiologie demselben Order/Result-Muster, aber mit Bildern statt Messwerten und zwei Spezialsystemen.

```match
question: "RIS oder PACS? Ordnen Sie die Aufgabe zu."
options: ["RIS", "PACS"]
items:
  - item: "Termine, Geräte und Personal planen"
    answer: "RIS"
  - item: "Bilder empfangen, speichern und langfristig archivieren"
    answer: "PACS"
  - item: "Arbeitslisten (Worklist) für die Modalitäten bereitstellen"
    answer: "RIS"
  - item: "Viewer und Vorbildvergleich"
    answer: "PACS"
  - item: "Befundtexte und Freigabe"
    answer: "RIS"
  - item: "Hunderte CT-Bilder schnell an Arbeitsplätze verteilen"
    answer: "PACS"
explain: "RIS ≈ spezialisiertes Auftrags- und Workflowsystem (die Text- und Prozesswelt), PACS ≈ spezialisiertes Daten- und Archivsystem (die Bildwelt). Das Bindeglied ist die **Accession Number**: eine Untersuchungsnummer, die das RIS vergibt und die in jedem Bild wieder auftaucht."
```

**Modality Worklist – kein Abtippen am CT:** Das Gerät fragt beim RIS nach den geplanten Untersuchungen und übernimmt Name, Geburtsdatum, Patienten-ID, Accession Number und Untersuchung; diese Daten stehen danach in jedem Bild (DICOM-Header), und das PACS ordnet die Bilder über Accession Number und Patienten-ID dem Auftrag zu. Ohne Worklist entstehen Tippfehler am Gerät – „Mueller“ statt „Müller“, falsche ID – und Bilder ohne Auftrag („verwaist“). Das ist dasselbe Prinzip wie der Barcode im Labor: einmal erfassen, dann nur noch weiterreichen. In IHE ist dieser Ablauf als Profil *Scheduled Workflow* beschrieben.

**DICOM ist mehr als ein Bildformat** (*Digital Imaging and Communications in Medicine*, seit 1993, Vorläufer ACR-NEMA 1985): ein **Dateiformat** mit Pixeldaten und Metadaten (Patient, Untersuchung, Gerät, Aufnahmeparameter), ein **Informationsmodell** mit fester Hierarchie, **Netzwerkdienste** (Speichern mit C-STORE, Suchen und Abrufen mit Query/Retrieve, Modality Worklist) und ein **Konformitätsmechanismus** (Conformance Statement der Hersteller). Ein JPEG eines Röntgenbilds ist medizinisch fast wertlos – ihm fehlt genau dieser Kontext.

```match
question: "DICOM-Hierarchie Patient → Study → Series → Instance: Auf welcher Ebene liegt das?"
options: ["Patient", "Study", "Series", "Instance"]
items:
  - item: "ID 4711 · Müller^Erika"
    answer: "Patient"
  - item: "CT-Thorax am Mittwoch mit Accession Number R-26-1231"
    answer: "Study"
  - item: "Lungenkernel-Rekonstruktion mit ca. 400 Bildern"
    answer: "Series"
  - item: "ein einzelnes Bild"
    answer: "Instance"
explain: "Jede Ebene hat eine weltweit eindeutige UID. Und jedes Bild trägt seinen vollständigen Kontext in sich – auch eine falsche Patientenzuordnung."
```

```reflect
question: "Aktivierung: Mittwoch, 09:20 – am CT wird in der Worklist versehentlich „Erika Möller“ statt „Erika Müller“ ausgewählt. Alle 801 Bilder sind technisch einwandfrei im PACS gespeichert, aber unter der falschen Patientin. Wer bemerkt es – und wann? Welche Folgen hat das für beide Patientinnen? Was muss in welchen Systemen korrigiert werden?"
intro: "Merke: **technisch fehlerfrei heißt nicht fachlich korrekt.** Erwartbare Punkte:"
answers:
  - "Bemerkt wird es oft erst bei der Befundung (der Befund passt nicht zur Anforderung) – oder gar nicht, wenn Frau Möller ebenfalls einen Thorax-Auftrag hatte."
  - "Frau Müller fehlt ein Befund, ihre Therapie verzögert sich."
  - "Frau Möller hat einen fremden Befund in der Akte, künftige Vorbildvergleiche werden falsch, und die Strahlenexposition ist der falschen Person zugeordnet."
  - "Korrigiert werden muss im PACS (Bilder umhängen, Header korrigieren), im RIS und im KIS – und in bereits weitergeleiteten Kopien (Teleradiologie, Forschungsplattform, Befund-CD). Dafür gibt es eigene Korrektur-Workflows, z. B. IHE Patient Information Reconciliation."
```

## 6 · Alles zusammen: ein Patientenfall, viele Systeme und eine Störung

Im Modul [[therapy]] haben Sie gesehen, dass eine Therapieentscheidung Daten aus vielen Quellen braucht. Hier sehen Sie, wie diese Daten tatsächlich fließen:

```timeline
title: "Frau Müllers erste Stunden als Nachrichtenfluss (vereinfacht)"
events:
  - when: "14:05"
    what: "Aufnahme `ADT^A01` an LIS, RIS und PACS"
  - when: "14:12"
    what: "Laborauftrag `OML^O21`"
  - when: "14:15"
    what: "Röntgenauftrag `ORM^O01` (neuer: `OMG^O19`)"
  - when: "14:50"
    what: "Worklist an die Modalität (DICOM, direkt)"
  - when: "15:05"
    what: "Bilder ins PACS (DICOM C-STORE, direkt)"
  - when: "15:12"
    what: "Laborbefund `ORU^R01`"
  - when: "15:40"
    what: "Röntgenbefund und Bildlink `ORU^R01`"
  - when: "18:40"
    what: "Verlegung `ADT^A02` an LIS, RIS und PACS"
```

Die HL7-v2-Nachrichten laufen über den Kommunikationsserver, zwischen RIS, Modalität und PACS wird DICOM meist direkt gesprochen. Das sind acht Nachrichten für ein paar Stunden einer einzigen Patientin – ein großes Klinikum verarbeitet täglich Hunderttausende. Was, wenn eine davon nicht ankommt?

```case
**Fehlerszenario.** 18:40 – die Verlegung ZNA → Intensivstation wird im KIS dokumentiert, `ADT^A02` wird erzeugt. 18:41 – die A02 an das LIS bleibt in der Queue des Kommunikationsservers hängen: Die LIS-Schnittstelle ist nach einem Update nicht erreichbar. 19:30 – die Blutkultur ist positiv, gramnegative Stäbchen. Das LIS sendet den Befund und löst die Telefonmeldung aus – an den Ort, den es kennt: „ZNA“.

Kein System hat einen „Fehler“ gemacht: KIS, LIS und Kommunikationsserver arbeiten jeweils korrekt – jedoch mit veraltetem Kontext.
```

```reflect
question: "Think – Pair – Share: Was könnte jetzt passieren? Wer merkt es – und wann? Wie hätte man es verhindern oder abfangen können?"
intro: "**Mögliche Folgen:** Der Befund landet in der ZNA-Arbeitsliste bzw. am ZNA-Drucker; die Telefonmeldung erreicht die ZNA, wo Frau Müller nicht mehr bekannt ist; Suche, Rückfragen, Zeitverlust; die Antibiotikatherapie wird verzögert angepasst; das ITS-Team sieht den Befund erst bei aktiver Suche in der Akte. **Gegenmaßnahmen:**"
answers:
  - "Monitoring des Kommunikationsservers: Queues, Quittungen (ACK), Alarme"
  - "Befunde patientenbezogen anzeigen, nicht nur ortsbezogen"
  - "kritische Werte an das behandelnde Team melden und die Rückbestätigung dokumentieren"
  - "Nachrichten nachliefern und Systeme regelmäßig abgleichen"
  - "klare Zuständigkeiten: Wer überwacht die Schnittstellen nachts?"
```

Das ist das sozio-technische Dreieck aus [[history]] in Reinform: Technik (Queue, ACK, Monitoring), Prozess (Meldeweg für kritische Werte) und Organisation (wer ist nachts zuständig?) müssen zusammenpassen – siehe auch [@sittig2010]. Und es knüpft an Hans Jonas an: Je größer die Reichweite technischer Systeme, desto größer die Verantwortung für ihre Folgen.

> **Schnittstellen sind kein IT-Detail, sondern Teil der Patientensicherheit.**

```match
question: "Synthese: Schnittstelle, Redundanz oder Ausfallrisiko?"
options: ["Schnittstelle", "Redundanz", "Ausfallrisiko"]
items:
  - item: "Analysegerät – Middleware – LIS"
    answer: "Schnittstelle"
  - item: "Patientenstammdaten als Kopie in KIS, LIS, RIS und PACS"
    answer: "Redundanz"
  - item: "verlorene ADT-Ereignisse und dadurch veraltete Kopien"
    answer: "Ausfallrisiko"
  - item: "RIS – Modalität – PACS"
    answer: "Schnittstelle"
  - item: "Befunde in LIS und KIS"
    answer: "Redundanz"
  - item: "Direktverbindungen ohne Monitoring"
    answer: "Ausfallrisiko"
  - item: "Papier-Notfallprozesse, die niemand geübt hat"
    answer: "Ausfallrisiko"
explain: "Redundanz ist nicht per se schlecht – Kopien machen Systeme schnell und ausfallsicher –, aber jede Kopie muss synchron gehalten werden. Übertragen Sie diese drei Fragen auf jeden neuen Patientenfall oder jedes neue System."
```

## Take-home Messages

1. **Krankenhaus-IT ist eine Systemlandschaft.** All-in-One vs. Best-of-Breed und Spaghetti vs. Stern sind zwei unabhängige Fragen.
2. **ADT liefert den gemeinsamen Kontext.** Wer? Welcher Fall? Wo? – Alle anderen Systeme hängen davon ab.
3. **Order/Result ist das gemeinsame Muster.** Labor und Radiologie folgen demselben Kreislauf – bis zur Kenntnisnahme.
4. **DICOM ist mehr als ein Bildformat.** Datenmodell, Metadaten und Kommunikation; die Accession Number verbindet Auftrag und Bilder.
5. **Integration ist Patientensicherheit.** Identität, Nachrichtenfluss und Monitoring entscheiden, ob der richtige Befund rechtzeitig ankommt.

## Ausblick: Was wir in HL7 FHIR wiederverwenden

Alles, was Sie hier konzeptionell gelernt haben, taucht in FHIR als Ressource wieder auf – die Konzepte bleiben, nur die technische Form ändert sich.

```match
question: "Welche FHIR-Ressource entspricht dem Konzept?"
options: ["Patient", "Encounter", "ServiceRequest", "Observation", "DiagnosticReport", "ImagingStudy"]
items:
  - item: "Patientin, Patienten-ID"
    answer: "Patient"
  - item: "Fall, Bewegung"
    answer: "Encounter"
  - item: "Auftrag (Order)"
    answer: "ServiceRequest"
  - item: "einzelner Messwert (OBX)"
    answer: "Observation"
  - item: "Befund"
    answer: "DiagnosticReport"
  - item: "DICOM-Study"
    answer: "ImagingStudy"
```

In den nächsten Wochen folgen HL7 v2 im Detail (Segmente, Felder, Quittungen), IHE-Profile wie *Scheduled Workflow* und Terminologien wie LOINC und SNOMED CT für die semantische Interoperabilität.

## Selbsttest

```quiz
question: "Warum braucht fast jedes System eine aktuelle Kopie des ADT-Kontexts?"
options:
  - "Weil das KIS keine Datenbank hat"
  - "Weil Zuordnung, Vorwerte, Befundrouting und Abrechnung von Patient, Fall und Ort abhängen"
  - "Weil HL7 v2 es vorschreibt"
answer: "Weil Zuordnung, Vorwerte, Befundrouting und Abrechnung von Patient, Fall und Ort abhängen"
```

```quiz
question: "Was verbindet einen Auftrag im RIS mit den Bildern im PACS?"
options: ["die Patienten-ID allein", "die Accession Number", "der Dateiname der Bilder"]
answer: "die Accession Number"
```

```quiz
question: "Eine Best-of-Breed-Landschaft ist …"
options:
  - "… immer eine Spaghetti-Architektur"
  - "… nicht automatisch Spaghetti – sie kann sauber über einen Kommunikationsserver integriert sein"
  - "… immer besser interoperabel als eine All-in-One-Suite"
answer: "… nicht automatisch Spaghetti – sie kann sauber über einen Kommunikationsserver integriert sein"
```
