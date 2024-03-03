import requests
import json
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


def create_subtask(project_key, parent_issue_key, summary, description, issue_type_id):
    data = {
        "fields": {
            "project": {"key": project_key},
            "parent": {"key": parent_issue_key},
            "summary": summary,
            # "description": description,
            "issuetype": {"id": issue_type_id},
        }
    }

    response = requests.post(
        f"{JIRA_URL}/rest/api/2/issue/", headers=HEADERS, data=json.dumps(data)
    )

    if response.status_code == 201:
        logging.info("Subtask created successfully.")
        return response.json()
    else:
        logging.error(
            f"Failed to create subtask. Status code: {response.status_code}, Response: {response.text}"
        )
        return None


def create_standard_subtasks(parent_issue_key):
    standard_subtasks = [
        {
            "summary": "Initial analysis for the ticket requirements",
            "issue_type_id": "5",
        },
        {
            "summary": "Coding | Development process",
            "issue_type_id": "5",
        },
        {
            "summary": "Fixing | Creating unit tests",
            "issue_type_id": "5",
        },
        {
            "summary": "Code Review | PR for the ticket",
            "issue_type_id": "5",
        },
        {
            "summary": "QA - Steps to test the ticket.",
            "issue_type_id": "5",
        },
        {
            "summary": "Show to Greg for approval",
            "issue_type_id": "5",
        },
        {
            "summary": "Merge the PR - Deployment to Production",
            "issue_type_id": "5",
        },
    ]

    for subtask in standard_subtasks:
        create_subtask(
            "TRIF",
            parent_issue_key,
            subtask["summary"],
            "",  # description
            subtask["issue_type_id"],
        )


def main():
    if len(sys.argv) > 1 and sys.argv[1].lower() == "standard":
        if len(sys.argv) >= 3:
            parent_issue_key = sys.argv[2]
            result = create_standard_subtasks(parent_issue_key)

            if result:
                logging.info(f"Standard subtask created with Key: {result['key']}")
        else:
            logging.error("No parent issue key provided.")
            sys.exit(1)
    else:
        if len(sys.argv) < 6:
            logging.error(
                "For custom subtask, usage: script.py <project_key> <parent_issue_key> <summary> <description> <issue_type_id>"
            )
            logging.info(
                "Or, use 'standard' to create a standard subtask with predefined parameters."
            )
            sys.exit(1)

        project_key, parent_issue_key, summary, description, issue_type_id = sys.argv[
            1:6
        ]
        result = create_subtask(
            project_key, parent_issue_key, summary, description, issue_type_id
        )
        if result:
            logging.info(f"Custom subtask created with Key: {result['key']}")


if __name__ == "__main__":
    main()
