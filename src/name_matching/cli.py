import argparse

from .loader import load_fake_names


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="name_matching")
    sub = parser.add_subparsers(dest="command", required=True)

    load_parser = sub.add_parser("load", help="Load fake names into a collection")
    load_parser.add_argument("--count", type=int, required=True)
    load_parser.add_argument(
        "--collection",
        required=True,
        help="Name of the collection to populate",
    )
    return parser


def main(argv: list[str] | None = None) -> None:
    parser = _build_parser()
    args = parser.parse_args(argv)

    if args.command == "load":
        db = load_fake_names(args.count, collection_name=args.collection)
        print(
            f"Loaded {db.count()} names into collection '{args.collection}'.",
        )


if __name__ == "__main__":  # pragma: no cover - manual invocation
    main()
