# Account Cookies

## Required Field

For every account-specific Xiaohongshu operation, require one of these fields:

```yaml
account_name: "<required account alias>"
cookies_str: "<required for cookie-based API workflows; account-specific cookie string>"
```

or:

```yaml
account_name: "<required account alias>"
cookies:
  a1: "<required when API expects cookie dict>"
  web_session: "<required when API/session needs it>"
```

## Rules

- Each account must have its own cookie value.
- Never reuse one account's cookie for another account.
- Never write cookie values into `SKILL.md`, reference files, committed fixtures, logs, or public output.
- Never upload cookie values to GitHub.
- Put local account config in ignored files such as `accounts.local.json`, `.env`, or a local secret store.
- If the user says which account to use but no cookie/login exists for that account, stop and ask for that account's cookie or browser login.

## Example Local Config Shape

This is a shape only. Do not include real cookie values in the repo.

```json
{
  "accounts": [
    {
      "account_name": "chengdu-student-a",
      "cookies_str": "<REQUIRED_PER_ACCOUNT_COOKIE>"
    }
  ]
}
```

## Browser Session Alternative

If using OpenCLI/browser automation with an already logged-in persistent browser session:

- Verify the active account before saving a draft.
- Treat the authenticated browser session as the credential source.
- Do not export or print cookies unless the user explicitly asks and understands the risk.
