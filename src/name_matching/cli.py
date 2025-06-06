import argparse

from .db import ChromaDB
from .loader import load_fake_names
from .matcher import NameMatcher


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

    match_parser = sub.add_parser("match", help="Find matches for a name")
    match_parser.add_argument("--name", required=True, help="Query name")
    match_parser.add_argument(
        "--type",
        choices=["fuzzy", "embedding", "hybrid"],
        required=True,
        help="Matching algorithm to use",
    )
    match_parser.add_argument(
        "--collection",
        default="names",
        help="Collection to search (default: names)",
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
    elif args.command == "match":
        db_instance = ChromaDB(collection_name=args.collection)
        names = db_instance.list_documents()
        matcher = NameMatcher(names, mode=args.type)
        matches = matcher.find_matches(args.name)
        for match in matches:
            print(match)


if __name__ == "__main__":  # pragma: no cover - manual invocation
    main()
