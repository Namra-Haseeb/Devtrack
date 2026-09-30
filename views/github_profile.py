import streamlit as st
import pandas as pd
import plotly.express as px

from src.github_api import (
    get_user_profile,
    get_user_repos,
    get_user_events,
)

from src.analyzer import analyze_profile
from src.scorer import (
    calculate_developer_score,
    score_repository,
)

from src.database import update_user_github_username


# =========================================================
# COLORS
# =========================================================

BLUE = "#0284C7"
LIGHT_BLUE = "#38BDF8"
DARK_BLUE = "#075985"


# =========================================================
# GLOBAL DASHBOARD STYLE
# =========================================================

def dashboard_style():

    st.markdown(
        f"""
        <style>

        .devtrack-blue {{
            color: {BLUE};
        }}

        .devtrack-light-blue {{
            color: {LIGHT_BLUE};
        }}

        .devtrack-dark-blue {{
            color: {DARK_BLUE};
        }}

        .dashboard-title {{
            color: {BLUE};
            font-size: 42px;
            font-weight: 800;
            margin-bottom: 5px;
        }}

        .dashboard-subtitle {{
            color: {BLUE};
            font-size: 17px;
            margin-bottom: 20px;
        }}

        .section-title {{
            color: {BLUE};
            font-size: 25px;
            font-weight: 750;
            margin-top: 10px;
            margin-bottom: 12px;
        }}

        .feature-number {{
            color: {LIGHT_BLUE};
            font-size: 30px;
            font-weight: 800;
        }}

        .feature-title {{
            color: {BLUE};
            font-size: 21px;
            font-weight: 700;
        }}

        .feature-text {{
            color: {BLUE};
            font-size: 16px;
            line-height: 1.5;
        }}

        </style>
        """,
        unsafe_allow_html=True,
    )


# =========================================================
# FORMAT NUMBER
# =========================================================

def format_number(number):

    try:

        number = int(number)

        if number >= 1_000_000:
            return f"{number / 1_000_000:.1f}M"

        if number >= 1_000:
            return f"{number / 1_000:.1f}K"

        return str(number)

    except Exception:

        return "0"


# =========================================================
# PAGE HEADER
# =========================================================

def render_page_header(title, subtitle):

    st.markdown(
        '<div class="devtrack-light-blue" style="font-size:16px;font-weight:800;letter-spacing:2px;">DEVTRACK</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        f'<div class="dashboard-title">{title}</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        f'<div class="dashboard-subtitle">{subtitle}</div>',
        unsafe_allow_html=True,
    )

    st.divider()


# =========================================================
# LOAD GITHUB DATA
# =========================================================

def get_github_data(username):

    profile = get_user_profile(username)

    if not profile:
        return None

    repos = get_user_repos(username)
    events = get_user_events(username)

    return {
        "profile": profile,
        "repos": repos or [],
        "events": events or [],
    }


# =========================================================
# EMPTY DASHBOARD
# =========================================================

