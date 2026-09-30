import re
from collections import Counter
from datetime import datetime, timezone


# =========================================================
# HELPERS
# =========================================================

def safe_int(value, default=0):
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def parse_github_date(value):
    """
    Convert GitHub ISO date into a timezone-aware datetime.
    """

    if not value:
        return None

    try:
        value = value.replace("Z", "+00:00")
        return datetime.fromisoformat(value)
    except (TypeError, ValueError):
        return None


def days_since(date_value):
    """
    Return number of days since a GitHub date.
    """

    parsed = parse_github_date(date_value)

    if not parsed:
        return 0

    now = datetime.now(timezone.utc)

    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)

    difference = now - parsed

    return max(0, difference.days)


def clean_text(value, fallback="No description available."):
    """
    Clean empty GitHub text fields.
    """

    if value is None:
        return fallback

    value = str(value).strip()

    if not value:
        return fallback

    return value


# =========================================================
# LANGUAGE ANALYSIS
# =========================================================

def analyze_languages(repos):
    """
    Calculate language usage across repositories.
    """

    language_counter = Counter()

    for repo in repos or []:

        language = repo.get("language")

        if language:
            language_counter[str(language)] += 1

    return dict(
        language_counter.most_common(15)
    )


# =========================================================
# TOPICS
# =========================================================

def extract_topics(repos):
    """
    Collect GitHub repository topics.
    """

    topics = Counter()

    for repo in repos or []:

        repo_topics = repo.get("topics", [])

        if not isinstance(repo_topics, list):
            continue

        for topic in repo_topics:

            if topic:
                topics[str(topic)] += 1

    return dict(
        topics.most_common(20)
    )


# =========================================================
# REPOSITORY ANALYSIS
# =========================================================

def analyze_repositories(repos):
    """
    Generate useful repository-level statistics.
    """

    repos = repos or []

    if not repos:
        return {
            "total": 0,
            "stars": 0,
            "forks": 0,
            "original_repos": 0,
            "forked_repos": 0,
            "documented_repos": 0,
            "licensed_repos": 0,
            "topic_repos": 0,
            "recent_repos": 0,
            "languages": {},
            "topics": {},
            "top_repositories": []
        }

    total_stars = 0
    total_forks = 0
    original_repos = 0
    forked_repos = 0
    documented_repos = 0
    licensed_repos = 0
    topic_repos = 0
    recent_repos = 0

    for repo in repos:

        total_stars += safe_int(
            repo.get("stargazers_count")
        )

        total_forks += safe_int(
            repo.get("forks_count")
        )

        if repo.get("fork"):
            forked_repos += 1
        else:
            original_repos += 1

        if repo.get("description"):
            documented_repos += 1

        if repo.get("license"):
            licensed_repos += 1

        if repo.get("topics"):
            topic_repos += 1

        updated_at = repo.get("updated_at")

        if updated_at and days_since(updated_at) <= 180:
            recent_repos += 1

    sorted_repos = sorted(
        repos,
        key=lambda repo: (
            safe_int(repo.get("stargazers_count")),
            safe_int(repo.get("forks_count"))
        ),
        reverse=True
    )

    top_repositories = []

    for repo in sorted_repos[:10]:

        top_repositories.append({
            "name": repo.get("name", "Unknown"),
            "full_name": repo.get("full_name", ""),
            "description": clean_text(
                repo.get("description")
            ),
            "language": repo.get("language") or "Not specified",
            "stars": safe_int(
                repo.get("stargazers_count")
            ),
            "forks": safe_int(
                repo.get("forks_count")
            ),
            "topics": repo.get("topics", []),
            "url": repo.get(
                "html_url",
                ""
            ),
            "updated_at": repo.get(
                "updated_at"
            ),
            "created_at": repo.get(
                "created_at"
            ),
            "license": (
                repo.get("license", {}) or {}
            ).get("spdx_id"),
            "fork": bool(
                repo.get("fork")
            )
        })

    return {
        "total": len(repos),
        "stars": total_stars,
        "forks": total_forks,
        "original_repos": original_repos,
        "forked_repos": forked_repos,
        "documented_repos": documented_repos,
        "licensed_repos": licensed_repos,
        "topic_repos": topic_repos,
        "recent_repos": recent_repos,
        "languages": analyze_languages(repos),
        "topics": extract_topics(repos),
        "top_repositories": top_repositories
    }


