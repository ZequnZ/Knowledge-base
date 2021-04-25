"""Generate a markdown file of with leetcode question info"""
import argparse
import json
import sys

import html2text
import requests


def parse_arguments(argv):

    # Define a parser
    parser = argparse.ArgumentParser(description="description")

    # Define arguments
    parser.add_argument("title", type=str, nargs="*", help="leetcode question title")

    return parser.parse_args()


def main(args):

    question = (" ").join(args.title).lower().replace(" ", "-")
    question_link = "https://leetcode.com/problems/" + question + "/"
    query = {
        "operationName": "questionData",
        "variables": {"titleSlug": question},
        "query": """query questionData($titleSlug: String\u0021) {
            question(titleSlug: $titleSlug) {
                questionId
                questionFrontendId
                title
                titleSlug
                content
                difficulty
                similarQuestions
                exampleTestcases
                topicTags {
                name
                slug}
                hints
                sampleTestCase
                metaData
        }
    }""",
    }
    headers = {"content-type": "application/json", "cache-control": "no-cache"}
    query_link = "https://leetcode.com/graphql"
    # Query the info of the question from leetcode
    r = requests.request(
        "POST",
        query_link,
        data=json.dumps(query),
        headers=headers,
        timeout=10,
    )

    # Parse the result:

    # title
    title = (
        r.json()["data"]["question"]["questionId"]
        + ". "
        + r.json()["data"]["question"]["title"]
    )

    # difficulty
    difficulty = (
        "Difficulty: " + "`" + r.json()["data"]["question"]["difficulty"] + "`\n\n"
    )

    # Tags
    tags = ""
    for tag in r.json()["data"]["question"]["topicTags"][:-1]:
        tags += "`" + tag["name"] + "`, "
    tags += "`" + r.json()["data"]["question"]["topicTags"][-1]["name"] + "`"
    tags = "<details>\n<summary> Tags</summary>\n\n" + tags + "\n</details>\n\n"

    # content
    content = (
        html2text.html2text(r.json()["data"]["question"]["content"])
        .replace("**Input:**", "Input:")
        .replace("**Output:**", "Output:")
        .replace("**Explanation:**", "Explanation:")
        .replace("**Constraints:**", "### Constraints:")
    )

    with open(title + ".md", "w", encoding="utf-8") as f:
        title = "# " + title + "\n"
        f.write(title)
        f.write(f"[Link]({question_link})\n\n")
        f.write(difficulty)
        f.write(tags)
        f.write("## Description:  \n" + content)
        if len(r.json()["data"]["question"]["hints"]) > 0:
            # hints
            hints = "### Hints:\n"
            for i, h in enumerate(r.json()["data"]["question"]["hints"], 1):
                hints += f"<details>\n<summary> hint {i}</summary>\n\n"
                hints += html2text.html2text(h)
                hints += "\n</details>\n"
            f.write(hints)
        f.write("\n\n## Solution:  \n")
        f.write("\n\n### Explanation:  \n")
        f.write("\n\n### Code:  \n")
        f.write("```python\n\n```\n")


if __name__ == "__main__":
    main(parse_arguments(sys.argv[1:]))
