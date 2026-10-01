---
title: "History and Development of Medical Informatics"
summary: "Why many of today's digitalization problems – silos, media breaks, low acceptance – have grown historically, and why medical informatics is always a socio-technical field."
duration_minutes: 30
level: "Introductory"
audiences: [med, cs, clin, tech, pat]
order: 1
course: "Introduction to Medical Informatics"
author: "Markus Wolfien"
objectives:
  - "Name early drivers of digitalization in health care"
  - "Place hospital, laboratory and imaging information systems (HIS, LIS, PACS) in their historical and functional context"
  - "Explain why data silos have grown historically"
  - "Describe medical informatics as a socio-technical field"
  - "Recognize basic ethical questions of responsibility and delegation"
readings: [haux2006, berg2001, sittig2010, hayrinen2008]
related_topics: [ehr-cis, fhir, cdss]
source: "Lecture 2 “History and Development of Medical Informatics”, Introduction to Medical Informatics (summer term 2026), Markus Wolfien, IMB & ZMI"
---

> *“Report needed – record not available – information collected again.”*

Almost everyone who has worked in a hospital knows this scene. That is why we don't start with a technical definition but with a historical perspective: **medical informatics is not simply computer science in the hospital.** It connects medical knowledge, data, organization, technology and responsibility.

```persona med
On the ward you will work with IT landscapes that have grown over decades. If you understand *why* results sit in three different systems, you can work with them better – and have a say in the next system rollout.
```

```persona cs
Hospital IT is a textbook case of legacy systems. Its history explains why "just build another interface" rarely does the job.
```

```persona clin
Much frustration with documentation systems comes from a poor fit, not from user error. This unit gives you the vocabulary to name it.
```

```persona tech
You know software architecture – here you learn why, in health care, it can never be designed without organization, law and clinical work.
```

```persona pat
Why do I have to bring my test results again and again? This unit explains how it came to this – and what is changing now.
```

## Why start with history?

When people talk about digitalization in health care today, the same terms come up again and again: **data silos, media breaks, interface problems, acceptance, data protection.** These problems did not appear overnight – many have historical, organizational and technical causes.

A first thesis:

> **"Digitalization in health care is never just a technical project."**

It changes clinical workflows, organizational responsibilities, information flows, accountability and room for decisions – and the relationship between patients, medicine and technology.

## 1 · From paper to early computing

Before digitalization, medical information was mainly paper-based, handwritten or form-based, available only locally and tied to particular places or people. Paper is not bad per se – for a long time it was a flexible and robust medium. But it has limits:

| Paper-based information | Digital information |
|---|---|
| local | potentially networked |
| hard to search | searchable |
| hard to analyze | analyzable |
| tied to a place | transferable |

Typical consequences of paper-based documentation: time spent searching, duplicate work, incomplete information, limited legibility, delayed hand-over and limited analysis. You know many of these problems from outside medicine too – but here they affect diagnosis, therapy and patient safety.

```quiz
question: "What was probably digitized **first** in hospitals?"
options:
  - "Complex therapy decisions"
  - "The doctor–patient conversation"
  - "Billing and documentation of services"
  - "Interprofessional case conferences"
answer: "Billing and documentation of services"
explain: "Digitalization often starts where processes are **formally describable, recurring, subject to documentation requirements and economically relevant** – and easy to turn into data structures. The *why* is what matters here."
```

The first IT applications covered areas that were easy to formalize: patient administration, documentation of services, billing, resource and bed management, reporting and simple statistics. So the beginning was not artificial intelligence or the digital twin – it was wherever information had to be counted, ordered, standardized and billed.

```match
question: "Guess the timeline: which phase belongs to which period?"
options: ["until the 1960s", "1960s–70s", "1970s–80s", "1990s–today"]
items:
  - item: "Networking, hospital information systems, electronic health records"
    answer: "1990s–today"
  - item: "Paper records as the standard"
    answer: "until the 1960s"
  - item: "First clinical subsystems, e.g. laboratory and image archiving"
    answer: "1970s–80s"
  - item: "Computing for administration (finance, admission)"
    answer: "1960s–70s"
explain: "Development went from administration via individual clinical subsystems to networking – not as a centrally planned master design. The periods are a rough orientation."
```

```timeline
title: "Rough lines of development"
collapsed: "Solution: show the timeline"
events:
  - when: "until the 1960s"
    what: "Paper-based documentation"
  - when: "1960s–70s"
    what: "Computing for administration: finance, admission"
  - when: "1970s–80s"
    what: "First clinical subsystems: laboratory, image archiving (PACS)"
  - when: "1990s–today"
    what: "Networking, hospital information systems, electronic health records"
```

