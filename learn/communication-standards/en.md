---
title: "Communication Standards I: HL7 v2, CDA, DICOM and IHE Profiles"
summary: "Mrs Müller is discharged – and her data, her discharge letter and her images have to leave the hospital. How do systems exchange data, documents and images in a standardised, reliable way? HL7 v2, CDA, DICOM, IHE profiles, communication patterns and xDT, worked through a case."
duration_minutes: 75
level: "In-depth"
audiences: [med, cs, clin, tech, pat]
order: 6
builds_on: [information-systems]
course: his
lecture: 4
author: "Kathrin Sobe"
objectives:
  - "Explain what HL7 v2, CDA and DICOM are used for and match them to typical scenarios (data, documents, images)"
  - "Read an HL7 v2 message (ADT, ORM, ORU) and explain how acknowledgements make the exchange reliable"
  - "Describe the structure of a CDA discharge letter and the basic principle of image communication with DICOM"
  - "Explain how IHE profiles, communication patterns, the communication server and xDT enable exchange across system and sector boundaries"
readings: [winter2023, benson2021, dolin2006]
related_topics: [fhir, ehr-cis, data-sharing, etl, privacy-ethics]
source: "Lecture 4 “Communication Standards I: HL7 v2, CDA, DICOM and IHE Profiles”, Health Information Systems (winter term 2026/27), Kathrin Sobe, IMB & ZMI"
---

> **Guiding question:** How do different medical information systems exchange data, documents and images in a standardised and reliable way?

In the module [[information-systems]] you saw how the HIS, LIS and RIS/PACS work together in the hospital, and you already touched on individual HL7 messages and DICOM terms – deliberately only on the surface. Now we look at the **standards themselves**: what is a standard for, how is it built, why did it come about this way – and where are its limits? Three kinds of object structure the module:

| Kind of object | Properties | Standard |
|---|---|---|
| **Data** | small-grained, event-related – “patient discharged” | HL7 v2 |
| **Documents** | complete, authored, signable – a discharge letter | HL7 CDA |
| **Images** | large objects with many metadata | DICOM |

On top of that come **workflows** (IHE profiles), **mediation** (communication patterns and the communication server) and the **outpatient sector** (xDT).

```persona med
Discharge letters, lab results and prior images reach you through exactly these standards – or they don't. If you understand what a “level 1 discharge letter” is, or why a result arrives later as “corrected”, you read results more safely.
```

```persona cs
HL7 v2 is a grammar with delimiters, CDA an XML schema with a reference model, DICOM an object model with negotiated connections, IHE a collection of sequence diagrams. You will recognise patterns from protocols, parsers and message brokers.
```

```persona clin
Why does the discharge letter arrive at the practice as a PDF even though it should be “structured”? Why are the prior images missing? This module shows where in the chain the answer lies.
```

```persona tech
MLLP, ACK, association, storage commitment, mapping tables in the communication server and exchange directories for xDT: the module is a map of the interfaces you operate.
```

```persona pat
Your discharge letter, your lab values and your X-rays travel between hospital, GP practice and radiology. This module shows which “languages” the systems speak for this – and why something sometimes gets lost on the way.
```

```case
**Mrs Erika Müller** (born 12 March 1958, patient ID 4711, case F2026-0815, community-acquired pneumonia) – the patient from [[information-systems]]. **Day 9, 21 October:** she is discharged.

1. **Discharge:** the case is closed – all subsystems need to know.
2. **Discharge letter:** written, signed off by a physician and sent to the GP.
3. **Images:** X-ray (13 Oct) and CT (14 Oct) are in the hospital's PACS.
4. **GP practice:** follow-up with an ECG on the device, CRP via the shared laboratory.
5. **Follow-up X-ray:** a few weeks later at a radiology practice – compared with the prior images.

**New compared with the last lecture:** the information leaves the hospital. Different vendors, different sectors, no shared database, no shared communication server – **only shared standards.** (Fictional case.)
```

```reflect
question: "Warm-up (30 seconds): what would the hospital, the GP practice and the radiology practice need to agree on for this to work?"
answers:
  - "**How** the data arrive (transport, connection, acknowledgement)"
  - "**How** they are structured (format, structure)"
  - "**What** they mean (shared codes, e.g. for diagnoses and lab values)"
  - "**Who** may exchange what with whom, and when (workflows, contracts, the patient's consent)"
  - "The next section sorts exactly these four levels."
```

## What a standard has to define: four levels

