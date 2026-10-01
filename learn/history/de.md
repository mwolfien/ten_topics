---
title: "Geschichte und Entwicklung der Medizinischen Informatik"
summary: "Warum viele heutige Digitalisierungsprobleme – Silos, Medienbrüche, geringe Akzeptanz – historisch gewachsen sind, und weshalb Medizinische Informatik immer ein sozio-technisches Feld ist."
duration_minutes: 30
level: "Einstieg"
audiences: [med, cs, clin, tech, pat]
order: 1
course: "Einführung in die Medizinische Informatik"
author: "Markus Wolfien"
objectives:
  - "Frühe Treiber der Digitalisierung im Gesundheitswesen benennen"
  - "KIS, LIS und PACS historisch und funktional einordnen"
  - "Erklären, warum Datensilos historisch gewachsen sind"
  - "Medizinische Informatik als sozio-technisches Feld beschreiben"
  - "Grundlegende ethische Fragen zu Verantwortung und Delegation erkennen"
readings: [haux2006, berg2001, sittig2010, hayrinen2008]
related_topics: [ehr-cis, fhir, cdss]
source: "Vorlesung 2 „Geschichte und Entwicklung der Medizinischen Informatik“, Einführung in die Medizinische Informatik (SoSe 2026), Markus Wolfien, IMB & ZMI"
---

> *„Befund gesucht – Akte nicht verfügbar – Information wird erneut erhoben.“*

Diese Szene kennt fast jede:r, die oder der schon einmal im Krankenhaus gearbeitet hat. Wir beginnen deshalb nicht mit einer technischen Definition, sondern mit einer historischen Perspektive: **Medizinische Informatik ist nicht einfach Informatik im Krankenhaus.** Sie verbindet medizinisches Wissen, Daten, Organisation, Technik und Verantwortung.

```persona med
Im Stationsalltag werden Sie mit gewachsenen Systemlandschaften arbeiten. Wer versteht, *warum* Befunde in drei Systemen liegen, kann besser mit ihnen umgehen – und bei der nächsten Einführung mitreden.
```

```persona cs
Krankenhaus-IT ist ein Paradebeispiel für Legacy-Systeme. Die Geschichte erklärt, warum „einfach eine neue Schnittstelle bauen“ selten reicht.
```

```persona clin
Viele Frustrationen mit Dokumentationssystemen sind Passungsprobleme, keine Bedienfehler. Diese Einheit gibt Ihnen Begriffe, um sie zu benennen.
```

```persona tech
Sie kennen Software-Architektur – hier lernen Sie, warum sie im Gesundheitswesen nie ohne Organisation, Recht und klinische Arbeit gedacht werden kann.
```

```persona pat
Warum muss ich meine Befunde immer wieder mitbringen? Diese Einheit erklärt, wie es dazu kam – und was sich gerade ändert.
```

## Warum mit Geschichte beginnen?

Wenn heute über Digitalisierung im Gesundheitswesen gesprochen wird, fallen immer wieder dieselben Begriffe: **Datensilos, Medienbrüche, Schnittstellenprobleme, Akzeptanz, Datenschutz.** Diese Probleme sind nicht plötzlich entstanden – viele haben historische, organisatorische und technische Ursachen.

Eine erste These:

> **„Digitalisierung im Gesundheitswesen ist nie nur ein technisches Projekt.“**

Sie verändert klinische Arbeitsprozesse, organisatorische Zuständigkeiten, Informationsflüsse, Verantwortung und Entscheidungsräume – und das Verhältnis zwischen Patient:innen, Medizin und Technik.

## 1 · Vom Papier zur frühen EDV

Vor der Digitalisierung war medizinische Information vor allem papierbasiert, handschriftlich oder formularbasiert, lokal verfügbar und an einzelne Orte oder Personen gebunden. Papier ist nicht automatisch schlecht – es war lange ein flexibles und robustes Medium. Aber es hat Grenzen:

| Papierbasierte Information | Digitale Information |
|---|---|
| lokal | potenziell vernetzt |
| schwer durchsuchbar | durchsuchbar |
| schwer auswertbar | auswertbar |
| ortsgebunden | übertragbar |

