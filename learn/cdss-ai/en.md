---
title: "Clinical Decision Support & AI – from Rules to Learning Systems"
summary: "How do clinical data become a recommendation – and how do we check that it is reliable, useful and safe enough for patient care? Rules, scores and pathways, integration into the workstation, validation, real-world systems and regulation, worked through the case of Maria K."
duration_minutes: 75
level: "In-depth"
audiences: [med, cs, clin, tech, pat]
order: 7
builds_on: [specialized-systems, communication-standards]
course: his
lecture: 6
author: "Markus Wolfien"
objectives:
  - "Explain rule-based CDSS and distinguish rules, guidelines and pathways"
  - "Describe how CDSS are integrated into the HIS and the clinical workstation"
  - "Assess CDSS with suitable metrics – sensitivity, PPV, threshold, calibration"
  - "Compare rule-based and learning systems and recognise typical sources of error"
  - "Place CDSS within the basic logic of the MDR and the AI Act"
readings: [wong2021, adams2022, zech2018, agniel2018, finlayson2021, singer2016, evans2021, collins2024, vasey2022, vandersijs2006]
related_topics: [cdss, data-quality, privacy-ethics, fhir, ehr-cis]
source: "Lecture 6 “Clinical Decision Support & AI – from Rules to Learning Systems”, Health Information Systems (winter term 2026/27), Markus Wolfien, IMB & ZMI"
---

> **Guiding question:** How do clinical data become a recommendation – and how do we check that it is reliable, useful and safe enough for patient care?

So far our systems have **provided** information: the HIS and its subsystems ([[information-systems]]), the workstation, CPOE and workflows ([[specialized-systems]]), standards ([[communication-standards]]). Now they start to **derive suggestions** from it. We assume you know what AI is and how training, testing and generalisation work; here we move one level closer to the clinical system: how does a recommendation come about, how does it reach the user, how is it validated – and when does it become regulated software? In the accompanying exercise you build this chain yourself.

```persona med
You will read scores, receive warnings and see risks displayed. This module shows what lies behind “risk 78 %”, why many alerts are false alarms – and why the decision still stays with you.
```

```persona cs
IF–THEN rules with unit tests, logistic regression with a threshold, confusion matrix, calibration, data leakage, dataset shift: here your tools meet clinical reality – and the question of when code becomes a medical device.
```

```persona clin
Why does the system warn all the time – and sometimes not when it matters? You will learn which questions to ask a CDSS before it is introduced, and who should decide on escalation levels.
```

```persona tech
CDS Hooks, FHIR subscriptions, schedulers, knowledge bases with versioning and regression tests, monitoring after go-live: a CDSS is an operation, not just a model.
```

```persona pat
More and more software supports physicians in their decisions. This module shows how it works, how to check whether it really helps – and which rules apply to it in the EU.
```

```case
**Maria K., 62 years** – the patient from the data protection lecture. History: type 2 diabetes, chronic kidney disease. Now: shortness of breath, fever, suspected pneumonia.

**Vital signs:** temperature 39.1 °C · heart rate 112/min · respiratory rate 26/min · systolic BP 96 mmHg · SpO₂ 91 % (room air) · alert and oriented

**Lab:** creatinine 1.6 mg/dl · eGFR 38 · CRP 186 mg/l

The **HIS** sees many individual values, each in its own field. The **physician** sees a possibly critically ill patient. And a **CDSS**? That depends on how we build it. (Fictional values, chosen for teaching. Remember: **lactate has not been measured.**)
```

```reflect
question: "Warm-up: should the system warn? (A) “BP 96 mmHg – outside the normal range”, (B) “pneumonia + tachypnoea + hypotension → increased attention”, (C) “risk of deterioration: 78 %” or (D) nothing at all? All four can be implemented correctly – but are they equally sensible clinically?"
intro: "The four options stand for four kinds of decision support:"
answers:
  - "**A** is a simple **threshold check** – isolated, without context."
  - "**B** is a **rule** or **score** – it combines several values with knowledge."
  - "**C** is the output of a **learning model** – hard to interpret without a threshold and calibration."
  - "**D** – not warning – is also a **design decision**, and sometimes the right one."
```

## 1 · What is clinical decision support?

