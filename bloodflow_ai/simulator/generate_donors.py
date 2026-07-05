"""
Synthetic Donor Generator

Generates realistic synthetic donors with guaranteed coverage.
"""

import csv
import random
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from collections import defaultdict, Counter

# ============================================================
# CONFIGURATION
# ============================================================

BLOOD_GROUP_DISTRIBUTION = [
    ("O+", 34),
    ("A+", 30),
    ("B+", 20),
    ("O-", 5),
    ("A-", 3),
    ("B-", 3),
    ("AB+", 3),
    ("AB-", 2),
]

LOCATION_DISTRIBUTION = [
    ("Dhaka", 40),
    ("Chittagong", 25),
    ("Rajshahi", 20),
    ("Khulna", 15),
]

PREFERRED_TIMES = ["Morning", "Afternoon", "Evening", "Any"]

FIRST_NAMES = [
    "Rahim", "Karim", "Rokeya", "Shahid", "Nasrin", "Kabir", "Laila",
    "Faisal", "Fatema", "Jahangir", "Shamim", "Taslima", "Rafiq", "Sajeda",
    "Hasan", "Amina", "Kamal", "Shirin", "Mizan", "Sabina", "Anwar", "Nadia",
    "Farid", "Jahanara", "Monir", "Razia", "Nasir", "Rupa", "Shafiq", "Sonia",
    "Mokhles", "Jannat", "Siraj", "Tania", "Shahjahan", "Nupur", "Alamgir",
    "Moushumi", "Morshed", "Papia", "Mohammad", "Hasina", "Zahid", "Rina",
    "Salam", "Shila", "Yusuf", "Lina", "Arif", "Parvin"
]

LAST_NAMES = [
    "Ahmed", "Ali", "Khan", "Hassan", "Rahman", "Islam", "Begum", "Haque",
    "Sarker", "Chowdhury", "Malik", "Hossain", "Hasan", "Bhuiyan", "Siddique",
    "Ahsan", "Karim", "Khatun", "Zaman", "Miah", "Uddin", "Kader", "Jahan"
]

# ============================================================
# HELPERS
# ============================================================

def _get_blood_group() -> str:
    """Generate blood group from distribution."""
    rand = random.randint(1, 100)
    cumulative = 0
    for bg, pct in BLOOD_GROUP_DISTRIBUTION:
        cumulative += pct
        if rand <= cumulative:
            return bg
    return "O+"


def _get_location() -> str:
    """Generate location from distribution."""
    rand = random.randint(1, 100)
    cumulative = 0
    for loc, pct in LOCATION_DISTRIBUTION:
        cumulative += pct
        if rand <= cumulative:
            return loc
    return "Dhaka"


def _generate_age() -> int:
    """Generate age between 18-65, centered around 30."""
    age = int(random.triangular(18, 65, 30))
    return max(18, min(65, age))


def _generate_name() -> str:
    """Generate random Bangladeshi name."""
    return f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"


def _generate_phone() -> str:
    """Generate valid 11-digit phone number."""
    prefix = random.choice(["017", "018", "019", "013", "014", "015", "016"])
    suffix = ''.join(str(random.randint(0, 9)) for _ in range(8))
    return prefix + suffix


def _generate_response_rate(age: int) -> float:
    """Generate response rate based on age."""
    base = random.uniform(0.3, 0.9)
    if age < 25:
        base += 0.1
    elif age > 50:
        base -= 0.15
    return round(max(0.1, min(0.95, base)), 2)


def _generate_status() -> str:
    """Generate donor status."""
    return "Active" if random.random() < 0.90 else "Inactive"


def _generate_available(status: str) -> bool:
    """Generate availability based on status."""
    if status != "Active":
        return False
    return random.random() < 0.85


def _generate_last_donation() -> Optional[str]:
    """Generate last donation date (1-2 years ago, or None)."""
    if random.random() < 0.30:
        return None
    days_ago = random.randint(365, 730)
    return (datetime.now() - timedelta(days=days_ago)).strftime("%Y-%m-%d")