Typische Folgen papierbasierter Dokumentation: Suchaufwand, Doppelarbeit, unvollständige Informationen, begrenzte Lesbarkeit, verzögerte Weitergabe und eingeschränkte Auswertbarkeit. Viele dieser Probleme kennen Sie auch außerhalb der Medizin – dort betreffen sie aber Diagnostik, Therapie und Patientensicherheit.

```quiz
question: "Was wurde in Krankenhäusern vermutlich **zuerst** digitalisiert?"
options:
  - "Komplexe Therapieentscheidungen"
  - "Das Arzt-Patienten-Gespräch"
  - "Abrechnung und Leistungsdokumentation"
  - "Interprofessionelle Fallkonferenzen"
answer: "Abrechnung und Leistungsdokumentation"
explain: "Digitalisierung beginnt oft dort, wo Prozesse **formal beschreibbar, wiederkehrend, dokumentationspflichtig und ökonomisch relevant** sind – und sich leicht in Datenstrukturen überführen lassen. Entscheidend ist hier das *Warum*."
```

Die ersten IT-Einsätze betrafen gut formalisierbare Bereiche: Patientenverwaltung, Leistungsdokumentation, Abrechnung, Ressourcen- und Bettenverwaltung, Berichtswesen und einfache Statistik. Der Anfang war also nicht die künstliche Intelligenz oder der digitale Zwilling – sondern dort, wo Informationen gezählt, geordnet, standardisiert und abgerechnet werden mussten.

```match
question: "Raten Sie die Zeitachse: Welche Phase gehört zu welchem Zeitraum?"
options: ["bis 1960er", "1960er–70er", "1970er–80er", "1990er–heute"]
items:
  - item: "Vernetzung, Krankenhausinformationssysteme, elektronische Akten (ePA)"
    answer: "1990er–heute"
  - item: "Papierakte als Standard"
    answer: "bis 1960er"
  - item: "Erste klinische Subsysteme, z. B. Labor und Bildarchivierung"
    answer: "1970er–80er"
  - item: "EDV für die Verwaltung (Finanzen, Aufnahme)"
    answer: "1960er–70er"
explain: "Die Entwicklung verlief von der Verwaltung über einzelne klinische Subsysteme hin zur Vernetzung – nicht als zentral geplanter Gesamtentwurf. Die Zeiträume sind grobe Orientierung."
```

```timeline
title: "Grobe Entwicklungslinien"
collapsed: "Auflösung: die Zeitachse anzeigen"
events:
  - when: "bis 1960er"
    what: "Papierbasierte Dokumentation"
  - when: "1960er–70er"
    what: "EDV für Verwaltung: Finanzen, Aufnahme"
  - when: "1970er–80er"
    what: "Erste klinische Subsysteme: Labor, Bildarchivierung (PACS)"
  - when: "1990er–heute"
    what: "Vernetzung, KIS, elektronische Patientenakten (ePA)"
```

### Warum gerade Dokumentation, Abrechnung und Verwaltung?

> **Was formal beschreibbar ist, wird oft zuerst digitalisiert.**

- **Standardisierbarkeit:** Viele administrative Abläufe lassen sich formal beschreiben.
- **Administrativer Druck:** Krankenhäuser müssen Leistungen dokumentieren und nachweisen.
- **Wirtschaftlichkeit:** Digitale Systeme versprachen Effizienz, Übersicht und Steuerbarkeit.

Administration ist dabei nicht nebensächlich: *Wer ist Patient:in? Wann beginnt ein Behandlungsfall? Welche Leistungen und Befunde gehören dazu? Wer ist verantwortlich?* Genau diese Strukturen erzeugen die Datenflüsse, auf denen spätere klinische und wissenschaftliche Nutzung aufbaut.

| Administrative Prozesse | Medizinische Entscheidungen |
|---|---|
| stärker regelbasiert | stärker kontextabhängig |
| gut standardisierbar | häufig mehrdeutig |
| formal dokumentierbar | abhängig von Erfahrung und Situation |
| ökonomisch relevant | klinisch und ethisch folgenreich |
| früh digitalisiert | später und vorsichtiger unterstützt |

## 2 · KIS, LIS und PACS

