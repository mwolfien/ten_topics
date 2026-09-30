<!-- This file is generated from data/topics.yaml, data/references.yaml and templates/README.md.in.
     Do not edit it directly: edit those files and run `python scripts/tentopics.py build`. -->
# Ten Topics for Medical Informatics

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23047297.svg)](https://doi.org/10.5281/zenodo.23047297)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC_BY_4.0-lightgrey.svg)](LICENSE)
[![Checks](https://github.com/mwolfien/ten_topics/actions/workflows/checks.yml/badge.svg)](https://github.com/mwolfien/ten_topics/actions/workflows/checks.yml)
![References](https://img.shields.io/badge/references-117-blue)
![Last update](https://img.shields.io/badge/last_update-2026--09-green)

**Website:** [mwolfien.github.io/ten_topics](https://mwolfien.github.io/ten_topics/): search all topics and references, and download them as [BibTeX](https://mwolfien.github.io/ten_topics/data/references.bib) or [CSL-JSON](https://mwolfien.github.io/ten_topics/data/references.json).

The vast and heterogeneous data being constantly generated in the clinics can provide great wealth for patients and research alike. The quickly evolving field of Medical Informatics research contributed numerous concepts, algorithms, and standards to facilitate this development.
The here addressed topics are part of our viewpoint article "Ten Topics to Get Started in Medical Informatics Research" - [Wolfien et al. 2023](https://doi.org/10.2196/45948), published in the Journal of Medical Internet Research.

This underlying summary and digital extension should provide likewise a condensed and extensible resource for the identified important, initial ten topics and beyond. It is maintained as a living, curated collection: contributors are welcome to comprehensively improve and extend the current state (see [Contributing](#contributing)).

In this online resource for content extension, all suggested topics are briefly introduced and then key words indicate topics and in-depth literature for further reading. In addition, the topics are set to cover current aspects and open research gaps of the Medical Informatics domain, including data regulations & concepts, data harmonization & processing, and data evaluation, visualization & dissemination.

## Data regulations & concepts

### Topic 1: Privacy & Ethics
Health information is sensitive and hence needs to be highly protected and should not be generously shared.

* Anonymization - [Meurers et al. 2021](https://doi.org/10.1093/gigascience/giab068)
* Pseudonymization - [Zuo et al. 2021](https://doi.org/10.2196/29871)
* Synthetic data as surrogate - [Chen et al. 2021](https://doi.org/10.1038/s41551-021-00751-8), with privacy and utility metrics - [Kaabachi et al. 2025](https://doi.org/10.1038/s41746-024-01359-3)
* Systemic oversight and embedded ethics - [Vayena et al. 2018](https://doi.org/10.1177/1073110518766026), [McLennan et al. 2022](https://doi.org/10.1186/S12910-022-00746-3)
* Ethical and regulatory challenges of Large Language Models (LLMs) in medicine - [Ong et al. 2024](https://doi.org/10.1016/S2589-7500(24)00061-X), [Haltaufderheide and Ranisch 2024](https://doi.org/10.1038/s41746-024-01157-x)
* EU AI Act and its implications for digital medicine - [Gilbert 2024](https://doi.org/10.1038/s41746-024-01116-6)

### Topic 2: Electronic health records & Clinical information systems
Hospitals run clinical information systems (CIS) to collect, store, and alter clinical data about patients. A CIS, independent of the specialization and specific vendor, covers many clinical subdomains and integrates the patient-related data to support doctors in their daily routine.

The implementation of an EHR, including an individual's medical data in a bundled form, into the CIS is one key aspect.

* EHR - [Häyrinen et al. 2008](https://doi.org/10.1016/J.IJMEDINF.2007.09.001)
* Systematic terminologies for EHR improvement - [Brender et al. 2000](https://doi.org/10.1016/S1386-5056(00)00092-7), [Haux et al. 2002](https://doi.org/10.1016/S1386-5056(02)00030-8), [De Hoop et al. 2021](https://doi.org/10.1055/S-0041-1739519), [Millar, 2016](https://doi.org/10.3233/978-1-61499-658-3-683)
* Improving the usability and user acceptance of EHRs - [Schaaf et al. 2021](https://doi.org/10.1186/S12911-021-01435-8)
* Reducing EHR documentation burden with team-based documentation support - [Holmgren et al. 2024](https://doi.org/10.1001/jamainternmed.2024.4123) and ambient AI scribes - [Tierney et al. 2024](https://doi.org/10.1056/CAT.23.0404), [Olson et al. 2025](https://doi.org/10.1001/jamanetworkopen.2025.34976), [Lukac et al. 2025](https://doi.org/10.1056/AIoa2501000)
* Limitations of LLMs for medical coding with standard terminologies - [Soroush et al. 2024](https://doi.org/10.1056/AIdbp2300040)

### Topic 3: Data Provenance
When explainable data is processed with interoperable tools, scientists can create automated and reusable workflows, provide access to reproducible research outcomes, and data analysis pipelines ([Palmblad et al. 2019](https://doi.org/10.1093/BIOINFORMATICS/BTY646)).

* Data provenance - [Palmblad et al. 2019](https://doi.org/10.1093/BIOINFORMATICS/BTY646), [Xu et al. 2018](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5961786/), [Gierend et al. 2024](https://doi.org/10.2196/51297)
* FAIRification - [Inau et al. 2021](https://doi.org/10.2196/22505), [Queralt-Rosinach et al. 2021](https://doi.org/10.1101/2021.08.13.21262023), [Frexia et al. 2021](https://doi.org/10.3233/SHTI210131), [Tai et al. 2025](https://doi.org/10.1016/j.jclinepi.2025.111920)

### Topic 4: Data Sharing
Cross-sectional medical data sharing is critical in modern clinical practice and medical research, in which the challenge of privacy-preserving transfer and utility needs to be addressed ([Scheibner et al. 2021](https://doi.org/10.2196/25120)).

* Federated learning, with e.g., DataSHIELD - [Gaye et al. 2014](https://doi.org/10.1093/IJE/DYU188), [Marcon et al. 2021](https://doi.org/10.1371/JOURNAL.PCBI.1008880) or Personal Health Train - [Beyan et al. 2020](https://doi.org/10.1162/DINT_A_00032)
* Secure-multi-party computation (SPMC) - [Dong et al. 2021](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8378657/)
* Clinical applications, technical architectures, and governance of federated learning - [Teo et al. 2024](https://doi.org/10.1016/j.xcrm.2024.101419), [Eden et al. 2025](https://doi.org/10.1038/s41746-025-01836-3)
* Secondary use of health data in the European Health Data Space (EHDS) - [Hussein et al. 2025](https://doi.org/10.2196/69813)

## Data harmonization & processing

### Topic 5: Extract, Transform, and Load (ETL) processes
Data handling in Medical Informatics remains a major challenge. Even though most data in medicine is available electronically, it often lacks interoperability ([Negro-Calduch et al. 2021](https://doi.org/10.1016/J.IJMEDINF.2021.104507)). As a first step to actually use the data, processes to Extract, Transform, and Load (ETL) are needed to obtain harmonized data from different data systems or clinical entities.

* ETL, as safe, secure, and accurate - [Prasser et al. 2019](https://doi.org/10.1016/J.IJMEDINF.2019.03.006), [Liaw et al. 2021](https://doi.org/10.1093/JAMIA/OCAA340)
* ETL, as scalable - [Helgheim et al. 2019](https://doi.org/10.3390/IJERPH16050769), and reusable - [Chapter 6 Extract Transform Load | The Book of OHDSI](https://ohdsi.github.io/TheBookOfOhdsi/ExtractTransformLoad.html#introduction-1) process
* Perform quality checks - [Guo et al. 2019](https://doi.org/10.1093/JAMIA/OCZ143)
* LLMs to extract structured information from unstructured clinical text - [Wiest et al. 2024](https://doi.org/10.1038/s41746-024-01233-2), [Hein et al. 2025](https://doi.org/10.1038/s41746-025-01686-z), [Hu et al. 2026](https://doi.org/10.1093/jamia/ocaf213)

### Topic 6: Fast Healthcare Interoperability Resources
Semantic and syntactic interoperability can be ensured by communication exchange standards, such as the Fast Healthcare Interoperability Resources (FHIR) standard of Health Level 7 (HL7) and medical terminologies.

* FHIR communication standard - [Andersen et al. 2018](https://doi.org/10.1515/bmt-2017-0021), [Lehne et al. 2019](https://doi.org/10.3233/SHTI190805), [Bender and Sartipi, 2013](https://doi.org/10.1109/CBMS.2013.6627810)
* SMART-on-FHIR enables third-party app development for health care applications - [Smart Health IT](https://apps.smarthealthit.org/apps/featured)
* Used for mobile health applications - [Lamprinakos et al. 2014](https://doi.org/10.4108/icst.mobihealth.2014.257232), [Benhamida et al. 2020](https://doi.org/10.1109/CINTI51262.2020.9305828), [Mandel et al. 2016](https://doi.org/10.1093/JAMIA/OCV189)
* Combining FHIR and LLMs, e.g., to convert clinical text into FHIR resources - [Li et al. 2024](https://doi.org/10.1056/AIcs2300301), or for clinical predictions directly on FHIR data - [Engelke et al. 2025](https://doi.org/10.1093/jamia/ocaf165)

### Topic 7: Observational Medical Outcomes Partnership Common Data Models
Data harmonization enables research teams to run real-world observational studies based on heterogeneous data across country borders. Thus, harmonized data embedded in a common data model (CDM), which is an agreement about the utilization of standardized terminologies for data representation, is crucial to exchange data and results on a large scale.

* OMOP and OHDSI - [Garza et al. 2016](https://doi.org/10.1016/J.JBI.2016.10.016), [Reinecke et al. 2021](https://doi.org/10.3233/SHTI210546)
* Applied to genomics, oncology, and imaging projects among others - [Peng et al. 2021](https://doi.org/10.3233/SHTI210545), [Ahmadi et al. 2022](https://doi.org/10.3390/ijms231911834), [Park et al. 2022](https://doi.org/10.3349/YMJ.2022.63.S74), [Wang et al. 2025a](https://doi.org/10.1038/s41746-025-01581-7)
* Large-scale federated OHDSI network studies - [Cai et al. 2025](https://doi.org/10.1001/jamaophthalmol.2024.6555)
* LLM-based automated mapping of source data to OMOP concepts - [Adams et al. 2025](https://doi.org/10.2196/69004)
* EHDEN Academy as a versatile training network - [Blacketer et al. 2021](https://doi.org/10.1093/JAMIA/OCAB132), with learnings from building the European Health Data & Evidence Network (EHDEN) - [Voss et al. 2024](https://doi.org/10.1093/jamia/ocad214), [Blacketer et al. 2025](https://doi.org/10.2196/74119)

## Data evaluation, visualization & dissemination

### Topic 8: Data Quality
Data quality depends on the quality of single data elements, data completeness, data conformance, and data plausibility aspects that may considerably determine the validity and veracity of analysis results.

* High data quality as a fundamental requirement - [Goncalves et al. 2020](https://doi.org/10.1186/S12874-020-00977-1)
* Data quality indicators and evaluation principles - [Löbe et al. 2022](https://doi.org/10.3233/SHTI210904), [Wang and Strong, 2015](https://doi.org/10.1080/07421222.1996.11518099), [Wahyudi et al. 2018](https://doi.org/10.1007/S10796-017-9822-7)
* Data quality for trustworthy AI in medicine (METRIC framework) - [Schwabe et al. 2024](https://doi.org/10.1038/s41746-024-01196-4)
* Publish high quality synthetic medical datasets - [Hahn et al. 2022](https://doi.org/10.3390/JPM12081278), and assess their quality - [Vallevik et al. 2024](https://doi.org/10.1016/j.ijmedinf.2024.105413), [Kaabachi et al. 2025](https://doi.org/10.1038/s41746-024-01359-3)

### Topic 9: Clinical Decision Support Systems
Clinical Decision Support Systems (CDSS) are computer systems designed to assist the medical staff with decision making tasks about individual patients and based on clinical data ([Sutton et al. 2020](https://doi.org/10.1038/s41746-020-0221-y)).

* Positive impact of a CDSS - [Shen et al. 2021](https://doi.org/10.1093/JAMIA/OCAA250), [Ronicke et al. 2019](https://doi.org/10.1186/S13023-019-1040-6), [Eltorai et al. 2020](https://doi.org/10.1097/RTI.0000000000000453), [Groenhof et al. 2019](https://doi.org/10.1007/S12471-019-01308-W)
* Negative impact of a CDSS - [Olakotan et al. 2020](https://doi.org/10.3233/SHTI200293), [Jacobs et al. 2021](https://doi.org/10.1038/s41398-021-01224-x)
* Explainable AI (XAI) - [Antoniadi et al. 2021](https://doi.org/10.3390/APP11115088), [Wolfien et al. 2020](https://doi.org/10.1016/J.EBIOM.2020.102862), [Kostick-Quenet and Gerke 2022](https://doi.org/10.1038/s41746-022-00737-z)
* A CDM as basis for an AI - [Reps et al. 2018](https://doi.org/10.1093/JAMIA/OCY032), [Chapter 13 Patient-Level Prediction | The Book of OHDSI](https://ohdsi.github.io/TheBookOfOhdsi/PatientLevelPrediction.html)
* Effect of Large Language Models (LLM) - [Singhal et al. 2023](https://doi.org/10.1038/s41586-023-06291-2), [Singhal et al. 2025](https://doi.org/10.1038/s41591-024-03423-7), [Van Veen et al. 2024](https://doi.org/10.1038/s41591-024-02855-5), or conversational diagnostic AI - [Tu et al. 2025](https://doi.org/10.1038/s41586-025-08866-7)
* Limitations of LLMs in clinical decision-making and their influence on physicians' diagnostic reasoning - [Hager et al. 2024](https://doi.org/10.1038/s41591-024-03097-1), [Goh et al. 2024](https://doi.org/10.1001/jamanetworkopen.2024.40969)
* Retrieval-augmented generation (RAG) to ground biomedical LLMs in curated, versioned, and auditable sources within research and clinical data infrastructures - [Wolfien et al. 2026](https://www.mdpi.com/2413-4155/8/9/266)
* Acceptance of AI among healthcare professionals in hospitals - [Lambert et al. 2023](https://doi.org/10.1038/s41746-023-00852-5)
* User-centred design characteristics and challenges of CDSS - [Bayor et al. 2025](https://doi.org/10.2196/63733)

### Topic 10: Visualizations
Large volumes of data collected from patient registries, health centers, genomic databases, and public records can potentially improve the efficiency and quality of healthcare via enhancing the interoperability of medical systems, assisting in clinical decision making, and delivering feedback on effective procedures.

* User-centred design for AI in health care - [Seneviratne et al. 2022](https://informatics.bmj.com/content/29/1/e100656), users' perspectives on AI-enabled decision aids - [Hassan et al. 2024](https://doi.org/10.1038/s41746-024-01326-y)
* Dashboards with positive influence [Clarke et al. 2016](https://pubmed.ncbi.nlm.nih.gov/27332223/) and design practices - [Vornhagen et al. 2026](https://doi.org/10.2196/77361), like [R Shiny](https://shiny.posit.co/) or [Plotly Dash](https://zenodo.org/record/3346213)
* Visualization of multi-dimensional biomedical data, e.g., cBioPortal - [Gao et al. 2013](https://doi.org/10.1126/scisignal.2004088), [Reimer et al. 2021](https://doi.org/10.3233/SHTI210833), [Brlek et al. 2021](https://doi.org/10.3390/cancers13133247), or i2b2 [Murphy et al. 2010](https://doi.org/10.1136/jamia.2009.000893), [Castro et al. 2022](https://doi.org/10.1093/jamia/ocab264)

## Additional Topics

### Computational Infrastructure
* Data storage and processing setups - [Ismail et al. 2020](https://doi.org/10.2196/17508), [Ozaydin et al. 2020](https://doi.org/10.2196/18579)
* Cloud-based research platforms for large-scale cohort and genomic data, e.g., All of Us Researcher Workbench - [All of Us Research Program Genomics Investigators 2024](https://doi.org/10.1038/s41586-023-06957-x)
* Synthetic data and federated networks for privacy-preserving access to real-world data - [Wang et al. 2025b](https://doi.org/10.1038/s41746-025-02126-8)

### Disease Maps
Disease Maps are a community-driven systems medicine approach to represent and model disease mechanisms. Disease maps serve both as a knowledgebase and analytical tools for advanced Omics data integration and interpretation, as well as hypothesis generation. These maps can further serve as a basis for clinical decision support systems ([Mazein et al. 2018](https://doi.org/10.1038/s41540-018-0059-y)).

Example Disease Maps:

* COVID-19 Disease Map - [Ostaszewski et al. 2021](https://doi.org/10.15252/msb.202110387)
* Atlas of Inflammation Resolution (AIR) - [Serhan and Gupta et al. 2020](https://doi.org/10.1016/j.mam.2020.100894)
* NaviCenta - (Navigate the Placenta) - [Scheel et al. 2021](https://www.sbi.uni-rostock.de/minerva/index.xhtml?id=NaviCenta)
* CyFi-Map (Cystic Fibrosis) - [Pereira et al. 2021](https://doi.org/10.1038/s41598-021-01618-3)
* Cellular Atlas of the Rheumatic Joint - [Zerrouk and Aghakhani 2022](https://doi.org/10.3389/fsysb.2022.925791), extended towards large-scale Boolean models - [Zerrouk et al. 2024a](https://doi.org/10.1038/s41540-024-00337-5) and a multi-cellular virtual twin of the synovial joint - [Zerrouk et al. 2024b](https://doi.org/10.1038/s41746-024-01396-y)
* AsthmaMap - [Mazein et al. 2021](https://doi.org/10.1016/j.jaci.2020.11.032)

FAIR assessment of Disease Maps to foster open science and crowdsourcing - [Balaur et al. 2025](https://doi.org/10.1038/s41597-025-05147-w)

## How to cite

If you use this resource, please cite the original article:

> Wolfien M, Ahmadi N, Fitzer K, Grummt S, Heine KL, Jung IC, Krefting D, Kühn A, Peng Y, Reinecke I, Scheel J, Schmidt T, Schmücker P, Schüttler C, Waltemath D, Zoch M, Sedlmayr M. Ten Topics to Get Started in Medical Informatics Research. *J Med Internet Res* 2023;25:e45948. [doi:10.2196/45948](https://doi.org/10.2196/45948)

To cite this living collection, please use:

> Wolfien M, Scheel J. Ten Topics for Medical Informatics [Data set]. Zenodo. [doi:10.5281/zenodo.23047297](https://doi.org/10.5281/zenodo.23047297)

This DOI always resolves to the latest version; the DOI of a specific version is listed on [Zenodo](https://doi.org/10.5281/zenodo.23047297). The "Cite this repository" button uses [CITATION.cff](CITATION.cff). Changes between versions are listed in the [CHANGELOG](CHANGELOG.md).

## Contributing

Suggestions are very welcome! The quickest way is to [suggest a reference](https://github.com/mwolfien/ten_topics/issues/new?template=suggest-reference.yml) or [propose a new topic](https://github.com/mwolfien/ten_topics/issues/new?template=propose-topic.yml) via an issue. To contribute directly, please read [CONTRIBUTING.md](CONTRIBUTING.md): it describes the inclusion criteria and how to add a reference to `data/references.yaml` and `data/topics.yaml`. Please stick to the original ten topics as much as possible; if no existing topic fits, novel ones can be proposed and integrated.

### Contributors list
- [Markus Wolfien](https://github.com/mwolfien)
- [Julia Scheel](https://github.com/JuliaScheel)

## License

The content of this repository is licensed under the [Creative Commons Attribution 4.0 International License (CC BY 4.0)](LICENSE).
