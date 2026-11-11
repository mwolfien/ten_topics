---
title: "Kommunikationsstandards I: HL7 v2, CDA, DICOM und IHE-Profile"
summary: "Frau Müller wird entlassen – und ihre Daten, ihr Arztbrief und ihre Bilder müssen das Krankenhaus verlassen. Wie tauschen Systeme Daten, Dokumente und Bilder standardisiert und zuverlässig aus? HL7 v2, CDA, DICOM, IHE-Profile, Kommunikationsmuster und xDT am Fall."
duration_minutes: 75
level: "Vertiefung"
audiences: [med, cs, clin, tech, pat]
order: 6
builds_on: [information-systems]
course: his
lecture: 4
author: "Kathrin Sobe"
objectives:
  - "Erklären, wofür HL7 v2, CDA und DICOM eingesetzt werden, und sie typischen Szenarien zuordnen (Daten, Dokumente, Bilder)"
  - "Eine HL7-v2-Nachricht (ADT, ORM, ORU) lesen und erläutern, wie Quittungen den Austausch zuverlässig machen"
  - "Den Aufbau eines CDA-Arztbriefs und das Grundprinzip der Bildkommunikation mit DICOM beschreiben"
  - "Begründen, wie IHE-Profile, Kommunikationsmuster, Kommunikationsserver und xDT den Austausch über System- und Sektorgrenzen ermöglichen"
readings: [winter2023, benson2021, dolin2006]
related_topics: [fhir, ehr-cis, data-sharing, etl, privacy-ethics]
source: "Vorlesung 4 „Kommunikationsstandards I: HL7 v2, CDA, DICOM und IHE-Profile“, Informationssysteme im Gesundheitswesen (WiSe 2026/27), Kathrin Sobe, IMB & ZMI"
---

> **Leitfrage:** Wie tauschen unterschiedliche medizinische Informationssysteme Daten, Dokumente und Bilder standardisiert und zuverlässig miteinander aus?

Im Modul [[information-systems]] haben Sie gesehen, wie KIS, LIS und RIS/PACS im Krankenhaus zusammenarbeiten, und dabei einzelne HL7-Nachrichten und DICOM-Begriffe schon gestreift – bewusst nur oberflächlich. Jetzt nehmen wir die **Standards selbst** in den Blick: Wozu ist ein Standard da, wie ist er gebaut, warum ist er so entstanden – und wo liegen seine Grenzen? Drei Objektarten strukturieren das Modul:

| Objektart | Eigenschaften | Standard |
|---|---|---|
| **Daten** | kleinteilig, ereignisbezogen – „Patientin entlassen“ | HL7 v2 |
| **Dokumente** | abgeschlossen, verantwortet, signierbar – ein Arztbrief | HL7 CDA |
| **Bilder** | große Objekte mit vielen Metadaten | DICOM |

Dazu kommen **Abläufe** (IHE-Profile), die **Vermittlung** (Kommunikationsmuster und Kommunikationsserver) und der **ambulante Sektor** (xDT).

```persona med
Arztbriefe, Laborbefunde und Vorbilder erreichen Sie über genau diese Standards – oder eben nicht. Wer versteht, was ein „Level-1-Arztbrief“ ist oder warum ein Befund als „korrigiert“ nachkommt, liest Befunde sicherer.
```

```persona cs
HL7 v2 ist eine Grammatik mit Trennzeichen, CDA ein XML-Schema mit Referenzmodell, DICOM ein Objektmodell mit ausgehandelten Verbindungen, IHE eine Sammlung von Sequenzdiagrammen. Sie werden Muster aus Protokollen, Parsern und Message-Brokern wiedererkennen.
```

```persona clin
Warum kommt der Entlassbrief in der Praxis als PDF an, obwohl er „strukturiert“ sein sollte? Warum fehlen die Vorbilder? Dieses Modul zeigt, an welcher Stelle der Kette die Antwort liegt.
```

```persona tech
MLLP, ACK, Association, Storage Commitment, Mapping-Tabellen im Kommunikationsserver und Austauschverzeichnisse für xDT: Das Modul ist eine Landkarte der Schnittstellen, die Sie betreiben.
```

```persona pat
Ihr Arztbrief, Ihre Laborwerte und Ihre Röntgenbilder wandern zwischen Klinik, Hausarztpraxis und Radiologie. Dieses Modul zeigt, welche „Sprachen“ die Systeme dafür sprechen – und warum dabei manchmal etwas verloren geht.
```

```case
**Frau Erika Müller** (*12.03.1958, Patienten-ID 4711, Fall F2026-0815, ambulant erworbene Pneumonie) – die Patientin aus [[information-systems]]. **Tag 9, 21.10.:** Sie wird entlassen.

1. **Entlassung:** Der Fall wird abgeschlossen – alle Subsysteme müssen es erfahren.
2. **Entlassbrief:** wird erstellt, ärztlich freigegeben und an die Hausärztin übermittelt.
3. **Bilder:** Röntgen (13.10.) und CT (14.10.) liegen im PACS des Klinikums.
4. **Hausarztpraxis:** Kontrolle mit EKG am Gerät, CRP über die Laborgemeinschaft.
5. **Kontroll-Röntgen:** einige Wochen später in einer radiologischen Praxis – mit Vergleich zu den Vorbildern.

**Neu gegenüber der letzten Vorlesung:** Die Informationen verlassen das Krankenhaus. Andere Hersteller, andere Sektoren, keine gemeinsame Datenbank, kein gemeinsamer Kommunikationsserver – **nur noch gemeinsame Standards.** (Fiktiver Fall.)
```

```reflect
question: "Aktivierung (30 Sekunden): Was müssten Klinikum, Hausarztpraxis und radiologische Praxis miteinander vereinbaren, damit das funktioniert?"
answers:
  - "**Wie** die Daten ankommen (Transport, Verbindung, Quittung)"
  - "**Wie** sie aufgebaut sind (Format, Struktur)"
  - "**Was** sie bedeuten (gemeinsame Codes, z. B. für Diagnosen und Laborwerte)"
  - "**Wer** wann was mit wem austauschen darf (Abläufe, Verträge, Einwilligung der Patientin)"
  - "Genau diese vier Ebenen ordnet der nächste Abschnitt."
```

## Was ein Standard festlegen muss: vier Ebenen

