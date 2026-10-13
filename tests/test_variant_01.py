"""Відкриті тести задачі 1: Хронологія подій.

Запуск: pytest tests/test_variant_01.py
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
          [
            {"event": "Ресурс додано", "after": []},
            {"event": "Читача зареєстровано", "after": []},
            {
              "event": "Ресурс заброньовано",
              "after": ["Ресурс додано", "Читача зареєстровано"],
            },
            {"event": "Лист надіслано", "after": ["Ресурс заброньовано"]},
            {"event": "Ресурс повернено", "after": ["Ресурс заброньовано"]},
            {"event": "Ресурс вилучено", "after": ["Ресурс додано"]},
          ],
        ),
        ["Ресурс додано", "Ресурс вилучено", "Читача зареєстровано",
         "Ресурс заброньовано", "Лист надіслано", "Ресурс повернено"],
    ),
    (
        "S2",
        (
          [
            {"event": "Товар додано", "after": []},
            {"event": "Кошик сформовано", "after": ["Товар додано"]},
            {"event": "Замовлення оформлено", "after": ["Кошик сформовано"]},
            {"event": "Оплату отримано", "after": ["Замовлення оформлено"]},
            {"event": "Товар зарезервовано", "after": ["Замовлення оформлено"]},
            {
              "event": "Посилку відправлено",
              "after": ["Оплату отримано", "Товар зарезервовано"],
            },
            {"event": "Замовлення скасовано", "after": ["Замовлення оформлено"]},
          ],
        ),
        ["Товар додано", "Кошик сформовано", "Замовлення оформлено",
         "Замовлення скасовано", "Оплату отримано", "Товар зарезервовано",
         "Посилку відправлено"],
    ),
    (
        "S3",
        (
          [
            {"event": "Заняття заплановано", "after": []},
            {"event": "Відвідування відмічено", "after": ["Заняття заплановано"]},
            {"event": "Оцінку виставлено", "after": ["Заняття заплановано"]},
            {
              "event": "Відомість закрито",
              "after": ["Оцінку виставлено", "Відвідування відмічено"],
            },
          ],
        ),
        ["Заняття заплановано", "Відвідування відмічено", "Оцінку виставлено",
         "Відомість закрито"],
    ),
    (
        "S3",
        (
          [
            {"event": "Заняття заплановано", "after": []},
            {"event": "Оцінку виставлено", "after": ["Заняття заплановано"]},
            {
              "event": "Оцінку виправлено",
              "after": ["Оцінку виставлено", "Підтвердження отримано"],
            },
            {"event": "Підтвердження отримано", "after": ["Оцінку виправлено"]},
          ],
        ),
        ValueError("Цикл між подіями: Оцінку виправлено, Підтвердження отримано"),
    ),
]


@pytest.mark.parametrize("tag,args,expected", CASES, ids=[f"T01-{c[0]}-{i}" for i, c in enumerate(CASES)])
def test_task_01(tag, args, expected):
    check(1, "order_events", args, expected)
