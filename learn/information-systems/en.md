---
title: "HIS, LIS and RIS/PACS – How Clinical Information Systems Work Together"
summary: "How the hospital information system, laboratory and radiology systems work together as one information system – and why integrating them is so hard. We follow one patient and her data through a hospital's system landscape."
duration_minutes: 50
level: "In-depth"
audiences: [med, cs, clin, tech, pat]
order: 3
builds_on: [history]
course: his
lecture: 2
author: "Eveline Prochaska, Markus Wolfien"
objectives:
  - "Distinguish and assess typical architectures of clinical system landscapes (all-in-one, best-of-breed, spaghetti, star)"
  - "Explain the role of ADT for patient identity and care context"
  - "Describe the order/result pattern as the shared logic of diagnostic systems"
  - "Trace the laboratory workflow from the order to the validated result"
  - "Explain the radiology workflow with RIS, PACS and DICOM"
  - "Identify interfaces, redundancies and failure risks in a patient case"
readings: [winter2023, carraro2007, sittig2010]
related_topics: [ehr-cis, fhir, data-quality]
source: "Lecture 2 “HIS, LIS and RIS/PACS – How Clinical Information Systems Work Together”, Health Information Systems (winter term 2026/27), Eveline Prochaska and Markus Wolfien, IMB & ZMI"
---

> **Guiding question:** How do the HIS, LIS and RIS/PACS work together as one information system – and why is integrating them so hard?

In the module [[history]] you saw *why* the hospital information system (HIS), the laboratory information system (LIS) and PACS came about: as answers to different data types and process logics. *Subsystems express professional specialisation, not just technical fragmentation.* Now we ask **how** these systems work together, technically and in practice. Rather than going system by system, we follow one flow of information – one patient, one case and her path through the system landscape.

```persona med
You will place orders, read results and transfer patients every day. This module shows what happens in the background – and where a result can get lost.
```

```persona cs
You know much of this under other names: order/result is a request–response pattern with correlation IDs, ADT is an event stream, the communication server is a message broker. What is new is what a lost event means here.
```

```persona clin
A result only counts as delivered once someone has seen it and acted on it. The module shows why transfers, duplicate records and critical values need special attention.
```

```persona tech
Spaghetti versus star is point-to-point versus hub-and-spoke. It gets interesting when you ask which direct connections bypass monitoring – and who is on call at night.
```

```persona pat
Why are you asked for your name and date of birth again and again in hospital, and why do you wear a wristband with a barcode? This module explains how much depends on it.
```

```case
**Mrs Erika Müller, 68 years** (born 12 March 1958). Tuesday, 14:05, emergency department (ED): temperature 39.2 °C, SpO₂ 89 %, respiratory rate 28/min, reduced general condition. Working diagnosis: suspected community-acquired pneumonia.

Over the next hours come admission and case creation, laboratory tests including blood gas analysis and blood cultures, a chest X-ray and, the next day, a CT. Mrs Müller deteriorates and is transferred to the intensive care unit. **We are not following the medicine, but the data.**
```

```quiz
question: "Warm-up: How many systems does Mrs Müller touch in the first 24 hours of her stay?"
options:
  - "1–2 – “The HIS does everything.”"
  - "3–5 – HIS plus lab and radiology"
  - "6–9 – a few more specialist systems"
  - "10 or more – a whole landscape"
answer: "10 or more – a whole landscape"
explain: "HIS with admission/ADT, order entry and clinical documentation, communication server, LIS for clinical chemistry, LIS for microbiology, POCT middleware for the blood gas analysis, RIS, modality (X-ray/CT), PACS, PDMS in intensive care, billing/DRG – and considerably more depending on the hospital. **Every one of these systems needs the same context: Who is the patient? Which case does this belong to? Where is she right now?**"
```

> **Integration is not the exception but everyday routine** – even for a “normal” routine admission.

## 1 · Architectures: how are clinical system landscapes built?

You can ask two questions of any system landscape – and the answers are **independent of each other** ([@winter2023]):

