import asyncio


async def invoke_with_retry(
    llm,
    messages,
    retries=3
):

    for attempt in range(retries):

        try:
            return await llm.ainvoke(messages)

        except Exception as e:

            if attempt == retries - 1:
                raise

            await asyncio.sleep(2 ** attempt)