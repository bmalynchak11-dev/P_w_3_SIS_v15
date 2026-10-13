"""Перевірка власного прикладу моделі: python check_design.py [design/my_case.json]

Файл містить номер вашої задачі, предметну область і вхідні дані для вашої функції з variants/variant_NN.py.
Програма запускає вашу функцію на цих даних і перевіряє, чи модель має властивості «хорошого» поділу
на обмежені контексти (див. розділ «Власний приклад» у student.md).
"""
import importlib.util
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
FUNCS = {1: "order_events", 2: "glossary_conflicts", 3: "candidate_contexts", 4: "classify_subdomains",
         5: "data_ownership", 6: "check_map", 7: "dependency_report", 8: "extraction_plan",
         9: "validate_message", 10: "breaking_changes"}


def load_variant(number):
    base = Path(os.environ.get("VARIANT_DIR", ROOT / "variants"))
    path = base / f"variant_{number:02d}.py"
    spec = importlib.util.spec_from_file_location(f"variant_{number:02d}", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _min(name, have, need, problems):
    if have < need:
        problems.append(f"{name}: {have}, потрібно щонайменше {need}")


def check_case(case, module=None):
    """Повертає список зауважень до прикладу (порожній список означає, що приклад прийнято)."""
    number = case.get("task")
    if number not in FUNCS:
        return ["Поле task має містити номер вашої задачі від 1 до 10"]
    if not case.get("domain", "").strip():
        return ["Поле domain порожнє: опишіть предметну область одним реченням"]
    module = module or load_variant(number)
    func = getattr(module, FUNCS[number])
    args = case.get("args", [])
    extra = case.get("extra", {})
    problems = []
    try:
        result = func(*args)
    except NotImplementedError:
        return [f"Функцію {FUNCS[number]} ще не реалізовано"]
    except ValueError as exc:
        return [f"Функція відхилила дані прикладу: {exc}"]
    if number == 1:
        _min("Подій", len(args[0]), 6, problems)
        if len(result) != len(args[0]):
            problems.append("Хронологія містить не всі події")
    elif number == 2:
        _min("Записів словника", len(args[0]), 8, problems)
        _min("Контекстів", len({e["context"] for e in args[0]}), 3, problems)
        if result["synonyms"]:
            problems.append(f"У словнику лишилися синоніми: {result['synonyms']}")
    elif number == 3:
        _min("Агрегатів", len(args[0]), 5, problems)
        if not 2 <= len(result) <= 5:
            problems.append(f"Груп контекстів {len(result)}, потрібно від 2 до 5 (змініть поріг або словники)")
    elif number == 4:
        values = list(result.values())
        _min("Субдоменів", len(values), 5, problems)
        if "core" not in values:
            problems.append("Немає жодного ядра")
        if "generic" not in values:
            problems.append("Немає жодного типового субдомену")
        if values.count("core") > len(values) // 2:
            problems.append("Ядром названо більше половини субдоменів")
    elif number == 5:
        _min("Контекстів", len(args[0]), 4, problems)
        if result["shared_writes"]:
            problems.append(f"Таблиці з кількома авторами запису: {sorted(result['shared_writes'])}")
        if result["foreign_reads"]:
            problems.append(f"Читання чужих таблиць: {len(result['foreign_reads'])}")
        if result["orphans"]:
            problems.append(f"Таблиці без власника: {result['orphans']}")
    elif number == 6:
        _min("Контекстів", len(args[0]), 4, problems)
        _min("Різних патернів", len({r["pattern"] for r in args[1]}), 3, problems)
        problems += [f"Зауваження карти: {item}" for item in result]
    elif number == 7:
        _min("Контекстів", len(result["fan_out"]), 5, problems)
        if result["cycles"]:
            problems.append(f"Цикли залежностей: {result['cycles']}")
    elif number == 8:
        _min("Контекстів", len(args[0]), 5, problems)
        if len(result["cut_edges"]) > 2:
            problems.append(f"Після виділення залишиться {len(result['cut_edges'])} мережевих викликів (допустимо не більше 2)")
    elif number == 9:
        fields = args[0]["fields"]
        _min("Полів контракту", len(fields), 5, problems)
        kinds = {spec["type"] for spec in fields.values()}
        for need in ("enum", "date"):
            if need not in kinds:
                problems.append(f"У контракті немає поля типу {need}")
        if result:
            problems.append(f"Коректне повідомлення відхилено: {result}")
        bad = extra.get("bad_message")
        if bad is None or not func(args[0], bad):
            problems.append("Поле extra.bad_message має містити повідомлення з помилкою, яку виявляє функція")
    elif number == 10:
        if extra.get("declared_bump") != result["bump"]:
            problems.append(f"Ви заявили підвищення версії {extra.get('declared_bump')}, а за зміною потрібне {result['bump']}")
    return problems


def main(argv):
    path = Path(argv[1]) if len(argv) > 1 else ROOT / "design" / "my_case.json"
    case = json.loads(path.read_text(encoding="utf-8"))
    problems = check_case(case)
    for item in problems:
        print("ЗАУВАЖЕННЯ:", item)
    print("Приклад прийнято" if not problems else f"Зауважень: {len(problems)}")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
