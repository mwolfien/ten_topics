---
title: "Specialised Clinical Systems – from the Workstation to the Biobank"
summary: "What happens inside specialised systems? We follow Mr Krause from the order via the tumour board, the operation and the first night in intensive care to the biobank – and analyse every system with the same five-question grid."
duration_minutes: 60
level: "In-depth"
audiences: [med, cs, clin, tech, pat]
order: 5
builds_on: [information-systems, therapy]
course: his
lecture: 3
author: "Markus Wolfien"
objectives:
  - "Explain the role of the clinical workstation and CPOE for orders and medication"
  - "Describe how a tumour board brings heterogeneous data together into a documented recommendation"
  - "Understand OR management as planning scarce, interdependent resources"
  - "Explain what is special about continuous data in the PDMS (devices, time series, alarms)"
  - "Explain how samples, consent and pseudonymisation connect care and research"
  - "Analyse any clinical information system with the five-question grid"
readings: [winter2023, bates1998, vandersijs2006, haynes2009, sendelbach2013]
related_topics: [ehr-cis, cdss, data-provenance, privacy-ethics, data-sharing, visualizations]
source: "Lecture 3 “Specialised Clinical Systems from the Workstation to the Biobank”, Health Information Systems (winter term 2026/27), Markus Wolfien, IMB & ZMI"
---

> **Guiding question:** How do specialised clinical systems support concrete work, decisions and therapy processes?

In the module [[information-systems]] you got to know a hospital's system landscape: how the HIS, LIS and RIS/PACS are connected through ADT, order/result and the communication server. We now take this infrastructure for granted and **zoom in**: what happens *inside* specialised systems – and how do they support the work with the patient?

```persona med
You will write orders, present cases at the tumour board and hand patients over to intensive care. This module shows which system takes on which work – and where it warns you, stops you or can mislead you.
```

```persona cs
Role-based permissions, rule engines, state machines, time series, pseudonymisation: specialised clinical systems are applied computer science. What makes them interesting is how these concepts have to work under time pressure with patient safety as a constraint.
```

```persona clin
Alert fatigue, alarm fatigue, missing results at the tumour board, no ICU bed: you know much of this from everyday work. Here you see which causes lie in the design of the systems – and what can be changed.
```

```persona tech
A device gateway that bypasses the communication server, a nightly export instead of a live connection, a trusted third party as a system of its own: the module shows why integration and operations decisions have direct clinical consequences.
```

```persona pat
Why is your wristband scanned before every dose of medication? Who decides about your treatment at the tumour board? And what happens to tissue you donate for research? This module gives answers – including on your right to withdraw consent.
```

```case
**Mr Peter Krause, 62 years** (born 14 May 1964) – the patient from the module [[therapy]]. He has smoked for over 25 years (about 30 pack-years); the low-dose CT of the lung cancer screening shows a **2.6 cm nodule in the right upper lobe**. Previous conditions: atrial fibrillation, type 2 diabetes, hypertension. Long-term medication: **apixaban**, metformin, ramipril.

The case is fictional and medically simplified. We are interested in which system manages which part of his data.
```

```timeline
title: "Mr Krause's path through the systems"
events:
  - when: "Week 2"
    what: "Inpatient work-up: bronchoscopy and biopsy – **workstation & CPOE**"
  - when: "Week 3"
    what: "Histology: adenocarcinoma · staging cT1c cN0 cM0"
  - when: "Week 4"
    what: "Thoracic tumour board recommends a lobectomy – **tumour board**"
  - when: "Week 5"
    what: "Minimally invasive right upper lobectomy (VATS) – **OR management**"
  - when: "Week 5"
    what: "First night in intensive care – **PDMS**"
  - when: "Week 5"
    what: "Tumour tissue goes to the biobank with consent – **biobank**"
```

### The tool: the five-question grid

Instead of memorising systems, we ask every system the same five questions. Once you master the grid, you can also analyse systems that do not appear here – such as pathology, emergency department or nursing systems.

