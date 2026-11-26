# Native runtime verification

The native reference exporters, docs typecheck, and docs build completed. The frontend exporter ran 19 reference checks. Backend Ruff and strict OpenSpec validation passed.

A fresh targeted backend run passed 35 checks for native MySQL, Valkey, SQLite, and settings generation. Before the session restart, the isolated native HTTPS stack passed Chromium sign-in setup and the two authentication cases. The full backend and browser runs did not produce a retained final summary. Hosted CI should verify the converted fixtures and all browser projects.

The example backend now runs as a native loopback development service. The retired Docker deployment and the tests specific to its isolation configuration were removed. Native application tests and PostgreSQL integration CI remain. Isolation for a shared deployment is no longer supplied by this example.

The native example suite passed all 11 tests. Docusaurus type checking and the docs build passed. The native runtime promotion passed 30 checks in PR #8.
