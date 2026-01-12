**Security & Secrets Guidance**

- **Do not commit secrets.** Never commit Personal Access Tokens (PATs), passwords, private keys, or other secrets to the repository. If a secret is accidentally committed, assume it is compromised.

- **Rotate immediately if exposed.** If any credential (PAT, key, or token) was pasted or exposed, revoke it immediately and create a replacement with the minimum required scopes.

- **Use GitHub Secrets / CI secrets.** Store registry tokens, model-download credentials, and other secrets in GitHub Secrets (or your CI provider secrets) and reference them in workflows — do not hard-code them in workflows or files.

- **Least privilege.** When creating PATs or service tokens grant only the minimal scopes required (e.g., `packages: write` for package pushes). Avoid `repo` scope unless necessary.

- **Avoid secrets in runtime envs.** If you must provide URLs or keys via environment variables (for model downloads), prefer secret-backed runtime injection (Runpod/host secrets) and never commit those values to the repo.

- **If you find exposed credentials in this repo** file an issue, revoke the credential, rotate the secret, and update the team. Consider scanning history for leaked values using `git log --all -S '<token-part>'` or tools like `git-secrets`.

Maintainers: please follow these rules and call out any accidental exposure immediately so we can respond quickly.

CI: This repository is configured to build and push container images via GitHub Actions. To trigger the CI build-and-push, push to `main` or run the `Build and push` workflow manually from the Actions tab.

Timestamp: 2026-01-12
