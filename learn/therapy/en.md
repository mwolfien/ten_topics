---
title: "Therapy, Guidelines and Patient-Centred Care"
summary: "How an abnormal finding becomes a good, patient-centred therapy decision – using lung cancer as the example, from screening via the tumour board to therapy over time."
duration_minutes: 40
level: "Foundations"
audiences: [med, cs, clin, tech, pat]
order: 2
builds_on: [history]
course: "Medicine for Computer Scientists"
author: "Markus Wolfien"
objectives:
  - "Name basic forms of therapy and explain them with examples"
  - "Distinguish therapy goals: cure, control, relieve, accompany"
  - "Explain why therapy is always a weighing of benefits and risks"
  - "Describe the principle of shared decision making"
  - "Explain why adherence, everyday life and the patient's perspective matter"
  - "Place PROs and PROMs as instruments for monitoring therapy"
  - "Understand guidelines as a framework for decisions and explain their limits"
readings: [elwyn2012, basch2016, dekoning2020, gladstone2025, hassan2024]
related_topics: [cdss, ehr-cis, fhir, data-quality, visualizations]
source: "Lecture 7 “Therapy, Guidelines and Patient-Centred Care”, Medicine for Computer Scientists (summer term 2026), Markus Wolfien, IMB & ZMI"
---

> **Guiding question:** How does an abnormal finding become a good, patient-centred therapy decision?

When we talk about therapy, many people first think of drugs or surgery. Medically, though, therapy starts earlier – with the question of **which goal** is being pursued. Therapy is therefore always a decision process, not just the application of a measure.

In the module [[history]] you saw that digitalization is never just a technical project and that information in hospitals is spread across many systems. In this module we follow one patient through care and see exactly where these data have to come together for a therapy decision.

```persona med
You learn the basic structure of every therapy decision here: goal, options, weighing benefits and risks, and deciding together. It applies far beyond oncology.
```

```persona cs
You don't need to know every cancer therapy. What matters is which information a therapy decision needs, where it is produced – and why it is so hard to bring together. That is exactly where you will work later.
```

```persona clin
This module connects guidelines, tumour boards and shared decision making with the question of how digital tools can make the patient's perspective visible over time.
```

```persona tech
A care pathway is a distributed process with many data sources, formats and people responsible. Here you see the clinical logic behind the data flows.
```

```persona pat
In a therapy decision, what counts is not only the test result but also what matters to you. This module shows how doctors and patients can decide together.
```

```case
A **62-year-old smoker** (for more than 25 years) comes to his family doctor for a check-up. He has no clear symptoms but an increased risk of lung cancer. They discuss lung cancer screening with **low-dose CT**, which is offered in Germany from April 2026.
```

## 1 · Therapy starts with a goal

Diseases have courses – therapy is a **deliberate intervention** meant to change that course.

> A medical measure is not automatically sensible just because it is possible.

Three questions come before every therapy decision:

1. **What should be achieved?** Cure, control, symptom relief, quality of life, support?
2. **Which measure can achieve this goal?** Drug, surgery, intervention, combination, supportive care?
3. **Does the measure fit the patient?** Condition, comorbidities, preferences, everyday life, risks?

### Forms of therapy

| Form of therapy | Basic idea | Examples |
|---|---|---|
| Drug therapy | active substances influence biological processes | antibiotics, painkillers, chemotherapy, immunotherapy |
| Interventional | targeted procedure, often minimally invasive | catheter procedures, endoscopy, bronchoscopy, biopsy |
| Surgical | operation to remove, reconstruct or correct | tumour surgery, appendectomy, joint replacement |

Along a care pathway these forms are often combined or used one after another. Supportive and palliative measures – pain management, control of breathlessness, nutrition, psycho-oncology – accompany many phases of treatment and are not only relevant at the end of life.

```match
question: "Match them: which form of therapy is it?"
options: ["drug therapy", "interventional", "surgical"]
items:
  - item: "Bronchoscopy with tissue sampling"
    answer: "interventional"
  - item: "Immunotherapy"
    answer: "drug therapy"
  - item: "Appendectomy"
    answer: "surgical"
  - item: "Antibiotic for a bacterial infection"
    answer: "drug therapy"
  - item: "Catheter procedure"
    answer: "interventional"
  - item: "Joint replacement"
    answer: "surgical"
```

