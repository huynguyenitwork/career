import asyncio
from app.service import external_service

class ExternalTimeout(Exception):
    pass

async def safe_call(delay: int, timeout: int):
    """
    Gọi external service có timeout.
    Timeout xảy ra => task bị cancel.
    """
    try:
        return await asyncio.wait_for(
            external_service(delay),
            timeout=timeout
        )
    except asyncio.TimeoutError:
        print("[safe_call] timeout, task cancelled")
        raise ExternalTimeout("External service timeout")
