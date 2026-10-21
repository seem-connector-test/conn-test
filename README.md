# seem GitHub connector test fixtures

Public, synthetic data for testing the seem GitHub connector against real GitHub
security alerts. **This code and its dependencies are intentionally vulnerable.
Do not deploy it or use it as an application template.** No real customer data or
credentials belong here.

## What the scanners should find

| Source | Fixture | Expected finding |
| --- | --- | --- |
| CodeQL | `app.py`, `/accounts` | SQL injection from a request parameter into an in-memory database query |
| CodeQL | `app.py`, `/greeting` | Reflected cross-site scripting from unescaped HTML |
| Dependabot | `requirements.txt`, Werkzeug 2.2.2 | Known dependency vulnerabilities, including multipart parsing resource exhaustion and cookie parsing issues |

The database contains only `demo-alice` and `demo-bob` and is discarded after each
request. There is no server startup code, external service, or persistent database.
Alert counts and severity depend on GitHub's current query suite and advisory data;
enabling a scan does not guarantee a particular count.

## Enable GitHub scanning

1. Push this repository's `main` branch to GitHub.
2. In repository **Settings → Advanced Security** (called **Code security and
   analysis** in some layouts), enable the dependency graph and Dependabot alerts.
   Leave automatic security updates off initially so the vulnerable baseline stays
   available. A `dependabot.yml` is not needed for dependency vulnerability alerts;
   that file configures scheduled version-update pull requests.
3. Allow GitHub Actions for this repository. The included **CodeQL** workflow scans
   Python on pushes to `main`, pull requests targeting `main`, and manual runs.
   It does not install dependencies or start the application. Use this workflow as
   CodeQL's **advanced setup**; do not also enable CodeQL default setup. If default
   setup is already enabled, switch it off before using this workflow.
4. After analysis finishes, check the repository's **Security** (or **Security and
   quality**) tab for code scanning and Dependabot alerts. Dependabot processing
   may finish separately from the CodeQL workflow.
5. Install the connector's GitHub App on this repository with the required alert
   read permissions. Keep its private key outside this repository.

## Optional local smoke test

Python 3.12 is suitable. Use a disposable virtual environment:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install --only-binary=:all: -r requirements.txt
.venv/bin/python -m unittest -v
```

The four tests use Flask's in-process test client: no listening port or external
network requests. Two tests deliberately confirm the flaws exist. When testing
remediation, update those expectations along with the code fix.

## Exercise connector metrics

First ingest the open alerts as a baseline. Then dismiss one alert with a synthetic
test explanation and ingest again to exercise dismissed-state handling. To test
fixed-state handling, fix a code flaw or upgrade an affected dependency on `main`,
wait for GitHub to update its alerts, and ingest again. Keep at least one open alert
for comparison. Real alert age starts when GitHub creates it; use the connector's
fake endpoint for deterministic historical dates and ageing boundaries.

## References

- [GitHub security feature availability](https://docs.github.com/en/code-security/getting-started/github-security-features)
- [Configure Dependabot alerts](https://docs.github.com/en/code-security/how-tos/secure-your-supply-chain/secure-your-dependencies/configure-dependabot-alerts)
- [CodeQL workflow configuration](https://docs.github.com/en/code-security/reference/code-scanning/workflow-configuration-options)
- [Werkzeug multipart parsing advisory](https://github.com/advisories/GHSA-xg9f-g7g7-2323)
- [Werkzeug cookie parsing advisory](https://github.com/advisories/GHSA-px8h-6qxv-m22q)
