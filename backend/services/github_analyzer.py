import requests


GITHUB_API_URL = "https://api.github.com"


def get_github_repositories(username: str):
    """
    Fetch public GitHub repositories for a user.
    """

    url = f"{GITHUB_API_URL}/users/{username}/repos"

    params = {
        "per_page": 100,
        "sort": "updated"
    }

    response = requests.get(
        url,
        params=params,
        timeout=10
    )

    if response.status_code == 404:
        raise ValueError("GitHub user not found")

    response.raise_for_status()

    repositories = response.json()

    return repositories


def analyze_github_profile(username: str):
    """
    Analyze a GitHub profile and return
    useful project information.
    """

    repositories = get_github_repositories(
        username
    )

    projects = []

    languages = {}

    for repo in repositories:

        if repo.get("fork"):
            continue

        repo_languages = repo.get(
            "language"
        )

        if repo_languages:

            languages[repo_languages] = (
                languages.get(
                    repo_languages,
                    0
                ) + 1
            )

        projects.append({
            "name": repo.get("name"),
            "description": repo.get("description"),
            "language": repo.get("language"),
            "url": repo.get("html_url"),
            "stars": repo.get("stargazers_count", 0),
            "forks": repo.get("forks_count", 0),
            "updated_at": repo.get("updated_at")
        })

    return {
        "username": username,
        "total_repositories": len(projects),
        "projects": projects,
        "languages": languages
    }