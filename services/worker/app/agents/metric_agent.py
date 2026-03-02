"""
Metric Suggestion Agent for proposing security metrics based on available fields.

This agent:
1. Examines available ECS fields and unmapped fields
2. Considers sample data statistics
3. Suggests relevant security metrics with compliance mapping
4. Returns structured output for human selection
"""

import json
import re
from typing import List, Dict, Any, Optional

from .prompts import METRIC_SUGGESTION_PROMPT, METRIC_AGENT_SYSTEM_PROMPT


# Default metrics that can always be computed with basic fields
DEFAULT_METRICS = [
    {
        "metric_id": "total_events",
        "name": "Total Events",
        "description": "Total number of log events in the time window",
        "category": "general",
        "required_fields": [],
        "computation": {
            "type": "count",
            "description": "Count all records",
        },
        "thresholds": {},
        "compliance_relevance": [],
        "priority": "low",
        "enabled": True,
    },
    {
        "metric_id": "distinct_users",
        "name": "Distinct Users",
        "description": "Number of unique users/principals in the logs",
        "category": "authentication",
        "required_fields": ["user"],
        "computation": {
            "type": "unique",
            "description": "Count distinct values of user field",
        },
        "thresholds": {},
        "compliance_relevance": ["NIS2-21.2(i)"],
        "priority": "medium",
        "enabled": True,
    },
    {
        "metric_id": "auth_failure_rate",
        "name": "Authentication Failure Rate",
        "description": "Percentage of authentication attempts that failed",
        "category": "authentication",
        "required_fields": ["status"],
        "computation": {
            "type": "ratio",
            "description": "Count(status='fail') / Count(all auth events)",
            "filter": "action in ['login', 'authenticate', 'auth']",
        },
        "thresholds": {
            "warning": "> 10%",
            "critical": "> 25%",
        },
        "compliance_relevance": ["NIS2-21.2(i)", "ISO27001-A.9.4.3"],
        "priority": "high",
        "enabled": True,
    },
    {
        "metric_id": "distinct_source_ips",
        "name": "Distinct Source IPs",
        "description": "Number of unique source IP addresses",
        "category": "anomaly",
        "required_fields": ["src_ip"],
        "computation": {
            "type": "unique",
            "description": "Count distinct values of src_ip field",
        },
        "thresholds": {},
        "compliance_relevance": [],
        "priority": "medium",
        "enabled": True,
    },
    {
        "metric_id": "failed_logins_by_ip",
        "name": "Failed Logins by IP",
        "description": "Top IPs with the most failed login attempts (brute force indicator)",
        "category": "threat",
        "required_fields": ["src_ip", "status"],
        "computation": {
            "type": "aggregation",
            "description": "Group by src_ip, count where status='fail', sort desc",
            "groupBy": ["src_ip"],
            "filter": "status='fail'",
        },
        "thresholds": {
            "warning": "> 10 failures from single IP",
            "critical": "> 50 failures from single IP",
        },
        "compliance_relevance": ["NIS2-21.2(d)", "ISO27001-A.12.4.1"],
        "priority": "high",
        "enabled": True,
    },
]