### Therapy goals

A common mistake is to equate therapy with cure. Cure is a central goal, but not the only one:

- **Cure:** remove the disease or achieve long-term freedom from disease – e.g. curative surgery, an antibiotic for a bacterial infection.
- **Control:** slow progression, keep the disease stable.
- **Relieve:** reduce symptoms and burden – e.g. pain management, treating breathlessness, anti-emetics for nausea.
- **Accompany:** support in living with the disease, its course and limitations – e.g. follow-up care, palliative care, psychosocial support.

These goals are no less medical – just different. The diagnosis "lung cancer" describes the disease, but it does not determine the therapy goal on its own:

```match
question: "Same diagnosis, different goals: which therapy goal comes first in each case?"
options: ["cure", "control", "relieve", "accompany"]
items:
  - item: "Small, localized tumour – surgery or local therapy"
    answer: "cure"
  - item: "Metastatic disease – systemic, targeted or immunotherapy"
    answer: "control"
  - item: "Severe breathlessness or pain – supportive and palliative measures"
    answer: "relieve"
  - item: "Chronic or palliative course – continuous care, symptom monitoring, follow-up"
    answer: "accompany"
explain: "In metastatic disease the aim is mainly to prolong life and control the tumour. In locally advanced disease a combined strategy can also be curative. What decides is the stage, general condition, available therapies and the patient's goals."
```

### Early detection changes what is possible

Screening is not a therapy in itself – but it can influence which therapy goals are realistic later. Many lung cancers cause few symptoms for a long time.

| Path A: early detection | Path B: late diagnosis |
|---|---|
| screening → early finding | symptoms → advanced disease |
| more often localized and potentially operable | more often metastatic, higher symptom burden |
| local treatment option | systemic therapy, palliative care |
| curative goal possible | control, relief, support |

The NELSON trial, for example, showed that CT screening in high-risk groups can reduce lung cancer mortality [@dekoning2020].

```quiz
question: "A palliative pain therapy does not shrink the tumour but clearly reduces the pain. Is it successful?"
options:
  - "No, because the tumour was not treated"
  - "Yes, because the success of a therapy depends on its goal"
  - "That can only be said after imaging"
answer: "Yes, because the success of a therapy depends on its goal"
explain: "**Success depends on the goal.** Cure: no detectable disease. Control: stable imaging, delayed progression. Relief: less pain, breathlessness, nausea. Support: better quality of life, security, orientation."
```

**Interim conclusion:** good therapy does not start with choosing a measure but with **clarifying the goal**. So far our patient only has an increased risk – before therapy can be discussed, finding, diagnosis, stage and the patient's goal must be clarified.

## 2 · From finding to therapy option

```case
The low-dose CT shows a **suspicious round lesion**. For the patient this is very stressful. Medically, though, an abnormal finding is only a hint – not yet a diagnosis, let alone a therapy decision.
```

```timeline
title: "The diagnostic chain in lung cancer"
events:
  - when: "Family doctor"
    what: "risk assessment, counselling, referral"
  - when: "Radiology"
    what: "low-dose CT, reporting, follow-up assessment"
  - when: "Pulmonology"
    what: "clinical assessment, lung function"
  - when: "Interventional diagnostics"
    what: "bronchoscopy, biopsy, tissue sampling"
  - when: "Pathology"
    what: "tumour entity, histology, biomarkers"
  - when: "Molecular diagnostics"
    what: "mutations, fusions, expression markers, therapeutic targets"
  - when: "Oncology / tumour board / MTB"
    what: "therapy options, guidelines, trials, individual decision"
```

Medical decisions are made **by division of labour**: every station produces its own information – and often stores it in its own system. Here you meet the specialized systems and silos from [[history]] again: images in the PACS, lab values in the LIS, results and documentation in the HIS, plus pathology and molecular reports, often as free text or PDF.

