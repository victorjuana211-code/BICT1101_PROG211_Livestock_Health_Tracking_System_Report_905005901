"""
Livestock Health & Tracking System
==================================
PROG211 - Object-Oriented Programming 1 (Assignment: Real-World Solutions
under DPG Standards)

Domain  : Agriculture
Problem : Smallholder farmers and community animal-health workers often track
          animal health on paper, so vaccinations are missed and sick animals
          are noticed late. This program keeps a simple digital register of
          animals, their health events and their vaccination status.

OOP concepts used
-----------------
* Classes, attributes and objects : HealthRecord, Animal, LivestockRegistry
* Python data structure           : a DICTIONARY (tag ID -> Animal object)
* Instance methods                : Animal.add_health_record(), display_info() ...
* Class methods                   : Animal.get_total_animals(), Animal.from_csv_line()
* Static methods                  : Animal.is_valid_tag(), Animal.months_between()
* Tuples (bonus)                  : SPECIES, HEALTH_STATUSES, VACCINE_SCHEDULE

Digital Public Goods (DPG) principles
-------------------------------------
* Open source        : plain Python, standard library only, hosted on GitHub.
* Accessible design  : numbered text menu, clear prompts, readable messages.
* Privacy-respecting : stores animal data only - no farmer names, phone
                       numbers, addresses or other personal information.
* Modular & reusable : each class has one job and can be reused in other
                       programs (for example a web or mobile front end).

Run:  python livestock_tracker.py          (interactive menu)
      python livestock_tracker.py --demo   (automatic demonstration)
"""

import re
import sys
from datetime import date

# ---------------------------------------------------------------------------
# TUPLES (immutable reference data that must never change while running)
# ---------------------------------------------------------------------------
SPECIES = ("Cattle", "Goat", "Sheep", "Pig", "Chicken")

HEALTH_STATUSES = ("Healthy", "Under Observation", "Sick", "Recovering",
                   "Quarantined")

# (species, vaccine, repeat interval in months) - simplified teaching schedule.
# Real schedules must be confirmed with a qualified veterinary officer.
VACCINE_SCHEDULE = (
    ("Cattle", "Anthrax", 12),
    ("Cattle", "Foot-and-Mouth Disease", 6),
    ("Goat", "PPR", 12),
    ("Goat", "Anthrax", 12),
    ("Sheep", "PPR", 12),
    ("Sheep", "Anthrax", 12),
    ("Pig", "Swine Fever", 6),
    ("Chicken", "Newcastle Disease", 3),
)


# ---------------------------------------------------------------------------
# CLASS 1: HealthRecord - one health event (illness, injury, check-up ...)
# ---------------------------------------------------------------------------
class HealthRecord:
    """A single health event belonging to one animal."""

    def __init__(self, record_id, condition, treatment, record_date=None):
        self.record_id = record_id                    # e.g. 1, 2, 3 ...
        self.condition = condition                    # e.g. "Fever"
        self.treatment = treatment                    # e.g. "Antibiotics"
        self.record_date = record_date or date.today()

    def describe(self):
        """Return the record as one readable line."""
        return (f"#{self.record_id} {self.record_date.isoformat()} | "
                f"{self.condition} | Treatment: {self.treatment}")