| | Question |
|---|---|
| **USER** | Who works with the system, and in which role? |
| **DATA** | Which data are created, which are needed? |
| **WORKFLOW** | Which workflow does the system support? |
| **INTERFACES** | Which systems does it have to exchange data with? |
| **RISK** | What can go wrong – and with what consequences? |

## 1 · Clinical workstation & CPOE: from decision to order

For its users, “the HIS” is not a box in an architecture diagram but a **workstation**. The same record looks different depending on the role:

| Role | mainly sees and edits |
|---|---|
| Physician | results, orders, progress, discharge letter |
| Nursing | chart, interventions, vital signs, care planning |
| Pharmacy | medication review, interactions, unit dose |
| Ward manager | bed occupancy, staff, open tasks |

Roles also determine **permissions**: who may order, who may sign off? Technically this is **role-based access control** (RBAC): permissions are attached not to people but to roles, and people are given roles. The header with name, date of birth and ward is the ADT context from the last lecture – visible on every screen so that nobody works in the wrong record. More on this in the topic [[topic:ehr-cis]].

**CPOE** (*computerized physician order entry*) means that the physician enters orders directly and **in structured form** in the system – not on paper and not verbally to a nurse who then types them in. An order is an object with fields: *what, for whom, when, how urgent, why*. That is why the system can check it before the order goes to the performing department; what happens next is the order/result pattern from [[information-systems]].

```case
Mr Krause's orders on the day of admission: **bronchoscopy with EBUS biopsy** (urgent, question: histology of the right nodule) · **lung function** incl. diffusion before possible resection · **lab**: blood count, coagulation, creatinine before the procedure · **pause apixaban** 48 h before the biopsy (according to the local SOP).
```

```quiz
question: "By how much did non-intercepted serious medication errors fall after CPOE was introduced in the classic study?"
options: ["by about 15 %", "by about 55 %", "by about 95 %", "not at all – only documentation became faster"]
answer: "by about 55 %"
explain: "From 10.7 to 4.86 per 1,000 patient-days [@bates1998]. CPOE works mainly through **structure and checks**, not through typing as such."
```

### Medication as a closed loop

Medication is the most important use case for CPOE. The loop is only closed if all steps are digitally linked **through the same IDs** – the same logic as the barcode in the laboratory. Every media break (copying, converting, preparing doses by hand) is a source of error. At administration, nurses check the **five rights**: right patient, right drug, right dose, right route, right time – scanning the wristband and the drug supports them technically. In Germany, digital medication management was funded, among other things, through the Hospital Future Act (KHZG).

```include medication-loop-en.svg
```

### Decision support and its downside

Structured orders make decision support possible ([[topic:cdss]]): **notes**, **warnings** and **hard stops**. For Mr Krause, for example: biopsy planned in two days – pause apixaban? Contrast CT ordered – check kidney function under metformin. A second anticoagulant selected – duplicate prescription.

```quiz
question: "According to a review, in how many cases are drug safety alerts in CPOE overridden?"
options: ["in 5–10 %", "in 20–30 %", "in 49–96 %"]
answer: "in 49–96 %"
shuffle: false  # options in a natural order
explain: "According to the review by van der Sijs et al. [@vandersijs2006] – often rightly so, because the warning was unspecific. A system that warns all the time is ignored – even when it happens to be right. That is **alert fatigue**."
```

Good alerts are **specific** to this patient, **actionable** (what should I do?), come **at the right moment** in the workflow and are **graded by severity**.

```match
question: "Warm-up: stop, note or no alert at all?"
options: ["Stop", "Note", "No alert"]
items:
  - item: "Penicillin allergy with anaphylaxis documented – amoxicillin (a penicillin derivative) is prescribed."
    answer: "Stop"
  - item: "Paracetamol with a prescribed daily dose of 8 g"
    answer: "Stop"
  - item: "Ramipril prescription, current potassium 5.3 mmol/l (slightly raised)"
    answer: "Note"
  - item: "“Mind kidney function” on every metformin prescription – the eGFR is normal."
    answer: "No alert"
explain: "The allergy and twice the maximum daily dose (a typical input error, e.g. single and daily dose confused) call for a stop, possibly with a documented reason. The potassium is clinically relevant, but the physician weighs it up. A permanent warning with normal kidney function is noise and trains people to click it away. **The art is to avoid case 4 so that case 1 is noticed.**"
```