| Level | Guiding question | Standards (examples) | For Mrs Müller |
|---|---|---|---|
| **Organisational** | Who exchanges what with whom, and when? | IHE profiles, contracts, consent | Prior images retrieved by the radiology practice |
| **Semantic** | What does the content mean? | LOINC, ICD-10-GM, SNOMED CT | Discharge diagnosis J18.9 (ICD-10-GM) |
| **Syntactic / structural** | How is the unit built? | HL7 v2, CDA, DICOM, xDT | Discharge letter as CDA XML |
| **Technical** | Does it arrive at all? | TCP/MLLP, DICOM association, HTTP, file | `ADT^A03` via MLLP to the LIS |

The levels follow the HIMSS definition of interoperability (*foundational, structural, semantic, organisational*). **Remember: a syntax standard alone does not guarantee interoperability.** For every standard, ask: which level does it cover – and which not?

```match
question: "At which level does the problem lie?"
options: ["Technical", "Syntactic / structural", "Semantic", "Organisational"]
items:
  - item: "The connection to the LIS is broken after an update."
    answer: "Technical"
  - item: "The HIS expects HL7 v2.5, the LIS sends v2.3 with a different segment order."
    answer: "Syntactic / structural"
  - item: "The lab sends the CRP value with the in-house code “CRP”, the HIS only knows LOINC."
    answer: "Semantic"
  - item: "Nobody has agreed whether the radiology practice may retrieve the prior images."
    answer: "Organisational"
```

This map shows where each standard is used:

| | Outpatient: practice | Inpatient: hospital | Across the boundary |
|---|---|---|---|
| **Data** | xDT: GDT (devices), LDT (lab), KVDT (billing) | HL7 v2 (ADT, ORM, ORU) via the communication server | – |
| **Documents** | letter in the practice management system (PVS) | CDA discharge letter from the HIS | sent via KIM or provided via IHE XDS |
| **Images** | radiology practice | DICOM: worklist, store, PACS | IHE XDS-I.b |

IHE profiles do not invent new formats; they define **how the standards work together for a workflow**.

## 1 · HL7 v2: events as messages – and their acknowledgement

**HL7 version 2** is an **event-driven messaging standard**: something happens in the source system – Mrs Müller is discharged – and this event (*trigger event*) triggers a message. It is published by HL7 International (founded 1987, ANSI-accredited). HL7 came about because hospitals in the 1980s had more and more departmental systems with vendor-specific interfaces – the spaghetti problem from [[information-systems]].

```quiz
question: "What does the “7” in Health Level 7 stand for?"
options:
  - "The seventh version of the standard"
  - "The application layer, layer 7 of the OSI model"
  - "The seven founding members"
answer: "The application layer, layer 7 of the OSI model"
explain: "HL7 defines **content**, not transport. Transport is usually handled by TCP with MLLP (see below)."
```

Versions range from 2.0 (1988) to 2.9 (December 2019) with the sub-version 2.9.1; many hospitals run older versions such as 2.3 or 2.5 in parallel. New fields are appended, old ones are not removed – v2 is **backward compatible**, which explains its longevity. HL7 version 3 (XML, Reference Information Model RIM) hardly caught on for messaging; the strategic successor is [[topic:fhir]].

### The discharge, field by field

The discharge is an `ADT^A03` (version 2.5, simplified; “…” stands for omitted empty fields):

```text
MSH|^~\&|KIS|KLINIKUM|KOMSERVER|KLINIKUM|20261021110000||ADT^A03^ADT_A03|MSG0918|P|2.5
EVN|A03|20261021110000
PID|1||4711^^^KLINIKUM^PI||Müller^Erika||19580312|F
PV1|1|I|P3^12^A|…|F2026-0815|…|01|…|20261021110000
```

One special feature: the delimiters are declared **in the message itself**, in MSH-1 (`|`) and MSH-2 (`^~\&`). Fields are not plain strings but have **data types**: PID-3 is of type CX (ID^^^assigning authority^ID type), PID-5 of type XPN (family name^given name), PV1-3 of type PL (ward^room^bed), and timestamps follow the pattern YYYYMMDDhhmmss. Relevant for the discharge are PV1-19 (case number), PV1-36 (discharge disposition, `01` = home) and PV1-45 (discharge time). (KIS is the German abbreviation for the hospital information system.)

```match
question: "What is in which field of the message header (MSH)?"
options: ["Field separator and encoding characters", "Sending application", "Receiving application", "Message type ^ event ^ structure", "Control ID", "Processing mode (P = production)", "HL7 version"]
items:
  - item: "MSH-1 / MSH-2: `|` and `^~\\&`"
    answer: "Field separator and encoding characters"
  - item: "MSH-3: `KIS`"
    answer: "Sending application"
  - item: "MSH-5: `KOMSERVER`"
    answer: "Receiving application"
  - item: "MSH-9: `ADT^A03^ADT_A03`"
    answer: "Message type ^ event ^ structure"
  - item: "MSH-10: `MSG0918`"
    answer: "Control ID"
  - item: "MSH-11: `P`"
    answer: "Processing mode (P = production)"
  - item: "MSH-12: `2.5`"
    answer: "HL7 version"
explain: "The acknowledgement will refer to the control ID MSG0918."
```

