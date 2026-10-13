"""Відкриті тести задачі 4: Тип субдомену.

Запуск: pytest tests/test_variant_04.py
Тут лише приклади з карток варіантів; повний набір перевірок є у викладача.
"""
import copy

import pytest
from conftest import load


def norm(value):
    """Кортежі й списки порівнюються однаково."""
    if isinstance(value, (list, tuple)):
        return [norm(v) for v in value]
    if isinstance(value, dict):
        return {k: norm(v) for k, v in value.items()}
    return value


def pids(n, rows):
    return [f"T{n:02d}-{r[0]}-p{i}" for i, r in enumerate(rows)]


def check(number, func, args, expected):
    call = getattr(load(number), func)
    before = copy.deepcopy(args)
    if isinstance(expected, ValueError):
        with pytest.raises(ValueError) as info:
            call(*args)
        assert str(info.value) == str(expected)
    else:
        assert norm(call(*args)) == norm(expected)
    assert args == before, "функція не повинна змінювати вхідні дані"


CASES = [
    (
        "S1",
        (
          {
            "Бронювання за правилами": {"diff": 5, "complexity": 4, "ready_solution": False},
            "Облік ресурсів": {"diff": 3, "complexity": 3, "ready_solution": False},
            "Облікові записи читачів": {"diff": 1, "complexity": 2, "ready_solution": True},
            "Сповіщення": {"diff": 2, "complexity": 1, "ready_solution": True},
            "Звітність": {"diff": 2, "complexity": 3, "ready_solution": False},
          },
        ),
        {"Бронювання за правилами": "core", "Облік ресурсів": "supporting",
         "Облікові записи читачів": "generic", "Сповіщення": "generic",
         "Звітність": "supporting"},
    ),
    (
        "S2",
        (
          {
            "Рекомендації": {"diff": 5, "complexity": 5, "ready_solution": False},
            "Ціноутворення": {"diff": 4, "complexity": 3, "ready_solution": False},
            "Каталог": {"diff": 3, "complexity": 2, "ready_solution": False},
            "Оплата": {"diff": 1, "complexity": 4, "ready_solution": True},
            "Склад": {"diff": 2, "complexity": 3, "ready_solution": False},
            "Доставка": {"diff": 4, "complexity": 2, "ready_solution": True},
          },
        ),
        {"Рекомендації": "core", "Ціноутворення": "core", "Каталог": "supporting",
         "Оплата": "generic", "Склад": "supporting", "Доставка": "supporting"},
    ),
    (
        "S3",
        (
          {
            "Розклад": {"diff": 3, "complexity": 5, "ready_solution": False},
            "Журнал": {"diff": 2, "complexity": 3, "ready_solution": False},
            "Вхід користувачів": {"diff": 1, "complexity": 3, "ready_solution": True},
            "Поштові листи": {"diff": 1, "complexity": 1, "ready_solution": True},
            "Аналітика успішності": {"diff": 5, "complexity": 3, "ready_solution": False},
            "Облік контингенту": {"diff": 2, "complexity": 2, "ready_solution": True},
          },
        ),
        {"Розклад": "supporting", "Журнал": "supporting", "Вхід користувачів": "generic",
         "Поштові листи": "generic", "Аналітика успішності": "core",
         "Облік контингенту": "generic"},
    ),
    (
        "S3",
        (
          {
            "Розклад": {"diff": 3, "complexity": 5, "ready_solution": False},
            "Журнал": {"diff": 6, "complexity": 3, "ready_solution": False},
          },
        ),
        ValueError("Оцінка поза межами 1-5: Журнал.diff"),
    ),
]


@pytest.mark.parametrize("tag,args,expected", CASES, ids=[f"T04-{c[0]}-{i}" for i, c in enumerate(CASES)])
def test_task_04(tag, args, expected):
    check(4, "classify_subdomains", args, expected)
