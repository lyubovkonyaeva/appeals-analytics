import random
from datetime import datetime, timedelta

from app.database import get_connection, init_db


CATEGORIES = {
    "Оплата": {
        "keywords": "оплата, карта, списание, платеж, возврат",
        "tickets": [
            ("Деньги списались дважды", "При оплате подписки с карты списали деньги два раза!"),
            ("Не проходит платеж", "Карта отклоняется при оплате, на на счете средства присутствуют"),
            ("Нужен возврат", "Мне нужно сделать возврат, услугой я не пользовался"),
        ],
    },

    "Доступ к аккаунту" : {
        "keywords" : "паролт, вход, аккаунт, логин, восстановление",
        "tickets": [
            ("Не могу войти", "Пишет неверный пароль, хотя я его точно не менял"),
            ("Не приходит письмо", "Письмо для восстановления пароля так и не пришло на почту"),
            ("Аккаунт заблокирован", "Не могу войти в аккаунт. Пишет, что он заблокирован"),
        ],
    },

    "Ошибка в работе": {
        "keywords": "ошибка, сбой, не работает, зависает, баг",
        "tickets": [
            ("Приложение зависает", "После обновления приложение зависает при открытии"),
            ("Страница не загружается", "Вместо страницы показывается ошибка 500"),
            ("Не сохраняются данные", "Изменения в профиле не сохраняются, это баг?"),
        ],
    },
    "Вопрос по функциям": {
        "keywords": "как, где, настроить, функция, возможность",
        "tickets": [
            ("Как включить уведомления", "Подскажите, где в настройках включить уведомления"),
            ("Есть ли экспорт данных", "Можно ли выгрузить свои данные в файл?"),
        ],
    },
    "Пожелание": {
        "keywords": "предложение, хотелось бы, добавьте, пожелание",
        "tickets": [
            ("Добавьте темную тему", "Хотелось бы темную тему оформления"),
            ("Предложение по поиску", "Добавьте фильтр по дате в поиск"),
        ],
    },
}

AUTHORS = [f"user{n}@example.com" for n in range(1,81)]
STATUSES = ["новое", "в работе", "закрыто"]
WEIGHTS = [30, 25, 25, 12, 8]

def seed(count=300):
    init_db()
    conn = get_connection()

    for name, data in CATEGORIES.items():
        conn.execute(
            "INSERT OR IGNORE INTO categories (name, keywords) VALUES (?, ?)",
            (name, data["keywords"]),
        )

    rows = conn.execute("SELECT id, name FROM categories").fetchall()
    category_ids = {row["name"]: row["id"] for row in rows}

    conn.execute("DELETE FROM tickets")

    now = datetime.now()
    tickets = []

    for _ in range(count):
        name = random.choices(list(CATEGORIES), weights=WEIGHTS)[0]
        title, text = random.choice(CATEGORIES[name]["tickets"])
        created = now - timedelta(days=random.randint(0, 59),
                                  minutes=random.randint(0, 1439))
        tickets.append((
            title,
            text,
            random.choice(AUTHORS),
            random.choice(STATUSES),
            category_ids[name],
            created.isoformat(sep=" ", timespec="seconds"),
        ))

    conn.executemany(
        "INSERT INTO tickets (title, text, author, status, category_id, created_at) "
        "VALUES (?, ?, ?, ?, ?, ?)",
        tickets,
    )

    conn.commit()
    conn.close()

    print(f"Добавлено обращений: {count}")


if __name__ == "__main__":
    seed()