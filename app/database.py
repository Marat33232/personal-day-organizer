import os
from dotenv import load_dotenv 
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase


# 1. Загрузка секретных данных
# Функция load_dotenv() читает твой файл .env и делает его переменные доступными для Python.
# Это нужно, чтобы не писать логины и пароли прямо в коде — так безопаснее.
load_dotenv()


# 2. Чтение настроек базы данных
# os.getenv("ИМЯ_ПЕРЕМЕННОЙ", "значение_по_умолчанию") ищет переменную в .env.
# Убедись, что ключи (DB_USER, DB_PASSWORD и т.д.) написаны точно так же, как в твоем .env.
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")




# 3. Формирование строки подключения (URL)
# Это специальная строка, которая говорит SQLAlchemy, куда и как подключаться.
# mysql+pymysql означает: "Подключись к MySQL, используя драйвер pymysql"[cite: 219].
SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# 4. Создание Движка (engine)
# engine — это наша физическая "труба" к базе данных[cite: 248].
# Он берет на себя самую тяжелую работу: устанавливает сетевое соединение с Docker-контейнером и держит его открытым[cite: 250].
engine = create_engine(SQLALCHEMY_DATABASE_URL)


# 5. Создание Фабрики сессий (SessionLocal)
# sessionmaker — это генератор временных "блокнотов" (сессий) для безопасной работы с данными[cite: 251].
# Когда нам нужно будет сохранить заметку, мы не будем создавать новое подключение, а попросим SessionLocal выдать нам сессию[cite: 252, 253].
# autocommit=False и autoflush=False означают, что данные не сохранятся в базу автоматически — мы будем управлять этим вручную (делать коммит), чтобы избежать ошибок[cite: 227].
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)



# Создаём общий базовый класс для всех моделей SQLAlchemy.
# Все будущие модели таблиц будут наследоваться от Base:
# например, class Note(Base), class Task(Base).
#
# Благодаря этому SQLAlchemy сможет увидеть все модели
# и создать для них таблицы в базе данных.
class Base(DeclarativeBase):
    pass







# 6. Dependency для получения сессии базы данных
# Эта функция создаёт отдельную сессию для одного API-запроса,
# отдаёт её endpoint-у и гарантированно закрывает после завершения запроса.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 7. Тестовый блок запуска
# Код внутри этого блока выполнится ТОЛЬКО в том случае, если ты запустишь конкретно этот файл напрямую.
if __name__ == "__main__":
    try:
        # Пытаемся физически подключиться к базе через нашу "трубу"
        with engine.connect() as connection:
            print("Успешное подключение к базе данных MySQL!")
    except Exception as e:
        # Если что-то пойдет не так (например, выключен Docker или опечатка в пароле),
        # мы перехватим ошибку и выведем её в консоль красным текстом, чтобы понять причину.
        print("Ошибка подключения к базе данных MySQL:")
        print(e)