```timeline
title: "From data to action"
events:
  - when: "Data"
    what: "BP 96"
  - when: "Information"
    what: "hypotension"
  - when: "Knowledge"
    what: "hypotension + infection can be critical"
  - when: "Decision support"
    what: "“please review clinically”"
  - when: "Decision"
    what: "medical assessment – **a person decides here**"
  - when: "Action"
    what: "diagnostics / therapy"
```

> **Working definition:** a clinical decision support system links **patient-specific data** with **medical knowledge or a model** and uses them to provide **context-specific** support for clinical decisions. **A CDSS is not an automatic decision.**

### Two grids, one zoom

In the module [[specialized-systems]] we analysed systems with the grid USER, DATA, WORKFLOW, INTERFACES, RISK. A CDSS is a special information-processing workflow that we zoom into – the new grid does not replace the old one:

```include chain-en.svg
```

```match
question: "Which link of the CDSS chain is meant for Maria?"
options: ["DATA", "TRIGGER", "LOGIC", "OUTPUT", "ACTION", "FEEDBACK"]
items:
  - item: "Respiratory rate 26, BP 96, SpO₂ 91 %"
    answer: "DATA"
  - item: "New vital signs are documented."
    answer: "TRIGGER"
  - item: "A rule or a model assesses the values."
    answer: "LOGIC"
  - item: "A note appears at the workstation."
    answer: "OUTPUT"
  - item: "The physician reviews Maria clinically."
    answer: "ACTION"
  - item: "The physician confirms or dismisses the note."
    answer: "FEEDBACK"
```

### What kinds of decision support are there?

| Kind | Example | Knowledge |
|---|---|---|
| Reminder | “check thrombosis prophylaxis” | explicit – formulated by people |
| Plausibility check | “dose too high” | explicit |
| Rule | IF A AND B THEN C | explicit |
| Score | qSOFA 2 points, NEWS2 12 points | explicit |
| Guideline-based | “matches recommendation X” | explicit |
| Predictive model | “risk 78 %” | learned – derived from data |
| Generative / agentic | summarise the case, prepare options | learned |

**Not all of this is AI.** Many established CDSS in hospitals are rule-based – and that is no flaw. More in the topic [[topic:cdss]].

## 2 · Rules, guidelines, pathways

The simplest form of a CDSS is an **IF–THEN rule** (simplified for teaching, not a clinical protocol):

```text
IF   suspected infection
AND  respiratory_rate >= 22
AND  systolic_bp <= 100
THEN “clinical re-evaluation”

# Python bridge
if respiratory_rate >= 22 and systolic_bp <= 100:
    create_alert("clinical re-evaluation")
```

At its core the rule is **qSOFA** from the Sepsis-3 definition [@singer2016]: respiratory rate ≥ 22/min, systolic blood pressure ≤ 100 mmHg, altered mentation – one point each, 2 or more points is positive. The **NEWS2** (Royal College of Physicians) scores seven parameters.

```quiz
question: "How many qSOFA points does Maria have?"
options: ["0", "1", "2", "3"]
answer: "2"
shuffle: false  # options in a natural order
explain: "Respiratory rate 26 ≥ 22 → 1, BP 96 ≤ 100 → 1, alert and oriented → 0. So 2 of 3 – positive."
```

```quiz
question: "And in NEWS2 (room air)? Respiratory rate 26 → 3, SpO₂ 91 % → 3, BP 96 → 2, heart rate 112 → 2, temperature 39.1 °C → 2, alert and on room air → 0."
options: ["6", "9", "12", "15"]
answer: "12"
shuffle: false  # options in a natural order
explain: "12 points – high urgency."
```

```quiz
question: "Same patient, different scores. What follows from this?"
options:
  - "One of the two scores has been calculated wrongly."
  - "A score can only be interpreted if it is clear which outcome it is meant to predict."
  - "You should always use the score with the higher number of points."
answer: "A score can only be interpreted if it is clear which outcome it is meant to predict."
explain: "qSOFA predicts poor outcomes in suspected infection, NEWS2 general clinical deterioration. The Surviving Sepsis Campaign 2021 recommends against using qSOFA, compared with SIRS, NEWS or MEWS, as a single screening tool for sepsis [@evans2021] – in the exercise you will see: high specificity, low sensitivity."
```

### Building blocks of a rule – and its context

