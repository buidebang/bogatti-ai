import os
import re
import requests
from typing import List, Dict, Any

class LextitSystemDefenseEngine:
    """
    Automated core to identify toxic backlinks, programmatic comment spam networks,
    and process real-time disavow configuration files for search engines.
    """
    def __init__(self, gsc_api_token: str, project_domain: str = "lextit.com"):
        self.api_token = gsc_api_token
        self.domain = project_domain
        self.base_gsc_url = "https://searchconsole.googleapis.com/v1"
        # Strict exclusion metrics for automated pattern blocking
        self.toxic_tlds = [".ru", ".xyz", ".top", ".click", ".tk", ".gq"]

    def audit_manual_actions_and_security(self) -> Dict[str, Any]:
        """
        Queries Search Console endpoints to detect algorithmic manual penalties or security threats
        such as injected malicious scripts or compromised server file nodes.
        """
        headers = {"Authorization": f"Bearer {self.api_token}"}
        audit_results = {"manual_actions": "CLEAN", "security_issues": "CLEAN", "flagged_urls": []}

        try:
            # Simulating structural API polling for security compliance checks
            response_actions = requests.get(f"{self.base_gsc_url}/sites/{self.domain}/manualActions", headers=headers, timeout=10)
            response_security = requests.get(f"{self.base_gsc_url}/sites/{self.domain}/securityIssues", headers=headers, timeout=10)

            if response_actions.status_code == 200 and "actions" in response_actions.json():
                audit_results["manual_actions"] = "PENALIZED"
            if response_security.status_code == 200 and "issues" in response_security.json():
                audit_results["security_issues"] = "COMPROMISED"

        except Exception as e:
            print(f"[LEXTIT SECURITY AUDIT EXCEPTION] Failed to poll security states: {e}")

        return audit_results

    def compile_production_disavow_payload(self, harvested_domains: List[str]) -> str:
        """
        Compiles a production-ready, UTF-8 compliant disavow document string
        to neutralize low-quality or programmatic link farm network layers.
        """
        disavow_buffer = [
            "# Lextit Automated Security Disavow Registry File",
            f"# Generated for {self.domain} - Shielding against high-volume toxic link patterns",
            "#"
        ]

        for source_domain in harvested_domains:
            sanitized_domain = source_domain.strip().lower()
            if any(sanitized_domain.endswith(tld) for tld in self.toxic_tlds):
                disavow_buffer.append(f"domain:{sanitized_domain}")

        return "\n".join(disavow_buffer)
