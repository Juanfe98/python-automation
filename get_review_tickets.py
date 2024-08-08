import requests
import logging
from datetime import datetime
from configparser import ConfigParser

# The last item in the array should be the last review information
review_data = [
    {"reviewDate": "2024-03-05", "personInCharge": "Juan"},
    {"reviewDate": "2024-05-07", "personInCharge": "Leyaim"},
]

# Setup logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

config = ConfigParser()
config.read("config.ini")

JIRA_URL = config.get("DEFAULT", "JiraUrl")
PAT = config.get("DEFAULT", "PersonalAccessToken")
HEADERS = {
    "Authorization": f"Bearer {PAT}",
    "Accept": "application/json",
    "Content-Type": "application/json",
}


def get_last_review_date():
    if review_data:
        last_review = review_data[-1]
        return last_review["reviewDate"]
    else:
        return "2024-01-01"


def get_last_review_presenter():
    if review_data:
        last_review = review_data[-1]
        return last_review["personInCharge"] + " on " + last_review["reviewDate"]
    else:
        return "No info"


def get_epic_titles(epic_keys):
    """
    Fetches the titles for given epic keys.

    :param epic_keys: A list of epic keys.
    :return: A dictionary mapping epic keys to their titles.
    """
    titles = {}
    for key in epic_keys:
        response = requests.get(f"{JIRA_URL}/rest/api/2/issue/{key}", headers=HEADERS)
        if response.status_code == 200:
            data = response.json()
            titles[key] = data["fields"]["summary"]
        else:
            logging.error(
                f"Failed to fetch epic title for {key}. Status code: {response.status_code}"
            )
    return titles


def get_issues_grouped_by_epic(
    start_date, end_date, project_key, epic_link_field_id, max_results=50
):
    """
    Fetches issues grouped by their epics within a specified date range.

    :param start_date: Start of the date range in 'YYYY-MM-DD' format.
    :param end_date: End of the date range in 'YYYY-MM-DD' format.
    :param project_key: Project key to fetch issues from.
    :param epic_link_field_id: The custom field ID for the epic link.
    :param max_results: Maximum number of issues to return (for each epic).
    :return: A dictionary of epics, each with a list of its issues.
    """
    # Fetch all issues first
    jql_query = (
        f"project = {project_key} AND issuetype in standardIssueTypes() "
        f"AND status changed TO Closed DURING ('{start_date}', '{end_date}') ORDER BY updated ASC"
    )
    api_url = f"{JIRA_URL}/rest/api/2/search?jql={jql_query}&maxResults={max_results}&fields={epic_link_field_id},summary,assignee"
    response = requests.get(api_url, headers=HEADERS)

    if response.status_code != 200:
        logging.error(
            f"Failed to fetch issues. Status code: {response.status_code}, Response: {response.text}"
        )
        return {}

    issues = response.json().get("issues", [])
    # Group issues by their epic link
    epic_keys = set(
        issue["fields"].get(epic_link_field_id)
        for issue in issues
        if issue["fields"].get(epic_link_field_id)
    )
    epic_titles = get_epic_titles(epic_keys)

    grouped_issues = {epic_titles[key]: [] for key in epic_keys if key in epic_titles}
    for issue in issues:
        epic_key = issue["fields"].get(epic_link_field_id)
        assignee_name = (
            issue["fields"]["assignee"]["displayName"]
            if issue["fields"].get("assignee")
            else "Unassigned"
        )
        if epic_key and epic_key in epic_titles:
            grouped_issues[epic_titles[epic_key]].append(
                f"{issue['key']}: {issue['fields']['summary']} -- Assignee: {assignee_name}"
            )

    return grouped_issues


def main():
    project_key = "TRIF"
    start_date = get_last_review_date()
    end_date = datetime.now().strftime("%Y-%m-%d")
    epic_link_field_id = "customfield_14003"
    max_results = 50

    issues_grouped_by_epic = get_issues_grouped_by_epic(
        start_date, end_date, project_key, epic_link_field_id, max_results
    )
    print(f"Last Review in charge of: {get_last_review_presenter()}")
    print(f"----" * 20)
    for epic_title, issues in issues_grouped_by_epic.items():
        print(f"Epic: {epic_title}")
        for issue in issues:
            print(f"  - {issue}")
        print()


if __name__ == "__main__":
    main()