```match
question: "Grid for workstation & CPOE: which question does the answer belong to?"
options: ["USER", "DATA", "WORKFLOW", "INTERFACES", "RISK"]
items:
  - item: "Physicians, nurses, pharmacy, ward manager – with different views and permissions"
    answer: "USER"
  - item: "Orders, medication, allergies, lab values, knowledge base for interactions"
    answer: "DATA"
  - item: "Decision → prescription → review → dispensing → administration → monitoring"
    answer: "WORKFLOW"
  - item: "HIS/ADT, LIS, RIS, pharmacy system, performing departments (order/result)"
    answer: "INTERFACES"
  - item: "Alert fatigue, wrong selection in a dropdown, copy & paste, workarounds when usability is poor"
    answer: "RISK"
explain: "Poor usability – long click paths, mandatory fields, floods of alerts – leads to workarounds such as notes on paper or batch entries."
```

## 2 · Tumour documentation & tumour board: many sources, one recommendation

The biopsy shows an **adenocarcinoma**. Now an interdisciplinary therapy decision is needed. The **tumour board** brings together all disciplines that contribute – for Mr Krause pulmonology, thoracic surgery, oncology, radiotherapy, radiology, nuclear medicine and pathology. In cancer centres certified by the German Cancer Society, presenting certain cases is mandatory; the molecular tumour board from [[therapy]] is a special form. What matters for informatics: **the result is not a conversation but a documented recommendation.**

```timeline
title: "The tumour board workflow"
events:
  - when: "1 · Registration"
    what: "Case, question, deadline – a form with mandatory fields"
  - when: "2 · Preparation"
    what: "Bring data together, preload images, check results"
  - when: "3 · Discussion"
    what: "Case view, image demonstration, video if needed – often only a few minutes per case"
  - when: "4 · Recommendation"
    what: "Structured minutes, sign-off by the chair"
  - when: "5 · Implementation"
    what: "Tasks, appointments, discharge letter, checking implementation – and re-presentation if needed"
```

Most of the work happens **before and after** the discussion: searching for data, implementing recommendations, keeping track of re-presentations.

```match
question: "Mr Krause's case on one screen: which system does the information come from?"
options: ["HIS", "PACS", "Pathology system", "Molecular pathology", "Function diagnostics", "LIS", "Conversation note"]
items:
  - item: "Clinical findings, smoking status, performance status ECOG 0"
    answer: "HIS"
  - item: "Low-dose CT and PET-CT"
    answer: "PACS"
  - item: "Histology: adenocarcinoma"
    answer: "Pathology system"
  - item: "EGFR, ALK, PD-L1"
    answer: "Molecular pathology"
  - item: "Lung function: FEV1 78 %"
    answer: "Function diagnostics"
  - item: "Blood count, coagulation, creatinine"
    answer: "LIS"
  - item: "Wish: “operate if possible”"
    answer: "Conversation note"
explain: "At least seven sources – in many hospitals still gathered by hand as PDFs, free text or screenshots. The tumour board is an **integration problem in its purest form**, and the case view a question of good [[topic:visualizations]]."
```

### The timeline – and which state is visible

Therapy decisions are based on **courses over time**, not on single results. A timeline places events from very different systems on one time axis:

```timeline
title: "Mr Krause's course from seven systems"
events:
  - when: "Week 0"
    what: "Low-dose CT: nodule (PACS)"
  - when: "Week 2"
    what: "Admission to pulmonology (HIS); bronchoscopy and EBUS biopsy (endoscopy); histology: adenocarcinoma (pathology)"
  - when: "Week 3"
    what: "PET-CT: cN0 cM0 (PACS); lung function FEV1 78 % (function diagnostics)"
  - when: "Week 4 · Mon 18:00"
    what: "**Export of the case view** for the tumour board"
  - when: "Week 4 · Tue 11:00"
    what: "Molecular result released (molecular pathology)"
  - when: "Week 4 · Tue 14:00"
    what: "Tumour board (tumour documentation)"
```

