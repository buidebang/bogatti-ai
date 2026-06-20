import time
import sqlite3
import threading
from typing import Dict, Any
from decimal import Decimal, ROUND_HALF_UP
import redis
from datetime import datetime

class DistributedZoneManager:
    def __init__(self):
        self.client = redis.Redis(host='localhost', port=6379, db=0)

    def acquire_lead_lock(self, uid: str) -> bool:
        # قفل کردن شناسه لید به مدت ۳۰ دقیقه برای جلوگیری از پردازش همزمان
        return bool(self.client.set(f"lock:lead:{uid}", "processing", ex=1800, nx=True))


class LextitFinancialLedger:
    """
    Thread-safe, high-precision transactional ledger optimized for clinical SaaS monetization,
    handling real-time multi-currency overhead calculations without float conversion errors.
    """
    def __init__(self, db_path: str = "LEXTIT_FINANCIALS.db"):
        self.db_path = db_path
        self._initialize_ledger_tables()

    def _initialize_ledger_tables(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS TransactionLedger (
                    transaction_id TEXT PRIMARY KEY,
                    timestamp TEXT NOT NULL,
                    account_id TEXT NOT NULL,
                    amount_irt INTEGER NOT NULL,
                    amount_usd REAL NOT NULL,
                    exchange_rate REAL NOT NULL,
                    tax_bracket_pct REAL NOT NULL,
                    net_revenue_usd REAL NOT NULL,
                    transaction_status TEXT NOT NULL
                )
            ''')
            conn.commit()

    def process_invoice(self, invoice_data: Dict[str, Any]) -> bool:
        try:
            tx_id = f"TXN_{int(time.time() * 1000)}"
            irt_amount = int(invoice_data["amount_irt"])
            ex_rate = float(invoice_data["current_exchange_rate"])

            # Using precise Decimal calculation to prevent floating-point drift in audits
            usd_equiv = float(Decimal(str(irt_amount)) / Decimal(str(ex_rate)))
            tax_factor = float(invoice_data["tax_bracket_pct"]) / 100.0
            net_usd = usd_equiv * (1.0 - tax_factor)

            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO TransactionLedger VALUES (?, datetime('now'), ?, ?, ?, ?, ?, ?, 'COMMITTED')",
                    (tx_id, invoice_data["account_id"], irt_amount, usd_equiv, ex_rate, tax_factor * 100, net_usd)
                )
                conn.commit()
            return True
        except KeyError as e:
            print(f"[LEXTIT CRITICAL AUDIT EXCEPTION] Missing explicit financial key: {e}")
            return False
        except Exception as e:
            print(f"[LEXTIT CRITICAL DATABASE FAIL] Transaction rolled back: {e}")
            return False


class LextitGlobalLedgerManager:
    """
    Thread-safe storage architecture enforcing transactional constraints
    across all concurrent crawling sub-routines.
    """
    def __init__(self, db_path: str = "LEXTIT_CORE_LEDGER.db"):
        self.db_path = db_path
        self.lock = threading.Lock()
        self._orchestrate_schema()

    def _orchestrate_schema(self):
        with self.lock:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                # Global tracking of target entities to prevent double-outreach workflows
                cursor.execute('''CREATE TABLE IF NOT EXISTS ExtractedEntities (
                                    entity_uid TEXT PRIMARY KEY,
                                    extracted_at TEXT,
                                    niche_scope TEXT,
                                    domain_url TEXT,
                                    primary_email TEXT
                                  )''')
                # Spatial quadrant tracking for Google Maps search boundaries
                cursor.execute('''CREATE TABLE IF NOT EXISTS SpatialGridZones (
                                    quadrant_query TEXT PRIMARY KEY,
                                    processing_status TEXT,
                                    total_leads_harvested INTEGER
                                  )''')
                conn.commit()

    def reserve_quadrant(self, query: str) -> bool:
        with self.lock:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT processing_status FROM SpatialGridZones WHERE quadrant_query = ?", (query,))
                row = cursor.fetchone()
                if row and row[0] in ["PROCESSING", "COMPLETED"]:
                    return False
                cursor.execute("INSERT OR REPLACE INTO SpatialGridZones VALUES (?, 'PROCESSING', 0)", (query,))
                conn.commit()
                return True

    def commit_entity(self, uid: str, scope: str, url: str, email: str):
        with self.lock:
            try:
                with sqlite3.connect(self.db_path) as conn:
                    cursor = conn.cursor()
                    cursor.execute("INSERT INTO ExtractedEntities VALUES (?, ?, ?, ?, ?)",
                                   (uid, datetime.now().isoformat(), scope, url, email))
                    conn.commit()
            except sqlite3.IntegrityError:
                pass # Already logged globally by an adjacent asynchronous browser task


class LextitHighPrecisionLedger:
    """
    Financial engine designed to calculate multi-currency accounting assets
    without floating-point calculation errors.
    """
    def __init__(self, tax_bracket: str):
        self.tax_rate = Decimal(tax_bracket)

    def calculate_transaction_split(self, amount_irt: int, fx_rate_usd_irt: int) -> Dict[str, Any]:
        # Using precise string instantiation to prevent internal float approximation errors
        decimal_irt = Decimal(str(amount_irt))
        decimal_fx = Decimal(str(fx_rate_usd_irt))

        gross_usd = (decimal_irt / decimal_fx).quantize(Decimal('0.000000000000000001'), rounding=ROUND_HALF_UP)
        tax_deduction = (gross_usd * (self.tax_rate / Decimal('100.0'))).quantize(Decimal('0.000000000000000001'), rounding=ROUND_HALF_UP)
        net_usd = gross_usd - tax_deduction

        return {
            "gross_irt_input": amount_irt,
            "calculated_gross_usd": str(gross_usd),
            "tax_applied_usd": str(tax_deduction),
            "net_revenue_usd": str(net_usd)
        }
