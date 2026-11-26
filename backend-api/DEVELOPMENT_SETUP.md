# Backend development

Follow the [native stack setup](../docs/tutorials/build-from-source/run-the-stack-from-source.md) for runtime installation and initial database configuration. Run the API from `backend` with `python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload` and start the worker separately with `python base_workers.py`.

For verification, see [Run the tests](../docs/tutorials/contribute/run-the-tests.md). Use a separate checkout and disposable databases for test runs.
