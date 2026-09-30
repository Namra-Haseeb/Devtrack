# =========================================================
# DEVTRACK SCORING ENGINE
# =========================================================
#
# These scores are internal progress indicators for DevTrack.
# They are NOT industry-standard hiring scores.
#
# =========================================================


# =========================================================
# HELPERS
# =========================================================

def safe_int(value, default=0):
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def clamp(value, minimum=0, maximum=100):
    return max(
        minimum,
        min(
            maximum,
            int(round(value))
        )
    )


# =========================================================
# LABELS
# =========================================================

def get_score_label(score):

    score = clamp(score)

    if score >= 85:
        return "Excellent"

    if score >= 70:
        return "Strong"

    if score >= 50:
        return "Developing"

    if score >= 30:
        return "Early Stage"

    return "Getting Started"


def get_repository_label(score):

    score = clamp(score)

    if score >= 85:
        return "Excellent"

    if score >= 70:
        return "Strong"

    if score >= 50:
        return "Developing"

    if score >= 30:
        return "Needs Work"

    return "Getting Started"


# =========================================================
# ACTIVITY SCORE
# =========================================================

def calculate_activity_score(
    profile,
    repos,
    events,
    analyzed_data
):
    """
    Calculate the activity component.

    Maximum: 25 points.
    """

    score = 0

    repo_count = len(
        repos or []
    )

    event_count = len(
        events or []
    )

    commits = safe_int(
        analyzed_data.get(
            "commits",
            0
        )
    )

    # Repositories
    if repo_count >= 20:
        score += 8
    elif repo_count >= 10:
        score += 6
    elif repo_count >= 5:
        score += 4
    elif repo_count >= 1:
        score += 2

    # Recent public activity
    if event_count >= 30:
        score += 7
    elif event_count >= 15:
        score += 5
    elif event_count >= 5:
        score += 3
    elif event_count >= 1:
        score += 1

    # Commit activity
    if commits >= 100:
        score += 10
    elif commits >= 50:
        score += 8
    elif commits >= 20:
        score += 5
    elif commits >= 5:
        score += 3
    elif commits >= 1:
        score += 1

    return min(score, 25)


# =========================================================
# TECHNOLOGY DIVERSITY
# =========================================================

def calculate_technology_score(
    analyzed_data
):
    """
    Maximum: 20 points.
    """

    languages = analyzed_data.get(
        "languages",
        {}
    )

    language_count = len(
        languages
    )

    if language_count >= 6:
        return 20

    if language_count >= 4:
        return 16

    if language_count >= 3:
        return 13

    if language_count >= 2:
        return 9

    if language_count >= 1:
        return 6

    return 0


# =========================================================
# COMMUNITY SCORE
# =========================================================

def calculate_community_score(
    profile,
    analyzed_data
):
    """
    Maximum: 20 points.
    """

    followers = safe_int(
        profile.get(
            "followers",
            0
        )
    )

    following = safe_int(
        profile.get(
            "following",
            0
        )
    )

    stars = safe_int(
        analyzed_data.get(
            "total_stars",
            0
        )
    )

    forks = safe_int(
        analyzed_data.get(
            "total_forks",
            0
        )
    )

    score = 0

    # Followers
    if followers >= 500:
        score += 7
    elif followers >= 100:
        score += 5
    elif followers >= 25:
        score += 3
    elif followers >= 5:
        score += 1

    # Stars
    if stars >= 100:
        score += 6
    elif stars >= 25:
        score += 4
    elif stars >= 10:
        score += 2
    elif stars >= 1:
        score += 1

    # Forks
    if forks >= 25:
        score += 4
    elif forks >= 10:
        score += 3
    elif forks >= 1:
        score += 1

    # Following shows some ecosystem exploration.
    if following >= 20:
        score += 3
    elif following >= 5:
        score += 2
    elif following >= 1:
        score += 1

    return min(score, 20)


