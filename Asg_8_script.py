# Biol 1595_2595 Asg 8 Script

# Finding Variables

# Focusing on Mimic IV data set

# 2026-05-03
# Biol 1595_2595 
# Finding Variables
# Focusing on MIMIC IV data set

import csv
import subprocess
import io
from datetime import datetime

def main():

    # Greet User
    print("Hi! We will be looking at the MIMIC-IV dataset and compiling information on patients with MI split by in-hospital mortality during the MI visit")

    # Define File Names
    patients_file_name = "/oscar/data/shared/ursa/mimic-iv/hosp/3.1/patients.csv"
    admissions_file_name = "/oscar/data/shared/ursa/mimic-iv/hosp/3.1/admissions.csv"
    diagnoses_file_name = "/oscar/data/shared/ursa/mimic-iv/hosp/3.1/diagnoses_icd.csv"
    chartevents_file_name = "/oscar/data/shared/ursa/mimic-iv/icu/3.1/chartevents.csv"
    labevents_file_name = "/oscar/data/shared/ursa/mimic-iv/hosp/3.1/labevents.csv"

    # Define diagnosis codes
    dx_code = set(["410", "I21"])
    print(f"I am going to look up patients who have diagnoses codes {dx_code}")

    # -------------------------
    # Define vital itemIDs
    # -------------------------
    vital_items = {
        "heart_rate": {"220045"},
        "sbp":        {"220179", "225309"},
        "dbp":        {"220180", "225310"},
        "map":        {"220052", "225312"},
        "spo2":       {"220277"},
        "resp_rate":  {"220210"},
        "temp_c":     {"223762"},
        "temp_f":     {"223761"},
        "gcs":        {"223900", "223901", "220739"},
    }

    itemid_to_vital = {}
    for vital_name, item_set in vital_items.items():
        for itemid in item_set:
            itemid_to_vital[itemid] = vital_name

    vital_outlier_bounds = {
        "heart_rate": (0, 300),
        "sbp":        (0, 300),
        "dbp":        (0, 200),
        "map":        (0, 250),
        "spo2":       (0, 100),
        "resp_rate":  (0, 80),
        "temp_c":     (25, 45),
        "temp_f":     (77, 113),
        "gcs":        (3, 15),
    }

    # -------------------------
    # Define lab itemIDs
    # -------------------------
    lab_items = {
        "troponin_i":  {"51002"},
        "troponin_t":  {"51003"},
        "ck":          {"50911"},
        "ck_mb":       {"50910"},
        "creatinine":  {"50912"},
        "bun":         {"51006"},
        "bnp":         {"50963"},
        "nt_probnp":   {"50970"},
        "lactate":     {"50813"},
        "hemoglobin":  {"51222"},
        "hematocrit":  {"51221"},
        "wbc":         {"51301"},
        "sodium":      {"50983"},
        "potassium":   {"50971"},
        "glucose":     {"50931"},
        "inr":         {"51237"},
        "pt":          {"51274"},
        "ph":          {"50820"},
        "bicarbonate": {"50882"},
    }

    itemid_to_lab = {}
    for lab_name, item_set in lab_items.items():
        for itemid in item_set:
            itemid_to_lab[itemid] = lab_name

    lab_outlier_bounds = {
        "troponin_i":  (0, 1000),
        "troponin_t":  (0, 100),
        "ck":          (0, 100000),
        "ck_mb":       (0, 10000),
        "creatinine":  (0, 50),
        "bun":         (0, 300),
        "bnp":         (0, 50000),
        "nt_probnp":   (0, 100000),
        "lactate":     (0, 30),
        "hemoglobin":  (0, 25),
        "hematocrit":  (0, 75),
        "wbc":         (0, 200),
        "sodium":      (100, 200),
        "potassium":   (1, 15),
        "glucose":     (0, 2000),
        "inr":         (0, 20),
        "pt":          (0, 200),
        "ph":          (6.5, 8.0),
        "bicarbonate": (0, 60),
    }

    # -------------------------
    # Lookup dictionaries
    # -------------------------
    gender_dict = {}
    race_dict = {}
    age_dict = {}

    gender_dict["M"] = "Male"
    gender_dict["F"] = "Female"

    race_dict["AMERICAN INDIAN/ALASKA NATIVE"] = "American Indian/Alaska Native"
    race_dict["ASIAN"] = "Asian"
    race_dict["ASIAN - ASIAN INDIAN"] = "Asian"
    race_dict["ASIAN - CHINESE"] = "Asian"
    race_dict["ASIAN - KOREAN"] = "Asian"
    race_dict["ASIAN - SOUTH EAST ASIAN"] = "Asian"
    race_dict["BLACK/AFRICAN"] = "Black"
    race_dict["BLACK/AFRICAN AMERICAN"] = "Black"
    race_dict["BLACK/CAPE VERDEAN"] = "Black"
    race_dict["BLACK/CARIBBEAN ISLAND"] = "Black"
    race_dict["HISPANIC/LATINO - CENTRAL AMERICAN"] = "Hispanic/Latino"
    race_dict["HISPANIC/LATINO - COLUMBIAN"] = "Hispanic/Latino"
    race_dict["HISPANIC/LATINO - CUBAN"] = "Hispanic/Latino"
    race_dict["HISPANIC/LATINO - DOMINICAN"] = "Hispanic/Latino"
    race_dict["HISPANIC/LATINO - GUATEMALAN"] = "Hispanic/Latino"
    race_dict["HISPANIC/LATINO - HONDURAN"] = "Hispanic/Latino"
    race_dict["HISPANIC/LATINO - MEXICAN"] = "Hispanic/Latino"
    race_dict["HISPANIC/LATINO - PUERTO RICAN"] = "Hispanic/Latino"
    race_dict["HISPANIC/LATINO - SALVADORAN"] = "Hispanic/Latino"
    race_dict["HISPANIC OR LATINO"] = "Hispanic/Latino"
    race_dict["MULTIPLE RACE/ETHNICITY"] = "Multiple Race/Ethnicity"
    race_dict["NATIVE HAWAIIAN OR OTHER PACIFIC ISLANDER"] = "Native Hawaiian or other Pacific Islander"
    race_dict["OTHER"] = "Other"
    race_dict["PATIENT DECLINED TO ANSWER"] = "Unknown"
    race_dict["PORTUGESE"] = "White"
    race_dict["PORTUGUESE"] = "White"
    race_dict["SOUTH AMERICAN"] = "Hispanic/Latino"
    race_dict["UNABLE TO OBTAIN"] = "Unknown"
    race_dict["UNKNOWN"] = "Unknown"
    race_dict["WHITE"] = "White"
    race_dict["WHITE - BRAZILIAN"] = "White"
    race_dict["WHITE - EASTERN EUROPEAN"] = "White"
    race_dict["WHITE - OTHER EUROPEAN"] = "White"
    race_dict["WHITE - RUSSIAN"] = "White"

    for age in range(18, 26):
        age_dict[age] = "Young Adult"
    for age in range(26, 40):
        age_dict[age] = "Adult"
    for age in range(40, 65):
        age_dict[age] = "Middle-age Adult"
    for age in range(65, 200):
        age_dict[age] = "Senior"

    # Define comorbidity prefixes
    comorbidity_prefixes = {
        "hypertension":  ["401", "I10"],
        "diabetes":      ["250", "E10", "E11", "E13"],
        "ckd":           ["585", "N18"],
        "heart_failure": ["428", "I50"],
        "past_mi":       ["412", "I252"],
        "copd":          ["496", "491", "492", "J44"],
    }

    # -------------------------
    # STEP 1: Find MI admissions
    # -------------------------
    mi_admission_dict = {}

    with open(diagnoses_file_name, "r", newline="") as diagnoses_file:
        diagnoses_reader = csv.DictReader(diagnoses_file)

        for row in diagnoses_reader:
            subject_id = row["subject_id"].strip()
            hadm_id = row["hadm_id"].strip()
            icd_code = row["icd_code"].strip()

            if icd_code.startswith("410") or icd_code.startswith("I21"):
                if subject_id not in mi_admission_dict:
                    mi_admission_dict[subject_id] = hadm_id

    print(f"A total of {len(mi_admission_dict)} patient ids was found with diagnoses codes {dx_code}")

    # -------------------------
    # STEP 1b: Find comorbidities for MI patients
    # -------------------------
    comorbidity_dict = {
        subject_id: {key: False for key in comorbidity_prefixes}
        for subject_id in mi_admission_dict
    }

    with open(diagnoses_file_name, "r", newline="") as diagnoses_file:
        diagnoses_reader = csv.DictReader(diagnoses_file)

        for row in diagnoses_reader:
            subject_id = row["subject_id"].strip()

            if subject_id not in mi_admission_dict:
                continue

            icd_code = row["icd_code"].strip()

            for condition, prefixes in comorbidity_prefixes.items():
                if any(icd_code.startswith(p) for p in prefixes):
                    comorbidity_dict[subject_id][condition] = True

    # -------------------------
    # STEP 2: Pull demographics from patients.csv
    # -------------------------
    patient_demo_dict = {}

    with open(patients_file_name, "r", newline="") as patients_file:
        patients_reader = csv.DictReader(patients_file)

        for row in patients_reader:
            subject_id = row["subject_id"].strip()

            if subject_id in mi_admission_dict:
                gender_code = row["gender"].strip()
                anchor_age_code = int(row["anchor_age"])

                gender_string = gender_dict.get(gender_code, "Unknown")
                anchor_age_string = age_dict.get(anchor_age_code, "Unknown")
                # NEW
                anchor_year_group = row["anchor_year_group"].strip()

                patient_demo_dict[subject_id] = {
                    "gender": gender_string,
                    "age": anchor_age_string,
                    "anchor_year_group": anchor_year_group      # NEW
                }

    # -------------------------
    # STEP 3: Pull MI admission details
    # -------------------------
    mi_visit_dict = {}

    with open(admissions_file_name, "r", newline="") as admissions_file:
        admissions_reader = csv.DictReader(admissions_file)

        for row in admissions_reader:
            subject_id = row["subject_id"].strip()
            hadm_id = row["hadm_id"].strip()

            if subject_id in mi_admission_dict and hadm_id == mi_admission_dict[subject_id]:
                insurance_code = row["insurance"].strip()
                race_code = row["race"].strip()
                hospital_expire_flag = row["hospital_expire_flag"].strip()
                admittime = row["admittime"].strip()

                # NEW: admission type and location
                admission_type = row["admission_type"].strip()
                admission_location = row["admission_location"].strip()

                 # NEW: derive hour and day of week from admittime
                try:
                    admit_dt = datetime.strptime(admittime, "%Y-%m-%d %H:%M:%S")
                    admit_hour = admit_dt.hour
                    admit_day_of_week = admit_dt.strftime("%A")
                except ValueError:
                    admit_hour = None
                    admit_day_of_week = None

                mi_visit_dict[subject_id] = {
                    "hadm_id": hadm_id,
                    "insurance": insurance_code,
                    "race": race_code,
                    "hospital_expire_flag": hospital_expire_flag,
                    "admittime": admittime,
                    "admission_type": admission_type,           # NEW
                    "admission_location": admission_location,   # NEW
                    "admit_hour": admit_hour,                   # NEW
                    "admit_day_of_week": admit_day_of_week      # NEW
                }
                

    # -------------------------
    # STEP 3b: Extract vitals from first 24h via streamed grep
    # -------------------------
    print("Reading chartevents (this may take a while)...")

    vital_raw = {subject_id: {vital: [] for vital in vital_items} for subject_id in mi_visit_dict}

    itemid_pattern = "|".join(itemid_to_vital.keys())

    proc = subprocess.Popen(
        ["grep", "-E", f"(^subject_id|{itemid_pattern})", chartevents_file_name],
        stdout=subprocess.PIPE
    )

    chart_reader = csv.DictReader(io.TextIOWrapper(proc.stdout, encoding="utf-8"))

    for row in chart_reader:
        subject_id = row["subject_id"].strip()

        if subject_id not in mi_visit_dict:
            continue

        itemid = row["itemid"].strip()

        if itemid not in itemid_to_vital:
            continue

        admittime_str = mi_visit_dict[subject_id]["admittime"]
        charttime_str = row["charttime"].strip()

        try:
            admittime = datetime.strptime(admittime_str, "%Y-%m-%d %H:%M:%S")
            charttime = datetime.strptime(charttime_str, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            continue

        hours_since_admit = (charttime - admittime).total_seconds() / 3600
        if hours_since_admit < 0 or hours_since_admit > 24:
            continue

        value_str = row["valuenum"].strip()
        if value_str == "":
            continue

        try:
            value = float(value_str)
        except ValueError:
            continue

        vital_name = itemid_to_vital[itemid]
        lo, hi = vital_outlier_bounds[vital_name]
        if not (lo <= value <= hi):
            continue

        vital_raw[subject_id][vital_name].append((charttime, value))

    proc.wait()

    # Compute per-patient vital summary stats
    vital_summary = {}

    for subject_id, vitals in vital_raw.items():
        vital_summary[subject_id] = {}

        for vital_name, readings in vitals.items():
            if len(readings) == 0:
                vital_summary[subject_id][vital_name + "_mean"]  = None
                vital_summary[subject_id][vital_name + "_min"]   = None
                vital_summary[subject_id][vital_name + "_max"]   = None
                vital_summary[subject_id][vital_name + "_first"] = None
                vital_summary[subject_id][vital_name + "_last"]  = None
                vital_summary[subject_id][vital_name + "_n"]     = 0
            else:
                readings_sorted = sorted(readings, key=lambda x: x[0])
                values = [v for _, v in readings_sorted]

                vital_summary[subject_id][vital_name + "_mean"]  = round(sum(values) / len(values), 2)
                vital_summary[subject_id][vital_name + "_min"]   = min(values)
                vital_summary[subject_id][vital_name + "_max"]   = max(values)
                vital_summary[subject_id][vital_name + "_first"] = values[0]
                vital_summary[subject_id][vital_name + "_last"]  = values[-1]
                vital_summary[subject_id][vital_name + "_n"]     = len(values)

    print("Vitals extraction complete.")

    # -------------------------
    # STEP 3c: Extract labs from first 24h via streamed grep
    # -------------------------
    print("Reading labevents (this may take a while)...")

    lab_raw = {subject_id: {lab: [] for lab in lab_items} for subject_id in mi_visit_dict}

    lab_itemid_pattern = "|".join(itemid_to_lab.keys())

    # Get header line separately
    with open(labevents_file_name, "r") as lab_header_file:
        lab_header = lab_header_file.readline().strip().split(",")

    lab_proc = subprocess.Popen(
        ["grep", "-E", f",{lab_itemid_pattern},", labevents_file_name],
        stdout=subprocess.PIPE
    )

    lab_reader = csv.DictReader(
        io.TextIOWrapper(lab_proc.stdout, encoding="utf-8"),
        fieldnames=lab_header
    )

    for row in lab_reader:
        subject_id = row["subject_id"].strip()

        if subject_id not in mi_visit_dict:
            continue

        itemid = row["itemid"].strip()

        if itemid not in itemid_to_lab:
            continue

        admittime_str = mi_visit_dict[subject_id]["admittime"]
        charttime_str = row["charttime"].strip()

        try:
            admittime = datetime.strptime(admittime_str, "%Y-%m-%d %H:%M:%S")
            charttime = datetime.strptime(charttime_str, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            continue

        hours_since_admit = (charttime - admittime).total_seconds() / 3600
        if hours_since_admit < 0 or hours_since_admit > 24:
            continue

        value_str = row["valuenum"].strip()
        if value_str == "":
            continue

        try:
            value = float(value_str)
        except ValueError:
            continue

        lab_name = itemid_to_lab[itemid]
        lo, hi = lab_outlier_bounds[lab_name]
        if not (lo <= value <= hi):
            continue

        lab_raw[subject_id][lab_name].append((charttime, value))

    lab_proc.wait()

    # Compute per-patient lab summary stats
    lab_summary = {}

    for subject_id, labs in lab_raw.items():
        lab_summary[subject_id] = {}

        for lab_name, readings in labs.items():
            if len(readings) == 0:
                lab_summary[subject_id][lab_name + "_mean"]  = None
                lab_summary[subject_id][lab_name + "_min"]   = None
                lab_summary[subject_id][lab_name + "_max"]   = None
                lab_summary[subject_id][lab_name + "_first"] = None
                lab_summary[subject_id][lab_name + "_last"]  = None
                lab_summary[subject_id][lab_name + "_n"]     = 0
            else:
                readings_sorted = sorted(readings, key=lambda x: x[0])
                values = [v for _, v in readings_sorted]

                lab_summary[subject_id][lab_name + "_mean"]  = round(sum(values) / len(values), 2)
                lab_summary[subject_id][lab_name + "_min"]   = min(values)
                lab_summary[subject_id][lab_name + "_max"]   = max(values)
                lab_summary[subject_id][lab_name + "_first"] = values[0]
                lab_summary[subject_id][lab_name + "_last"]  = values[-1]
                lab_summary[subject_id][lab_name + "_n"]     = len(values)

    print("Labs extraction complete.")

    # -------------------------
    # STEP 3d: ICU admission flag
    # -------------------------
    icustays_file_name = "/oscar/data/shared/ursa/mimic-iv/icu/3.1/icustays.csv"

    icu_set = set()

    with open(icustays_file_name, "r", newline="") as icu_file:
        icu_reader = csv.DictReader(icu_file)

        for row in icu_reader:
            subject_id = row["subject_id"].strip()
            hadm_id = row["hadm_id"].strip()

            # Only flag if ICU stay is tied to the MI admission
            if subject_id in mi_visit_dict and hadm_id == mi_visit_dict[subject_id]["hadm_id"]:
                icu_set.add(subject_id)

    print(f"MI patients with ICU admission: {len(icu_set)}")

    # -------------------------
    # STEP 4: Split into died vs survived
    # -------------------------
    died_set = set()
    survived_set = set()

    for subject_id in mi_visit_dict:
        expire_flag = mi_visit_dict[subject_id]["hospital_expire_flag"]

        if expire_flag == "1":
            died_set.add(subject_id)
        elif expire_flag == "0":
            survived_set.add(subject_id)

    print(f"MI patients who died during MI hospitalization: {len(died_set)}")
    print(f"MI patients who survived MI hospitalization: {len(survived_set)}")

    # -------------------------
    # STEP 5: Helper function to count demographics
    # -------------------------
    def count_stats(subject_set):
        gender_count_dict = {}
        age_count_dict = {}
        race_count_dict = {}
        insurance_count_dict = {}
        comorbidity_count_dict = {key: 0 for key in comorbidity_prefixes}

        admission_type_count_dict = {}
        admission_location_count_dict = {}
        admit_hour_count_dict = {}
        admit_day_count_dict = {}
        anchor_year_group_count_dict = {}
        icu_count = 0

        vital_keys = [
            vname + suffix
            for vname in vital_items
            for suffix in ("_mean", "_min", "_max", "_first", "_last")
        ]
        vital_agg = {k: [] for k in vital_keys}

        lab_keys = [
            lname + suffix
            for lname in lab_items
            for suffix in ("_mean", "_min", "_max", "_first", "_last")
        ]
        lab_agg = {k: [] for k in lab_keys}

        for subject_id in subject_set:
            if subject_id not in patient_demo_dict:
                continue
            if subject_id not in mi_visit_dict:
                continue

            gender_string = patient_demo_dict[subject_id]["gender"]
            age_string = patient_demo_dict[subject_id]["age"]
            race_code = mi_visit_dict[subject_id]["race"]
            insurance_string = mi_visit_dict[subject_id]["insurance"]
            race_string = race_dict.get(race_code, "Unknown")

            # Gender
            if gender_string in gender_count_dict:
                gender_count_dict[gender_string] += 1
            else:
                gender_count_dict[gender_string] = 1

            # Age
            if age_string in age_count_dict:
                age_count_dict[age_string] += 1
            else:
                age_count_dict[age_string] = 1

            # Race
            if race_string in race_count_dict:
                race_count_dict[race_string] += 1
            else:
                race_count_dict[race_string] = 1

            # Insurance
            if insurance_string in insurance_count_dict:
                insurance_count_dict[insurance_string] += 1
            else:
                insurance_count_dict[insurance_string] = 1

            # Comorbidities
            if subject_id in comorbidity_dict:
                for condition, has_it in comorbidity_dict[subject_id].items():
                    if has_it:
                        comorbidity_count_dict[condition] += 1

            # Vitals
            if subject_id in vital_summary:
                for k in vital_keys:
                    val = vital_summary[subject_id].get(k)
                    if val is not None:
                        vital_agg[k].append(val)

         # Labs
            if subject_id in lab_summary:
                for k in lab_keys:
                    val = lab_summary[subject_id].get(k)
                    if val is not None:
                        lab_agg[k].append(val)

            # Admission type  <-- ALL OF THESE ARE NOW INDENTED INSIDE THE LOOP
            admission_type = mi_visit_dict[subject_id]["admission_type"]
            if admission_type in admission_type_count_dict:
                admission_type_count_dict[admission_type] += 1
            else:
                admission_type_count_dict[admission_type] = 1

            # Admission location
            admission_location = mi_visit_dict[subject_id]["admission_location"]
            if admission_location in admission_location_count_dict:
                admission_location_count_dict[admission_location] += 1
            else:
                admission_location_count_dict[admission_location] = 1

            # Admit hour
            admit_hour = mi_visit_dict[subject_id]["admit_hour"]
            if admit_hour is not None:
                if admit_hour in admit_hour_count_dict:
                    admit_hour_count_dict[admit_hour] += 1
                else:
                    admit_hour_count_dict[admit_hour] = 1

            # Admit day of week
            admit_day = mi_visit_dict[subject_id]["admit_day_of_week"]
            if admit_day is not None:
                if admit_day in admit_day_count_dict:
                    admit_day_count_dict[admit_day] += 1
                else:
                    admit_day_count_dict[admit_day] = 1

            # Anchor year group
            anchor_year_group = patient_demo_dict[subject_id]["anchor_year_group"]
            if anchor_year_group in anchor_year_group_count_dict:
                anchor_year_group_count_dict[anchor_year_group] += 1
            else:
                anchor_year_group_count_dict[anchor_year_group] = 1

            # ICU flag
            if subject_id in icu_set:
                icu_count += 1

        # These stay OUTSIDE the loop — they summarize after all patients processed
        vital_group_summary = {}
        for k, vals in vital_agg.items():
            if len(vals) > 0:
                vital_group_summary[k] = round(sum(vals) / len(vals), 2)
            else:
                vital_group_summary[k] = None

        lab_group_summary = {}
        for k, vals in lab_agg.items():
            if len(vals) > 0:
                lab_group_summary[k] = round(sum(vals) / len(vals), 2)
            else:
                lab_group_summary[k] = None

        return (
            gender_count_dict,
            age_count_dict,
            race_count_dict,
            insurance_count_dict,
            comorbidity_count_dict,
            vital_group_summary,
            lab_group_summary,
            admission_type_count_dict,
            admission_location_count_dict,
            admit_hour_count_dict,
            admit_day_count_dict,
            anchor_year_group_count_dict,
            icu_count
        )

    
    (
        died_gender_count_dict,
        died_age_count_dict,
        died_race_count_dict,
        died_insurance_count_dict,
        died_comorbidity_count_dict,
        died_vital_group_summary,
        died_lab_group_summary,
        died_admission_type_count_dict,
        died_admission_location_count_dict,
        died_admit_hour_count_dict,
        died_admit_day_count_dict,
        died_anchor_year_group_count_dict,
        died_icu_count
    ) = count_stats(died_set)

    (
        survived_gender_count_dict,
        survived_age_count_dict,
        survived_race_count_dict,
        survived_insurance_count_dict,
        survived_comorbidity_count_dict,
        survived_vital_group_summary,
        survived_lab_group_summary,
        survived_admission_type_count_dict,
        survived_admission_location_count_dict,
        survived_admit_hour_count_dict,
        survived_admit_day_count_dict,
        survived_anchor_year_group_count_dict,
        survived_icu_count
    ) = count_stats(survived_set)  

    # -------------------------
    # STEP 6: Print output
    # -------------------------
    print("\nDIED DURING MI VISIT")
    print("--------------------")

    print("Gender:")
    for gender in died_gender_count_dict:
        print(f"  {gender}|{died_gender_count_dict[gender]}")

    print("\nAge:")
    for age in died_age_count_dict:
        print(f"  {age}|{died_age_count_dict[age]}")

    print("\nRace:")
    for race in died_race_count_dict:
        print(f"  {race}|{died_race_count_dict[race]}")

    print("\nInsurance:")
    for insurance in died_insurance_count_dict:
        print(f"  {insurance}|{died_insurance_count_dict[insurance]}")

    print("\nComorbidities:")
    for condition in died_comorbidity_count_dict:
        print(f"  {condition}|{died_comorbidity_count_dict[condition]}")

    print("\nVitals (group averages over first 24h):")
    for stat, val in died_vital_group_summary.items():
        print(f"  {stat}|{val}")

    print("\nLabs (group averages over first 24h):")
    for stat, val in died_lab_group_summary.items():
        print(f"  {stat}|{val}")
    
    
    print("\nAdmission Type:")
    for atype, count in died_admission_type_count_dict.items():
        print(f"  {atype}|{count}")

    print("\nAdmission Location:")
    for aloc, count in died_admission_location_count_dict.items():
        print(f"  {aloc}|{count}")

    print("\nAdmit Hour:")
    for hour in sorted(died_admit_hour_count_dict.keys()):
        print(f"  {hour}|{died_admit_hour_count_dict[hour]}")

    print("\nAdmit Day of Week:")
    for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]:
        print(f"  {day}|{died_admit_day_count_dict.get(day, 0)}")

    print("\nAnchor Year Group:")
    for ygroup, count in died_anchor_year_group_count_dict.items():
        print(f"  {ygroup}|{count}")

    print(f"\nICU Admission: {died_icu_count}")



    print("\nSURVIVED MI VISIT")
    print("-----------------")

    print("Gender:")
    for gender in survived_gender_count_dict:
        print(f"  {gender}|{survived_gender_count_dict[gender]}")

    print("\nAge:")
    for age in survived_age_count_dict:
        print(f"  {age}|{survived_age_count_dict[age]}")

    print("\nRace:")
    for race in survived_race_count_dict:
        print(f"  {race}|{survived_race_count_dict[race]}")

    print("\nInsurance:")
    for insurance in survived_insurance_count_dict:
        print(f"  {insurance}|{survived_insurance_count_dict[insurance]}")

    print("\nComorbidities:")
    for condition in survived_comorbidity_count_dict:
        print(f"  {condition}|{survived_comorbidity_count_dict[condition]}")

    print("\nVitals (group averages over first 24h):")
    for stat, val in survived_vital_group_summary.items():
        print(f"  {stat}|{val}")

    print("\nLabs (group averages over first 24h):")
    for stat, val in survived_lab_group_summary.items():
        print(f"  {stat}|{val}")

    print("\nAdmission Type:")
    for atype, count in survived_admission_type_count_dict.items():
        print(f"  {atype}|{count}")

    print("\nAdmission Location:")
    for aloc, count in survived_admission_location_count_dict.items():
        print(f"  {aloc}|{count}")

    print("\nAdmit Hour:")
    for hour in sorted(survived_admit_hour_count_dict.keys()):
        print(f"  {hour}|{survived_admit_hour_count_dict[hour]}")

    print("\nAdmit Day of Week:")
    for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]:
        print(f"  {day}|{survived_admit_day_count_dict.get(day, 0)}")

    print("\nAnchor Year Group:")
    for ygroup, count in survived_anchor_year_group_count_dict.items():
        print(f"  {ygroup}|{count}")

    print(f"\nICU Admission: {survived_icu_count}")


# Call main function
main()