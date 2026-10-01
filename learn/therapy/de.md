---
title: "Therapie, Leitlinien und Patientenzentrierung"
summary: "Wie aus einem auffälligen Befund eine gute, patientenzentrierte Therapieentscheidung wird – am Beispiel des Lungenkarzinoms, vom Screening über das Tumorboard bis zur Therapie im Verlauf."
duration_minutes: 40
level: "Grundlagen"
audiences: [med, cs, clin, tech, pat]
order: 2
builds_on: [history]
course: "Grundlagen der Medizin für Informatiker:innen"
author: "Markus Wolfien"
objectives:
  - "Grundlegende Therapieformen benennen und an Beispielen erklären"
  - "Therapieziele unterscheiden: heilen, kontrollieren, lindern, begleiten"
  - "Erläutern, warum Therapie immer eine Nutzen-Risiko-Abwägung ist"
  - "Das Prinzip des Shared Decision Making beschreiben"
  - "Erklären, warum Adhärenz, Lebensrealität und Patientensicht wichtig sind"
  - "PROs und PROMs als Instrumente der Therapiekontrolle einordnen"
  - "Leitlinien als Entscheidungsrahmen verstehen und ihre Grenzen erklären"
readings: [elwyn2012, basch2016, dekoning2020, gladstone2025, hassan2024]
related_topics: [cdss, ehr-cis, fhir, data-quality, visualizations]
source: "Vorlesung 7 „Therapie, Leitlinien und Patientenzentrierung“, Grundlagen der Medizin für Informatiker:innen (SoSe 2026), Markus Wolfien, IMB & ZMI"
---

> **Leitfrage:** Wie wird aus einem auffälligen Befund eine gute, patientenzentrierte Therapieentscheidung?

Wenn wir über Therapie sprechen, denken viele zuerst an Medikamente oder Operationen. Medizinisch beginnt Therapie aber früher – mit der Frage, **welches Ziel** verfolgt wird. Therapie ist deshalb immer ein Entscheidungsprozess und nicht nur die Anwendung einer Maßnahme.

Im Modul [[history]] haben Sie gesehen, dass Digitalisierung nie nur ein technisches Projekt ist und Information im Krankenhaus in vielen Systemen verteilt liegt. In diesem Modul folgen wir einem Patienten durch die Versorgung und sehen, wo genau diese Daten für eine Therapieentscheidung zusammenkommen müssen.

```persona med
Sie lernen hier das Grundgerüst jeder Therapieentscheidung: Ziel, Optionen, Nutzen-Risiko-Abwägung und gemeinsame Entscheidung. Das gilt weit über die Onkologie hinaus.
```

```persona cs
Sie müssen nicht jede Krebstherapie kennen. Wichtig ist, welche Informationen eine Therapieentscheidung braucht, wo sie entstehen – und warum sie so schwer zusammenzuführen sind. Genau da arbeiten Sie später.
```

```persona clin
Das Modul verbindet Leitlinien, Tumorboard und Shared Decision Making mit der Frage, wie digitale Werkzeuge die Patientensicht im Verlauf sichtbar machen können.
```

```persona tech
Ein Versorgungspfad ist ein verteilter Prozess mit vielen Datenquellen, Formaten und Verantwortlichen. Hier sehen Sie die fachliche Logik hinter den Datenflüssen.
```

```persona pat
Bei einer Therapieentscheidung zählt nicht nur der Befund, sondern auch, was Ihnen wichtig ist. Dieses Modul zeigt, wie Ärzt:innen und Patient:innen gemeinsam entscheiden können.
```

```case
Ein **62-jähriger Raucher** (seit mehr als 25 Jahren) kommt zur hausärztlichen Kontrolle. Er hat keine eindeutigen Beschwerden, aber ein erhöhtes Risiko für Lungenkrebs. Im Gespräch wird ein Lungenkrebs-Screening mittels **Niedrigdosis-CT** thematisiert, das ab April 2026 angeboten wird.
```

