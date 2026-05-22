import asyncio
from ai_service import AIService

async def test_ai_service():
    service = AIService()
    response = await service.get_response("GPT-4o", "openai", "Hello")
    print(f"Response: {response}")
    assert "OpenAI" in response
    await service.close()

if __name__ == "__main__":
    asyncio.run(test_ai_service())
