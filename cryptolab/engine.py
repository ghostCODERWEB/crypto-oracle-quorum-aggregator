"""Filter stale feeds, enforce distinct reporters and evaluate median deviation under quorum requirements."""

from .common import (
    number,
    integer,
    identity,
    records,
    chronology,
    allocate,
    result,
    validate_document,
)
from decimal import Decimal


def _analyze(d):
    now = integer(d["now"])
    age = integer(d["max_age"])
    quorum = integer(d["quorum"], 1)
    maxdev = number(d["max_deviation"], maximum=1)
    accepted = []
    rejected = []
    for f in records(d["feeds"], "id"):
        timestamp = integer(f["timestamp"])
        price = number(f["price"], minimum="0.000000000000000001")
        if timestamp > now or now - timestamp > age:
            rejected.append({"id": f["id"], "reason": "timestamp"})
        else:
            accepted.append((price, f["id"]))
    if len(accepted) < quorum:
        raise ValueError("insufficient fresh quorum")
    values = sorted(p for p, _ in accepted)
    middle = len(values) // 2
    median = (
        values[middle] if len(values) % 2 else (values[middle - 1] + values[middle]) / 2
    )
    inliers = [(p, i) for p, i in accepted if abs(p - median) / median <= maxdev]
    for p, i in accepted:
        if abs(p - median) / median > maxdev:
            rejected.append({"id": i, "reason": "deviation"})
    if len(inliers) < quorum:
        raise ValueError("insufficient inlier quorum")
    return result(
        {
            "median": median,
            "accepted": [i for _, i in inliers],
            "rejected": rejected,
            "spread": (max(p for p, _ in inliers) - min(p for p, _ in inliers))
            / median,
        }
    )


def analyze(document):
    validate_document(document)
    try:
        return result(_analyze(document))
    except (KeyError, TypeError, ArithmeticError, RecursionError) as error:
        raise ValueError("invalid domain input: " + str(error)) from error