```quiz
question: "What stands out in this timeline?"
options:
  - "The PET-CT came too late for the tumour board."
  - "The molecular result was released after the case view's data cut-off, but before the board."
  - "The lung function is missing from the case view."
answer: "The molecular result was released after the case view's data cut-off, but before the board."
explain: "The result is in the pathology system but not in the case view. In clinical systems, time is not only an axis but also a question: **which state is currently visible?** A good case view therefore shows its data cut-off."
```

### Tumour documentation: record once, use many times

Tumour documentation is specialised, highly structured documentation:

| Field | for Mr Krause |
|---|---|
| Diagnosis | ICD-10-GM C34.1 · upper lobe (bronchus) |
| Morphology | ICD-O-3 8140/3 · adenocarcinoma |
| Clinical TNM | cT1c cN0 cM0 (UICC, 9th edition) |
| Stage | UICC IA3 |
| Performance status | ECOG 0 |
| Tumour board | date, recommendation, guideline reference |

Classifications are **versioned**: since 1 January 2026 the UICC has recommended the 9th edition of the TNM classification. Nothing changes for Mr Krause, but the version has to be documented.

```match
question: "Who uses the same tumour data, and for what?"
options: ["Treatment", "Clinical cancer registry", "Centre certification", "Research"]
items:
  - item: "Discharge letter, therapy planning, follow-up care"
    answer: "Treatment"
  - item: "Mandatory reporting under § 65c of the German Social Code (SGB V) in the uniform oncological basic data set (oBDS)"
    answer: "Clinical cancer registry"
  - item: "Key figures and quality indicators"
    answer: "Centre certification"
  - item: "Cohorts, registries, study recruitment"
    answer: "Research"
explain: "Without structured recording, the same information sits in the HIS, the tumour documentation, the registry report, the centre's form and the study CRF – **multiple documentation**. The goal: record once in structured form, use many times."
```

### The recommendation – and where it comes from

```case
**Thoracic tumour board · week 4, Tue 14:00.** *Recommendation:* anatomical right upper lobectomy (VATS) with systematic lymph node dissection. *Reasoning:* cT1c cN0 cM0, UICC IA3, functionally operable (FEV1 78 %, ECOG 0). *Guideline:* German S3 guideline on lung cancer, compliant. *Next:* re-presentation after surgery with pTNM and molecular result. *Data basis:* case view, as of Mon 18:00 – **molecular result not considered**. *Sign-off:* chair, Tue 15:10, 7 disciplines present.
```

**Provenance** means a record of origin ([[topic:data-provenance]]). You can ask five questions of every recommendation: who recommended it? On which data basis? Following which guideline – or deliberately deviating? Which information was missing? Was the recommendation implemented? **Without its data basis, a recommendation cannot be traced** – for liability, quality assurance and research.

```reflect
question: "Warm-up: Tue 14:20 – Mr Krause is being discussed. A pathologist mentions: “The molecular result has been released since this morning.” It is missing from the case view. (A) Give the recommendation without the molecular result, (B) postpone the case to next week, or (C) open the result live, include it and document the data state? And how do you prevent this from happening again?"
intro: "Usually **C** – or A with a documented re-presentation: for the surgery decision at an early stage the molecular result is probably not decisive, but it is for possible perioperative or adjuvant systemic therapy. To prevent it from happening again:"
answers:
  - "**System:** a live connection instead of a nightly export; an event “new result released” sent to the tumour board list; a visible data cut-off in the case view"
  - "**Process:** a checklist of “pending results” at registration"
  - "**Organisation:** registration deadlines and clear responsibility for preparation"
  - "Key message: **an outdated data state is a typical risk of every combined view.**"
```

## 3 · OR management: a resource puzzle