A rule consists of a **variable** (`egfr`), an **operator** (`<`), a **threshold** (`60`), **logic** (AND / OR / NOT) and an **action** (`create_alert()`). Several rules are often maintained as a **decision table** – here for a renally excreted antibiotic (simplified for teaching; the real limits are in the summary of product characteristics):

| eGFR (ml/min/1.73 m²) | Situation | Output |
|---|---|---|
| ≥ 60 | standard dose | no alert |
| 30–59 | adjust dose | note |
| 15–29 | reduce considerably | warning |
| < 15 / dialysis | only after consultation | hard stop with reason |

```quiz
question: "Maria has an eGFR of 38. What does the decision table output?"
options: ["no alert", "note: adjust dose", "warning: reduce considerably", "hard stop"]
answer: "note: adjust dose"
shuffle: false  # options in a natural order
```

```reflect
question: "And suddenly the rule needs more. Which questions does it have to answer before it runs safely for Maria?"
answers:
  - "**Which value?** Today's creatinine or the one from three days ago?"
  - "**Acute situation?** In acute kidney injury, the eGFR formula is unreliable."
  - "**Planned?** Is a contrast CT planned?"
  - "**Missing value?** What does the rule do if there is no creatinine?"
  - "Remember: **rule = data + operators + action – plus context.**"
```

**Drug checking in CPOE** is the most common CDSS in hospitals: when an order is signed, it is checked against the patient context (allergies, eGFR 38, metformin, ramipril, age 62) and a knowledge base (interactions, contraindications, dosing rules by kidney function) – in Germany typically a commercially maintained drug database. The CDSS sits **between prescribing and execution**. From [[specialized-systems]] you know the downside: 49–96 % of drug warnings are overridden [@vandersijs2006]. Quality depends less on the technology than on the knowledge base and the grading.

### Rule set ≠ guideline: the problem of formalisation

```match
question: "Guideline or executable rule?"
options: ["Guideline", "Rule"]
items:
  - item: "narrative evidence"
    answer: "Guideline"
  - item: "grades of recommendation and exceptions"
    answer: "Guideline"
  - item: "room for clinical interpretation"
    answer: "Guideline"
  - item: "formal and unambiguous"
    answer: "Rule"
  - item: "machine-readable"
    answer: "Rule"
  - item: "testable"
    answer: "Rule"
explain: "For a system to execute a guideline, it has to be **formalised** – translation work with room for interpretation."
```

There are dedicated languages for executable knowledge: **Arden Syntax** is the classic (an HL7 standard since the 1990s), with *medical logic modules* made of trigger, logic and action – almost our CDSS chain. More important today is **CQL** (*Clinical Quality Language*, HL7): human-readable, machine-executable, used for CDS and quality measures, and closely tied to [[topic:fhir]].

### From guideline to clinical pathway

A **clinical pathway** translates a guideline into a local treatment path – across four levels: the **narrative guideline** (e.g. the German S3 guideline on community-acquired pneumonia), **decision points** (severity? risk?), **executable rules** (e.g. using the CRB-65 score) and a **workflow** with tasks, appointments and responsibilities in the HIS.

```timeline
title: "Pneumonia pathway for Maria (simplified)"
events:
  - when: "1"
    what: "Suspicion"
  - when: "2"
    what: "Severity"
  - when: "3"
    what: "Diagnostics"
  - when: "4"
    what: "Therapy"
  - when: "5"
    what: "Re-evaluation"
```

```reflect
question: "What does this mean for implementation? Which questions does the team have to settle before the pathway runs in the HIS?"
answers:
  - "What does “severe” mean – which score, which cut-off?"
  - "Which value, how recent?"
  - "What happens with a missing value?"
  - "What about a justified deviation – and how is it documented?"
  - "A pathway is **guideline + local process**. Each level loses nuance – and gains executability."
```

## 3 · Integration into the HIS and the workstation

A CDSS does not float in a vacuum: it needs data from HIS/ADT, PDMS, LIS and CPOE, has to know the patient context, links it with a knowledge base or model in a **CDSS engine** and delivers an output to the workstation. What matters is the **trigger** – when the system runs. The abstract triggers of our chain have real interoperability standards (see [[communication-standards]]):