# =========================================================
# PROJECT QUALITY SCORE
# =========================================================

def calculate_project_quality_score(
    repos,
    analyzed_data
):
    """
    Maximum: 20 points.

    Looks at:
    - descriptions
    - topics
    - licenses
    - original repositories
    - repository activity
    """

    repos = repos or []

    if not repos:
        return 0

    score = 0

    repo_analysis = analyzed_data.get(
        "repository_analysis",
        {}
    )

    documented = safe_int(
        repo_analysis.get(
            "documented_repos",
            0
        )
    )

    licensed = safe_int(
        repo_analysis.get(
            "licensed_repos",
            0
        )
    )

    topics = safe_int(
        repo_analysis.get(
            "topic_repos",
            0
        )
    )

    original = safe_int(
        repo_analysis.get(
            "original_repos",
            0
        )
    )

    total = len(repos)

    # Documentation quality
    documentation_ratio = (
        documented / total
    )

    if documentation_ratio >= 0.8:
        score += 6
    elif documentation_ratio >= 0.5:
        score += 4
    elif documentation_ratio >= 0.25:
        score += 2

    # Topics
    topic_ratio = (
        topics / total
    )

    if topic_ratio >= 0.6:
        score += 4
    elif topic_ratio >= 0.3:
        score += 3
    elif topic_ratio > 0:
        score += 1

    # Licenses
    license_ratio = (
        licensed / total
    )

    if license_ratio >= 0.6:
        score += 3
    elif license_ratio >= 0.3:
        score += 2
    elif license_ratio > 0:
        score += 1

    # Original projects
    original_ratio = (
        original / total
    )

    if original_ratio >= 0.8:
        score += 4
    elif original_ratio >= 0.5:
        score += 3
    elif original_ratio >= 0.25:
        score += 2

    # Recent repositories
    recent = safe_int(
        repo_analysis.get(
            "recent_repos",
            0
        )
    )

    if recent >= 5:
        score += 3
    elif recent >= 2:
        score += 2
    elif recent >= 1:
        score += 1

    return min(score, 20)


# =========================================================
# CONSISTENCY SCORE
# =========================================================

def calculate_consistency_score(
    repos,
    analyzed_data
):
    """
    Maximum: 15 points.

    Measures recent GitHub activity and repository updates.
    """

    repos = repos or []

    if not repos:
        return 0

    repo_analysis = analyzed_data.get(
        "repository_analysis",
        {}
    )

    recent_repos = safe_int(
        repo_analysis.get(
            "recent_repos",
            0
        )
    )

    total_repos = len(repos)

    if total_repos == 0:
        return 0

    ratio = (
        recent_repos / total_repos
    )

    if ratio >= 0.75:
        return 15

    if ratio >= 0.5:
        return 12

    if ratio >= 0.3:
        return 9

    if ratio >= 0.15:
        return 6

    if ratio > 0:
        return 3

    return 0


# =========================================================
# MAIN DEVELOPER SCORE
# =========================================================

def calculate_developer_score(
    profile,
    repos,
    events,
    analyzed_data
):
    """
    Calculate DevTrack's internal developer progress score.

    Maximum = 100.

    Breakdown:
        Activity        25
        Technology      20
        Community       20
        Project Quality 20
        Consistency     15
    """

    profile = profile or {}
    repos = repos or []
    events = events or []
    analyzed_data = analyzed_data or {}

    activity = calculate_activity_score(
        profile,
        repos,
        events,
        analyzed_data
    )

    technology = calculate_technology_score(
        analyzed_data
    )

    community = calculate_community_score(
        profile,
        analyzed_data
    )

    project_quality = calculate_project_quality_score(
        repos,
        analyzed_data
    )

    consistency = calculate_consistency_score(
        repos,
        analyzed_data
    )

    total = (
        activity
        + technology
        + community
        + project_quality
        + consistency
    )

    total = clamp(total)

    breakdown = {
        "Activity": {
            "score": activity,
            "max": 25
        },
        "Technology": {
            "score": technology,
            "max": 20
        },
        "Community": {
            "score": community,
            "max": 20
        },
        "Project Quality": {
            "score": project_quality,
            "max": 20
        },
        "Consistency": {
            "score": consistency,
            "max": 15
        }
    }

    return {
        "total": total,
        "score": total,
        "breakdown": breakdown,
        "label": get_score_label(total)
    }