## 1 · Therapie beginnt mit einem Ziel

Krankheiten haben Verläufe – Therapie ist eine **bewusste Intervention**, die diese Verläufe gezielt beeinflussen soll.

> Eine medizinische Maßnahme ist nicht automatisch sinnvoll, nur weil sie möglich ist.

Vor jeder Therapieentscheidung stehen drei Fragen:

1. **Was soll erreicht werden?** Heilung, Kontrolle, Symptomlinderung, Lebensqualität, Begleitung?
2. **Welche Maßnahme kann dieses Ziel erreichen?** Medikament, Operation, Intervention, Kombination, Supportivtherapie?
3. **Passt die Maßnahme zum Patienten?** Zustand, Begleiterkrankungen, Präferenzen, Alltag, Risiken?

### Therapieformen

| Therapieform | Grundidee | Beispiele |
|---|---|---|
| Medikamentös | Wirkstoffe beeinflussen biologische Prozesse | Antibiotika, Schmerzmittel, Chemotherapie, Immuntherapie |
| Interventionell | gezielter Eingriff, häufig minimal-invasiv | Katheterverfahren, Endoskopie, Bronchoskopie, Biopsie |
| Operativ | chirurgischer Eingriff zur Entfernung, Rekonstruktion oder Korrektur | Tumoroperation, Appendektomie, Gelenkersatz |

Im Versorgungspfad werden diese Formen häufig kombiniert oder nacheinander eingesetzt. Supportive und palliative Maßnahmen – Schmerztherapie, Atemnotkontrolle, Ernährung, Psychoonkologie – begleiten viele Phasen der Behandlung und sind nicht erst am Lebensende relevant.

```match
question: "Ordnen Sie zu: Welche Therapieform ist das?"
options: ["medikamentös", "interventionell", "operativ"]
items:
  - item: "Bronchoskopie mit Gewebeentnahme"
    answer: "interventionell"
  - item: "Immuntherapie"
    answer: "medikamentös"
  - item: "Appendektomie"
    answer: "operativ"
  - item: "Antibiotikum bei bakterieller Infektion"
    answer: "medikamentös"
  - item: "Katheterverfahren"
    answer: "interventionell"
  - item: "Gelenkersatz"
    answer: "operativ"
```

### Therapieziele

Ein häufiger Denkfehler ist, Therapie automatisch mit Heilung gleichzusetzen. Heilung ist ein zentrales Ziel, aber nicht das einzige:

- **Heilen:** Beseitigung der Erkrankung oder langfristige Krankheitsfreiheit – z. B. kurative Operation, Antibiotikum bei bakterieller Infektion.
- **Kontrollieren:** das Fortschreiten verlangsamen, die Erkrankung stabil halten.
- **Lindern:** Beschwerden und Belastung reduzieren – z. B. Schmerztherapie, Behandlung von Atemnot, Antiemese bei Übelkeit.
- **Begleiten:** Unterstützung im Umgang mit Erkrankung, Verlauf und Einschränkungen – z. B. Nachsorge, palliative Versorgung, psychosoziale Unterstützung.

Diese Ziele sind nicht weniger medizinisch – nur anders. Die Diagnose „Lungenkarzinom“ beschreibt die Erkrankung, bestimmt aber nicht allein das Therapieziel:

```match
question: "Gleiche Diagnose, unterschiedliche Ziele: Welches Therapieziel steht jeweils im Vordergrund?"
options: ["heilen", "kontrollieren", "lindern", "begleiten"]
items:
  - item: "Kleiner, lokal begrenzter Tumor – Operation oder lokale Therapie"
    answer: "heilen"
  - item: "Metastasierte Erkrankung – Systemtherapie, zielgerichtete Therapie, Immuntherapie"
    answer: "kontrollieren"
  - item: "Starke Atemnot oder Schmerzen – supportive und palliative Maßnahmen"
    answer: "lindern"
  - item: "Chronischer oder palliativer Verlauf – kontinuierliche Betreuung, Symptommonitoring, Nachsorge"
    answer: "begleiten"
explain: "Bei metastasierter Erkrankung geht es vor allem darum, Lebenszeit zu verlängern und den Tumor zu kontrollieren. Bei lokal fortgeschrittener Erkrankung kann eine kombinierte Strategie auch kurativ sein. Entscheidend sind Stadium, Allgemeinzustand, verfügbare Therapien und die Ziele des Patienten."
```

