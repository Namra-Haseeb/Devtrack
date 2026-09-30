import streamlit as st
from datetime import datetime


# =========================================================
# NAVIGATION
# =========================================================

def navigate(page):
    st.session_state["page"] = page
    st.rerun()


# =========================================================
# HELPERS
# =========================================================

def get_user():
    return st.session_state.get("user")


def get_github_data():
    return st.session_state.get("github_data")


def get_github_repos():
    return st.session_state.get("github_repos")


def calculate_github_stats():
    github_data = get_github_data()
    repos = get_github_repos()

    if not github_data:
        return {
            "connected": False,
            "repos": 0,
            "followers": 0,
            "following": 0,
        }

    repo_count = github_data.get(
        "public_repos",
        0
    )

    if isinstance(repos, list):
        repo_count = len(repos)

    return {
        "connected": True,
        "repos": repo_count,
        "followers": github_data.get(
            "followers",
            0
        ),
        "following": github_data.get(
            "following",
            0
        ),
    }


# =========================================================
# DASHBOARD
# =========================================================

def show_dashboard():

    user = get_user()

    if not user:
        st.error("User session not found.")
        return

    name = user.get(
        "name",
        "Developer"
    )

    career = user.get(
        "career_path",
        "Developer"
    )

    github = calculate_github_stats()

    # =====================================================
    # CSS
    # =====================================================

    st.markdown(
        """
        <style>

        /* =========================
           PAGE
        ========================= */

        .block-container {
            max-width: 1400px !important;
            padding-top: 2rem !important;
            padding-bottom: 4rem !important;
        }


        /* =========================
           HEADER
        ========================= */

        .dashboard-header {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;

            margin-bottom: 1.8rem;
        }

        .greeting {
            font-size: 0.78rem;
            font-weight: 600;

            color: #0284C7;

            text-transform: uppercase;
            letter-spacing: 0.08em;

            margin-bottom: 0.35rem;
        }

        .dashboard-title {
            font-size: 2.25rem;
            font-weight: 800;

            color: #0F172A;

            letter-spacing: -1px;

            line-height: 1.1;
        }

        .dashboard-subtitle {
            color: #64748B;

            font-size: 0.92rem;

            margin-top: 0.45rem;
        }


        /* =========================
           PROFILE PILL
        ========================= */

        .profile-pill {
            display: flex;
            align-items: center;

            gap: 10px;

            background: white;

            border: 1px solid #E2E8F0;

            padding:
                0.55rem
                0.8rem;

            border-radius: 12px;

            box-shadow:
                0 4px 12px
                rgba(15,23,42,0.04);
        }

        .profile-avatar {
            width: 35px;
            height: 35px;

            border-radius: 10px;

            background:
                linear-gradient(
                    135deg,
                    #38BDF8,
                    #0284C7
                );

            color: white;

            display: flex;
            align-items: center;
            justify-content: center;

            font-weight: 800;
        }

        .profile-name {
            color: #0F172A;
            font-size: 0.8rem;
            font-weight: 700;
        }

        .profile-role {
            color: #94A3B8;
            font-size: 0.68rem;
        }


        /* =========================
           HERO
        ========================= */

        .hero {
            position: relative;

            overflow: hidden;

            background:
                linear-gradient(
                    115deg,
                    #0284C7 0%,
                    #0EA5E9 55%,
                    #38BDF8 100%
                );

            border-radius: 20px;

            padding:
                2rem 2.2rem;

            min-height: 185px;

            color: white;

            box-shadow:
                0 15px 35px
                rgba(2,132,199,0.18);

            margin-bottom: 1.5rem;
        }

        .hero::after {
            content: "";

            position: absolute;

            width: 300px;
            height: 300px;

            border-radius: 50%;

            background:
                rgba(255,255,255,0.08);

            right: -90px;
            top: -130px;
        }

        .hero::before {
            content: "";

            position: absolute;

            width: 180px;
            height: 180px;

            border-radius: 50%;

            border:
                30px solid
                rgba(255,255,255,0.05);

            right: 150px;
            bottom: -100px;
        }

        .hero-content {
            position: relative;
            z-index: 2;

            max-width: 680px;
        }

        .hero-label {
            font-size: 0.68rem;

            font-weight: 700;

            letter-spacing: 0.1em;

            text-transform: uppercase;

            opacity: 0.8;

            margin-bottom: 0.6rem;
        }

        .hero-title {
            font-size: 1.7rem;

            font-weight: 800;

            margin-bottom: 0.5rem;

            letter-spacing: -0.5px;
        }

        .hero-text {
            font-size: 0.86rem;

            opacity: 0.88;

            line-height: 1.6;

            max-width: 600px;
        }


        /* =========================
           SECTION
        ========================= */

        .section-heading {
            display: flex;

            align-items: center;

            justify-content: space-between;

            margin:
                1.7rem 0
                0.85rem;
        }

        .section-title {
            font-size: 1rem;

            font-weight: 800;

            color: #0F172A;
        }

        .section-description {
            font-size: 0.72rem;

            color: #94A3B8;
        }


        /* =========================
           STAT CARDS
        ========================= */

        .stat-card {
            background: white;

            border:
                1px solid #E2E8F0;

            border-radius: 15px;

            padding: 1.15rem;

            min-height: 125px;

            transition:
                transform 0.15s ease,
                border-color 0.15s ease;
        }

        .stat-card:hover {
            transform: translateY(-2px);

            border-color: #BAE6FD;
        }

        .stat-top {
            display: flex;

            justify-content: space-between;

            align-items: center;

            margin-bottom: 0.9rem;
        }

        .stat-icon {
            width: 34px;
            height: 34px;

            border-radius: 9px;

            display: flex;
            align-items: center;
            justify-content: center;

            background: #F0F9FF;

            font-size: 16px;
        }

        .stat-arrow {
            color: #CBD5E1;
            font-size: 14px;
        }

        .stat-label {
            color: #64748B;

            font-size: 0.7rem;

            font-weight: 600;

            margin-bottom: 0.2rem;
        }

        .stat-value {
            color: #0F172A;

            font-size: 1.45rem;

            font-weight: 800;

            letter-spacing: -0.5px;
        }

        .stat-description {
            color: #94A3B8;

            font-size: 0.65rem;

            margin-top: 0.15rem;
        }


        /* =========================
           MAIN CARDS
        ========================= */

        .content-card {
            background: white;

            border:
                1px solid #E2E8F0;

            border-radius: 16px;

            padding: 1.35rem;

            height: 100%;
        }

        .content-card-title {
            color: #0F172A;

            font-size: 0.92rem;

            font-weight: 800;

            margin-bottom: 0.2rem;
        }

        .content-card-subtitle {
            color: #94A3B8;

            font-size: 0.68rem;

            margin-bottom: 1.1rem;
        }


        /* =========================
           CAREER PROGRESS
        ========================= */

        .career-path {
            color: #0284C7;

            font-size: 0.72rem;

            font-weight: 700;

            background: #E0F2FE;

            display: inline-block;

            padding:
                0.3rem
                0.55rem;

            border-radius: 6px;

            margin-bottom: 1rem;
        }

        .progress-row {
            margin-bottom: 0.85rem;
        }

        .progress-info {
            display: flex;

            justify-content: space-between;

            margin-bottom: 0.3rem;
        }

        .progress-name {
            font-size: 0.72rem;

            color: #475569;

            font-weight: 600;
        }

        .progress-value {
            font-size: 0.68rem;

            color: #94A3B8;
        }

        .progress-track {
            height: 6px;

            width: 100%;

            background: #E2E8F0;

            border-radius: 10px;

            overflow: hidden;
        }

        .progress-fill {
            height: 100%;

            background:
                linear-gradient(
                    90deg,
                    #38BDF8,
                    #0284C7
                );

            border-radius: 10px;
        }


        /* =========================
           ACTIONS
        ========================= */

        .action-item {
            display: flex;

            align-items: center;

            gap: 10px;

            padding:
                0.75rem 0;

            border-bottom:
                1px solid #F1F5F9;
        }

        .action-item:last-child {
            border-bottom: none;
        }

        .action-icon {
            width: 32px;
            height: 32px;

            border-radius: 8px;

            background: #F8FAFC;

            display: flex;
            align-items: center;
            justify-content: center;

            font-size: 14px;
        }

        .action-text {
            flex: 1;
        }

        .action-title {
            color: #334155;

            font-size: 0.73rem;

            font-weight: 600;
        }

        .action-subtitle {
            color: #94A3B8;

            font-size: 0.62rem;

            margin-top: 2px;
        }


        /* =========================
           JOB PIPELINE
        ========================= */

        .job-number {
            font-size: 1.55rem;

            color: #0F172A;

            font-weight: 800;
        }

        .job-label {
            font-size: 0.65rem;

            color: #64748B;

            margin-top: 2px;
        }

        .job-column {
            text-align: center;

            padding:
                0.7rem 0.3rem;

            border-right:
                1px solid #E2E8F0;
        }

        .job-column:last-child {
            border-right: none;
        }


        /* =========================
           QUICK ACTION
        ========================= */

        .quick-card {
            background: white;

            border:
                1px solid #E2E8F0;

            border-radius: 13px;

            padding: 1rem;

            text-align: center;

            min-height: 110px;
        }

        .quick-icon {
            font-size: 21px;

            margin-bottom: 0.45rem;
        }

        .quick-title {
            color: #0F172A;

            font-size: 0.72rem;

            font-weight: 700;
        }

        .quick-text {
            color: #94A3B8;

            font-size: 0.6rem;

            margin-top: 3px;
        }


        /* =========================
           FOOTER
        ========================= */

        .dashboard-footer {
            text-align: center;

            color: #CBD5E1;

            font-size: 0.62rem;

            margin-top: 2.5rem;
        }

        </style>
        """,
        unsafe_allow_html=True
    )


    # =====================================================
    # HEADER
    # =====================================================

    hour = datetime.now().hour

    if hour < 12:
        greeting = "Good morning"
    elif hour < 18:
        greeting = "Good afternoon"
    else:
        greeting = "Good evening"


    first_name = name.split()[0]


    avatar = first_name[0].upper()


    st.markdown(
        f"""
        <div class="dashboard-header">

            <div>

                <div class="greeting">
                    {greeting}
                </div>

                <div class="dashboard-title">
                    Welcome back, {first_name} 👋
                </div>

                <div class="dashboard-subtitle">
                    Here's your developer progress at a glance.
                </div>

            </div>

            <div class="profile-pill">

                <div class="profile-avatar">
                    {avatar}
                </div>

                <div>

                    <div class="profile-name">
                        {name}
                    </div>

                    <div class="profile-role">
                        {career}
                    </div>

                </div>

            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    # =====================================================
    # HERO
    # =====================================================

    st.markdown(
        f"""
        <div class="hero">

            <div class="hero-content">

                <div class="hero-label">
                    YOUR DEVELOPER JOURNEY
                </div>

                <div class="hero-title">
                    Build your skills. Track your progress.
                </div>

                <div class="hero-text">
                    DevTrack brings your GitHub activity,
                    technical skills, learning roadmap,
                    projects and job preparation together
                    in one place.
                </div>

            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    # =====================================================
    # SNAPSHOT
    # =====================================================

    st.markdown(
        """
        <div class="section-heading">

            <div class="section-title">
                Developer Snapshot
            </div>

            <div class="section-description">
                Your current activity
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    c1, c2, c3, c4 = st.columns(4)


    # -----------------------------------------------------
    # GITHUB
    # -----------------------------------------------------

    with c1:

        if github["connected"]:

            github_value = github["repos"]

            github_desc = (
                f'{github["followers"]} followers'
            )

        else:

            github_value = "—"

            github_desc = "Connect your GitHub"


        st.markdown(
            f"""
            <div class="stat-card">

                <div class="stat-top">

                    <div class="stat-icon">
                        💻
                    </div>

                    <div class="stat-arrow">
                        →
                    </div>

                </div>

                <div class="stat-label">
                    GITHUB
                </div>

                <div class="stat-value">
                    {github_value}
                </div>

                <div class="stat-description">
                    {github_desc}
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    # -----------------------------------------------------
    # CAREER
    # -----------------------------------------------------

    with c2:

        st.markdown(
            """
            <div class="stat-card">

                <div class="stat-top">

                    <div class="stat-icon">
                        🎯
                    </div>

                    <div class="stat-arrow">
                        →
                    </div>

                </div>

                <div class="stat-label">
                    CAREER READINESS
                </div>

                <div class="stat-value">
                    0%
                </div>

                <div class="stat-description">
                    Start building your profile
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    # -----------------------------------------------------
    # DSA
    # -----------------------------------------------------

    with c3:

        st.markdown(
            """
            <div class="stat-card">

                <div class="stat-top">

                    <div class="stat-icon">
                        🧩
                    </div>

                    <div class="stat-arrow">
                        →
                    </div>

                </div>

                <div class="stat-label">
                    DSA PROBLEMS
                </div>

                <div class="stat-value">
                    0
                </div>

                <div class="stat-description">
                    Problems solved
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    # -----------------------------------------------------
    # PROJECTS
    # -----------------------------------------------------

    with c4:

        st.markdown(
            """
            <div class="stat-card">

                <div class="stat-top">

                    <div class="stat-icon">
                        🚀
                    </div>

                    <div class="stat-arrow">
                        →
                    </div>

                </div>

                <div class="stat-label">
                    PROJECTS
                </div>

                <div class="stat-value">
                    0
                </div>

                <div class="stat-description">
                    Portfolio projects
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    # =====================================================
    # CAREER + ACTIONS
    # =====================================================

    st.markdown(
        """
        <div class="section-heading">

            <div class="section-title">
                Your Career Progress
            </div>

            <div class="section-description">
                Based on your selected career path
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    left, right = st.columns(
        [1.35, 1],
        gap="large"
    )


    # =====================================================
    # CAREER PROGRESS CARD
    # =====================================================

    with left:

        st.markdown(
            f"""
            <div class="content-card">

                <div class="content-card-title">
                    {career}
                </div>

                <div class="content-card-subtitle">
                    Build the skills needed for your target role.
                </div>

                <div class="career-path">
                    {career}
                </div>

                <div class="progress-row">

                    <div class="progress-info">

                        <div class="progress-name">
                            Programming Fundamentals
                        </div>

                        <div class="progress-value">
                            0%
                        </div>

                    </div>

                    <div class="progress-track">
                        <div
                            class="progress-fill"
                            style="width:0%"
                        ></div>
                    </div>

                </div>


                <div class="progress-row">

                    <div class="progress-info">

                        <div class="progress-name">
                            Data Structures & Algorithms
                        </div>

                        <div class="progress-value">
                            0%
                        </div>

                    </div>

                    <div class="progress-track">
                        <div
                            class="progress-fill"
                            style="width:0%"
                        ></div>
                    </div>

                </div>


                <div class="progress-row">

                    <div class="progress-info">

                        <div class="progress-name">
                            Backend / Technical Skills
                        </div>

                        <div class="progress-value">
                            0%
                        </div>

                    </div>

                    <div class="progress-track">
                        <div
                            class="progress-fill"
                            style="width:0%"
                        ></div>
                    </div>

                </div>


                <div class="progress-row">

                    <div class="progress-info">

                        <div class="progress-name">
                            Projects & Portfolio
                        </div>

                        <div class="progress-value">
                            0%
                        </div>

                    </div>

                    <div class="progress-track">
                        <div
                            class="progress-fill"
                            style="width:0%"
                        ></div>
                    </div>

                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


        st.markdown(
            "<div style='height:8px'></div>",
            unsafe_allow_html=True
        )


        if st.button(
            "🗺️  Continue Roadmap",
            key="dashboard_roadmap",
            use_container_width=True
        ):

            navigate("roadmap")


    # =====================================================
    # TODAY'S ACTIONS
    # =====================================================

    with right:

        st.markdown(
            """
            <div class="content-card">

                <div class="content-card-title">
                    Today's Actions
                </div>

                <div class="content-card-subtitle">
                    Small steps that move your profile forward.
                </div>


                <div class="action-item">

                    <div class="action-icon">
                        💻
                    </div>

                    <div class="action-text">

                        <div class="action-title">
                            Connect GitHub
                        </div>

                        <div class="action-subtitle">
                            Analyze your developer profile
                        </div>

                    </div>

                </div>


                <div class="action-item">

                    <div class="action-icon">
                        📚
                    </div>

                    <div class="action-text">

                        <div class="action-title">
                            Add your skills
                        </div>

                        <div class="action-subtitle">
                            Build your technical profile
                        </div>

                    </div>

                </div>


                <div class="action-item">

                    <div class="action-icon">
                        🧩
                    </div>

                    <div class="action-text">

                        <div class="action-title">
                            Start DSA practice
                        </div>

                        <div class="action-subtitle">
                            Track your first problem
                        </div>

                    </div>

                </div>


                <div class="action-item">

                    <div class="action-icon">
                        🚀
                    </div>

                    <div class="action-text">

                        <div class="action-title">
                            Add a project
                        </div>

                        <div class="action-subtitle">
                            Start building your portfolio
                        </div>

                    </div>

                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    # =====================================================
    # JOB PREPARATION
    # =====================================================

    st.markdown(
        """
        <div class="section-heading">

            <div class="section-title">
                Job Preparation
            </div>

            <div class="section-description">
                Keep your applications organized
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    st.markdown(
        """
        <div class="content-card">

            <div class="content-card-title">
                Application Pipeline
            </div>

            <div class="content-card-subtitle">
                Your current job application activity.
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    j1, j2, j3, j4, j5 = st.columns(5)


    job_items = [
        ("0", "Saved"),
        ("0", "Applied"),
        ("0", "Assessment"),
        ("0", "Interview"),
        ("0", "Offer"),
    ]


    for column, (number, label) in zip(
        [j1, j2, j3, j4, j5],
        job_items
    ):

        with column:

            st.markdown(
                f"""
                <div style="
                    text-align:center;
                    padding:1rem 0;
                ">

                    <div class="job-number">
                        {number}
                    </div>

                    <div class="job-label">
                        {label}
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )


    if st.button(
        "💼  Open Job Tracker",
        key="dashboard_jobs"
    ):

        navigate("jobs")


    # =====================================================
    # QUICK ACTIONS
    # =====================================================

    st.markdown(
        """
        <div class="section-heading">

            <div class="section-title">
                Quick Actions
            </div>

            <div class="section-description">
                Jump into DevTrack
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    q1, q2, q3, q4 = st.columns(4)


    # GitHub

    with q1:

        st.markdown(
            """
            <div class="quick-card">

                <div class="quick-icon">
                    💻
                </div>

                <div class="quick-title">
                    GitHub Analyzer
                </div>

                <div class="quick-text">
                    Analyze your profile
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button(
            "Open",
            key="quick_github",
            use_container_width=True
        ):

            navigate("github")


    # Skills

    with q2:

        st.markdown(
            """
            <div class="quick-card">

                <div class="quick-icon">
                    📚
                </div>

                <div class="quick-title">
                    Skills
                </div>

                <div class="quick-text">
                    Track your skills
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button(
            "Open",
            key="quick_skills",
            use_container_width=True
        ):

            navigate("skills")


    # Projects

    with q3:

        st.markdown(
            """
            <div class="quick-card">

                <div class="quick-icon">
                    🚀
                </div>

                <div class="quick-title">
                    Projects
                </div>

                <div class="quick-text">
                    Build your portfolio
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button(
            "Open",
            key="quick_projects",
            use_container_width=True
        ):

            navigate("projects")


    # Resume

    with q4:

        st.markdown(
            """
            <div class="quick-card">

                <div class="quick-icon">
                    📄
                </div>

                <div class="quick-title">
                    Resume
                </div>

                <div class="quick-text">
                    Improve your resume
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button(
            "Open",
            key="quick_resume",
            use_container_width=True
        ):

            navigate("resume")


    # =====================================================
    # FOOTER
    # =====================================================

    st.markdown(
        """
        <div class="dashboard-footer">
            DevTrack · Build. Track. Grow.
        </div>
        """,
        unsafe_allow_html=True
    )