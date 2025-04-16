import os
from langfuse.callback import CallbackHandler
from typing import Optional

_langfuse_handler: Optional[CallbackHandler] = None

def get_langfuse_handler() -> CallbackHandler:
    global _langfuse_handler
    if _langfuse_handler is None:
        public_key = os.environ.get("LANGFUSE_PUBLIC_KEY")
        secret_key = os.environ.get("LANGFUSE_SECRET_KEY")

        if not public_key or not secret_key:
            raise ValueError("Langfuse public key or secret key not found in environment variables.")  

        _langfuse_handler = CallbackHandler(
            secret_key=secret_key,
            public_key=public_key,
            host="https://cloud.langfuse.com"
        )
    return _langfuse_handler


langfuse_handler = get_langfuse_handler()