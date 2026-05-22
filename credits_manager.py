import os
import json
import base64

class CreditManager:
    def __init__(self, storage_path="credits.bin", rate=100000, secret="bugatti_secret"):
        self.storage_path = storage_path
        self.rate = rate  # Toman per USD
        self.secret = secret
        self._balance_toman = self._load_balance()

    def _xor_crypt(self, data: str) -> str:
        return "".join(chr(ord(c) ^ ord(self.secret[i % len(self.secret)])) for i, c in enumerate(data))

    def _load_balance(self):
        if not os.path.exists(self.storage_path):
            return 0
        try:
            with open(self.storage_path, "rb") as f:
                encoded = f.read()
                # Base64 decode then XOR decrypt
                decoded_b64 = base64.b64decode(encoded).decode()
                decrypted = self._xor_crypt(decoded_b64)
                data = json.loads(decrypted)
                return data.get("balance_toman", 0)
        except Exception:
            return 0

    def _save_balance(self):
        data_str = json.dumps({"balance_toman": self._balance_toman})
        # XOR encrypt then Base64 encode
        encrypted = self._xor_crypt(data_str)
        encoded = base64.b64encode(encrypted.encode())
        with open(self.storage_path, "wb") as f:
            f.write(encoded)

    @property
    def balance_usd(self):
        return self._balance_toman / self.rate

    def deduct_usd(self, amount_usd):
        amount_toman = amount_usd * self.rate
        if self._balance_toman >= amount_toman:
            self._balance_toman -= amount_toman
            self._save_balance()
            return True
        return False

    def add_toman(self, amount_toman):
        self._balance_toman += amount_toman
        self._save_balance()

    def get_balance_usd_str(self):
        return f"{self.balance_usd:.2f}"
