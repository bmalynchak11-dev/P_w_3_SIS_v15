"""Відкриті тести задачі 5: Власність на дані.

Запуск: pytest tests/test_variant_05.py
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
            "Каталог": {"writes": ["catalog_resources"], "reads": []},
            "Видача": {
              "writes": ["lending_reservations"],
              "reads": ["catalog_resources", "members_accounts"],
            },
            "Читачі": {"writes": ["members_accounts"], "reads": []},
            "Сповіщення": {
              "writes": ["notifications_outbox"],
              "reads": ["lending_reservations", "members_accounts"],
            },
            "Звітність": {
              "writes": ["report_cache", "lending_reservations"],
              "reads": ["catalog_resources", "notifications_outbox", "audit_log"],
            },
          },
        ),
        {
          "owners": {"catalog_resources": "Каталог", "members_accounts": "Читачі",
           "notifications_outbox": "Сповіщення", "report_cache": "Звітність"},
          "shared_writes": {"lending_reservations": ["Видача", "Звітність"]},
          "foreign_reads": [
            ["Видача", "catalog_resources", "Каталог"],
            ["Видача", "members_accounts", "Читачі"],
            ["Звітність", "catalog_resources", "Каталог"],
            ["Звітність", "notifications_outbox", "Сповіщення"],
            ["Сповіщення", "members_accounts", "Читачі"],
          ],
          "orphans": ["audit_log"],
        },
    ),
    (
        "S2",
        (
          {
            "Каталог": {"writes": ["catalog_products"], "reads": []},
            "Замовлення": {
              "writes": ["orders_orders", "orders_lines"],
              "reads": ["catalog_products", "stock_levels"],
            },
            "Оплата": {"writes": ["payments_payments"], "reads": ["orders_orders"]},
            "Склад":
              {"writes": ["stock_levels"], "reads": ["catalog_products", "orders_lines"]},
            "Доставка": {
              "writes": ["shipping_parcels"],
              "reads": ["orders_orders", "payments_payments", "orders_lines"],
            },
          },
        ),
        {
          "owners": {"catalog_products": "Каталог", "orders_orders": "Замовлення",
           "orders_lines": "Замовлення", "payments_payments": "Оплата",
           "stock_levels": "Склад", "shipping_parcels": "Доставка"},
          "shared_writes": {},
          "foreign_reads": [["Доставка", "orders_lines", "Замовлення"],
           ["Доставка", "orders_orders", "Замовлення"],
           ["Доставка", "payments_payments", "Оплата"],
           ["Замовлення", "catalog_products", "Каталог"],
           ["Замовлення", "stock_levels", "Склад"],
           ["Оплата", "orders_orders", "Замовлення"],
           ["Склад", "catalog_products", "Каталог"],
           ["Склад", "orders_lines", "Замовлення"]],
          "orphans": [],
        },
    ),
    (
        "S3",
        (
          {
            "Розклад": {
              "writes": ["schedule_lessons"],
              "reads": ["curriculum_plans", "contingent_groups"],
            },
            "Журнал": {
              "writes": ["journal_marks", "journal_attendance"],
              "reads": ["schedule_lessons", "journal_marks", "contingent_students"],
            },
            "Контингент":
              {"writes": ["contingent_students", "contingent_groups"], "reads": []},
            "Навчальні плани": {
              "writes": ["curriculum_plans", "journal_marks"],
              "reads": ["contingent_groups"],
            },
            "Повідомлення": {
              "writes": ["messages_outbox"],
              "reads": ["journal_marks", "contingent_students", "messages_templates"],
            },
          },
        ),
        {
          "owners": {"schedule_lessons": "Розклад", "journal_attendance": "Журнал",
           "contingent_students": "Контингент", "contingent_groups": "Контингент",
           "curriculum_plans": "Навчальні плани", "messages_outbox": "Повідомлення"},
          "shared_writes": {"journal_marks": ["Журнал", "Навчальні плани"]},
          "foreign_reads": [
            ["Журнал", "contingent_students", "Контингент"],
            ["Журнал", "schedule_lessons", "Розклад"],
            ["Навчальні плани", "contingent_groups", "Контингент"],
            ["Повідомлення", "contingent_students", "Контингент"],
            ["Розклад", "contingent_groups", "Контингент"],
            ["Розклад", "curriculum_plans", "Навчальні плани"],
          ],
          "orphans": ["messages_templates"],
        },
    ),
]


@pytest.mark.parametrize("tag,args,expected", CASES, ids=[f"T05-{c[0]}-{i}" for i, c in enumerate(CASES)])
def test_task_05(tag, args, expected):
    check(5, "data_ownership", args, expected)
