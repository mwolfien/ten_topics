---
title: "Übung: Wenn Systeme sich nicht einig sind"
summary: "Selbstständige Transferübung zur Vorlesung über KIS, LIS und RIS/PACS: Ein unbekannter Notfallpatient wird später identifiziert – und nicht alle Systeme folgen. Sie analysieren Systemlandschaft, ADT, Orders & Results und ein Schnittstellenproblem."
duration_minutes: 90
level: "Übung · Transfer"
audiences: [med, cs, clin, tech]
order: 4
builds_on: [information-systems]
course: his
lecture: 2
kind: exercise
author: "Eveline Prochaska, Markus Wolfien"
objectives:
  - "Aus einem klinischen Fall eine Systemlandschaft rekonstruieren"
  - "All-in-One/Best-of-Breed und Stern/Spaghetti unabhängig voneinander bewerten"
  - "Relevante ADT-Ereignisse und Versorgungskontexte identifizieren"
  - "Order/Result-Flüsse zwischen KIS und diagnostischen Subsystemen nachvollziehen"
  - "Auswirkungen eines Schnittstellenfehlers auf mehrere Systeme analysieren"
  - "Technische und organisatorische Gegenmaßnahmen ableiten"
readings: [winter2023, sittig2010]
related_topics: [ehr-cis, data-quality, fhir]
source: "Übung zu Vorlesung 2 „KIS, LIS und RIS/PACS – Zusammenspiel klinischer Informationssysteme“, Informationssysteme im Gesundheitswesen (WiSe 2026/27), Eveline Prochaska und Markus Wolfien, IMB & ZMI"
---

> **Worum es geht:** In der Vorlesung und im Modul [[information-systems]] haben Sie Frau Müller durch die Systemlandschaft begleitet. Hier wenden Sie dieselben Konzepte auf einen **neuen Fall** an – mit einem anderen Problem: Nicht eine Verlegung geht verloren, sondern **die Identität des Patienten ändert sich, und nicht alle Systeme folgen.**

## Bearbeitungshinweise

- Bearbeiten Sie die Übung allein oder zu zweit. Planen Sie etwa **90 Minuten** ein; Sie können jederzeit unterbrechen.
- Bei den **offenen Aufgaben** (✏️) schreiben Sie zuerst Ihre eigene Antwort. Erst dann lassen sich die Lösungshinweise aufklappen. Vergleichen Sie danach: Was hatten Sie, was fehlte, wo sehen Sie es anders?
- Die **Auswahlaufgaben** (❓) geben sofort Rückmeldung.
- Ihre Antworten bleiben **nur in Ihrem Browser** gespeichert. Am Ende können Sie sie als Datei herunterladen, z. B. für die Besprechung in der Übungsgruppe.
- Für Aufgabe 2.2 brauchen Sie Papier und Stift (oder ein Zeichenprogramm).

| Teil | Inhalt | Zeit |
|---|---|---:|
| 1 | Systeme erkennen | 10 min |
| 2 | Architektur analysieren | 15 min |
| 3 | ADT und Identität | 15 min |
| 4 | Orders & Results | 15 min |
| 5 | Schnittstellenfehler analysieren | 20 min |
| 6 | Architektur verbessern | 15 min |
| | **Gesamt** | **90 min** |

## Der Fall

```case
**Dienstag, 14:05 Uhr.** Ein etwa 35-jähriger Mann wird nach einem Fahrradunfall bewusstseinsgetrübt in die Zentrale Notaufnahme (ZNA) gebracht. Ausweisdokumente hat er nicht bei sich, Angehörige sind nicht erreichbar.

Bei der Aufnahme wird deshalb eine **vorläufige Identität** angelegt:

- **Patient:** „Unbekannt, männlich“, geschätztes Geburtsdatum 01.01.1991
- **temporäre Patienten-ID:** 99127
- **Fall:** F2026-1048

In den ersten 90 Minuten folgen: Aufnahme in der ZNA, Blutbild, Gerinnung und Blutgruppenbestimmung, ein CT von Kopf und Thorax, die operative Versorgung und anschließend die Verlegung auf die Intensivstation.

Beteiligt sind unter anderem: **KIS – Kommunikationsserver – LIS – Blutbank – RIS – PACS – OP-System – PDMS.**

**Um 20:00 Uhr** wird der Patient als **Max Berger** identifiziert. Er war bereits früher im Haus in Behandlung und hat deshalb schon eine Patienten-ID: **34821**. Die beiden Identitäten müssen zusammengeführt werden.
```

