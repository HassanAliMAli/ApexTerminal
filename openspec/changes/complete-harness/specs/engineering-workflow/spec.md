## ADDED Requirements

### Requirement: Native specialist discovery

Both supported assistants SHALL discover repository-scoped specialist roles through their native agent format.

#### Scenario: Select a reviewer

- **WHEN** the parent delegates independent review
- **THEN** the reviewer checks the supplied change scope and reports evidence without editing the implementation

### Requirement: Staged secret gate

The local commit hook SHALL scan staged changes with redacted output.

#### Scenario: Commit with a staged secret

- **WHEN** the hook detects a secret in the index
- **THEN** the commit check fails and the secret value is redacted
