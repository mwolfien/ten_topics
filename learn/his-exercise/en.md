---
title: "Exercise: When Systems Disagree"
summary: "Self-paced transfer exercise for the lecture on HIS, LIS and RIS/PACS: an unknown emergency patient is identified later – and not every system follows. You analyse the system landscape, ADT, orders & results and an interface problem."
duration_minutes: 90
level: "Exercise · transfer"
audiences: [med, cs, clin, tech]
order: 4
builds_on: [information-systems]
course: his
lecture: 2
kind: exercise
author: "Eveline Prochaska, Markus Wolfien"
objectives:
  - "Reconstruct a system landscape from a clinical case"
  - "Assess all-in-one/best-of-breed and star/spaghetti independently of each other"
  - "Identify the relevant ADT events and care contexts"
  - "Trace order/result flows between the HIS and diagnostic subsystems"
  - "Analyse how an interface failure affects several systems"
  - "Derive technical and organisational countermeasures"
readings: [winter2023, sittig2010]
related_topics: [ehr-cis, data-quality, fhir]
source: "Exercise for lecture 2 “HIS, LIS and RIS/PACS – How Clinical Information Systems Work Together”, Health Information Systems (winter term 2026/27), Eveline Prochaska and Markus Wolfien, IMB & ZMI"
---

> **What this is about:** In the lecture and in the module [[information-systems]] you followed Mrs Müller through the system landscape. Here you apply the same concepts to a **new case** – with a different problem: no transfer gets lost; instead **the patient's identity changes, and not every system follows.**

## How to work through this exercise

- Work alone or in pairs. Allow about **90 minutes**; you can stop at any time.
- For the **open tasks** (✏️), write your own answer first. Only then can you open the solution notes. Then compare: what did you have, what was missing, where do you see it differently?
- The **choice tasks** (❓) give immediate feedback.
- Your answers are saved **only in your browser**. At the end you can download them, e.g. to discuss them in your tutorial group.
- For task 2.2 you need pen and paper (or a drawing tool).

| Part | Content | Time |
|---|---|---:|
| 1 | Identify the systems | 10 min |
| 2 | Analyse the architecture | 15 min |
| 3 | ADT and identity | 15 min |
| 4 | Orders & results | 15 min |
| 5 | Analyse an interface failure | 20 min |
| 6 | Improve the architecture | 15 min |
| | **Total** | **90 min** |

## The case

```case
**Tuesday, 14:05.** A man of about 35 is brought to the emergency department (ED) with reduced consciousness after a bicycle accident. He has no identity documents with him, and no relatives can be reached.

A **provisional identity** is therefore created at admission:

- **Patient:** “Unknown, male”, estimated date of birth 1 January 1991
- **temporary patient ID:** 99127
- **Case:** F2026-1048

The first 90 minutes bring: admission in the ED, blood count, coagulation and blood group typing, a CT of head and chest, surgery and then transfer to the intensive care unit.

Systems involved include: **HIS – communication server – LIS – blood bank – RIS – PACS – OR system – PDMS.**

**At 20:00** the patient is identified as **Max Berger**. He has been treated in the hospital before and therefore already has a patient ID: **34821**. The two identities have to be merged.
```

## Part 1 · Which systems are involved? (10 min)

```match
question: "Task 1.1: What is the system's main function in this case?"
options:
  - "Admission, case creation, orders, documentation"
  - "Measure and report blood count and coagulation"
  - "Type the blood group, provide blood products"
  - "Schedule the CT, provide the worklist, report text"
  - "Store, archive and display CT images"
  - "Plan and document the operation"
  - "Vital signs and therapy in intensive care"
  - "Distribute and translate messages between systems"
items:
  - item: "HIS"
    answer: "Admission, case creation, orders, documentation"
  - item: "LIS"
    answer: "Measure and report blood count and coagulation"
  - item: "Blood bank"
    answer: "Type the blood group, provide blood products"
  - item: "RIS"
    answer: "Schedule the CT, provide the worklist, report text"
  - item: "PACS"
    answer: "Store, archive and display CT images"
  - item: "OR system"
    answer: "Plan and document the operation"
  - item: "PDMS"
    answer: "Vital signs and therapy in intensive care"
  - item: "Communication server"
    answer: "Distribute and translate messages between systems"
explain: "Eight systems in 90 minutes – and all of them work with the same patient."
```