## Teil 1 · Welche Systeme sind beteiligt? (10 min)

```match
question: "Aufgabe 1.1: Welche Funktion hat das System in diesem Fall vor allem?"
options:
  - "Aufnahme, Fallanlage, Aufträge, Dokumentation"
  - "Blutbild und Gerinnung messen und befunden"
  - "Blutgruppe bestimmen, Konserven bereitstellen"
  - "CT planen, Worklist bereitstellen, Befundtext"
  - "CT-Bilder speichern, archivieren, anzeigen"
  - "Operation planen und dokumentieren"
  - "Vitaldaten und Therapie auf der Intensivstation"
  - "Nachrichten zwischen den Systemen verteilen und übersetzen"
items:
  - item: "KIS"
    answer: "Aufnahme, Fallanlage, Aufträge, Dokumentation"
  - item: "LIS"
    answer: "Blutbild und Gerinnung messen und befunden"
  - item: "Blutbank"
    answer: "Blutgruppe bestimmen, Konserven bereitstellen"
  - item: "RIS"
    answer: "CT planen, Worklist bereitstellen, Befundtext"
  - item: "PACS"
    answer: "CT-Bilder speichern, archivieren, anzeigen"
  - item: "OP-System"
    answer: "Operation planen und dokumentieren"
  - item: "PDMS"
    answer: "Vitaldaten und Therapie auf der Intensivstation"
  - item: "Kommunikationsserver"
    answer: "Nachrichten zwischen den Systemen verteilen und übersetzen"
explain: "Acht Systeme in 90 Minuten – und alle arbeiten mit demselben Patienten."
```

```reflect
question: "**Aufgabe 1.2:** Welche Systeme benötigen Informationen (a) zur Patientenidentität, (b) zum Fall und (c) zum aktuellen Aufenthaltsort? Begründen Sie kurz."
intro: "Mögliche Antwort:"
answers:
  - "**Identität:** praktisch alle – LIS, Blutbank, RIS, PACS, OP-System und PDMS müssen Proben, Bilder, Konserven und Messwerte eindeutig dem richtigen Menschen zuordnen. Für die Blutbank ist das besonders kritisch (Verwechslung → Transfusionszwischenfall)."
  - "**Fall:** KIS und Abrechnung (Leistungen, DRG), aber auch LIS, RIS, OP-System und PDMS, weil Leistungen und Dokumentation dem Fall F2026-1048 zugeordnet werden."
  - "**Aufenthaltsort:** LIS und Blutbank (Befund- und Konservenzustellung, Meldung kritischer Werte), RIS (Patient zum CT holen, Befundrouting), OP-System (Übergabe), PDMS (Bettenliste der Intensivstation)."
```

```reflect
question: "**Transferfrage:** Warum reicht es nicht, wenn nur das KIS die korrekten Patientendaten kennt?"
answers:
  - "Die Subsysteme fragen das KIS nicht bei jeder Aktion. Sie halten eine **eigene Kopie** des ADT-Kontexts und arbeiten damit – auch wenn das KIS kurz nicht erreichbar ist."
  - "Proben, Bilder und Konserven tragen die Identität **in sich** (Barcode, DICOM-Header, Etikett). Ändert sich die Identität nur im KIS, sind diese Daten weiter falsch beschriftet."
  - "Deshalb muss jede Änderung als Ereignis an alle Systeme gehen – und dort auch korrekt verarbeitet werden."
```

## Teil 2 · Architektur der Systemlandschaft (15 min)

Sie erhalten vereinfachte Informationen über die Landschaft des Hauses:

