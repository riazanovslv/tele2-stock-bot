import json
from collections import deque
from contextlib import suppress
from enum import Enum
from time import sleep

from api_client import Tele2Client, Tele2ClientError

TELE2_BASE_URL = "https://spb.tele2.ru/"


class LotType(Enum):
    gb = "gb"
    min = "min"


class TrafficType(Enum):
    voice = "voice"
    data = "data"


class LotService:
    def __init__(self, phone_number, token):
        self._phone_number = phone_number
        self._client = Tele2Client(TELE2_BASE_URL, token)

    def add_lot(self, lot_type: LotType, amount, price):
        volume = {"value": amount, "uom": lot_type.value}
        cost = {"amount": price, "currency": "rub"}

        if lot_type == LotType.min:
            traffic_type = TrafficType.voice.value
        else:
            traffic_type = TrafficType.data.value

        response = self._client.add_lot(
            self._phone_number,
            volume=volume,
            trafficType=traffic_type,
            cost=cost,
        )

        return response["data"]["id"]

    def update_lot(self, lot, price, emojis):
        cost = {"amount": price, "currency": "rub"}

        response = self._client.update_lot(
            self._phone_number,
            lot,
            emojis=emojis,
            cost=cost,
        )

        return response["data"]["id"]

    def remove_lot(self, lot):
        with suppress(Tele2ClientError):
            self._client.delete_lot(
                self._phone_number,
                lot,
            )


class TradeService:
    def __init__(
        self,
        phone_number,
        token,
        lot_price,
        lot_volume,
        lot_type,
        lot_emojis,
        max_lots=1,
        max_iterations=100,
        delay=60 * 10,
    ):
        self._lot_service = LotService(phone_number, token)
        self._current_lots = deque()
        self._max_lots = max_lots
        self._max_iterations = max_iterations
        self._delay = delay
        self._lot_type = lot_type
        self._lot_volume = lot_volume
        self._lot_price = lot_price
        self._lot_emojis = lot_emojis

    def run(self):
        try:
            self.place_lots(self._max_iterations, self._delay)
        finally:
            for lot in self._current_lots:
                self._lot_service.remove_lot(lot)

    def place_lots(self, count, delay):
        for _ in range(count):
            if len(self._current_lots) == self._max_lots:
                self._lot_service.remove_lot(self._current_lots.popleft())

            self._current_lots.append(self._add_lot())

            sleep(delay)

    def _add_lot(self):
        lot = self._lot_service.add_lot(
            self._lot_type,
            self._lot_volume,
            self._lot_price,
        )
        self._lot_service.update_lot(
            lot,
            self._lot_price,
            self._lot_emojis,
        )

        return lot
