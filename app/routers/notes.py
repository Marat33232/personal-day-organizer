from fastapi import APIRouter, Depends, Body, HTTPException
from sqlalchemy.orm import Session

from app import models
from app.database import get_db

# APIRouter — это отдельный набор endpoint-ов.
# Здесь будут лежать только endpoint-ы, связанные с заметками.
# Благодаря prefix="/notes" все адреса внутри этого файла начнутся с /notes.
router = APIRouter(
    prefix="/notes", 
    tags=["notes"],
)



# Получить список всех заметок.
# Полный адрес: GET /notes
@router.get("/")
def get_notes(db: Session = Depends(get_db)):
    notes = db.query(models.Note).order_by(models.Note.id).all()

    # Возвращаем список словарей вручную.
    return[
        {
            "id": note.id, 
            "title": note.title,
            "content": note.content, 
            "created_at": note.created_at,
        }
        for note in notes
    ]



# Создать новую заметку.
# Полный адрес: POST /notes
@router.post("/")
def create_note(
    title: str = Body(...),
    content: str = Body(""), 
    db: Session = Depends(get_db)):
    # Создаём ORM-объект заметки в памяти.
    note = models.Note(title=title, content=content)
    
    # Добавляем заметку текущую сессию.
    db.add(note)
    # Фиксируем изменение в базе данных.
    db.commit()
     # Обновляем объект из базы, чтобы получить id и created_at.
    db.refresh(note)

    # Возвращаем созданную заметку.
    return {
        "id": note.id,
        "title": note.title,
        "content": note.content,
        "created_at": note.created_at,
    }


# Получить одну заметку по id.
# Полный адрес: GET /notes/{note_id}
@router.get("/{note_id}")
def get_note(note_id: int, db: Session = Depends(get_db)):
    # Ищем первую заметку, у которой id совпадает с note_id из URL.
    note = db.query(models.Note).filter(models.Note.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return {
        "id": note.id,
        "title": note.title,
        "content": note.content,
        "created_at": note.created_at,
    }


# Удалить заметку по id.
# Полный адрес: DELETE /notes/{note_id}
@router.delete("/{note_id}")
def delete_note(note_id: int, db: Session = Depends(get_db)):
    # Ищем заметку, у которой id совпадает с note_id из URL.
    note = db.query(models.Note).filter(models.Note.id == note_id).first()
    # # Если такой заметки нет, возвращаем HTTP 404.
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    # Удаляем заметку из базы данных.
    db.delete(note)
    # Фиксируем изменение.
    db.commit()
    # Возвращаем сообщение об успешном удалении.
    return {"status": "deleted", "id": note_id}




# Обновить заметку по id.
# Полный адрес: PUT /notes/{note_id}
@router.put("/{note_id}")
def update_mote(
    note_id: int,
    title: str = Body(...), 
    content: str = Body(...),
    db: Session = Depends(get_db), 
):
    # Сначала ищем заметку, которую хотим изменить.
    note = db.query(models.Note).filter(models.Note.id == note_id).first()


    # Если заметка не найдена, возвращаем HTTP 404.
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    # Меняем поля ORM-объекта.
    note.title = title
    note.content = content

    # Фиксируем изменения в базе данных.
    db.commit()

    # Обновляем объект из базы.
    db.refresh(note)

    # Возвращаем обновлённую заметку.
    return {
        "id": note.id,
        "title": note.title,
        "content": note.content,
        "created_at": note.created_at,
    }