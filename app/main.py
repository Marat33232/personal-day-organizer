from fastapi import FastAPI, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app import models 
from app.database import Base, engine, get_db

# Импортируем роутер заметок.
# Внутри него лежат endpoint-ы GET /notes и POST /notes.
from app.routers import notes


# Временное создание таблиц для учебного этапа.
# SQLAlchemy смотрит на все модели, которые унаследованы от Base,
# и создаёт соответствующие таблицы в базе данных, если их ещё нет.
#
# Важно: импорт from app import models нужен выше,
# чтобы SQLAlchemy увидела модель Note до вызова create_all().
#
# Позже, когда появятся миграции Alembic, эту строку уберём.
Base.metadata.create_all(bind= engine)



# Создаём экземпляр FastAPI-приложения.
# Именно этот объект запускает Uvicorn командой:
# uvicorn app.main:app --reload
app = FastAPI()




# Подключаем notes router к основному FastAPI-приложению.
app.include_router(notes.router)


# Простой endpoint для проверки, что приложение запустилось.
# Если GET /health возвращает {"status": "ok"},
# значит FastAPI работает.
@app.get("/health")
def health_check():
    return {"status": "ok"}




# Тестовый endpoint для проверки подключения к базе данных через Dependency.
# Он нужен, чтобы убедиться:
# 1. FastAPI вызывает get_db()
# 2. get_db() создаёт SQLAlchemy Session
# 3. endpoint получает эту сессию в параметр db
# 4. через db можно выполнить SQL-запрос к MySQL
# 5. после завершения запроса сессия будет закрыта в get_db()
@app.get("/db-check")
def db_check(db: Session = Depends(get_db)):
        # Выполняем самый простой SQL-запрос.
        # SELECT 1 не читает реальные таблицы и не меняет данные.
        # Он просто проверяет, что соединение с MySQL работает.
        result = db.execute(text("SELECT 1")).scalar()

        # Возвращаем результат проверки.
        # Если всё хорошо, db_result будет равен 1.
        return {"status": "ok", "db_result": result}