| Ebene | Leitfrage | Standards (Beispiele) | Bei Frau Müller |
|---|---|---|---|
| **Organisatorisch** | Wer tauscht wann was mit wem aus? | IHE-Profile, Verträge, Einwilligung | Vorbilder-Abruf durch die radiologische Praxis |
| **Semantisch** | Was bedeutet der Inhalt? | LOINC, ICD-10-GM, SNOMED CT | Entlassdiagnose J18.9 (ICD-10-GM) |
| **Syntaktisch / strukturell** | Wie ist die Einheit aufgebaut? | HL7 v2, CDA, DICOM, xDT | Entlassbrief als CDA-XML |
| **Technisch** | Kommt sie überhaupt an? | TCP/MLLP, DICOM-Association, HTTP, Datei | `ADT^A03` per MLLP an das LIS |

Die Ebenen folgen der Interoperabilitäts-Definition der HIMSS (*foundational, structural, semantic, organizational*). **Merke: Ein Syntaxstandard allein garantiert keine Interoperabilität.** Fragen Sie bei jedem Standard: Welche Ebene deckt er ab – und welche nicht?

```match
question: "Auf welcher Ebene liegt das Problem?"
options: ["Technisch", "Syntaktisch / strukturell", "Semantisch", "Organisatorisch"]
items:
  - item: "Die Verbindung zum LIS ist nach einem Update unterbrochen."
    answer: "Technisch"
  - item: "Das KIS erwartet HL7 v2.5, das LIS sendet v2.3 mit anderer Segmentfolge."
    answer: "Syntaktisch / strukturell"
  - item: "Das Labor schickt den CRP-Wert mit dem Hauscode „CRP“, das KIS kennt nur LOINC."
    answer: "Semantisch"
  - item: "Niemand hat geregelt, ob die radiologische Praxis die Vorbilder abrufen darf."
    answer: "Organisatorisch"
```

Diese Landkarte zeigt, wo welcher Standard eingesetzt wird:

| | Ambulant: Arztpraxis | Stationär: Klinikum | Über die Grenze |
|---|---|---|---|
| **Daten** | xDT: GDT (Geräte), LDT (Labor), KVDT (Abrechnung) | HL7 v2 (ADT, ORM, ORU) über den Kommunikationsserver | – |
| **Dokumente** | Arztbrief im Praxisverwaltungssystem (PVS) | CDA-Entlassbrief aus dem KIS | Versand per KIM oder Bereitstellung über IHE XDS |
| **Bilder** | radiologische Praxis | DICOM: Worklist, Store, PACS | IHE XDS-I.b |

IHE-Profile erfinden keine neuen Formate, sondern legen fest, **wie die Standards für einen Ablauf zusammenspielen**.

## 1 · HL7 v2: Ereignisse als Nachrichten – und ihre Quittung

**HL7 Version 2** ist ein **ereignisgesteuerter Nachrichtenstandard**: Im Quellsystem passiert etwas – Frau Müller wird entlassen –, und dieses Ereignis (*trigger event*) löst eine Nachricht aus. Herausgeber ist HL7 International (gegründet 1987, ANSI-akkreditiert). Entstanden ist HL7, weil Krankenhäuser in den 1980er Jahren immer mehr Abteilungssysteme mit herstellerspezifischen Schnittstellen hatten – das Spaghetti-Problem aus [[information-systems]].

```quiz
question: "Wofür steht die „7“ in Health Level 7?"
options:
  - "Für die siebte Version des Standards"
  - "Für die Anwendungsschicht, Schicht 7 des OSI-Modells"
  - "Für die sieben Gründungsmitglieder"
answer: "Für die Anwendungsschicht, Schicht 7 des OSI-Modells"
explain: "HL7 regelt **Inhalte**, nicht den Transport. Den Transport übernimmt meist TCP mit MLLP (siehe unten)."
```

Die Versionen reichen von 2.0 (1988) bis 2.9 (Dezember 2019) mit der Unterversion 2.9.1; in vielen Häusern laufen ältere Versionen wie 2.3 oder 2.5 parallel. Neue Felder werden hinten angehängt, alte nicht entfernt – v2 ist **rückwärtskompatibel**, und das erklärt seine Langlebigkeit. HL7 Version 3 (XML, Referenzinformationsmodell RIM) hat sich im Nachrichtenbereich kaum durchgesetzt; der strategische Nachfolger ist [[topic:fhir]].

### Die Entlassung, feldgenau

Die Entlassung ist ein `ADT^A03` (Version 2.5, vereinfacht; „…“ steht für ausgelassene leere Felder):

```text
MSH|^~\&|KIS|KLINIKUM|KOMSERVER|KLINIKUM|20261021110000||ADT^A03^ADT_A03|MSG0918|P|2.5
EVN|A03|20261021110000
PID|1||4711^^^KLINIKUM^PI||Müller^Erika||19580312|F
PV1|1|I|P3^12^A|…|F2026-0815|…|01|…|20261021110000
```

Eine Besonderheit: Die Trennzeichen werden **in der Nachricht selbst** deklariert, in MSH-1 (`|`) und MSH-2 (`^~\&`). Felder sind keine einfachen Strings, sondern haben **Datentypen**: PID-3 ist vom Typ CX (ID^^^Vergabestelle^ID-Typ), PID-5 vom Typ XPN (Nachname^Vorname), PV1-3 vom Typ PL (Station^Zimmer^Bett), Zeitstempel folgen dem Muster JJJJMMTThhmmss. Für die Entlassung relevant sind PV1-19 (Fallnummer), PV1-36 (Entlassart, `01` = nach Hause) und PV1-45 (Entlasszeitpunkt).

```match
question: "Was steht in welchem Feld des Nachrichtenkopfs (MSH)?"
options: ["Trennzeichen und Kodierzeichen", "sendende Anwendung", "empfangende Anwendung", "Nachrichtentyp ^ Ereignis ^ Struktur", "Kontroll-ID", "Verarbeitungsmodus (P = Produktion)", "HL7-Version"]
items:
  - item: "MSH-1 / MSH-2: `|` und `^~\\&`"
    answer: "Trennzeichen und Kodierzeichen"
  - item: "MSH-3: `KIS`"
    answer: "sendende Anwendung"
  - item: "MSH-5: `KOMSERVER`"
    answer: "empfangende Anwendung"
  - item: "MSH-9: `ADT^A03^ADT_A03`"
    answer: "Nachrichtentyp ^ Ereignis ^ Struktur"
  - item: "MSH-10: `MSG0918`"
    answer: "Kontroll-ID"
  - item: "MSH-11: `P`"
    answer: "Verarbeitungsmodus (P = Produktion)"
  - item: "MSH-12: `2.5`"
    answer: "HL7-Version"
explain: "Auf die Kontroll-ID MSG0918 bezieht sich gleich die Quittung."
```

