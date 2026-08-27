import os
import uuid
from pathlib import Path
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from PIL import Image
import io
from app.config import settings
from app.models.user import User
from app.core.deps import require_admin

router = APIRouter(prefix='/api/admin/upload', tags=['Admin Uploads'])

@router.post('')
async def upload_image(
    file: UploadFile = File(...),
    admin_user: User = Depends(require_admin)
):
    if file.content_type not in settings.ALLOWED_IMAGE_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'Недопустимый формат файла. Разрешены: {", ".join(settings.ALLOWED_IMAGE_TYPES)}'
        )

    contents = await file.read()
    if len(contents) > settings.MAX_UPLOAD_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Размер файла превышает лимит в 5 МБ'
        )

    try:
        image = Image.open(io.BytesIO(contents))
        image.verify()
        image = Image.open(io.BytesIO(contents))
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Некорректный или поврежденный файл изображения'
        )

    ext = 'webp' if image.format in ['JPEG', 'PNG', 'WEBP'] else 'jpg'
    filename = f'{uuid.uuid4().hex}.{ext}'
    save_path = settings.UPLOAD_DIR / filename

    max_dim = 2000
    if max(image.size) > max_dim:
        image.thumbnail((max_dim, max_dim), Image.Resampling.LANCZOS)

    if image.mode in ('RGBA', 'P') and ext == 'jpg':
        image = image.convert('RGB')

    image.save(save_path, quality=85, optimize=True)

    url = f'/static/uploads/{filename}'
    return {'url': url, 'filename': filename, 'message': 'Изображение успешно загружено'}
