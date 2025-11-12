import polars as pl
from typing import Tuple

def rollups(df: pl.DataFrame) -> dict:
    # coerce missing columns
    for col in ["@ts","user","src_ip","status"]:
        if col not in df.columns:
            df = df.with_columns(pl.lit(None).alias(col))
    # simple counts
    by_user = df.group_by("user").len().rename({"len":"events"})
    fails = df.filter(pl.col("status")=="fail").group_by("user").len().rename({"len":"failures"})
    merged = by_user.join(fails, on="user", how="left")
    return {
        "events_by_user": merged.fill_null(0).to_dict(as_series=False),
        "distinct_users": int(df.select(pl.col("user").n_unique()).item()),
        "distinct_ips": int(df.select(pl.col("src_ip").n_unique()).item()),
        "fail_rate": float((df.filter(pl.col("status")=="fail").height) / max(df.height,1))
    }