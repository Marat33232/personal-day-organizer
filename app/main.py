from fastapi import FastAPI

from app import models 
from app.database import Base, engine



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


# Простой endpoint для проверки, что приложение запустилось.
# Если GET /health возвращает {"status": "ok"},
# значит FastAPI работает.
@app.get("/health")
def health_check():
    return {"status": "ok"}

