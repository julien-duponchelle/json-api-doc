import sys
import json
from . import parse


def main():
    content = sys.stdin.read()
    content = json.loads(content)
    doc = parse(content)
    print(json.dumps(doc, indent=4))


if __name__ == "__main__":
    main()