### Früherkennung verändert den Möglichkeitsraum

Screening ist selbst keine Therapie – aber es kann beeinflussen, welche Therapieziele später realistisch sind. Viele Lungenkarzinome bleiben lange symptomarm.

| Pfad A: Früherkennung | Pfad B: späte Diagnose |
|---|---|
| Screening → früher Befund | Symptome → fortgeschrittene Erkrankung |
| häufiger lokal begrenzt und potenziell operabel | häufiger metastasiert, höhere Symptomlast |
| lokale Therapieoption | Systemtherapie, Palliativversorgung |
| kuratives Ziel möglich | Kontrolle, Linderung, Begleitung |

Dass ein CT-Screening bei Risikogruppen die Lungenkrebssterblichkeit senken kann, zeigt z. B. die NELSON-Studie [@dekoning2020].

```quiz
question: "Eine palliative Schmerztherapie verkleinert den Tumor nicht, reduziert aber die Schmerzen deutlich. Ist sie erfolgreich?"
options:
  - "Nein, denn der Tumor wurde nicht behandelt"
  - "Ja, denn Therapieerfolg hängt vom Therapieziel ab"
  - "Das lässt sich erst nach einer Bildgebung sagen"
answer: "Ja, denn Therapieerfolg hängt vom Therapieziel ab"
explain: "**Therapieerfolg ist zielabhängig.** Heilung: keine nachweisbare Erkrankung. Kontrolle: stabile Bildgebung, verzögerte Progression. Linderung: weniger Schmerzen, Atemnot, Übelkeit. Begleitung: bessere Lebensqualität, Sicherheit, Orientierung."
```

**Zwischenfazit:** Gute Therapie beginnt nicht mit der Auswahl einer Maßnahme, sondern mit **Zielklärung**. Unser Patient hat bisher nur ein erhöhtes Risiko – bevor über Therapie gesprochen werden kann, müssen Befund, Diagnose, Stadium und Patientenziel geklärt werden.

## 2 · Vom Befund zur Therapieoption

```case
Das Niedrigdosis-CT zeigt einen **auffälligen Rundherd**. Für den Patienten ist das sehr belastend. Medizinisch ist ein auffälliger Befund aber nur ein Hinweis – noch keine Diagnose und erst recht keine Therapieentscheidung.
```

```timeline
title: "Die diagnostische Kette im Lungenkarzinom"
events:
  - when: "Hausärztliche Versorgung"
    what: "Risikoeinschätzung, Beratung, Überweisung"
  - when: "Radiologie"
    what: "Niedrigdosis-CT, Befundung, Verlaufsbeurteilung"
  - when: "Pneumologie"
    what: "klinische Einschätzung, Lungenfunktion"
  - when: "Interventionelle Diagnostik"
    what: "Bronchoskopie, Biopsie, Gewebegewinnung"
  - when: "Pathologie"
    what: "Tumorentität, Histologie, Biomarker"
  - when: "Molekulardiagnostik"
    what: "Mutationen, Fusionen, Expressionsmarker, therapeutische Zielstrukturen"
  - when: "Onkologie / Tumorboard / MTB"
    what: "Therapieoptionen, Leitlinien, Studien, individuelle Entscheidung"
```

