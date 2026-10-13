# Стартовий проєкт SIS-P03

1. Відкрийте проєкт у GitHub Codespaces (Code → Codespaces → Create codespace) або локально: `python3 -m venv .venv`, `source .venv/bin/activate` (у Windows: `.venv\Scripts\activate`), `pip install -r requirements.txt`.
2. Визначте свою задачу за номером варіанта: задача = `(номер - 1) // 3 + 1`, набір = `(номер - 1) % 3 + 1`. Реалізуйте задачу у файлі `variants/variant_NN.py` за карткою.
3. Запускайте відкриті тести своєї задачі: `pytest tests/test_variant_NN.py` (NN з двома цифрами). Права адміністратора не потрібні.
4. Свій приклад моделі предметної області опишіть у `design/my_case.json` і перевірте командою `python check_design.py`.
5. Змінюйте лише свій файл у `variants/`, файл `tests/test_my.py`, файл `design/my_case.json` і файл `ANSWERS.md` (створіть його в корені проєкту).