### ADT, ORM and ORU: context, order, result

**Mnemonic:** ADT says *who and where*; ORM, *what should be done*; ORU, *what came of it*. You know the most important ADT events: A01 admission, A02 transfer, A03 discharge, A04 outpatient registration, A08 update of patient data, A40 merge of IDs.

The X-ray order of 13 October as `ORM^O01` and the CRP check before discharge as `ORU^R01`:

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

An order consists of **ORC** (order control, `NW` = new order) and **OBR** (what is requested); a result of OBR and one or more **OBX** (individual observation). Simplified: ORM = MSH · PID · { ORC · OBR }, ORU = MSH · { PID · { OBR · { OBX } } }. Newer HL7 versions use more specialised messages for orders, such as OML for the laboratory.

```quiz
question: "How does the HIS recognise that the CRP value is final – and what happens if it is corrected later?"
options:
  - "By the `H` – on correction, the message is deleted"
  - "By the `F` in OBX-11 – on correction, the lab sends a new ORU with `C`"
  - "By the control ID – on correction, it is incremented"
answer: "By the `F` in OBX-11 – on correction, the lab sends a new ORU with `C`"
explain: "`F` = final, `C` = corrected, `P` = preliminary. `H` only flags “above the reference range”."
```

### Structure, transport and acknowledgement

Three things turn text into **reliable** communication:

1. **Structure:** the abstract message definition specifies which segments come in which order – for ADT_A03, for example, `MSH EVN PID [PD1] PV1 [PV2] [{DG1}] [{OBX}]`; `[ ]` means optional, `{ }` repeatable. This is a grammar, comparable to an XML schema.
2. **Transport:** HL7 only covers the application layer. Transmission usually uses TCP with the **Minimal Lower Layer Protocol (MLLP)**: a start byte `0x0B`, the message (segments separated by CR), the end bytes `0x1C 0x0D`. This tells the receiver where a message starts and ends in the byte stream.
3. **Acknowledgement:** the receiver replies with an **ACK**; the MSA segment contains a code and the control ID of the original message.

```text
MSH|^~\&|KOMSERVER|KLINIKUM|KIS|KLINIKUM|20261021110001||ACK^A03^ACK|ACK7731|P|2.5
MSA|AA|MSG0918
```

```match
question: "What does the code in MSA-1 mean?"
options: ["accepted", "error during processing", "rejected"]
items:
  - item: "`AA` (application accept)"
    answer: "accepted"
  - item: "`AE` (application error)"
    answer: "error during processing"
  - item: "`AR` (application reject)"
    answer: "rejected"
explain: "In enhanced mode (MSH-15/-16) there is also a pure receipt acknowledgement with CA, CE and CR."
```

```quiz
question: "The HIS receives no ACK for the A03. What is right?"
options:
  - "The HIS assumes everything has arrived."
  - "The HIS resends; the control ID lets the receiver detect duplicates."
  - "The HIS sends a new A03 with a new control ID."
answer: "The HIS resends; the control ID lets the receiver detect duplicates."
explain: "Exactly this mechanism – plus monitoring of missing acknowledgements – would have made the stuck queue in the failure scenario from [[information-systems]] visible."
```

### HL7 v2 viewed critically

| Strengths | Weaknesses |
|---|---|
| simple, compact, quick to parse | many optional fields → every interface is different |
| huge installed base, tools, know-how | Z segments for site-specific content |
| backward compatible – systems can age at their own pace | no formal information model, semantics often local |
| event orientation fits clinical workflows | no built-in security (TLS or a secured network needed) |

> “If you've seen one HL7 v2 interface, you've seen one HL7 v2 interface.” – a saying in the community

```reflect
question: "For discussion: is the flexibility of HL7 v2 a success factor or a birth defect? And would you migrate a v2 landscape that runs stably in-house to FHIR? Note your answer – the next lecture comes back to it."
answers:
  - "**Success factor:** flexibility is what made v2 usable in the first place – every hospital could adapt it to its workflows, and old systems stayed connectable."
  - "**Birth defect:** the same flexibility makes every interface unique: mapping, testing and maintenance cost money permanently, and semantics stay local."
  - "**Migration:** in-house it rarely pays off on its own – often v2 runs internally and FHIR in parallel for new, cross-organisational or app-based use cases, with the communication server translating."
```

## 2 · Documents: HL7 CDA