The recommendation is a lobectomy. An operation only takes place if **all resources are available at the same time**: operating room, thoracic surgery, anaesthesia, OR nursing, instruments and sterile supplies (VATS tower, trays), blood products, an ICU bed for afterwards – and a prepared patient. For Mr Krause, “patient ready” means: informed and consented, fasting, **apixaban paused in time**, lab and blood group up to date, surgical site marked. This is where the circle closes back to CPOE: without the medication order from earlier, the operation would be dangerous or cancelled.

The OR schedule shows the rooms on a time axis; planning is always **re-planning**, for example when an emergency is squeezed in. The status board shows where each case stands. Technically this is a **state model**: *planned → prepared → checked in → in surgery → finished → transferred*. Events trigger the transitions, each creates a timestamp – and can trigger a message to other systems.

```match
question: "Which state is reached after the event?"
options: ["prepared", "checked in", "in surgery", "finished", "transferred"]
items:
  - item: "Consent signed, fasting, apixaban paused, site marked"
    answer: "prepared"
  - item: "07:05 – Mr Krause arrives in the OR area"
    answer: "checked in"
  - item: "07:58 – incision"
    answer: "in surgery"
  - item: "10:31 – closure"
    answer: "finished"
  - item: "11:15 – handover to the ICU"
    answer: "transferred"
explain: "The timestamps yield incision-to-closure time, changeover times, room utilisation, the operation report and the OPS procedure codes for billing. Clinical workflows are very often modelled as state models."
```

### Safety as a workflow: the WHO checklist

The WHO Surgical Safety Checklist structures three moments. Digitally, the checkpoints become **mandatory steps** in the OR system, with timestamp and name – the next state can only be reached once the checkpoint has been documented.

```match
question: "When is the item checked?"
options: ["Sign in – before anaesthesia", "Team time out – before incision", "Sign out – before leaving the OR"]
items:
  - item: "Identity, procedure and site confirmed; consent available"
    answer: "Sign in – before anaesthesia"
  - item: "Allergies, airway, expected blood loss"
    answer: "Sign in – before anaesthesia"
  - item: "The team introduces itself; patient, procedure and site are confirmed out loud"
    answer: "Team time out – before incision"
  - item: "Anticipated critical events are discussed"
    answer: "Team time out – before incision"
  - item: "Instruments and swabs counted"
    answer: "Sign out – before leaving the OR"
  - item: "Specimens labelled correctly"
    answer: "Sign out – before leaving the OR"
explain: "The last item leads directly to pathology – and later to the biobank."
```

```quiz
question: "What did the study in eight hospitals show after the checklist was introduced?"
options:
  - "no measurable effect"
  - "fewer complications, but no lower mortality"
  - "mortality fell from 1.5 % to 0.8 % and complications from 11.0 % to 7.0 %"
answer: "mortality fell from 1.5 % to 0.8 % and complications from 11.0 % to 7.0 %"
explain: "7,688 patients in eight hospitals worldwide [@haynes2009]. But beware: a ticked box is not the same as a time out that is actually lived – a socio-technical issue."
```

```reflect
question: "Warm-up: Thu, 06:45 – the ICU reports: “We have no ICU bed before 2 pm.” Mr Krause has been fasting since 10 pm, apixaban has been paused for two days, OR 3 is scheduled for him from 07:30. What happens now with him and OR 3? Who needs to be informed – through which system? What could the system have made visible earlier?"
answers:
  - "**Options:** swap the order in OR 3 (bring forward a mediastinoscopy that needs no ICU bed); move Mr Krause to the afternoon – then clarify fasting and the anticoagulation pause; check an intermediate care bed instead of ICU; in the worst case, cancel."
  - "**Inform:** OR coordination, anaesthesia, the ward, the patient, the ICU, possibly the blood bank."
  - "**System:** the OR system should know the ICU bed occupancy – ideally with a warning the day before: “post-operative ICU bed not secured”. In many hospitals this interface between OR planning and bed management exists only by phone."
```

## 4 · PDMS in intensive care: when data are created continuously

Mr Krause arrives in the ICU at 11:15 – and the nature of the data changes fundamentally.

