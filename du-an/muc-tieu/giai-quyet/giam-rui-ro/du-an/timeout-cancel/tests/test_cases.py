import asyncio
from app.safe_call import safe_call, ExternalTimeout

# thực hiện trong 2s, chờ 5s => OK
async def case_success():
    print("\n--- CASE SUCCESS ---")
    result = await safe_call(delay=2, timeout=5)
    print("result:", result)

# thực hiện trong 10s, chờ 3s => timeout
async def case_timeout():
    print("\n--- CASE TIMEOUT ---")
    try:
        await safe_call(delay=10, timeout=3)
    except ExternalTimeout as e:
        print("handled:", e)

# thực hiện trong 10s, chờ 20s, nhưng hủy task sau 2s (người dùng thực hiện) => cancel
async def case_cancel():
    print("\n--- CASE CANCEL ---")
    task = asyncio.create_task(
        safe_call(delay=10, timeout=20)
    )

    await asyncio.sleep(2)
    print("cancel task manually")
    task.cancel()

    try:
        await task
    except asyncio.CancelledError:
        print("task cancelled cleanly")
