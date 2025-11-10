#!/bin/bash

# Author: Pooja
# Date: 09/08/2025
# Version: v1
# Description:
# This script lists all users with READ (pull) access to a given GitHub repository
# using the GitHub REST API.

# Function to show usage help and exit if incorrect arguments are provided
function helper() {
    expected_cmd_args=2
    if [ $# -ne $expected_cmd_args ]; then
        echo "Usage: $0 <repo_owner> <repo_name>"
        echo "Example: $0 octocat Hello-World"
        exit 1
    fi
}

# Call helper to check arguments
helper "$@"

# GitHub API URL
API_URL="https://api.github.com"

# GitHub username and personal access token
USERNAME=$username
TOKEN=$token

# Check if USERNAME and TOKEN are set
if [[ -z "$USERNAME" || -z "$TOKEN" ]]; then
    echo "Error: Please export your GitHub username and token as environment variables:"
    echo "  export username=your_username"
    echo "  export token=your_token"
    exit 1
fi

# User and Repository information
REPO_OWNER=$1
REPO_NAME=$2

# Function to make a GET request to the GitHub API
function github_api_get {
    local endpoint="$1"
    local url="${API_URL}/${endpoint}"

    # Send a GET request to the GitHub API with authentication
    curl -s -u "${USERNAME}:${TOKEN}" "$url"
}

# Function to list users with read access to the repository
function list_users_with_read_access {
    local endpoint="repos/${REPO_OWNER}/${REPO_NAME}/collaborators"

    # Fetch the list of collaborators on the repository
    collaborators="$(github_api_get "$endpoint" | jq -r '.[] | select(.permissions.pull == true) | .login')"

    # Display the list of collaborators with read access
    if [[ -z "$collaborators" ]]; then
        echo "No users with read access found for ${REPO_OWNER}/${REPO_NAME}."
    else
        echo "Users with read access to ${REPO_OWNER}/${REPO_NAME}:"
        echo "$collaborators"
    fi
}

# Main script
echo "Listing users with read access to ${REPO_OWNER}/${REPO_NAME}..."
list_users_with_read_access