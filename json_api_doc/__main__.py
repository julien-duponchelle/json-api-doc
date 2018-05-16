import sys
import json
from json_api_doc import json_api_doc


def main():
    content = sys.stdin.read()
    content = json.loads(content)
    doc = json_api_doc.parse(content)
    print(json.dumps(doc, indent=4))


if __name__ == "__main__":
    main()
