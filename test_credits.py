from credits_manager import CreditManager
import os

def test_credit_manager():
    storage = "test_credits.bin"
    if os.path.exists(storage):
        os.remove(storage)

    cm = CreditManager(storage_path=storage, rate=100000)
    assert cm.balance_usd == 0.0

    cm.add_toman(100000) # $1.00
    assert cm.balance_usd == 1.0
    assert cm.get_balance_usd_str() == "1.00"

    success = cm.deduct_usd(0.05)
    assert success is True
    assert cm.balance_usd == 0.95

    success = cm.deduct_usd(1.0)
    assert success is False
    assert cm.balance_usd == 0.95

    if os.path.exists(storage):
        os.remove(storage)

if __name__ == "__main__":
    test_credit_manager()
    print("Test passed!")