Medizinische Entscheidungen entstehen **arbeitsteilig**: Jede Station erzeugt eigene Informationen – und speichert sie oft im eigenen System. Hier begegnen Ihnen die spezialisierten Systeme und Silos aus [[history]] wieder: Bilddaten im PACS, Laborwerte im LIS, Befunde und Dokumentation im KIS, dazu Pathologie- und Molekularbefunde, häufig als Freitext oder PDF.

```match
question: "Welche Daten braucht die Therapieentscheidung? Ordnen Sie die Beispiele dem Datenbereich zu."
options: ["Bildgebung", "Pathologie", "Molekulare Daten", "Laborwerte", "Medikationsdaten", "Patientensicht"]
items:
  - item: "Tumorgröße, Lokalisation, Metastasen"
    answer: "Bildgebung"
  - item: "Tumorentität, Histologie, Differenzierung"
    answer: "Pathologie"
  - item: "Mutationen, Biomarker, therapeutische Zielstrukturen"
    answer: "Molekulare Daten"
  - item: "Organfunktion, Entzündung, Blutbild"
    answer: "Laborwerte"
  - item: "Dauermedikation, Allergien, Interaktionen"
    answer: "Medikationsdaten"
  - item: "Präferenzen, Belastung, Lebensqualität"
    answer: "Patientensicht"
explain: "Dazu kommen klinische Daten (Symptome, Allgemeinzustand, Begleiterkrankungen) und Versorgungsdaten (Vorbehandlungen, Termine, verfügbare Studien). **Therapieentscheidungen sind datenreich – aber Daten müssen verfügbar, verständlich und verknüpfbar sein.**"
```

**Typische Herausforderungen:** Daten liegen in verschiedenen Einrichtungen; Bilddaten, Freitexte und strukturierte Daten sind getrennt; Befunde sind nicht immer maschinenlesbar; molekulare Befunde müssen klinisch interpretiert werden; Patientenangaben werden oft nicht systematisch erfasst.

**Beitrag der Medizinischen Informatik:** Datenintegration und strukturierte Dokumentation, Interoperabilität, Visualisierung und Verlaufsdarstellung, Entscheidungsunterstützung und die Einbindung von PROs/PROMs.

```persona cs
Jede Zeile der Übung oben ist eine eigene Datenquelle mit eigenem Format. Die Vorbereitung eines Tumorboards ist damit eine echte Integrationsaufgabe – genau hier setzen Standards wie FHIR an.
```

### Medikamente: Wirkung, Nebenwirkung, Wechselwirkung

Medikamente wirken nicht isoliert, sondern in einem biologischen Gesamtsystem.

| Therapieform in der Onkologie | Grundprinzip |
|---|---|
| Chemotherapie | greift vor allem schnell teilende Zellen an |
| Immuntherapie | beeinflusst die körpereigene Immunantwort gegen Tumorzellen |
| Zielgerichtete Therapie | richtet sich gegen spezifische molekulare Veränderungen |
| Supportive Medikation | behandelt Symptome oder Nebenwirkungen |

```match
question: "Gewünschte Wirkung, Nebenwirkung oder Wechselwirkung?"
options: ["gewünschte Wirkung", "Nebenwirkung", "Wechselwirkung"]
items:
  - item: "Tumorwachstum bremsen"
    answer: "gewünschte Wirkung"
  - item: "Fatigue"
    answer: "Nebenwirkung"
  - item: "Einfluss auf andere Medikamente"
    answer: "Wechselwirkung"
  - item: "Schmerzen reduzieren"
    answer: "gewünschte Wirkung"
  - item: "Infektionsrisiko"
    answer: "Nebenwirkung"
  - item: "veränderte Wirkung bei eingeschränkter Nierenfunktion"
    answer: "Wechselwirkung"
explain: "Die gewünschte Wirkung ist nur ein Teil der biologischen Gesamtwirkung. Deshalb braucht jede medikamentöse Therapie Monitoring – und die Frage nach der Adhärenz."
```