1. **How many applications?** (logical level) One vendor's integrated suite – *all-in-one* – or the strongest specialist system for each area – *best-of-breed*?
2. **How do they communicate?** (technical level) Many direct point-to-point connections – *spaghetti* – or communication through a central integration layer – *star*?

| | All-in-one | Best-of-breed |
|---|---|---|
| Idea | as many functions as possible from one suite | the strongest system for each area |
| Strengths | uniform interface and data base, few internal interfaces, one contract partner | systems that fit each specialty, exchangeable components, innovation per department |
| Weaknesses | vendor dependence (lock-in), some modules weaker in their field, special processes hard to map | many interfaces, high integration effort, redundant master data, inconsistent user interfaces, many contracts |

In reality – including at the University Hospital Dresden (UKDD) – you mostly find **hybrids**: a core HIS plus specialised subsystems (LIS, RIS/PACS, PDMS …). Specialisation makes sense clinically, but it shifts complexity into integration.

```match
question: "All-in-one or best-of-breed? Assign each property."
options: ["All-in-one", "Best-of-breed"]
items:
  - item: "one contract partner"
    answer: "All-in-one"
  - item: "individual components can be exchanged"
    answer: "Best-of-breed"
  - item: "dependence on the vendor (lock-in)"
    answer: "All-in-one"
  - item: "redundant master data in many systems"
    answer: "Best-of-breed"
  - item: "uniform interface and data base"
    answer: "All-in-one"
  - item: "innovation per department"
    answer: "Best-of-breed"
```

### Spaghetti or star?

In the **spaghetti** pattern every system talks directly to every other. In the worst case the number of interfaces grows quadratically: **n · (n − 1) / 2**. Each one has to be built, tested, checked with every update and monitored. In the **star** pattern each system has exactly one connection to the communication server – that grows linearly: **n**. With 6 systems that is 15 versus 6 connections.

```quiz
question: "A hospital has 30 systems. How many interfaces would the spaghetti pattern need in the worst case?"
options: ["30", "60", "435", "900"]
answer: "435"
explain: "30 · 29 / 2 = 435 – the star would need 30. The calculation is a worst case, because not every system has to talk to every other. The principle holds: direct connections scale badly."
```

The **communication server** (also integration engine or interface engine) is more than a distributor. It takes on four tasks – and is at the same time a *single point of failure* that needs high availability, monitoring and clear responsibilities.

```match
question: "Which task of the communication server is needed in each case?"
options: ["Routing", "Transformation & mapping", "Buffering (queueing)", "Monitoring & logging"]
items:
  - item: "Every transfer should go to the LIS, RIS and PDMS."
    answer: "Routing"
  - item: "The HIS sends HL7 v2.3, the LIS expects v2.5 and different ward codes."
    answer: "Transformation & mapping"
  - item: "The LIS is briefly unreachable after an update; no message may be lost."
    answer: "Buffering (queueing)"
  - item: "A message did not arrive and needs to be traced and resent."
    answer: "Monitoring & logging"
explain: "Remember the buffering: in the failure scenario at the end, a stuck queue plays the leading role."
```

| | All-in-one | Best-of-breed |
|---|---|---|
| **Star** | integrated suite, third-party systems cleanly connected via the communication server | many specialist systems, consistently integrated via the communication server |
| **Spaghetti** | suite, but additional systems “bolted on” directly | grown landscape with many direct interfaces |

*Best-of-breed is not automatically spaghetti, and all-in-one is not automatically interoperable.* Integrated internally does not mean standardised externally – for referring physicians, the electronic patient record (ePA) or research, for instance. The bottom right is the historically grown state from [[history]]: *grown rather than designed*.

```include landscape-en.svg
```

