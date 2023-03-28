# Ten Topics for Medical Informatics
The vast and heterogeneous data being constantly generated in the clinics can provide great wealth for patients and research alike. The quickly evolving field of Medical Informatics research contributed numerous concepts, algorithms, and standards to facilitate this development. 
There here addressed topics are part of our viewpoints and perspectives article "Ten topics to get started in Medical Informatics research", which is currently in peer-review.

This underlying summary and digital extension should provide likewise a condensed and extensible ressource for the identified important, initial ten topics and beyond. Contributors are welcome to comprehesively improve and extend the current state (See Contributors section).

In this online ressource, all suggested topics are briefly introduced and then key words indicate topics and in-depths literature for further reading. In addition, the topics are set to cover current aspects and open research gaps of the Medical Informatics domain, including data regulations & concepts, data harmonization & processing, and data evaluation, visualization & dissemination.  

## Data regulations & concepts
### Privacy & Ethics
Health information is sensitive and hence needs to be highly protected and should not be generously shared. 
* Anonymization 18
* Pseudonymization 19
* Synthetic data as surrogate 20
* Systemic oversight and ethics 21,22
* URLs and URLs in angle brackets will automatically get turned into links http://www.example.com or <http://www.example.com>

### Electronic health records & Clinical information systems 
Hospitals run clinical information systems (CIS) to collect, store, and alter clinical data about patients. A CIS, independent of the specialization and specific vendor, covers many clinical subdomains and integrates the patient-related data to support doctors in their daily routine.
The implementation of an EHR, including an individual's medical data in a bundled form, into the CIS is one key aspect. 
* EHR 30
* Systematic terminolgies for EHR improvement 31-34
* Improving the usability and user acceptance of EHRs 37

### Data Provenance
When explainable data is processed with interoperable tools, scientists can create automated and reusable workflows, provide access to reproducible research outcomes, and  data analysis pipelines. 42
* Data provenance 42,43
* FAIRification 45,46,47

### Data Sharing
Cross-sectional medical data sharing is critical in modern clinical practice and medical research, in which the challenge of privacy-preserving transfer and utility needs to be addressed. 51
* Federated learning, with e.g., DataSHIELD 53,54 or Personal Health Train 56
* Secure-multi-party computation (SPMC) 57

## Data harmonization & processing
### Extract, Transform, and Load (ETL) processes 
Data handling in Medical Informatics remains a major challenge. Even though most data in medicine is available electronically, it often lacks interoperability [60]. As a first step to actually use the data, processes to Extract, Transform, and Load (ETL) are needed to obtain harmonized data from different data systems or clinical entities. 
* ETL, as safe, secure, and accurate 61,67
* ETL, as scalable 62, and reusable 63 process
* Perform quality checks 64

### Fast Healthcare Interoperability Resources 
Semantic and syntactic interoperability can be ensured by communication exchange standards, such as the Fast Healthcare Interoperability Resources (FHIR) standard of Health Level 7 (HL7) and medical terminologies.
* FHIR communication standard 71,72,73
* SMART-on-FHIR enables third-party app development for health care applications 78
* Used for mobile health applications 76,77,79

### Observational Medical Outcomes Partnership Common Data Models
Data harmonization enables research teams to run real-world observational studies based on heterogeneous data across country borders. Thus, harmonized data embedded in a common data model (CDM), which is an agreement about the utilization of standardized terminologies for data representation, is crucial to exchange data and results on a large scale. 
* OMOP and OHDSI 81,82
* Applied to genomics, oncology, and imaging projects among others 84,85,86
* EHDEN Academy as a versatile training network 88

## Data evaluation, visualization & dissemination

### Data Quality 
Data quality depends on the quality of single data elements, data completeness, data conformance, and data plausibility aspects that may considerably determine the validity and veracity of analysis results. 89,90
* High data quality as a fundamental requirement 92
* Data quality indicators and evaluation principles 93,94,95
* Publish high quality synthetic medical datasets 103

### Clinical Decision Support Systems
Clinical Decision Support Systems (CDSS) are computer systems designed to assist the medical staff with decision making tasks about individual patients and based on clinical data. 104
* Positive impact of a CDSS 106,107,108,110
* Negative impact of a CDSS 112, 114
* Explainable AI (XAI) 113, 115
* A CDM as basis for an AI 116, 117

### Visualizations
Large volumes of data collected from patient registries, health centers, genomic databases, and public records can potentially improve the efficiency and quality of healthcare via enhancing the interoperability of medical systems, assisting in clinical decision making, and delivering feedback on effective procedures. 121  
* Dashboards with postive influence 127, like R Shiny 125 or Plotly Dash 126
* Visualization of multi-dimensional biomedical data, e.g., cBioPortal 129, 130, 131, or i2b2 132,133

## Contribution

### How can I contribute to the "Ten Topics for Medical Informatics" initiative?
1. "Star" or "Watch" our project =) (optional)
2. Fork the project
3. Contribute towards the desired topic, in which your keyword and or reference fits best. Here, it is good to stick to the orinial ten topics as much as possible. If there is no actual topic available, novel ones can be proposed and integrated.
4. Create a pull request and we will merge your suggestion(s) to the main branch after curation.
5. Add yourself to the contributors list!

### Contributors list
[Markus Wolfien](https://github.com/mwolfien)