```reflect
question: "**Task 1.2:** Which systems need information on (a) patient identity, (b) the case and (c) the current location? Give brief reasons."
intro: "A possible answer:"
answers:
  - "**Identity:** practically all of them – LIS, blood bank, RIS, PACS, OR system and PDMS must assign samples, images, blood products and measurements unambiguously to the right person. For the blood bank this is especially critical (mix-up → transfusion incident)."
  - "**Case:** the HIS and billing (services, DRG), but also LIS, RIS, OR system and PDMS, because services and documentation are assigned to case F2026-1048."
  - "**Location:** LIS and blood bank (delivering results and blood products, reporting critical values), RIS (fetching the patient for the CT, result routing), OR system (hand-over), PDMS (ICU bed list)."
```

```reflect
question: "**Transfer question:** Why is it not enough for only the HIS to know the correct patient data?"
answers:
  - "The subsystems do not ask the HIS for every action. They keep **their own copy** of the ADT context and work with it – even if the HIS is briefly unavailable."
  - "Samples, images and blood products carry the identity **with them** (barcode, DICOM header, label). If the identity changes only in the HIS, these data remain wrongly labelled."
  - "That is why every change has to reach all systems as an event – and be processed correctly there."
```

## Part 2 · Architecture of the system landscape (15 min)

You receive simplified information about the hospital's landscape:

- Admission, documentation, order entry and billing come from an **HIS suite by vendor A**.
- LIS, blood bank, RIS, PACS, PDMS and OR system come from **different vendors**.
- HIS, LIS, blood bank, RIS, PDMS and OR system communicate mostly via a **communication server**.
- RIS and PACS have a **direct connection**.
- The PDMS communicates **directly** with the monitoring devices.

```quiz
question: "Task 2.1a: How do you classify the landscape at the application level?"
options:
  - "All-in-one"
  - "Best-of-breed"
  - "Hybrid: core suite plus specialist systems from different vendors"
answer: "Hybrid: core suite plus specialist systems from different vendors"
explain: "The HIS suite is all-in-one in itself, but the landscape as a whole is best-of-breed – the typical hybrid."
```

```quiz
question: "Task 2.1b: And at the communication level?"
options:
  - "Pure star"
  - "Spaghetti"
  - "Mostly star, with some direct connections"
answer: "Mostly star, with some direct connections"
explain: "The two questions are independent: a best-of-breed landscape can be integrated mostly as a star."
```

```reflect
question: "**Task 2.2:** Draw a simplified system landscape with the most important connections. Note here what strikes you while drawing."
rows: 3
answers:
  - "You will find the sample solution below this box. Pay special attention to the **PACS**: which connections does it have – and which does it not have?"
```

```include landscape-solution-en.svg
Show the sample solution for task 2.2
```

```reflect
question: "**Task 2.3:** What are the advantages and disadvantages of this architecture?"
answers:
  - "**Advantages:** specialist systems that fit each field (laboratory, blood bank, radiology, intensive care); a uniform interface for the core processes; the communication server limits the number of interfaces and bundles routing, mapping, buffering and monitoring."
  - "**Disadvantages:** many vendors and contracts; master data in many copies; the communication server is a single point of failure."
  - "**Direct connections** (RIS ↔ PACS, PDMS ↔ devices) are well justified (image data, real time), but they bypass the server's monitoring – and the PACS only receives changes indirectly."
```

## Part 3 · ADT and patient identity (15 min)

