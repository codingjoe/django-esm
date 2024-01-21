from django.conf import settings
from django.core.files.storage import FileSystemStorage

root_storage = FileSystemStorage(
    location=settings.BASE_DIR, base_url=settings.STATIC_URL
)
node_modules_storage = FileSystemStorage(
    location=settings.BASE_DIR / "node_modules", base_url=settings.STATIC_URL
)