- Aufnahme, Dokumentation, Order Entry und Abrechnung stammen aus einer **KIS-Suite von Hersteller A**.
- LIS, Blutbank, RIS, PACS, PDMS und OP-System stammen von **unterschiedlichen Herstellern**.
- KIS, LIS, Blutbank, RIS, PDMS und OP-System kommunizieren überwiegend über einen **Kommunikationsserver**.
- RIS und PACS besitzen eine **direkte Verbindung**.
- Das PDMS kommuniziert **direkt** mit den Monitoring-Geräten.

```quiz
question: "Aufgabe 2.1a: Wie ordnen Sie die Landschaft auf der Anwendungsebene ein?"
options:
  - "All-in-One"
  - "Best-of-Breed"
  - "Hybrid: Kern-Suite plus Spezialsysteme verschiedener Hersteller"
answer: "Hybrid: Kern-Suite plus Spezialsysteme verschiedener Hersteller"
explain: "Die KIS-Suite ist in sich All-in-One, die Landschaft insgesamt aber Best-of-Breed – die typische Mischform."
```

```quiz
question: "Aufgabe 2.1b: Und auf der Kommunikationsebene?"
options:
  - "Reiner Stern"
  - "Spaghetti"
  - "Überwiegend Stern, mit einzelnen Direktverbindungen"
answer: "Überwiegend Stern, mit einzelnen Direktverbindungen"
explain: "Beide Fragen sind unabhängig: Eine Best-of-Breed-Landschaft kann überwiegend als Stern integriert sein."
```

```reflect
question: "**Aufgabe 2.2:** Zeichnen Sie eine vereinfachte Systemlandschaft mit den wichtigsten Verbindungen. Notieren Sie hier, was Ihnen beim Zeichnen auffällt."
rows: 3
answers:
  - "Die Musterlösung finden Sie unter diesem Kasten. Achten Sie besonders auf das **PACS**: Welche Verbindungen hat es – und welche nicht?"
```

```include landscape-solution-de.svg
Musterlösung zu Aufgabe 2.2 anzeigen
```

```reflect
question: "**Aufgabe 2.3:** Welche Vor- und Nachteile hat diese Architektur?"
answers:
  - "**Vorteile:** fachlich passende Spezialsysteme (Labor, Blutbank, Radiologie, Intensivmedizin); einheitliche Oberfläche für die Kernprozesse; der Kommunikationsserver begrenzt die Zahl der Schnittstellen und bündelt Routing, Mapping, Pufferung und Monitoring."
  - "**Nachteile:** viele Hersteller und Verträge; Stammdaten in vielen Kopien; der Kommunikationsserver ist ein Single Point of Failure."
  - "**Direktverbindungen** (RIS ↔ PACS, PDMS ↔ Geräte) sind fachlich gut begründet (Bilddaten, Echtzeit), laufen aber am Monitoring des Servers vorbei – und das PACS bekommt Änderungen nur auf Umwegen."
```

## Teil 3 · ADT und Patientenidentität (15 min)

```timeline
title: "Der Weg des Patienten"
events:
  - when: "14:05"
    what: "Aufnahme in der ZNA als „Unbekannt, männlich“, ID 99127, Fall F2026-1048"
  - when: "15:20"
    what: "Verlegung in den OP"
  - when: "17:05"
    what: "Verlegung auf die Intensivstation"
  - when: "20:00"
    what: "Identität geklärt: ID 99127 ist Max Berger, der bereits die ID 34821 hat"
```

```match
question: "Aufgabe 3.1: Was ändert sich jeweils?"
options:
  - "neuer Patient, neuer Fall und erste Bewegung"
  - "nur die Bewegung (Aufenthaltsort)"
  - "die Patientenidentität – Fall und Bewegungen bleiben"
items:
  - item: "14:05 Aufnahme in der ZNA"
    answer: "neuer Patient, neuer Fall und erste Bewegung"
  - item: "15:20 Verlegung in den OP"
    answer: "nur die Bewegung (Aufenthaltsort)"
  - item: "17:05 Verlegung auf die Intensivstation"
    answer: "nur die Bewegung (Aufenthaltsort)"
  - item: "20:00 Identität geklärt"
    answer: "die Patientenidentität – Fall und Bewegungen bleiben"
explain: "Patient ≠ Fall ≠ Bewegung: Um 20:00 bleibt der Fall F2026-1048 mit allen Bewegungen bestehen, er gehört jetzt nur zu einer anderen – der dauerhaften – Patientenidentität."
```

