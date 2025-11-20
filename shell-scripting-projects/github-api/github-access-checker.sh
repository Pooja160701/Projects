#!/bin/bash

############################################################
# GitHub Repository Access Checker (Upgraded Version)
# Features:
#  - Lists users with Read / Write / Admin access
#  - Lists external collaborators
#  - Shows pending invitations
#  - Shows repo visibility + metadata
#  - Great error handling
#  - Colorful output
############################################################

API_URL="https://api.github.com"

# Colors
RED="\033[31m"
GREEN="\033[32m"
YELLOW="\033[33m"
CYAN="\033[36m"
RESET="\033[0m"

############################################################
# Validate environment variables
############################################################

if [[ -z "$GITHUB_USERNAME" ]]; then
    echo -e "${RED}ERROR:${RESET} GITHUB_USERNAME is not set."
    echo "Run: export GITHUB_USERNAME=\"your-username\""
    exit 1
fi

if [[ -z "$GITHUB_TOKEN" ]]; then
    echo -e "${RED}ERROR:${RESET} GITHUB_TOKEN is not set."
    echo "Run: export GITHUB_TOKEN=\"your-token\""
    exit 1
fi

############################################################
# Validate arguments
############################################################

if [[ $# -ne 2 ]]; then
    echo -e "${YELLOW}Usage:${RESET} $0 <repo-owner> <repo-name>"
    exit 1
fi

REPO_OWNER=$1
REPO_NAME=$2

############################################################
# GitHub API GET helper
############################################################

github_api_get() {
    curl -s -u "$GITHUB_USERNAME:$GITHUB_TOKEN" "$API_URL/$1"
}

############################################################
# Check if repo exists
############################################################

repo_check=$(github_api_get "repos/$REPO_OWNER/$REPO_NAME" | jq -r '.message')

if [[ "$repo_check" == "Not Found" ]]; then
    echo -e "${RED}ERROR:${RESET} Repository ${REPO_OWNER}/${REPO_NAME} does not exist or token lacks permission."
    exit 1
fi

############################################################
# Fetch repository metadata
############################################################

echo -e "${CYAN} REPOSITORY METADATA${RESET}"

metadata=$(github_api_get "repos/$REPO_OWNER/$REPO_NAME")

name=$(echo "$metadata" | jq -r '.name')
visibility=$(echo "$metadata" | jq -r '.visibility')
stars=$(echo "$metadata" | jq -r '.stargazers_count')
forks=$(echo "$metadata" | jq -r '.forks_count')
watchers=$(echo "$metadata" | jq -r '.watchers_count')

echo -e "Repository: ${GREEN}$name${RESET}"
echo -e "Visibility: ${YELLOW}$visibility${RESET}"
echo -e "Stars: ${GREEN}$stars${RESET}, Forks: ${GREEN}$forks${RESET}, Watchers: ${GREEN}$watchers${RESET}"
echo ""

############################################################
# List collaborators by permission
############################################################

echo -e "${CYAN} COLLABORATORS BY ACCESS LEVEL${RESET}"

collaborators=$(github_api_get "repos/$REPO_OWNER/$REPO_NAME/collaborators")

if echo "$collaborators" | jq -e "type==\"array\"" >/dev/null; then
    read_users=$(echo "$collaborators" | jq -r '.[] | select(.permissions.pull == true and .permissions.push == false) | .login')
    write_users=$(echo "$collaborators" | jq -r '.[] | select(.permissions.push == true and .permissions.admin == false) | .login')
    admin_users=$(echo "$collaborators" | jq -r '.[] | select(.permissions.admin == true) | .login')

    echo -e "${GREEN} Read Access:${RESET}"
    echo "${read_users:-None}"
    echo ""

    echo -e "${GREEN} Write Access:${RESET}"
    echo "${write_users:-None}"
    echo ""

    echo -e "${GREEN} Admin Access:${RESET}"
    echo "${admin_users:-None}"
    echo ""
else
    echo -e "${YELLOW}No collaborators found.${RESET}"
fi

############################################################
# External collaborators
############################################################

echo -e "${CYAN} EXTERNAL COLLABORATORS${RESET}"

external=$(github_api_get "repos/$REPO_OWNER/$REPO_NAME/collaborators?affiliation=outside")

if echo "$external" | jq -e 'type=="array"' >/dev/null; then
    ext_users=$(echo "$external" | jq -r '.[].login')
    echo "${ext_users:-None}"
else
    echo "None"
fi

echo ""

############################################################
# Pending Invitations
############################################################

echo -e "${CYAN} PENDING INVITATIONS${RESET}"

invitations=$(github_api_get "repos/$REPO_OWNER/$REPO_NAME/invitations")

if echo "$invitations" | jq -e 'type=="array"' >/dev/null; then
    invited=$(echo "$invitations" | jq -r '.[].invitee.login')
    echo "${invited:-None}"
else
    echo "None"
fi

echo ""
echo -e "${GREEN} COMPLETED${RESET}"