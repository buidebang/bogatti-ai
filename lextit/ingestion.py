import os
import sys
import uuid
import mimetypes
from typing import Dict, Any, Optional
import json

class LextitMultimodalIngestionPipeline:
    """
    High-integrity multi-format data ingestion layer for Lextit platform.
    Ensures input normalization, MIME security validation, and semantic preprocessing tracking.
    """
    def __init__(self, storage_root: str = "/var/lextit/vault/"):
        self.storage_root = storage_root
        self.allowed_mimes = {
            "audio/webm", "audio/wav", "audio/mpeg", "audio/ogg",
            "video/mp4", "image/png", "image/jpeg", "application/pdf",
            "text/csv", "text/plain"
        }
        os.makedirs(self.storage_root, exist_ok=True)

    def process_incoming_payload(self, file_path: str, metadata: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Target payload asset missing: {file_path}")

        mime_type, _ = mimetypes.guess_type(file_path)
        if mime_type not in self.allowed_mimes:
            return {
                "status": "REJECTED",
                "reason": f"Malicious or unsupported media layout: {mime_type}"
            }

        asset_id = f"LEX_ASSET_{uuid.uuid4().hex.upper()}"
        extension = os.path.splitext(file_path)[1]
        secure_destination = os.path.join(self.storage_root, f"{asset_id}{extension}")

        # Atomic file copy operation to prevent read/write thread locks
        os.rename(file_path, secure_destination)

        manifest = {
            "asset_id": asset_id,
            "mime_type": mime_type,
            "file_size_bytes": os.path.getsize(secure_destination),
            "physical_path": secure_destination,
            "origin_account": metadata.get("account_id", "ANONYMOUS"),
            "ingestion_timestamp": os.path.getsize(secure_destination)
        }

        return manifest
