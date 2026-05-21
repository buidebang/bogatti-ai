import asyncio
from main import BugattiApp
import os
import json

async def test_history_persistence():
    app = BugattiApp()
    async with app.run_test() as pilot:
        # Add some credits to make sure it works
        app.credit_manager.add_toman(100000)

        # Simulate user input
        await pilot.click("#chat-input")
        for char in "Hello":
            await pilot.press(char)
        await pilot.press("enter")
        await asyncio.sleep(2) # Wait for AI response

        # Check if history file exists
        history_files = os.listdir("history")
        print(f"History files: {history_files}")
        assert len(history_files) > 0

        # Check content
        with open(f"history/{history_files[0]}", "r") as f:
            data = json.load(f)
            assert data[0]["text"] == "Hello"
            assert data[1]["sender"] == "ai"

    print("History persistence test passed!")

if __name__ == "__main__":
    asyncio.run(test_history_persistence())