### Why documentation, billing and administration first?

> **What can be described formally is often digitized first.**

- **Standardizability:** many administrative workflows can be described formally.
- **Administrative pressure:** hospitals have to document and prove the services they provide.
- **Cost-effectiveness:** digital systems promised efficiency, overview and control.

Administration is not a side issue: *Who is the patient? When does a treatment case begin? Which services and results belong to it? Who is responsible?* These structures create the data flows on which later clinical and scientific use is built.

| Administrative processes | Medical decisions |
|---|---|
| more rule-based | more context-dependent |
| easy to standardize | often ambiguous |
| formally documentable | dependent on experience and situation |
| economically relevant | clinically and ethically consequential |
| digitized early | supported later and more cautiously |

## 2 · HIS, LIS and PACS

The early islands of digitalization grew into specialized information systems – for admission and administration, wards, laboratories, radiology, operating rooms and discharge.

- **HIS – hospital information system** (German: KIS): the "backbone" of the digital hospital. Patient admission and case management, clinical documentation, orders and results, documentation of services, discharge, interfaces to subsystems.
- **LIS – laboratory information system:** supports laboratory processes from sample to result. Laboratories were *early adopters*: highly standardizable, structured data, clear process chains.
- **PACS – picture archiving and communication system:** stores, archives and communicates image data between devices and workstations and provides prior images for comparison. Image data are large, visual and time-critical – they need their own infrastructure.

| Area | Data type | Process logic | Typical system |
|---|---|---|---|
| Ward | clinical documentation | continuous care | HIS |
| Laboratory | measurements, samples | standardized analysis | LIS |
| Radiology | image data | imaging and reporting | PACS |
| Administration | case and billing data | administrative control | HIS / ERP |

```match
question: "Mini exercise: which system does what?"
options: ["HIS", "LIS", "PACS"]
items:
  - item: "Validate and transmit laboratory values"
    answer: "LIS"
  - item: "Store and display radiological images"
    answer: "PACS"
  - item: "Support patient admission and case management"
    answer: "HIS"
  - item: "Prepare the discharge letter"
    answer: "HIS"
  - item: "Provide prior images for comparison"
    answer: "PACS"
  - item: "Track sample status"
    answer: "LIS"
explain: "The systems are not separate by accident: they reflect different tasks, data types and process logics. *Subsystems express professional specialization, not just technical fragmentation.*"
```

Specialization is a strength at first: tailored support, closeness to the process, better representation of specific data types. **But** integration becomes more complex, data models differ, responsibilities are distributed – and interfaces become necessary. Clinical IT landscapes grew step by step, over many years, with different vendors and local adaptations:

> **Hospital IT has often grown rather than been designed.**

## 3 · Silos and processes

Landscapes that grew historically lead to **silos** – and not only technical ones:

| Technical silos | Organizational silos |
|---|---|
| separate databases | separate responsibilities |
| different interfaces | different documentation cultures |
| incompatible data formats | department-specific processes |
| lack of semantic harmonization | local priorities |

That is why interoperability is never just about interfaces. An IT system never acts alone; it is always part of a larger system of work and care – with data, users, processes, organization, law and infrastructure.

```include triangle-en.svg
```

The **socio-technical triangle** is a key idea for everything that follows – from electronic health records to interoperability and AI-based decision support. [@sittig2010] describe a more detailed model with eight dimensions.

**Systems don't just mirror processes – they change them.** A single mandatory field changes what gets documented; an automatic notification changes who reacts when. Before: verbal hand-over, a paper note, a later entry. Today: a digital form, mandatory fields, automatic forwarding. Conversely, good systems must know clinical reality: time pressure, exceptions, different professions, critical situations, uncertain information – otherwise they create extra work and workarounds.

> **Acceptance ≈ benefit + fit + trust – extra effort**

```reflect
question: "Mini case: a hospital introduces a new documentation system. It formally meets all requirements. Afterwards, doctors and nurses report extra clicks, duplicate documentation, unclear responsibilities and falling acceptance. Is the problem technical, organizational or about processes?"
intro: "Usually not either–or, but a **problem of fit** between the logic of the system, of the work, of documentation, of responsibility and of the organization. Levers include:"
answers:
  - "improving the technical implementation"
  - "process analysis *before* the rollout"
  - "training and support"
  - "clear responsibilities"
  - "user orientation and a step-by-step rollout strategy"
```

