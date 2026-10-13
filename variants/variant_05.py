"""
Задача 5. Власність на дані
Перевірка правила «кожна таблиця має одного власника».
"""

def data_ownership(usage: dict) -> dict:
    """
    Аналізує доступ контекстів до таблиць:
    - owners: таблиці з єдиним автором запису {таблиця: власник}
    - shared_writes: таблиці з кількома авторами {таблиця: sorted([автори])}
    - foreign_reads: сортований список [читач, таблиця, власник] (для таблиць з єдиним власником != читач)
    - orphans: таблиці, які хтось читає, але ніхто не пише (відсортовані)
    """
    # 1. Збір авторів (writers) та читачів (readers) для кожної таблиці
    table_writers = {}
    table_readers = {}

    for context, perms in usage.items():
        writes = perms.get("writes", [])
        reads = perms.get("reads", [])

        # Використовуємо set для уникнення дублікатів у межах одного контексту
        for table in set(writes):
            table_writers.setdefault(table, set()).add(context)

        for table in set(reads):
            table_readers.setdefault(table, set()).add(context)

    owners = {}
    shared_writes = {}

    # 2. Визначення власників та спільних записів
    for table, writers in table_writers.items():
        if len(writers) == 1:
            owners[table] = next(iter(writers))
        elif len(writers) > 1:
            shared_writes[table] = sorted(list(writers))

    foreign_reads = []
    orphans = set()

    # 3. Класифікація читань
    for reader_context, perms in usage.items():
        reads = set(perms.get("reads", []))
        for table in reads:
            # Читання таблиць без авторів (orphans)
            if table not in table_writers:
                orphans.add(table)
            # Читання таблиць, що мають єдиного власника, відмінного від читача
            elif table in owners:
                owner = owners[table]
                if owner != reader_context:
                    foreign_reads.append([reader_context, table, owner])

    # Сортування результатів відповідно до правил
    foreign_reads.sort()
    sorted_orphans = sorted(list(orphans))

    return {
        "owners": owners,
        "shared_writes": shared_writes,
        "foreign_reads": foreign_reads,
        "orphans": sorted_orphans,
    }