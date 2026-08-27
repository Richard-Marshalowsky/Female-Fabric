import os
import uuid
import io
from pathlib import Path
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from PIL import Image
import httpx
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

    max_dim = 2000
    if max(image.size) > max_dim:
        image.thumbnail((max_dim, max_dim), Image.Resampling.LANCZOS)

    if image.mode in ('RGBA', 'P') and ext == 'jpg':
        image = image.convert('RGB')

    output_buffer = io.BytesIO()
    image.save(output_buffer, format='WEBP' if ext == 'webp' else 'JPEG', quality=85, optimize=True)
    processed_bytes = output_buffer.getvalue()

    # 1. Try Supabase Storage if configured (Cloudflare Worker production environment)
    if settings.SUPABASE_URL and settings.SUPABASE_KEY:
        try:
            supabase_endpoint = f"{settings.SUPABASE_URL}/storage/v1/object/{settings.SUPABASE_STORAGE_BUCKET}/{filename}"
            headers = {
                "Authorization": f"Bearer {settings.SUPABASE_KEY}",
                "Content-Type": f"image/{ext}"
            }
            async with httpx.AsyncClient(timeout=10.0) as client:
                res = await client.post(supabase_endpoint, content=processed_bytes, headers=headers)
                if res.status_code in (200, 201):
                    public_url = f"{settings.SUPABASE_URL}/storage/v1/object/public/{settings.SUPABASE_STORAGE_BUCKET}/{filename}"
                    return {'url': public_url, 'filename': filename, 'message': 'Изображение успешно загружено в Supabase Storage'}
        except Exception as e:
            print(f"[Supabase Storage Warn] {e}")

    # 2. Local filesystem storage (for local dev server / writable environment)
    try:
        save_path = settings.UPLOAD_DIR / filename
        with open(save_path, 'wb') as f:
            f.write(processed_bytes)
        url = f'/static/uploads/{filename}'
        return {'url': url, 'filename': filename, 'message': 'Изображение успешно загружено'}
    except Exception as e:
        import base64
        b64 = base64.b64encode(processed_bytes).decode('utf-8')
        mime = f'image/{ext}'
        url = f'data:{mime};base64,{b64}'
        return {'url': url, 'filename': filename, 'message': 'Изображение обработано (Data URI)'}