```match
question: "Which data does the therapy decision need? Match the examples to the data domain."
options: ["imaging", "pathology", "molecular data", "laboratory values", "medication data", "patient perspective"]
items:
  - item: "Tumour size, location, metastases"
    answer: "imaging"
  - item: "Tumour entity, histology, differentiation"
    answer: "pathology"
  - item: "Mutations, biomarkers, therapeutic targets"
    answer: "molecular data"
  - item: "Organ function, inflammation, blood count"
    answer: "laboratory values"
  - item: "Long-term medication, allergies, interactions"
    answer: "medication data"
  - item: "Preferences, burden, quality of life"
    answer: "patient perspective"
explain: "Add clinical data (symptoms, general condition, comorbidities) and care data (previous treatments, appointments, available trials). **Therapy decisions are data-rich – but data must be available, understandable and linkable.**"
```

**Typical challenges:** data sit in different institutions; images, free text and structured data are separate; reports are not always machine-readable; molecular findings need clinical interpretation; information from patients is often not captured systematically.

**What medical informatics contributes:** data integration and structured documentation, interoperability, visualization of the course of treatment, decision support and the integration of PROs/PROMs.

```persona cs
Every row of the exercise above is a separate data source with its own format. Preparing a tumour board is therefore a real integration task – exactly where standards such as FHIR come in.
```

### Drugs: effects, side effects, interactions

Drugs don't act in isolation but within a whole biological system.

| Form of therapy in oncology | Basic principle |
|---|---|
| Chemotherapy | mainly attacks rapidly dividing cells |
| Immunotherapy | influences the body's own immune response against tumour cells |
| Targeted therapy | acts against specific molecular alterations |
| Supportive medication | treats symptoms or side effects |

```match
question: "Intended effect, side effect or interaction?"
options: ["intended effect", "side effect", "interaction"]
items:
  - item: "Slowing tumour growth"
    answer: "intended effect"
  - item: "Fatigue"
    answer: "side effect"
  - item: "Influence on other drugs"
    answer: "interaction"
  - item: "Reducing pain"
    answer: "intended effect"
  - item: "Risk of infection"
    answer: "side effect"
  - item: "Changed effect when kidney function is impaired"
    answer: "interaction"
explain: "The intended effect is only part of the overall biological effect. That is why every drug therapy needs monitoring – and the question of adherence."
```

Patients rarely have only one diagnosis. Especially in older people, long-term medication, cardiovascular disease, COPD, impaired kidney or liver function, diabetes, bleeding risks, allergies and earlier therapies can change the weighing considerably.

### Weighing benefits and risks

| Expected benefit | Possible risks and burdens |
|---|---|
| tumour control | side effects |
| longer life | interactions |
| symptom relief | complications |
| chance of cure | reduced quality of life |
| avoiding progression | organizational burden |
| better everyday functioning | stopping therapy or non-adherence |

> **Does the expected benefit outweigh the risks for *this* patient in *this* situation?**

### Off-label use and personalized therapy

**Off-label use** means a drug is used outside its officially approved indication. In oncology this matters because molecular diagnostics increasingly finds alterations for which suitable substances exist in principle. Then the questions are: Is the substance approved for this tumour type? How strong is the evidence? Are there trials or alternatives? How high is the risk – and does the option fit the therapy goal?

```timeline
title: "From molecular finding to therapy option"
events:
  - when: "1"
    what: "Tumour marker / mutation"
  - when: "2"
    what: "matching substance"
  - when: "3"
    what: "evidence"
  - when: "4"
    what: "approval: approved therapy, trial or off-label option?"
  - when: "5"
    what: "risk"
  - when: "6"
    what: "the patient's goal"
  - when: "7"
    what: "decision – often made jointly in a molecular tumour board (MTB)"
```

[@gladstone2025] summarize how effective recommendations from molecular tumour boards are and where evaluation gaps remain.

```quiz
question: "What does \"off-label use\" mean?"
options:
  - "A drug is dispensed without a prescription"
  - "A drug is used outside its officially approved indication"
  - "A drug is tested in humans for the first time in a clinical trial"
answer: "A drug is used outside its officially approved indication"
explain: "A matching molecular finding does not automatically mean that a therapy is approved, reimbursed or sensible in the specific case."
```

