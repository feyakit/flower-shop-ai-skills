# Draft Save

## Default Behavior

Save to draft box only. Do not publish unless the user explicitly asks for publication.

## OpenCLI Browser Path

Use this path when the correct Xiaohongshu account is already logged in through a persistent browser session:

```bash
opencli xiaohongshu whoami --site-session persistent -f yaml
opencli xiaohongshu publish "<body>" \
  --title "<title>" \
  --images "/abs/path/cover.jpg,/abs/path/detail.jpg" \
  --draft \
  --site-session persistent \
  -f yaml
```

Before saving, verify the logged-in account. If it is the wrong account, stop and ask the user to switch/login.

## Cookie-Based API Path

Use this path only when the selected account has `cookies_str` or `cookies`.

Required input:

```yaml
account_name: "<required>"
cookies_str: "<required, account-specific>"
```

Never commit or print the cookie value.

## Verification

After saving:

- Read the draft list and find the expected title.
- Confirm image count.
- Confirm content. If normal draft readers show empty content, inspect raw fields such as:
  - `content.draftStore.desc`
  - `content.draftStore.descInnerHTML`
  - `content.draftStore.imgList`

## Cleanup

If retries create duplicate drafts:

- Delete only drafts clearly created in the current task.
- Prefer UI/tool deletion first.
- If local creator drafts are stored in IndexedDB and tool deletion leaves stale records, only remove the exact current-task draft key after verifying title and image count.
