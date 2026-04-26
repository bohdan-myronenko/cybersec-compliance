"""
Insight Generation Agent for analyzing metrics and providing actionable recommendations.

This agent:
1. Analyzes computed security metrics
2. Compares against historical baselines
3. Identifies anomalies and compliance concerns
4. Generates prioritized, actionable insights
"""

import json
import re
from typing import Dict, List, Any, Optional

from .prompts import INSIGHT_GENERATION_PROMPT, INSIGHT_AGENT_SYSTEM_PROMPT


class InsightGenerationAgent:
    """
    Agent for generating security insights from computed metrics.
    
    Produces actionable findings for compliance reports,
    including severity ratings and specific recommendations.
    """
    
    def __init__(self, chat_client):
        """
        Initialize the agent with an LLM chat client.
        
        Args:
            chat_client: A chat client instance (OllamaChatClient or ExternalChatClient)
        """
        self.chat_client = chat_client
    
    def analyze(
        self,
        metrics: Dict[str, Any],
        baseline: Optional[List[Dict]] = None,
        framework: str = "NIS2",
        period: str = "This Period",
    ) -> Dict[str, Any]:
        """
        Analyze metrics and generate insights.
        
        Args:
            metrics: Computed metrics dict (as produced by MetricsAccumulator.finalize())
            baseline: Historical baseline data for comparison (list of previous periods)
            framework: Compliance framework to focus on (NIS2, ISO27001, etc.)
            period: Human-readable period description
            
        Returns:
            Dict containing:
                - summary: Executive summary
                - risk_level: Overall risk assessment
                - findings: List of specific findings with recommendations
                - positive_observations: Things going well
                - trend_analysis: Improving/degrading/stable metrics
                - raw_response: Original LLM response
                - _eval: Evaluation metadata for research comparison
        """
        import time

        # Format baseline for prompt
        baseline_text = self._format_baseline(baseline)
        
        # Build prompt
        prompt = INSIGHT_GENERATION_PROMPT.format(
            metrics_json=json.dumps(metrics, indent=2),
            baseline=baseline_text,
            framework=framework,
            period=period,
        )
        
        # ---- LLM call with timing ----
        llm_start = time.time()
        llm_error = None
        response = ""
        try:
            response = self.chat_client.chat(INSIGHT_AGENT_SYSTEM_PROMPT, prompt)
        except Exception as e:
            llm_error = str(e)
            result = self._error_response(f"LLM call failed: {str(e)}")
            result["raw_response"] = ""
            result["_eval"] = {
                "llm_latency_seconds": round(time.time() - llm_start, 3),
                "llm_success": False,
                "llm_error": llm_error,
                "json_extract_success": False,
                "json_parse_success": False,
                "raw_parsed_json": None,
                "llm_findings_count": 0,
                "heuristic_findings_added": 0,
                "total_findings_count": 0,
                "prompt_text": prompt,
            }
            return result
        llm_latency = time.time() - llm_start

        # ---- Track JSON extraction/parsing ----
        json_found = bool(re.search(r'\{[\s\S]*\}', response))
        raw_parsed = None
        json_parse_ok = False
        if json_found:
            try:
                raw_parsed = json.loads(re.search(r'\{[\s\S]*\}', response).group())
                json_parse_ok = True
            except (json.JSONDecodeError, AttributeError):
                pass

        # Parse and validate response
        result = self._parse_response(response)
        result["raw_response"] = response

        llm_findings_count = len(result.get("findings", []))
        
        # Add heuristic-based insights if LLM response is incomplete
        result = self._enhance_with_heuristics(result, metrics, baseline)

        total_findings = len(result.get("findings", []))

        # ---- Store eval metadata ----
        result["_eval"] = {
            "llm_latency_seconds": round(llm_latency, 3),
            "llm_success": True,
            "llm_error": None,
            "json_extract_success": json_found,
            "json_parse_success": json_parse_ok,
            "raw_parsed_json": raw_parsed,
            "llm_findings_count": llm_findings_count,
            "heuristic_findings_added": total_findings - llm_findings_count,
            "total_findings_count": total_findings,
            "prompt_text": prompt,
        }
        
        return result
    
    def _format_baseline(self, baseline: Optional[List[Dict]]) -> str:
        """Format baseline data for the prompt."""
        if not baseline:
            return "No historical baseline available - this is the first analysis."
        
        lines = ["Historical data from previous periods:"]
        for i, period_data in enumerate(baseline[:3], 1):  # Limit to 3 periods
            window = period_data.get("window", f"Period {i}")
            period_metrics = period_data.get("metrics", {})
            lines.append(f"\n--- {window} ---")
            lines.append(json.dumps(period_metrics, indent=2))
        
        return "\n".join(lines)
    
    def _parse_response(self, response: str) -> Dict[str, Any]:
        """Parse LLM response into structured insights."""
        # Try to extract JSON from response
        json_match = re.search(r'\{[\s\S]*\}', response)
        
        if not json_match:
            return self._error_response("No JSON found in response")
        
        try:
            data = json.loads(json_match.group())
            return self._validate_insights(data)
        except json.JSONDecodeError as e:
            return self._error_response(f"Failed to parse JSON: {str(e)}")
    
    def _validate_insights(self, data: Dict) -> Dict[str, Any]:
        """Validate and normalize the insights structure."""
        # Ensure required fields exist with defaults
        validated = {
            "summary": data.get("summary", "Analysis complete. Review findings below."),
            "risk_level": self._normalize_risk_level(data.get("risk_level", "medium")),
            "findings": [],
            "positive_observations": data.get("positive_observations", []),
            "trend_analysis": data.get("trend_analysis", {
                "improving": [],
                "degrading": [],
                "stable": [],
            }),
        }
        
        # Validate findings
        raw_findings = data.get("findings", [])
        for i, finding in enumerate(raw_findings):
            validated_finding = self._validate_finding(finding, i + 1)
            if validated_finding:
                validated["findings"].append(validated_finding)
        
        # Sort findings by priority
        validated["findings"].sort(key=lambda f: f.get("priority", 999))
        
        return validated
    
    def _validate_finding(self, finding: Dict, index: int) -> Optional[Dict]:
        """Validate a single finding."""
        if not isinstance(finding, dict):
            return None
        
        return {
            "id": finding.get("id", f"finding_{index:03d}"),
            "severity": self._normalize_severity(finding.get("severity", "medium")),
            "category": finding.get("category", "general"),
            "title": finding.get("title", "Untitled Finding"),
            "description": finding.get("description", ""),
            "evidence": finding.get("evidence", {}),
            "compliance_impact": finding.get("compliance_impact", []),
            "recommendation": finding.get("recommendation", "Review and investigate."),
            "priority": finding.get("priority", index),
        }
    
    def _normalize_risk_level(self, level: str) -> str:
        """Normalize risk level to valid values."""
        level = str(level).lower().strip()
        valid_levels = {"low", "medium", "high", "critical"}
        return level if level in valid_levels else "medium"
    
    def _normalize_severity(self, severity: str) -> str:
        """Normalize severity to valid values."""
        severity = str(severity).lower().strip()
        valid_severities = {"critical", "high", "medium", "low", "info"}
        return severity if severity in valid_severities else "medium"
    
    def _error_response(self, error_msg: str) -> Dict[str, Any]:
        """Generate an error response structure."""
        return {
            "summary": "Analysis could not be completed due to an error.",
            "risk_level": "medium",
            "findings": [{
                "id": "error_001",
                "severity": "info",
                "category": "system",
                "title": "Analysis Error",
                "description": error_msg,
                "evidence": {},
                "compliance_impact": [],
                "recommendation": "Retry the analysis or review metrics manually.",
                "priority": 1,
            }],
            "positive_observations": [],
            "trend_analysis": {"improving": [], "degrading": [], "stable": []},
            "error": error_msg,
        }
    
    def _enhance_with_heuristics(
        self, 
        result: Dict[str, Any], 
        metrics: Dict[str, Any],
        baseline: Optional[List[Dict]],
    ) -> Dict[str, Any]:
        """Add heuristic-based insights to complement LLM analysis."""
        findings = result.get("findings", [])
        existing_ids = {f.get("id") for f in findings}
        
        # Check for high failure rate
        auth_failures = metrics.get("auth_failures", {})
        fail_rate = auth_failures.get("fail_rate", 0)
        
        if fail_rate > 0.25 and "high_fail_rate" not in existing_ids:
            findings.append({
                "id": "high_fail_rate",
                "severity": "high",
                "category": "authentication",
                "title": "High Authentication Failure Rate",
                "description": f"Authentication failure rate is {fail_rate:.1%}, which exceeds the 25% critical threshold.",
                "evidence": {
                    "metric": "fail_rate",
                    "current_value": f"{fail_rate:.1%}",
                    "threshold": "25%",
                },
                "compliance_impact": [
                    {"framework": "NIS2", "clause": "Article 21.2(i)", 
                     "description": "High failure rates may indicate inadequate access control measures."}
                ],
                "recommendation": "Investigate sources of failed authentications. Consider implementing rate limiting and account lockout policies.",
                "priority": 1,
            })
        elif fail_rate > 0.10 and "elevated_fail_rate" not in existing_ids:
            findings.append({
                "id": "elevated_fail_rate",
                "severity": "medium",
                "category": "authentication",
                "title": "Elevated Authentication Failure Rate",
                "description": f"Authentication failure rate is {fail_rate:.1%}, which exceeds the 10% warning threshold.",
                "evidence": {
                    "metric": "fail_rate",
                    "current_value": f"{fail_rate:.1%}",
                    "threshold": "10%",
                },
                "compliance_impact": [],
                "recommendation": "Monitor for potential brute force attempts. Review failed login patterns.",
                "priority": 2,
            })
        
        # Check for attack IP attempts
        attack_attempts = auth_failures.get("attack_ip_attempts", 0)
        if attack_attempts > 0 and "attack_ip_detected" not in existing_ids:
            distinct_attack_ips = auth_failures.get("attack_ip_distinct_ips", 0)
            findings.append({
                "id": "attack_ip_detected",
                "severity": "critical" if attack_attempts > 100 else "high",
                "category": "threat",
                "title": "Known Malicious IP Addresses Detected",
                "description": f"Detected {attack_attempts} login attempts from {distinct_attack_ips} known malicious IP address(es).",
                "evidence": {
                    "metric": "attack_ip_attempts",
                    "current_value": str(attack_attempts),
                    "distinct_ips": str(distinct_attack_ips),
                },
                "compliance_impact": [
                    {"framework": "NIS2", "clause": "Article 21.2(d)",
                     "description": "Threat intelligence integration required for supply chain security."}
                ],
                "recommendation": "Block identified malicious IPs. Review affected accounts for compromise indicators.",
                "priority": 0,
            })
        
        # Check for account takeovers
        takeovers = auth_failures.get("account_takeovers", 0)
        if takeovers > 0 and "account_takeover" not in existing_ids:
            users_affected = auth_failures.get("users_with_takeover", 0)
            findings.append({
                "id": "account_takeover",
                "severity": "critical",
                "category": "threat",
                "title": "Account Takeover Events Detected",
                "description": f"Detected {takeovers} account takeover event(s) affecting {users_affected} user(s).",
                "evidence": {
                    "metric": "account_takeovers",
                    "current_value": str(takeovers),
                    "users_affected": str(users_affected),
                },
                "compliance_impact": [
                    {"framework": "NIS2", "clause": "Article 21.2(i)",
                     "description": "Account security is a fundamental access control requirement."},
                    {"framework": "GDPR", "clause": "Article 32",
                     "description": "Personal data may have been compromised."}
                ],
                "recommendation": "Immediately investigate affected accounts. Force password resets and review recent activity.",
                "priority": 0,
            })
        
        # Check MFA coverage
        mfa = metrics.get("mfa", {})
        mfa_coverage = mfa.get("coverage_pct", 0)
        if mfa_coverage < 100 and "low_mfa_coverage" not in existing_ids:
            total_users = mfa.get("total_users", 0)
            enabled_users = mfa.get("enabled_users", 0)
            findings.append({
                "id": "low_mfa_coverage",
                "severity": "medium" if mfa_coverage > 50 else "high",
                "category": "compliance",
                "title": "Incomplete MFA Coverage",
                "description": f"MFA is enabled for {enabled_users}/{total_users} users ({mfa_coverage:.1f}%).",
                "evidence": {
                    "metric": "mfa_coverage",
                    "current_value": f"{mfa_coverage:.1f}%",
                    "target": "100%",
                },
                "compliance_impact": [
                    {"framework": "NIS2", "clause": "Article 21.2(j)",
                     "description": "Multi-factor authentication is explicitly required."}
                ],
                "recommendation": "Enforce MFA for all user accounts, prioritizing privileged accounts.",
                "priority": 2,
            })
        
        # Re-sort findings by priority
        findings.sort(key=lambda f: f.get("priority", 999))
        result["findings"] = findings
        
        # Update risk level based on findings
        if any(f.get("severity") == "critical" for f in findings):
            result["risk_level"] = "critical"
        elif any(f.get("severity") == "high" for f in findings):
            result["risk_level"] = "high"
        
        return result
    
    def get_summary_text(self, insights: Dict[str, Any]) -> str:
        """Generate a plain-text summary from insights for embedding in reports."""
        lines = []
        
        # Executive summary
        lines.append(f"**Risk Level: {insights.get('risk_level', 'unknown').upper()}**")
        lines.append("")
        lines.append(insights.get("summary", ""))
        lines.append("")
        
        # Key findings
        findings = insights.get("findings", [])
        if findings:
            lines.append("### Key Findings")
            for f in findings[:5]:  # Top 5 findings
                severity = f.get("severity", "medium").upper()
                title = f.get("title", "Untitled")
                desc = f.get("description", "")
                rec = f.get("recommendation", "")
                
                lines.append(f"\n**[{severity}] {title}**")
                lines.append(f"- {desc}")
                lines.append(f"- *Recommendation*: {rec}")
        
        # Positive observations
        positives = insights.get("positive_observations", [])
        if positives:
            lines.append("\n### Positive Observations")
            for p in positives[:3]:
                lines.append(f"- {p}")
        
        return "\n".join(lines)