```reflect
question: "Warm-up: all-in-one, best-of-breed, star or spaghetti – what do you see in this landscape? And where would you look first when something goes wrong?"
intro: "It is a **hybrid**:"
answers:
  - "The HIS suite is all-in-one internally (six modules, one vendor)."
  - "With LIS, RIS, PDMS and OR system from different vendors, the landscape as a whole is best-of-breed."
  - "In terms of communication it is mostly a star around the communication server – but with direct connections: RIS ↔ PACS, LIS ↔ POCT middleware, PDMS ↔ medical devices and the image link HIS → PACS."
  - "Direct connections are often well justified (data volume, real time, vendor coupling), but they bypass the communication server's monitoring. When something fails, people look at the server first – the direct connections are easily forgotten."
```

## 2 · ADT: the organisational backbone

**ADT** stands for *admission, discharge, transfer* and answers three questions: **Who is the patient, in which case, and where is she right now?** That sounds like administration, but it is the underrated key to everything that follows.

```timeline
title: "Mrs Müller's stay as ADT events"
events:
  - when: "Tue 14:05 · A01"
    what: "Admission in the emergency department"
  - when: "Tue 18:40 · A02"
    what: "Transfer to the intensive care unit"
  - when: "Fri 10:15 · A02"
    what: "Transfer to pulmonology (ward P3)"
  - when: "Day 9, 11:00 · A03"
    what: "Discharge home"
```

Every movement changes the context in which all other systems work. Three levels need to be kept apart:

| Level | Meaning | for Mrs Müller |
|---|---|---|
| **Patient** | the person: master data such as name, date of birth, sex, insurance; the patient ID stays the same within the hospital | ID 4711 |
| **Case** | one episode of care: the bracket for documentation, services and billing (DRG) | F2024-0312 (hip surgery, closed) and F2026-0815 (pneumonia, current) |
| **Movement** | where and when within the case: ward, bed, department, period | ED → ICU → P3 |

Terms vary by vendor; in HL7 v2 the case level is called *visit* (PV1 segment), in FHIR *Encounter*.

```match
question: "Which level is the system looking at?"
options: ["Patient", "Case", "Movement"]
items:
  - item: "The LIS looks up Mrs Müller's previous values."
    answer: "Patient"
  - item: "Billing groups the DRG."
    answer: "Case"
  - item: "The PDMS shows Mrs Müller on the ICU ward list."
    answer: "Movement"
  - item: "The PACS finds the images from the 2024 hip surgery as priors."
    answer: "Patient"
```

Almost every system keeps a **copy of the ADT context**: the LIS (for sample assignment, previous values, result routing and age- and sex-specific reference ranges), RIS/PACS (for assigning images and priors), the PDMS (for the ward list and monitor data), billing (for the DRG and the data transfer to the health insurer under § 301 of the German Social Code, SGB V) and even bed and kitchen planning. **These copies have to stay current.**

### Events instead of queries

The systems do not keep asking the HIS. Instead the HIS reports every event, and the communication server distributes it to all subscribers. The consequence: **if an event is lost, the copy is out of date – often without anyone noticing.**

```match
question: "Which HL7 v2 event type fits?"
options: ["A01", "A02", "A03", "A08", "A11", "A40"]
items:
  - item: "Mrs Müller is admitted to the emergency department."
    answer: "A01"
  - item: "She is transferred to the intensive care unit."
    answer: "A02"
  - item: "She is discharged home."
    answer: "A03"
  - item: "Her address is corrected."
    answer: "A08"
  - item: "An admission created by mistake is cancelled."
    answer: "A11"
  - item: "Two records of the same person are merged."
    answer: "A40"
explain: "The corrections in particular – cancellations (A11) and merges (A40) – are error-prone, because every receiving system has to apply them correctly."
```

This is what the transfer looks like as a (simplified) HL7 v2 message. Each line is a segment, `|` separates fields, `^` separates components:

```text
MSH|^~\&|KIS|KLINIKUM|LIS|LABOR|202610131840||ADT^A02|MSG0471|P|2.5
EVN|A02|202610131840
PID|1||4711^^^KLINIKUM^PI||Müller^Erika||19580312|F
PV1|1|I|ITS^01^B|||ZNA^03^A|||||||||||||F2026-0815
```

