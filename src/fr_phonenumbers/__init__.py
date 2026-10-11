import csv
import bisect
import importlib.resources
from typing import Optional, Dict, Tuple, List
from . import data

_OPERATORS_CACHE: Optional[Dict[str, str]] = None
_RANGES_CACHE: Optional[List[Tuple[int, int, str, str]]] = None


def _load_data() -> Tuple[Dict[str, str], List[Tuple[int, int, str, str]]]:
    """Charge et met en cache les fichiers CSV au premier appel."""
    global _OPERATORS_CACHE, _RANGES_CACHE
    if _OPERATORS_CACHE is not None and _RANGES_CACHE is not None:
        return _OPERATORS_CACHE, _RANGES_CACHE

    operators = {}
    with importlib.resources.files(data).joinpath("operators.csv").open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            operators[row["code"].strip()] = row["operateur"].strip()

    ranges = []
    with importlib.resources.files(data).joinpath("num_ranges.csv").open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            start = int(row["num_debut"])
            end = int(row["num_fin"])
            op_code = row["operateur"].strip()
            zone = row["zone"].strip()
            ranges.append((start, end, op_code, zone))

    ranges.sort(key=lambda x: x[0])

    _OPERATORS_CACHE = operators
    _RANGES_CACHE = ranges
    return _OPERATORS_CACHE, _RANGES_CACHE


def parse_phone_number(numero_str: str) -> int:
    """
    Nettoie, valide un numéro de téléphone français et retourne sa version entière (ex: 105700000).
    Lève une ValueError si le format est invalide.
    """
    if not isinstance(numero_str, str):
        raise ValueError("Le numéro doit être une chaîne de caractères.")

    cleaned = "".join(c for c in numero_str if c.isdigit() or c == "+")

    if cleaned.startswith("+33"):
        cleaned = "0" + cleaned[3:]
    elif cleaned.startswith("0033"):
        cleaned = "0" + cleaned[4:]

    if not cleaned.startswith("0") or len(cleaned) != 10:
        raise ValueError(f"Format de numéro français invalide : '{numero_str}'")

    try:
        return int(cleaned)
    except ValueError:
        raise ValueError(f"Impossible de convertir le numéro en entier : '{numero_str}'")


def get_operator(numero_str: str) -> Optional[Dict[str, str]]:
    """
    Prend un numéro français (string) et retourne un dictionnaire avec les infos de l'opérateur,
    ou None si le numéro n'est rattaché à aucune plage connue.
    """
    operators, ranges = _load_data()
    
    try:
        num_int = parse_phone_number(numero_str)
    except ValueError:
        return None

    bornes_min = [r[0] for r in ranges]
    idx = bisect.bisect_right(bornes_min, num_int) - 1

    if idx < 0:
        return None

    borne_min, borne_max, op_code, zone = ranges[idx]

    if borne_min <= num_int <= borne_max:
        operator_name = operators.get(op_code, op_code)
        return {
            "code": op_code,
            "operator": operator_name,
            "zone": zone,
        }

    return None