import asyncio
from tests.test_cases import (
    case_success,
    case_timeout,
    case_cancel
)

async def main():
    await case_success()
    await case_timeout()
    await case_cancel()

if __name__ == "__main__":
    asyncio.run(main())
