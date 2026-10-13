"""Відкриті тести задачі 6: Карта контекстів і звірка з імпортами.

Запуск: pytest tests/test_variant_06.py
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
          ["Каталог", "Видача", "Читачі", "Сповіщення", "Звітність"],
          [
            {"upstream": "Каталог", "downstream": "Видача", "pattern": "acl"},
            {"upstream": "Читачі", "downstream": "Видача", "pattern": "acl"},
            {"upstream": "Видача", "downstream": "Сповіщення", "pattern": "ohs_pl"},
            {"upstream": "Читачі", "downstream": "Сповіщення", "pattern": "conformist"},
            {"upstream": "Каталог", "downstream": "Звітність",
             "pattern": "customer_supplier"},
            {"upstream": "Видача", "downstream": "Звітність", "pattern": "separate_ways"},
          ],
          [["Видача", "Каталог"], ["Видача", "Читачі"], ["Сповіщення", "Видача"],
           ["Сповіщення", "Читачі"], ["Звітність", "Видача"], ["Видача", "Сповіщення"]],
        ),
        [
          ("separate_ways_violated", "Видача", "Звітність"),
          ("stale_relation", "Звітність", "Каталог"),
          ("wrong_direction", "Видача", "Сповіщення"),
        ],
    ),
    (
        "S2",
        (
          ["Каталог", "Замовлення", "Оплата", "Склад", "Доставка"],
          [
            {"upstream": "Каталог", "downstream": "Замовлення", "pattern": "ohs_pl"},
            {"upstream": "Замовлення", "downstream": "Оплата",
             "pattern": "customer_supplier"},
            {"upstream": "Замовлення", "downstream": "Склад", "pattern": "partnership"},
            {"upstream": "Замовлення", "downstream": "Доставка",
             "pattern": "shared_kernel"},
            {"upstream": "Оплата", "downstream": "Доставка", "pattern": "conformist"},
            {"upstream": "Склад", "downstream": "Каталог", "pattern": "foo_bar"},
            {"upstream": "Склад", "downstream": "Склад", "pattern": "acl"},
            {"upstream": "Доставка", "downstream": "Бонуси", "pattern": "acl"},
            {"upstream": "Замовлення", "downstream": "Каталог", "pattern": "acl"},
          ],
          [["Замовлення", "Каталог"], ["Оплата", "Замовлення"], ["Склад", "Замовлення"],
           ["Доставка", "Оплата"], ["Доставка", "Склад"], ["Склад", "Бонуси"]],
        ),
        [
          ("duplicate_relation", "Замовлення", "Каталог"),
          ("self_relation", "Склад", "Склад"),
          ("stale_relation", "Доставка", "Замовлення"),
          ("stale_relation", "Каталог", "Замовлення"),
          ("undeclared_dependency", "Доставка", "Склад"),
          ("unknown_context", "Бонуси", ""),
          ("unknown_pattern", "Склад", "Каталог"),
        ],
    ),
    (
        "S3",
        (
          ["Розклад", "Журнал", "Контингент", "Навчальні плани", "Повідомлення"],
          [
            {"upstream": "Контингент", "downstream": "Журнал", "pattern": "ohs_pl"},
            {"upstream": "Контингент", "downstream": "Розклад", "pattern": "ohs_pl"},
            {"upstream": "Навчальні плани", "downstream": "Розклад",
             "pattern": "customer_supplier"},
            {"upstream": "Розклад", "downstream": "Журнал", "pattern": "customer_supplier"},
            {"upstream": "Журнал", "downstream": "Повідомлення", "pattern": "acl"},
            {"upstream": "Контингент", "downstream": "Повідомлення",
             "pattern": "separate_ways"},
          ],
          [["Журнал", "Контингент"], ["Розклад", "Контингент"],
           ["Розклад", "Навчальні плани"], ["Журнал", "Розклад"],
           ["Повідомлення", "Журнал"]],
        ),
        [],
    ),
]


@pytest.mark.parametrize("tag,args,expected", CASES, ids=[f"T06-{c[0]}-{i}" for i, c in enumerate(CASES)])
def test_task_06(tag, args, expected):
    check(6, "check_map", args, expected)
