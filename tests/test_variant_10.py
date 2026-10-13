"""Відкриті тести задачі 10: Сумісність версій контракту.

Запуск: pytest tests/test_variant_10.py
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
            "name": "ReservationCreated",
            "version": "1.0",
            "fields": {
              "reservation_id": {"type": "str", "required": True},
              "resource_id": {"type": "str", "required": True},
              "reader_id": {"type": "str", "required": True},
              "until": {"type": "date", "required": True},
              "channel": {"type": "enum", "required": False, "values": ["email", "sms"]},
            },
          },
          {
            "name": "ReservationCreated",
            "version": "2.0",
            "fields": {
              "reservation_id": {"type": "str", "required": True},
              "resource_id": {"type": "str", "required": True},
              "reader_id": {"type": "int", "required": True},
              "channel": {"type": "enum", "required": False, "values": ["email"]},
              "note": {"type": "str", "required": False},
              "priority": {"type": "int", "required": True},
            },
          },
        ),
        {
          "breaking": [["enum_narrowed", "channel"], ["new_required", "priority"],
           ["type_changed", "reader_id"], ["field_removed", "until"]],
          "compatible": [["field_added_optional", "note"]],
          "bump": "major",
        },
    ),
    (
        "S2",
        (
          {
            "name": "OrderPlaced",
            "version": "2.1",
            "fields": {
              "order_id": {"type": "str", "required": True},
              "total": {"type": "number", "required": True},
              "items": {"type": "list", "required": True},
              "gift": {"type": "bool", "required": True},
              "payment": {"type": "enum", "required": True, "values": ["card"]},
            },
          },
          {
            "name": "OrderPlaced",
            "version": "2.2",
            "fields": {
              "order_id": {"type": "str", "required": True},
              "total": {"type": "number", "required": True},
              "items": {"type": "list", "required": True},
              "gift": {"type": "bool", "required": False},
              "payment": {"type": "enum", "required": True, "values": ["card", "cash"]},
              "delivery":
                {"type": "enum", "required": False, "values": ["courier", "pickup"]},
            },
          },
        ),
        {
          "breaking": [],
          "compatible": [["field_added_optional", "delivery"], ["became_optional", "gift"],
           ["enum_widened", "payment"]],
          "bump": "minor",
        },
    ),
    (
        "S3",
        (
          {
            "name": "MarkSet",
            "version": "1.0",
            "fields": {
              "student_id": {"type": "str", "required": True},
              "value": {"type": "int", "required": True, "min": 1, "max": 12},
            },
          },
          {
            "name": "MarkSet",
            "version": "1.0.1",
            "fields": {
              "value": {"type": "int", "required": True, "min": 1, "max": 12},
              "student_id": {"type": "str", "required": True},
            },
          },
        ),
        {"breaking": [], "compatible": [], "bump": "patch"},
    ),
]


@pytest.mark.parametrize("tag,args,expected", CASES, ids=[f"T10-{c[0]}-{i}" for i, c in enumerate(CASES)])
def test_task_10(tag, args, expected):
    check(10, "breaking_changes", args, expected)