# =========================================================
# ACTIVITY ANALYSIS
# =========================================================

def analyze_activity(events):
    """
    Analyze recent public GitHub activity.
    """

    events = events or []

    event_counter = Counter()

    push_events = 0
    pull_requests = 0
    issues = 0
    stars = 0
    forks = 0
    commits = 0

    recent_dates = []

    for event in events:

        event_type = event.get(
            "type",
            "UnknownEvent"
        )

        event_counter[event_type] += 1

        created_at = event.get("created_at")

        if created_at:
            recent_dates.append(created_at)

        if event_type == "PushEvent":

            push_events += 1

            payload = event.get(
                "payload",
                {}
            )

            commits += len(
                payload.get("commits", []) or []
            )

        elif event_type == "PullRequestEvent":
            pull_requests += 1

        elif event_type == "IssuesEvent":
            issues += 1

        elif event_type == "WatchEvent":
            stars += 1

        elif event_type == "ForkEvent":
            forks += 1

    readable_events = []

    for event_type, count in event_counter.most_common(10):

        readable_name = (
            event_type
            .replace("Event", "")
            .replace("_", " ")
        )

        readable_events.append({
            "type": readable_name,
            "count": count
        })

    return {
        "total_events": len(events),
        "push_events": push_events,
        "pull_requests": pull_requests,
        "issues": issues,
        "stars_received": stars,
        "forks_received": forks,
        "commits": commits,
        "event_types": readable_events,
        "recent_dates": recent_dates[:20]
    }


# =========================================================
# REPOSITORY QUALITY
# =========================================================

def calculate_repository_quality(repo):
    """
    Lightweight quality indicator for a repository.

    This is an internal DevTrack metric, not an industry
    standard or hiring score.
    """

    if not repo:
        return 0

    score = 0

    # Description
    if repo.get("description"):
        score += 15

    # Stars
    stars = safe_int(
        repo.get("stargazers_count")
    )

    if stars >= 10:
        score += 20
    elif stars >= 5:
        score += 15
    elif stars >= 1:
        score += 8

    # Forks
    forks = safe_int(
        repo.get("forks_count")
    )

    if forks >= 5:
        score += 15
    elif forks >= 1:
        score += 8

    # Topics
    topics = repo.get("topics", [])

    if topics:
        score += 15

    # License
    if repo.get("license"):
        score += 15

    # Recent activity
    updated_at = repo.get("updated_at")

    if updated_at:

        age = days_since(updated_at)

        if age <= 30:
            score += 20
        elif age <= 90:
            score += 15
        elif age <= 180:
            score += 8

    return min(score, 100)


# =========================================================
# TOP REPOSITORIES
# =========================================================

def get_top_repositories(repos, limit=5):
    """
    Return repositories ordered using stars, forks,
    documentation and recent activity.
    """

    repos = repos or []

    def repository_score(repo):

        stars = safe_int(
            repo.get("stargazers_count")
        )

        forks = safe_int(
            repo.get("forks_count")
        )

        quality = calculate_repository_quality(
            repo
        )

        return (
            stars * 3
            + forks * 2
            + quality
        )

    sorted_repos = sorted(
        repos,
        key=repository_score,
        reverse=True
    )

    return sorted_repos[:limit]


# =========================================================
# PROFILE ANALYSIS
# =========================================================