Patient:innen haben selten nur eine Diagnose. Gerade bei älteren Menschen können Dauermedikation, Herz-Kreislauf-Erkrankungen, COPD, eingeschränkte Nieren- oder Leberfunktion, Diabetes, Blutungsrisiken, Allergien und frühere Therapien die Abwägung erheblich verändern.

### Nutzen-Risiko-Abwägung

| Erwarteter Nutzen | Mögliche Risiken und Belastungen |
|---|---|
| Tumorkontrolle | Nebenwirkungen |
| Lebensverlängerung | Wechselwirkungen |
| Symptomlinderung | Komplikationen |
| Heilungschance | Einschränkung der Lebensqualität |
| Vermeidung von Progression | organisatorische Belastung |
| bessere Alltagsfähigkeit | Therapieabbrüche oder Nicht-Adhärenz |

> **Überwiegt der erwartete Nutzen für *diesen* Patienten in *dieser* Situation?**

### Off-Label Use und personalisierte Therapie

**Off-Label Use** bedeutet: Ein Medikament wird außerhalb der offiziell zugelassenen Anwendung eingesetzt. In der Onkologie ist das relevant, weil die Molekulardiagnostik immer häufiger Veränderungen findet, für die es grundsätzlich passende Wirkstoffe gibt. Dann stellen sich Fragen: Ist der Wirkstoff für diese Tumorart zugelassen? Wie stark ist die Evidenz? Gibt es Studien oder Alternativen? Wie hoch ist das Risiko – und passt die Option zum Therapieziel?

```timeline
title: "Vom molekularen Befund zur Therapieoption"
events:
  - when: "1"
    what: "Tumormarker / Mutation"
  - when: "2"
    what: "passender Wirkstoff"
  - when: "3"
    what: "Evidenz"
  - when: "4"
    what: "Zulassung: zugelassene Therapie, Studie oder Off-Label-Option?"
  - when: "5"
    what: "Risiko"
  - when: "6"
    what: "Ziel der Patientin / des Patienten"
  - when: "7"
    what: "Entscheidung – häufig interdisziplinär im Molecular Tumor Board (MTB)"
```

Wie wirksam Empfehlungen von Molecular Tumor Boards sind und wo Evaluationslücken bestehen, fasst [@gladstone2025] zusammen.

```quiz
question: "Was bedeutet „Off-Label Use“?"
options:
  - "Ein Medikament wird ohne Rezept abgegeben"
  - "Ein Medikament wird außerhalb der offiziell zugelassenen Anwendung eingesetzt"
  - "Ein Medikament wird in einer klinischen Studie erstmals am Menschen getestet"
answer: "Ein Medikament wird außerhalb der offiziell zugelassenen Anwendung eingesetzt"
explain: "Ein passender molekularer Befund heißt nicht automatisch, dass eine Therapie zugelassen, erstattungsfähig oder im konkreten Fall sinnvoll ist."
```

**Zwischenfazit:** Daten sind notwendig, aber sie entscheiden nicht allein. Unser Patient hat nun einen abgeklärten Befund und mögliche Therapieoptionen. Die nächste Frage lautet: *Welche dieser Optionen passt medizinisch und persönlich zu ihm?*

## 3 · Gemeinsam entscheiden

```case
Je nach Stadium und Befunden kommen für unseren Patienten mehrere Wege infrage: Operation, Systemtherapie, Immuntherapie, eine Studie, Supportivtherapie oder Verlaufskontrolle. Manche unterscheiden sich stark, andere haben ähnliche Erfolgsaussichten, aber unterschiedliche Belastungen.
```

**Shared Decision Making (SDM)** bedeutet: Ärzt:innen und Patient:innen treffen eine Therapieentscheidung gemeinsam, wenn mehrere medizinisch vertretbare Optionen bestehen. Drei zentrale Schritte:

