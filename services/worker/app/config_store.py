"""
Redis-backed configuration store for format mappings and metrics.

Provides persistent storage for:
- Format detection rules and field mappings (approved by humans)
- Metric configurations per format
- Historical baselines for insight generation
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional

import redis


class FormatConfigStore:
    """
    Redis-backed store for log format configurations.
    
    All configurations stored here have been reviewed and approved by humans,
    ensuring deterministic behavior in the processing pipeline.
    """
    
    def __init__(self, redis_url: Optional[str] = None):
        url = redis_url or os.getenv("REDIS_URL", "redis://localhost:6379")
        self.client = redis.from_url(url, decode_responses=True)
        
    # ------------------------------------------------------------------
    # Format Configurations
    # ------------------------------------------------------------------
    
    def save_format(self, format_id: str, config: dict, approved_by: str = "system") -> None:
        """
        Save an approved format configuration.
        
        Args:
            format_id: Unique identifier for this format
            config: Configuration dict containing:
                - format_name: Human-readable name
                - detection_rules: Rules for detecting this format
                - field_mappings: Mapping from source fields to ECS fields
                - confidence: Agent's confidence score (for reference)
                - reasoning: Agent's reasoning (for audit)
            approved_by: Identifier of who approved this config
        """
        config_with_meta = {
            **config,
            "_approved_by": approved_by,
            "_approved_at": datetime.utcnow().isoformat(),
            "_format_id": format_id,
        }
        self.client.hset("format_configs", format_id, json.dumps(config_with_meta))
    
    def get_format(self, format_id: str) -> Optional[dict]:
        """Retrieve a format configuration by ID."""
        data = self.client.hget("format_configs", format_id)
        return json.loads(data) if data else None
    
    def list_formats(self) -> List[str]:
        """List all registered format IDs."""
        return list(self.client.hkeys("format_configs"))
    
    def get_all_formats(self) -> Dict[str, dict]:
        """Retrieve all format configurations."""
        all_data = self.client.hgetall("format_configs")
        return {k: json.loads(v) for k, v in all_data.items()}
    
    def delete_format(self, format_id: str) -> bool:
        """Delete a format configuration. Returns True if deleted."""
        return self.client.hdel("format_configs", format_id) > 0
    
    # ------------------------------------------------------------------
    # Metric Configurations
    # ------------------------------------------------------------------
    
    def save_metric_config(self, format_id: str, metrics: List[dict]) -> None:
        """
        Save approved metrics for a format.
        
        Args:
            format_id: The format these metrics apply to
            metrics: List of metric configurations, each containing:
                - metric_id: Unique ID
                - name: Human-readable name
                - description: What it measures
                - required_fields: List of required ECS fields
                - computation: Description of aggregation logic
                - enabled: Whether this metric is active
        """
        config = {
            "format_id": format_id,
            "metrics": metrics,
            "_updated_at": datetime.utcnow().isoformat(),
        }
        self.client.hset("metric_configs", format_id, json.dumps(config))
    
    def get_metric_config(self, format_id: str) -> Optional[List[dict]]:
        """Retrieve metric configurations for a format."""
        data = self.client.hget("metric_configs", format_id)
        if data:
            config = json.loads(data)
            return config.get("metrics", [])
        return None
    
    def get_enabled_metrics(self, format_id: str) -> List[dict]:
        """Retrieve only enabled metrics for a format."""
        metrics = self.get_metric_config(format_id)
        if metrics:
            return [m for m in metrics if m.get("enabled", True)]
        return []
    
    # ------------------------------------------------------------------
    # Historical Baselines (for insight generation)
    # ------------------------------------------------------------------
    
    def save_baseline(self, format_id: str, window_key: str, metrics: dict) -> None:
        """
        Save computed metrics as a historical baseline.
        
        Args:
            format_id: The format these metrics came from
            window_key: Time window identifier (e.g., "2024-01-15T00:00:00")
            metrics: The computed metrics dict
        """
        key = f"baseline:{format_id}:{window_key}"
        data = {
            "metrics": metrics,
            "_saved_at": datetime.utcnow().isoformat(),
        }
        self.client.set(key, json.dumps(data))
        # Also maintain a sorted set for easy retrieval of recent baselines
        self.client.zadd(
            f"baselines:{format_id}",
            {window_key: datetime.utcnow().timestamp()}
        )
    
    def get_baseline(self, format_id: str, window_key: str) -> Optional[dict]:
        """Retrieve a specific baseline."""
        key = f"baseline:{format_id}:{window_key}"
        data = self.client.get(key)
        if data:
            return json.loads(data).get("metrics")
        return None
    
    def get_recent_baselines(self, format_id: str, count: int = 5) -> List[dict]:
        """Retrieve the most recent baselines for comparison."""
        # Get recent window keys
        window_keys = self.client.zrevrange(f"baselines:{format_id}", 0, count - 1)
        baselines = []
        for wk in window_keys:
            baseline = self.get_baseline(format_id, wk)
            if baseline:
                baselines.append({"window": wk, "metrics": baseline})
        return baselines
    
    # ------------------------------------------------------------------
    # Utility Methods
    # ------------------------------------------------------------------
    
    def ping(self) -> bool:
        """Check if Redis connection is healthy."""
        try:
            return self.client.ping()
        except redis.ConnectionError:
            return False
    
    def clear_all(self) -> None:
        """Clear all configurations. USE WITH CAUTION - for testing only."""
        self.client.delete("format_configs")
        self.client.delete("metric_configs")
        # Note: baselines are not cleared to preserve historical data


# Singleton instance for easy import
_store_instance: Optional[FormatConfigStore] = None


def get_config_store() -> FormatConfigStore:
    """Get or create the singleton config store instance."""
    global _store_instance
    if _store_instance is None:
        _store_instance = FormatConfigStore()
    return _store_instance