# ---------------------------------------------------------------------------
# CLASS 2: Animal - one animal in the register
# ---------------------------------------------------------------------------
class Animal:
    """One animal with its identity, health status and history."""

    # Class attribute shared by ALL Animal objects
    total_animals = 0

    def __init__(self, tag_id, species, breed, age_months, weight_kg):
        self.tag_id = tag_id.upper()
        self.species = species
        self.breed = breed
        self.age_months = age_months
        self.weight_kg = weight_kg
        self.health_status = "Healthy"
        # Dictionaries keep this class consistent with the single data
        # structure chosen for the project.
        self.health_records = {}      # record_id -> HealthRecord
        self.vaccinations = {}        # vaccine name -> date last given
        Animal.total_animals += 1

    # ----------------------------- instance methods ------------------------
    def add_health_record(self, condition, treatment, new_status=None,
                          record_date=None):
        """Create a HealthRecord object and attach it to this animal."""
        record_id = len(self.health_records) + 1
        record = HealthRecord(record_id, condition, treatment, record_date)
        self.health_records[record_id] = record
        if new_status:
            self.update_status(new_status)
        return record

    def update_status(self, new_status):
        """Change the health status (must be one of HEALTH_STATUSES)."""
        if new_status not in HEALTH_STATUSES:
            raise ValueError(f"Status must be one of: {', '.join(HEALTH_STATUSES)}")
        self.health_status = new_status

    def update_weight(self, new_weight_kg):
        """Update the weight after checking the value is sensible."""
        if new_weight_kg <= 0:
            raise ValueError("Weight must be greater than zero.")
        self.weight_kg = new_weight_kg

    def record_vaccination(self, vaccine, given_on=None):
        """Remember the date a vaccine was given."""
        self.vaccinations[vaccine] = given_on or date.today()

    def vaccinations_due(self, today=None):
        """Return a list of (vaccine, reason) tuples that are due now."""
        today = today or date.today()
        due = []
        for species, vaccine, interval in VACCINE_SCHEDULE:
            if species != self.species:
                continue
            last_given = self.vaccinations.get(vaccine)
            if last_given is None:
                due.append((vaccine, "never given"))
            elif Animal.months_between(last_given, today) >= interval:
                due.append((vaccine, f"last given {last_given.isoformat()}"))
        return due

    def needs_attention(self):
        """True when the animal is not healthy or has vaccinations due."""
        return self.health_status != "Healthy" or len(self.vaccinations_due()) > 0

    def display_info(self):
        """Print a full profile of the animal."""
        print(f"  Tag ID  : {self.tag_id}")
        print(f"  Species : {self.species} ({self.breed})")
        print(f"  Age     : {self.age_months} months")
        print(f"  Weight  : {self.weight_kg} kg")
        print(f"  Status  : {self.health_status}")
        if self.vaccinations:
            print("  Vaccines:")
            for vaccine, given in self.vaccinations.items():
                print(f"    - {vaccine} (given {given.isoformat()})")
        else:
            print("  Vaccines: none recorded")
        if self.health_records:
            print("  Health history:")
            for record in self.health_records.values():
                print(f"    {record.describe()}")
        else:
            print("  Health history: none recorded")

    # ----------------------------- class methods ---------------------------
    @classmethod
    def get_total_animals(cls):
        """Return how many Animal objects have been created."""
        return cls.total_animals

    @classmethod
    def from_csv_line(cls, line):
        """Alternative constructor: 'CT-001,Cattle,Zebu,36,250'."""
        tag, species, breed, age, weight = [p.strip() for p in line.split(",")]
        return cls(tag, species, breed, int(age), float(weight))

    # ----------------------------- static methods --------------------------
    @staticmethod
    def is_valid_tag(tag_id):
        """A valid tag looks like CT-001: 2-4 letters, a dash, 3 digits."""
        return re.fullmatch(r"[A-Za-z]{2,4}-\d{3}", tag_id.strip()) is not None

    @staticmethod
    def months_between(start, end):
        """Whole months between two dates."""
        return (end.year - start.year) * 12 + (end.month - start.month)