1. **Optionen erklären** – Welche Behandlungswege gibt es?
2. **Nutzen und Risiken besprechen** – Was ist wahrscheinlich, was unsicher, welche Belastungen sind möglich?
3. **Präferenzen einbeziehen** – Was ist dem Patienten wichtig? Was passt zu Alltag, Werten und Zielen?

Die Entscheidung entsteht dort, wo **medizinische Evidenz, klinische Erfahrung und Patientenpräferenzen** zusammenkommen. Das bedeutet nicht, dass medizinische Verantwortung abgegeben wird – sie wird gemeinsam tragfähig gemacht. Ein verbreitetes Modell für die Praxis beschreiben [@elwyn2012]. Erinnern Sie sich an Weizenbaums Frage aus [[history]]: Die Therapieentscheidung gehört zu den Aufgaben, die nicht vollständig an ein technisches System delegiert werden sollten.

```persona pat
Für den einen Menschen ist maximale Lebensverlängerung zentral, auch bei hoher Belastung. Für einen anderen sind Alltagsfähigkeit oder Symptomfreiheit wichtiger. Beides ist legitim – und gehört in das Gespräch.
```

Eine Therapie muss nicht nur medizinisch sinnvoll, sondern auch **im Alltag umsetzbar** sein:

| Bereich | Beispiele |
|---|---|
| Körperliche Belastbarkeit | Fatigue, Atemnot, Mobilität, Lungenfunktion |
| Soziales Umfeld | Angehörige, Pflege, Unterstützung, Alleinleben |
| Organisation | Anfahrt, Termine, Therapiezyklen, Wartezeiten |
| Gesundheitskompetenz | Verständnis von Diagnose, Risiko und Therapieplan |
| Emotionale Situation | Angst, Unsicherheit, Therapieerwartungen |
| Persönliche Werte | Lebensqualität, Selbstständigkeit, Lebensverlängerung |

**Adhärenz** beschreibt, inwieweit eine gemeinsam vereinbarte Therapie im Alltag tatsächlich umgesetzt wird – und das sieht primär der Patient selbst.

```quiz
question: "Ein Patient nimmt sein Medikament nicht wie vereinbart ein. Was ist der beste erste Schritt?"
options:
  - "Ihn auf seine Pflicht zur Mitarbeit hinweisen"
  - "Die Gründe verstehen: Nebenwirkungen, Verständnis des Plans, Passung zum Alltag"
  - "Die Therapie sofort beenden"
answer: "Die Gründe verstehen: Nebenwirkungen, Verständnis des Plans, Passung zum Alltag"
explain: "Nicht-Adhärenz sollte nicht moralisch bewertet werden. Werden die Gründe nicht erkannt, bleibt eine Therapie nur theoretisch wirksam."
```

### Patient-Reported Outcomes

**Patient-Reported Outcomes (PROs)** sind Angaben zum Gesundheitszustand, die direkt von Patient:innen berichtet werden; **PROMs** sind die Instrumente (z. B. Fragebögen), mit denen sie erhoben werden. Sie zeigen, wie belastend eine Therapie wirklich ist, ob Symptome zunehmen, ob Nebenwirkungen im Alltag relevant werden und ob Therapieziele erreicht werden. Beim Lungenkrebs sind Atemnot, Husten, Fatigue und Schmerzen besonders relevant. Wie Symptom-Monitoring mit PROs in der Routineversorgung untersucht wurde, zeigt die randomisierte Studie von [@basch2016].

```reflect
question: "Eine Therapie aus zwei Perspektiven: Klinisch ist der Tumor stabil, die Laborwerte sind unauffällig, die Therapie wird planmäßig gegeben. Der Patient berichtet ausgeprägte Fatigue, Angst und Schlafprobleme, sein Alltag ist stark eingeschränkt – er überlegt abzubrechen. Ist die Therapie erfolgreich?"
intro: "Es gibt keine einfache Antwort. Gute Therapiebewertung braucht **beide Perspektiven** – klinische Wirksamkeit und erlebte Belastung. Mögliche nächste Schritte:"
answers:
  - "Belastung strukturiert erfassen (PROs) statt nur zu dokumentieren"
  - "Supportive Maßnahmen gegen Fatigue, Übelkeit und Schlafprobleme prüfen"
  - "das Therapieziel gemeinsam neu besprechen"
  - "Dosis, Rhythmus oder Therapie anpassen"
```

