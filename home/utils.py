import os
import uuid

import requests
from django.core.files.base import ContentFile

ALLOWED_IMAGE_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.webp', '.gif'}


def download_image_to_field(url: str, instance, field_name: str):
    """
    Download an image from a URL and attach it to a model ImageField.
    Returns (success: bool, message: str).
    """
    if not url:
        return False, "No image URL provided"

    # Strip query params for extension check
    path = url.split("?")[0]
    ext = os.path.splitext(path)[1].lower()
    if ext not in ALLOWED_IMAGE_EXTENSIONS:
        return False, f"Unsupported image type: {ext or 'unknown'}"

    try:
        response = requests.get(url, stream=True, timeout=10)
    except requests.RequestException as exc:
        return False, f"Failed to download image: {exc}"

    if response.status_code != 200:
        return False, f"Failed to download image: HTTP {response.status_code}"

    try:
        content = response.content
    except Exception:
        return False, "Failed to read image content"

    file_field = getattr(instance, field_name, None)
    if file_field is None:
        return False, f"Field '{field_name}' not found on instance"

    filename = f"{uuid.uuid4().hex}{ext}"
    file_field.save(filename, ContentFile(content), save=False)
    return True, "Downloaded"
