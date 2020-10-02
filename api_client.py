import uplink

# https://spb.tele2.ru/api/subscribers/79523812302/exchange/lots/created
from uplink.auth import BearerToken

USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36"


class Tele2ClientError(Exception):
    """Base exception."""


@uplink.response_handler
def raise_for_status(response):
    if response.status_code == 200:
        return response

    raise Tele2ClientError(
        "{0}: {1}".format(
            response.status_code,
            response.text,
        )
    )


@uplink.returns.json
@uplink.json
@uplink.ratelimit(calls=2, period=1)
class Tele2Client(uplink.Consumer):
    def __init__(self, base_url, access_token):
        bearer_auth = BearerToken(access_token)
        super().__init__(base_url=base_url, auth=bearer_auth, hooks=(raise_for_status,))
        self.session.headers["User-Agent"] = USER_AGENT

    @uplink.put("api/subscribers/{phone_number}/exchange/lots/created")
    def add_lot(
        self,
        phone_number: uplink.Path(),
        **lot_data: uplink.FieldMap(),
    ):
        """Add a lot."""

    @uplink.patch("api/subscribers/{phone_number}/exchange/lots/created/{lot}")
    def update_lot(
        self,
        phone_number: uplink.Path(),
        lot: uplink.Path(),
        **lot_data: uplink.FieldMap(),
    ):
        """Update the lot."""

    @uplink.delete("api/subscribers/{phone_number}/exchange/lots/created/{lot}")
    def delete_lot(
        self,
        phone_number: uplink.Path(),
        lot: uplink.Path(),
    ):
        """Removes the lot."""