### ADT, ORM und ORU: Kontext, Auftrag, Ergebnis

**Merkhilfe:** ADT sagt, *wer und wo*; ORM, *was gemacht werden soll*; ORU, *was herausgekommen ist*. Die wichtigsten ADT-Ereignisse kennen Sie: A01 Aufnahme, A02 Verlegung, A03 Entlassung, A04 ambulante Registrierung, A08 Änderung der Patientendaten, A40 Zusammenführung von IDs.

Der Röntgenauftrag vom 13.10. als `ORM^O01` und die CRP-Kontrolle vor der Entlassung als `ORU^R01`:

```text
MSH|^~\&|KIS|KLINIKUM|RIS|RADIOLOGIE|20261013141500||ORM^O01^ORM_O01|MSG0412|P|2.5
PID|1||4711^^^KLINIKUM^PI||Müller^Erika||19580312|F
ORC|NW|A-77830^KIS
OBR|1|A-77830^KIS||RTHO^Röntgen-Thorax^L

MSH|^~\&|LIS|LABOR|KIS|KLINIKUM|20261021073000||ORU^R01^ORU_R01|LAB5120|P|2.5
PID|1||4711^^^KLINIKUM^PI||Müller^Erika||19580312|F
OBR|1|A-77950^KIS|L-56012^LIS|CRP^CRP-Kontrolle^L
OBX|1|NM|1988-5^C-reaktives Protein^LN||12|mg/L|<5|H|||F
```

Ein Auftrag besteht aus **ORC** (Auftragssteuerung, `NW` = neuer Auftrag) und **OBR** (was angefordert wird); ein Ergebnis aus OBR und einem oder mehreren **OBX** (einzelne Beobachtung). Vereinfacht: ORM = MSH · PID · { ORC · OBR }, ORU = MSH · { PID · { OBR · { OBX } } }. Neuere HL7-Versionen nutzen für Aufträge spezialisiertere Nachrichten, etwa OML für das Labor.

```quiz
question: "Woran erkennt das KIS, dass der CRP-Wert final ist – und was passiert bei einer späteren Korrektur?"
options:
  - "Am `H` – bei einer Korrektur wird die Nachricht gelöscht"
  - "Am `F` in OBX-11 – bei einer Korrektur schickt das Labor eine neue ORU mit `C`"
  - "An der Kontroll-ID – bei einer Korrektur wird sie hochgezählt"
answer: "Am `F` in OBX-11 – bei einer Korrektur schickt das Labor eine neue ORU mit `C`"
explain: "`F` = final, `C` = korrigiert, `P` = vorläufig. `H` ist nur das Kennzeichen „oberhalb des Referenzbereichs“."
```

### Struktur, Transport und Quittung

Drei Dinge machen aus Text eine **zuverlässige** Kommunikation:

1. **Struktur:** Die abstrakte Nachrichtendefinition legt fest, welche Segmente in welcher Reihenfolge kommen – für ADT_A03 etwa `MSH EVN PID [PD1] PV1 [PV2] [{DG1}] [{OBX}]`; `[ ]` heißt optional, `{ }` wiederholbar. Das ist eine Grammatik, vergleichbar mit einem XML-Schema.
2. **Transport:** HL7 regelt nur die Anwendungsschicht. Übertragen wird meist über TCP mit dem **Minimal Lower Layer Protocol (MLLP)**: ein Startbyte `0x0B`, die Nachricht (Segmente mit CR getrennt), die Endbytes `0x1C 0x0D`. So weiß der Empfänger im Bytestrom, wo eine Nachricht beginnt und endet.
3. **Quittung:** Der Empfänger antwortet mit einem **ACK**; im MSA-Segment stehen ein Code und die Kontroll-ID der ursprünglichen Nachricht.

```text
MSH|^~\&|KOMSERVER|KLINIKUM|KIS|KLINIKUM|20261021110001||ACK^A03^ACK|ACK7731|P|2.5
MSA|AA|MSG0918
```

```match
question: "Was bedeutet der Code in MSA-1?"
options: ["angenommen", "Fehler beim Verarbeiten", "abgelehnt"]
items:
  - item: "`AA` (Application Accept)"
    answer: "angenommen"
  - item: "`AE` (Application Error)"
    answer: "Fehler beim Verarbeiten"
  - item: "`AR` (Application Reject)"
    answer: "abgelehnt"
explain: "Im erweiterten Modus (MSH-15/-16) gibt es zusätzlich eine reine Empfangsbestätigung mit CA, CE und CR."
```

```quiz
question: "Das KIS erhält auf die A03 kein ACK. Was ist richtig?"
options:
  - "Das KIS geht davon aus, dass alles angekommen ist."
  - "Das KIS sendet erneut; die Kontroll-ID erlaubt dem Empfänger, Duplikate zu erkennen."
  - "Das KIS schickt eine neue A03 mit neuer Kontroll-ID."
answer: "Das KIS sendet erneut; die Kontroll-ID erlaubt dem Empfänger, Duplikate zu erkennen."
explain: "Genau dieser Mechanismus – plus Monitoring der ausbleibenden Quittungen – hätte die hängende Queue im Fehlerszenario aus [[information-systems]] sichtbar gemacht."
```

### HL7 v2 kritisch betrachtet

| Stärken | Schwächen |
|---|---|
| einfach, kompakt, schnell zu parsen | viele optionale Felder → jede Schnittstelle ist anders |
| riesige installierte Basis, Werkzeuge, Know-how | Z-Segmente für Hausspezifisches |
| rückwärtskompatibel – Systeme altern in Ruhe | kein formales Informationsmodell, Semantik oft lokal |
| Ereignisorientierung passt zu klinischen Abläufen | keine eingebaute Sicherheit (TLS oder abgesichertes Netz nötig) |

> „Kennt man eine HL7-v2-Schnittstelle, kennt man genau eine.“ – geflügeltes Wort der Community

```reflect
question: "Zur Diskussion: Ist die Flexibilität von HL7 v2 Erfolgsfaktor oder Geburtsfehler? Und würden Sie eine intern stabil laufende v2-Landschaft auf FHIR migrieren? Halten Sie Ihre Antwort fest – in der nächsten Vorlesung kommen wir darauf zurück."
answers:
  - "**Erfolgsfaktor:** Die Flexibilität hat v2 überhaupt erst einsetzbar gemacht – jedes Haus konnte es an seine Abläufe anpassen, und alte Systeme blieben anschlussfähig."
  - "**Geburtsfehler:** Dieselbe Flexibilität macht jede Schnittstelle zum Einzelstück: Mapping, Tests und Pflege kosten dauerhaft Geld, und Semantik bleibt lokal."
  - "**Migration:** Innerhalb des Hauses lohnt sie sich selten allein – oft laufen v2 intern und FHIR für neue, einrichtungsübergreifende oder App-basierte Anwendungsfälle parallel, und der Kommunikationsserver übersetzt."
```