Aus den frühen Digitalisierungsinseln entwickelten sich spezialisierte Informationssysteme – für Aufnahme und Verwaltung, Station, Labor, Radiologie, OP und Entlassmanagement.

- **KIS – Krankenhausinformationssystem:** das „Rückgrat“ der digitalen Krankenhausorganisation. Patientenaufnahme und Fallverwaltung, klinische Dokumentation, Anordnungen und Befunde, Leistungsdokumentation, Entlassmanagement, Schnittstellen zu Subsystemen.
- **LIS – Laborinformationssystem:** unterstützt Laborprozesse von der Probe bis zum Befund. Labore waren *Early Adopter*: hohe Standardisierbarkeit, strukturierte Daten, klare Prozessketten.
- **PACS – Picture Archiving and Communication System:** speichert, archiviert und kommuniziert Bilddaten zwischen Geräten und Arbeitsplätzen und stellt Voraufnahmen für den Vergleich bereit. Bilddaten sind groß, visuell und zeitkritisch – sie brauchen eine eigene Infrastruktur.

| Bereich | Datentyp | Prozesslogik | Typisches System |
|---|---|---|---|
| Station | klinische Dokumentation | kontinuierliche Versorgung | KIS |
| Labor | Messwerte, Proben | standardisierte Analyse | LIS |
| Radiologie | Bilddaten | Bildgebung und Befundung | PACS |
| Verwaltung | Fall- und Abrechnungsdaten | administrative Steuerung | KIS / ERP |

```match
question: "Mini-Übung: Welches System macht was?"
options: ["KIS", "LIS", "PACS"]
items:
  - item: "Laborwerte validieren und übermitteln"
    answer: "LIS"
  - item: "Radiologische Bilddaten speichern und anzeigen"
    answer: "PACS"
  - item: "Patientenaufnahme und Fallverwaltung unterstützen"
    answer: "KIS"
  - item: "Entlassbrief vorbereiten"
    answer: "KIS"
  - item: "Voraufnahmen für den Bildvergleich bereitstellen"
    answer: "PACS"
  - item: "Probenstatus nachverfolgen"
    answer: "LIS"
explain: "Die Systeme sind nicht zufällig getrennt: Sie spiegeln unterschiedliche Aufgaben, Datentypen und Prozesslogiken wider. *Subsysteme sind Ausdruck fachlicher Spezialisierung, nicht nur technischer Fragmentierung.*"
```

Spezialisierung ist zunächst eine Stärke: passgenaue Unterstützung, hohe Prozessnähe, bessere Abbildung spezifischer Datenarten. **Aber** die Integration wird komplexer, Datenmodelle unterscheiden sich, Verantwortlichkeiten verteilen sich – und Schnittstellen werden notwendig. Klinische IT-Landschaften entstanden schrittweise, über viele Jahre, mit unterschiedlichen Herstellern und lokalen Anpassungen:

> **Krankenhaus-IT ist oft eher gewachsen als entworfen.**

## 3 · Silos und Prozesse

Historisch gewachsene Landschaften führen zu **Silos** – und zwar nicht nur technischen:

| Technische Silos | Organisatorische Silos |
|---|---|
| getrennte Datenbanken | getrennte Verantwortlichkeiten |
| unterschiedliche Schnittstellen | unterschiedliche Dokumentationskulturen |
| inkompatible Datenformate | abteilungsspezifische Prozesse |
| fehlende semantische Harmonisierung | lokale Prioritäten |

Deshalb ist Interoperabilität nie nur ein Schnittstellenthema. Ein IT-System wirkt nie allein, sondern ist immer Teil eines größeren Arbeits- und Versorgungssystems – mit Daten, Nutzer:innen, Prozessen, Organisation, Recht und Infrastruktur.

```include triangle-de.svg
```

Das **sozio-technische Dreieck** ist eine Schlüsselidee für alle weiteren Themen – von der elektronischen Patientenakte über Interoperabilität bis zur KI-gestützten Entscheidungsunterstützung. Ein ausführlicheres Modell mit acht Dimensionen beschreiben [@sittig2010].