# ---------------------------------------------------------------------------
# CLASS 3: LivestockRegistry - stores many Animal objects in a DICTIONARY
# ---------------------------------------------------------------------------
class LivestockRegistry:
    """The register for one herd/flock. Uses a dictionary: tag ID -> Animal."""

    def __init__(self, farm_code):
        # An anonymous code such as "FARM-01" is used - never a person's name.
        self.farm_code = farm_code
        self.animals = {}

    def add_animal(self, animal):
        """Add an Animal object; the tag ID is the dictionary key."""
        if not Animal.is_valid_tag(animal.tag_id):
            raise ValueError("Tag ID must look like CT-001 (letters, dash, 3 digits).")
        if animal.species not in SPECIES:
            raise ValueError(f"Species must be one of: {', '.join(SPECIES)}")
        if animal.tag_id in self.animals:
            raise ValueError(f"Tag {animal.tag_id} is already registered.")
        self.animals[animal.tag_id] = animal

    def find_animal(self, tag_id):
        """Return the Animal for a tag, or None if not found."""
        return self.animals.get(tag_id.strip().upper())

    def display_all(self):
        """Print a compact table of every animal."""
        if not self.animals:
            print("  No animals registered yet.")
            return
        print(f"  {'TAG':<8}{'SPECIES':<9}{'BREED':<14}{'AGE(m)':<8}"
              f"{'KG':<7}{'STATUS'}")
        print("  " + "-" * 62)
        for tag, a in self.animals.items():
            print(f"  {tag:<8}{a.species:<9}{a.breed:<14}{a.age_months:<8}"
                  f"{a.weight_kg:<7}{a.health_status}")

    def animals_needing_attention(self):
        """Return a list of animals that are unwell or have vaccines due."""
        return [a for a in self.animals.values() if a.needs_attention()]

    def summary_by_status(self):
        """Return a dictionary such as {'Healthy': 3, 'Sick': 1}."""
        counts = {}
        for animal in self.animals.values():
            counts[animal.health_status] = counts.get(animal.health_status, 0) + 1
        return counts

    @classmethod
    def supported_species(cls):
        """Return the tuple of species this system supports."""
        return SPECIES


# ---------------------------------------------------------------------------
# Helper functions: safe input (keeps the program from crashing)
# ---------------------------------------------------------------------------
def ask_text(prompt):
    return input(prompt).strip()


def ask_number(prompt, as_type=float):
    """Keep asking until the user types a valid positive number."""
    while True:
        try:
            value = as_type(input(prompt))
            if value > 0:
                return value
            print("  Please enter a number greater than zero.")
        except ValueError:
            print("  That is not a valid number. Try again.")


def ask_choice(prompt, options):
    """Show a numbered list of options and return the one chosen."""
    for number, option in enumerate(options, start=1):
        print(f"    {number}. {option}")
    while True:
        picked = input(prompt).strip()
        if picked.isdigit() and 1 <= int(picked) <= len(options):
            return options[int(picked) - 1]
        print("  Please pick a number from the list.")


# ---------------------------------------------------------------------------
# Menu actions
# ---------------------------------------------------------------------------
def register_animal(registry):
    print("\n--- Register a new animal ---")
    tag = ask_text("  Tag ID (e.g. CT-001): ")
    if not Animal.is_valid_tag(tag):
        print("  Invalid tag. Use letters, a dash and 3 digits, e.g. CT-001.")
        return
    print("  Species:")
    species = ask_choice("  Choose species number: ", registry.supported_species())
    breed = ask_text("  Breed: ") or "Local"
    age = ask_number("  Age in months: ", int)
    weight = ask_number("  Weight in kg: ", float)
    try:
        registry.add_animal(Animal(tag, species, breed, age, weight))
        print(f"  Animal {tag.upper()} registered successfully.")
    except ValueError as error:
        Animal.total_animals -= 1          # undo count for the rejected object
        print(f"  Could not register: {error}")


def view_animals(registry):
    print("\n--- All registered animals ---")
    registry.display_all()


def search_animal(registry):
    print("\n--- Search for an animal ---")
    animal = registry.find_animal(ask_text("  Enter tag ID: "))
    if animal is None:
        print("  No animal found with that tag.")
    else:
        animal.display_info()


def add_health_event(registry):
    print("\n--- Add a health record ---")
    animal = registry.find_animal(ask_text("  Enter tag ID: "))
    if animal is None:
        print("  No animal found with that tag.")
        return
    condition = ask_text("  Condition/symptom: ")
    treatment = ask_text("  Treatment given: ")
    print("  New health status:")
    status = ask_choice("  Choose status number: ", HEALTH_STATUSES)
    animal.add_health_record(condition, treatment, status)
    print(f"  Record saved. {animal.tag_id} is now '{animal.health_status}'.")


def update_animal_weight(registry):
    print("\n--- Update weight ---")
    animal = registry.find_animal(ask_text("  Enter tag ID: "))
    if animal is None:
        print("  No animal found with that tag.")
        return
    animal.update_weight(ask_number("  New weight in kg: ", float))
    print(f"  Weight of {animal.tag_id} is now {animal.weight_kg} kg.")