`MSH` is the header (sender, receiver, type), `EVN` the event, `PID` the patient, `PV1` the stay or case. (The sender here is the German *KIS*, the receiver the *LIS*; *ITS* is the intensive care unit, *ZNA* the emergency department.) The many empty fields are normal: HL7 v2 is a toolkit from which each organisation uses only a part – a strength and a weakness at the same time.

```match
question: "Read along: what is where in the message?"
options: ["Patient ID (who?)", "new location (ward^room^bed)", "previous location", "case number (which case?)", "message type and event"]
items:
  - item: "`ADT^A02`"
    answer: "message type and event"
  - item: "`4711`"
    answer: "Patient ID (who?)"
  - item: "`ITS^01^B`"
    answer: "new location (ward^room^bed)"
  - item: "`ZNA^03^A`"
    answer: "previous location"
  - item: "`F2026-0815`"
    answer: "case number (which case?)"
```

### Patient identity: duplicates and mix-ups

| | Duplicate: one person, two IDs | Mix-up: two people, one ID |
|---|---|---|
| Example | ID 4711 Erika Müller and ID 8823 Erika Mueller, both born 12 March 1958 | ID 4711 Erika Müller born 12 March 1958 and born 7 November 1961 |
| Risk | results are split across two records, previous values and priors are missing | results of the wrong person → wrong therapy decision |
| Countermeasure | merging (A40), master patient index, duplicate checks | a second identifier, patient wristband with barcode |

> **Patient identification is not an administrative matter but patient safety.**

```match
question: "Duplicate or mix-up?"
options: ["Duplicate", "Mix-up"]
items:
  - item: "The delta check finds no previous value although Mrs Müller has often been in the hospital."
    answer: "Duplicate"
  - item: "The record contains a lab value that belongs to another patient."
    answer: "Mix-up"
  - item: "“Müller” and “Mueller” with the same date of birth under two IDs"
    answer: "Duplicate"
  - item: "Two patients with the same name are kept under one ID."
    answer: "Mix-up"
explain: "Duplicates are common and more of a nuisance than an acute danger; mix-ups are rarer but dangerous. That is why clinical practice always uses two identifiers."
```

## 3 · Orders & results: what should happen – and what came of it?

**ADT** says: *Who? Which case? Where?* **Order/result** says: *What should happen – and what came of it?* Think of ADT as the rail on which many order loops hang: laboratory (blood count, CRP, PCT), radiology (chest X-ray), microbiology (blood cultures), consultations. Every loop inherits its context from the rail – **if the rail is wrong, every loop is addressed wrongly too.**

```include loop-en.svg
```

An order passes through the states *requested → accepted → in progress → preliminary → final*, plus the special states *cancelled* and *corrected*, which also have to be transmitted. Preliminary and corrected results are not exceptions but everyday routine – in microbiology, for example.

```quiz
question: "When is the order loop closed?"
options:
  - "When the LIS has technically sent the result to the HIS"
  - "When the result is stored in the HIS"
  - "When someone has seen the result and acted on it"
answer: "When someone has seen the result and acted on it"
explain: "The loop does not end with the technical transmission, but only with acknowledgement. Results that are not followed up (“test result follow-up”) are a well-known patient safety issue."
```

**Placer and filler:** the HIS as the ordering party (*placer*) assigns an order number (e.g. A-77812), the LIS as the performing party (*filler*) assigns its own lab or sample number (e.g. L-55301). Both numbers travel in every message – that is how the result finds its way back to its order. Two typical faults only show up if someone **actively monitors open orders**: *result without order* (e.g. a test added directly in the lab, an emergency sample without an electronic order) and *order without result* (sample never arrived, message lost, examination cancelled).

Warm-up: put the steps in the right order.

```match
question: "Order/result puzzle, laboratory: which step comes at which position?"
options: ["1", "2", "3", "4", "5", "6", "7"]
items:
  - item: "Technical validation"
    answer: "5"
  - item: "Order in the HIS"
    answer: "1"
  - item: "Sample receipt and barcode scan"
    answer: "3"
  - item: "Result visible in the HIS"
    answer: "7"
  - item: "Measurement on the analyser"
    answer: "4"
  - item: "Medical validation"
    answer: "6"
  - item: "Blood draw with label"
    answer: "2"
explain: "Technical validation comes before medical validation."
```

