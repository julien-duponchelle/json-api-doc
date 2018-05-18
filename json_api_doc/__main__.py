import sys
import json
from . import parse


def main():
    if len(sys.argv) > 1:
        for path in sys.argv[1:]:
            with open(path) as f:
                _read_file(f)
    else:
        _read_file(sys.stdin)


def _read_file(content):
    try:
        content = json.load(content)
    except json.decoder.JSONDecodeError:
        print("Invalid JSON file", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        sys.exit(1)
    doc = parse(content)
    print(json.dumps(doc, indent=4))


if __name__ == "__main__":
    main()
