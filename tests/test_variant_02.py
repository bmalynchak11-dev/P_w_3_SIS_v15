"""Відкриті тести задачі 2: Єдина мова: омоніми й синоніми.

Запуск: pytest tests/test_variant_02.py
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
            {"term": "Ресурс", "context": "Каталог",
             "definition": "Одиниця обліку з інвентарним номером"},
            {"term": "Ресурс", "context": "Видача",
             "definition": "Те, що можна позичити на строк"},
            {"term": "Статус", "context": "Каталог",
             "definition": "Стан ресурсу: доступний чи вилучений"},
            {"term": "Статус", "context": "Читачі",
             "definition": "Стан облікового запису читача"},
            {"term": "Читач", "context": "Читачі",
             "definition": "Особа з обліковим записом"},
            {"term": "Користувач", "context": "Сповіщення",
             "definition": "Особа з обліковим записом"},
            {"term": "Бронювання", "context": "Видача",
             "definition": "Закріплення ресурсу за читачем"},
            {"term": "Резервування", "context": "Звітність",
             "definition": "Закріплення ресурсу за читачем."},
          ],
        ),
        {
          "homonyms": {"ресурс": ["Видача", "Каталог"], "статус": ["Каталог", "Читачі"]},
          "synonyms": [["бронювання", "резервування"], ["користувач", "читач"]],
        },
    ),
    (
        "S2",
        (
          [
            {"term": "Товар", "context": "Каталог",
             "definition": "Предмет продажу з артикулом"},
            {"term": "Товар", "context": "Склад",
             "definition": "Одиниця зберігання на полиці"},
            {"term": "Товар", "context": "Замовлення",
             "definition": "Рядок замовлення з кількістю"},
            {"term": "Клієнт", "context": "Замовлення",
             "definition": "Особа, що оформила замовлення"},
            {"term": "Покупець", "context": "Оплата",
             "definition": "Особа, що оформила замовлення"},
            {"term": "Одержувач", "context": "Доставка",
             "definition": "Особа, що отримує посилку"},
            {"term": "Адреса", "context": "Замовлення",
             "definition": "Місце доставки посилки"},
            {"term": "Адреса", "context": "Доставка",
             "definition": "Місце доставки посилки"},
          ],
        ),
        {
          "homonyms": {"товар": ["Замовлення", "Каталог", "Склад"]},
          "synonyms": [["клієнт", "покупець"]],
        },
    ),
    (
        "S3",
        (
          [
            {"term": "Група", "context": "Контингент",
             "definition": "Академічна група зі спеціальності"},
            {"term": "Група", "context": "Розклад",
             "definition": "Студенти, які ходять на заняття разом"},
            {"term": "Оцінка", "context": "Журнал",
             "definition": "Число від 1 до 12 за відповідь"},
            {"term": "Оцінка", "context": "Навчальні плани",
             "definition": "Число від 1 до 12 за відповідь"},
            {"term": "Пара", "context": "Розклад",
             "definition": "Заняття тривалістю 90 хвилин"},
            {"term": "Заняття", "context": "Журнал",
             "definition": "Заняття   тривалістю 90 ХВИЛИН"},
            {"term": "Студент", "context": "Контингент",
             "definition": "Особа, зарахована до коледжу"},
            {"term": "Здобувач", "context": "Навчальні плани",
             "definition": "Особа, зарахована до коледжу"},
            {"term": "Здобувач", "context": "Повідомлення", "definition": "Адресат листа"},
          ],
        ),
        {
          "homonyms": {
            "група": ["Контингент", "Розклад"],
            "здобувач": ["Навчальні плани", "Повідомлення"],
          },
          "synonyms": [["заняття", "пара"], ["здобувач", "студент"]],
        },
    ),
]


@pytest.mark.parametrize("tag,args,expected", CASES, ids=[f"T02-{c[0]}-{i}" for i, c in enumerate(CASES)])
def test_task_02(tag, args, expected):
    check(2, "glossary_conflicts", args, expected)