The **Clinical Document Architecture (CDA)** is an XML-based HL7 standard for the structure and semantics of clinical documents – discharge letters, reports, discharge summaries [@dolin2006]. It is derived from the HL7 v3 Reference Information Model (RIM), which makes it the most successful part of the v3 family, and as ISO/HL7 27932:2009 it is also an international standard. Release 1 appeared in 2000, release 2 in 2005, release 2.1 in 2019; mostly R2 is implemented. CDA is used, for example, in the USA as Consolidated CDA (C-CDA), in Austria as the basis of the ELGA documents, and in Germany through discharge letter guides (VHitG letter 2006, HL7 Germany).

**Why a separate standard next to HL7 v2?** Because medicine is **document-centred**: Mrs Müller's discharge letter is a finished piece of work for which a physician takes responsibility, which has to be archived unchanged and which a person must be able to read. Messages alone cannot represent that.

```match
question: "Six properties of a clinical document according to CDA: which one is meant?"
options: ["Persistence", "Stewardship", "Potential for authentication", "Context", "Wholeness", "Human readability"]
items:
  - item: "The letter stays unchanged for the legal retention period."
    answer: "Persistence"
  - item: "The hospital is responsible for keeping the document."
    answer: "Stewardship"
  - item: "A physician signs off the letter and can sign it."
    answer: "Potential for authentication"
  - item: "Patient, stay and author apply to the whole content without being repeated each time."
    answer: "Context"
  - item: "The letter is signed off as a whole, not section by section."
    answer: "Wholeness"
  - item: "The GP can read it without special software."
    answer: "Human readability"
```

### Header, body and the three levels

A CDA document has two main parts. The **header** is always structured and answers: who is it about (`recordTarget`), who wrote it (`author`), which organisation keeps it (`custodian`), who is legally responsible (`legalAuthenticator`), in which stay was it created (`encompassingEncounter`) – plus document type, date and confidentiality. That is why CDA documents can be managed in registries even if the content is only a PDF. The **body** contains sections (`section`) with code, title and **text**; the text is the **binding** content, and `entry` elements can additionally contain the same statements in coded form.

```text
<ClinicalDocument xmlns="urn:hl7-org:v3">
  <typeId root="2.16.840.1.113883.1.3" extension="POCD_HD000040"/>
  <id root="1.2.3.999" extension="EB-2026-0815"/>   <!-- fictional OID -->
  <code code="18842-5" codeSystem="2.16.840.1.113883.6.1"
        displayName="Discharge summary"/>          <!-- LOINC -->
  <title>Entlassbrief</title>
  <effectiveTime value="20261021"/>
  <confidentialityCode code="N" codeSystem="2.16.840.1.113883.5.25"/>
  <recordTarget> … Erika Müller, *12.03.1958, ID 4711 … </recordTarget>
  <author> … Dr. A. Beispiel, internal medicine … </author>
  <custodian> … hospital … </custodian>
  <legalAuthenticator> … </legalAuthenticator>
  <component><structuredBody>
    <component><section>
      <code code="11535-2" codeSystem="2.16.840.1.113883.6.1"/>
      <title>Entlassdiagnose</title>
      <text>Ambulant erworbene Pneumonie (ICD-10-GM J18.9)</text>
      <entry> … coded diagnosis (level 3) … </entry>
    </section></component>
  </structuredBody></component>
</ClinicalDocument>
```

The text is typically displayed as HTML via an XSLT stylesheet. In Germany, guides from HL7 Germany define templates and mandatory content – deliberately left out here. **Without guides, CDA is almost as open as HL7 v2.**

```match
question: "The same discharge letter at three levels: which level is meant?"
options: ["Level 1", "Level 2", "Level 3"]
items:
  - item: "Structured header, content only as an embedded PDF (`nonXMLBody`) – readable but not analysable"
    answer: "Level 1"
  - item: "The section is coded with LOINC 11535-2 – software finds “discharge diagnosis” but only reads text"
    answer: "Level 2"
  - item: "In addition, an `entry` contains the diagnosis J18.9 in coded form – machine-analysable, the text remains binding"
    answer: "Level 3"
explain: "The levels are a **migration path**: start with level 1 and add more structure step by step."
```

### CDA compared and viewed critically

| Criterion | PDF/A (letter as a file) | HL7 CDA R2 | FHIR document (Bundle) |
|---|---|---|---|
| human-readable | yes | yes (stylesheet) | yes (narrative) |
| machine-readable | hardly | depending on level 1–3 | yes, resource-based |
| signature / persistence | yes | yes, core concept | yes, core concept |
| format / technology | binary layout | XML, v3 RIM | JSON/XML, REST |
| barrier to entry | low | high (RIM, templates) | medium |

The comparison is a didactic simplification. **Criticism:** in practice it often stays at level 1 – a structured PDF in an XML envelope; text and entries can contradict each other; the complexity of the RIM deters developers. CDA solves the document problem that messaging standards leave open – its value grows with the degree of structure and with binding guides. FHIR takes over the document concept but also makes the content usable as individual resources.