```timeline
title: "The patient's path"
events:
  - when: "14:05"
    what: "Admission in the ED as “Unknown, male”, ID 99127, case F2026-1048"
  - when: "15:20"
    what: "Transfer to the operating room"
  - when: "17:05"
    what: "Transfer to the intensive care unit"
  - when: "20:00"
    what: "Identity resolved: ID 99127 is Max Berger, who already has ID 34821"
```

```match
question: "Task 3.1: What changes each time?"
options:
  - "new patient, new case and first movement"
  - "only the movement (location)"
  - "the patient identity – case and movements stay"
items:
  - item: "14:05 admission in the ED"
    answer: "new patient, new case and first movement"
  - item: "15:20 transfer to the operating room"
    answer: "only the movement (location)"
  - item: "17:05 transfer to the intensive care unit"
    answer: "only the movement (location)"
  - item: "20:00 identity resolved"
    answer: "the patient identity – case and movements stay"
explain: "Patient ≠ case ≠ movement: at 20:00, case F2026-1048 with all its movements remains – it now simply belongs to a different, permanent patient identity."
```

```reflect
question: "**Task 3.2:** Which systems need to be informed about the transfer to the intensive care unit – and why?"
answers:
  - "**PDMS:** the patient has to appear on the bed list, and monitor data have to be assigned to him."
  - "**LIS and blood bank:** results, critical-value calls and blood products have to go to the ICU instead of the ED or the operating room."
  - "**RIS (and through it the PACS):** for result routing and further examinations, e.g. a follow-up CT."
  - "**OR system:** the stay in the operating room is over."
  - "**Billing:** ICU days and the department are relevant for billing."
  - "Technically this is an `ADT^A02`, which the communication server distributes to all subscribers."
```

```quiz
question: "Task 3.3a: Which HL7 v2 event fits the merge at 20:00?"
options: ["A02 – transfer", "A08 – update patient information", "A11 – cancel admission", "A40 – merge patient"]
answer: "A40 – merge patient"
shuffle: false  # options in a natural order
explain: "With `ADT^A40` the temporary ID 99127 is merged into the existing ID 34821. The permanent ID remains, and the temporary one is marked as merged. An A08 would only change the data under 99127 – the two records would stay separate."
```

```reflect
question: "**Task 3.3b:** What does merging the two identities mean for the connected systems?"
answers:
  - "**It is not only the HIS that has to be corrected.** Every copy of the patient context in LIS, blood bank, RIS, PACS, OR system and PDMS has to apply the merge."
  - "All data under 99127 – lab values, blood group, CT images, operation report, vital signs – now belong to 34821. Conversely, the **previous results** under 34821 only become visible now, e.g. earlier lab values, prior images, previous illnesses, allergies or an earlier blood group result."
  - "Merges are harder than simple updates: every system has to apply them correctly, and a wrong merge is hard to undo."
```

## Part 4 · Reconstructing orders & results (15 min)

Two information flows run in parallel:

- **Laboratory:** HIS → order → LIS → sample → analysis → validation → result → HIS
- **Radiology:** HIS → order → RIS → modality → PACS → reading → report and image link → HIS

```match
question: "Task 4.1: Which phase of the order/result pattern does the step belong to?"
options: ["Order", "Execution", "Validation / reading", "Result"]
items:
  - item: "Ordering blood count and coagulation in the HIS"
    answer: "Order"
  - item: "Measuring coagulation on the analyser"
    answer: "Execution"
  - item: "Medical validation of the coagulation values"
    answer: "Validation / reading"
  - item: "Lab result in the HIS"
    answer: "Result"
  - item: "Ordering the CT in the HIS"
    answer: "Order"
  - item: "CT examination, images go to the PACS"
    answer: "Execution"
  - item: "The radiologist reads the images"
    answer: "Validation / reading"
  - item: "Report and image link in the HIS"
    answer: "Result"
explain: "Laboratory and radiology follow the same pattern – only the systems and data types differ."
```

