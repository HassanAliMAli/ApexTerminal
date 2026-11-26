## Why

Local ApexTerminal development and repository verification must run on native processes.

## Changes

- Replace container-driven startup, reference generation, tests, and CI with native commands.
- Preserve the service versions, test coverage, and security controls used by each existing path.
- Remove container build and publishing definitions after their callers migrate.

## Impact

Developer startup, test service provisioning, browser CI, documentation, and release tooling.