```reflect
question: "**Aufgabe 3.2:** Welche Systeme müssen über die Verlegung auf die Intensivstation informiert werden – und wozu?"
answers:
  - "**PDMS:** Der Patient muss auf der Bettenliste erscheinen, Monitordaten müssen ihm zugeordnet werden."
  - "**LIS und Blutbank:** Befunde, Meldungen kritischer Werte und Blutkonserven müssen an die Intensivstation statt an die ZNA oder den OP gehen."
  - "**RIS (und darüber PACS):** für Befundrouting und weitere Untersuchungen, z. B. ein Kontroll-CT."
  - "**OP-System:** Der OP-Aufenthalt ist abgeschlossen."
  - "**Abrechnung:** Intensivtage und die Fachabteilung sind abrechnungsrelevant."
  - "Technisch ist das eine `ADT^A02`, die der Kommunikationsserver an alle Abonnenten verteilt."
```

```quiz
question: "Aufgabe 3.3a: Welches HL7-v2-Ereignis passt zur Zusammenführung um 20:00?"
options: ["A02 – Verlegung", "A08 – Patientendaten aktualisieren", "A11 – Aufnahme stornieren", "A40 – Patienten zusammenführen"]
answer: "A40 – Patienten zusammenführen"
shuffle: false  # options in a natural order
explain: "Mit `ADT^A40` wird die temporäre ID 99127 in die bestehende ID 34821 überführt. Die dauerhafte ID bleibt, die temporäre wird als zusammengeführt markiert. Ein A08 würde nur die Daten unter 99127 ändern – die beiden Akten blieben getrennt."
```

```reflect
question: "**Aufgabe 3.3b:** Was bedeutet die Zusammenführung der beiden Identitäten für die angeschlossenen Systeme?"
answers:
  - "**Nicht nur das KIS muss korrigiert werden.** Jede Kopie des Patientenkontexts in LIS, Blutbank, RIS, PACS, OP-System und PDMS muss die Zusammenführung nachvollziehen."
  - "Alle Daten unter 99127 – Laborwerte, Blutgruppe, CT-Bilder, OP-Bericht, Vitaldaten – gehören jetzt zu 34821. Umgekehrt werden die **Vorbefunde** unter 34821 erst jetzt sichtbar, z. B. frühere Laborwerte, Vorbilder, Vorerkrankungen, Allergien oder eine frühere Blutgruppenbestimmung."
  - "Zusammenführungen sind schwieriger als einfache Änderungen: Jedes System muss sie korrekt umsetzen, und eine falsche Zusammenführung ist kaum rückgängig zu machen."
```

## Teil 4 · Orders & Results rekonstruieren (15 min)

Zwei Informationsflüsse laufen parallel:

- **Labor:** KIS → Auftrag → LIS → Probe → Analyse → Validation → Ergebnis → KIS
- **Radiologie:** KIS → Auftrag → RIS → Modalität → PACS → Befundung → Befund und Bildlink → KIS

```match
question: "Aufgabe 4.1: Zu welcher Phase des Order/Result-Musters gehört der Schritt?"
options: ["Order", "Durchführung", "Validation / Befundung", "Result"]
items:
  - item: "Anforderung von Blutbild und Gerinnung im KIS"
    answer: "Order"
  - item: "Messung der Gerinnung am Analysegerät"
    answer: "Durchführung"
  - item: "Medizinische Validation der Gerinnungswerte"
    answer: "Validation / Befundung"
  - item: "Laborbefund im KIS"
    answer: "Result"
  - item: "CT-Anforderung im KIS"
    answer: "Order"
  - item: "CT-Untersuchung, Bilder gehen ins PACS"
    answer: "Durchführung"
  - item: "Radiologin befundet die Bilder"
    answer: "Validation / Befundung"
  - item: "Befund und Bildlink im KIS"
    answer: "Result"
explain: "Labor und Radiologie folgen demselben Muster – nur die Systeme und Datentypen unterscheiden sich."
```