```reflect
question: "For discussion: in case of dispute, what is “the discharge letter” – the signed text or the coded data? And who is liable if software at the GP practice only analyses the entries?"
answers:
  - "According to CDA, the **text is binding** – the entries are an additional machine-readable representation."
  - "If the two contradict each other, software that only reads the entries can draw wrong conclusions. Several parties are then responsible: the vendor of the producing system (consistency of text and entries), the vendor of the analysing software (handling contradictions) and the users who rely on it."
  - "Guides and conformance testing reduce the risk – but do not remove it completely."
```

## 3 · Images: DICOM

The letter alone is not enough for the radiologist at the practice – she needs the images: the chest X-ray of 13 October (accession no. R-26-1188) and the CT of 14 October (R-26-1231, several series, around 800 images).

```reflect
question: "Warm-up (2 minutes): apart from the pixels, which information does the radiologist need to compare safely? Why is it not enough to send the images as JPEGs by email? Who needs to talk to whom?"
answers:
  - "Patient, examination, date, device, body side, positioning, scale and acquisition parameters – exactly the metadata a DICOM object carries."
  - "A JPEG loses this context, the full bit depth and the link to patient and order; email also raises data protection and reliability issues."
  - "Hospital and practice need an agreed workflow (who may retrieve which prior images?) – the organisational level that IHE profiles such as XDS-I address."
```

**DICOM** (*Digital Imaging and Communications in Medicine*) is at the same time a **data model, file format and network protocol**, also standardised as ISO 12052, maintained by the DICOM Standards Committee (secretariat at NEMA/MITA) and published as a new edition several times a year (parts PS3.x). In the early 1980s, CT and MR images could practically only be read with the device vendor's software; ACR and NEMA formed a joint committee in 1983.

```timeline
title: "From ACR-NEMA to DICOMweb"
events:
  - when: "1985"
    what: "ACR-NEMA 1.0 – point-to-point, dedicated hardware interface"
  - when: "1988"
    what: "ACR-NEMA 2.0 – extended, still no network"
  - when: "1993"
    what: "DICOM 3.0 – TCP/IP, object model, services: the basis to this day"
  - when: "from the 2000s"
    what: "DICOMweb – HTTP/REST services (WADO-RS, QIDO-RS, STOW-RS)"
```

### Services, roles and connection set-up

From [[information-systems]] you know how a DICOM object is structured (patient → study → series → instance). Now: how are objects **moved**?

- **SOP class** = information object + service, each with a globally unique UID – for example *CT Image Storage* (1.2.840.10008.5.1.4.1.1.2) or *Modality Worklist – FIND* (1.2.840.10008.5.1.4.31).
- **Roles:** the *service class user* (SCU) uses a service, the *service class provider* (SCP) provides it. When storing, the modality is the SCU and the PACS the SCP. Addressing uses **AE title + IP + port** (registered: 104, often 11112).
- **Association:** unlike HL7 v2, there is **negotiation** first: the modality proposes SOP classes and encodings (*transfer syntaxes*) (A-ASSOCIATE-RQ), the PACS confirms what it supports (A-ASSOCIATE-AC). Only then does the service follow, e.g. C-STORE, and finally an orderly release (A-RELEASE). If capabilities don't match, the negotiation fails with a clear error message instead of broken data.
- **Services:** C services for composite objects such as images (C-ECHO, C-STORE, C-FIND, C-MOVE, C-GET), N services for normalised objects such as status messages (N-CREATE, N-SET …). Every system must support *Implicit VR Little Endian*.

```match
question: "Mrs Müller's chest X-ray: put the DICOM steps in the right order."
options: ["1", "2", "3", "4", "5"]
items:
  - item: "C-FIND modality worklist: “who's next?” – the modality takes over the patient data from the RIS"
    answer: "1"
  - item: "MPPS (N-CREATE/N-SET): examination started or completed"
    answer: "2"
  - item: "C-STORE: images to the PACS"
    answer: "3"
  - item: "Storage commitment: are the images safely archived?"
    answer: "4"
  - item: "Search and load at the reading workstation: C-FIND/C-MOVE or QIDO-RS/WADO-RS"
    answer: "5"
explain: "DICOMweb (PS3.18) offers the same functions via HTTP/REST – the basis of many web viewers."
```

```quiz
question: "A modality deletes images locally before they are safely archived. Which step is missing?"
options: ["Modality worklist", "MPPS", "Storage commitment", "C-ECHO"]
answer: "Storage commitment"
explain: "Storage commitment is the **DICOM counterpart to the HL7 ACK**: only once the PACS confirms safe archiving may the modality delete."
```

### DICOM viewed critically

