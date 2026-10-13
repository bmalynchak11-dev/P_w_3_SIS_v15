import pytest
from conftest import load

# Завантажуємо модуль і витягуємо потрібну функцію
mod = load(5)
data_ownership = getattr(mod, "data_ownership", mod)


def test_regular_case():
    """Звичайний випадок: коректна ізоляція та одне стороннє читання."""
    usage = {
        "Каталог": {
            "writes": ["products"],
            "reads": ["products"],
        },
        "Замовлення": {
            "writes": ["orders"],
            "reads": ["orders", "products"],
        },
    }
    result = data_ownership(usage)
    assert result["owners"] == {"products": "Каталог", "orders": "Замовлення"}
    assert result["shared_writes"] == {}
    assert result["foreign_reads"] == [["Замовлення", "products", "Каталог"]]
    assert result["orphans"] == []


def test_boundary_empty_and_own_reads():
    """Граничний випадок: порожні списки або читання лише власних таблиць."""
    usage = {
        "Аудит": {"writes": [], "reads": []},
        "Склад": {
            "writes": ["stocks"],
            "reads": ["stocks"],
        },
    }
    result = data_ownership(usage)
    assert result["owners"] == {"stocks": "Склад"}
    assert result["shared_writes"] == {}
    assert result["foreign_reads"] == []
    assert result["orphans"] == []


def test_violation_shared_and_orphans():
    """Випадок із порушеннями: спільний запис (shared_writes) та таблиці-сироти (orphans)."""
    usage = {
        "МодульА": {
            "writes": ["shared_table"],
            "reads": ["missing_table"],
        },
        "МодульБ": {
            "writes": ["shared_table"],
            "reads": ["shared_table"],
        },
    }
    result = data_ownership(usage)
    assert result["owners"] == {}
    assert result["shared_writes"] == {"shared_table": ["МодульА", "МодульБ"]}
    assert result["foreign_reads"] == []
    assert result["orphans"] == ["missing_table"]