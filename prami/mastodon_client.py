import logging

from mastodon import Mastodon

log = logging.getLogger("prami.mastodon")


class PramiClient:
    def __init__(self, config):
        self.config = config
        self.api = Mastodon(
            access_token=config.mastodon_access_token,
            api_base_url=config.mastodon_base_url,
            ratelimit_method="pace",
        )
        self.me = self.api.account_verify_credentials()
        log.info("Authenticated as @%s (id=%s)", self.me.acct, self.me.id)

    def fetch_mentions(self, since_id=None):
        return self.api.notifications(types=["mention"], since_id=since_id, limit=30)

    def reply(self, status, text, visibility):
        return self.api.status_post(text, in_reply_to_id=status.id, visibility=visibility)

    def post(self, text, visibility):
        return self.api.status_post(text, visibility=visibility)

    def favourite(self, status):
        return self.api.status_favourite(status.id)

    def boost(self, status):
        return self.api.status_reblog(status.id)