| Trigger | Example for Maria | Standard / technology |
|---|---|---|
| user-triggered | the physician opens Maria's record | CDS Hooks: `patient-view` |
| order-triggered | an antibiotic is selected or signed | CDS Hooks: `order-select` / `order-sign` |
| event-triggered | a new vital sign or lab value | HL7 v2 message, FHIR subscription |
| time-triggered | re-evaluation after 6 hours | scheduler, task in the workflow |

### The “five rights” and the escalation level

The standard framework for integration is the **five rights of CDS** (Osheroff et al. 2012): the right **information** to the right **person** in the right **format** through the right **channel** at the right **time**.

```match
question: "Which “right” is meant for Maria's dosing warning?"
options: ["Information", "Person", "Format", "Channel", "Time"]
items:
  - item: "eGFR 38 → adjust dose"
    answer: "Information"
  - item: "the prescribing physician – not everyone"
    answer: "Person"
  - item: "a note with a reason and a dose suggestion"
    answer: "Format"
  - item: "in the CPOE dialogue, not by email"
    answer: "Channel"
  - item: "when selecting, not in the discharge letter"
    answer: "Time"
```

Then the **escalation level**: *info* (“creatinine raised.”), *warning* (“check dose adjustment.”), *recommendation* (“based on X and Y, consider dose Z.”), *hard stop* (the order cannot be completed). CDS Hooks represents this with the card indicator `info`, `warning`, `critical`. **Same logic, different effect:** the escalation level is a **governance decision** (e.g. a drug and therapeutics committee, a CDS committee with clinicians, pharmacy and informatics), not just a technical one.

```match
question: "Warm-up: when and how to intervene? Which trigger and which level fit?"
options:
  - "order-select · note/warning with a dose suggestion"
  - "event (new lab result) · warning to the responsible team"
  - "order-sign · hard stop, override only with a reason"
  - "patient-view or admission workflow · info/reminder"
items:
  - item: "A renally excreted antibiotic is selected for Maria, eGFR 38."
    answer: "order-select · note/warning with a dose suggestion"
  - item: "A new lactate value of 4.2 mmol/l arrives for Maria."
    answer: "event (new lab result) · warning to the responsible team"
  - item: "Penicillin allergy with anaphylaxis documented – amoxicillin is signed."
    answer: "order-sign · hard stop, override only with a reason"
  - item: "No thrombosis prophylaxis has been ordered on admission."
    answer: "patient-view or admission workflow · info/reminder"
explain: "In the module [[specialized-systems]] it was about the level – now it is also about logic and timing. A lactate above 4 mmol/l is clinically relevant; the warning belongs with the responsible team, not with everyone."
```

## 4 · Quality and validation

A CDSS can be wrong in **two ways**:

| | Patient deteriorates | stays stable |
|---|---|---|
| **Alert** | **TP** true positive – alert, and Maria really becomes critical | **FP** false positive – unnecessary interruption, alarm fatigue |
| **No alert** | **FN** false negative – critical course missed | **TN** true negative – no alert, stable: the normal case |

```reflect
question: "In screening for deterioration: which error would you rather accept – and does that still hold with 30 false alarms per shift?"
answers:
  - "The first answer is usually: rather a false positive than a missed critical course."
  - "With 30 false alarms per shift this flips: alarm fatigue means real alarms get missed too."
  - "There is **no blanket answer** – it depends on the consequences of missing a case and on resources. **Every decision for fewer FN is paid for with more FP – and vice versa.**"
```

### Sensitivity, specificity, PPV in 100 patients

20 of 100 patients deteriorate. The system detects 18 (TP), misses 2 (FN), alerts for 8 stable patients (FP) and leaves 72 alone (TN).

```match
question: "Match the metric, the question and the result."
options: ["Sensitivity = 18/20 = 90 %", "Specificity = 72/80 = 90 %", "PPV = 18/26 = 69 %"]
items:
  - item: "How many of the sick does the system find? TP / (TP + FN)"
    answer: "Sensitivity = 18/20 = 90 %"
  - item: "How many of the healthy does it leave alone? TN / (TN + FP)"
    answer: "Specificity = 72/80 = 90 %"
  - item: "How often is an alert right? TP / (TP + FP)"
    answer: "PPV = 18/26 = 69 %"
explain: "On the ward, the **PPV** is what counts: how many alerts are worth it?"
```