```quiz
question: "On a normal ward, vital signs are recorded about three times a day. How many measurements per parameter and day are created in intensive care if the monitor delivers one value per second?"
options: ["24", "1,440", "86,400", "over 1 million"]
answer: "86,400"
shuffle: false  # options in a natural order
explain: "24 × 60 × 60 = 86,400. A PDMS typically stores condensed values, e.g. one per minute, and displays them as a **chart**."
```

The **PDMS** (patient data management system) takes over device data automatically, shows everything on one time axis, manages orders and infusion pumps, calculates fluid balances and scores, and documents nursing and ward rounds. Scores such as SAPS II and TISS also feed into the billing of intensive care (OPS 8-980 in Germany).

**Device integration:** monitor, ventilator, syringe pumps and blood gas analysis usually do not talk to the PDMS directly but through a **device gateway** – historically vendor-specific, often HL7 v2, increasingly the open standard ISO/IEEE 11073 SDC. Sound familiar? It is the **direct connection bypassing the communication server** from [[information-systems]]. And: **a measured value is not the same as a documented value.** In many hospitals, nurses actively accept values and discard artefacts – responsibility stays with people.

```timeline
title: "Mr Krause's first night in the chart"
events:
  - when: "02:10"
    what: "Alarm: heart rate above 130/min, blood pressure falling"
  - when: "02:15"
    what: "Physician at the bedside, ECG: atrial fibrillation – common after lung resections, and Mr Krause has a history"
  - when: "02:25"
    what: "Medication ordered and given in the PDMS"
  - when: "03:40"
    what: "Heart rate back to normal"
```

The chart connects **measurements, orders and actions** over time – that is its real value. It is the same medication loop as in CPOE, only in minutes instead of days.

### Alarms: between safety and alarm fatigue

```quiz
question: "According to a review, what share of clinical alarms are false alarms?"
options: ["5–10 %", "25–40 %", "72–99 %"]
answer: "72–99 %"
shuffle: false  # options in a natural order
explain: "According to Sendelbach and Funk [@sendelbach2013]. The consequence is **alarm fatigue**: desensitisation, so that real alarms are missed or noticed too late – like alert fatigue in CPOE, only audible and around the clock."
```

```match
question: "Warm-up: which value is real? Raise an alarm and accept it into the record?"
options: ["Artefact – check, do not accept", "Real – act and document"]
items:
  - item: "SpO₂ drops briefly – 14:06, the nurse repositions Mr Krause"
    answer: "Artefact – check, do not accept"
  - item: "Mean arterial pressure first 8, then 250 mmHg – 14:07, blood sample taken from the arterial line, then flushed"
    answer: "Artefact – check, do not accept"
  - item: "Persistently high heart rate – no manipulation, patient awake, feels palpitations"
    answer: "Real – act and document"
explain: "Whether a value is real depends on the **context** – and that is not in the measurement itself. That is why nurses validate values, and why alarms without context are so often wrong. The third case is a second episode of Mr Krause's atrial fibrillation. More on when data can be relied on in the topic [[topic:data-quality]]."
```

Countermeasures are partly technical, partly organisational: **individual limits** per patient instead of factory settings, **delay and prioritisation** (wait out brief outliers, distinguish severity levels), **targeted routing** to the responsible nurse instead of everyone, and **“smart alarms”** that combine several parameters. The goal is not “fewer alarms” but **the right alarms for the right person**.

```match
question: "Grid for the PDMS: which question does the answer belong to?"
options: ["USER", "DATA", "WORKFLOW", "INTERFACES", "RISK"]
items:
  - item: "ICU nurses, intensivists, physiotherapy, pharmacy – around the clock"
    answer: "USER"
  - item: "Time series of vital signs, ventilation, infusion pumps, fluid balances, scores"
    answer: "DATA"
  - item: "Measure → validate → assess → act → document, in minutes instead of days"
    answer: "WORKFLOW"
  - item: "Medical devices via gateway, HIS/ADT, LIS (blood gas analysis), pharmacy, billing"
    answer: "INTERFACES"
  - item: "Alarm fatigue, artefacts recorded as measurements, gateway failure, data flood"
    answer: "RISK"
```