**Interim conclusion:** data are necessary, but they don't decide on their own. Our patient now has a confirmed finding and possible therapy options. The next question is: *which of these options fits him medically and personally?*

## 3 · Deciding together

```case
Depending on stage and findings, several paths are possible for our patient: surgery, systemic therapy, immunotherapy, a clinical trial, supportive care or watchful follow-up. Some differ greatly; others have similar chances of success but different burdens.
```

**Shared decision making (SDM)** means doctors and patients make a therapy decision together when several medically justifiable options exist. Three central steps:

1. **Explain the options** – which treatment paths are there?
2. **Discuss benefits and risks** – what is likely, what is uncertain, which burdens are possible?
3. **Include preferences** – what matters to the patient? What fits everyday life, values and goals?

The decision is made where **medical evidence, clinical experience and patient preferences** meet. This does not mean giving up medical responsibility – it means making the decision sustainable together. [@elwyn2012] describe a widely used model for practice. Remember Weizenbaum's question from [[history]]: the therapy decision is one of the tasks that should not be delegated entirely to a technical system.

```persona pat
For one person, living as long as possible is what matters most, even with a high burden. For another, being able to manage everyday life or being free of symptoms is more important. Both are legitimate – and belong in the conversation.
```

A therapy must not only be medically sound but also **workable in everyday life**:

| Area | Examples |
|---|---|
| Physical capacity | fatigue, breathlessness, mobility, lung function |
| Social environment | relatives, care, support, living alone |
| Organization | travel, appointments, treatment cycles, waiting times |
| Health literacy | understanding of diagnosis, risk and treatment plan |
| Emotional situation | fear, uncertainty, expectations of therapy |
| Personal values | quality of life, independence, longer life |

**Adherence** describes to what extent a jointly agreed therapy is actually carried out in everyday life – and it is primarily the patient who sees this.

```quiz
question: "A patient does not take his medication as agreed. What is the best first step?"
options:
  - "Remind him of his duty to cooperate"
  - "Understand the reasons: side effects, understanding of the plan, fit with everyday life"
  - "Stop the therapy immediately"
answer: "Understand the reasons: side effects, understanding of the plan, fit with everyday life"
explain: "Non-adherence should not be judged morally. If the reasons are not recognized, a therapy remains effective only in theory."
```

### Patient-reported outcomes

**Patient-reported outcomes (PROs)** are statements about health status reported directly by patients; **PROMs** are the instruments (e.g. questionnaires) used to collect them. They show how burdensome a therapy really is, whether symptoms increase, whether side effects matter in daily life and whether therapy goals are reached. In lung cancer, breathlessness, cough, fatigue and pain are especially relevant. The randomized trial by [@basch2016] studied symptom monitoring with PROs during routine cancer treatment.

```reflect
question: "One therapy, two perspectives: clinically the tumour is stable, lab values are normal, the therapy is given as planned. The patient reports severe fatigue, fear and sleep problems; his everyday life is heavily restricted – he is thinking about stopping. Is the therapy successful?"
intro: "There is no simple answer. Good evaluation of therapy needs **both perspectives** – clinical effectiveness and the burden experienced. Possible next steps:"
answers:
  - "capture the burden systematically (PROs) instead of just documenting it"
  - "check supportive measures against fatigue, nausea and sleep problems"
  - "discuss the therapy goal again together"
  - "adjust dose, schedule or therapy"
```