```reflect
question: "**Aufgabe 4.2:** Wo muss in beiden Flüssen die korrekte Patientenidentität mitgeführt werden?"
answers:
  - "**Labor:** im Auftrag (HL7-Nachricht), auf dem **Barcode-Etikett** der Probe, im LIS-Auftrag und im Ergebnis (`ORU`) zurück ins KIS – und in der Blutbank auf Blutgruppenbefund und Konserve."
  - "**Radiologie:** im Auftrag an das RIS, in der **Worklist** an das CT, im **DICOM-Header** jedes Bildes, im PACS und im Befund zurück ins KIS."
  - "In diesem Fall ist das überall die **temporäre ID 99127**. Sie steckt nicht nur in Datenbanken, sondern auch in Etiketten und Bilddateien. Genau das macht die spätere Zusammenführung so aufwendig."
```

```match
question: "Aufgabe 4.3: Welche Verbindung erwarten Sie eher über den Kommunikationsserver, welche eher als direkte Verbindung?"
options: ["über den Kommunikationsserver", "direkt"]
items:
  - item: "Laborauftrag KIS → LIS"
    answer: "über den Kommunikationsserver"
  - item: "Laborbefund LIS → KIS"
    answer: "über den Kommunikationsserver"
  - item: "Blutgruppenbefund Blutbank → KIS"
    answer: "über den Kommunikationsserver"
  - item: "CT-Auftrag KIS → RIS"
    answer: "über den Kommunikationsserver"
  - item: "Worklist RIS → CT"
    answer: "direkt"
  - item: "CT-Bilder → PACS"
    answer: "direkt"
  - item: "Vitaldaten Monitor → PDMS"
    answer: "direkt"
explain: "Die HL7-Nachrichten zwischen KIS und Subsystemen laufen über den Server. DICOM zwischen RIS, Modalität und PACS sowie die Gerätedaten am PDMS laufen meist direkt – wegen Datenvolumen, Echtzeit und enger Herstellerkopplung."
```

## Teil 5 · Das Fehlerszenario (20 min)

```case
**20:00 Uhr.** Im KIS werden die temporäre ID **99127** und die bestehende ID **34821** korrekt zusammengeführt. Die Änderungsnachricht erreicht KIS, LIS, Blutbank, RIS und PDMS.

**Das PACS erhält die Änderung jedoch nicht.** Dort liegen die CT-Bilder von Kopf und Thorax weiterhin unter „Unbekannt, männlich – ID 99127“.
```

```reflect
question: "**Aufgabe 5.1:** Welche Probleme könnten daraus entstehen?"
answers:
  - "Unter Max Berger (34821) fehlen im PACS die aktuellen CT-Bilder. Der Bildlink im KIS führt ins Leere oder zu einer „unbekannten“ Akte."
  - "Neue Bilder, z. B. ein Kontroll-CT am nächsten Tag, landen unter 34821. Der Vergleich mit dem Erst-CT ist nicht ohne Weiteres möglich."
  - "Im PACS existieren jetzt zwei „Patienten“ für denselben Menschen – eine Dublette, die niemand bemerkt hat."
  - "Weitergegebene Kopien (Teleradiologie, Konsil, Befund-CD) tragen die falsche Identität."
```

```reflect
question: "**Aufgabe 5.2:** Welche Systeme erscheinen aus ihrer eigenen Sicht trotzdem „korrekt“?"
answers:
  - "**Alle.** Das KIS hat zusammengeführt und die Nachricht verschickt. LIS, Blutbank, RIS und PDMS haben sie verarbeitet. Das PACS hat einwandfrei gespeicherte Bilder unter einer gültigen ID."
  - "Das PACS hat keinen „Fehler“ – es weiß nur nichts von der Änderung. **Technisch korrekt heißt nicht fachlich korrekt.**"
  - "Ein möglicher Grund liegt in der Architektur aus Teil 2: Das PACS ist **nicht direkt am Kommunikationsserver** angebunden, sondern bekommt Patientenänderungen nur über das RIS. Wenn das RIS die Zusammenführung nicht weiterreicht, kommt sie im PACS nie an – und das Monitoring des Servers sieht davon nichts."
```