def analyze_profile(
    profile,
    repos=None,
    events=None
):
    """
    Create the main DevTrack GitHub analysis object.

    This function keeps the output compatible with the
    previous version while adding richer statistics.
    """

    repos = repos or []
    events = events or []

    if not profile:
        return {}

    # -----------------------------------------------------
    # Basic profile information
    # -----------------------------------------------------

    username = profile.get(
        "login",
        ""
    )

    name = profile.get(
        "name"
    ) or username

    bio = profile.get(
        "bio"
    ) or ""

    location = profile.get(
        "location"
    ) or ""

    avatar_url = profile.get(
        "avatar_url"
    ) or ""

    profile_url = profile.get(
        "html_url"
    ) or ""

    joined_date = profile.get(
        "created_at"
    )

    # -----------------------------------------------------
    # Repository information
    # -----------------------------------------------------

    repo_analysis = analyze_repositories(
        repos
    )

    languages = repo_analysis[
        "languages"
    ]

    topics = repo_analysis[
        "topics"
    ]

    top_language = (
        next(iter(languages))
        if languages
        else None
    )

    # -----------------------------------------------------
    # Activity information
    # -----------------------------------------------------

    activity = analyze_activity(
        events
    )

    # -----------------------------------------------------
    # Account age
    # -----------------------------------------------------

    account_age_days = days_since(
        joined_date
    )

    years_active = round(
        account_age_days / 365.25,
        1
    )

    # -----------------------------------------------------
    # Recent repository activity
    # -----------------------------------------------------

    recent_repositories = []

    for repo in sorted(
        repos,
        key=lambda item: item.get(
            "updated_at",
            ""
        ),
        reverse=True
    )[:10]:

        recent_repositories.append({
            "name": repo.get(
                "name",
                "Unknown"
            ),
            "updated_at": repo.get(
                "updated_at"
            ),
            "language": repo.get(
                "language"
            ),
            "stars": safe_int(
                repo.get(
                    "stargazers_count"
                )
            ),
            "url": repo.get(
                "html_url",
                ""
            )
        })

    # -----------------------------------------------------
    # Top repositories
    # -----------------------------------------------------

    top_repos_raw = get_top_repositories(
        repos,
        limit=5
    )

    top_repos = []

    for repo in top_repos_raw:

        top_repos.append({
            "name": repo.get(
                "name",
                "Unknown"
            ),
            "stars": safe_int(
                repo.get(
                    "stargazers_count"
                )
            ),
            "forks": safe_int(
                repo.get(
                    "forks_count"
                )
            ),
            "language": repo.get(
                "language"
            ) or "Not specified",
            "description": clean_text(
                repo.get(
                    "description"
                )
            ),
            "url": repo.get(
                "html_url",
                ""
            ),
            "quality": calculate_repository_quality(
                repo
            )
        })

    # -----------------------------------------------------
    # Consistency indicator
    # -----------------------------------------------------

    recent_repo_count = repo_analysis[
        "recent_repos"
    ]

    consistency_percentage = 0

    if repos:

        consistency_percentage = round(
            min(
                (
                    recent_repo_count
                    / len(repos)
                ) * 100,
                100
            )
        )

    # -----------------------------------------------------
    # Documentation percentage
    # -----------------------------------------------------

    documentation_percentage = 0

    if repos:

        documentation_percentage = round(
            (
                repo_analysis[
                    "documented_repos"
                ]
                / len(repos)
            ) * 100
        )

    # -----------------------------------------------------
    # Original project percentage
    # -----------------------------------------------------

    original_percentage = 0

    if repos:

        original_percentage = round(
            (
                repo_analysis[
                    "original_repos"
                ]
                / len(repos)
            ) * 100
        )

    # -----------------------------------------------------
    # Final analysis object
    # -----------------------------------------------------

    return {

        # Basic identity
        "username": username,
        "name": name,
        "bio": bio,
        "location": location,
        "avatar_url": avatar_url,
        "profile_url": profile_url,

        # Account
        "joined": joined_date,
        "account_age_days": account_age_days,
        "years_active": years_active,

        # GitHub metrics
        "public_repos": safe_int(
            profile.get(
                "public_repos"
            )
        ),
        "followers": safe_int(
            profile.get(
                "followers"
            )
        ),
        "following": safe_int(
            profile.get(
                "following"
            )
        ),
        "public_gists": safe_int(
            profile.get(
                "public_gists"
            )
        ),

        # Repository metrics
        "total_repos": repo_analysis[
            "total"
        ],
        "total_stars": repo_analysis[
            "stars"
        ],
        "total_forks": repo_analysis[
            "forks"
        ],
        "original_repos": repo_analysis[
            "original_repos"
        ],
        "forked_repos": repo_analysis[
            "forked_repos"
        ],

        # Documentation
        "documented_repos": repo_analysis[
            "documented_repos"
        ],
        "licensed_repos": repo_analysis[
            "licensed_repos"
        ],
        "topic_repos": repo_analysis[
            "topic_repos"
        ],

        # Percentages
        "documentation_percentage": documentation_percentage,
        "original_percentage": original_percentage,
        "consistency_percentage": consistency_percentage,

        # Technologies
        "languages": languages,
        "top_language": top_language,
        "topics": topics,

        # Activity
        "days_active": account_age_days,
        "recent_activity": activity[
            "event_types"
        ],
        "total_recent_events": activity[
            "total_events"
        ],
        "push_events": activity[
            "push_events"
        ],
        "pull_requests": activity[
            "pull_requests"
        ],
        "issues": activity[
            "issues"
        ],
        "commits": activity[
            "commits"
        ],

        # Repository data
        "recent_repositories": recent_repositories,
        "top_repos": top_repos,

        # Full analysis
        "repository_analysis": repo_analysis,
        "activity_analysis": activity,

        # Original raw data
        "raw_profile": profile
    }


