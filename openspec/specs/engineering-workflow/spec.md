# Engineering workflow

## Purpose

Retain reproducible engineering decisions and verification evidence.

## Requirements

### Requirement: Shared change record

A substantial engineering change SHALL retain its requirements, acceptance criteria, design decisions, and verification evidence in the repository.

#### Scenario: Hand off a change for independent review

- **WHEN** implementation is ready for review
- **THEN** the handoff identifies the OpenSpec change, branch, relevant files, verification evidence, and outstanding risks

### Requirement: Isolated local verification

Local automation SHALL use authorized targets and preserve application credentials and user data.

#### Scenario: Verify a browser or performance tool

- **WHEN** a setup smoke test needs a browser or a server
- **THEN** it uses an isolated browser profile and a loopback fixture