## 5 · Biobank: from care to research

While Mr Krause is in intensive care, his tumour tissue has long been on its way.

```timeline
title: "The sample's path"
events:
  - when: "09:42 · OR"
    what: "Specimen removed"
  - when: "09:58 · Pathology"
    what: "Diagnostics come first: pathology decides which material is needed for the diagnosis; only surplus material goes to the biobank."
  - when: "10:15 · Processing"
    what: "Tumour, normal tissue, plasma – frozen"
  - when: "10:30 · Biobank IS"
    what: "Sample ID, aliquots, storage location (e.g. −80 °C or vapour phase over liquid nitrogen)"
  - when: "later"
    what: "Release after an approved application"
```

```quiz
question: "How long was the cold ischaemia time of Mr Krause's tumour tissue (from removal to freezing)?"
options: ["16 min", "33 min", "48 min", "73 min"]
answer: "33 min"
shuffle: false  # options in a natural order
explain: "09:42 → 10:15. The time is documented with the sample because it affects whether RNA or proteins can later be measured reliably – **pre-analytics matter**, just as in the laboratory."
```

For material from care to become a research resource, two things are needed ([[topic:privacy-ethics]]):

1. **Consent:** university hospitals increasingly use the **broad consent of the Medical Informatics Initiative** (MII) – a nationally harmonised template for using data and samples in future research that is not yet specified, revocable at any time.
2. **Pseudonymisation via a trusted third party:** the hospital knows the identity; the link to the pseudonym and the consent status are managed separately by the trusted third party; the biobank and researchers work with pseudonymised data. The architecture differs locally – the principle of separation is the same everywhere.

```include trust-center-en.svg
```

```match
question: "Who knows what?"
options: ["Hospital", "Trusted third party", "Biobank & research"]
items:
  - item: "Name and date of birth together with patient ID 4711-K"
    answer: "Hospital"
  - item: "The link 4711-K ↔ PSN-7Q2K-91XD and the consent status"
    answer: "Trusted third party"
  - item: "Samples and clinical data under PSN-7Q2K-91XD"
    answer: "Biobank & research"
explain: "So the trusted third party is an information system too – with a very particular USER and a very particular RISK."
```

**No research without clinical context:** a sample is scientifically only worth as much as its context – otherwise it is just frozen tissue. This includes the final stage (pT1c pN0 (0/18) R0, from the tumour documentation), histology and molecular result (pathology), smoking status and previous conditions (HIS), therapy and course as well as follow-up, recurrence and survival (cancer registry). These data are linked via the pseudonym: in the MII, **data integration centres** bring them together in standardised form, researchers apply via the **German Portal for Medical Research Data** (Forschungsdatenportal für Gesundheit) and, after review, receive pseudonymised data and samples (see [[topic:data-sharing]]). Provenance tracks every sample from collection to use: *who did what with the sample, when – and under which consent?* It is the same question as at the tumour board.

```reflect
question: "Warm-up: two years later, Mr Krause withdraws his consent. His samples are stored in the biobank, his data have been used in two projects, one of which is published. Where are his samples and data? What has to happen now – in which system? What can no longer be undone?"
intro: "Remember: **consent is a status that can change – not a form that is filed once.**"
answers:
  - "**Where:** samples in the biobank information system (storage location, aliquots, possibly already released to projects), data in the data integration centre and in the project data sets, the consent status at the trusted third party."
  - "**What has to happen:** change the status at the trusted third party, pass the event on to the biobank and the data integration centre, destroy the samples or – depending on the consent and the law – anonymise them, delete or block the data."
  - "**Cannot be undone:** results of analyses already completed and publications."
  - "Withdrawal is an event that has to travel through several systems – like an ADT message. And what happens if this message gets stuck in a queue? (See the exercise [[his-exercise]].)"
```

## Synthesis: one grid, five systems

