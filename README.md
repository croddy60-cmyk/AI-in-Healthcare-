# Myocardial Infarction In Hospitality Mortality Demographic Information Script

## Overview
This project analyzes key demographic and clinical characteristics of patients presenting with myocardial infarction (MI) using the MIMIC-IV database.

## Requirements
- Python 3.13+
- Standard libraries: `csv`, `io`, `datetime`, `subprocess`
- Access to a secure HPC cluster with MIMIC-IV credentials
- Approved access to the MIMIC-IV database

## Features

### Demographics
- Gender
- Age group
- Race/Ethnicity
- Insurance status

### Admissions Data
- Anchor year
- Admission type
- Admission location
- Hour of admission
- Day of week
- ICU admission flag

### Comorbidities
- Hypertension
- Chronic Kidney Disease (CKD)
- Diabetes
- Heart Failure
- Prior Myocardial Infarction
- Chronic Obstructive Pulmonary Disease (COPD)

### Vitals (First 24 Hours)
- Heart Rate (HR)
- Systolic Blood Pressure (SBP)
- Diastolic Blood Pressure (DBP)
- Mean Arterial Pressure (MAP)
- Oxygen Saturation (SpO₂)
- Respiratory Rate (RR)
- Temperature
- Glasgow Coma Scale (GCS)

### Laboratory Values (First 4 Hours)
- Troponin T & I
- Creatine Kinase (CK)
- CK-MB
- Creatinine
- Blood Urea Nitrogen (BUN)
- B-type Natriuretic Peptide (BNP)
- NT-proBNP
- Lactate
- Hemoglobin
- Hematocrit
- White Blood Cell Count (WBC)
- Potassium (K⁺)