```match
question: "Order/result puzzle, radiology: which step comes at which position?"
options: ["1", "2", "3", "4", "5", "6", "7"]
items:
  - item: "Images to the PACS"
    answer: "5"
  - item: "Order in the HIS"
    answer: "1"
  - item: "Reading at the reporting workstation"
    answer: "6"
  - item: "Appointment and justification in the RIS"
    answer: "2"
  - item: "Report and image link in the HIS"
    answer: "7"
  - item: "Patient data to the modality via worklist"
    answer: "3"
  - item: "Examination on the CT"
    answer: "4"
explain: "Often forgotten: the justification of the exposure is made *before* the examination."
```

| | Order | Preparation | Execution | Review / reporting | Result |
|---|---|---|---|---|---|
| **Laboratory** | order in the HIS | label, blood draw, sample receipt | measurement | technical and medical validation | result in the HIS |
| **Radiology** | order in the HIS | appointment, justification, worklist | examination, images to the PACS | reading | report and image link in the HIS |

> **One shared information pattern – not two isolated systems.** Once you understand it, you also understand pathology, cardiology or consultations.

## 4 · The LIS in detail: from order to validated result

The LIS controls three phases. The actual measurement in the analyser is only the middle part:

| Pre-analytical | Analytical | Post-analytical |
|---|---|---|
| order, labelling, blood draw, transport, sample receipt | sample distribution, measurement on the analyser, quality control | technical and medical validation, result transmission, archiving |

```quiz
question: "In which phase did a study of an emergency laboratory find the largest share of confirmed laboratory errors?"
options: ["Pre-analytical", "Analytical", "Post-analytical"]
answer: "Pre-analytical"
explain: "Of 160 confirmed errors, 61.9 % were pre-analytical, 15.0 % analytical and 23.1 % post-analytical [@carraro2007]. Most errors do not happen in the analyser but at the hand-overs – identification, label, transport, transmission. That is exactly where information systems can help."
```

```case
One medical order, three speeds: the **blood gas analysis** runs as a point-of-care test directly in the ED (the device is connected to the LIS via POCT middleware). **Blood count, CRP, PCT and lactate** come from clinical chemistry and haematology. The **blood cultures** go to microbiology, often a separate subsystem – with a preliminary result (e.g. Gram stain for a positive culture) and only after days the final result with susceptibility testing.
```

```match
question: "Roughly when is each result available? (times are examples)"
options: ["after minutes", "after about 1 hour", "after several days, with a preliminary result"]
items:
  - item: "Blood gas analysis on the POCT device"
    answer: "after minutes"
  - item: "Blood count, CRP, PCT, lactate"
    answer: "after about 1 hour"
  - item: "Blood cultures in microbiology"
    answer: "after several days, with a preliminary result"
explain: "For the HIS this means several partial results, several subsystems, preliminary and final results – all for the same order and case. Exactly these late-arriving results become important in the failure scenario."
```

**The barcode as a bridge:** it links the physical sample to the digital order – scan the wristband, place the order in the HIS, print a label with order and sample number, stick it on at the bedside straight away; the analyser reads the barcode and fetches the order. Typical pre-analytical errors are swapped labels or wrong tubes, haemolysed samples or wrong material, samples that never arrive and wrong collection times (e.g. for drug levels). Labels printed “in advance” and kept in the ward office are a classic source of mix-ups.

In the laboratory a **middleware** often distributes the orders to the analysers and collects the measured values. Then come three levels of checking: (1) **technical validation** – is the device working, is quality control within range, is the measurement formally plausible? (2) **rule-based checks** – reference range, delta check (deviation from the previous value), plausibility across parameters; (3) **medical validation** – does the overall picture fit the patient? **Critical values** are additionally reported actively to the treating team, e.g. by phone; a message alone is not enough here.