```reflect
question: "**Task 4.2:** Where does the correct patient identity have to travel along in both flows?"
answers:
  - "**Laboratory:** in the order (HL7 message), on the sample's **barcode label**, in the LIS order and in the result (`ORU`) back to the HIS – and in the blood bank on the blood group result and the blood product."
  - "**Radiology:** in the order to the RIS, in the **worklist** to the CT, in the **DICOM header** of every image, in the PACS and in the report back to the HIS."
  - "In this case that is the **temporary ID 99127** everywhere. It is not only in databases but also on labels and in image files. That is exactly what makes the later merge so laborious."
```

```match
question: "Task 4.3: Which connection would you expect to go via the communication server, and which to be direct?"
options: ["via the communication server", "direct"]
items:
  - item: "Lab order HIS → LIS"
    answer: "via the communication server"
  - item: "Lab result LIS → HIS"
    answer: "via the communication server"
  - item: "Blood group result blood bank → HIS"
    answer: "via the communication server"
  - item: "CT order HIS → RIS"
    answer: "via the communication server"
  - item: "Worklist RIS → CT"
    answer: "direct"
  - item: "CT images → PACS"
    answer: "direct"
  - item: "Vital signs monitor → PDMS"
    answer: "direct"
explain: "HL7 messages between the HIS and the subsystems run via the server. DICOM between RIS, modality and PACS and device data at the PDMS usually run directly – because of data volume, real time and tight vendor coupling."
```

## Part 5 · The failure scenario (20 min)

```case
**20:00.** In the HIS, the temporary ID **99127** and the existing ID **34821** are merged correctly. The change message reaches the HIS, LIS, blood bank, RIS and PDMS.

**The PACS, however, does not receive the change.** There, the head and chest CT images are still filed under “Unknown, male – ID 99127”.
```

```reflect
question: "**Task 5.1:** What problems could this cause?"
answers:
  - "Under Max Berger (34821) the PACS has no current CT images. The image link in the HIS leads nowhere or to an “unknown” record."
  - "New images, e.g. a follow-up CT the next day, are filed under 34821. Comparing them with the first CT is not straightforward."
  - "The PACS now has two “patients” for the same person – a duplicate that nobody has noticed."
  - "Copies passed on (teleradiology, consultation, report CD) carry the wrong identity."
```

```reflect
question: "**Task 5.2:** Which systems still appear “correct” from their own point of view?"
answers:
  - "**All of them.** The HIS has merged and sent the message. LIS, blood bank, RIS and PDMS have processed it. The PACS has flawlessly stored images under a valid ID."
  - "The PACS has no “error” – it simply does not know about the change. **Technically correct does not mean clinically correct.**"
  - "One possible reason lies in the architecture from part 2: the PACS is **not connected directly to the communication server**, but only receives patient changes via the RIS. If the RIS does not pass on the merge, it never reaches the PACS – and the server's monitoring sees nothing of it."
```

```reflect
question: "**Task 5.3:** Where would the failure probably be noticed first?"
answers:
  - "In clinical use, not in IT: when the ICU or neurosurgery wants to open the images from Max Berger's record and finds none."
  - "Or when a follow-up CT is read and the radiologist finds no prior study – although one must exist."
  - "In the worst case it is not noticed at all: everyone assumes there is no prior CT."
```

```reflect
question: "**Task 5.4:** What consequences could there be for (a) the current reading, (b) later comparisons with priors, (c) future treatment of the patient and (d) research or data export?"
rows: 5
answers:
  - "**(a) Current reading:** report and images belong to different identities. The radiologist lacks clinical information from the patient's history (34821)."
  - "**(b) Comparisons with priors:** a follow-up CT is read without comparison, e.g. on whether a bleed has grown. This leads to misjudgements or unnecessary repeat examinations with additional radiation."
  - "**(c) Future treatment:** at a later admission the accident images are missing from the record. Important findings (fractures, implants) cannot be found."
  - "**(d) Research and data export:** one person has two records. Cohorts are counted wrongly, courses of disease are split, and pseudonymisation produces two pseudonyms. Data quality is also a question of identity."
```

