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

    list_parser = sub.add_parser("list", help="List names in a collection")
    list_parser.add_argument(
        "--direction",
        choices=["top", "bottom"],
        default="top",
        help="List from the top or bottom of the collection (default: top)",
    )
    list_parser.add_argument(
        "--count",
        type=int,
        default=10,
        help="Number of names to list (default: 10)",
    )
    list_parser.add_argument(
        "--collection",
        default="names",
        help="Collection to list from (default: names)",
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
    elif args.command == "list":
        db_instance = ChromaDB(collection_name=args.collection)
        names = db_instance.list_documents()
        count = args.count
        selected = names[:count] if args.direction == "top" else names[-count:]
        for name in selected:
            print(name)


if __name__ == "__main__":  # pragma: no cover - manual invocation
    main()
