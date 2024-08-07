# ------------------------------------
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
# ------------------------------------
from datetime import datetime, timezone
from typing import Optional


def raise_if_time_invalid(not_before: Optional[datetime], expires_on: Optional[datetime]) -> None:
    now = datetime.now(timezone.utc)
    if (not_before and expires_on) and not not_before <= now <= expires_on:
        raise ValueError(f"This client's key is useable only between {not_before} and {expires_on} (UTC)")
    if not_before and not_before > now:
        raise ValueError(f"This client's key is not useable until {not_before} (UTC)")
    if expires_on and expires_on <= now:
        raise ValueError(f"This client's key expired at {expires_on} (UTC)")