```reflect
question: "**Aufgabe 5.3:** Wo würde der Fehler wahrscheinlich zuerst auffallen?"
answers:
  - "In der klinischen Nutzung, nicht in der IT: wenn die Intensivstation oder die Neurochirurgie die Bilder aus der Akte von Max Berger öffnen will und keine findet."
  - "Oder bei der Befundung eines Kontroll-CTs, wenn die Radiologin keine Voraufnahme findet – obwohl eine existieren muss."
  - "Im schlechtesten Fall fällt es gar nicht auf: Man geht davon aus, dass es kein Vor-CT gibt."
```

```reflect
question: "**Aufgabe 5.4:** Welche Folgen könnten entstehen für (a) die aktuelle Befundung, (b) spätere Vorbildvergleiche, (c) eine erneute Behandlung des Patienten und (d) Forschung oder Datenexport?"
rows: 5
answers:
  - "**(a) Aktuelle Befundung:** Befund und Bilder hängen an verschiedenen Identitäten. Klinische Angaben aus der Vorgeschichte (34821) fehlen der Radiologin."
  - "**(b) Vorbildvergleiche:** Ein Kontroll-CT wird ohne Vergleich befundet, z. B. bei der Frage, ob eine Blutung größer geworden ist. Das führt zu Fehleinschätzungen oder unnötigen Wiederholungsuntersuchungen mit zusätzlicher Strahlung."
  - "**(c) Erneute Behandlung:** Bei einer späteren Aufnahme fehlen die Unfallbilder in der Akte. Wichtige Befunde (Frakturen, Implantate) sind nicht auffindbar."
  - "**(d) Forschung und Datenexport:** Für eine Person existieren zwei Datensätze. Kohorten werden falsch gezählt, Verläufe zerreißen, und bei der Pseudonymisierung entstehen zwei Pseudonyme. Datenqualität ist auch eine Frage der Identität."
```

```reflect
question: "**Aufgabe 5.5:** Ist das primär ein Softwarefehler, ein Schnittstellenfehler, ein Prozessfehler, ein organisatorisches Problem – oder eine Kombination? Begründen Sie."
answers:
  - "**Eine Kombination** – das ist das sozio-technische Dreieck aus [[history]]."
  - "**Schnittstelle / Architektur:** Die Zusammenführung wird nicht an das PACS geroutet, oder die Direktverbindung RIS ↔ PACS reicht sie nicht weiter."
  - "**Prozess:** Es gibt keine Checkliste, welche Systeme nach einer Zusammenführung geprüft werden müssen, und keine Rückmeldung, ob alle Systeme sie umgesetzt haben."
  - "**Organisation:** Unklar ist, wer für Zusammenführungen verantwortlich ist (Patientenaufnahme? Radiologie? IT?) und wer Fehler in Direktverbindungen überwacht."
  - "Merke: **Technisch korrekt ≠ fachlich korrekt** – und **Integration ist Patientensicherheit.**"
```

## Teil 6 · Das System verbessern (15 min)

```reflect
question: "**Aufgabe 6.1:** Nennen Sie mindestens vier Maßnahmen, die das Risiko reduzieren könnten. Denken Sie an Technik, Monitoring, Identitätsmanagement, Prozesse und Zuständigkeiten."
rows: 5
answers:
  - "**Technik:** das PACS mit einem eigenen ADT-Feed (inkl. A40) an den Kommunikationsserver anbinden; Zusammenführungen per IHE *Patient Information Reconciliation* abbilden."
  - "**Monitoring:** Empfangsquittungen (ACK) für Zusammenführungen von *allen* Systemen; nächtlicher Abgleich, ob temporäre IDs in irgendeinem System noch Daten tragen."
  - "**Identitätsmanagement:** ein Master Patient Index; klare Regeln für Notfall-Identitäten; Dublettenprüfung, sobald die Identität bekannt ist."
  - "**Prozess:** eine Checkliste „Identität geklärt“ mit allen betroffenen Systemen und einem Abschluss erst nach Prüfung in jedem System."
  - "**Organisation:** benannte Verantwortliche für Zusammenführungen (z. B. Patientenmanagement) und für die Direktverbindungen; Schulung und klare Meldewege bei Auffälligkeiten."
```

