"""
Prompt templates for the agentic compliance system.

These prompts are designed to:
1. Produce structured JSON outputs for easy parsing
2. Include confidence scores for human review
3. Provide reasoning for audit trails
"""

# -----------------------------------------------------------------------------
# Schema Inference Prompt
# -----------------------------------------------------------------------------

SCHEMA_INFERENCE_PROMPT = """You are a log format analysis expert. Analyze the provided log samples and infer their structure.

LOG SAMPLES:
{samples}

TARGET ECS (Elastic Common Schema) FIELDS:
- @ts: timestamp (ISO 8601 or epoch)
- user: username, user ID, or principal identifier
- src_ip: source IP address
- dst_ip: destination IP address
- action: event type (login, logout, access, create, delete, sudo, etc.)
- status: outcome (success, fail, denied, error, unknown)
- resource: target resource (file path, URL, service name, database, etc.)
- msg: human-readable message or description

ANALYSIS INSTRUCTIONS:
1. Identify the log format type (JSON, CSV, syslog, key=value, custom, etc.)
2. Map source fields to ECS fields where possible
3. Note any security-relevant fields that don't map to ECS
4. Provide detection rules that can identify this format

Return a JSON object with this exact structure:
{{
  "format_name": "descriptive name for this log format",
  "format_type": "jsonl|csv|syslog|kv|custom",
  "detection_rules": {{
    "type": "pattern|header|structure",
    "pattern": "regex pattern if applicable",
    "required_fields": ["field1", "field2"],
    "description": "how to detect this format"
  }},
  "field_mappings": {{
    "source_field_name": "ecs_field_name"
  }},
  "unmapped_fields": [
    {{"name": "field_name", "sample_value": "example", "potential_use": "description"}}
  ],
  "confidence": 0.85,
  "reasoning": "explanation of the analysis and any uncertainties"
}}

IMPORTANT:
- Only map fields you are confident about
- Set confidence between 0.0 and 1.0 based on clarity of the format
- List all potentially useful unmapped fields for metric suggestions
- Be conservative - it's better to leave a field unmapped than map it incorrectly
"""

# -----------------------------------------------------------------------------
# Metric Suggestion Prompt
# -----------------------------------------------------------------------------

METRIC_SUGGESTION_PROMPT = """You are a security metrics expert. Given the available data fields, suggest relevant security metrics that can be computed.

AVAILABLE ECS FIELDS: {fields}

ADDITIONAL UNMAPPED FIELDS: {unmapped_fields}

SAMPLE DATA STATISTICS:
{stats}

COMPLIANCE FRAMEWORKS TO CONSIDER:
- NIS2 (Network and Information Security Directive 2)
- ISO 27001 (Information Security Management)
- SOC 2 (Service Organization Control)
- GDPR (General Data Protection Regulation)
- PCI DSS (Payment Card Industry Data Security Standard)

METRIC CATEGORIES:
1. Authentication & Access Control (login failures, MFA coverage, privilege usage)
2. Anomaly Detection (unusual patterns, geographic anomalies, time-based anomalies)
3. Threat Indicators (known bad IPs, account takeover attempts, brute force)
4. Compliance Posture (policy violations, audit gaps, control effectiveness)

Return a JSON array of metric suggestions:
[
  {{
    "metric_id": "unique_snake_case_id",
    "name": "Human Readable Metric Name",
    "description": "What this metric measures and why it matters",
    "category": "authentication|anomaly|threat|compliance",
    "required_fields": ["ecs_field1", "ecs_field2"],
    "computation": {{
      "type": "count|ratio|unique|aggregation|threshold",
      "description": "How to compute this metric",
      "groupBy": ["field to group by, if any"],
      "filter": "condition to filter records, if any"
    }},
    "thresholds": {{
      "warning": "threshold value or description",
      "critical": "threshold value or description"
    }},
    "compliance_relevance": ["NIS2-21.2", "ISO27001-A.9.4"],
    "priority": "high|medium|low"
  }}
]

GUIDELINES:
- Only suggest metrics that can be computed from the available fields
- Prioritize security-relevant metrics over general statistics
- Include specific compliance clause references where applicable
- Provide practical thresholds based on industry standards
"""

# -----------------------------------------------------------------------------
# Insight Generation Prompt
# -----------------------------------------------------------------------------

INSIGHT_GENERATION_PROMPT = """You are a cybersecurity compliance analyst. Analyze the computed metrics and provide actionable insights.

COMPUTED METRICS:
{metrics_json}

HISTORICAL BASELINE (previous periods for comparison):
{baseline}

COMPLIANCE FRAMEWORK FOCUS: {framework}

TIME PERIOD ANALYZED: {period}

ANALYSIS REQUIREMENTS:
1. Identify anomalies by comparing current metrics to baseline
2. Flag compliance concerns with specific regulation references
3. Prioritize findings by severity and actionability
4. Provide specific, actionable recommendations

Return a JSON object with this structure:
{{
  "summary": "One paragraph executive summary of the security posture",
  "risk_level": "low|medium|high|critical",
  "findings": [
    {{
      "id": "finding_001",
      "severity": "critical|high|medium|low|info",
      "category": "authentication|access_control|anomaly|compliance|threat",
      "title": "Brief title of the finding",
      "description": "Detailed explanation of what was observed",
      "evidence": {{
        "metric": "metric_name",
        "current_value": "value",
        "baseline_value": "value if available",
        "deviation": "percentage or description of change"
      }},
      "compliance_impact": [
        {{"framework": "NIS2", "clause": "Article 21.2(i)", "description": "impact on compliance"}}
      ],
      "recommendation": "Specific action to take",
      "priority": 1
    }}
  ],
  "positive_observations": [
    "List of things that are working well"
  ],
  "trend_analysis": {{
    "improving": ["metrics showing improvement"],
    "degrading": ["metrics showing degradation"],
    "stable": ["metrics that are stable"]
  }}
}}

GUIDELINES:
- Be specific with numbers and percentages
- Reference actual metric values in findings
- Prioritize findings by risk and actionability (priority 1 = most urgent)
- Include both problems and positive observations for balanced reporting
- Keep recommendations practical and implementable
"""

# -----------------------------------------------------------------------------
# System Prompts
# -----------------------------------------------------------------------------

SCHEMA_AGENT_SYSTEM_PROMPT = """You are an expert log format analyst specializing in security logs. 
Your task is to analyze log samples and produce accurate field mappings to the Elastic Common Schema (ECS).
Always respond with valid JSON. Be conservative in your mappings - accuracy is more important than completeness."""

METRIC_AGENT_SYSTEM_PROMPT = """You are a security metrics specialist with expertise in compliance frameworks.
Your task is to suggest relevant, computable metrics based on available data fields.
Always respond with valid JSON. Focus on metrics that provide actionable security insights."""

INSIGHT_AGENT_SYSTEM_PROMPT = """You are a senior cybersecurity compliance analyst.
Your task is to analyze security metrics and provide actionable insights for compliance reporting.
Always respond with valid JSON. Be specific, cite evidence, and prioritize findings by severity."""