**Systeme bilden Prozesse nicht nur ab – sie verändern sie.** Schon ein Pflichtfeld verändert, was dokumentiert wird; eine automatische Benachrichtigung verändert, wer wann reagiert. Früher: mündliche Übergabe, Papiernotiz, späterer Eintrag. Heute: digitale Maske, Pflichtfelder, automatische Weiterleitung. Umgekehrt müssen gute Systeme die klinische Realität kennen: Zeitdruck, Ausnahmen, verschiedene Berufsgruppen, kritische Situationen, unsichere Informationen – sonst entstehen Zusatzaufwand und Workarounds.

> **Akzeptanz ≈ Nutzen + Passung + Vertrauen – Zusatzaufwand**

```reflect
question: "Mini-Fall: Ein Krankenhaus führt ein neues Dokumentationssystem ein. Es erfüllt formal alle Anforderungen. Danach berichten Ärzt:innen und Pflegekräfte über zusätzliche Klicks, doppelte Dokumentation, unklare Zuständigkeiten und sinkende Akzeptanz. Ist das Problem technisch, organisatorisch oder prozessual?"
intro: "Meist nicht entweder–oder, sondern ein **Passungsproblem** zwischen System-, Arbeits-, Dokumentations-, Verantwortungs- und Organisationslogik. Hebel sind z. B.:"
answers:
  - "technische Umsetzung nachbessern"
  - "Prozessanalyse *vor* der Einführung"
  - "Schulung und Begleitung"
  - "klare Verantwortlichkeiten"
  - "Nutzerorientierung und eine schrittweise Einführungsstrategie"
```

| Typische Fehlentwicklung | Mögliche Folge |
|---|---|
| fehlende Prozessanalyse | System passt nicht zum Alltag |
| geringe Nutzerbeteiligung | geringe Akzeptanz |
| mangelnde Interoperabilität | Datensilos |
| unklare Verantwortung | keine nachhaltige Verbesserung |

Viele Projekte scheitern nicht an der technischen Idee, sondern an Einführung, Einbettung und Anschlussfähigkeit – siehe auch [@berg2001].

```quiz
question: "Eine Klinik will ein KI-Tool zur Entscheidungsunterstützung einführen. Welche Lehre aus der Geschichte ist am wichtigsten?"
options:
  - "Das beste Modell auswählen – der Rest ergibt sich"
  - "Erst die Prozesse und Verantwortlichkeiten verstehen, dann das System einführen"
  - "Das Tool zunächst ohne Einbeziehung der Nutzer:innen testen"
answer: "Erst die Prozesse und Verantwortlichkeiten verstehen, dann das System einführen"
explain: "Alte Muster, neue Technologien: Auch KI wird nicht erfolgreich sein, wenn Datenqualität, Prozessintegration, Verantwortung und Nutzbarkeit nicht stimmen. Dasselbe gilt für Dashboards, Telemedizin, Forschungsdatenplattformen und Patienten-Apps."
```

```persona clin
Wenn Sie an einer Systemeinführung beteiligt sind: Fragen Sie früh nach Prozessanalyse, Schulung und Evaluation nach der Einführung. Das sind die Punkte, an denen Projekte am häufigsten scheitern.
```

```persona cs
Anforderungen „formal erfüllt“ heißt nicht „im Alltag nutzbar“. Beobachten Sie reale Arbeitsabläufe, bevor Sie Datenmodelle und Masken entwerfen.
```

## 4 · Verantwortung

Ethik kommt nicht erst mit der künstlichen Intelligenz ins Spiel. Schon die Digitalisierung von Dokumentation und Informationsflüssen verändert, wer was sehen kann, was standardisiert wird und wie Verantwortung verteilt ist.

| Technische Entwicklung | Ethische Frage |
|---|---|
| digitale Dokumentation | Wer darf was wissen? |
| strukturierte Datenerfassung | Was geht bei Standardisierung verloren? |
| Entscheidungsunterstützung | Wer trägt Verantwortung? |
| Datenintegration | Wie bleibt Vertrauen erhalten? |

**Joseph Weizenbaum** – der Informatiker, der 1966 mit ELIZA eines der ersten Chatprogramme schrieb – warnte später in *Die Macht der Computer und die Ohnmacht der Vernunft* (1977) vor naiver Technikeuphorie. Sinngemäß: *Nicht alles, was technisch möglich ist, sollte unreflektiert an Computer delegiert werden.* Er betonte den Schutz menschlicher Urteilskraft und die Sensibilität für menschliche Beziehungen – Fragen, die mit heutigen Sprachmodellen aktueller sind denn je.

