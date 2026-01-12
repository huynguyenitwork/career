import asyncio

async def external_service(delay: int):
    """
    Giả lập service bên ngoài:
    - delay nhỏ: OK
    - delay lớn: coi như treo
    """
    print(f"[external] start, delay={delay}s")
    await asyncio.sleep(delay)
    print("[external] done")
    return "OK"
