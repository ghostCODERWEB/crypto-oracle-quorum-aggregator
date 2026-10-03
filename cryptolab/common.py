"""Validation and arithmetic shared by the synthetic reference applications."""

import math
from decimal import Decimal, InvalidOperation


def number(value, minimum=0, maximum=None):
    if isinstance(value, bool) or not isinstance(value, (int, float, str)):
        raise ValueError("number required")
    try:
        value = Decimal(str(value))
    except InvalidOperation:
        raise ValueError("invalid decimal")
    if (
        not value.is_finite()
        or value < Decimal(str(minimum))
        or (maximum is not None and value > Decimal(str(maximum)))
    ):
        raise ValueError("number outside allowed range")
    return value


def integer(value, minimum=0, maximum=None):
    if (
        isinstance(value, bool)
        or not isinstance(value, int)
        or value < minimum
        or (maximum is not None and value > maximum)
    ):
        raise ValueError("integer outside allowed range")
    return value


def identity(value):
    if not isinstance(value, str) or not value.strip() or len(value) > 200:
        raise ValueError("nonempty identifier required")
    return value


def records(value, key=None):
    if (
        not isinstance(value, list)
        or len(value) > 10000
        or any(not isinstance(row, dict) for row in value)
    ):
        raise ValueError("bounded object list required")
    if key:
        ids = [identity(row[key]) for row in value]
        if len(set(ids)) != len(ids):
            raise ValueError("duplicate identifier")
    return value


def chronology(value):
    value = records(value)
    times = [integer(row["timestamp"]) for row in value]
    if times != sorted(times):
        raise ValueError("chronological events required")
    return value


def result(value):
    if isinstance(value, Decimal):
        return str(value.normalize()) if value else "0"
    if isinstance(value, dict):
        return {str(k): result(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [result(v) for v in value]
    if isinstance(value, float) and not math.isfinite(value):
        raise ValueError("nonfinite result")
    return value


def allocate(total, weights):
    integer(total)
    if any(integer(v) < 0 for v in weights.values()) or sum(weights.values()) == 0:
        raise ValueError("positive total weight required")
    denominator = sum(weights.values())
    out = {k: total * v // denominator for k, v in weights.items()}
    ranked = sorted(weights, key=lambda k: (-(total * weights[k] % denominator), k))
    for k in ranked[: total - sum(out.values())]:
        out[k] += 1
    return out


def validate_document(document):
    if not isinstance(document, dict):
        raise ValueError("input must be an object")
    count = 0

    def walk(value, depth):
        nonlocal count
        count += 1
        if count > 100000 or depth > 25:
            raise ValueError("document limit exceeded")
        if isinstance(value, float) and not math.isfinite(value):
            raise ValueError("nonfinite input")
        if isinstance(value, (list, dict)):
            if len(value) > 10000:
                raise ValueError("collection limit exceeded")
            for item in value.values() if isinstance(value, dict) else value:
                walk(item, depth + 1)

    walk(document, 0)