## 2 · Dokumente: HL7 CDA

Die **Clinical Document Architecture (CDA)** ist ein XML-basierter HL7-Standard für Struktur und Semantik klinischer Dokumente – Arztbrief, Befundbericht, Entlassbrief [@dolin2006]. Sie ist aus dem Referenzinformationsmodell (RIM) von HL7 v3 abgeleitet, damit der erfolgreichste Teil der v3-Familie, und als ISO/HL7 27932:2009 auch internationale Norm. Release 1 erschien 2000, Release 2 2005, Release 2.1 2019; implementiert wird überwiegend R2. Verbreitet ist CDA etwa in den USA als Consolidated CDA (C-CDA), in Österreich als Grundlage der ELGA-Dokumente und in Deutschland über Arztbrief-Leitfäden (VHitG-Arztbrief 2006, HL7 Deutschland).

**Warum ein eigener Standard neben HL7 v2?** Weil Medizin **dokumentenzentriert** ist: Frau Müllers Entlassbrief ist ein abgeschlossenes Werk, für das eine Ärztin verantwortlich zeichnet, das unverändert archiviert werden muss und das ein Mensch lesen können muss. Nachrichten allein bilden das nicht ab.

```match
question: "Sechs Eigenschaften eines klinischen Dokuments nach CDA: Welche ist gemeint?"
options: ["Persistenz", "Verantwortung (Stewardship)", "Authentifizierbarkeit", "Kontext", "Ganzheit (Wholeness)", "Menschenlesbarkeit"]
items:
  - item: "Der Brief bleibt über die gesetzliche Aufbewahrungsfrist unverändert erhalten."
    answer: "Persistenz"
  - item: "Das Klinikum ist für die Verwahrung des Dokuments zuständig."
    answer: "Verantwortung (Stewardship)"
  - item: "Eine Ärztin gibt den Brief frei und kann ihn signieren."
    answer: "Authentifizierbarkeit"
  - item: "Patientin, Aufenthalt und Verfasser gelten für den ganzen Inhalt, ohne jeweils wiederholt zu werden."
    answer: "Kontext"
  - item: "Freigegeben wird der Brief als Ganzes, nicht Abschnitt für Abschnitt."
    answer: "Ganzheit (Wholeness)"
  - item: "Die Hausärztin kann ihn ohne Spezialsoftware lesen."
    answer: "Menschenlesbarkeit"
```

### Header, Body und die drei Level

Ein CDA-Dokument hat zwei Hauptteile. Der **Header** ist immer strukturiert und beantwortet: Um wen geht es (`recordTarget`), wer hat es verfasst (`author`), welche Einrichtung verwahrt es (`custodian`), wer ist rechtlich verantwortlich (`legalAuthenticator`), in welchem Aufenthalt ist es entstanden (`encompassingEncounter`) – dazu Dokumenttyp, Datum und Vertraulichkeit. Deshalb lassen sich CDA-Dokumente in Registern verwalten, selbst wenn der Inhalt nur ein PDF ist. Der **Body** enthält Abschnitte (`section`) mit Code, Titel und **Text**; der Text ist der **verbindliche** Inhalt, `entry`-Elemente können dieselben Aussagen zusätzlich codiert enthalten.

```text
<ClinicalDocument xmlns="urn:hl7-org:v3">
  <typeId root="2.16.840.1.113883.1.3" extension="POCD_HD000040"/>
  <id root="1.2.3.999" extension="EB-2026-0815"/>   <!-- fiktive OID -->
  <code code="18842-5" codeSystem="2.16.840.1.113883.6.1"
        displayName="Discharge summary"/>          <!-- LOINC -->
  <title>Entlassbrief</title>
  <effectiveTime value="20261021"/>
  <confidentialityCode code="N" codeSystem="2.16.840.1.113883.5.25"/>
  <recordTarget> … Erika Müller, *12.03.1958, ID 4711 … </recordTarget>
  <author> … Dr. A. Beispiel, Innere Medizin … </author>
  <custodian> … Klinikum … </custodian>
  <legalAuthenticator> … </legalAuthenticator>
  <component><structuredBody>
    <component><section>
      <code code="11535-2" codeSystem="2.16.840.1.113883.6.1"/>
      <title>Entlassdiagnose</title>
      <text>Ambulant erworbene Pneumonie (ICD-10-GM J18.9)</text>
      <entry> … codierte Diagnose (Level 3) … </entry>
    </section></component>
  </structuredBody></component>
</ClinicalDocument>
```

Der Text wird typischerweise per XSLT-Stylesheet als HTML dargestellt. In Deutschland legen Leitfäden von HL7 Deutschland Templates und Pflichtinhalte fest – hier bewusst weggelassen. **Ohne Leitfäden ist CDA ähnlich offen wie HL7 v2.**

```match
question: "Derselbe Entlassbrief auf drei Stufen: Welches Level ist gemeint?"
options: ["Level 1", "Level 2", "Level 3"]
items:
  - item: "Header strukturiert, Inhalt nur als eingebettetes PDF (`nonXMLBody`) – lesbar, aber nicht auswertbar"
    answer: "Level 1"
  - item: "Der Abschnitt ist per LOINC 11535-2 codiert – eine Software findet „Entlassdiagnose“, liest aber nur Text"
    answer: "Level 2"
  - item: "Zusätzlich enthält ein `entry` die Diagnose J18.9 codiert – maschinell auswertbar, der Text bleibt verbindlich"
    answer: "Level 3"
explain: "Die Stufung ist ein **Migrationspfad**: Man startet mit Level 1 und liefert schrittweise mehr Struktur."
```

### CDA im Vergleich und kritisch betrachtet

| Kriterium | PDF/A (Brief als Datei) | HL7 CDA R2 | FHIR-Document (Bundle) |
|---|---|---|---|
| menschenlesbar | ja | ja (Stylesheet) | ja (Narrative) |
| maschinenlesbar | kaum | je nach Level 1–3 | ja, ressourcenbasiert |
| Signatur / Persistenz | ja | ja, Kernkonzept | ja, Kernkonzept |
| Format / Technologie | Binär-Layout | XML, v3-RIM | JSON/XML, REST |
| Einstiegshürde | gering | hoch (RIM, Templates) | mittel |

