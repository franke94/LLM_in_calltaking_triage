# B – Breathing Assessment Guidelines
Context: Analysis of transcribed emergency calls

## Purpose
Assess breathing effectiveness and oxygenation.

## What to Evaluate
- breathing difficulty
- breathing effort and speed
- speech ability
- signs of oxygen deficiency

## Caller Language Indicators

### Normal
- breathing normal
- speaking normally
- no shortness of breath

### Mild / Moderate Impairment
- shortness of breath
- breathing fast
- cannot lie flat
- chest tightness# B – Breathing Assessment (LLM Instruction)

## Context  
Analyze transcribed emergency calls to assess breathing status (exclude airway and circulation).

## Goal  
Identify if breathing is normal, impaired, or critically compromised based on caller descriptions.

## Key Notes  
- Assess only **breathing** (rate, effort, pattern, speech).  
- A patient who is alert and speaks in full sentences usually has **normal breathing**.  
- Impaired breathing can include shortness of breath, fatigue, or abnormal sounds (e.g. wheezing).  
- If evidence is unclear, infer cautiously and reflect uncertainty in the confidence score.  

## Severity Scale  
| Severity | Description |
|-----------|--------------|
| **0** | No information or no conclusion possible |
| **1** | Normal or minor impairment; no immediate intervention needed |
| **2** | Significant impairment; requires ambulance intervention |
| **3** | Critical or life-threatening breathing problem; needs ambulance + emergency physician |

## Example Indicators  

### Severity 1  
- No breathing issues reported  
- Patient speaks clearly and in full sentences  
- Only mild cold or irritation without vital threat  

### Severity 2  
- Mild shortness of breath (e.g. COPD, asthma) without acute danger  
- Hyperventilation due to stress or emotional cause  
- Slowly developing dyspnea without vital compromise  

### Severity 3  
- Severe shortness of breath with one- or two‑word speech, confusion, or bluish lips  
- Exhausted patient unable to hold head upright or remain seated  
- Unresponsive or cyanotic patient, no reaction to voice or pain  
- Chest pain with shortness of breath after chest trauma  
- Respiratory arrest or ongoing resuscitation  

## Confidence Score  
- Range: **0.0–1.0**  
- High confidence = explicit transcript evidence  
- Low confidence = ambiguous or indirect signs  
- Wrong judgement with high confidence = severe penalty  