# =========================================================
# REPOSITORY SCORE
# =========================================================

def score_repository(repo):
    """
    Calculate an internal DevTrack quality score
    for an individual repository.

    Maximum = 100.
    """

    if not repo:
        return {
            "total": 0,
            "score": 0,
            "label": "No Data",
            "breakdown": {}
        }

    score = 0

    breakdown = {}

    # -----------------------------------------------------
    # Description
    # -----------------------------------------------------

    if repo.get("description"):

        description_score = 15
        score += description_score

    else:

        description_score = 0

    breakdown["Description"] = {
        "score": description_score,
        "max": 15
    }

    # -----------------------------------------------------
    # Stars
    # -----------------------------------------------------

    stars = safe_int(
        repo.get(
            "stargazers_count",
            0
        )
    )

    if stars >= 50:
        stars_score = 20
    elif stars >= 20:
        stars_score = 16
    elif stars >= 10:
        stars_score = 12
    elif stars >= 5:
        stars_score = 8
    elif stars >= 1:
        stars_score = 4
    else:
        stars_score = 0

    score += stars_score

    breakdown["Stars"] = {
        "score": stars_score,
        "max": 20
    }

    # -----------------------------------------------------
    # Forks
    # -----------------------------------------------------

    forks = safe_int(
        repo.get(
            "forks_count",
            0
        )
    )

    if forks >= 20:
        forks_score = 15
    elif forks >= 10:
        forks_score = 12
    elif forks >= 5:
        forks_score = 9
    elif forks >= 1:
        forks_score = 5
    else:
        forks_score = 0

    score += forks_score

    breakdown["Forks"] = {
        "score": forks_score,
        "max": 15
    }

    # -----------------------------------------------------
    # Topics
    # -----------------------------------------------------

    topics = repo.get(
        "topics",
        []
    )

    if not isinstance(topics, list):
        topics = []

    if len(topics) >= 5:
        topic_score = 15
    elif len(topics) >= 3:
        topic_score = 11
    elif len(topics) >= 1:
        topic_score = 7
    else:
        topic_score = 0

    score += topic_score

    breakdown["Topics"] = {
        "score": topic_score,
        "max": 15
    }

    # -----------------------------------------------------
    # Recent Activity
    # -----------------------------------------------------

    updated_at = repo.get(
        "updated_at"
    )

    recent_score = 0

    if updated_at:

        try:
            from datetime import datetime, timezone

            parsed = datetime.fromisoformat(
                updated_at.replace(
                    "Z",
                    "+00:00"
                )
            )

            now = datetime.now(
                timezone.utc
            )

            if parsed.tzinfo is None:
                parsed = parsed.replace(
                    tzinfo=timezone.utc
                )

            days_old = (
                now - parsed
            ).days

            if days_old <= 30:
                recent_score = 15
            elif days_old <= 90:
                recent_score = 12
            elif days_old <= 180:
                recent_score = 8
            elif days_old <= 365:
                recent_score = 4

        except (
            TypeError,
            ValueError
        ):
            recent_score = 0

    score += recent_score

    breakdown["Recent Activity"] = {
        "score": recent_score,
        "max": 15
    }

    # -----------------------------------------------------
    # License
    # -----------------------------------------------------

    license_score = (
        10
        if repo.get("license")
        else 0
    )

    score += license_score

    breakdown["License"] = {
        "score": license_score,
        "max": 10
    }

    # -----------------------------------------------------
    # Final
    # -----------------------------------------------------

    total = clamp(score)

    return {
        "total": total,
        "score": total,
        "label": get_repository_label(
            total
        ),
        "breakdown": breakdown
    }


