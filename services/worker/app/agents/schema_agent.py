"""
Schema Inference Agent for analyzing log formats and inferring field mappings.

This agent:
1. Accepts raw log samples
2. Analyzes structure and field patterns
3. Proposes mappings to ECS (Elastic Common Schema) fields
4. Returns structured output for human review
"""

import json
import re
from typing import List, Dict, Optional, Any

from .prompts import SCHEMA_INFERENCE_PROMPT, SCHEMA_AGENT_SYSTEM_PROMPT


# Valid ECS fields that can be mapped to
VALID_ECS_FIELDS = {"@ts", "user", "src_ip", "dst_ip", "action", "status", "resource", "msg"}


class SchemaInferenceAgent:
    """
    Agent for inferring log format schemas from sample data.
    
    Uses an LLM to analyze log samples and propose field mappings,
    but all outputs require human approval before use.
    """
    
    def __init__(self, chat_client):
        """
        Initialize the agent with an LLM chat client.
        
        Args:
            chat_client: A chat client instance (OllamaChatClient or ExternalChatClient)
        """
        self.chat_client = chat_client
    
    def analyze(self, samples: List[str], max_samples: int = 20) -> Dict[str, Any]:
        """
        Analyze log samples and infer schema.
        
        Args:
            samples: List of raw log lines/entries
            max_samples: Maximum number of samples to include in prompt
            
        Returns:
            Dict containing:
                - format_name: Descriptive name
                - format_type: Type of format (jsonl, csv, etc.)
                - detection_rules: Rules for detecting this format
                - field_mappings: Mapping from source to ECS fields
                - unmapped_fields: Fields that couldn't be mapped
                - confidence: Agent's confidence score (0-1)
                - reasoning: Explanation of the analysis
                - raw_response: Original LLM response for debugging
        """
        # Prepare samples for prompt
        samples_text = self._prepare_samples(samples, max_samples)
        
        # Build prompt
        prompt = SCHEMA_INFERENCE_PROMPT.format(samples=samples_text)
        
        # Call LLM
        try:
            response = self.chat_client.chat(SCHEMA_AGENT_SYSTEM_PROMPT, prompt)
        except Exception as e:
            return {
                "error": f"LLM call failed: {str(e)}",
                "confidence": 0.0,
            }
        
        # Parse response
        result = self._parse_response(response)
        result["raw_response"] = response
        
        # Validate and sanitize mappings
        result = self._validate_mappings(result)
        
        return result
    
    def _prepare_samples(self, samples: List[str], max_samples: int) -> str:
        """Prepare samples for inclusion in prompt."""
        # Take up to max_samples, preferring diverse examples
        selected = samples[:max_samples]
        
        # Format as numbered list
        lines = []
        for i, sample in enumerate(selected, 1):
            # Truncate very long lines
            sample_clean = sample.strip()
            if len(sample_clean) > 500:
                sample_clean = sample_clean[:500] + "..."
            lines.append(f"{i}. {sample_clean}")
        
        return "\n".join(lines)
    
    def _parse_response(self, response: str) -> Dict[str, Any]:
        """Parse LLM response into structured format."""
        # Try to extract JSON from response
        json_match = re.search(r'\{[\s\S]*\}', response)
        
        if not json_match:
            return {
                "error": "No JSON found in response",
                "confidence": 0.0,
                "raw_text": response,
            }
        
        try:
            data = json.loads(json_match.group())
            return data
        except json.JSONDecodeError as e:
            return {
                "error": f"Failed to parse JSON: {str(e)}",
                "confidence": 0.0,
                "raw_text": response,
            }
    
    def _validate_mappings(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """Validate and sanitize field mappings."""
        if "error" in result:
            return result
        
        # Validate field_mappings
        field_mappings = result.get("field_mappings", {})
        validated_mappings = {}
        invalid_mappings = []
        
        for source_field, ecs_field in field_mappings.items():
            if ecs_field in VALID_ECS_FIELDS:
                validated_mappings[source_field] = ecs_field
            else:
                invalid_mappings.append({
                    "source": source_field,
                    "target": ecs_field,
                    "reason": f"'{ecs_field}' is not a valid ECS field"
                })
        
        result["field_mappings"] = validated_mappings
        if invalid_mappings:
            result["invalid_mappings"] = invalid_mappings
        
        # Ensure confidence is in valid range
        confidence = result.get("confidence", 0.5)
        result["confidence"] = max(0.0, min(1.0, float(confidence)))
        
        # Ensure required fields exist
        result.setdefault("format_name", "Unknown Format")
        result.setdefault("format_type", "unknown")
        result.setdefault("detection_rules", {})
        result.setdefault("unmapped_fields", [])
        result.setdefault("reasoning", "")
        
        return result
    
    def quick_analyze(self, samples: List[str]) -> Dict[str, Any]:
        """
        Quick heuristic-based analysis without LLM.
        
        Useful for initial format detection before engaging the LLM.
        """
        if not samples:
            return {"format_type": "unknown", "confidence": 0.0}
        
        sample = samples[0].strip()
        
        # Check for JSON
        if sample.startswith("{") and sample.endswith("}"):
            try:
                json.loads(sample)
                return {"format_type": "jsonl", "confidence": 0.9}
            except json.JSONDecodeError:
                pass
        
        # Check for CSV (has commas and consistent field count)
        if "," in sample:
            comma_count = sample.count(",")
            consistent = all(
                s.strip().count(",") == comma_count 
                for s in samples[:10] if s.strip()
            )
            if consistent and comma_count >= 2:
                return {"format_type": "csv", "confidence": 0.7}
        
        # Check for syslog pattern
        syslog_pattern = r"^\w{3}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2}\s"
        if re.match(syslog_pattern, sample):
            return {"format_type": "syslog", "confidence": 0.85}
        
        # Check for key=value pairs
        kv_pattern = r"\w+=\S+"
        if len(re.findall(kv_pattern, sample)) >= 3:
            return {"format_type": "kv", "confidence": 0.7}
        
        return {"format_type": "unknown", "confidence": 0.3}
