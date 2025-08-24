from pathlib import Path
import aiofiles
import hashlib
from datetime import datetime

async def save_uploaded_file(file) -> str:
    """Securely save uploaded file with timestamp and hash"""
    upload_dir = Path("output/uploaded_files")
    upload_dir.mkdir(exist_ok=True)
    
    file_hash = hashlib.md5()
    file_content = await file.read()
    file_hash.update(file_content)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    ext = Path(file.filename).suffix
    new_filename = f"{timestamp}_{file_hash.hexdigest()[:8]}{ext}"
    save_path = upload_dir / new_filename
    
    async with aiofiles.open(save_path, "wb") as f:
        await f.write(file_content)
    
    return str(save_path)
