"""Відкриті тести задачі 9: Перевірка повідомлення за контрактом.

Запуск: pytest tests/test_variant_09.py
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
              "priority": {"type": "int", "required": False},
            },
          },
          {"reservation_id": "B-17", "resource_id": "R3", "reader_id": "S5",
           "until": "2040-09-15", "channel": "sms"},
        ),
        [],
    ),
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
              "priority": {"type": "int", "required": False},
            },
          },
          {"reservation_id": 17, "resource_id": "R3", "until": "2040-02-30",
           "channel": "push", "extra": 1},
        ),
        [["bad_value", "channel"], ["unknown_field", "extra"], ["missing", "reader_id"],
         ["wrong_type", "reservation_id"], ["bad_value", "until"]],
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
              "paid": {"type": "bool", "required": True},
              "coupon": {"type": "str", "required": False},
            },
          },
          {"order_id": "A1", "total": 199.5, "items": [], "paid": False},
        ),
        [],
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
              "paid": {"type": "bool", "required": True},
              "coupon": {"type": "str", "required": False},
            },
          },
          {"order_id": "A1", "total": True, "items": "x", "paid": False, "coupon": None},
        ),
        [["wrong_type", "coupon"], ["wrong_type", "items"], ["wrong_type", "total"]],
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
              "paid": {"type": "bool", "required": True},
              "coupon": {"type": "str", "required": False},
            },
          },
          {"order_id": "A1", "total": 199, "items": [], "paid": 1},
        ),
        [["wrong_type", "paid"]],
    ),
    (
        "S3",
        (
          {
            "name": "MarkSet",
            "version": "1.0",
            "fields": {
              "student_id": {"type": "str", "required": True},
              "subject": {"type": "str", "required": True},
              "value": {"type": "int", "required": True, "min": 1, "max": 12},
              "lesson_date": {"type": "date", "required": True},
              "kind": {"type": "enum", "required": True, "values": ["current", "final"]},
            },
          },
          {"student_id": "S1", "subject": "Фізика", "value": 12,
           "lesson_date": "2040-10-01", "kind": "current"},
        ),
        [],
    ),
    (
        "S3",
        (
          {
            "name": "MarkSet",
            "version": "1.0",
            "fields": {
              "student_id": {"type": "str", "required": True},
              "subject": {"type": "str", "required": True},
              "value": {"type": "int", "required": True, "min": 1, "max": 12},
              "lesson_date": {"type": "date", "required": True},
              "kind": {"type": "enum", "required": True, "values": ["current", "final"]},
            },
          },
          {"student_id": "S1", "subject": "Фізика", "value": 13,
           "lesson_date": "2040-10-01", "kind": "current"},
        ),
        [["bad_value", "value"]],
    ),
    (
        "S3",
        (
          {
            "name": "MarkSet",
            "version": "1.0",
            "fields": {
              "student_id": {"type": "str", "required": True},
              "subject": {"type": "str", "required": True},
              "value": {"type": "int", "required": True, "min": 1, "max": 12},
              "lesson_date": {"type": "date", "required": True},
              "kind": {"type": "enum", "required": True, "values": ["current", "final"]},
            },
          },
          [],
        ),
        ValueError("Повідомлення має бути словником"),
    ),
]


@pytest.mark.parametrize("tag,args,expected", CASES, ids=[f"T09-{c[0]}-{i}" for i, c in enumerate(CASES)])
def test_task_09(tag, args, expected):
    check(9, "validate_message", args, expected)
