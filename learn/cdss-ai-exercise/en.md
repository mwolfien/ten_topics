---
title: "Exercise: Build and Test a CDSS Yourself"
summary: "Self-paced Python exercise for the lecture on clinical decision support & AI: implement a rule with tests, train a model, choose a threshold, discover leakage and test the system in a second hospital – right in the browser or locally in Jupyter."
duration_minutes: 90
level: "Exercise · Python"
audiences: [med, cs, clin, tech]
order: 8
builds_on: [cdss-ai]
course: his
lecture: 6
kind: exercise
author: "Markus Wolfien"
objectives:
  - "Implement a qSOFA-like rule as a function and check it with reference, boundary and regression tests"
  - "Train a logistic regression and assess it with the AUC"
  - "Choose and justify a threshold under a realistic alert limit"
  - "Recognise a leakage variable"
  - "Validate a model externally and distinguish discrimination from calibration"
  - "Explain how missing values can reflect documentation behaviour"
  - "Describe the CDSS chain and the intended purpose for your own system"
readings: [collins2024, finlayson2021, agniel2018]
related_topics: [cdss, data-quality]
source: "Exercise for lecture 6 “Clinical Decision Support & AI – from Rules to Learning Systems”, Health Information Systems (winter term 2026/27), Markus Wolfien, IMB & ZMI"
---

> **What this is about:** in the module [[cdss-ai]] you met the CDSS chain: **DATA → TRIGGER → LOGIC → OUTPUT → ACTION → FEEDBACK**. Now you build its middle part yourself – a **rule**, a **model**, a **threshold** – and check whether the whole thing still works in a second hospital.

**Note:** the notebook, its comments and the column names are in **German**. The questions below give an English version of each question in the notebook.

## How to start

<div class="launch">
<a class="primary" href="../../../lab/index.html?path=cdss-ai-exercise/Uebung_VL6_CDSS_Aufgaben.ipynb">▶ Open the notebook in your browser</a>
<a href="../notebook.zip" download>⬇ Download notebook and data (ZIP)</a>
</div>

**In the browser (recommended):** the notebook runs entirely in your browser (JupyterLite with Pyodide) – no installation, no account, no server; the data never leave your device.

- On first start, the browser loads Python and the libraries; depending on your connection this takes **about a minute**. The first code cell also takes a little longer.
- Use a **normal browser window** (Chrome, Edge, Firefox, Safari) – in private mode, especially in Firefox, the notebook cannot find the CSV files.
- Your changes are saved **only in this browser**. Save your notebook now and then via *File → Download*.

**Locally:** unzip the file and open the notebook in Jupyter (e.g. JupyterLab or VS Code). You need Python ≥ 3.10 with `numpy`, `pandas`, `scikit-learn` and `matplotlib` (plus `scipy` for the bonus in part 6). The CSV files must be in the same folder as the notebook.

> ⚠️ The data set is **fully synthetic** (hospital A: 2,000, hospital B: 1,500 patients). The outcome `verschlechterung_6h` (deterioration within 6 h) is defined for teaching – **not a sepsis diagnosis**. What you build is a **teaching prototype** with no medical intended purpose.

## Outline

| Part | Topic | Link to the lecture | Time |
|---|---|---|---:|
| 0 | Setup | | 5 min |
| 1 | Getting to know the data | DATA | 10 min |
| 2 | A rule as a function – with tests | “A rule can be wrong too” | 15 min |
| 3 | Training a model | rule vs. learned function | 10 min |
| 4 | Choosing the threshold | “The threshold changes the system” | 15 min |
| 5 | A suspiciously good variable | sources of error | 8 min |
| 6 | External validation: hospital B | discrimination vs. calibration, monitoring | 15 min |
| 7 | What does a missing value mean? | sources of error | 7 min |
| 8 | From model to CDSS | synthesis, regulation | 5 min |
| | **Total** | | **90 min** |

You work on the programming tasks (marked `TODO`) in the notebook; one to three lines are usually enough. As long as a task is open, the cell tells you what is missing. You will find the **questions** below in the notebook too – note your answers there or here; here they stay saved in your browser and can be downloaded at the end, e.g. for the discussion.

## Questions for each part

```reflect
question: "**Part 1b:** go through the columns. Which information would **actually be available** at the time of prediction – and which are you unsure about?"
```

```reflect
question: "**Part 2c:** a colleague suggests changing the respiratory rate threshold to `> 22`. Which test fails – and what do you learn from it?"
```

```reflect
question: "**Part 2d:** the rule's specificity is high, its sensitivity low. Does that fit the statement that qSOFA is not recommended as a single screening tool?"
```

```reflect
question: "**Part 3:** the AUC tells you how well the model *ranks* patients with and without the event. Can you trigger an alert with an AUC alone? What is still missing?"
```

```reflect
question: "**Part 4b:** the ward says: “We no longer take more than 15 alerts per 100 patients seriously.” Which threshold do you choose? What are the sensitivity and PPV then? And who should actually make this decision?"
```

```reflect
question: "**Part 5b:** with `antibiotikum_gegeben` (antibiotic given) the model becomes much “better”. Would you roll it out like this? **When was this information available?**"
```

```reflect
question: "**Part 6:** the AUC is almost the same in hospital B. What does it mean for the physician in hospital B when the system shows “risk 40 %”?"
```

```reflect
question: "**Part 7b:** what sign does the coefficient of `laktat_fehlt` (lactate missing) have – and what has the model actually learned from it? Would this knowledge transfer to hospital A?"
```

```reflect
question: "**Part 8:** fill in the CDSS chain for your system, in keywords: **DATA** (which data, how current?), **TRIGGER** (when does it run?), **LOGIC** (rule, model or both? which threshold?), **OUTPUT** (info, warning, hard stop? to whom?), **ACTION** (what exactly should the person do?), **FEEDBACK** (which metrics do you monitor after go-live?)."
rows: 7
```

```reflect
question: "**Final question:** your notebook is a teaching prototype. What would have to change for it to become a medical device – and what role does the **intended purpose** play?"
```