```reflect
question: "Welche Aufgabe sollte Ihrer Meinung nach niemals vollständig an ein technisches System delegiert werden – und warum?"
intro: "Häufig genannte Beispiele:"
answers:
  - "die Therapieentscheidung"
  - "das Gespräch über schlechte Nachrichten"
  - "die Priorisierung in Grenzfällen"
  - "die finale Übernahme von Verantwortung"
```

**Hans Jonas** (*Das Prinzip Verantwortung*, 1979) betont sinngemäß: *Je größer die Reichweite technischer Möglichkeiten, desto größer die Verantwortung für ihre Folgen.* Je weiter digitale Systeme in klinisches Handeln hineinreichen, desto wichtiger wird ethische Reflexion – nicht als Gegensatz zur Innovation, sondern als ihre Voraussetzung.

```persona pat
Sie haben ein Recht darauf zu wissen, wer Ihre Daten sieht und wie Systeme Entscheidungen über Ihre Behandlung vorbereiten. Die Verantwortung bleibt bei den Menschen, die Sie behandeln.
```

## Take-home Messages

1. Frühe Digitalisierung in der Medizin begann vor allem mit **Dokumentation, Abrechnung und Verwaltung**.
2. Klinische Informationssysteme entstanden als **spezialisierte Lösungen** für unterschiedliche Datenarten und Arbeitsprozesse.
3. Viele heutige Probleme – Silos, mangelnde Interoperabilität, geringe Akzeptanz – sind **historisch und organisatorisch gewachsen**.
4. Medizinische Informatik ist ein **sozio-technisches Feld**: Technik, Prozesse, Organisation und Verantwortung gehören zusammen.
5. Geschichte erklärt die Gegenwart und öffnet den Blick auf die Zukunft der Medizin.

## Selbsttest

```quiz
question: "Wofür steht PACS?"
options:
  - "Patient Administration and Care System"
  - "Picture Archiving and Communication System"
  - "Process Analysis and Clinical Support"
answer: "Picture Archiving and Communication System"
explain: "PACS speichert, archiviert und kommuniziert medizinische Bilddaten."
```

```quiz
question: "Warum waren Labore „Early Adopter“ der Digitalisierung?"
options:
  - "Weil Labore die meisten Mitarbeitenden hatten"
  - "Wegen hoher Standardisierbarkeit, strukturierter Daten und klarer Prozessketten"
  - "Weil Laborbefunde nicht dokumentiert werden müssen"
answer: "Wegen hoher Standardisierbarkeit, strukturierter Daten und klarer Prozessketten"
```

```quiz
question: "Welche Aussage über Datensilos trifft am besten zu?"
options:
  - "Silos sind ein rein technisches Problem fehlender Schnittstellen"
  - "Silos haben technische und organisatorische Ursachen"
  - "Silos gibt es seit der Einführung von FHIR nicht mehr"
answer: "Silos haben technische und organisatorische Ursachen"
explain: "Getrennte Datenbanken und Formate *und* getrennte Verantwortlichkeiten, Dokumentationskulturen und lokale Prioritäten."
```

```quiz
question: "Welche drei Ecken hat das sozio-technische Dreieck?"
options:
  - "Hardware, Software, Netzwerk"
  - "Technik, Organisation, Prozesse"
  - "Ärzt:innen, Pflege, Verwaltung"
answer: "Technik, Organisation, Prozesse"
```

```quiz
question: "Worauf wies Joseph Weizenbaum besonders hin?"
options:
  - "Computer sollten möglichst alle ärztlichen Entscheidungen übernehmen"
  - "Nicht alles technisch Mögliche sollte unreflektiert an Computer delegiert werden"
  - "Ethik spielt erst bei künstlicher Intelligenz eine Rolle"
answer: "Nicht alles technisch Mögliche sollte unreflektiert an Computer delegiert werden"
```

**Ausblick:** Die nächste Einheit behandelt nationale und internationale Fachgesellschaften, die wissenschaftliche Kultur und die Professionalisierung der Medizinischen Informatik.
