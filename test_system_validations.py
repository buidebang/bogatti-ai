import pytest
from fastapi.testclient import TestClient
from lextit.api import app
from lextit.geospatial import LextitGeospatialScoringEngine
from lextit.cms import LextitDatabaseTuningEngine
from decimal import Decimal
import sqlite3
import os

client = TestClient(app)

def test_anti_omission_failsafe():
    payload = {
        "message_id": "123",
        "patient_uid": "p456",
        "physician_id": "doc789",
        "raw_message_body": "Patient is here for a checkup.",
        "declared_allergies": [],
        "proposed_prescriptions": [],
        "pertinent_negatives_declared": ["denies_shortness_of_breath"]  # Missing denies_chest_pain
    }

    response = client.post("/api/v5/patient/portal/message", json=payload)

    assert response.status_code == 400
    assert response.json()["detail"]["error_code"] == "FAILED_SAFETY_VALIDATION"
    assert "OMISSION ANOMALY DETECTED" in response.json()["detail"]["remediation_payload"][0]

def test_precision_weighting_evaluation():
    engine = LextitGeospatialScoringEngine("Yazd")
    business_node = {
        "Name": "Dr. Smith Clinic",
        "Rating": "4.5",
        "Reviews_Count": "100",
        "Fake_Suspect": "NO",
        "Has_Verified_Email": "YES"
    }
    local_market_baseline = 4.8

    result = engine.calculate_strategic_opportunity(business_node, local_market_baseline)

    market_deviation = Decimal("4.8") - Decimal("4.5")
    scaling_factor = market_deviation * Decimal("2.0")
    calculated_yield = Decimal("100") * scaling_factor
    expected_score = int(calculated_yield.quantize(Decimal("1"), rounding="ROUND_HALF_UP"))

    assert result["computed_opportunity_score"] == expected_score

def test_database_script_verification(tmp_path):
    db_path = tmp_path / "test_db.sqlite"

    # Setup mock database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE wp_posts (
            id INTEGER PRIMARY KEY,
            post_type TEXT,
            content TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE wp_postmeta (
            meta_id INTEGER PRIMARY KEY,
            post_id INTEGER
        )
    """)

    # Insert dummy data
    cursor.execute("INSERT INTO wp_posts (post_type, content) VALUES ('post', 'Hello World')")
    cursor.execute("INSERT INTO wp_posts (post_type, content) VALUES ('revision', 'Hello World Revision')")
    cursor.execute("INSERT INTO wp_posts (post_type, content) VALUES ('page', 'About Us')")
    conn.commit()
    conn.close()

    engine = LextitDatabaseTuningEngine(f"sqlite:///{db_path}", "localhost")

    # Mocking optimize table for sqlite because it is not supported
    import unittest.mock

    with unittest.mock.patch('sqlalchemy.engine.base.Connection.execute') as mock_execute:
        def side_effect(query):
            if "OPTIMIZE" in str(query):
                return
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute(str(query))
            class MockResult:
                rowcount = cursor.rowcount
            res = MockResult()
            conn.commit()
            conn.close()
            return res
        mock_execute.side_effect = side_effect
        result = engine.purge_redundant_post_revisions()

    assert result["status"] == "SUCCESS"
    assert result["purged_revisions"] == 1

    # Verify core content is not destabilized
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT post_type FROM wp_posts")
    remaining_posts = [row[0] for row in cursor.fetchall()]
    conn.close()

    assert "revision" not in remaining_posts
    assert "post" in remaining_posts
    assert "page" in remaining_posts
