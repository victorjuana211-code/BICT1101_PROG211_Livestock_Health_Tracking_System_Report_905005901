# Livestock Health & Tracking System

A simple, open-source Python program that helps farmers and community animal-health workers keep a digital register of their animals, record health events and see which animals need attention.

Built for **PROG211 – Object-Oriented Programming 1** (Limkokwing University of Creative Technology, Sierra Leone) – *Real-World Solutions under DPG Standards*. Domain: **Agriculture**.

## Features
- Register animals with a validated tag ID (e.g. `CT-001`)
- View, search and update animals (status, weight)
- Add health records (condition, treatment, new status)
- Record vaccinations and see which are due
- Alert list of sick animals or animals with vaccines due
- Herd summary by health status

## Requirements
Python 3.8 or newer. No external libraries – standard library only.

## How to run
```bash
python livestock_tracker.py          # interactive menu
python livestock_tracker.py --demo   # automatic demonstration with sample data
```

## OOP concepts used
| Concept | Where |
|---|---|
| Classes & objects | `HealthRecord`, `Animal`, `LivestockRegistry` |
| Attributes | `tag_id`, `species`, `breed`, `age_months`, `weight_kg`, `health_status` ... |
| Data structure | **Dictionary**: tag ID → `Animal` object (`LivestockRegistry.animals`) |
| Instance methods | `add_health_record()`, `update_status()`, `update_weight()`, `record_vaccination()`, `vaccinations_due()`, `display_info()` |
| Class methods | `Animal.get_total_animals()`, `Animal.from_csv_line()`, `LivestockRegistry.supported_species()` |
| Static methods | `Animal.is_valid_tag()`, `Animal.months_between()` |
| Tuples (bonus) | `SPECIES`, `HEALTH_STATUSES`, `VACCINE_SCHEDULE` |

## How this solution aligns with Digital Public Goods (DPG) standards
| DPG principle | How it is met |
|---|---|
| **Open-source** | Plain Python, standard library only, published on GitHub for anyone to read, use and improve. |
| **Inclusive & accessible design** | Simple numbered text menu, plain-language prompts, clear error messages, runs on low-spec computers with no internet. |
| **Privacy-respecting** | Stores **animal data only**. No farmer names, phone numbers, addresses or ID numbers. Farms are identified by an anonymous code (e.g. `FARM-01`). |
| **Modular & reusable** | One class per responsibility; the classes can be reused with a web, mobile or database front end. |

## Example usage (sample output)
```text
$ python livestock_tracker.py --demo
  TAG     SPECIES  BREED         AGE(m)  KG     STATUS
  --------------------------------------------------------------
  CT-001  Cattle   Zebu          36      250.0  Healthy
  CT-002  Cattle   N'Dama        48      270.0  Sick
  GT-001  Goat     West African  18      32.0   Healthy
  SH-001  Sheep    Djallonke     24      30.0   Healthy

--- Animals needing attention ---
  CT-002 (Cattle) - status: Sick
      vaccine due: Anthrax (never given)
      vaccine due: Foot-and-Mouth Disease (never given)
```

## Sample input (interactive menu)
```text
Choose an option: 1
  Tag ID (e.g. CT-001): CT-001
  Choose species number: 1
  Breed: Zebu
  Age in months: 36
  Weight in kg: 250
  Animal CT-001 registered successfully.
```

## Disclaimer
The vaccine schedule is a simplified teaching example. Always confirm real schedules and treatments with a qualified veterinary officer.

## Licence
MIT Licence – free to use, modify and share.