```quiz
question: "Same system (sensitivity 90 %, specificity 90 %), but only 2 % prevalence: 1,000 patients, 20 deteriorate. What is the PPV?"
options: ["about 16 %", "about 50 %", "about 69 %", "about 90 %"]
answer: "about 16 %"
shuffle: false  # options in a natural order
explain: "18 correct alerts (90 % of 20) and 98 false alarms (10 % of 980): 18 / 116 ≈ 16 %. Five out of six alerts are false alarms. For rare events, most alerts are false alarms – **alert fatigue is also mathematics.** That is why a CDSS always has to be assessed in its target population."
```

### The threshold changes the system

A model delivers a risk between 0 and 1 – only the **threshold** turns it into an alert. The figures come from the synthetic exercise data set (hospital A, test data, n = 600, logistic regression):

| Threshold | Character | Sensitivity | PPV | Alerts per 100 patients |
|---|---|---|---|---|
| 0.2 | many alerts, little missed | 68 % | 39 % | 30 |
| 0.5 | compromise | 27 % | 60 % | 8 |
| 0.8 | few alerts, much missed | 7 % | 70 % | 2 |

```quiz
question: "Who should decide on the threshold?"
options:
  - "The data scientists – it is a purely mathematical optimisation."
  - "Clinicians, nursing, quality management and informatics together – it depends on how many alerts a ward can handle and what a missed case costs."
  - "The vendor – it is fixed in the product."
answer: "Clinicians, nursing, quality management and informatics together – it depends on how many alerts a ward can handle and what a missed case costs."
explain: "The threshold is not a purely mathematical decision but a clinical and organisational one. This is exactly what you practise in the exercise."
```

### Discrimination and calibration

```match
question: "Discrimination or calibration?"
options: ["Discrimination (AUC)", "Calibration"]
items:
  - item: "Does the model rank patients with the event higher than those without?"
    answer: "Discrimination (AUC)"
  - item: "Does a displayed risk of 30 % really mean that 3 in 10 such patients have the event?"
    answer: "Calibration"
  - item: "measures the ranking"
    answer: "Discrimination (AUC)"
  - item: "compares predicted with observed risks"
    answer: "Calibration"
explain: "In the exercise data, the model trained in hospital A has an AUC of 0.80 in both A and B – but in B it predicts 19.7 % on average while only 8.6 % is observed. **The ranking is right, the number is not.** For a physician reading “40 %”, that is a big difference."
```

### A rule can be wrong too

Validation is not just an ML topic. Rule-based CDSS are validated **like software – plus maintenance of the knowledge base**:

```text
# reference cases
assert cds_alert(rr=26, bp=96) == True
assert cds_alert(rr=18, bp=125) == False
# boundary value
assert cds_alert(rr=22, bp=100) == True
```

**Regression test:** if I change rule B, rule A must not silently break – all tests run again with every change to the knowledge base.

```match
question: "At which level is the rule checked?"
options: ["Logic correct?", "Knowledge correct?", "Knowledge up to date?", "Useful in the workflow?"]
items:
  - item: "unit tests and reference cases"
    answer: "Logic correct?"
  - item: "comparison with guideline, product information, score definition"
    answer: "Knowledge correct?"
  - item: "versioning, update process, named owners"
    answer: "Knowledge up to date?"
  - item: "override rate, alert frequency, acceptance"
    answer: "Useful in the workflow?"
```

### From internal to external validation – and beyond

You know generalisation from the introduction to AI; clinically it becomes a sequence of stages. Most published models never get beyond stage 2.

```timeline
title: "Stages of validation (example)"
events:
  - when: "1 · Training"
    what: "e.g. Dresden"
  - when: "2 · Internal validation"
    what: "Dresden, new patients"
  - when: "3 · External validation"
    what: "another hospital, e.g. Leipzig"
  - when: "4 · Prospective evaluation"
    what: "in the real workflow"
  - when: "5 · Clinical benefit"
    what: "Does care improve?"
```

```match
question: "Which reporting guideline is for what?"
options: ["TRIPOD+AI (2024)", "DECIDE-AI (2022)", "CONSORT-AI (2020)"]
items:
  - item: "development and validation of prediction models, including machine learning"
    answer: "TRIPOD+AI (2024)"
  - item: "early clinical evaluation of AI-based decision support"
    answer: "DECIDE-AI (2022)"
  - item: "randomised trials with an AI intervention"
    answer: "CONSORT-AI (2020)"
explain: "See [@collins2024] and [@vasey2022]."
```