```match
question: "Ordnen Sie die Maßnahmen den Kategorien zu."
options: ["Technik", "Monitoring", "Identitätsmanagement", "Prozess", "Organisation"]
items:
  - item: "PACS erhält einen eigenen ADT-Feed über den Kommunikationsserver"
    answer: "Technik"
  - item: "Alarm, wenn ein System die Zusammenführung nicht quittiert"
    answer: "Monitoring"
  - item: "Master Patient Index mit Dublettenprüfung"
    answer: "Identitätsmanagement"
  - item: "Checkliste „Identität geklärt“ für alle betroffenen Systeme"
    answer: "Prozess"
  - item: "Benannte Verantwortliche für Zusammenführungen"
    answer: "Organisation"
```

```reflect
question: "**Aufgabe 6.2:** Wäre ein All-in-One-System automatisch sicherer? Begründen Sie."
answers:
  - "**Nicht automatisch.** Innerhalb einer Suite mit gemeinsamer Datenbasis wäre die Zusammenführung leichter konsistent zu halten."
  - "Aber: Auch eine Suite hat Spezialsysteme und Geräte, die sie nicht selbst abdeckt (Modalitäten, Analysegeräte, Monitoring), und externe Kopien (Teleradiologie, Forschung)."
  - "Einzelne Module können fachlich schwächer sein. Und Fehler in einer Suite treffen dann alle Bereiche gleichzeitig."
  - "Die Sicherheit hängt weniger vom Architekturtyp ab als davon, wie Identität, Ereignisse und Monitoring gelöst sind."
```

```reflect
question: "**Aufgabe 6.3:** Wäre es sinnvoll, jede Direktverbindung durch den Kommunikationsserver zu ersetzen?"
answers:
  - "**Nicht zwingend.** DICOM-Bilddaten (Hunderte Bilder pro CT) und Echtzeit-Vitaldaten über den HL7-Server zu leiten, wäre technisch unsinnig und würde ihn zum Engpass machen."
  - "Sinnvoll ist aber, dass **Patientenkontext und Identitätsänderungen** jedes System über einen überwachten Weg erreichen – auch Systeme, deren Nutzdaten direkt fließen."
  - "Direktverbindungen brauchen eigenes Monitoring und klare Zuständigkeiten."
  - "Merke: **Architekturentscheidungen sind Abwägungen**, nicht „Stern gut, Spaghetti böse“."
```

## Abschlussaufgabe

```reflect
question: "**Abschluss:** Was würden Sie bei der Einführung eines neuen diagnostischen Subsystems zuerst prüfen? Antworten Sie in maximal drei Sätzen."
rows: 4
intro: "Ihre Antwort sollte mehrere dieser Aspekte enthalten:"
answers:
  - "**Identität:** Wie erhält das System Patientenidentität und Identitätsänderungen (inkl. Zusammenführungen)?"
  - "**Fallkontext:** Kennt es Fall und Aufenthaltsort, und wie bleiben diese aktuell?"
  - "**Orders/Results:** Wie kommen Aufträge hinein und Ergebnisse zurück – mit Placer- und Filler-Nummer?"
  - "**Schnittstellen:** über den Kommunikationsserver oder direkt – und warum?"
  - "**Monitoring:** Wer merkt, wenn eine Nachricht nicht ankommt?"
  - "**Fehlerprozesse:** Wie werden Korrekturen, Ausfälle und Notfall-Identitäten behandelt – und wer ist zuständig?"
```

> **Zum Mitnehmen:** Krankenhaus-IT ist kein einzelnes System, sondern eine Landschaft, in der viele Systeme denselben Patienten- und Fallkontext korrekt teilen müssen – auch dann, wenn sich dieser Kontext nachträglich ändert.