Ein praktisches Beispiel ist das Projekt [PM4Onco](https://pm4onco.de/): Die Patientin oder der Patient füllt einen PROM aus → die Daten werden strukturiert gespeichert → der Verlauf wird visualisiert → das Behandlungsteam bzw. das MTB sieht relevante Veränderungen → die Therapieentscheidung wird angepasst. Erst wenn Technik, Prozesse und Organisation zusammenspielen – das sozio-technische Dreieck aus [[history]] –, wird die Patientensicht tatsächlich entscheidungsrelevant.

```include cycle-de.svg
```

**Therapie ist ein Verlauf, keine Einzelentscheidung.** Im Verlauf können sich Tumoransprechen, Symptomlast, Nebenwirkungen, Patientenziele, Leistungsfähigkeit, molekulare Resistenzmechanismen und verfügbare Therapieoptionen ändern – jedes Mal entsteht eine neue Entscheidungssituation.

## 4 · Leitlinien und Versorgungsrealität

Medizinisches Wissen ist umfangreich, dynamisch und komplex. **Leitlinien** machen es für die Versorgung nutzbar: Sie fassen aktuelle Evidenz zusammen, geben Orientierung für Diagnostik und Therapie, standardisieren Versorgungsprozesse, verbessern Qualität und Sicherheit, reduzieren Über-, Unter- und Fehlversorgung und machen Entscheidungen nachvollziehbar. Sie ersetzen aber nicht das klinische Urteil.

| Standardisierung | Individualisierung |
|---|---|
| Qualität sichern | Einzelfall berücksichtigen |
| Evidenz anwenden | Komorbiditäten beachten |
| Prozesse strukturieren | Patientenpräferenzen einbeziehen |
| Vergleichbarkeit schaffen | Lebensrealität berücksichtigen |
| Fehlversorgung reduzieren | Therapieziel anpassen |

Zu wenig Standardisierung führt zu uneinheitlicher Versorgung; zu wenig Individualisierung dazu, dass die Therapie nicht zum Patienten passt, Risiken unterschätzt werden und die Adhärenz sinkt. Die **medizinische Dokumentation** ist dabei ein Hauptfaktor: Nur was dokumentiert ist, kann begründet von der Leitlinie abweichen.

```match
question: "Leitlinien betreffen den ganzen Versorgungspfad. Zu welcher Station gehört die Frage?"
options: ["Screening", "Pathologie / Molekulardiagnostik", "Staging", "Therapieplanung", "Nachsorge"]
items:
  - item: "Wer soll untersucht werden? Mit welcher Methode?"
    answer: "Screening"
  - item: "Welche Marker sollen bestimmt werden?"
    answer: "Pathologie / Molekulardiagnostik"
  - item: "Wie wird das Ausmaß der Erkrankung klassifiziert?"
    answer: "Staging"
  - item: "Welche Optionen sind empfohlen?"
    answer: "Therapieplanung"
  - item: "Welche Kontrollen sind sinnvoll?"
    answer: "Nachsorge"
```

| Im Idealprozess … | In der Versorgungsrealität … |
|---|---|
| sind alle relevanten Daten vollständig verfügbar | liegen Daten verteilt in verschiedenen Systemen |
| sind Befunde strukturiert und verständlich | sind viele Informationen Freitext, PDF oder Scan |
| sind Leitlinien auf die Situation anwendbar | kommen Befunde zeitversetzt |
| verstehen Patient:innen ihre Optionen | wird die Patientensicht nicht systematisch erhoben |
| liegen PROs im Verlauf vor | erschweren sektorale Brüche den Überblick |

Das ist die Systemlandschaft aus [[history]] – *eher gewachsen als entworfen* – im klinischen Alltag. Medizinische Informatik adressiert hier nicht nur technische Datenprobleme, sondern unterstützt reale Entscheidungsprozesse.

```persona clin
Leitlinien geben Orientierung, aber keine automatische Antwort. Dokumentieren Sie, warum Sie im Einzelfall abweichen – das macht Entscheidungen nachvollziehbar und später auch auswertbar.
```

```quiz
question: "Welche Aussage über Leitlinien trifft zu?"
options:
  - "Leitlinien schreiben jede Einzelfallentscheidung verbindlich vor"
  - "Leitlinien geben Orientierung, ersetzen aber nicht das klinische Urteil"
  - "Leitlinien betreffen nur die Wahl des Medikaments"
answer: "Leitlinien geben Orientierung, ersetzen aber nicht das klinische Urteil"
explain: "Leitlinien strukturieren den ganzen Pfad – vom Screening bis zur Nachsorge – und müssen mit Komorbiditäten, Präferenzen und Lebensrealität verbunden werden."
```

## Zurück zur Leitfrage

> Aus einem Befund wird erst dann eine gute Therapieentscheidung, wenn **medizinische Evidenz, individuelle Patientensituation und Patient:innensicht** zusammengeführt werden.

## Take-home Messages

1. **Therapie ist zielgerichtete Intervention** – heilen, kontrollieren, lindern oder begleiten.
2. **Therapieentscheidungen brauchen Abwägung** von Nutzen, Risiken und Belastungen.
3. **Gute Therapie entsteht gemeinsam** – Shared Decision Making verbindet Evidenz, Erfahrung und Präferenzen.
4. **Patientensicht muss sichtbar gemacht werden** – z. B. mit PROs im Verlauf.
5. **Leitlinien geben Orientierung, aber keine automatische Antwort.**

## Selbsttest

```quiz
question: "Womit beginnt eine gute Therapieentscheidung?"
options:
  - "Mit der Auswahl des wirksamsten Medikaments"
  - "Mit der Klärung des Therapieziels"
  - "Mit der Terminplanung"
answer: "Mit der Klärung des Therapieziels"
```

```quiz
question: "Was ist ein Patient-Reported Outcome (PRO)?"
options:
  - "Ein Laborwert, den die Patientin selbst misst"
  - "Eine Angabe zum Gesundheitszustand, die direkt von Patient:innen berichtet wird"
  - "Der Arztbrief, den Patient:innen erhalten"
answer: "Eine Angabe zum Gesundheitszustand, die direkt von Patient:innen berichtet wird"
```

```quiz
question: "Wann ist Shared Decision Making besonders wichtig?"
options:
  - "Wenn es genau eine medizinisch sinnvolle Option gibt"
  - "Wenn mehrere medizinisch vertretbare Optionen bestehen"
  - "Nur bei Studienteilnahmen"
answer: "Wenn mehrere medizinisch vertretbare Optionen bestehen"
```

```quiz
question: "Warum ist die Vorbereitung eines Tumorboards eine Aufgabe für die Medizinische Informatik?"
options:
  - "Weil Tumorboards nur online stattfinden"
  - "Weil die nötigen Daten aus vielen Systemen und Formaten zusammengeführt werden müssen"
  - "Weil Informatiker:innen die Therapie festlegen"
answer: "Weil die nötigen Daten aus vielen Systemen und Formaten zusammengeführt werden müssen"
explain: "Bildgebung, Pathologie, Molekulardiagnostik, Labor, Medikation und Patientensicht entstehen an verschiedenen Orten – das ist die Integrationsaufgabe aus Abschnitt 2."
```

**Ausblick:** Die nächste Einheit behandelt die Pflege als Profession – Pflegeaufgaben, Pflegeprozess sowie Pflegedokumentation und IT.