def _generate_donor(donor_id: int) -> Dict[str, Any]:
    """Generate a single synthetic donor."""
    age = _generate_age()
    status = _generate_status()
    
    return {
        "id": donor_id,
        "name": _generate_name(),
        "blood_group": _get_blood_group(),
        "age": age,
        "location": _get_location(),
        "phone": _generate_phone(),
        "last_donation": _generate_last_donation(),
        "available": _generate_available(status),
        "response_rate": _generate_response_rate(age),
        "preferred_time": random.choice(PREFERRED_TIMES),
        "status": status
    }


# ============================================================
# MAIN FUNCTIONS
# ============================================================

def generate_donors(count: int = 100, start_id: int = 21) -> List[Dict[str, Any]]:
    """Generate multiple synthetic donors."""
    return [_generate_donor(start_id + i) for i in range(count)]


def ensure_available_donors(donors: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Ensure each blood group has at least 3 available donors.
    Special guarantee for O- (critical for demos).
    """
    groups = defaultdict(list)
    for donor in donors:
        groups[donor['blood_group']].append(donor)
    
    for bg, group in groups.items():
        avail = [d for d in group if d['available']]
        if len(avail) < 3:
            print(f"[Simulator] ⚠️ {bg} only has {len(avail)} available donors")
            for donor in group:
                if not donor['available'] and len(avail) < 3:
                    donor['available'] = True
                    avail.append(donor)
                    print(f"[Simulator]   → Made {donor['name']} available")
    
    # Special guarantee for O- (needs at least 2 available)
    o_minus = [d for d in donors if d['blood_group'] == 'O-']
    o_avail = [d for d in o_minus if d['available']]
    if len(o_avail) < 2:
        print(f"[Simulator] ⚠️ O- only has {len(o_avail)} available donors")
        for donor in o_minus:
            if not donor['available'] and len(o_avail) < 2:
                donor['available'] = True
                o_avail.append(donor)
                print(f"[Simulator]   → Guaranteed O-: {donor['name']}")
    
    return donors


def save_to_csv(
    donors: List[Dict[str, Any]],
    file_path: Path,
    backup: bool = True
) -> None:
    """
    Save donors to CSV (OVERWRITE MODE).
    
    ⚠️ This does NOT append — it completely replaces the file.
    This ensures we never accumulate corrupted data.
    """
    # Create backup if requested and file exists
    if backup and file_path.exists():
        backup_path = file_path.with_suffix(".csv.bak")
        if backup_path.exists():
            backup_path.unlink()
        file_path.rename(backup_path)
        print(f"[Simulator] Created backup: {backup_path}")
    
    # Fieldnames in correct order
    fieldnames = [
        'id', 'name', 'blood_group', 'age', 'location', 'phone',
        'last_donation', 'available', 'response_rate', 'preferred_time', 'status'
    ]
    
    # Write fresh CSV (overwrite)
    with open(file_path, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(donors)
    
    print(f"[Simulator] ✅ Saved {len(donors)} donors to {file_path}")


# ============================================================
# SCRIPT ENTRY POINT
# ============================================================

def main():
    """Main entry point."""
    print("=" * 60)
    print("BLOODFLOW AI — SYNTHETIC DONOR GENERATOR")
    print("=" * 60)
    
    csv_path = Path(__file__).parent.parent / "data" / "donors.csv"
    print(f"[Simulator] CSV path: {csv_path}")
    
    print("[Simulator] Generating 100 synthetic donors...")
    donors = generate_donors(count=100, start_id=21)
    donors = ensure_available_donors(donors)
    
    # Show distribution
    counts = Counter(d['blood_group'] for d in donors)
    print("\n[Simulator] Distribution:")
    for bg, count in sorted(counts.items()):
        avail = sum(1 for d in donors if d['blood_group'] == bg and d['available'])
        print(f"  - {bg}: {count} donors, {avail} available")
    
    print("\n[Simulator] Saving to CSV...")
    save_to_csv(donors, csv_path)
    
    print("\n✅ Donor generation complete!")


if __name__ == "__main__":
    main()