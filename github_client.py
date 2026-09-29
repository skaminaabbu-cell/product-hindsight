import requests


# ==========================================
# HYPERSWITCH GITHUB REPOSITORY
# ==========================================

OWNER = "juspay"
REPO = "hyperswitch"

BASE_URL = f"https://api.github.com/repos/{OWNER}/{REPO}"


# ==========================================
# GET GITHUB ISSUES
# ==========================================

def get_issues():
    """
    Fetch issues from the Hyperswitch GitHub repository.
    Pull requests are removed because we only want actual issues.
    """

    url = f"{BASE_URL}/issues"

    params = {
        "state": "all",
        "per_page": 50
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        print("GitHub API error:", response.status_code)
        return []

    data = response.json()

    issues = []

    for item in data:

        # GitHub returns pull requests inside the issues endpoint.
        # We don't want pull requests here.
        if "pull_request" not in item:

            issues.append(item)

    return issues


# ==========================================
# CLEAN GITHUB ISSUE
# ==========================================

def clean_issue(issue):
    """
    Convert a GitHub issue into a simple format
    that ProductHindsight can use.
    """

    return {
        "id": issue["number"],
        "title": issue["title"],
        "body": issue.get("body") or "",
        "url": issue["html_url"],
        "created_at": issue["created_at"],
        "updated_at": issue["updated_at"],
        "labels": [
            label["name"]
            for label in issue.get("labels", [])
        ]
    }


# ==========================================
# GET GITHUB RELEASES
# ==========================================

def get_releases():
    """
    Fetch recent releases from the Hyperswitch
    GitHub repository.
    """

    url = f"{BASE_URL}/releases"

    params = {
        "per_page": 20
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        print(
            "GitHub Releases API error:",
            response.status_code
        )
        return []

    releases = response.json()

    cleaned_releases = []

    for release in releases:

        cleaned_releases.append({
            "name": release.get("name")
                    or release.get("tag_name"),

            "tag": release.get("tag_name"),

            "body": release.get("body") or "",

            "published_at": release.get("published_at"),

            "url": release.get("html_url")
        })

    return cleaned_releases


# ==========================================
# TEST THE GITHUB CONNECTION
# ==========================================

if __name__ == "__main__":

    print("\n================================")
    print("PRODUCTHINDSIGHT GITHUB TEST")
    print("================================\n")

    # Test issues
    issues = get_issues()

    print("Number of issues:", len(issues))

    if issues:

        print("\nFirst 5 issues:\n")

        for issue in issues[:5]:

            print("Issue:", issue["number"])
            print("Title:", issue["title"])
            print("URL:", issue["html_url"])
            print("-" * 50)

    # Test releases
    releases = get_releases()

    print("\nNumber of releases:", len(releases))

    if releases:

        print("\nRecent releases:\n")

        for release in releases[:5]:

            print("Release:", release["name"])
            print("Tag:", release["tag"])
            print("Published:", release["published_at"])
            print("URL:", release["url"])
            print("-" * 50)