Der Vergleich ist eine didaktische Vereinfachung. **Kritik:** In der Praxis bleibt es oft bei Level 1 – ein strukturiertes PDF im XML-Umschlag; Text und entries können sich widersprechen; die Komplexität des RIM schreckt Entwickler ab. CDA löst das Dokumentproblem, das Nachrichtenstandards offenlassen – sein Nutzen wächst mit dem Strukturierungsgrad und mit verbindlichen Leitfäden. FHIR übernimmt das Dokumentkonzept, macht die Inhalte aber auch einzeln nutzbar.

```reflect
question: "Zur Diskussion: Was ist im Streitfall „der Arztbrief“ – der signierte Text oder die codierten Daten? Und wer haftet, wenn eine Software in der Hausarztpraxis nur die entries auswertet?"
answers:
  - "Nach CDA ist der **Text verbindlich** – die entries sind eine maschinenlesbare Zusatzdarstellung."
  - "Widersprechen sich beide, kann eine Software, die nur die entries auswertet, zu falschen Schlüssen führen. Verantwortlich sind dann mehrere: der Hersteller des erzeugenden Systems (Konsistenz von Text und entries), der Hersteller der auswertenden Software (Umgang mit Widersprüchen) und die Nutzer:innen, die sich darauf verlassen."
  - "Leitfäden und Konformitätsprüfungen reduzieren das Risiko – lösen es aber nicht vollständig."
```

## 3 · Bilder: DICOM

Der Brief allein reicht der Radiologin in der Praxis nicht – sie braucht die Bilder: das Röntgen-Thorax vom 13.10. (Accession-Nr. R-26-1188) und das CT vom 14.10. (R-26-1231, mehrere Serien, rund 800 Einzelbilder).

```reflect
question: "Aktivierung (2 Minuten): Welche Informationen braucht die Radiologin außer den Bildpunkten, um sicher zu vergleichen? Warum genügt es nicht, die Bilder als JPEG per E-Mail zu schicken? Wer muss dafür mit wem sprechen?"
answers:
  - "Patient, Untersuchung, Datum, Gerät, Körperseite, Lagerung, Maßstab und Aufnahmeparameter – also genau die Metadaten, die ein DICOM-Objekt mitträgt."
  - "Ein JPEG verliert diesen Kontext, die volle Bildtiefe und die Zuordnung zu Patientin und Auftrag; per E-Mail kommen außerdem Datenschutz und Verlässlichkeit hinzu."
  - "Klinikum und Praxis brauchen einen abgestimmten Ablauf (wer darf welche Vorbilder abrufen?) – das ist die organisatorische Ebene, die IHE-Profile wie XDS-I adressieren."
```

**DICOM** (*Digital Imaging and Communications in Medicine*) ist zugleich **Datenmodell, Dateiformat und Netzwerkprotokoll**, auch als ISO 12052 normiert, gepflegt vom DICOM Standards Committee (Sekretariat bei NEMA/MITA) und mehrmals im Jahr als neue Edition veröffentlicht (Teile PS3.x). Anfang der 1980er Jahre waren CT- und MR-Bilder praktisch nur mit der Software des Geräteherstellers lesbar; ACR und NEMA bildeten 1983 ein gemeinsames Komitee.

```timeline
title: "Von ACR-NEMA zu DICOMweb"
events:
  - when: "1985"
    what: "ACR-NEMA 1.0 – Punkt-zu-Punkt, eigene Hardwareschnittstelle"
  - when: "1988"
    what: "ACR-NEMA 2.0 – erweitert, weiterhin kein Netzwerk"
  - when: "1993"
    what: "DICOM 3.0 – TCP/IP, Objektmodell, Dienste: die Grundlage bis heute"
  - when: "ab 2000er"
    what: "DICOMweb – HTTP/REST-Dienste (WADO-RS, QIDO-RS, STOW-RS)"
```

### Dienste, Rollen und Verbindungsaufbau

Aus [[information-systems]] kennen Sie den Aufbau eines DICOM-Objekts (Patient → Study → Series → Instance). Jetzt: Wie werden Objekte **bewegt**?

- **SOP-Klasse** = Informationsobjekt + Dienst, jeweils mit weltweit eindeutiger UID – etwa *CT Image Storage* (1.2.840.10008.5.1.4.1.1.2) oder *Modality Worklist – FIND* (1.2.840.10008.5.1.4.31).
- **Rollen:** Der *Service Class User* (SCU) nimmt einen Dienst in Anspruch, der *Service Class Provider* (SCP) erbringt ihn. Beim Speichern ist die Modalität SCU, das PACS SCP. Adressiert wird über **AE Title + IP + Port** (registriert: 104, häufig 11112).
- **Association:** Anders als bei HL7 v2 wird zuerst **verhandelt**: Die Modalität schlägt SOP-Klassen und Kodierungen (*Transfer Syntaxes*) vor (A-ASSOCIATE-RQ), das PACS bestätigt, was es unterstützt (A-ASSOCIATE-AC). Erst dann folgt der Dienst, etwa C-STORE, und am Ende die geordnete Freigabe (A-RELEASE). Passen die Fähigkeiten nicht zusammen, scheitert die Verhandlung mit einer klaren Fehlermeldung statt mit kaputten Daten.
- **Dienste:** C-Dienste für zusammengesetzte Objekte wie Bilder (C-ECHO, C-STORE, C-FIND, C-MOVE, C-GET), N-Dienste für normalisierte Objekte wie Statusmeldungen (N-CREATE, N-SET …). *Implicit VR Little Endian* muss jedes System beherrschen.

```match
question: "Das Röntgen-Thorax von Frau Müller: Bringen Sie die DICOM-Schritte in die richtige Reihenfolge."
options: ["1", "2", "3", "4", "5"]
items:
  - item: "C-FIND Modality Worklist: „Wer ist dran?“ – die Modalität übernimmt die Patientendaten vom RIS"
    answer: "1"
  - item: "MPPS (N-CREATE/N-SET): Untersuchung begonnen bzw. beendet"
    answer: "2"
  - item: "C-STORE: Bilder ans PACS"
    answer: "3"
  - item: "Storage Commitment: Sind die Bilder sicher archiviert?"
    answer: "4"
  - item: "Suchen und Laden an der Befundworkstation: C-FIND/C-MOVE oder QIDO-RS/WADO-RS"
    answer: "5"
explain: "DICOMweb (PS3.18) bietet dieselben Funktionen über HTTP/REST – darauf basieren viele Web-Viewer."
```

