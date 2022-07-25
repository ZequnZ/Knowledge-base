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
        r.json()["data"]["question"]["questionFrontendId"]
        + ". "
        + r.json()["data"]["question"]["title"]
    )

    # difficulty
    difficulty = (
        "Difficulty: " + "`" + r.json()["data"]["question"]["difficulty"] + "`\n\n"
    )

    # Tags
    num_of_tag = len(r.json()["data"]["question"]["topicTags"])
    # No tag
    if not num_of_tag:
        tags = "<details>\n<summary> Tags</summary>\n\n" + "\n</details>\n\n"
    else: 
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

    # similar question
    sq_list = json.loads(r.json()["data"]["question"]["similarQuestions"])

    with open(title + ".md", "w", encoding="utf-8") as f:
        f.write("# " + title + "\n")
        f.write(f"[Link]({question_link})\n\n")
        f.write(difficulty)
        f.write(tags)
        # If similar question exists
        if len(sq_list) > 0:
            sq = ""
            for q in sq_list:
                sq += f"[{q['title']}](https://leetcode.com/problems/{q['titleSlug']}/)\t`{q['difficulty']}`\n\n"
            sq = (
                "<details>\n<summary> Similar Questions</summary>\n\n"
                + sq
                + "\n</details>\n\n"
            )
            f.write(sq)

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
        f.write("\n\n### Time complexity:  \n")
        f.write("`O()`  \n")
        f.write("\n\n### Space complexity:  \n")
        f.write("`O()`  \n")

        f.write("\n\n### Code:  \n")
        f.write("```python\n\n```\n")
        f.write("\n\n### Other great solutions:\n\n")
        f.close()

        # Insert the link in README.md:

        # Get the current content
        with open("./README.md", "r", encoding="utf-8") as f:
            lines = f.readlines()
            f.close()

        # Insert the link:
        lines.insert(2, f"[{title}](./{title.replace(' ', '%20')}.md)  \n")

        # Write it back
        with open("./README.md", "w", encoding="utf-8") as f:
            for line in lines:
                f.write(line)
            f.close()

    print(f"Successfully generate file {title}")


if __name__ == "__main__":
    main(parse_arguments(sys.argv[1:]))