```reflect
question: "**Task 5.5:** Is this primarily a software error, an interface error, a process error, an organisational problem – or a combination? Give reasons."
answers:
  - "**A combination** – this is the socio-technical triangle from [[history]]."
  - "**Interface / architecture:** the merge is not routed to the PACS, or the direct RIS ↔ PACS connection does not pass it on."
  - "**Process:** there is no checklist of which systems need to be checked after a merge, and no feedback on whether all systems have applied it."
  - "**Organisation:** it is unclear who is responsible for merges (patient admission? radiology? IT?) and who monitors failures on direct connections."
  - "Remember: **technically correct ≠ clinically correct** – and **integration is patient safety.**"
```

## Part 6 · Improving the system (15 min)

```reflect
question: "**Task 6.1:** Name at least four measures that could reduce the risk. Think of technology, monitoring, identity management, processes and responsibilities."
rows: 5
answers:
  - "**Technology:** connect the PACS to the communication server with its own ADT feed (incl. A40); handle merges with IHE *Patient Information Reconciliation*."
  - "**Monitoring:** acknowledgements (ACK) for merges from *all* systems; a nightly reconciliation of whether temporary IDs still carry data in any system."
  - "**Identity management:** a master patient index; clear rules for emergency identities; a duplicate check as soon as the identity is known."
  - "**Process:** an “identity resolved” checklist covering all affected systems, closed only after each system has been checked."
  - "**Organisation:** named people responsible for merges (e.g. patient management) and for the direct connections; training and clear reporting paths when something looks wrong."
```

```match
question: "Assign the measures to the categories."
options: ["Technology", "Monitoring", "Identity management", "Process", "Organisation"]
items:
  - item: "The PACS gets its own ADT feed via the communication server"
    answer: "Technology"
  - item: "An alert when a system does not acknowledge the merge"
    answer: "Monitoring"
  - item: "Master patient index with duplicate check"
    answer: "Identity management"
  - item: "“Identity resolved” checklist for all affected systems"
    answer: "Process"
  - item: "Named people responsible for merges"
    answer: "Organisation"
```

```reflect
question: "**Task 6.2:** Would an all-in-one system automatically be safer? Give reasons."
answers:
  - "**Not automatically.** Within a suite with a shared database, the merge would be easier to keep consistent."
  - "But even a suite has specialist systems and devices it does not cover itself (modalities, analysers, monitoring), and external copies (teleradiology, research)."
  - "Individual modules can be weaker in their field. And failures in a suite then hit all areas at once."
  - "Safety depends less on the type of architecture than on how identity, events and monitoring are handled."
```

```reflect
question: "**Task 6.3:** Would it make sense to replace every direct connection with the communication server?"
answers:
  - "**Not necessarily.** Routing DICOM image data (hundreds of images per CT) and real-time vital signs through the HL7 server would make little technical sense and turn it into a bottleneck."
  - "What does make sense is that **patient context and identity changes** reach every system via a monitored path – including systems whose payload data flow directly."
  - "Direct connections need their own monitoring and clear responsibilities."
  - "Remember: **architecture decisions are trade-offs**, not “star good, spaghetti bad”."
```

## Final task

```reflect
question: "**Final task:** What would you check first when introducing a new diagnostic subsystem? Answer in no more than three sentences."
rows: 4
intro: "Your answer should cover several of these aspects:"
answers:
  - "**Identity:** how does the system receive patient identity and identity changes (incl. merges)?"
  - "**Case context:** does it know the case and location, and how do they stay current?"
  - "**Orders/results:** how do orders get in and results get back – with placer and filler numbers?"
  - "**Interfaces:** via the communication server or direct – and why?"
  - "**Monitoring:** who notices when a message does not arrive?"
  - "**Failure processes:** how are corrections, outages and emergency identities handled – and who is responsible?"
```

> **Take-home message:** hospital IT is not a single system but a landscape in which many systems have to share the same patient and case context correctly – even when that context changes after the fact.
