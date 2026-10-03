# Local application threat model

The trust boundary is caller-supplied JSON, never chain state. No private keys, signatures, transaction broadcasting or remote fetches are involved. JSON parsing rejects duplicate keys and nonfinite constants. Domain inputs have collection bounds. HTTP requests use same-origin checks and a random process-local token; the service binds only to 127.0.0.1. Input and output snapshots are stored in an append-only SQLite database. Labels and supplied values are rendered as text.

A local process with access to the loopback bootstrap or database can inspect saved records. The database has no encryption, retention pruning or multi-user permissions. Identifier labels do not establish ownership. Computational bounds prevent some accidental large inputs but do not constitute a hardened untrusted hosting service. The single-threaded server can pause while a bounded analysis runs. This reference app has not been independently security audited.