```quiz
question: "Eine Modalität löscht Bilder lokal, bevor sie sicher im Archiv sind. Welcher Schritt fehlt?"
options: ["Modality Worklist", "MPPS", "Storage Commitment", "C-ECHO"]
answer: "Storage Commitment"
explain: "Storage Commitment ist das **DICOM-Gegenstück zum HL7-ACK**: Erst wenn das PACS die sichere Archivierung bestätigt, darf die Modalität löschen."
```

### DICOM kritisch betrachtet

**Erfolgsfaktoren:** herstellerübergreifend akzeptiert, Bild und Metadaten untrennbar, kontinuierliche Pflege durch Supplements; Hersteller legen im **Conformance Statement** (PS3.2) offen, was ihre Geräte können. **Probleme:** Ein Conformance Statement garantiert kein Zusammenspiel; *private Tags* enthalten herstellerspezifische Inhalte; die Datenmengen sind enorm (CT, digitale Pathologie); ohne Worklist entstehen Fehlzuordnungen. **Sicherheit:** Klassisches DICOM überträgt unverschlüsselt; PS3.15 definiert u. a. TLS und Profile zur De-Identifikation – sie müssen aktiv genutzt werden. Metadaten und eingebrannter Text können Personenbezug enthalten.

```reflect
question: "Zur Diskussion: DICOM-Bestände sind Trainingsmaterial für KI. Reicht es, Name und Patienten-ID zu entfernen, um wirksam zu anonymisieren – etwa wenn sich aus einem Kopf-CT ein Gesicht rekonstruieren lässt?"
answers:
  - "**Nein.** Personenbezug steckt auch in weiteren Header-Feldern (Daten, Einrichtung, Gerät), in privaten Tags, in eingebranntem Text im Bild – und im Bildinhalt selbst."
  - "Aus Kopf-CT oder -MRT lassen sich Gesichter rekonstruieren; dagegen helfen nur zusätzliche Verfahren wie das Entfernen der Gesichtsweichteile (*defacing*)."
  - "Wirksame De-Identifikation ist ein Prozess mit Profilen (PS3.15), Prüfung und Restrisikobewertung – siehe das Thema [[topic:privacy-ethics]]."
```

## 4 · IHE-Profile: Standards zu Abläufen kombinieren

Wir haben drei Standards gesehen – und bei allen dasselbe Problem: **viele offene Optionen**. **IHE** (*Integrating the Healthcare Enterprise*) ist eine Initiative von Anwendern und Herstellern, 1998 von RSNA und HIMSS gegründet, weil man feststellte: Die Standards sind da, aber *Plug & Play* funktioniert trotzdem nicht. IHE definiert in der Regel **keine neuen Formate**, sondern **Integrationsprofile**, die bestehende Standards für konkrete Anwendungsfälle festlegen.

```timeline
title: "Der IHE-Prozess"
events:
  - when: "1"
    what: "Anwendungsfall (Use Case)"
  - when: "2"
    what: "Integrationsprofil: Akteure (abstrakte Rollen) und Transaktionen zwischen ihnen"
  - when: "3"
    what: "Technical Framework: Spezifikation bis auf einzelne HL7- und DICOM-Felder"
  - when: "4"
    what: "Connectathon: Hersteller testen direkt gegeneinander"
  - when: "5"
    what: "Integration Statement im Produkt – die Klinik fordert in der Ausschreibung nicht „HL7“, sondern „Akteur X im Profil Y“"
```

**Scheduled Workflow (SWF)** ist genau der DICOM-Ablauf von eben als Profil: KIS (ADT, Order Placer) schickt per HL7 Patientendaten und Auftrag ans RIS (Order Filler; RAD-1, -2, -4), danach übernimmt DICOM mit Worklist (RAD-5), MPPS (RAD-6/-7), Speichern (RAD-8) und Storage Commitment (RAD-10).

**Cross-Enterprise Document Sharing (XDS.b)** – jetzt verlässt Frau Müllers Entlassbrief das Haus:

```include xds-de.svg
```

```match
question: "Welche XDS.b-Transaktion ist gemeint?"
options: ["ITI-41", "ITI-42", "ITI-18", "ITI-43"]
items:
  - item: "Das Klinikum stellt den CDA-Entlassbrief in das Repository (Provide & Register)."
    answer: "ITI-41"
  - item: "Das Repository registriert die Metadaten aus dem CDA-Header in der Registry."
    answer: "ITI-42"
  - item: "Die Hausarztpraxis sucht in der Registry nach Dokumenten zu Frau Müller (Stored Query)."
    answer: "ITI-18"
  - item: "Die Hausarztpraxis holt den Brief aus dem Repository (Retrieve)."
    answer: "ITI-43"
explain: "Für die Vorbilder der radiologischen Praxis gibt es **XDS-I.b** nach demselben Prinzip. In Deutschland orientiert sich u. a. die Dokumentenverwaltung der ePA an IHE-XDS-Transaktionen (siehe [[topic:data-sharing]])."
```

Weitere Bausteine: **PIX/PDQ** lösen das Problem unterschiedlicher Patientennummern über Einrichtungen hinweg – die 4711 gilt nur im Klinikum –, **ATNA** sorgt für Audit-Protokolle und gesicherte Verbindungen, **CT** (*Consistent Time*) für synchrone Uhren. **Kritisch:** Profile sind umfangreich, auch sie lassen Optionen, und ein bestandener Connectathon heißt noch nicht stabiler Betrieb.

```quiz
question: "Brauchen wir IHE noch, wenn es FHIR gibt?"
options:
  - "Nein – FHIR ersetzt IHE vollständig."
  - "Ja – die Idee „Profile für Anwendungsfälle“ ist technologieunabhängig; IHE spezifiziert inzwischen auch FHIR-basierte Profile wie MHD."
  - "Nur in der Radiologie."
answer: "Ja – die Idee „Profile für Anwendungsfälle“ ist technologieunabhängig; IHE spezifiziert inzwischen auch FHIR-basierte Profile wie MHD."
```

## 5 · Kommunikationsmuster und Kommunikationsserver

Quer über alle Standards: **Wer stößt den Austausch an – und wer übersetzt?**

```include patterns-de.svg
```