**Success factors:** accepted across vendors, image and metadata inseparable, continuous maintenance through supplements; vendors disclose what their devices can do in a **conformance statement** (PS3.2). **Problems:** a conformance statement does not guarantee interoperation; *private tags* contain vendor-specific content; data volumes are huge (CT, digital pathology); without a worklist, misassignments happen. **Security:** classic DICOM transmits unencrypted; PS3.15 defines TLS and de-identification profiles, among others – they have to be actively used. Metadata and burned-in text can contain personal data.

```reflect
question: "For discussion: DICOM archives are training material for AI. Is removing name and patient ID enough for effective anonymisation – for example when a face can be reconstructed from a head CT?"
answers:
  - "**No.** Personal data also sit in other header fields (dates, institution, device), in private tags, in text burned into the image – and in the image content itself."
  - "Faces can be reconstructed from head CT or MRI; only additional methods such as removing the facial soft tissue (*defacing*) help."
  - "Effective de-identification is a process with profiles (PS3.15), checks and an assessment of the residual risk – see the topic [[topic:privacy-ethics]]."
```

## 4 · IHE profiles: combining standards into workflows

We have seen three standards – and the same problem in all of them: **many open options**. **IHE** (*Integrating the Healthcare Enterprise*) is an initiative of users and vendors, founded in 1998 by RSNA and HIMSS, because people realised: the standards are there, but *plug & play* still doesn't work. IHE generally defines **no new formats** but **integration profiles** that specify how existing standards are used for concrete use cases.

```timeline
title: "The IHE process"
events:
  - when: "1"
    what: "Use case"
  - when: "2"
    what: "Integration profile: actors (abstract roles) and transactions between them"
  - when: "3"
    what: "Technical framework: specification down to individual HL7 and DICOM fields"
  - when: "4"
    what: "Connectathon: vendors test directly against each other"
  - when: "5"
    what: "Integration statement in the product – the hospital's tender asks not for “HL7” but for “actor X in profile Y”"
```

**Scheduled Workflow (SWF)** is exactly the DICOM workflow above as a profile: the HIS (ADT, order placer) sends patient data and the order to the RIS (order filler) via HL7 (RAD-1, -2, -4), then DICOM takes over with the worklist (RAD-5), MPPS (RAD-6/-7), storage (RAD-8) and storage commitment (RAD-10).

**Cross-Enterprise Document Sharing (XDS.b)** – now Mrs Müller's discharge letter leaves the hospital:

```include xds-en.svg
```

```match
question: "Which XDS.b transaction is meant?"
options: ["ITI-41", "ITI-42", "ITI-18", "ITI-43"]
items:
  - item: "The hospital puts the CDA discharge letter into the repository (provide & register)."
    answer: "ITI-41"
  - item: "The repository registers the metadata from the CDA header in the registry."
    answer: "ITI-42"
  - item: "The GP practice searches the registry for documents about Mrs Müller (stored query)."
    answer: "ITI-18"
  - item: "The GP practice fetches the letter from the repository (retrieve)."
    answer: "ITI-43"
explain: "For the radiology practice's prior images there is **XDS-I.b** on the same principle. In Germany, document management in the electronic patient record (ePA), among others, is based on IHE XDS transactions (see [[topic:data-sharing]])."
```

Further building blocks: **PIX/PDQ** solve the problem of different patient numbers across organisations – 4711 only applies in the hospital –, **ATNA** provides audit logs and secured connections, **CT** (*consistent time*) synchronised clocks. **Critically:** profiles are extensive, they too leave options, and passing a connectathon does not mean stable operation.

```quiz
question: "Do we still need IHE now that FHIR exists?"
options:
  - "No – FHIR replaces IHE completely."
  - "Yes – the idea of “profiles for use cases” is technology-independent; IHE now also specifies FHIR-based profiles such as MHD."
  - "Only in radiology."
answer: "Yes – the idea of “profiles for use cases” is technology-independent; IHE now also specifies FHIR-based profiles such as MHD."
```

## 5 · Communication patterns and the communication server

Across all standards: **who initiates the exchange – and who translates?**

```include patterns-en.svg
```

```match
question: "Which pattern is it?"
options: ["Push", "Pull", "Publish/subscribe"]
items:
  - item: "Mrs Müller is discharged – the HIS immediately sends the A03."
    answer: "Push"
  - item: "The discharge letter is sent to the GP via KIM."
    answer: "Push"
  - item: "The modality queries the worklist."
    answer: "Pull"
  - item: "The GP fetches the letter via XDS when she needs it."
    answer: "Pull"
  - item: "The practice system regularly checks the exchange directory for new xDT files."
    answer: "Pull"
  - item: "The communication server distributes every ADT message to all subsystems that have subscribed to it."
    answer: "Publish/subscribe"
  - item: "FHIR subscriptions or IHE DSUB notify subscribers about new documents."
    answer: "Publish/subscribe"
explain: "**Push:** current and efficient, but the sender must know the receiver, and if the receiver fails, queues are needed. **Pull:** the receiver decides when; polling creates load and delay. **Publish/subscribe:** decoupling, easy to extend – but the broker becomes a critical component. You know these patterns from webhooks, REST APIs and message brokers such as MQTT or Kafka."
```

