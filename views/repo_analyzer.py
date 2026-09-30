import streamlit as st
import pandas as pd
import plotly.express as px

from src.github_api import get_user_repos
from src.scorer import score_repository


# =========================================================
# COLORS
# =========================================================

BLUE = "#0284C7"
LIGHT_BLUE = "#38BDF8"
DARK_BLUE = "#075985"


# =========================================================
# STYLE
# =========================================================

def repo_style():

    st.markdown(
        f"""
        <style>

        h1, h2, h3, h4, h5, h6 {{
            color: {BLUE} !important;
        }}

        .stApp p,
        .stApp span,
        .stApp label {{
            color: #0F172A;
        }}

        .repo-title {{
            color: {BLUE} !important;
            font-size: 40px;
            font-weight: 800;
        }}

        .repo-subtitle {{
            color: {DARK_BLUE} !important;
            font-size: 17px;
        }}

        .section-title {{
            color: {BLUE} !important;
            font-size: 24px;
            font-weight: 750;
        }}

        .score-number {{
            color: {BLUE} !important;
            font-size: 36px;
            font-weight: 800;
        }}

        </style>
        """,
        unsafe_allow_html=True,
    )


# =========================================================
# MAIN PAGE
# =========================================================

def show_repo_analyzer():

    repo_style()

    st.markdown(
        '<div class="repo-title">Repository Analyzer</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="repo-subtitle">Review your projects and identify practical improvements for your developer portfolio.</div>',
        unsafe_allow_html=True,
    )

    st.divider()

    username = st.session_state.get(
        "github_username"
    )

    if not username:

        st.info(
            "Analyze your GitHub profile first. Your public repositories will appear here automatically."
        )

        if st.button(
            "Go to GitHub Analyzer",
            type="primary",
        ):

            st.session_state["page"] = "GitHub"
            st.rerun()

        return

    # =====================================================
    # LOAD REPOSITORIES
    # =====================================================

    with st.spinner(
        "Loading repositories..."
    ):

        repos = get_user_repos(
            username
        )

    if not repos:

        st.warning(
            "No public repositories were found."
        )

        return

    # =====================================================
    # REPOSITORY SELECTOR
    # =====================================================

    st.markdown(
        '<div class="section-title">Select a Repository</div>',
        unsafe_allow_html=True,
    )

    repo_names = [
        repo.get(
            "name",
            "Unknown Repository"
        )
        for repo in repos
    ]

    selected_name = st.selectbox(
        "Repository",
        repo_names,
    )

    selected_repo = next(
        (
            repo
            for repo in repos
            if repo.get("name") == selected_name
        ),
        None,
    )

    if not selected_repo:
        return

    st.divider()

    # =====================================================
    # REPOSITORY INFORMATION
    # =====================================================

    st.markdown(
        f'<div class="repo-title">{selected_repo.get("name", "Repository")}</div>',
        unsafe_allow_html=True,
    )

    st.write(
        selected_repo.get(
            "description"
        )
        or "No repository description available."
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Stars",
            selected_repo.get(
                "stargazers_count",
                0,
            ),
        )

    with col2:

        st.metric(
            "Forks",
            selected_repo.get(
                "forks_count",
                0,
            ),
        )

    with col3:

        st.metric(
            "Open Issues",
            selected_repo.get(
                "open_issues_count",
                0,
            ),
        )

    with col4:

        st.metric(
            "Language",
            selected_repo.get(
                "language"
            )
            or "N/A",
        )

    st.divider()

    # =====================================================
    # REPOSITORY SCORE
    # =====================================================

    st.markdown(
        '<div class="section-title">Repository Quality</div>',
        unsafe_allow_html=True,
    )

    try:

        result = score_repository(
            selected_repo
        )

        if isinstance(
            result,
            dict,
        ):

            score = result.get(
                "total",
                result.get(
                    "score",
                    0,
                ),
            )

        else:

            score = int(result)

    except Exception:

        score = 0

    score = max(
        0,
        min(
            int(score),
            100,
        ),
    )

    col1, col2 = st.columns(
        [1, 3]
    )

    with col1:

        st.markdown(
            f'<div class="score-number">{score}/100</div>',
            unsafe_allow_html=True,
        )

    with col2:

        st.progress(
            score / 100
        )

        if score >= 80:

            st.success(
                "Strong repository profile."
            )

        elif score >= 60:

            st.info(
                "Good repository with room for improvement."
            )

        else:

            st.warning(
                "This repository has several areas that could be improved."
            )

    st.divider()

    # =====================================================
    # PROJECT DETAILS
    # =====================================================

    st.markdown(
        '<div class="section-title">Project Details</div>',
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)

    with col1:

        st.write(
            f"**Created:** "
            f"{selected_repo.get('created_at', 'Unknown')}"
        )

        st.write(
            f"**Updated:** "
            f"{selected_repo.get('updated_at', 'Unknown')}"
        )

        st.write(
            f"**Default Branch:** "
            f"{selected_repo.get('default_branch', 'Unknown')}"
        )

    with col2:

        st.write(
            f"**Fork:** "
            f"{'Yes' if selected_repo.get('fork') else 'No'}"
        )

        st.write(
            f"**Archived:** "
            f"{'Yes' if selected_repo.get('archived') else 'No'}"
        )

        st.write(
            f"**Size:** "
            f"{selected_repo.get('size', 0)} KB"
        )

    st.divider()

    # =====================================================
    # TOPICS
    # =====================================================

    topics = selected_repo.get(
        "topics",
        []
    )

    st.markdown(
        '<div class="section-title">Technologies & Topics</div>',
        unsafe_allow_html=True,
    )

    if topics:

        st.write(
            " • ".join(
                topics
            )
        )

    else:

        st.info(
            "No repository topics have been added."
        )

    st.divider()

    # =====================================================
    # SUGGESTIONS
    # =====================================================

    st.markdown(
        '<div class="section-title">Portfolio Improvements</div>',
        unsafe_allow_html=True,
    )

    suggestions = []

    description = selected_repo.get(
        "description"
    )

    if not description:

        suggestions.append(
            "Add a clear and concise project description."
        )

    if not topics:

        suggestions.append(
            "Add GitHub topics so recruiters can understand the technologies used."
        )

    if selected_repo.get(
        "stargazers_count",
        0,
    ) == 0:

        suggestions.append(
            "Improve project visibility by sharing the project and adding it to your portfolio."
        )

    if not selected_repo.get(
        "homepage"
    ):

        suggestions.append(
            "Consider adding a live demo or project website."
        )

    if not suggestions:

        suggestions.append(
            "Your repository already has the basic portfolio information. Continue improving documentation and code quality."
        )

    for suggestion in suggestions:

        st.write(
            f"• {suggestion}"
        )

    st.divider()

    # =====================================================
    # GITHUB LINK
    # =====================================================

    repo_url = selected_repo.get(
        "html_url"
    )

    if repo_url:

        st.link_button(
            "Open Repository on GitHub",
            repo_url,
            type="primary",
        )