**Good performance is not yet clinical benefit.** Four stages, each needing a different study: **model performance** (does the model detect patterns? AUC, sensitivity, PPV), **clinical validity** (is the association plausible – right target, no leakage?), **clinical utility** (does it change decisions sensibly – workflow, acceptance, response time?) and **patient outcome** (are patients better off – mortality, complications, length of stay?). Evidence has levels too: **model evaluation ≠ impact evaluation ≠ causal evidence.** A model can be statistically excellent and clinically useless. See also [[topic:data-quality]].

## 5 · What happens with real systems

| | Rule | Machine learning |
|---|---|---|
| Decision function | a person defines f(x): `RR >= 22 AND BP <= 100` | a model learns f(x) from examples: `model.fit(X, y)` |
| Knowledge | explicit | learned from data |
| Traceability | mostly high | variable |
| Adaptation | manual, versioned | retraining, recalibration |
| Data needed | little | a lot |
| outside known cases | rigid | more flexible, but uncertain |

Not “old versus modern” but different tools – **many good systems are hybrid**.

```match
question: "Warm-up: rule, ML or both?"
options: ["Rule", "ML", "Combination"]
items:
  - item: "check a known drug allergy"
    answer: "Rule"
  - item: "detect a lung nodule on CT"
    answer: "ML"
  - item: "monitor the maximum daily dose"
    answer: "Rule"
  - item: "risk of deterioration from 40 time-dependent variables"
    answer: "Combination"
explain: "Allergy and maximum dose are unambiguous, explicit knowledge. A nodule on CT is high-dimensional input that is hard to express as a rule. For the deterioration risk, a model usually provides the risk while rules handle plausibility, hard exclusions and the alert logic – exactly how you build it in the exercise."
```

### Widely implemented – does that make it validated?

```case
**Epic Sepsis Model:** a proprietary sepsis prediction model from a large EHR vendor, in use at hundreds of US hospitals. External validation at Michigan Medicine: 38,455 hospitalisations, 7 % with sepsis [@wong2021].
```

```match
question: "What did the external validation show?"
options: ["0.63", "18 %", "67 %"]
items:
  - item: "AUC in the external validation"
    answer: "0.63"
  - item: "share of all hospitalisations that triggered an alert"
    answer: "18 %"
  - item: "share of sepsis cases that were nevertheless missed"
    answer: "67 %"
explain: "**Wide use is not evidence.** A vendor's internal figures do not replace independent external validation. Everything from the validation section comes together here: discrimination, PPV, alert burden, external validation."
```

**TREWS** is the counterexample: an ML-based early warning system studied prospectively in real operation at five hospitals – 590,736 monitored patients, analysis of 6,877 sepsis cases in which the alert fired before antibiotics were given [@adams2022].

```quiz
question: "When the TREWS alert was confirmed by a physician within 3 hours, adjusted in-hospital mortality was 3.3 percentage points lower. Which wording is correct?"
options:
  - "“TREWS reduced mortality by 3.3 percentage points.”"
  - "“Prompt confirmation of the TREWS alert was associated with 3.3 percentage points lower mortality.”"
  - "“TREWS is causally effective because 590,736 patients were studied.”"
answer: "“Prompt confirmation of the TREWS alert was associated with 3.3 percentage points lower mortality.”"
explain: "A **cohort study** shows an association, not a causal effect. TREWS sits between model evaluation and causal evidence (RCT): at impact evaluation."
```

### Imaging: what has the model actually learned?

Zech et al. trained pneumonia classifiers (CNNs) on 158,323 chest X-rays from three hospital systems [@zech2018]. The CNN could recognise the **hospital of origin** almost perfectly – 99.95 % for the NIH images. Because pneumonia prevalence differed enormously between hospitals (34 % versus around 1 %), **simply sorting by hospital achieved an AUC of 0.86** – without looking at the lung.

```quiz
question: "What is this phenomenon called?"
options: ["Overfitting to noise", "Shortcut learning", "Automation bias"]
answer: "Shortcut learning"
explain: "The model uses features that correlate with the label – device, markers, hospital – but not the disease itself. **The model learns something – but maybe not what we think.** Consequence: good in its own hospital, clearly worse in the next. A form of dataset shift."
```