# =========================================================
# SCORE IMPROVEMENT SUGGESTIONS
# =========================================================

def get_repository_suggestions(repo):
    """
    Generate practical suggestions for improving
    a repository.
    """

    if not repo:
        return [
            "Select a repository to see improvement suggestions."
        ]

    suggestions = []

    # Description
    if not repo.get("description"):
        suggestions.append(
            "Add a clear project description so visitors immediately understand what the project does."
        )

    # Topics
    topics = repo.get(
        "topics",
        []
    )

    if not topics:
        suggestions.append(
            "Add relevant GitHub topics such as Java, Python, Streamlit, SQLite, or Machine Learning."
        )

    # License
    if not repo.get("license"):
        suggestions.append(
            "Consider adding an open-source license if you want others to reuse your project."
        )

    # Stars
    stars = safe_int(
        repo.get(
            "stargazers_count",
            0
        )
    )

    if stars == 0:
        suggestions.append(
            "Improve the README, project presentation, and documentation before sharing the repository."
        )

    # Activity
    updated_at = repo.get(
        "updated_at"
    )

    if updated_at:

        try:
            from datetime import datetime, timezone

            parsed = datetime.fromisoformat(
                updated_at.replace(
                    "Z",
                    "+00:00"
                )
            )

            now = datetime.now(
                timezone.utc
            )

            if parsed.tzinfo is None:
                parsed = parsed.replace(
                    tzinfo=timezone.utc
                )

            days_old = (
                now - parsed
            ).days

            if days_old > 180:
                suggestions.append(
                    "This repository has not been updated recently. Add improvements or document its current state."
                )

        except (
            TypeError,
            ValueError
        ):
            pass

    # README
    if not repo.get(
        "has_wiki",
        False
    ):
        suggestions.append(
            "Keep the README strong with setup steps, screenshots, features, tech stack, and usage instructions."
        )

    # Generic portfolio advice
    suggestions.append(
        "For a portfolio-ready project, include screenshots, a clear feature list, installation steps, and a demo link when possible."
    )

    return suggestions


# =========================================================
# SCORE BREAKDOWN HELPERS
# =========================================================

def get_score_percentage(score, maximum):
    """
    Convert a score into a percentage.
    """

    maximum = safe_int(
        maximum
    )

    if maximum <= 0:
        return 0

    return clamp(
        (safe_int(score) / maximum) * 100
    )


def get_developer_score_summary(score_data):
    """
    Create simple dashboard-friendly summary data.
    """

    if not score_data:
        return {
            "score": 0,
            "label": "No Data",
            "strongest_area": None,
            "weakest_area": None
        }

    breakdown = score_data.get(
        "breakdown",
        {}
    )

    if not breakdown:
        return {
            "score": score_data.get(
                "total",
                0
            ),
            "label": score_data.get(
                "label",
                "No Data"
            ),
            "strongest_area": None,
            "weakest_area": None
        }

    normalized = []

    for name, data in breakdown.items():

        current = safe_int(
            data.get(
                "score",
                0
            )
        )

        maximum = safe_int(
            data.get(
                "max",
                0
            )
        )

        percentage = (
            (current / maximum) * 100
            if maximum > 0
            else 0
        )

        normalized.append({
            "name": name,
            "score": current,
            "max": maximum,
            "percentage": percentage
        })

    strongest = max(
        normalized,
        key=lambda item: item["percentage"]
    )

    weakest = min(
        normalized,
        key=lambda item: item["percentage"]
    )

    return {
        "score": score_data.get(
            "total",
            0
        ),
        "label": score_data.get(
            "label",
            "No Data"
        ),
        "strongest_area": strongest,
        "weakest_area": weakest,
        "breakdown": normalized
    }