def record_vaccine(registry):
    print("\n--- Record a vaccination ---")
    animal = registry.find_animal(ask_text("  Enter tag ID: "))
    if animal is None:
        print("  No animal found with that tag.")
        return
    options = [v for s, v, _ in VACCINE_SCHEDULE if s == animal.species]
    print(f"  Vaccines for {animal.species}:")
    vaccine = ask_choice("  Choose vaccine number: ", options)
    animal.record_vaccination(vaccine)
    print(f"  {vaccine} recorded for {animal.tag_id} (today).")


def show_alerts(registry):
    print("\n--- Animals needing attention ---")
    flagged = registry.animals_needing_attention()
    if not flagged:
        print("  Great news - every animal is healthy and up to date.")
        return
    for animal in flagged:
        print(f"  {animal.tag_id} ({animal.species}) - status: {animal.health_status}")
        for vaccine, reason in animal.vaccinations_due():
            print(f"      vaccine due: {vaccine} ({reason})")


def show_summary(registry):
    print("\n--- Herd summary ---")
    print(f"  Farm code            : {registry.farm_code}")
    print(f"  Animals in register  : {len(registry.animals)}")
    print(f"  Animals ever created : {Animal.get_total_animals()}")
    for status, count in registry.summary_by_status().items():
        print(f"    {status:<18}: {count}")


MENU = (
    ("Register a new animal", register_animal),
    ("View all animals", view_animals),
    ("Search for an animal", search_animal),
    ("Add a health record", add_health_event),
    ("Update an animal's weight", update_animal_weight),
    ("Record a vaccination", record_vaccine),
    ("Show animals needing attention", show_alerts),
    ("Show herd summary", show_summary),
)


def load_sample_data(registry):
    """Fill the registry with example animals (no personal data)."""
    for line in ("CT-001,Cattle,Zebu,36,250",
                 "CT-002,Cattle,N'Dama,48,270",
                 "GT-001,Goat,West African,18,32",
                 "SH-001,Sheep,Djallonke,24,30"):
        registry.add_animal(Animal.from_csv_line(line))
    today = date.today()
    registry.animals["CT-001"].record_vaccination("Anthrax", today)
    registry.animals["CT-001"].record_vaccination("Foot-and-Mouth Disease", today)
    registry.animals["CT-002"].add_health_record(
        "Fever and loss of appetite", "Antibiotics", "Sick")
    registry.animals["GT-001"].record_vaccination("PPR", date(2025, 1, 15))


def print_banner():
    print("=" * 60)
    print("   LIVESTOCK HEALTH & TRACKING SYSTEM")
    print("   Open-source tool for animal health workers and farmers")
    print("=" * 60)


def run_menu(registry):
    """Main loop: show the menu until the user chooses 0."""
    print_banner()
    while True:
        print("\nMAIN MENU")
        for number, (label, _) in enumerate(MENU, start=1):
            print(f"  {number}. {label}")
        print("  0. Exit")
        choice = input("Choose an option: ").strip()
        if choice == "0":
            print("Goodbye! Keep your animals healthy.")
            break
        if choice.isdigit() and 1 <= int(choice) <= len(MENU):
            MENU[int(choice) - 1][1](registry)
        else:
            print("  Invalid option. Please choose a number from the menu.")


def run_demo():
    """Non-interactive demonstration of objects, dictionary and methods."""
    print_banner()
    registry = LivestockRegistry("FARM-01")
    load_sample_data(registry)

    print("\n[1] Registry loaded from CSV lines (class method from_csv_line):")
    registry.display_all()

    print("\n[2] Tag validation (static method is_valid_tag):")
    for tag in ("CT-003", "cow3", "GT-1"):
        print(f"  {tag:<8} -> {Animal.is_valid_tag(tag)}")

    print("\n[3] Object interaction - animal profile with health history:")
    registry.find_animal("CT-002").display_info()

    print("\n[4] Animals needing attention:")
    show_alerts(registry)

    print("\n[5] Herd summary (class attribute + dictionary count):")
    show_summary(registry)


if __name__ == "__main__":
    if "--demo" in sys.argv:
        run_demo()
    else:
        run_menu(LivestockRegistry("FARM-01"))
