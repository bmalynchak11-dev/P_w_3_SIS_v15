"""Відкриті тести задачі 7: Звіт про залежності контекстів.

Запуск: pytest tests/test_variant_07.py
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
            "Видача": ["Каталог", "Читачі", "Сповіщення"],
            "Сповіщення": ["Видача", "Читачі"],
            "Звітність": ["Видача", "Каталог"],
            "Каталог": [],
            "Читачі": [],
          },
        ),
        {
          "cycles": [["Видача", "Сповіщення"]],
          "fan_out":
            {"Видача": 3, "Сповіщення": 2, "Звітність": 2, "Каталог": 0, "Читачі": 0},
          "fan_in": {"Каталог": 2, "Читачі": 2, "Сповіщення": 1, "Видача": 2, "Звітність": 0},
          "roots": ["Каталог", "Читачі"],
          "order": None,
        },
    ),
    (
        "S2",
        (
          {
            "Замовлення": ["Каталог", "Склад"],
            "Оплата": ["Замовлення"],
            "Склад": ["Каталог"],
            "Доставка": ["Оплата", "Склад"],
            "Каталог": [],
          },
        ),
        {
          "cycles": [],
          "fan_out": {"Замовлення": 2, "Оплата": 1, "Склад": 1, "Доставка": 2, "Каталог": 0},
          "fan_in": {"Каталог": 2, "Склад": 2, "Замовлення": 1, "Оплата": 1, "Доставка": 0},
          "roots": ["Каталог"],
          "order": ["Каталог", "Склад", "Замовлення", "Оплата", "Доставка"],
        },
    ),
    (
        "S3",
        (
          {
            "Журнал": ["Розклад", "Контингент"],
            "Розклад": ["Контингент", "Навчальні плани"],
            "Навчальні плани": ["Журнал"],
            "Повідомлення": ["Журнал", "Контингент"],
            "Контингент": [],
          },
        ),
        {
          "cycles": [["Журнал", "Навчальні плани", "Розклад"]],
          "fan_out": {"Журнал": 2, "Розклад": 2, "Навчальні плани": 1, "Повідомлення": 2,
           "Контингент": 0},
          "fan_in": {"Розклад": 1, "Контингент": 3, "Навчальні плани": 1, "Журнал": 2,
           "Повідомлення": 0},
          "roots": ["Контингент"],
          "order": None,
        },
    ),
]


@pytest.mark.parametrize("tag,args,expected", CASES, ids=[f"T07-{c[0]}-{i}" for i, c in enumerate(CASES)])
def test_task_07(tag, args, expected):
    check(7, "dependency_report", args, expected)