### The communication server translates

From [[information-systems]] you know routing, transformation, queueing and monitoring. The focus here is on **transformation**: the LIS still speaks HL7 2.3 and sends the CRP value with the in-house code “CRP”; the HIS expects 2.5 and LOINC.

```text
Input from the LIS (HL7 v2.3, in-house code):
MSH|^~\&|LIS|...||ORU^R01|...|P|2.3
OBX|1|NM|CRP^CRP^L||182|mg/L|<5|H|||F

Output to the HIS (HL7 v2.5, LOINC):
MSH|^~\&|LIS|...||ORU^R01^ORU_R01|...|P|2.5
OBX|1|NM|1988-5^C-reaktives Protein^LN||182|mg/L|<5|H|||F
```

Typically translated are **versions** (MSH-9 and -12, new mandatory fields), **codes** (in-house code → LOINC), **identifiers** (local IDs, ward codes) and **transport routes** (MLLP, file directory for xDT, web service). Product examples, without judgement: Infor Cloverleaf, Rhapsody, NextGen Connect (formerly Mirth Connect), soffico Orchestra. This is a form of [[topic:etl]] in live operation.

```reflect
question: "The server compensates for missing standard compliance – and thereby hides it. If “CRP” is mapped to a wrong LOINC code, the value is formally correct and clinically wrong. Who is responsible if a mapping is wrong – IT, the laboratory or the vendor?"
answers:
  - "**Every mapping table is domain logic**: it needs clinical ownership (the lab for lab codes), technical implementation (IT / interface team) and checking against the standard."
  - "It needs a documented sign-off for every mapping change, tests with realistic messages and version control."
  - "In the long run, the better solution is to use the standard at the source – then the server has less to translate."
```

## 6 · xDT: data exchange in the doctor's practice

In the German outpatient sector, the **xDT formats** dominate. They were developed in the late 1980s / early 1990s on behalf of the National Association of Statutory Health Insurance Physicians (KBV), among others by the Central Research Institute of Ambulatory Health Care (Zi) – a German special path, closely tied to billing and practice IT.

```match
question: "What is the xDT format used for?"
options: ["KVDT", "BDT", "GDT", "LDT"]
items:
  - item: "Billing with the Association of Statutory Health Insurance Physicians (formerly “ADT” – not to be confused with HL7 ADT)"
    answer: "KVDT"
  - item: "Treatment data, e.g. when switching practice software or for archiving"
    answer: "BDT"
  - item: "Connecting medical devices such as the ECG in Mrs Müller's GP practice"
    answer: "GDT"
  - item: "Lab orders and results, e.g. the CRP value from the shared laboratory"
    answer: "LDT"
explain: "KVDT and LDT are maintained by the KBV, BDT and GDT by the Qualitätsring Medizinische Software (QMS); the current version is GDT 3.5 (2022)."
```

The structure is deliberately simple: **each line is a field** – three digits of line length, four digits of field ID, then the content, and CR LF at the end. Here the practice management system (PVS) asks the ECG device for an examination of Mrs Müller (simplified, based on GDT 2.1):

```text
01380006302      8000 record type 6302 = request new examination
014810000130     8100 record length in bytes
0158315EKG_01    8315 receiver ID
0158316PVS_01    8316 sender ID
014921802.10     9218 GDT version
01330002093      3000 patient number
0153101Müller    3101 family name
0143102Erika     3102 given name
017310312031958  3103 date of birth
```

```quiz
question: "Check the arithmetic: why does the first line start with “013”?"
options:
  - "3 digits of length + 4 digits of field ID + 4 characters of content + 2 characters of line end = 13"
  - "Because the record type has 13 fields"
  - "Because the GDT version is 13"
answer: "3 digits of length + 4 digits of field ID + 4 characters of content + 2 characters of line end = 13"
explain: "By the way, the practice's patient number (2093) differs from the hospital's 4711 – exactly the identity problem that IHE PIX/PDQ addresses."
```

**The GDT workflow:** the PVS writes the request as a file into an exchange directory → the device reads it and measures → the device writes the result (record type 6310) → the PVS takes it over. File-based, **without an acknowledgement protocol**. For an implementation, the current QMS record description applies.

