import datetime
from sqlalchemy import String, Text, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


# 1. СОЗДАЕМ МОДЕЛЬ ДАННЫХ ДЛЯ ЗАМЕТОК
# Наследуемся от Base. Теперь Python понимает, что класс Note — это чертеж таблицы для базы данных.
class Note(Base):
    # __tablename__ жестко задает имя физической таблицы внутри базы MySQL
    __tablename__ = "notes"

    # --- ОПИСАНИЕ КОЛОНОК ТАБЛИЦЫ ---

    # id: Уникальный номер заметки (Primary Key). 
    # autoincrement=True означает, что MySQL сама будет считать: 1, 2, 3... 
    # Нам не нужно придумывать ID вручную. Mapped[int] подсказывает, что это целое число.
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)


    # title: Заголовок заметки.
    # String(150) ограничивает длину заголовка до 150 символов.
    # nullable=False — это жесткое правило: база выдаст ошибку и не сохранит заметку, если заголовок пустой.
    title: Mapped[str] = mapped_column(String(150), nullable=False)


    # content: Основной текст заметки.
    # Тип Text, в отличие от String, позволяет хранить очень длинные тексты без жестких лимитов.
    # nullable=False — это жесткое правило: база выдаст ошибку и не сохранит заметку, если текст пустой.
    content: Mapped[str] = mapped_column(Text, nullable=False)

    
    # created_at: Дата и время создания записи.
    # server_default=func.now() — это хитрость: мы перекладываем работу на саму базу данных.
    # В момент сохранения MySQL сама подставит свое текущее время в эту колонку.
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())



# --- ТЕСТОВЫЙ БЛОК ---
# Код ниже сработает ТОЛЬКО в том случае, если ты запустишь этот файл напрямую через терминал.
if __name__ == "__main__":
    # Импортируем нашу физическую "трубу" к базе данных (engine)
    from app.database import engine

    try:
        # Base.metadata хранит чертежи всех классов, унаследованных от Base (пока там только Note).
        # Метод create_all берет эти чертежи, подключается к MySQL через engine и физически создает таблицы,
        # если их там еще нет. Существующие таблицы он не трогает и не удаляет.
        Base.metadata.create_all(bind=engine)
        print("Таблица 'notes' успешно создана")
    except Exception as e:
        print(f"Ошибка при создании таблицы: {e}")