```quiz
question: "The delta check compares a measured value with the previous value. What does it require?"
options:
  - "A particularly accurate analyser"
  - "A correct patient identity across all stays"
  - "A preliminary result"
answer: "A correct patient identity across all stays"
explain: "With a duplicate the delta check finds no previous value; with a mix-up it compares against another person's values. This is where the circle closes back to ADT."
```

The result goes back to the HIS as an HL7 v2 message `ORU^R01` (simplified; `OBR` = order, `OBX` = a single measured value):

```text
MSH|^~\&|LIS|LABOR|KIS|KLINIKUM|202610131512||ORU^R01|MSG0533|P|2.5
PID|1||4711^^^KLINIKUM^PI||Müller^Erika||19580312|F
OBR|1|A-77812|L-55301|ENTZ^Inflammation markers|||202610131420
OBX|1|NM|1988-5^CRP^LN||182|mg/L|<5|H|||F
OBX|2|NM|6690-2^Leukocytes^LN||15.8|10*3/uL|3.9-10.2|H|||F
```

```match
question: "What do the highlighted parts of the result message mean?"
options: ["Placer and filler number", "LOINC code: what exactly was measured", "Value, unit, reference range", "Flag: above the reference range", "Status: final"]
items:
  - item: "`A-77812|L-55301`"
    answer: "Placer and filler number"
  - item: "`1988-5^CRP^LN`"
    answer: "LOINC code: what exactly was measured"
  - item: "`182|mg/L|<5`"
    answer: "Value, unit, reference range"
  - item: "`H`"
    answer: "Flag: above the reference range"
  - item: "`F` at the end of the line"
    answer: "Status: final"
explain: "The LOINC code makes it internationally unambiguous what was measured – regardless of the local abbreviation: semantic interoperability. A preliminary microbiology result would have status P, a correction C. The flag H means “above the reference range”, but not automatically “critical”."
```

## 5 · RIS/PACS and DICOM: from imaging order to report with images

```timeline
title: "Mrs Müller's chest X-ray in seven steps"
events:
  - when: "1 · HIS"
    what: "Order: the physician requests a chest X-ray."
  - when: "2 · RIS"
    what: "Justification and appointment: radiology checks and schedules device and time."
  - when: "3 · RIS → modality"
    what: "Worklist: the patient data go to the device."
  - when: "4 · Modality"
    what: "Examination: X-ray or CT produces images."
  - when: "5 · PACS"
    what: "Store, archive and distribute images."
  - when: "6 · PACS + RIS"
    what: "Reading: view images, dictate the report."
  - when: "7 · HIS"
    what: "Report and image link in the clinical context."
```

**Justification of the exposure:** before every X-ray or CT examination, a physician with the required expertise determines that the benefit outweighs the radiation risk (in Germany, § 83 of the Radiation Protection Act, StrlSchG) – a process step that the RIS documents. Compared with the laboratory, radiology follows the same order/result pattern, but with images instead of measured values and two specialist systems.

```match
question: "RIS or PACS? Assign each task."
options: ["RIS", "PACS"]
items:
  - item: "Schedule appointments, devices and staff"
    answer: "RIS"
  - item: "Receive, store and archive images long-term"
    answer: "PACS"
  - item: "Provide worklists for the modalities"
    answer: "RIS"
  - item: "Viewer and comparison with priors"
    answer: "PACS"
  - item: "Report texts and sign-off"
    answer: "RIS"
  - item: "Distribute hundreds of CT images quickly to workstations"
    answer: "PACS"
explain: "RIS ≈ specialised order and workflow system (the world of text and process), PACS ≈ specialised data and archive system (the world of images). The link is the **accession number**: an examination number assigned by the RIS that reappears in every image."
```

**Modality worklist – no retyping at the CT:** the device asks the RIS for the scheduled examinations and takes over name, date of birth, patient ID, accession number and examination; these data then appear in every image (DICOM header), and the PACS assigns the images to the order via accession number and patient ID. Without a worklist, typing errors happen at the device – “Mueller” instead of “Müller”, a wrong ID – and images without an order (“orphaned”). It is the same principle as the barcode in the laboratory: capture once, then only pass on. IHE describes this workflow in the *Scheduled Workflow* profile.

