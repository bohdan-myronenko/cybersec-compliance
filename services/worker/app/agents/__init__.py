"""
Agent modules for the hybrid agentic compliance system.

This package contains LLM-powered agents that assist with:
- Schema inference for new log formats
- Metric suggestions based on available fields
- Insight generation from computed metrics

All agent outputs require human approval before affecting the pipeline.
"""

from .schema_agent import SchemaInferenceAgent
from .metric_agent import MetricSuggestionAgent
from .insight_agent import InsightGenerationAgent

__all__ = [
    "SchemaInferenceAgent",
    "MetricSuggestionAgent", 
    "InsightGenerationAgent",
]
