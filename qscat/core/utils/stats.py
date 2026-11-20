# Copyright (c) 2024 UP-MSI COASTER TEAM.
# QSCAT Plugin — GPL-3.0 license

"""Pure-Python statistics helpers (no compiled dependencies, works on any OS)."""

from __future__ import annotations

import math
from functools import cache


def student_t_cdf(t: float, df: int) -> float:
    """Cumulative distribution function of Student's t distribution.

    Uses the closed-form series for integer degrees of freedom
    (Abramowitz & Stegun, 26.7.3 and 26.7.4).

    Args:
        df: Degrees of freedom (integer >= 1).

    Returns:
        P(T <= t).
    """
    theta = math.atan2(t, math.sqrt(df))
    sin_t, cos_t = math.sin(theta), math.cos(theta)
    cos2 = cos_t * cos_t

    if df % 2 == 1:
        a = theta
        if df > 1:
            term = total = cos_t
            for k in range(3, df, 2):
                term *= cos2 * (k - 1) / k
                total += term
            a += sin_t * total
        a *= 2 / math.pi
    else:
        term = total = 1.0
        for k in range(2, df, 2):
            term *= cos2 * (k - 1) / k
            total += term
        a = sin_t * total

    return 0.5 + 0.5 * a


@cache
def inv_student_t(df: int, p: float) -> float:
    """Inverse of Student's t CDF (the t value such that P(T <= t) = p).

    Drop-in replacement for ALGLIB's ``invstudenttdistribution(k, p)``.

    Args:
        df: Degrees of freedom (integer >= 1).
        p: Probability, 0 < p < 1.

    Returns:
        The t value.

    Raises:
        ValueError: If df is not an integer >= 1 or p is not in (0, 1).
    """
    if int(df) != df or df < 1:
        raise ValueError(f"Degrees of freedom must be an integer >= 1, got {df}.")
    if not 0 < p < 1:
        raise ValueError(f"Probability must be between 0 and 1 (exclusive), got {p}.")
    df = int(df)

    if p == 0.5:
        return 0.0
    if p < 0.5:
        return -inv_student_t(df, 1 - p)

    # Bracket the root, then bisect until floating-point precision.
    lo, hi = 0.0, 1.0
    while student_t_cdf(hi, df) < p:
        lo, hi = hi, hi * 2
    while True:
        mid = (lo + hi) / 2
        if mid in (lo, hi):
            return mid
        if student_t_cdf(mid, df) < p:
            lo = mid
        else:
            hi = mid