```match
question: "Welches Muster ist es?"
options: ["Push", "Pull", "Publish/Subscribe"]
items:
  - item: "Frau Müller wird entlassen – das KIS schickt sofort die A03."
    answer: "Push"
  - item: "Der Entlassbrief wird per KIM an die Hausärztin versandt."
    answer: "Push"
  - item: "Die Modalität fragt die Worklist ab."
    answer: "Pull"
  - item: "Die Hausärztin holt den Brief per XDS, wenn sie ihn braucht."
    answer: "Pull"
  - item: "Das PVS schaut regelmäßig im Austauschverzeichnis nach neuen xDT-Dateien."
    answer: "Pull"
  - item: "Der Kommunikationsserver verteilt jede ADT-Nachricht an alle Subsysteme, die sie abonniert haben."
    answer: "Publish/Subscribe"
  - item: "FHIR Subscriptions oder IHE DSUB benachrichtigen Abonnenten über neue Dokumente."
    answer: "Publish/Subscribe"
explain: "**Push:** aktuell und effizient, aber der Sender muss den Empfänger kennen, und fällt der Empfänger aus, braucht es Warteschlangen. **Pull:** Der Empfänger bestimmt den Zeitpunkt; Polling erzeugt Last und Verzögerung. **Publish/Subscribe:** Entkopplung, leicht erweiterbar – aber der Vermittler wird zur kritischen Komponente. Sie kennen diese Muster aus Webhooks, REST-APIs und Message-Brokern wie MQTT oder Kafka."
```

### Der Kommunikationsserver übersetzt

Aus [[information-systems]] kennen Sie Routing, Transformation, Queueing und Monitoring. Im Fokus steht hier die **Transformation**: Das LIS spricht noch HL7 2.3 und schickt den CRP-Wert mit dem Hauscode „CRP“; das KIS erwartet 2.5 und LOINC.

```text
Eingang vom LIS (HL7 v2.3, Hauscode):
MSH|^~\&|LIS|...||ORU^R01|...|P|2.3
OBX|1|NM|CRP^CRP^L||182|mg/L|<5|H|||F

Ausgang zum KIS (HL7 v2.5, LOINC):
MSH|^~\&|LIS|...||ORU^R01^ORU_R01|...|P|2.5
OBX|1|NM|1988-5^C-reaktives Protein^LN||182|mg/L|<5|H|||F
```

Übersetzt werden typischerweise **Versionen** (MSH-9 und -12, neue Pflichtfelder), **Codes** (Hauscode → LOINC), **Identifikatoren** (lokale IDs, Stationskürzel) und **Transportwege** (MLLP, Dateiverzeichnis für xDT, Webservice). Produktbeispiele ohne Wertung: Infor Cloverleaf, Rhapsody, NextGen Connect (ehemals Mirth Connect), soffico Orchestra. Das ist eine Form von [[topic:etl]] im laufenden Betrieb.

```reflect
question: "Der Server gleicht fehlende Standardtreue aus – und versteckt sie damit. Wird „CRP“ auf einen falschen LOINC-Code gemappt, ist der Wert formal korrekt und fachlich falsch. Wer ist verantwortlich, wenn ein Mapping falsch ist – die IT, das Labor oder der Hersteller?"
answers:
  - "**Jede Mapping-Tabelle ist Fachlogik**: Sie gehört fachlich verantwortet (Labor für Laborcodes), technisch umgesetzt (IT / Schnittstellenteam) und gegen den Standard geprüft."
  - "Nötig sind eine dokumentierte Freigabe jeder Mapping-Änderung, Tests mit realistischen Nachrichten und Versionsverwaltung."
  - "Langfristig ist die bessere Lösung, den Standard an der Quelle zu verwenden – dann muss der Server weniger übersetzen."
```

## 6 · xDT: Datenaustausch in der Arztpraxis

Im deutschen ambulanten Sektor dominieren die **xDT-Formate**. Sie entstanden Ende der 1980er / Anfang der 1990er Jahre im Auftrag der Kassenärztlichen Bundesvereinigung (KBV), u. a. durch das Zentralinstitut für die kassenärztliche Versorgung (Zi) – ein deutscher Sonderweg, eng an Abrechnung und Praxis-EDV gekoppelt.

```match
question: "Wofür wird das xDT-Format eingesetzt?"
options: ["KVDT", "BDT", "GDT", "LDT"]
items:
  - item: "Abrechnung mit der Kassenärztlichen Vereinigung (früher „ADT“ – nicht zu verwechseln mit HL7-ADT)"
    answer: "KVDT"
  - item: "Behandlungsdaten, z. B. beim Wechsel der Praxissoftware oder zur Archivierung"
    answer: "BDT"
  - item: "Anbindung von Medizingeräten wie dem EKG in Frau Müllers Hausarztpraxis"
    answer: "GDT"
  - item: "Laboraufträge und -befunde, z. B. der CRP-Wert von der Laborgemeinschaft"
    answer: "LDT"
explain: "KVDT und LDT pflegt die KBV, BDT und GDT der Qualitätsring Medizinische Software (QMS); aktuell ist GDT 3.5 (2022)."
```

Der Aufbau ist bewusst einfach: **Jede Zeile ist ein Feld** – drei Stellen Zeilenlänge, vier Stellen Feldkennung, dann der Inhalt, am Ende CR LF. Hier fordert das Praxisverwaltungssystem (PVS) beim EKG-Gerät eine Untersuchung für Frau Müller an (vereinfacht, angelehnt an GDT 2.1):

```text
01380006302      8000 Satzart 6302 = neue Untersuchung anfordern
014810000130     8100 Satzlänge in Byte
0158315EKG_01    8315 Empfänger-ID
0158316PVS_01    8316 Sender-ID
014921802.10     9218 GDT-Version
01330002093      3000 Patientennummer
0153101Müller    3101 Name
0143102Erika     3102 Vorname
017310312031958  3103 Geburtsdatum
```

```quiz
question: "Rechnen Sie nach: Warum beginnt die erste Zeile mit „013“?"
options:
  - "3 Stellen Länge + 4 Stellen Feldkennung + 4 Zeichen Inhalt + 2 Zeichen Zeilenende = 13"
  - "Weil die Satzart 13 Felder hat"
  - "Weil die GDT-Version 13 ist"
answer: "3 Stellen Länge + 4 Stellen Feldkennung + 4 Zeichen Inhalt + 2 Zeichen Zeilenende = 13"
explain: "Die Patientennummer der Praxis (2093) ist übrigens eine andere als die 4711 des Klinikums – genau das Identitätsproblem, das IHE PIX/PDQ adressiert."
```

**Ablauf bei GDT:** Das PVS schreibt die Anforderung als Datei in ein Austauschverzeichnis → das Gerät liest sie und misst → das Gerät schreibt das Ergebnis (Satzart 6310) → das PVS übernimmt es. Dateibasiert, **ohne Quittungsprotokoll**. Für eine Implementierung gilt die aktuelle QMS-Satzbeschreibung.