# =========================================================
# PROFILE SUMMARY
# =========================================================

def get_profile_summary(analyzed_data):
    """
    Generate short text suitable for dashboard cards.
    """

    if not analyzed_data:
        return {
            "headline": "No GitHub profile analyzed yet.",
            "description": "Connect a GitHub profile to start your DevTrack analysis."
        }

    username = analyzed_data.get(
        "username",
        "Developer"
    )

    repos = safe_int(
        analyzed_data.get(
            "total_repos"
        )
    )

    stars = safe_int(
        analyzed_data.get(
            "total_stars"
        )
    )

    languages = analyzed_data.get(
        "languages",
        {}
    )

    top_language = analyzed_data.get(
        "top_language"
    )

    if top_language:
        headline = (
            f"{username} is building with "
            f"{top_language}."
        )
    else:
        headline = (
            f"{username}'s GitHub profile "
            f"is connected."
        )

    description = (
        f"{repos} public repositories, "
        f"{stars} total stars and "
        f"{len(languages)} detected languages."
    )

    return {
        "headline": headline,
        "description": description
    }


# =========================================================
# SKILL SIGNALS
# =========================================================

def get_skill_signals(analyzed_data):
    """
    Convert GitHub language/activity information into
    simple signals that can be used by DevTrack's
    career features.
    """

    if not analyzed_data:
        return {}

    languages = analyzed_data.get(
        "languages",
        {}
    )

    signals = {}

    for language, count in languages.items():

        key = re.sub(
            r"[^a-zA-Z0-9]+",
            "_",
            language.lower()
        ).strip("_")

        signals[key] = count

    # Activity signals

    signals["repositories"] = safe_int(
        analyzed_data.get(
            "total_repos"
        )
    )

    signals["stars"] = safe_int(
        analyzed_data.get(
            "total_stars"
        )
    )

    signals["forks"] = safe_int(
        analyzed_data.get(
            "total_forks"
        )
    )

    signals["commits"] = safe_int(
        analyzed_data.get(
            "commits"
        )
    )

    signals["pull_requests"] = safe_int(
        analyzed_data.get(
            "pull_requests"
        )
    )

    signals["issues"] = safe_int(
        analyzed_data.get(
            "issues"
        )
    )

    return signals