A practical example is the [PM4Onco](https://pm4onco.de/) project: the patient fills in a PROM → the data are stored in a structured way → the course is visualized → the care team or MTB sees relevant changes → the therapy decision is adjusted. Only when technology, processes and organization work together – the socio-technical triangle from [[history]] – does the patient's perspective really inform decisions.

```include cycle-en.svg
```

**Therapy is a course, not a single decision.** Over time, tumour response, symptom burden, side effects, patient goals, performance status, molecular resistance mechanisms and available therapy options can change – and each time a new decision situation arises.

## 4 · Guidelines and the reality of care

Medical knowledge is extensive, dynamic and complex. **Clinical guidelines** make it usable in care: they summarize current evidence, give orientation for diagnosis and therapy, standardize care processes, improve quality and safety, reduce over-, under- and misuse of care and make decisions traceable. But they do not replace clinical judgment.

| Standardization | Individualization |
|---|---|
| ensure quality | consider the individual case |
| apply evidence | take comorbidities into account |
| structure processes | include patient preferences |
| enable comparability | consider everyday life |
| reduce inappropriate care | adapt the therapy goal |

Too little standardization leads to inconsistent care; too little individualization means the therapy doesn't fit the patient, risks are underestimated and adherence falls. **Medical documentation** is a key factor: only what is documented can justify a deviation from the guideline.

```match
question: "Guidelines cover the whole care pathway. Which station does the question belong to?"
options: ["screening", "pathology / molecular diagnostics", "staging", "therapy planning", "follow-up"]
items:
  - item: "Who should be examined? With which method?"
    answer: "screening"
  - item: "Which markers should be determined?"
    answer: "pathology / molecular diagnostics"
  - item: "How is the extent of the disease classified?"
    answer: "staging"
  - item: "Which options are recommended?"
    answer: "therapy planning"
  - item: "Which check-ups make sense?"
    answer: "follow-up"
```

| In the ideal process … | In the reality of care … |
|---|---|
| all relevant data are fully available | data are spread across different systems |
| reports are structured and understandable | much information is free text, PDF or scans |
| guidelines apply to the situation | results arrive with delays |
| patients understand their options | the patient's perspective is not collected systematically |
| PROs are available over time | breaks between care sectors make an overview difficult |

This is the IT landscape from [[history]] – *grown rather than designed* – in everyday clinical work. Here, medical informatics addresses not only technical data problems but supports real decision processes.

```persona clin
Guidelines give orientation, not an automatic answer. Document why you deviate in an individual case – that makes decisions traceable and, later, analyzable.
```

```quiz
question: "Which statement about clinical guidelines is correct?"
options:
  - "Guidelines prescribe every individual decision in a binding way"
  - "Guidelines give orientation but do not replace clinical judgment"
  - "Guidelines only concern the choice of drug"
answer: "Guidelines give orientation but do not replace clinical judgment"
explain: "Guidelines structure the whole pathway – from screening to follow-up – and must be combined with comorbidities, preferences and everyday life."
```

## Back to the guiding question

> A finding only becomes a good therapy decision when **medical evidence, the individual patient's situation and the patient's perspective** are brought together.

## Take-home messages

1. **Therapy is a targeted intervention** – to cure, control, relieve or accompany.
2. **Therapy decisions require weighing** benefits, risks and burdens.
3. **Good therapy is decided together** – shared decision making connects evidence, experience and preferences.
4. **The patient's perspective must be made visible** – e.g. with PROs over time.
5. **Guidelines give orientation, not an automatic answer.**

## Self-check

```quiz
question: "What does a good therapy decision start with?"
options:
  - "Choosing the most effective drug"
  - "Clarifying the therapy goal"
  - "Scheduling appointments"
answer: "Clarifying the therapy goal"
```

```quiz
question: "What is a patient-reported outcome (PRO)?"
options:
  - "A lab value the patient measures herself"
  - "A statement about health status reported directly by patients"
  - "The discharge letter patients receive"
answer: "A statement about health status reported directly by patients"
```

```quiz
question: "When is shared decision making particularly important?"
options:
  - "When there is exactly one medically sensible option"
  - "When several medically justifiable options exist"
  - "Only when patients take part in trials"
answer: "When several medically justifiable options exist"
```

```quiz
question: "Why is preparing a tumour board a task for medical informatics?"
options:
  - "Because tumour boards only take place online"
  - "Because the required data must be brought together from many systems and formats"
  - "Because computer scientists decide on the therapy"
answer: "Because the required data must be brought together from many systems and formats"
explain: "Imaging, pathology, molecular diagnostics, lab values, medication and the patient's perspective are produced in different places – that is the integration task from section 2."
```

**Outlook:** the next unit covers nursing as a profession – nursing tasks, the nursing process, and nursing documentation and IT.