### Six well-known sources of error

```match
question: "Which source of error is it?"
options: ["Sampling bias", "Label bias", "Data leakage", "Missingness", "Dataset shift", "Automation bias"]
items:
  - item: "trained at a university hospital, used in a district hospital"
    answer: "Sampling bias"
  - item: "“sepsis” is defined as a billing code instead of the clinical course"
    answer: "Label bias"
  - item: "“antibiotic given” is used as a predictor"
    answer: "Data leakage"
  - item: "for the model, “lactate not measured” means: probably healthy"
    answer: "Missingness"
  - item: "hospital B has a different population, different devices, different processes and a different prevalence"
    answer: "Dataset shift"
  - item: "“The system didn't warn, so everything is fine.”"
    answer: "Automation bias"
explain: "Real evidence: the mere fact that a lab test was ordered was associated with survival for 86 % of 272 tests [@agniel2018] – a model can learn documentation behaviour instead of disease. On dataset shift, see [@finlayson2021]. You will meet leakage and missingness again in the exercise – remember Maria's missing lactate."
```

### When a model seems to keep working

The most dangerous scenario is not a crash but a model that **seems to keep working** (illustrative values): in 2026 AUC 0.88, calibrated, PPV 40 %; in 2028 AUC 0.87 – but the population has changed, risks are overestimated, and the PPV is 22 %.

```reflect
question: "Is the model still good in 2028? What should be monitored after go-live?"
answers:
  - "**No** – the AUC is almost the same, but the risks are no longer right, the PPV falls and the alert burden rises."
  - "**Performance:** sensitivity and PPV against later outcomes"
  - "**Calibration:** predicted vs. observed"
  - "**Data drift:** distributions of the input data"
  - "**Alert frequency** (per patient and shift) and **override rate**"
  - "**Outcomes:** are patients better off?"
  - "A CDSS is not finished after go-live – **FEEDBACK is an ongoing process.**"
```

## 6 · Regulation: MDR and AI Act

Regulation is not a legal appendix but the logical last question: who decides what evidence, quality assurance and oversight are needed? The decisive question is **not “Is it AI?” but: what is the software intended for?** – the **intended purpose** set by the manufacturer (see also [[topic:privacy-ethics]]).

```match
question: "Medical device software (MDSW) or not?"
options: ["no medical purpose", "pure information management – usually not a medical device", "MDSW if it has a medical intended purpose"]
items:
  - item: "appointment scheduling, billing"
    answer: "no medical purpose"
  - item: "displaying the medication list"
    answer: "pure information management – usually not a medical device"
  - item: "dose checking, risk score, sepsis alert"
    answer: "MDSW if it has a medical intended purpose"
```

For MDSW, **rule 11 of the MDR** usually applies (Annex VIII; see MDCG 2019-11): **class IIa** by default; **IIb** if wrong information could lead to serious deterioration or a surgical intervention; **III** if it could lead to death or irreversible deterioration. Software for monitoring vital parameters where variations could result in immediate danger is IIb; all other software is class I. From class IIa onwards, a **notified body** is involved. **Function + purpose + potential harm determine the classification.**

```match
question: "Which class under MDR rule 11?"
options: ["IIa", "IIb", "III"]
items:
  - item: "default case: software provides information used for diagnostic or therapeutic decisions"
    answer: "IIa"
  - item: "wrong information could lead to serious deterioration or a surgical intervention"
    answer: "IIb"
  - item: "wrong information could lead to death or irreversible deterioration"
    answer: "III"
```

**The MDR and the AI Act are two axes.** The MDR asks about the **medical purpose** and the danger from wrong information (→ class, conformity assessment, clinical evaluation). The AI Act asks whether it is an **AI system** and which **risk category** it falls into (→ among other things data quality, documentation, human oversight). AI in medical devices that need a notified body counts as high-risk AI (Art. 6(1)).

```timeline
title: "AI Act timeline (as of November 2026, amended by the Digital Omnibus on AI)"
events:
  - when: "1 Aug 2024"
    what: "entry into force"
  - when: "2 Feb 2025"
    what: "prohibitions"
  - when: "2 Aug 2025"
    what: "obligations for general-purpose AI models"
  - when: "2 Aug 2026"
    what: "general application"
  - when: "2 Dec 2027"
    what: "high-risk AI under Annex III"
  - when: "2 Aug 2028"
    what: "high-risk AI under Annex I – including medical devices"
```

