# Mastodon setup

How to give Prami its own Mastodon account and go live — after everything passes locally.

> Do not connect Prami to Mastodon until the local tests pass and you've tried the CLI.
> See [LOCAL_TESTING.md](LOCAL_TESTING.md).

## 1. Create the pet's account

Make a dedicated Mastodon account for Prami on your instance. Don't use a personal account —
Prami posts and reacts on its own.

## 2. Create an access token

1. Log in as the **pet's** account.
2. Go to **Preferences → Development → New application**.
3. Name it (e.g. `Prami`) and grant these scopes:
   - `read:notifications` — to see mentions
   - `read:accounts` — to identify users
   - `read:statuses` — to read mention content
   - `write:statuses` — to reply and post
   - `write:favourites` — only if you enable favourites
   - `write:follows` is **not** needed
4. Save, open the application, and copy the **access token**.

Reblogs (boosts) use the standard `write:statuses` scope.

## 3. Configure `.env`

```bash
cp .env.example .env
```

Set at least:

- `MASTODON_BASE_URL` — e.g. `https://your.instance.social`
- `MASTODON_ACCESS_TOKEN` — the token from step 2
- `BOT_ACCOUNT_ACCT` — the pet's acct, e.g. `prami@your.instance.social`

The social features start **off**. Turn them on deliberately once you're comfortable:

- `ENABLE_FAVOURITES=true` to let Prami favourite worthy interactions
- `ENABLE_TEACH_COMMAND=true` plus `ADMIN_ACCOUNTS=...` to open the moderated teach queue
- `ENABLE_EVENTS=true` for community events
- `ENABLE_BOOSTS=true` only if you really want boosts (they stay rare)

## 4. Run

```bash
docker compose up -d
docker compose logs -f prami
```

Prami authenticates, starts polling for mentions, runs state decay, and posts on its own at
the configured interval. Mention it with `@prami help` from another account to confirm it
replies.

## 5. Going-live checklist

- [ ] `pytest` passes locally
- [ ] You've driven Prami through the CLI (see LOCAL_TESTING.md)
- [ ] `.env` has the token, base URL, and bot acct set
- [ ] You've decided which social features to enable (favourites/boosts/teach/events)
- [ ] `ADMIN_ACCOUNTS` is set if you enabled teach
- [ ] Default visibility is `unlisted` (recommended) so Prami doesn't flood timelines
- [ ] `docker compose up -d` shows a successful authentication in the logs
