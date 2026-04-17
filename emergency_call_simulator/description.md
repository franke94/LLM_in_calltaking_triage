# Emergency call simulator

Working with real emergency data carries a huge legal burden. While some research is conducted using real calls, in most cases the raw data is not published. 
To enable unrestricted work with emergency calls, we used AI support to generate synthetic emergency calls. For traceability purposes, the code and prompts used to generate the data are included in this repository.

Personal data such as names, addresses, and medical histories are randomised and are the output of the LLM used (GPT 5.2). 

## Case distribution 

The aim is to generate calls that are as realistic as possible.
The rough distribution of cases should follow a realistic distribution, with the number of cases allocated to each category reflecting the actual number of cases in the german EMS. This applies to both case numbers and severity levels. 
Due to a lack of real data, we used the study by Sefrin et al. (2025) on the distribution of emergency cases within the German Red Cross. 
Although this data is from 2014 and only covers 3,127 cases, clear divisions between different case and severity groups can be seen.

The data preprocessing is shown in cases_generation.py. A case and severity distribution table was derived from the study data. 
To differentiate between different severity scores, the NACA-Store (National Advisory Committee for Aeronautics) is used, as well as in the studies by Sefrin et al. (2015) and Gonvers et al. (2020). 

| NACA | Description | Clinical Meaning |
|------|------------|------------------|
| I | Minor disturbance | Minor illness or injury; no medical treatment required |
| II | Slight to moderate disturbance | Medical evaluation needed, but no acute threat |
| III | Moderate disturbance | Requires hospital treatment; not life-threatening |
| IV | Severe disturbance | Potentially life-threatening condition |
| V | Acute threat to life | Life-threatening condition requiring immediate intervention |
| VI | Resuscitation | Cardiac or respiratory arrest; resuscitation in progress |
| VII | Death | Fatal injury or illness |

Sefrin et al. (2015) classified most of the data into just two categories: NACA I-III and NACA IV-VII. 
To enable a finer distribution, we attempted to derive a more detailed classification (NACA I-II, NACA III, NACA IV-V and NACA VI-VII).
According to the cases described by Sefrin et al. (2015), the probability of NACA I-II in the NACA I-III category is 565/(1934+565) ≈ 0.45, and the probability of NACA VI-VII is 40/565 ≈ 0.07.
## Case generation 

Due to our experience, it is useful to take a step prior to generating actual calls in order to generate a higher degree of realism. 
Regarding the case distribution, we generated a set of cases using OpenAI's GPT-5.2. The prompt can be found in cases_generation.py.
Due to the work with German emergency calls being respected, the cases are generated in German.
The output is a short case descriptions without diagnoses or treatments, but with detailed descriptions of the symptoms and situation.

The cases are found in the folder cases. 


## Emergency call generation

The actual cases are then used to generate emergency calls. The emergency call generation is shown in emergency_call.py.

``````
python3 emergency_call.py casenumber       (For german version)

python3 emergency_call_en.py casenumber    (For englisch version)
``````

The used model is the caller, the user is the calltaker.

*/end*
ends the process and saves the emergency call as a markdown in emergency_calls folder. 

## Evaluation 
The test cases are generated with the following vales: 


The generated calls are evaluated by two medical experts (german paramedics "Notfallsanitäter" with a background in emergency call centers). The evaluation is based on the call transcript.
So far the evaluation is based on the ABCDE-scheme that is used to get a quick overview of the patient's situation. (Michael 2025)

| Step | Focus |
|------|--------|
| **A** | Airway |
| **B** | Breathing |
| **C** | Circulation |
| **D** | Disability |
| **E** | Exposure |

The severity is categorized in a 4-point scale (0-3) based on the information given in the call.

| Severity | Description |
|----------|-------------|
| **0** | No information available; no conclusions possible |
| **1** | No or only minor impairment suspected; patient can speak clearly and reports no distress |
| **2** | Significant impairment present; no acute life threat suspected (ambulance indicated) |
| **3** | Severe impairment; vital threat possible or likely; immediate intervention required (urgent ambulance, possibly physician response unit) |


A deeper description of the evaluation process and the guidelines for the ABCDE-analysis can be found in abcde_guidelines.md.
The steps are based on different german guidelines when to alarm an emergency physician ("Notarzt"):
- Notarztindikationskatalog als Handlungsempfehlung für Disponenten in Rettungsleitstellen - Deutscher Berufsverband Rettungsdienst e. V. (2024) https://dbrd.de/images/NAIK/DBRD_NAIK24_Web.pdf (last accessed 22.02.2026)
- Notarztindikationskatalog Hessen (2024) https://familie.hessen.de/sites/familie.hessen.de/files/2024-09/2024-09-20_notarztindikationskatalog_2024.pdf (last accessed 22.02.2026)
- Empfehlungen für einen Indikationskatalog für den Notarzteinsatz Handreichung für Disponenten in Rettungsleitstellen und Notdienstzentralen (NAIK) - Bundesärztekammer (2023) https://www.bundesaerztekammer.de/fileadmin/user_upload/wissenschaftlicher-beirat/Veroeffentlichungen/Bek_BAEK_Empfehlungen_fuer_einen_Indikationskatalog_fuer_den_Notarzteinsatz_NAIK_.pdf (last accessed 22.02.2026)


## Sources

    Sefrin, P., Händlmeyer, A. & Kast, W. Leistungen des Notfall-Rettungsdienstes.  Notarzt 31, S34–S48 (2015).

    Gonvers, E., Spichiger, T., Albrecht, E. & Dami, F. Use of peripheral vascular access in the prehospital setting: is there room for improvement? BMC Emerg. Med. 20, 46 (2020).

    Michael, M. ABCDE-Schema bei akut vitalbedrohten Notfallpatienten. in Klinische Akut- und Notfallmedizin (eds. Gries, A., Seekamp, A., Christ, M. & Dodt, C.) (MWV Medizinisch Wissenschaftliche Verlagsgesellschaft, 2025).
  

  

  