```quiz
question: "An AI-based medical device needs a notified body. What applies?"
options:
  - "Only the MDR – the AI Act does not apply to medical devices."
  - "Only the AI Act – it replaces the MDR for AI."
  - "Both: the MDR obligations unchanged, the AI Act's high-risk obligations from 2 August 2028."
answer: "Both: the MDR obligations unchanged, the AI Act's high-risk obligations from 2 August 2028."
explain: "**The MDR asks about the medical product. The AI Act asks about the AI risk.**"
```

### In-house manufacture – and the CDSS from the exercise

Particularly relevant for university hospitals: under **Art. 5(5) MDR**, health institutions may manufacture devices themselves and use them internally – among other conditions, if they are not transferred to another legal entity, an appropriate quality management system is in place, it is justified that no equivalent device on the market meets the need, the general safety and performance requirements are met, and there is documentation, a public declaration and a review of experience.

```reflect
question: "In the exercise you build a CDSS in a Jupyter notebook. Is it a medical device? And when would the question have to be asked again?"
answers:
  - "**No** – the notebook serves teaching and research only and has **no medical intended purpose**. Writing a logistic regression does not make a medical device."
  - "**As soon as** software is intended by its manufacturer for a medical purpose, its regulatory status must be clarified – **before** it is used clinically."
  - "Many CDSS are built in-house: in-house manufacture is **not an exception from quality but a framework of its own for it**."
```

## Synthesis: a CDSS is more than an algorithm

```match
question: "Which check question belongs to which link of the chain?"
options: ["DATA", "TRIGGER", "LOGIC", "OUTPUT", "ACTION", "FEEDBACK"]
items:
  - item: "Are the data correct, up to date and available at that moment?"
    answer: "DATA"
  - item: "Does the system become active at the right moment?"
    answer: "TRIGGER"
  - item: "Is the rule or model valid and calibrated?"
    answer: "LOGIC"
  - item: "Is the recommendation understandable and correctly graded?"
    answer: "OUTPUT"
  - item: "Can the user respond sensibly?"
    answer: "ACTION"
  - item: "Do we know whether the system helped?"
    answer: "FEEDBACK"
```

> **An algorithm only becomes a clinical decision support system through data, workflow, validation, user interaction and governance.**

## Take-home messages

1. **A CDSS links patient data with knowledge or a model.** Not everything is AI – many established clinical CDSS are rule-based.
2. **Integration determines the effect:** right information, person, format, channel, time.
3. **Validation means more than AUC:** PPV, threshold, calibration, external and prospective evaluation.
4. **Real systems fail on data and operations:** leakage, shift, missingness, automation bias – monitoring is a must.
5. **Intended purpose and risk determine regulation:** MDR rule 11; AI Act high-risk obligations for medical devices from 2 August 2028.

## Outlook: the exercise

In the exercise you build the chain yourself: a qSOFA-like **rule** with `assert` tests, a **logistic regression** with `predict_proba()`, choosing a **threshold** under a realistic alert limit, the **confusion matrix**, a suspiciously good variable (**leakage**) and missing lactate (**missingness**), the external test in **hospital B** with a calibration curve – and finally the CDSS chain and the intended purpose for your system. The data set is fully synthetic; the outcome is a deterioration within 6 hours defined for teaching, not a sepsis diagnosis.

## Self-test

```quiz
question: "A system has 90 % sensitivity and 90 % specificity. Why can most alerts still be false alarms?"
options:
  - "Because the sensitivity was calculated wrongly"
  - "Because the PPV depends on prevalence – for rare events, false alarms dominate"
  - "Because specificity only applies to healthy patients"
answer: "Because the PPV depends on prevalence – for rare events, false alarms dominate"
```

```quiz
question: "In hospital B a model has the same AUC as in hospital A but overestimates every risk. What is the problem?"
options: ["discrimination", "calibration", "sensitivity"]
answer: "calibration"
```

```quiz
question: "What decides whether a CDSS software is a medical device?"
options:
  - "whether it uses AI"
  - "its intended purpose set by the manufacturer"
  - "how many patients use it"
answer: "its intended purpose set by the manufacturer"
```
