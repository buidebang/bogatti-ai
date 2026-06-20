import json
import time
import enum
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

class AllergySeverity(str, enum.Enum):
    MILD = "MILD_CUTANEOUS_REACTION"
    MODERATE = "MODERATE_IMMUNOLOGICAL_RESPONSE"
    ANAPHYLAXIS = "SEVERE_LIFE_THREATENING_ANAPHYLAXIS"

class DrugAllergyNode(BaseModel):
    allergen_class: str = Field(..., description="The verified chemical family of the drug, e.g., Penicillins, Sulfonamides.")
    reported_symptom: str = Field(..., description="Exact clinical manifestation described by the patient, e.g., bronchospasm, urticaria.")
    severity_tier: AllergySeverity = Field(..., description="Categorized physiological risk parameter used for prescriptive cross-reactivity audits.")

class ClinicalScribeChartSchema(BaseModel):
    subjective_notes: str = Field(..., description="Raw historical context provided by the patient payload during session audio ingestion.")
    pertinent_negatives_verified: List[str] = Field(..., description="Explicitly stated negative symptoms validated during transcription sweeps to prevent omission penalties.")
    identified_allergies: List[DrugAllergyNode] = Field(default_factory=list, description="Structured array tracking explicit drug allergy disclosures.")
    prescriptive_intent_block: List[str] = Field(..., description="List of proposed pharmacological agents target-selected by the primary care physician.")


class LextitClinicalFailsafeValidator:
    """
    Evaluates extracted clinical data structures against global contraindication charts,
    preventing critical data omissions and cross-reactive prescription delivery errors.
    """
    def __init__(self, cross_reactivity_db_path: str):
        with open(cross_reactivity_db_path, "r", encoding="utf-8") as db_file:
            self.cross_reactivity_rules: Dict[str, list] = json.load(db_file)

    def audit_chart_integrity(self, structured_chart: Dict[str, Any]) -> Dict[str, Any]:
        """
        Enforces structural verification across clinical data inputs, scanning for missing fields,
        omitted negative findings, and high-risk treatment path contradictions.
        """
        audit_report = {
            "evaluation_state": "PASSED_COMPLIANCE_CHECKS",
            "critical_omissions_found": [],
            "deadly_cross_reactivities_flagged": []
        }

        # 1. Anti-Omission Screening: Validating tracking declarations for critical negative symptoms
        required_negatives = ["denies_chest_pain", "denies_shortness_of_breath", "no_known_drug_allergies"]
        for target_negative in required_negatives:
            if target_negative not in structured_chart.get("pertinent_negatives_verified", []):
                audit_report["evaluation_state"] = "FAILED_SAFETY_VALIDATION"
                audit_report["critical_omissions_found"].append(
                    f"OMISSION ANOMALY: Missing explicit statement confirming client {target_negative.replace('_', ' ')} status."
                )

        # 2. Pharmacological Evaluation: Cross-checking cross-reactivity matrices for allergy risks
        for allergy in structured_chart.get("identified_allergies", []):
            allergen_class = allergy.get("allergen_class", "").upper()
            severity = allergy.get("severity_tier", "")

            # Intercepts life-threatening drug choices (e.g., matching Carbapenems with a prior Penicillin Anaphylaxis history)
            if severity == "SEVERE_LIFE_THREATENING_ANAPHYLAXIS" and allergen_class in self.cross_reactivity_rules:
                banned_cross_reactive_agents = self.cross_reactivity_rules[allergen_class]

                for intended_drug in structured_chart.get("prescriptive_intent_block", []):
                    if intended_drug.upper() in banned_cross_reactive_agents:
                        audit_report["evaluation_state"] = "LOCK_TRANICTION_CRITICAL_RISK"
                        audit_report["deadly_cross_reactivities_flagged"].append(
                            f"FATAL ALERGEN TRIGGER: Intent to prescribe [{intended_drug}] conflicts with historic [{allergen_class}] Anaphylaxis block."
                        )

        return audit_report


class LextitInboxTriageRouter:
    """
    Processes messy omnichannel text feeds from patient portals,
    calculates clinical urgency levels, and organizes routing priorities.
    """
    def __init__(self, nlp_client: Any, notification_broker: Any):
        self.nlp = nlp_client
        self.broker = notification_broker
        self.urgency_keywords = {
            "CRITICAL_RED": ["chest pain", "shortness of breath", "dropping sugar", "suicidal planning", "vomiting"],
            "ROUTINE_AMBER": ["refill prescription", "appointment update", "billing question", "normal lab check"]
        }

    def evaluate_message_urgency(self, message_payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parses incoming text context to evaluate clinical priority states,
        filtering structural communication streams based on intent types.
        """
        body_text = message_payload.get("message_body", "").lower()
        computed_acuity_score = 0.0
        target_routing_lane = "AUTOMATED_QUEUE_GREEN"

        # Scan text structures for critical clinical indicators
        if any(keyword in body_text for keyword in self.urgency_keywords["CRITICAL_RED"]):
            computed_acuity_score = 95.5
            target_routing_lane = "IMMEDIATE_ESCALATION_RED"
        elif any(keyword in body_text for keyword in self.urgency_keywords["ROUTINE_AMBER"]):
            computed_acuity_score = 40.0
            target_routing_lane = "STANDARDIZED_QUEUE_AMBER"

        processed_ticket = {
            "message_id": message_payload.get("message_id"),
            "timestamp": time.time(),
            "acuity_score": computed_acuity_score,
            "routing_lane": target_routing_lane,
            "billable_tracking_event": "AUTOMATED_PORTAL_TRIAGE"
        }

        # Trigger high-priority mobile alerts for time-sensitive symptoms
        if target_routing_lane == "IMMEDIATE_ESCALATION_RED":
            self.broker.dispatch_push_alert(
                recipient_id=message_payload.get("assigned_physician_id"),
                alert_payload={"title": "CRITICAL INBOX EVENT", "body": "High-urgency symptom pattern detected inside patient data feed."}
            )

        return processed_ticket
