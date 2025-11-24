import polars as pl
from typing import Tuple


def rollups(df: pl.DataFrame) -> dict:
    """
    Compute simple rollups over the normalised ECS-like dataframe.

    Notes:
    - We coerce missing columns AND cast to safe types so that operations like
      equality on 'status' don't break when Polars infers a Null dtype.
    - Output is a plain dict, suitable for storing as JSON in a database or
      passing to an LLM.

    Expected columns (if present):
      @ts, user, src_ip, status
    """

    # Ensure key columns exist
    for col in ["@ts", "user", "src_ip", "status"]:
        if col not in df.columns:
            df = df.with_columns(pl.lit(None).alias(col))

    # Cast to Utf8 and fill nulls so we avoid Null-typed series
    df = df.with_columns([
        pl.col("user").cast(pl.Utf8, strict=False).fill_null(""),
        pl.col("src_ip").cast(pl.Utf8, strict=False).fill_null(""),
        pl.col("status").cast(pl.Utf8, strict=False).fill_null(""),
    ])

    # Normalise status to lower-case for comparisons
    df = df.with_columns(
        pl.col("status").str.to_lowercase().alias("status")
    )

    # Simple counts by user
    by_user = (
        df.group_by("user")
          .len()
          .rename({"len": "events"})
    )

    # Failures by user (heuristic: status == 'fail')
    fails_df = df.filter(pl.col("status") == "fail")
    if not fails_df.is_empty():
        fails = (
            fails_df.group_by("user")
                    .len()
                    .rename({"len": "failures"})
        )
    else:
        # empty failures frame with same key column
        fails = pl.DataFrame({"user": [], "failures": []})

    merged = (
        by_user.join(fails, on="user", how="left")
               .fill_null(0)
    )

    # Aggregated metrics
    events_by_user = merged.to_dict(as_series=False)
    distinct_users = int(df.select(pl.col("user").n_unique()).item())
    distinct_ips = int(df.select(pl.col("src_ip").n_unique()).item())

    total_rows = max(df.height, 1)
    fail_rows = fails_df.height
    fail_rate = float(fail_rows / total_rows)

    return {
        "events_by_user": events_by_user,
        "distinct_users": distinct_users,
        "distinct_ips": distinct_ips,
        "fail_rate": fail_rate,
    }