```match
question: "xDT or HL7 v2?"
options: ["xDT", "HL7 v2"]
items:
  - item: "outpatient, Germany"
    answer: "xDT"
  - item: "mainly inpatient, international"
    answer: "HL7 v2"
  - item: "line = length + field ID + content"
    answer: "xDT"
  - item: "segments, fields, delimiters"
    answer: "HL7 v2"
  - item: "mostly a file in an exchange directory, no acknowledgement in the protocol"
    answer: "xDT"
  - item: "mostly TCP with MLLP, ACK mechanism"
    answer: "HL7 v2"
explain: "**Criticism of xDT:** a national special path with few international tools; file exchange brings locking, error and security issues (half-written files, access rights). **But:** robust, simple, available in almost every practice system. Cross-sector communication is moving into the telematics infrastructure (TI): KIM for sending (e.g. the eArztbrief), the ePA and the KBV's FHIR-based medical information objects (MIO)."
```

```reflect
question: "For discussion: should Germany switch consistently to international standards in outpatient care? Who bears the costs of the switch – practices, vendors, insurers?"
answers:
  - "**For:** international tools and skilled staff, simpler cross-sector communication, less translation at every boundary."
  - "**Against / hurdles:** tens of thousands of practices with working installations, tight coupling to billing, switching effort without immediate benefit for the individual practice."
  - "A **gradual transition** via the telematics infrastructure (KIM, ePA, FHIR-based MIOs) is realistic, with xDT running in parallel for devices and billing for a long time."
```

## Summary: Mrs Müller's path – resolved

```match
question: "Which standard (and which pattern) fits?"
options:
  - "HL7 v2 ADT^A03 via MLLP with ACK – push via the communication server"
  - "HL7 CDA R2 – push via KIM or pull via IHE XDS"
  - "DICOM (association, C-STORE, storage commitment) within IHE SWF"
  - "xDT: GDT, LDT, KVDT – file-based, polling"
  - "IHE XDS-I.b – pull"
items:
  - item: "The discharge has to reach all subsystems in the hospital."
    answer: "HL7 v2 ADT^A03 via MLLP with ACK – push via the communication server"
  - item: "The discharge letter has to go to the GP."
    answer: "HL7 CDA R2 – push via KIM or pull via IHE XDS"
  - item: "X-ray and CT are created and archived."
    answer: "DICOM (association, C-STORE, storage commitment) within IHE SWF"
  - item: "At the GP practice: ECG, CRP via the shared lab, billing."
    answer: "xDT: GDT, LDT, KVDT – file-based, polling"
  - item: "The radiology practice retrieves the prior images."
    answer: "IHE XDS-I.b – pull"
```

> **Mnemonic:** data → HL7 v2 · documents → CDA · images → DICOM · workflows → IHE · translation → communication server · outpatient → xDT

## Take-home messages

1. **Purpose before format:** data → HL7 v2 · documents → CDA · images → DICOM. If you know the purpose, you choose the right standard.
2. **Reliable means more than syntax:** acknowledgements, unique IDs, shared codes and agreed workflows (IHE) make the exchange safe.
3. **Crossing boundaries:** in-house, the communication server mediates; across organisational and sector boundaries you need profiles, the telematics infrastructure and – in outpatient care – xDT.

## Comprehension question

```reflect
question: "Mrs Müller's GP is to receive the discharge letter, the shared laboratory is to report back a CRP value, and the radiology practice is to retrieve the prior images. Which standard do you use in each case – and why?"
rows: 4
answers:
  - "**Discharge letter:** as a CDA document (an authored, signable, human-readable document) – sent via KIM or provided via IHE XDS."
  - "**CRP value:** via LDT – the established standard between shared laboratory and practice management system in outpatient care."
  - "**Prior images:** as DICOM objects (with all metadata) via IHE XDS-I – the practice queries when needed (pull)."
```

## Outlook: Communication Standards II – FHIR

The next lecture covers [[topic:fhir]]: resources instead of messages and documents, REST instead of MLLP – and the question of how much of HL7 v2, CDA and IHE lives on in it.

## Self-test

```quiz
question: "Which statement about HL7 v2 is true?"
options:
  - "HL7 v2 also defines the encryption of the transmission."
  - "New fields are appended and old ones are not removed – which is why v2 is backward compatible."
  - "Every field of a v2 message is mandatory."
answer: "New fields are appended and old ones are not removed – which is why v2 is backward compatible."
```

```quiz
question: "What is legally binding in a CDA document?"
options: ["the text of the sections", "the coded entries", "the header alone"]
answer: "the text of the sections"
```

```quiz
question: "How does connection set-up in DICOM differ from HL7 v2?"
options:
  - "In an association, DICOM first negotiates SOP classes and transfer syntaxes."
  - "DICOM always uses a file in an exchange directory."
  - "There is no difference."
answer: "In an association, DICOM first negotiates SOP classes and transfer syntaxes."
```
