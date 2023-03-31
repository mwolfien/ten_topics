# Ten Topics for Medical Informatics
The vast and heterogeneous data being constantly generated in the clinics can provide great wealth for patients and research alike. The quickly evolving field of Medical Informatics research contributed numerous concepts, algorithms, and standards to facilitate this development. 
There here addressed topics are part of our viewpoints and perspectives article "Ten topics to get started in Medical Informatics research", which is currently in peer-review.

This underlying summary and digital extension should provide likewise a condensed and extensible ressource for the identified important, initial ten topics and beyond. Contributors are welcome to comprehesively improve and extend the current state (See Contributors section).

In this the online ressource for content extension, all suggested topics are briefly introduced and then key words indicate topics and in-depths literature for further reading. In addition, the topics are set to cover current aspects and open research gaps of the Medical Informatics domain, including data regulations & concepts, data harmonization & processing, and data evaluation, visualization & dissemination.  

## Data regulations & concepts

### Topic 1: Privacy & Ethics
Health information is sensitive and hence needs to be highly protected and should not be generously shared. 
* Anonymization - [Meurers et al. 2021](https://doi.org/10.1093/gigascience/giab068)
* Pseudonymization - [Zuo et al. 2021](https://doi.org/10.2196/29871)
* Synthetic data as surrogate - [Chen et al. 2021](https://doi.org/10.1038/s41551-021-00751-8)
* Systemic oversight and embedded ethics - [Vayena et al. 2018](https://doi.org/10.1177/1073110518766026), [McLennan et al. 2022](https://doi.org/10.1186/S12910-022-00746-3)

### Topic 2: Electronic health records & Clinical information systems 
Hospitals run clinical information systems (CIS) to collect, store, and alter clinical data about patients. A CIS, independent of the specialization and specific vendor, covers many clinical subdomains and integrates the patient-related data to support doctors in their daily routine.
The implementation of an EHR, including an individual's medical data in a bundled form, into the CIS is one key aspect. 
* EHR - [Häyrinen et al. 2008](https://doi.org/10.1016/J.IJMEDINF.2007.09.001)
* Systematic terminolgies for EHR improvement - [Brender et al. 2000](https://doi.org/10.1016/S1386-5056(00)00092-7), [Haux et al. 2002](https://doi.org/10.1016/S1386-5056(02)00030-8), [De Hoop et al. 2021](https://doi.org/10.1055/S-0041-1739519), [Millar, 2016](https://doi.org/10.3233/978-1-61499-658-3-683)
* Improving the usability and user acceptance of EHRs - [Schaaf et al. 2021](https://doi.org/10.1186/S12911-021-01435-8)

### Topic 3: Data Provenance
When explainable data is processed with interoperable tools, scientists can create automated and reusable workflows, provide access to reproducible research outcomes, and  data analysis pipelines ([Palmblad et al. 2019](https://doi.org/10.1093/BIOINFORMATICS/BTY646)). 
* Data provenance - [Palmblad et al. 2019](https://doi.org/10.1093/BIOINFORMATICS/BTY646), [Xu et al. 2018](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5961786/)
* FAIRification - [Inau et al. 2021](https://doi.org/10.2196/22505), [Queralt-Rosinach et al. 2021](https://doi.org/10.1101/2021.08.13.21262023), [Frexia et al. 2021](https://doi.org/10.3233/SHTI210131)

### Topic 4: Data Sharing
Cross-sectional medical data sharing is critical in modern clinical practice and medical research, in which the challenge of privacy-preserving transfer and utility needs to be addressed ([Scheibner et al. 2021](https://doi.org/10.2196/25120)).
* Federated learning, with e.g., DataSHIELD - [Gaye et al. 2014](https://doi.org/10.1093/IJE/DYU188), [Marcon et al. 2021](https://doi.org/10.1371/JOURNAL.PCBI.1008880) or Personal Health Train - [Beyan et al. 2020](https://doi.org/10.1162/DINT_A_00032)
* Secure-multi-party computation (SPMC) - [Dong et al. 2021](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8378657/)

## Data harmonization & processing

### Topic 5: Extract, Transform, and Load (ETL) processes 
Data handling in Medical Informatics remains a major challenge. Even though most data in medicine is available electronically, it often lacks interoperability ([Negro-Calduch et al. 2021](https://doi.org/10.1016/J.IJMEDINF.2021.104507)). As a first step to actually use the data, processes to Extract, Transform, and Load (ETL) are needed to obtain harmonized data from different data systems or clinical entities. 
* ETL, as safe, secure, and accurate - [Prasser et al. 2019](https://doi.org/10.1016/J.IJMEDINF.2019.03.006), [Liaw et al. 2021](https://doi.org/10.1093/JAMIA/OCAA340)
* ETL, as scalable - [Helgheim et al. 2019](https://doi.org/10.3390/IJERPH16050769), and reusable - [Chapter 6 Extract Transform Load | The Book of OHDSI](https://ohdsi.github.io/TheBookOfOhdsi/ExtractTransformLoad.html#introduction-1) process
* Perform quality checks - [Guo et al. 2019](https://doi.org/10.1093/JAMIA/OCZ143)

### Topic 6: Fast Healthcare Interoperability Resources 
Semantic and syntactic interoperability can be ensured by communication exchange standards, such as the Fast Healthcare Interoperability Resources (FHIR) standard of Health Level 7 (HL7) and medical terminologies.
* FHIR communication standard - [Andersen et al. 2018](https://doi.org/10.1515/BMT-2017-0021/MACHINEREADABLECITATION/RIS), [Lehne et al. 2019](https://doi.org/10.3233/SHTI190805), [Bender and Sartipi, 2013](https://doi.org/10.1109/CBMS.2013.6627810)
* SMART-on-FHIR enables third-party app development for health care applications - [Smart Health IT](https://apps.smarthealthit.org/apps/featured)
* Used for mobile health applications - [Lamprinakos et al. 2015](https://doi.org/10.1109/MOBIHEALTH.2014.7015927), [Benhamida et al. 2020](https://doi.org/10.1109/CINTI51262.2020.9305828), [Mandel et al. 2016](https://doi.org/10.1093/JAMIA/OCV189)

### Topic 7: Observational Medical Outcomes Partnership Common Data Models
Data harmonization enables research teams to run real-world observational studies based on heterogeneous data across country borders. Thus, harmonized data embedded in a common data model (CDM), which is an agreement about the utilization of standardized terminologies for data representation, is crucial to exchange data and results on a large scale. 
* OMOP and OHDSI - [Garza et al. 2016](https://doi.org/10.1016/J.JBI.2016.10.016), [Reinecke et al. 2021](https://doi.org/10.3233/SHTI210546)
* Applied to genomics, oncology, and imaging projects among others - [Peng et al. 2021](https://doi.org/10.3233/SHTI210545), [Ahmadi et al. 2022](https://doi.org/10.3390/IJMS231911834/S1), [Park et al. 2022](https://doi.org/10.3349/YMJ.2022.63.S74)
* EHDEN Academy as a versatile training network - [Blacketer et al. 2021](https://doi.org/10.1093/JAMIA/OCAB132)

## Data evaluation, visualization & dissemination

### Topic 8: Data Quality 
Data quality depends on the quality of single data elements, data completeness, data conformance, and data plausibility aspects that may considerably determine the validity and veracity of analysis results. 89,90
* High data quality as a fundamental requirement - [Goncalves et al. 2020](https://doi.org/10.1186/S12874-020-00977-1)
* Data quality indicators and evaluation principles - [Löbe et al. 2022](https://doi.org/10.3233/SHTI210904), [Wang and Strong, 2015](https://doi.org/10.1080/07421222.1996.11518099), [Wahyudi et al. 2018](https://doi.org/10.1007/S10796-017-9822-7)
* Publish high quality synthetic medical datasets - [Hahn et al. 2022](https://doi.org/10.3390/JPM12081278)

### Topic 9: Clinical Decision Support Systems
Clinical Decision Support Systems (CDSS) are computer systems designed to assist the medical staff with decision making tasks about individual patients and based on clinical data ([Sutton et al. 2020](https://doi.org/10.1038/s41746-020-0221-y)).
* Positive impact of a CDSS - [Shen et al. 2021](https://doi.org/10.1093/JAMIA/OCAA250), [Ronicke et al. 2019](https://doi.org/10.1186/S13023-019-1040-6), [Eltorai et al. 2020](https://doi.org/10.1097/RTI.0000000000000453), [](https://doi.org/), [Groenhof et al. 2019](https://doi.org/10.1007/S12471-019-01308-W)
* Negative impact of a CDSS - [Olakotan et al. 2020](https://doi.org/10.3233/SHTI200293), [Jacobs et al. 2021](https://doi.org/10.1038/s41398-021-01224-x)
* Explainable AI (XAI) - [Antoniadi et al. 2021](https://doi.org/10.3390/APP11115088), [Wolfien et al. 2020](https://doi.org/10.1016/J.EBIOM.2020.102862)
* A CDM as basis for an AI - [Reps et al. 2018](https://doi.org/10.1093/JAMIA/OCY032), [Chapter 13 Patient-Level Prediction | The Book of OHDSI](https://ohdsi.github.io/TheBookOfOhdsi/PatientLevelPrediction.html)

### Topic 10: Visualizations
Large volumes of data collected from patient registries, health centers, genomic databases, and public records can potentially improve the efficiency and quality of healthcare via enhancing the interoperability of medical systems, assisting in clinical decision making, and delivering feedback on effective procedures. 121  
* Dashboards with postive influence 127, like R Shiny 125 or Plotly Dash 126
* Visualization of multi-dimensional biomedical data, e.g., cBioPortal 129, 130, 131, or i2b2 132,133

## Additional Topics

### Computational Infrastructure
* Data storage and processing setups - [Ismail et al. 2020](https://doi.org/10.2196/17508), [Ozaydin et al. 2020](https://doi.org/10.2196/18579)  

### Disease Maps
Disease Maps are a community-driven systems medicine approach to represent and model disease mechanisms. Disease maps serve both as a knowledgebase and analytical tools for advanced Omics data integration and interpretation, as well as hypothesis generation. These maps can further serve as a basis for clinical decision support systems [Mazein, A., Ostaszewski, M., Kuperstein, I. et al. 2018](https://doi.org/10.1038/s41540-018-0059-y). 

Example Disease Maps
* COVID-19 Disease Map
* Atlas of Inflammation Resolution (AIR)
* NaviCenta - (Navigate the Placenta)
* CyFi-Map (Cystic Fibrosis)
* Cellular Atlas of the Rheumatic Joint
* Asthma-ap

## Contribution

### How can I contribute to the "Ten Topics for Medical Informatics" initiative?
1. "Star" or "Watch" our project =) (optional)
2. Fork the project
3. Contribute towards the desired topic, in which your keyword and or reference fits best. Here, it is good to stick to the orinial ten topics as much as possible. If there is no actual topic available, novel ones can be proposed and integrated.
4. Create a pull request and we will merge your suggestion(s) to the main branch after curation.
5. Add yourself to the contributors list!

### Contributors list
[Markus Wolfien](https://github.com/mwolfien)  
[Julia Scheel](https://github.com/JuliaScheel)
