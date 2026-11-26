## ADDED Requirements

### Requirement: Native application and verification tooling

ApexTerminal SHALL provide native startup, documentation generation and verification entry points.

#### Scenario: Run development and CI without a container runtime

- **WHEN** an operator provisions the documented native database, cache, and language runtimes
- **THEN** the application, docs exporters, and verification jobs run without a container daemon
- **AND** test and application data are isolated
