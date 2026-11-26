# Native runtime verification

The native reference exporters, docs typecheck, and docs build completed. The frontend exporter ran 19 reference checks. Backend Ruff and strict OpenSpec validation passed.

A fresh targeted backend run passed 35 checks for native MySQL, Valkey, SQLite, and settings generation. Before the session restart, the isolated native HTTPS stack passed Chromium sign-in setup and the two authentication cases. The full backend and browser runs did not produce a retained final summary. Hosted CI should verify the converted fixtures and all browser projects.

The standalone example backend still uses Docker to test network boundaries, read-only filesystems, privileges, and resource limits. It needs an equivalent verified Linux sandbox before those definitions can be removed. No security assertions were removed.
