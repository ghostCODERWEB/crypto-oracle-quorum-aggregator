# Oracle quorum median aggregator

Filter stale feeds, enforce distinct reporters and evaluate median deviation under quorum requirements.

An original AI-assisted, offline reference application. The domain model is in `cryptolab/engine.py`; validation, scenario comparison, local dashboard, SQLite history and CLI infrastructure are shared with the companion crypto laboratory projects. Repeated infrastructure is not presented as independent protocol innovation. This is neither an audited smart contract nor a production financial service.

## Run and verify

Python 3.11 or later; runtime uses the standard library only.

```sh
python3 -m unittest discover -s tests -v
python3 -m cryptolab examples/input.json
python3 -m cryptolab examples/input.json --format csv --output result.csv
python3 -m cryptolab.server --port 8787 --db runs.sqlite3
```

Use a different port when running several projects. The HTTP service binds to loopback; the dashboard offers editable JSON, independent scenario patches, batch runs, scalar output comparison, exports and persistent run history. It does not connect to wallets, chains or remote price feeds.

## Domain scope

Reporter IDs are labels, not authenticated keys. Median computed before outlier filtering; result includes the fresh-feed median rather than recomputing it.

Input fixture: [examples/input.json](examples/input.json). Recorded regression output: [examples/expected.json](examples/expected.json). Amounts are caller-defined units; monetary normalization is not implicit. Decimal results are strings to avoid binary floating-point serialization; models that explicitly use fractional powers document floating-point approximations.

## Tests and architecture

Domain tests include four independently specified known answers, malformed input rejection, immutability and deterministic replay. Golden outputs guard future changes but do not constitute independent correctness evidence. Workflow tests cover partial batch failure, isolated scenario patching, SQLite persistence and authenticated HTTP routes. CLI tests verify JSON/CSV and atomic output preservation on errors. CI runs on Python 3.11 through 3.14.

Read [model and assumptions](docs/model.md), [dashboard API](docs/dashboard.md), [threat model](docs/threat-model.md), [development roadmap](docs/roadmap.md) and [security reporting](SECURITY.md). No deployments, user funds, audit claims, fabricated history or score guarantees are included.
