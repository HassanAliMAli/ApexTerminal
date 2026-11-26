## Design

Use PostgreSQL and MySQL for the same migration cases they cover now. Run test data stores on loopback with disposable databases and run browser fixtures as native processes. Use the existing Python reference exporter and the Node reference commands directly.

Keep application data untouched during the migration. Use separate test identities and directories and terminate only processes created by the test harness.
