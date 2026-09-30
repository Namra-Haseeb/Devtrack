import os
import requests
import streamlit as st
from dotenv import load_dotenv


# =========================================================
# CONFIGURATION
# =========================================================

load_dotenv()

BASE_URL = "https://api.github.com"

TOKEN = os.getenv("GITHUB_TOKEN", "").strip()

REQUEST_TIMEOUT = 12


def get_headers():
    """
    Build GitHub API headers.

    A token is optional. Public GitHub data can still be
    accessed without one, although rate limits are lower.
    """

    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "DevTrack"
    }

    if TOKEN:
        headers["Authorization"] = f"Bearer {TOKEN}"

    return headers


# =========================================================
# API REQUEST HELPER
# =========================================================

def github_request(endpoint, params=None):
    """
    Centralized GitHub API request handler.

    Returns:
        dict/list -> successful API response
        None      -> failed request
    """

    url = f"{BASE_URL}{endpoint}"

    try:

        response = requests.get(
            url,
            headers=get_headers(),
            params=params,
            timeout=REQUEST_TIMEOUT
        )

    except requests.exceptions.Timeout:
        return None

    except requests.exceptions.ConnectionError:
        return None

    except requests.exceptions.RequestException:
        return None

    # -----------------------------------------------------
    # Success
    # -----------------------------------------------------

    if response.status_code == 200:
        try:
            return response.json()
        except ValueError:
            return None

    # -----------------------------------------------------
    # Not Found
    # -----------------------------------------------------

    if response.status_code == 404:
        return None

    # -----------------------------------------------------
    # Rate Limited
    # -----------------------------------------------------

    if response.status_code == 403:

        remaining = response.headers.get(
            "X-RateLimit-Remaining"
        )

        if remaining == "0":
            return None

    # -----------------------------------------------------
    # Other API errors
    # -----------------------------------------------------

    return None


# =========================================================
# USER PROFILE
# =========================================================

@st.cache_data(ttl=600, show_spinner=False)
def get_user_profile(username):

    if not username:
        return None

    username = username.strip()

    if not username:
        return None

    return github_request(
        f"/users/{username}"
    )


# =========================================================
# USER REPOSITORIES
# =========================================================

@st.cache_data(ttl=600, show_spinner=False)
def get_user_repos(username):

    if not username:
        return []

    username = username.strip()

    if not username:
        return []

    repos = []

    page = 1

    while True:

        data = github_request(
            f"/users/{username}/repos",
            params={
                "per_page": 100,
                "page": page,
                "sort": "updated",
                "direction": "desc"
            }
        )

        if not isinstance(data, list):
            break

        if not data:
            break

        repos.extend(data)

        # GitHub normally returns less than 100 when
        # there are no more pages.

        if len(data) < 100:
            break

        page += 1

        # Safety limit so a malformed API response
        # cannot cause an endless loop.

        if page > 20:
            break

    return repos


# =========================================================
# USER EVENTS
# =========================================================

@st.cache_data(ttl=300, show_spinner=False)
def get_user_events(username):

    if not username:
        return []

    username = username.strip()

    if not username:
        return []

    data = github_request(
        f"/users/{username}/events/public",
        params={
            "per_page": 100
        }
    )

    if not isinstance(data, list):
        return []

    return data


# =========================================================
# REPOSITORY DETAILS
# =========================================================

@st.cache_data(ttl=600, show_spinner=False)
def get_repository(owner, repo):

    if not owner or not repo:
        return None

    owner = owner.strip()
    repo = repo.strip()

    if not owner or not repo:
        return None

    return github_request(
        f"/repos/{owner}/{repo}"
    )


# =========================================================
# REPOSITORY LANGUAGES
# =========================================================

@st.cache_data(ttl=600, show_spinner=False)
def get_repository_languages(owner, repo):

    if not owner or not repo:
        return {}

    data = github_request(
        f"/repos/{owner}/{repo}/languages"
    )

    if not isinstance(data, dict):
        return {}

    return data


# =========================================================
# REPOSITORY CONTRIBUTORS
# =========================================================

@st.cache_data(ttl=600, show_spinner=False)
def get_repository_contributors(owner, repo):

    if not owner or not repo:
        return []

    data = github_request(
        f"/repos/{owner}/{repo}/contributors",
        params={
            "per_page": 10
        }
    )

    if not isinstance(data, list):
        return []

    return data


# =========================================================
# GITHUB README
# =========================================================

@st.cache_data(ttl=600, show_spinner=False)
def get_repository_readme(owner, repo):

    if not owner or not repo:
        return None

    data = github_request(
        f"/repos/{owner}/{repo}/readme"
    )

    return data


# =========================================================
# GITHUB COMMITS
# =========================================================

@st.cache_data(ttl=300, show_spinner=False)
def get_repository_commits(owner, repo, per_page=20):

    if not owner or not repo:
        return []

    data = github_request(
        f"/repos/{owner}/{repo}/commits",
        params={
            "per_page": min(int(per_page), 100)
        }
    )

    if not isinstance(data, list):
        return []

    return data


# =========================================================
# USER FOLLOWERS
# =========================================================

@st.cache_data(ttl=600, show_spinner=False)
def get_user_followers(username):

    if not username:
        return []

    data = github_request(
        f"/users/{username}/followers",
        params={
            "per_page": 100
        }
    )

    if not isinstance(data, list):
        return []

    return data


# =========================================================
# USER FOLLOWING
# =========================================================

@st.cache_data(ttl=600, show_spinner=False)
def get_user_following(username):

    if not username:
        return []

    data = github_request(
        f"/users/{username}/following",
        params={
            "per_page": 100
        }
    )

    if not isinstance(data, list):
        return []

    return data


# =========================================================
# SEARCH USER
# =========================================================

@st.cache_data(ttl=600, show_spinner=False)
def search_github_user(username):

    if not username:
        return None

    data = github_request(
        "/search/users",
        params={
            "q": username,
            "per_page": 5
        }
    )

    if not isinstance(data, dict):
        return None

    items = data.get("items", [])

    if not items:
        return None

    # Prefer an exact username match.

    username_lower = username.strip().lower()

    for user in items:

        login = str(
            user.get("login", "")
        ).lower()

        if login == username_lower:
            return user

    return items[0]


# =========================================================
# API STATUS
# =========================================================

def get_api_status():

    data = github_request("/rate_limit")

    if not isinstance(data, dict):
        return {
            "available": False,
            "authenticated": bool(TOKEN),
            "remaining": None,
            "limit": None
        }

    core = data.get("resources", {}).get(
        "core",
        {}
    )

    return {
        "available": True,
        "authenticated": bool(TOKEN),
        "remaining": core.get("remaining"),
        "limit": core.get("limit")
    }


# =========================================================
# CACHE CONTROL
# =========================================================

def clear_github_cache():

    try:
        get_user_profile.clear()
        get_user_repos.clear()
        get_user_events.clear()
        get_repository.clear()
        get_repository_languages.clear()
        get_repository_contributors.clear()
        get_repository_readme.clear()
        get_repository_commits.clear()
        get_user_followers.clear()
        get_user_following.clear()
        search_github_user.clear()
    except Exception:
        pass