def render_empty_dashboard():

    st.markdown(
        '<div class="section-title">Welcome to DevTrack</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="dashboard-title">Build your developer profile with data.</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="dashboard-subtitle">Connect your GitHub account to analyze repositories, technologies, activity and development progress.</div>',
        unsafe_allow_html=True,
    )

    st.info(
        "Go to the GitHub section from the sidebar and enter your GitHub username to get started."
    )

    st.divider()

    st.markdown(
        '<div class="section-title">What DevTrack can analyze</div>',
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown(
            '<div class="feature-number">01</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            '<div class="feature-title">GitHub Analysis</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            '<div class="feature-text">Understand your repositories, technologies and development activity.</div>',
            unsafe_allow_html=True,
        )

    with col2:

        st.markdown(
            '<div class="feature-number">02</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            '<div class="feature-title">Skill Development</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            '<div class="feature-text">Identify the skills required for your target career path.</div>',
            unsafe_allow_html=True,
        )

    with col3:

        st.markdown(
            '<div class="feature-number">03</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            '<div class="feature-title">Career Roadmap</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            '<div class="feature-text">Turn your skill gaps into a structured learning plan.</div>',
            unsafe_allow_html=True,
        )


# =========================================================
# SCORE
# =========================================================

def render_score(score):

    st.markdown(
        '<div class="section-title">DevTrack Score</div>',
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns([1, 3])

    with col1:

        st.metric(
            "Developer Score",
            f"{score}/100",
        )

    with col2:

        st.progress(
            max(0, min(score, 100)) / 100
        )

        if score >= 80:

            st.success(
                "Strong developer profile."
            )

        elif score >= 60:

            st.info(
                "Good progress. Keep improving."
            )

        elif score >= 40:

            st.warning(
                "There are several areas you can improve."
            )

        else:

            st.warning(
                "Start building your developer profile."
            )


# =========================================================
# DASHBOARD
# =========================================================

def show_home():

    dashboard_style()

    render_page_header(
        "Developer Dashboard",
        "A single view of your GitHub activity, progress and career direction.",
    )

    username = st.session_state.get(
        "github_username"
    )

    if not username:

        render_empty_dashboard()

        return

    data = get_github_data(username)

    if not data:

        st.error(
            "Unable to load your GitHub profile. Please check your username."
        )

        return

    profile = data["profile"]
    repos = data["repos"]
    events = data["events"]

    try:

        analysis = analyze_profile(
            profile,
            repos,
            events,
        )

    except Exception:

        analysis = {}

    # =====================================================
    # PROFILE
    # =====================================================

    st.markdown(
        f'<div class="section-title">Welcome back, {profile.get("name") or username}</div>',
        unsafe_allow_html=True,
    )

    st.write(
        profile.get("bio")
        or "Keep building projects and growing your developer profile."
    )

    st.divider()

    # =====================================================
    # BASIC METRICS
    # =====================================================

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Repositories",
            format_number(
                profile.get(
                    "public_repos",
                    0,
                )
            ),
        )

    with col2:

        st.metric(
            "Followers",
            format_number(
                profile.get(
                    "followers",
                    0,
                )
            ),
        )

    with col3:

        st.metric(
            "Following",
            format_number(
                profile.get(
                    "following",
                    0,
                )
            ),
        )

    with col4:

        st.metric(
            "Public Gists",
            format_number(
                profile.get(
                    "public_gists",
                    0,
                )
            ),
        )

    st.divider()

    # =====================================================
    # SCORE
    # =====================================================

    try:

        score = calculate_developer_score(
            analysis
        )

        if isinstance(score, dict):

            score = score.get(
                "total",
                score.get(
                    "score",
                    0,
                ),
            )

        score = int(score)

    except Exception:

        score = 0

    render_score(score)

    st.divider()

    # =====================================================
    # DEVELOPMENT OVERVIEW
    # =====================================================

    st.markdown(
        '<div class="section-title">Development Overview</div>',
        unsafe_allow_html=True,
    )

    total_stars = sum(
        int(
            repo.get(
                "stargazers_count",
                0,
            )
            or 0
        )
        for repo in repos
    )

    total_forks = sum(
        int(
            repo.get(
                "forks_count",
                0,
            )
            or 0
        )
        for repo in repos
    )

    languages = {}

    for repo in repos:

        language = repo.get(
            "language"
        )

        if language:

            languages[language] = (
                languages.get(
                    language,
                    0,
                )
                + 1
            )

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Repositories",
            format_number(
                len(repos)
            ),
        )

    with col2:

        st.metric(
            "Stars",
            format_number(
                total_stars
            ),
        )

    with col3:

        st.metric(
            "Forks",
            format_number(
                total_forks
            ),
        )

    with col4:

        st.metric(
            "Languages",
            format_number(
                len(languages)
            ),
        )

    st.divider()

    # =====================================================
    # TECHNOLOGY CHART
    # =====================================================

    st.markdown(
        '<div class="section-title">Technology Usage</div>',
        unsafe_allow_html=True,
    )

    if languages:

        language_df = pd.DataFrame(
            {
                "Technology": list(
                    languages.keys()
                ),
                "Repositories": list(
                    languages.values()
                ),
            }
        )

        language_df = language_df.sort_values(
            "Repositories",
            ascending=False,
        )

        fig = px.bar(
            language_df,
            x="Technology",
            y="Repositories",
            title="Languages Used Across Repositories",
        )

        fig.update_layout(
            height=400,
            margin=dict(
                l=20,
                r=20,
                t=60,
                b=20,
            ),
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
        )

    else:

        st.info(
            "No programming language data was found."
        )

    st.divider()

    # =====================================================
    # FEATURED REPOSITORIES
    # =====================================================

    st.markdown(
        '<div class="section-title">Featured Repositories</div>',
        unsafe_allow_html=True,
    )

    if not repos:

        st.info(
            "No public repositories found."
        )

    else:

        sorted_repos = sorted(
            repos,
            key=lambda repo: (
                int(
                    repo.get(
                        "stargazers_count",
                        0,
                    )
                    or 0
                ),
                int(
                    repo.get(
                        "forks_count",
                        0,
                    )
                    or 0
                ),
            ),
            reverse=True,
        )

        for repo in sorted_repos[:5]:

            st.subheader(
                repo.get(
                    "name",
                    "Repository",
                )
            )

            st.write(
                repo.get(
                    "description"
                )
                or "No description available."
            )

            col1, col2, col3 = st.columns(3)

            with col1:

                st.write(
                    f"**Language:** "
                    f"{repo.get('language') or 'Not specified'}"
                )

            with col2:

                st.write(
                    f"**Stars:** "
                    f"{repo.get('stargazers_count', 0)}"
                )

            with col3:

                st.write(
                    f"**Forks:** "
                    f"{repo.get('forks_count', 0)}"
                )

            repo_url = repo.get(
                "html_url"
            )

            if repo_url:

                st.link_button(
                    "View Repository",
                    repo_url,
                )

            st.divider()

    # =====================================================
    # QUICK ACTIONS
    # =====================================================

    st.markdown(
        '<div class="section-title">Quick Actions</div>',
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        if st.button(
            "📦 Repositories",
            use_container_width=True,
        ):

            st.session_state["page"] = "Repositories"
            st.rerun()

    with col2:

        if st.button(
            "📚 Skills",
            use_container_width=True,
        ):

            st.session_state["page"] = "Skills"
            st.rerun()

    with col3:

        if st.button(
            "🗺️ Roadmap",
            use_container_width=True,
        ):

            st.session_state["page"] = "Roadmap"
            st.rerun()


# =========================================================
# GITHUB ANALYZER
# =========================================================

def show_github_analyzer():

    dashboard_style()

    render_page_header(
        "GitHub Analyzer",
        "Analyze your GitHub profile, repositories and development activity.",
    )

    current_username = st.session_state.get(
        "github_username",
        "",
    )

    username = st.text_input(
        "GitHub Username",
        value=current_username,
        placeholder="Enter your GitHub username",
    )

    col1, col2 = st.columns(2)

    with col1:

        analyze_button = st.button(
            "Analyze GitHub",
            type="primary",
            use_container_width=True,
        )

    with col2:

        clear_button = st.button(
            "Clear",
            use_container_width=True,
        )

    if clear_button:

        st.session_state.pop(
            "github_data",
            None,
        )

        st.session_state.pop(
            "github_username",
            None,
        )

        st.rerun()

    if analyze_button:

        username = username.strip()

        if not username:

            st.warning(
                "Please enter a GitHub username."
            )

            return

        with st.spinner(
            "Analyzing GitHub profile..."
        ):

            data = get_github_data(
                username
            )

        if not data:

            st.error(
                "GitHub user not found or GitHub API request failed."
            )

            return

        st.session_state[
            "github_username"
        ] = username

        st.session_state[
            "github_data"
        ] = data

        user_id = st.session_state.get(
            "user_id"
        )

        if user_id:

            try:

                update_user_github_username(
                    user_id,
                    username,
                )

            except Exception:

                pass

        st.success(
            "GitHub profile analyzed successfully."
        )

    data = st.session_state.get(
        "github_data"
    )

    if not data:

        st.info(
            "Enter a GitHub username above to begin the analysis."
        )

        return

    profile = data["profile"]
    repos = data["repos"]
    events = data["events"]

    try:

        analysis = analyze_profile(
            profile,
            repos,
            events,
        )

    except Exception:

        analysis = {}

    # =====================================================
    # PROFILE METRICS
    # =====================================================

    st.markdown(
        '<div class="section-title">Profile Overview</div>',
        unsafe_allow_html=True,
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Repositories",
            format_number(
                profile.get(
                    "public_repos",
                    0,
                )
            ),
        )

    with col2:

        st.metric(
            "Followers",
            format_number(
                profile.get(
                    "followers",
                    0,
                )
            ),
        )

    with col3:

        st.metric(
            "Following",
            format_number(
                profile.get(
                    "following",
                    0,
                )
            ),
        )

    with col4:

        st.metric(
            "Gists",
            format_number(
                profile.get(
                    "public_gists",
                    0,
                )
            ),
        )

    st.divider()

    # =====================================================
    # SCORE
    # =====================================================

    try:

        score = calculate_developer_score(
            analysis
        )

        if isinstance(score, dict):

            score = score.get(
                "total",
                score.get(
                    "score",
                    0,
                ),
            )

        score = int(score)

    except Exception:

        score = 0

    render_score(score)

    st.divider()

    # =====================================================
    # TABS
    # =====================================================

    overview_tab, repositories_tab, activity_tab = st.tabs(
        [
            "Overview",
            "Repositories",
            "Activity",
        ]
    )

    # =====================================================
    # OVERVIEW
    # =====================================================

    with overview_tab:

        st.markdown(
            '<div class="section-title">Languages</div>',
            unsafe_allow_html=True,
        )

        languages = {}

        for repo in repos:

            language = repo.get(
                "language"
            )

            if language:

                languages[language] = (
                    languages.get(
                        language,
                        0,
                    )
                    + 1
                )

        if languages:

            language_df = pd.DataFrame(
                {
                    "Language": list(
                        languages.keys()
                    ),
                    "Repositories": list(
                        languages.values()
                    ),
                }
            )

            language_df = language_df.sort_values(
                "Repositories",
                ascending=False,
            )

            fig = px.bar(
                language_df,
                x="Language",
                y="Repositories",
                title="Language Distribution",
            )

            st.plotly_chart(
                fig,
                use_container_width=True,
            )

        else:

            st.info(
                "No language information available."
            )

    # =====================================================
    # REPOSITORIES
    # =====================================================

    with repositories_tab:

        st.markdown(
            '<div class="section-title">Repository Analysis</div>',
            unsafe_allow_html=True,
        )

        if not repos:

            st.info(
                "No repositories found."
            )

        else:

            repository_rows = []

            for repo in repos:

                repository_rows.append(
                    {
                        "Repository": repo.get(
                            "name",
                            "",
                        ),
                        "Language": repo.get(
                            "language"
                        )
                        or "—",
                        "Stars": repo.get(
                            "stargazers_count",
                            0,
                        ),
                        "Forks": repo.get(
                            "forks_count",
                            0,
                        ),
                        "Issues": repo.get(
                            "open_issues_count",
                            0,
                        ),
                    }
                )

            repo_df = pd.DataFrame(
                repository_rows
            )

            st.dataframe(
                repo_df,
                use_container_width=True,
                hide_index=True,
            )

            st.divider()

            st.markdown(
                '<div class="section-title">Repository Scores</div>',
                unsafe_allow_html=True,
            )

            for repo in repos[:10]:

                try:

                    repo_score = score_repository(
                        repo
                    )

                    if isinstance(
                        repo_score,
                        dict,
                    ):

                        value = repo_score.get(
                            "total",
                            repo_score.get(
                                "score",
                                0,
                            ),
                        )

                    else:

                        value = int(
                            repo_score
                        )

                    value = int(value)

                except Exception:

                    value = 0

                st.write(
                    f"**{repo.get('name', 'Repository')}** — "
                    f"{value}/100"
                )

                st.progress(
                    max(
                        0,
                        min(
                            value,
                            100,
                        ),
                    )
                    / 100
                )

    # =====================================================
    # ACTIVITY
    # =====================================================

    with activity_tab:

        st.markdown(
            '<div class="section-title">GitHub Activity</div>',
            unsafe_allow_html=True,
        )

        st.write(
            f"Recent GitHub events analyzed: **{len(events)}**"
        )

        if events:

            activity_rows = []

            for event in events[:20]:

                repo_name = (
                    event.get(
                        "repo",
                        {}
                    ).get(
                        "name",
                        "Unknown",
                    )
                )

                activity_rows.append(
                    {
                        "Event": event.get(
                            "type",
                            "Unknown",
                        ),
                        "Repository": repo_name,
                        "Date": event.get(
                            "created_at",
                            "",
                        ),
                    }
                )

            activity_df = pd.DataFrame(
                activity_rows
            )

            st.dataframe(
                activity_df,
                use_container_width=True,
                hide_index=True,
            )

        else:

            st.info(
                "No recent public activity found."
            )

