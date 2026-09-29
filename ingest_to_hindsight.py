from github_client import get_issues
from hindsight_connection import client

issues = get_issues()

print(f"Found {len(issues)} GitHub issues.")

for issue in issues[:10]:
    content = f"""
Hyperswitch GitHub Issue #{issue['number']}
Title: {issue['title']}
Description: {issue.get('body') or 'No description'}
URL: {issue['html_url']}
Created: {issue['created_at']}
Updated: {issue['updated_at']}
"""

    client.retain(
        bank_id="product-hindsight",
        content=content
    )

    print(f"Saved issue #{issue['number']}")