**DICOM is more than an image format** (*Digital Imaging and Communications in Medicine*, since 1993, predecessor ACR-NEMA 1985): a **file format** with pixel data and metadata (patient, study, device, acquisition parameters), an **information model** with a fixed hierarchy, **network services** (storing with C-STORE, finding and fetching with query/retrieve, modality worklist) and a **conformance mechanism** (vendors' conformance statements). A JPEG of an X-ray image is almost worthless medically – it lacks exactly this context.

```match
question: "DICOM hierarchy patient → study → series → instance: at which level does this sit?"
options: ["Patient", "Study", "Series", "Instance"]
items:
  - item: "ID 4711 · Müller^Erika"
    answer: "Patient"
  - item: "Chest CT on Wednesday with accession number R-26-1231"
    answer: "Study"
  - item: "Lung kernel reconstruction with about 400 images"
    answer: "Series"
  - item: "a single image"
    answer: "Instance"
explain: "Every level has a globally unique UID. And every image carries its full context with it – including a wrong patient assignment."
```

```reflect
question: "Warm-up: Wednesday, 09:20 – at the CT, “Erika Möller” is selected from the worklist by mistake instead of “Erika Müller”. All 801 images are stored in the PACS without any technical fault, but under the wrong patient. Who notices – and when? What are the consequences for both patients? What needs to be corrected in which systems?"
intro: "Remember: **technically flawless does not mean clinically correct.** Points to expect:"
answers:
  - "It is often only noticed during reading (the findings do not match the order) – or not at all if Mrs Möller also had a chest order."
  - "Mrs Müller is missing a report, and her therapy is delayed."
  - "Mrs Möller has someone else's report in her record, future comparisons with priors will be wrong, and the radiation exposure is attributed to the wrong person."
  - "Corrections are needed in the PACS (reassign images, correct headers), in the RIS and in the HIS – and in copies already passed on (teleradiology, research platform, report CD). There are dedicated correction workflows for this, e.g. IHE Patient Information Reconciliation."
```

## 6 · Putting it together: one patient case, many systems and one fault

In the module [[therapy]] you saw that a therapy decision needs data from many sources. Here you see how those data actually flow:

```timeline
title: "Mrs Müller's first hours as a message flow (simplified)"
events:
  - when: "14:05"
    what: "Admission `ADT^A01` to LIS, RIS and PACS"
  - when: "14:12"
    what: "Lab order `OML^O21`"
  - when: "14:15"
    what: "X-ray order `ORM^O01` (newer: `OMG^O19`)"
  - when: "14:50"
    what: "Worklist to the modality (DICOM, direct)"
  - when: "15:05"
    what: "Images to the PACS (DICOM C-STORE, direct)"
  - when: "15:12"
    what: "Lab result `ORU^R01`"
  - when: "15:40"
    what: "X-ray report and image link `ORU^R01`"
  - when: "18:40"
    what: "Transfer `ADT^A02` to LIS, RIS and PACS"
```

The HL7 v2 messages run through the communication server; between RIS, modality and PACS, DICOM is usually spoken directly. That is eight messages for a few hours of a single patient – a large hospital processes hundreds of thousands a day. What if one of them does not arrive?

```case
**Failure scenario.** 18:40 – the transfer ED → intensive care unit is documented in the HIS, `ADT^A02` is generated. 18:41 – the A02 to the LIS gets stuck in the communication server's queue: the LIS interface is unreachable after an update. 19:30 – the blood culture is positive, Gram-negative rods. The LIS sends the result and triggers the phone notification – to the location it knows: “ED”.

No system made an “error”: HIS, LIS and communication server each work correctly – but with outdated context.
```

```reflect
question: "Think – pair – share: what could happen now? Who notices – and when? How could it have been prevented or caught?"
intro: "**Possible consequences:** the result lands in the ED work list or on the ED printer; the phone call reaches the ED, where Mrs Müller is no longer known; searching, call-backs, lost time; the antibiotic therapy is adjusted late; the ICU team only sees the result when actively searching the record. **Countermeasures:**"
answers:
  - "Monitoring of the communication server: queues, acknowledgements (ACK), alerts"
  - "Show results per patient, not only per location"
  - "Report critical values to the treating team and document the read-back"
  - "Resend messages and reconcile systems regularly"
  - "Clear responsibilities: who monitors the interfaces at night?"
```

This is the socio-technical triangle from [[history]] in its purest form: technology (queue, ACK, monitoring), process (reporting path for critical values) and organisation (who is responsible at night?) have to fit together – see also [@sittig2010]. And it connects to Hans Jonas: the greater the reach of technical systems, the greater the responsibility for their consequences.

> **Interfaces are not an IT detail but part of patient safety.**

```match
question: "Synthesis: interface, redundancy or failure risk?"
options: ["Interface", "Redundancy", "Failure risk"]
items:
  - item: "Analyser – middleware – LIS"
    answer: "Interface"
  - item: "Patient master data as copies in HIS, LIS, RIS and PACS"
    answer: "Redundancy"
  - item: "lost ADT events and the resulting outdated copies"
    answer: "Failure risk"
  - item: "RIS – modality – PACS"
    answer: "Interface"
  - item: "Results in both LIS and HIS"
    answer: "Redundancy"
  - item: "Direct connections without monitoring"
    answer: "Failure risk"
  - item: "Paper downtime procedures that nobody has practised"
    answer: "Failure risk"
explain: "Redundancy is not bad in itself – copies make systems fast and resilient – but every copy has to be kept in sync. Apply these three questions to every new patient case or every new system."
```

## Take-home messages

1. **Hospital IT is a system landscape.** All-in-one vs. best-of-breed and spaghetti vs. star are two independent questions.
2. **ADT provides the shared context.** Who? Which case? Where? – All other systems depend on it.
3. **Order/result is the shared pattern.** Laboratory and radiology follow the same loop – right up to acknowledgement.
4. **DICOM is more than an image format.** Data model, metadata and communication; the accession number links order and images.
5. **Integration is patient safety.** Identity, message flow and monitoring decide whether the right result arrives in time.

## Outlook: what we reuse in HL7 FHIR

Everything you have learned here conceptually reappears in FHIR as a resource – the concepts stay, only the technical form changes.

```match
question: "Which FHIR resource corresponds to the concept?"
options: ["Patient", "Encounter", "ServiceRequest", "Observation", "DiagnosticReport", "ImagingStudy"]
items:
  - item: "patient, patient ID"
    answer: "Patient"
  - item: "case, movement"
    answer: "Encounter"
  - item: "order"
    answer: "ServiceRequest"
  - item: "single measured value (OBX)"
    answer: "Observation"
  - item: "report"
    answer: "DiagnosticReport"
  - item: "DICOM study"
    answer: "ImagingStudy"
```

The coming weeks cover HL7 v2 in detail (segments, fields, acknowledgements), IHE profiles such as *Scheduled Workflow* and terminologies such as LOINC and SNOMED CT for semantic interoperability.

## Self-test

```quiz
question: "Why does almost every system need a current copy of the ADT context?"
options:
  - "Because the HIS has no database"
  - "Because assignment, previous values, result routing and billing depend on patient, case and location"
  - "Because HL7 v2 requires it"
answer: "Because assignment, previous values, result routing and billing depend on patient, case and location"
```

```quiz
question: "What links an order in the RIS to the images in the PACS?"
options: ["the patient ID alone", "the accession number", "the file name of the images"]
answer: "the accession number"
```

```quiz
question: "A best-of-breed landscape is …"
options:
  - "… always a spaghetti architecture"
  - "… not automatically spaghetti – it can be cleanly integrated via a communication server"
  - "… always more interoperable than an all-in-one suite"
answer: "… not automatically spaghetti – it can be cleanly integrated via a communication server"
```