class MetricSuggestionAgent:
    """
    Agent for suggesting security metrics based on available data fields.
    
    Uses an LLM to propose relevant metrics, but can also provide
    default metrics based on available ECS fields without LLM.
    """
    
    def __init__(self, chat_client=None):
        """
        Initialize the agent.
        
        Args:
            chat_client: Optional LLM chat client. If None, only default metrics are returned.
        """
        self.chat_client = chat_client
    
    def suggest(
        self,
        available_fields: List[str],
        unmapped_fields: Optional[List[Dict]] = None,
        sample_stats: Optional[Dict] = None,
    ) -> List[Dict[str, Any]]:
        """
        Suggest metrics based on available fields.
        
        Args:
            available_fields: List of ECS fields that are mapped
            unmapped_fields: List of unmapped fields with potential uses
            sample_stats: Statistics from sample data (row count, value distributions, etc.)
            
        Returns:
            List of metric suggestions, each containing:
                - metric_id: Unique identifier
                - name: Human-readable name
                - description: What it measures
                - category: Metric category
                - required_fields: Required ECS fields
                - computation: How to compute
                - thresholds: Warning/critical thresholds
                - compliance_relevance: Related compliance clauses
                - priority: high/medium/low
                - enabled: Default enabled state
        """
        # Start with default metrics filtered by available fields
        metrics = self._get_default_metrics(available_fields)
        
        # If LLM is available, get additional suggestions
        if self.chat_client:
            llm_metrics = self._get_llm_suggestions(
                available_fields, 
                unmapped_fields or [],
                sample_stats or {}
            )
            # Merge, avoiding duplicates by metric_id
            existing_ids = {m["metric_id"] for m in metrics}
            for m in llm_metrics:
                if m.get("metric_id") not in existing_ids:
                    metrics.append(m)
        
        # Sort by priority
        priority_order = {"high": 0, "medium": 1, "low": 2}
        metrics.sort(key=lambda m: priority_order.get(m.get("priority", "low"), 2))
        
        return metrics
    
    def _get_default_metrics(self, available_fields: List[str]) -> List[Dict[str, Any]]:
        """Get default metrics that can be computed with available fields."""
        available_set = set(available_fields)
        applicable_metrics = []
        
        for metric in DEFAULT_METRICS:
            required = set(metric.get("required_fields", []))
            if required.issubset(available_set):
                # Make a copy to avoid modifying the template
                applicable_metrics.append(dict(metric))
        
        return applicable_metrics
    
    def _get_llm_suggestions(
        self,
        available_fields: List[str],
        unmapped_fields: List[Dict],
        sample_stats: Dict,
    ) -> List[Dict[str, Any]]:
        """Get additional metric suggestions from LLM."""
        # Format unmapped fields for prompt
        unmapped_text = ""
        if unmapped_fields:
            unmapped_lines = []
            for f in unmapped_fields[:10]:  # Limit to 10
                name = f.get("name", "unknown")
                sample = f.get("sample_value", "N/A")
                use = f.get("potential_use", "")
                unmapped_lines.append(f"- {name}: sample='{sample}', potential use: {use}")
            unmapped_text = "\n".join(unmapped_lines)
        else:
            unmapped_text = "None"
        
        # Format stats
        stats_text = json.dumps(sample_stats, indent=2) if sample_stats else "No statistics available"
        
        # Build prompt
        prompt = METRIC_SUGGESTION_PROMPT.format(
            fields=", ".join(available_fields),
            unmapped_fields=unmapped_text,
            stats=stats_text,
        )
        
        try:
            response = self.chat_client.chat(METRIC_AGENT_SYSTEM_PROMPT, prompt)
        except Exception as e:
            # Return empty list on error - we still have default metrics
            return []
        
        # Parse response
        return self._parse_response(response)
    
    def _parse_response(self, response: str) -> List[Dict[str, Any]]:
        """Parse LLM response into list of metric suggestions."""
        # Try to extract JSON array from response
        json_match = re.search(r'\[[\s\S]*\]', response)
        
        if not json_match:
            return []
        
        try:
            data = json.loads(json_match.group())
            if not isinstance(data, list):
                return []
            
            # Validate each metric
            valid_metrics = []
            for item in data:
                if self._validate_metric(item):
                    # Ensure enabled defaults to True for new suggestions
                    item.setdefault("enabled", True)
                    valid_metrics.append(item)
            
            return valid_metrics
        except json.JSONDecodeError:
            return []
    
    def _validate_metric(self, metric: Dict) -> bool:
        """Validate a metric suggestion has required fields."""
        required_keys = ["metric_id", "name", "required_fields"]
        for key in required_keys:
            if key not in metric:
                return False
        
        # Ensure metric_id is valid identifier
        metric_id = metric.get("metric_id", "")
        if not re.match(r'^[a-z][a-z0-9_]*$', metric_id):
            # Try to fix it
            metric["metric_id"] = re.sub(r'[^a-z0-9_]', '_', metric_id.lower())
        
        return True
    
    def filter_by_fields(
        self, 
        metrics: List[Dict[str, Any]], 
        available_fields: List[str]
    ) -> List[Dict[str, Any]]:
        """Filter a list of metrics to only those computable with available fields."""
        available_set = set(available_fields)
        return [
            m for m in metrics
            if set(m.get("required_fields", [])).issubset(available_set)
        ]