```match
question: "xDT oder HL7 v2?"
options: ["xDT", "HL7 v2"]
items:
  - item: "ambulant, Deutschland"
    answer: "xDT"
  - item: "vor allem stationär, international"
    answer: "HL7 v2"
  - item: "Zeile = Länge + Feldkennung + Inhalt"
    answer: "xDT"
  - item: "Segmente, Felder, Trennzeichen"
    answer: "HL7 v2"
  - item: "meist Datei im Austauschverzeichnis, keine Quittung im Protokoll"
    answer: "xDT"
  - item: "meist TCP mit MLLP, ACK-Mechanismus"
    answer: "HL7 v2"
explain: "**Kritik an xDT:** nationaler Sonderweg mit wenigen internationalen Werkzeugen; Dateiaustausch bringt Sperr-, Fehler- und Sicherheitsfragen (halb geschriebene Dateien, Zugriffsrechte). **Aber:** robust, einfach, in nahezu jedem PVS vorhanden. Die sektorübergreifende Kommunikation verlagert sich in die Telematikinfrastruktur: KIM für den Versand (z. B. eArztbrief), die ePA und FHIR-basierte Medizinische Informationsobjekte (MIO) der KBV."
```

```reflect
question: "Zur Diskussion: Sollte Deutschland ambulant konsequent auf internationale Standards wechseln? Wer trägt die Umstellungskosten – Praxen, Hersteller, Kassen?"
answers:
  - "**Dafür:** internationale Werkzeuge und Fachkräfte, einfachere sektorübergreifende Kommunikation, weniger Übersetzung an jeder Grenze."
  - "**Dagegen / Hürden:** zehntausende Praxen mit funktionierenden Installationen, enge Kopplung an die Abrechnung, Umstellungsaufwand ohne unmittelbaren Nutzen für die einzelne Praxis."
  - "Realistisch ist ein **schrittweiser Übergang** über die Telematikinfrastruktur (KIM, ePA, MIO auf FHIR-Basis), bei dem xDT für Geräte und Abrechnung noch lange parallel läuft."
```

## Zusammenfassung: Frau Müllers Weg – aufgelöst

```match
question: "Welcher Standard (und welches Muster) passt?"
options:
  - "HL7 v2 ADT^A03 über MLLP mit ACK – Push über den Kommunikationsserver"
  - "HL7 CDA R2 – Push per KIM oder Pull per IHE XDS"
  - "DICOM (Association, C-STORE, Storage Commitment) im Rahmen von IHE SWF"
  - "xDT: GDT, LDT, KVDT – dateibasiert, Polling"
  - "IHE XDS-I.b – Pull"
items:
  - item: "Die Entlassung muss alle Subsysteme im Klinikum erreichen."
    answer: "HL7 v2 ADT^A03 über MLLP mit ACK – Push über den Kommunikationsserver"
  - item: "Der Entlassbrief soll zur Hausärztin."
    answer: "HL7 CDA R2 – Push per KIM oder Pull per IHE XDS"
  - item: "Röntgen und CT werden erzeugt und archiviert."
    answer: "DICOM (Association, C-STORE, Storage Commitment) im Rahmen von IHE SWF"
  - item: "In der Hausarztpraxis: EKG, CRP über die Laborgemeinschaft, Abrechnung."
    answer: "xDT: GDT, LDT, KVDT – dateibasiert, Polling"
  - item: "Die radiologische Praxis ruft die Vorbilder ab."
    answer: "IHE XDS-I.b – Pull"
```

> **Merkzeile:** Daten → HL7 v2 · Dokumente → CDA · Bilder → DICOM · Abläufe → IHE · Übersetzung → Kommunikationsserver · ambulant → xDT

## Take-home Messages

1. **Zweck vor Format:** Daten → HL7 v2 · Dokumente → CDA · Bilder → DICOM. Wer den Zweck kennt, wählt den passenden Standard.
2. **Zuverlässig heißt mehr als Syntax:** Quittungen, eindeutige IDs, gemeinsame Codes und abgestimmte Abläufe (IHE) machen den Austausch sicher.
3. **Grenzen überwinden:** Im Haus vermittelt der Kommunikationsserver; über Einrichtungs- und Sektorgrenzen braucht es Profile, die Telematikinfrastruktur und – ambulant – xDT.

## Verständnisfrage

```reflect
question: "Frau Müllers Hausärztin soll den Entlassbrief erhalten, die Laborgemeinschaft einen CRP-Wert zurückmelden und die radiologische Praxis die Vorbilder abrufen. Welchen Standard setzen Sie jeweils ein – und warum?"
rows: 4
answers:
  - "**Entlassbrief:** als CDA-Dokument (ein verantwortetes, signierbares, menschenlesbares Dokument) – versendet per KIM oder bereitgestellt über IHE XDS."
  - "**CRP-Wert:** per LDT – der etablierte Standard zwischen Laborgemeinschaft und Praxisverwaltungssystem im ambulanten Sektor."
  - "**Vorbilder:** als DICOM-Objekte (mit allen Metadaten) über IHE XDS-I – die Praxis fragt bei Bedarf ab (Pull)."
```

## Ausblick: Kommunikationsstandards II – FHIR

In der nächsten Vorlesung folgt [[topic:fhir]]: Ressourcen statt Nachrichten und Dokumente, REST statt MLLP – und die Frage, wie viel von HL7 v2, CDA und IHE darin weiterlebt.

## Selbsttest

```quiz
question: "Welche Aussage über HL7 v2 trifft zu?"
options:
  - "HL7 v2 regelt auch die Verschlüsselung der Übertragung."
  - "Neue Felder werden hinten angehängt, alte nicht entfernt – deshalb ist v2 rückwärtskompatibel."
  - "Jedes Feld einer v2-Nachricht ist verpflichtend."
answer: "Neue Felder werden hinten angehängt, alte nicht entfernt – deshalb ist v2 rückwärtskompatibel."
```

```quiz
question: "Was ist in einem CDA-Dokument rechtlich verbindlich?"
options: ["der Text der Abschnitte", "die codierten entries", "der Header allein"]
answer: "der Text der Abschnitte"
```

```quiz
question: "Was unterscheidet den Verbindungsaufbau bei DICOM von dem bei HL7 v2?"
options:
  - "DICOM handelt in einer Association zuerst SOP-Klassen und Transfer Syntaxes aus."
  - "DICOM verwendet immer eine Datei im Austauschverzeichnis."
  - "Es gibt keinen Unterschied."
answer: "DICOM handelt in einer Association zuerst SOP-Klassen und Transfer Syntaxes aus."
```
