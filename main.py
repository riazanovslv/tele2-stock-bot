import argparse

from trade import TradeService, LotType

parser = argparse.ArgumentParser()
parser.add_argument(
    "--phone-number", type=str, help="Your phone number.", required=True
)
parser.add_argument("--token", type=str, help="Token for the tele2 api.", required=True)
parser.add_argument("--lot-price", type=int, help="Lot price.", required=True)
parser.add_argument("--lot-volume", type=int, help="Lot volume.", required=True)
parser.add_argument(
    "--lot-type",
    type=LotType,
    help="Lot type: `min` or `gb`.",
    required=True,
    choices=list(LotType),
)
parser.add_argument(
    "--max-lots",
    type=int,
    help="Max lots that will be places in the same time.",
    default=4,
)

parser.add_argument(
    "--max-iterations",
    type=int,
    help="Number of bids. Defaults to tele2 limit of 100.",
    default=100,
)
parser.add_argument(
    "--delay", type=int, help="Delay between lot placements, default is 3.", default=3
)

if __name__ == "__main__":
    args = parser.parse_args()

    TradeService(
        phone_number=args.phone_number,
        token=args.token,
        lot_price=args.lot_price,
        lot_volume=args.lot_volume,
        lot_type=args.lot_type,
        lot_emojis=["scream", "scream", "scream"],
        max_lots=args.max_lots,
        max_iterations=args.max_iterations,
        delay=args.delay,
    ).run()