| | Workstation & CPOE | Tumour board | OR management | PDMS | Biobank |
|---|---|---|---|---|---|
| **USER** | physicians, nurses, pharmacy | interdisciplinary board | OR team, coordination | ICU nurses and physicians | pathology, researchers, patient |
| **DATA** | orders, medication | results from 7+ sources, TNM | schedule, resources, timestamps | time series, alarms, scores | samples, consent, pseudonyms |
| **WORKFLOW** | prescribe → review → give | register → discuss → recommend | plan → operate → re-plan | measure → validate → act | consent → store → release |
| **INTERFACES** | LIS, RIS, pharmacy | PACS, pathology, cancer registry | beds, blood bank, pathology | medical devices, LIS | trusted third party, DIC |
| **RISK** | alert fatigue | outdated data state | resource conflict | alarm fatigue, artefacts | withdrawal, re-identification |

```match
question: "Which system does the typical risk belong to?"
options: ["Workstation & CPOE", "Tumour board", "OR management", "PDMS", "Biobank"]
items:
  - item: "Warnings are clicked away by reflex"
    answer: "Workstation & CPOE"
  - item: "The case view shows the state of last night"
    answer: "Tumour board"
  - item: "Room, team and patient are ready – the ICU bed is missing"
    answer: "OR management"
  - item: "A flushing manoeuvre ends up in the record as a blood pressure of 250 mmHg"
    answer: "PDMS"
  - item: "A withdrawal of consent does not reach every system"
    answer: "Biobank"
```

Read the table row by row: the systems are very different, but they share **basic patterns**. All need the **patient context** from ADT. All work with **time** – as the time of an order, a data cut-off, a timestamp, a time series or a date of consent. All represent **status**. All need **provenance**. And every INTERFACES row lists different systems.

## Take-home messages

1. **Specialised systems support work – not just data storage.** Roles, views, rules and status shape how clinical work is done.
2. **CPOE makes orders structured and therefore checkable.** Good decision support is specific – otherwise alert fatigue sets in.
3. **Therapy decisions need integrated data** – with a visible data state and traceable origin (provenance).
4. **Time is the central dimension** – as an OR schedule and timestamps, or as a continuous time series in the PDMS.
5. **Care becomes research only with consent, pseudonym and context.** The five-question grid works for each of these systems – and for every new one.

## Outlook: from specialised systems to standards

This module was about **what** the systems have to do; the next lecture is about **how** we get them to talk to each other: HL7 v2 (ADT, ORU), CDA for structured documents such as the discharge letter, DICOM, IHE profiles, xDT in outpatient care and the communication patterns push, pull and publish–subscribe. The topic [[topic:fhir]] offers an outlook on the modern standard.

## Self-test

```quiz
question: "Why can CPOE check an order, but a paper order cannot be checked?"
options:
  - "Because it is written faster"
  - "Because it exists as a structured object with fields (what, for whom, when, how urgent, why)"
  - "Because the pharmacy sees it earlier"
answer: "Because it exists as a structured object with fields (what, for whom, when, how urgent, why)"
```

```quiz
question: "What must a traceable tumour board recommendation always include?"
options: ["the data basis with its cut-off", "the number of participants", "the length of the discussion"]
answer: "the data basis with its cut-off"
```

```quiz
question: "What makes a biobank sample scientifically valuable?"
options:
  - "as much tissue as possible"
  - "consent, pseudonym, pre-analytical data and clinical context"
  - "storage for as long as possible"
answer: "consent, pseudonym, pre-analytical data and clinical context"
```

```reflect
question: "Transfer: apply the five-question grid to a system that did not appear here – such as an emergency department, pathology or nursing documentation system – and compare it with the synthesis table."
answers:
  - "Example **emergency department system** – USER: triage nurses, ED physicians, ambulance handover; DATA: triage level, vital signs, waiting times, provisional identity; WORKFLOW: arrival → triage → treatment → disposition (admission or discharge); INTERFACES: HIS/ADT, LIS, RIS, bed management, ambulance service; RISK: unknown identity, overcrowding, patients “disappearing” in the waiting area."
  - "Shared with the five systems: patient context, time (waiting times), status (triage level, treatment stage) and provenance."
```
