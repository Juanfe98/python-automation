# JIRA Script Utilities

This repository is a collection of Python scripts designed to automate and facilitate various interactions with the JIRA REST API. The utilities cover a range of functionalities, including but not limited to creating subtasks, fetching issue comments, and more, aiming to improve the efficiency of managing JIRA tickets.

## Overview

The scripts in this repository interact with JIRA's REST API to perform a variety of tasks that help in managing projects, issues, and subtasks within JIRA. They are intended to be standalone utilities that can be used as needed, depending on the task at hand.

## Configuration

To use the scripts, a `config.ini` file is required for storing essential configuration details like the JIRA URL and personal access tokens. Create a `config.ini` file in the root of the repository with the following content (replace placeholder values with your actual data):

```ini
[DEFAULT]
JiraUrl = YOUR_JIRA_URL_HERE
PersonalAccessToken = YOUR_PERSONAL_ACCESS_TOKEN_HERE
```

## Requirements
- Python 3.x
- requests library
- Install the necessary dependency with pip: `pip install requests`

## Usage
Each script in the repository can be executed from the command line, typically requiring one or more arguments to specify the action and targets within JIRA. For detailed usage instructions, refer to the comment header at the beginning of each script.

Example:

`python script_name.py [arguments]`

Replace script_name.py with the actual script file you wish to run and [arguments] with the appropriate command-line arguments for that script.

## Contributing

We welcome contributions to this repository. If you have improvements or new scripts that you'd like to share, please:

1. Fork the repository.

2. Create a new branch for your feature or fix.

3. Commit your changes.

4. Push your branch and submit a pull request.
