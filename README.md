# Prami

A federated community virtual pet that lives as a Mastodon account. It polls for
mentions, replies to commands, drifts its state over time, and posts on its own now
and then.

## Run

```bash
cp .env.example .env
# set MASTODON_BASE_URL, MASTODON_ACCESS_TOKEN and BOT_ACCOUNT_ACCT
docker compose up -d
docker compose logs -f prami
```

Stop with `docker compose stop`. Reset the database with `docker compose down -v`.

## Try it locally first (no Mastodon needed)

```bash
python -m prami.cli status
python -m prami.cli feed --user @alice@example.com
python -m prami.cli shell
```

Full guide: [docs/local-testing.en.md](docs/local-testing.en.md) ·
[docs/local-testing.pt-br.md](docs/local-testing.pt-br.md)


## License

AGPL-3.0-or-later. See [LICENSE](LICENSE).