| Typical pitfall | Possible consequence |
|---|---|
| no process analysis | system doesn't fit daily work |
| little user involvement | low acceptance |
| poor interoperability | data silos |
| unclear responsibility | no lasting improvement |

Many projects don't fail because of the technical idea but because of the rollout, embedding and connectivity – see also [@berg2001].

```quiz
question: "A hospital wants to introduce an AI tool for decision support. Which lesson from history matters most?"
options:
  - "Pick the best model – the rest will follow"
  - "First understand the processes and responsibilities, then introduce the system"
  - "Test the tool without involving the users first"
answer: "First understand the processes and responsibilities, then introduce the system"
explain: "Old patterns, new technologies: AI won't succeed either if data quality, process integration, responsibility and usability are not right. The same holds for dashboards, telemedicine, research data platforms and patient apps."
```

```persona clin
If you are involved in a system rollout: ask early about process analysis, training and evaluation after go-live. These are the points where projects most often fail.
```

```persona cs
Requirements "formally met" does not mean "usable in daily work". Observe real workflows before you design data models and forms.
```

## 4 · Responsibility

Ethics does not only come into play with artificial intelligence. Digitizing documentation and information flows already changes who can see what, what gets standardized and how responsibility is distributed.

| Technical development | Ethical question |
|---|---|
| digital documentation | Who may know what? |
| structured data capture | What is lost through standardization? |
| decision support | Who is responsible? |
| data integration | How is trust maintained? |

**Joseph Weizenbaum** – the computer scientist who wrote ELIZA, one of the first chat programs, in 1966 – later warned against naive enthusiasm for technology in *Computer Power and Human Reason* (1976). In essence: *not everything that is technically possible should be delegated to computers without reflection.* He stressed protecting human judgment and sensitivity to human relationships – questions that are more relevant than ever with today's language models.

```reflect
question: "Which task do you think should never be delegated entirely to a technical system – and why?"
intro: "Frequently mentioned examples:"
answers:
  - "the therapy decision"
  - "the conversation about bad news"
  - "prioritization in borderline cases"
  - "taking final responsibility"
```

**Hans Jonas** (*The Imperative of Responsibility*, German original 1979) argues, in essence: *the greater the reach of technical possibilities, the greater the responsibility for their consequences.* The further digital systems reach into clinical action, the more important ethical reflection becomes – not as the opposite of innovation, but as its precondition.

```persona pat
You have a right to know who sees your data and how systems prepare decisions about your treatment. Responsibility stays with the people who treat you.
```

## Take-home messages

1. Early digitalization in medicine began mainly with **documentation, billing and administration**.
2. Clinical information systems emerged as **specialized solutions** for different data types and workflows.
3. Many of today's problems – silos, poor interoperability, low acceptance – have **grown historically and organizationally**.
4. Medical informatics is a **socio-technical field**: technology, processes, organization and responsibility belong together.
5. History explains the present and opens a view on the future of medicine.

## Self-check

```quiz
question: "What does PACS stand for?"
options:
  - "Patient Administration and Care System"
  - "Picture Archiving and Communication System"
  - "Process Analysis and Clinical Support"
answer: "Picture Archiving and Communication System"
explain: "PACS stores, archives and communicates medical image data."
```

```quiz
question: "Why were laboratories early adopters of digitalization?"
options:
  - "Because laboratories had the most staff"
  - "Because of high standardizability, structured data and clear process chains"
  - "Because laboratory results do not need to be documented"
answer: "Because of high standardizability, structured data and clear process chains"
```

```quiz
question: "Which statement about data silos fits best?"
options:
  - "Silos are a purely technical problem of missing interfaces"
  - "Silos have technical and organizational causes"
  - "Silos no longer exist since FHIR was introduced"
answer: "Silos have technical and organizational causes"
explain: "Separate databases and formats *and* separate responsibilities, documentation cultures and local priorities."
```

```quiz
question: "What are the three corners of the socio-technical triangle?"
options:
  - "Hardware, software, network"
  - "Technology, organization, processes"
  - "Doctors, nurses, administration"
answer: "Technology, organization, processes"
```

```quiz
question: "What did Joseph Weizenbaum particularly point out?"
options:
  - "Computers should take over as many medical decisions as possible"
  - "Not everything technically possible should be delegated to computers without reflection"
  - "Ethics only matters for artificial intelligence"
answer: "Not everything technically possible should be delegated to computers without reflection"
```

**Outlook:** the next unit covers national and international professional societies, the scientific culture and the professionalization of medical informatics.
