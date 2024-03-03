import requests
import logging
import sys
from configparser import ConfigParser

# Setup logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# Read configurations
config = ConfigParser()
config.read("config.ini")

JIRA_URL = config.get("DEFAULT", "JiraUrl")
PAT = config.get("DEFAULT", "PersonalAccessToken")
HEADERS = {
    "Authorization": f"Bearer {PAT}",
    "Accept": "application/json",
    "Content-Type": "application/json",
}


def get_ticket_comments(issue_key):
    response = requests.get(
        f"{JIRA_URL}/rest/api/2/issue/{issue_key}/comment", headers=HEADERS
    )

    if response.status_code == 200:
        logging.info("Comments fetched successfully.")
        logging.info(response.json())
        return response.json()
    else:
        logging.error(
            f"Failed to fetch comments. Status code: {response.status_code}, Response: {response.text}"
        )
        return None


def get_issue_details(issue_key):
    """Fetch issue details, including comments and attachments."""
    response = requests.get(
        f"{JIRA_URL}/rest/api/2/issue/{issue_key}?fields=comment,attachment",
        headers=HEADERS,
    )

    if response.status_code == 200:
        logging.info("Issue details fetched successfully.")
        return response.json()
    else:
        logging.error(
            f"Failed to fetch issue details. Status code: {response.status_code}, Response: {response.text}"
        )
        return None


def display_attachments(attachments_json):
    if attachments_json:
        print("Attachments:")
        for attachment in attachments_json:
            filename = attachment["filename"]
            url = attachment["content"]
            print(f"Filename: {filename}\nURL: {url}\n" + "-" * 80)


def print_colored(text, color_code):
    print(f"\033[{color_code}m{text}\033[0m")


def display_comments_colored(comments_json):
    if comments_json and "comments" in comments_json and comments_json["comments"]:
        print_colored("\nComments:\n" + "=" * 80, 34)  # Blue
        for comment in comments_json["comments"]:
            author = comment["author"]["displayName"]
            created = comment["created"][:10]
            body = comment["body"].replace("\r", "").replace("\n", "\n\t")
            print_colored(f"Author: {author}", 32)  # Green
            print_colored(f"Date: {created}", 36)  # Cyan
            print_colored(f"Comment:\n\t{body}\n" + "-" * 80, 0)  # Default
    else:
        print_colored("No comments found.", 31)  # Red


def display_comments(comments_json):
    if comments_json and "comments" in comments_json and comments_json["comments"]:
        print("\nComments:\n" + "=" * 80)
        for comment in comments_json["comments"]:
            author = comment["author"]["displayName"]
            created = comment["created"][:10]  # Simplify the date to YYYY-MM-DD
            body = comment["body"].replace("\r", "").replace("\n", "\n\t")
            print(f"Author: {author}\nDate: {created}\nComment:\n\t{body}\n" + "-" * 80)
    else:
        print("No comments found.")


def main():
    if len(sys.argv) < 2:
        logging.error("Usage: script.py <issue_key>")
        sys.exit(1)

    issue_key = sys.argv[1]
    issue_details = get_issue_details(issue_key)
    if issue_details:
        comments_json = issue_details.get("fields", {}).get("comment", {})
        attachments_json = issue_details.get("fields", {}).get("attachment", {})
        display_comments_colored(comments_json)
        display_attachments(attachments_json)


if __name__ == "__main__":
    main()
