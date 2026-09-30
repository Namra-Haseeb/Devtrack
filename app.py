import streamlit as st

from src.database import (
    init_db,
    create_user,
    authenticate_user,
    get_user_by_id,
)

from views.github_profile import show_home, show_github_analyzer
from views.repo_analyzer import show_repo_analyzer
from views.roadmap import show_roadmap
from views.skill_gap import show_skill_gap
from views.projects import show_projects
from views.job_tracker import show_job_tracker
from views.goals import show_goals
from views.achievements import show_achievements
from views.resume import show_resume
from views.profile import show_profile
from views.career_profile import show_career_profile
from views.job_analyzer import show_job_analyzer


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="DevTrack",
    page_icon="D",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# DATABASE
# =========================================================

init_db()


# =========================================================
# SESSION STATE
# =========================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user_id" not in st.session_state:
    st.session_state.user_id = None

if "user" not in st.session_state:
    st.session_state.user = None

if "page" not in st.session_state:
    st.session_state.page = "Dashboard"

if "github_username" not in st.session_state:
    st.session_state.github_username = ""


# =========================================================
# GLOBAL CSS
# =========================================================

st.markdown(
    """
    <style>

    /* =====================================================
       GLOBAL
       ===================================================== */

    @import url(
        'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap'
    );

    html,
    body,
    [class*="css"] {
        font-family: "Inter", sans-serif;
    }


    /* =====================================================
       MAIN BACKGROUND
       DARK BLUE
            ↓
       BLUE
            ↓
       LIGHT BLUE
            ↓
       WHITE
       ===================================================== */

    .stApp {

        background:
            radial-gradient(
                circle at 5% 0%,
                rgba(56, 189, 248, 0.30),
                transparent 30%
            ),

            radial-gradient(
                circle at 95% 5%,
                rgba(14, 116, 144, 0.22),
                transparent 30%
            ),

            linear-gradient(
                180deg,
                #075985 0%,
                #0c4a6e 18%,
                #164e63 32%,
                #3b829d 48%,
                #9cc9d8 65%,
                #dceff5 82%,
                #ffffff 100%
            );

        background-attachment: fixed;
        min-height: 100vh;
    }


    /* =====================================================
       MAIN CONTAINER
       ===================================================== */

    .main .block-container {

        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1500px;
    }


    /* =====================================================
       HIDE STREAMLIT DEFAULT UI
       ===================================================== */

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    header[data-testid="stHeader"] {
        background: transparent;
    }


    /* =====================================================
       MAIN PAGE TEXT
       ===================================================== */

    .main h1,
    .main h2,
    .main h3,
    .main h4,
    .main h5,
    .main h6 {
        color: white !important;
    }

    .main p {
        color: rgba(255, 255, 255, 0.95) !important;
    }

    .main li {
        color: rgba(255, 255, 255, 0.95) !important;
    }

    .main .stMarkdown {
        color: white !important;
    }

    .main .stMarkdown p {
        color: rgba(255, 255, 255, 0.95) !important;
    }

    .main .stCaption,
    .main [data-testid="stCaptionContainer"] {
        color: rgba(255, 255, 255, 0.78) !important;
    }

    .main label {
        color: white !important;
    }

    .main [data-testid="stWidgetLabel"] {
        color: white !important;
    }

    .main [data-testid="stWidgetLabel"] p {
        color: white !important;
    }

    .main [data-testid="stMetricLabel"] {
        color: white !important;
    }

    .main [data-testid="stMetricValue"] {
        color: white !important;
    }


    /* =====================================================
       INPUTS
       ===================================================== */

    .main input,
    .main textarea {
        color: #0f172a !important;
        background: white !important;
    }

    .main input::placeholder,
    .main textarea::placeholder {
        color: #64748b !important;
    }


    /* =====================================================
       SELECT BOX
       ===================================================== */

    .main [data-baseweb="select"] {
        background: white !important;
        border-radius: 10px;
    }

    .main [data-baseweb="select"] * {
        color: #0f172a !important;
    }


    /* =====================================================
       STREAMLIT WHITE CONTAINERS
       ===================================================== */

    .main [data-testid="stVerticalBlockBorderWrapper"] {

        background: rgba(255, 255, 255, 0.96);

        border-color:
            rgba(255, 255, 255, 0.40);

        border-radius: 16px;
    }

    .main [data-testid="stVerticalBlockBorderWrapper"] h1,
    .main [data-testid="stVerticalBlockBorderWrapper"] h2,
    .main [data-testid="stVerticalBlockBorderWrapper"] h3,
    .main [data-testid="stVerticalBlockBorderWrapper"] h4,
    .main [data-testid="stVerticalBlockBorderWrapper"] h5,
    .main [data-testid="stVerticalBlockBorderWrapper"] h6 {

        color: #0f172a !important;
    }

    .main [data-testid="stVerticalBlockBorderWrapper"] p,
    .main [data-testid="stVerticalBlockBorderWrapper"] span,
    .main [data-testid="stVerticalBlockBorderWrapper"] li {

        color: #0f172a !important;
    }


    /* =====================================================
       GENERAL BUTTONS
       ===================================================== */

    .stButton > button {

        border-radius: 10px;

        font-weight: 600;
    }


    /* =====================================================
       GENERAL CARDS
       ===================================================== */

    .dt-card {

        background: white;

        border-radius: 18px;

        padding: 22px;

        border:
            1px solid rgba(148, 163, 184, 0.18);

        box-shadow:
            0 10px 30px rgba(15, 23, 42, 0.06);
    }

    .dt-card,
    .dt-card * {

        color: #0f172a !important;
    }


    /* =====================================================
       PAGE TITLES
       ===================================================== */

    .dt-page-title {

        font-size: 32px;

        font-weight: 800;

        color: white;
    }

    .dt-page-subtitle {

        font-size: 14px;

        color:
            rgba(255, 255, 255, 0.85);

        margin-top: 5px;
    }


    /* =====================================================
       AUTH COLUMN PANELS
       ===================================================== */

    [data-testid="column"]:has(.auth-logo-box) {

        background:
            linear-gradient(
                145deg,
                #064e73 0%,
                #075985 45%,
                #0284c7 75%,
                #38bdf8 100%
            );

        border-radius: 24px;

        padding: 42px !important;

        min-height: 650px;

        box-shadow:
            0 25px 70px
            rgba(15, 23, 42, 0.12);
    }


    [data-testid="column"]:has(.auth-form-title) {

        background: white;

        border-radius: 24px;

        padding: 42px !important;

        min-height: 650px;

        box-shadow:
            0 25px 70px
            rgba(15, 23, 42, 0.12);
    }


    /* =====================================================
       AUTH LEFT SIDE
       ===================================================== */

    .auth-logo-box {

        width: 62px;

        height: 62px;

        border-radius: 17px;

        background: white;

        color: #0284c7;

        display: flex;

        align-items: center;

        justify-content: center;

        font-size: 34px;

        font-weight: 800;

        margin-bottom: 18px;

        box-shadow:
            0 12px 30px
            rgba(0, 0, 0, 0.15);
    }


    .auth-brand {

        font-size: 38px;

        font-weight: 800;

        line-height: 1.1;

        color: #38bdf8;

        margin-bottom: 7px;
    }


    .auth-tagline {

        font-size: 15px;

        color: #38bdf8;
    }


    .auth-message-title {

        font-size: 27px;

        line-height: 1.3;

        font-weight: 700;

        color: #38bdf8;

        margin-top: 145px;

        margin-bottom: 18px;
    }


    .auth-message-text {

        font-size: 14px;

        line-height: 1.75;

        color: #38bdf8;

        margin-bottom: 25px;
    }


    .auth-feature {

        font-size: 14px;

        font-weight: 500;

        color: #38bdf8;

        margin: 13px 0;
    }


    /* =====================================================
       AUTH RIGHT SIDE
       ===================================================== */

    .auth-form-title {

        font-size: 29px;

        font-weight: 800;

        color: #0f172a;

        margin-bottom: 6px;
    }


    .auth-form-subtitle {

        font-size: 14px;

        color: #64748b;

        margin-bottom: 25px;
    }


    .auth-right-space {
        height: 5px;
    }


    /* =====================================================
       AUTH INPUTS
       ===================================================== */

    [data-testid="column"]:has(.auth-form-title)
    .stTextInput input {

        height: 46px;

        border-radius: 10px;

        border:
            1px solid #cbd5e1;

        background: white;

        color: #0f172a;
    }


    [data-testid="column"]:has(.auth-form-title)
    .stTextInput input:focus {

        border-color: #0284c7;

        box-shadow:
            0 0 0 1px #0284c7;
    }


    [data-testid="column"]:has(.auth-form-title)
    .stButton > button {

        height: 46px;

        border-radius: 10px;

        font-weight: 700;
    }


    [data-testid="column"]:has(.auth-form-title)
    .stTabs [data-baseweb="tab-list"] {

        background: #f1f5f9;

        border-radius: 11px;

        padding: 4px;

        gap: 4px;
    }


    [data-testid="column"]:has(.auth-form-title)
    .stTabs [data-baseweb="tab"] {

        border-radius: 8px;

        padding: 9px 18px;
    }


    /* =====================================================
       SIDEBAR
       ===================================================== */

    section[data-testid="stSidebar"] {

        background:
            linear-gradient(
                180deg,
                #064e73 0%,
                #075985 45%,
                #0369a1 75%,
                #0284c7 100%
            );
    }


    section[data-testid="stSidebar"] * {
        color: white;
    }


    .sidebar-logo {

        width: 42px;

        height: 42px;

        border-radius: 12px;

        background: white;

        color: #0284c7;

        display: flex;

        align-items: center;

        justify-content: center;

        font-size: 24px;

        font-weight: 800;

        margin-bottom: 12px;
    }


    .sidebar-title {

        font-size: 23px;

        font-weight: 800;

        color: white;
    }


    .sidebar-subtitle {

        font-size: 12px;

        color:
            rgba(255, 255, 255, 0.70);
    }


    .sidebar-section {

        font-size: 10px;

        font-weight: 700;

        letter-spacing: 1.2px;

        color:
            rgba(255, 255, 255, 0.55);

        margin: 22px 0 8px 0;
    }


    /* =====================================================
       SIDEBAR BUTTONS
       ===================================================== */

    section[data-testid="stSidebar"]
    .stButton > button {

        color: white !important;

        background: transparent;

        border: none;

        text-align: left;

        border-radius: 10px;
    }


    section[data-testid="stSidebar"]
    .stButton > button:hover {

        background:
            rgba(255, 255, 255, 0.12);

        color: white !important;
    }


    /* =====================================================
       SIDEBAR SELECT
       ===================================================== */

    section[data-testid="stSidebar"]
    [data-baseweb="select"] {

        background:
            rgba(255, 255, 255, 0.10) !important;
    }


    section[data-testid="stSidebar"]
    [data-baseweb="select"] * {

        color: white !important;
    }


    /* =====================================================
       SCROLLBAR
       ===================================================== */

    ::-webkit-scrollbar {
        width: 8px;
    }

    ::-webkit-scrollbar-track {
        background:
            rgba(255, 255, 255, 0.15);
    }

    ::-webkit-scrollbar-thumb {

        background:
            rgba(7, 89, 133, 0.65);

        border-radius: 10px;
    }

    ::-webkit-scrollbar-thumb:hover {

        background:
            rgba(7, 89, 133, 0.85);
    }


    /* =====================================================
       RESPONSIVE
       ===================================================== */

    @media (max-width: 900px) {

        [data-testid="column"]:has(.auth-logo-box),
        [data-testid="column"]:has(.auth-form-title) {

            min-height: auto;

            padding: 30px !important;

            border-radius: 20px;
        }


        .auth-message-title {

            margin-top: 70px;

            font-size: 23px;
        }


        .auth-brand {

            font-size: 32px;
        }


        .auth-form-title {

            font-size: 25px;
        }
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# AUTHENTICATION PAGE
# =========================================================

def show_auth():

    left_column, right_column = st.columns(
        [1.05, 0.95],
        gap="medium"
    )


    # =====================================================
    # LEFT PANEL
    # =====================================================

    with left_column:

        st.markdown(
            """
            <div class="auth-logo-box">
                D
            </div>

            <div class="auth-brand">
                DevTrack
            </div>

            <div class="auth-tagline">
                Build. Track. Grow.
            </div>
            """,
            unsafe_allow_html=True
        )


        st.markdown(
            """
            <div class="auth-message-title">
                Turn your developer journey
                into measurable progress.
            </div>

            <div class="auth-message-text">
                DevTrack brings your GitHub activity,
                skills, projects, job applications,
                goals and career preparation into
                one focused workspace.
            </div>

            <div class="auth-feature">
                ✓ Analyze your GitHub profile
            </div>

            <div class="auth-feature">
                ✓ Find your skill gaps
            </div>

            <div class="auth-feature">
                ✓ Follow a role-based roadmap
            </div>

            <div class="auth-feature">
                ✓ Track projects and applications
            </div>

            <div class="auth-feature">
                ✓ Build your resume
            </div>
            """,
            unsafe_allow_html=True
        )


    # =====================================================
    # RIGHT PANEL
    # =====================================================

    with right_column:

        st.markdown(
            """
            <div class="auth-form-title">
                Welcome to DevTrack
            </div>

            <div class="auth-form-subtitle">
                Your developer growth workspace.
            </div>
            """,
            unsafe_allow_html=True
        )


        login_tab, signup_tab = st.tabs(
            ["Login", "Create Account"]
        )


        # =================================================
        # LOGIN
        # =================================================

        with login_tab:

            st.write("")

            login_email = st.text_input(
                "Email",
                placeholder="you@example.com",
                key="login_email"
            )


            login_password = st.text_input(
                "Password",
                type="password",
                placeholder="Enter your password",
                key="login_password"
            )


            st.write("")


            if st.button(
                "Login to DevTrack",
                use_container_width=True,
                type="primary",
                key="login_button"
            ):

                if not login_email or not login_password:

                    st.error(
                        "Please enter your email and password."
                    )

                else:

                    try:

                        user = authenticate_user(
                            login_email.strip(),
                            login_password
                        )


                        if user:

                            if isinstance(user, dict):

                                st.session_state.user = user

                                st.session_state.user_id = (
                                    user.get("id")
                                )

                            else:

                                st.session_state.user_id = user

                                st.session_state.user = (
                                    get_user_by_id(user)
                                )


                            st.session_state.logged_in = True

                            st.session_state.page = "Dashboard"

                            st.rerun()


                        else:

                            st.error(
                                "Invalid email or password."
                            )


                    except Exception as e:

                        st.error(
                            f"Login error: {e}"
                        )


        # =================================================
        # SIGN UP
        # =================================================

        with signup_tab:

            st.write("")


            signup_name = st.text_input(
                "Full Name",
                placeholder="Your name",
                key="signup_name"
            )


            signup_email = st.text_input(
                "Email",
                placeholder="you@example.com",
                key="signup_email"
            )


            signup_password = st.text_input(
                "Password",
                type="password",
                placeholder="Create a password",
                key="signup_password"
            )


            signup_confirm = st.text_input(
                "Confirm Password",
                type="password",
                placeholder="Confirm your password",
                key="signup_confirm"
            )


            st.write("")


            if st.button(
                "Create DevTrack Account",
                use_container_width=True,
                type="primary",
                key="signup_button"
            ):

                if (
                    not signup_name
                    or not signup_email
                    or not signup_password
                ):

                    st.error(
                        "Please fill in all required fields."
                    )


                elif signup_password != signup_confirm:

                    st.error(
                        "Passwords do not match."
                    )


                elif len(signup_password) < 6:

                    st.error(
                        "Password must contain at least 6 characters."
                    )


                else:

                    try:

                        result = create_user(
                            signup_name.strip(),
                            signup_email.strip(),
                            signup_password
                        )


                        if result:

                            st.success(
                                "Account created successfully."
                            )

                            st.info(
                                "Go to the Login tab to sign in."
                            )


                        else:

                            st.error(
                                "An account with this email "
                                "may already exist."
                            )


                    except Exception as e:

                        st.error(
                            f"Signup error: {e}"
                        )


# =========================================================
# SIDEBAR
# =========================================================

def show_sidebar():

    with st.sidebar:

        st.markdown(
            '<div class="sidebar-logo">D</div>',
            unsafe_allow_html=True
        )


        st.markdown(
            '<div class="sidebar-title">DevTrack</div>',
            unsafe_allow_html=True
        )


        st.markdown(
            '<div class="sidebar-subtitle">Developer Growth Platform</div>',
            unsafe_allow_html=True
        )


        # =================================================
        # MAIN
        # =================================================

        st.markdown(
            '<div class="sidebar-section">MAIN</div>',
            unsafe_allow_html=True
        )


        if st.button(
            "🏠  Dashboard",
            use_container_width=True,
            key="nav_dashboard"
        ):

            st.session_state.page = "Dashboard"
            st.rerun()


        # =================================================
        # DEVELOPMENT
        # =================================================

        st.markdown(
            '<div class="sidebar-section">DEVELOPMENT</div>',
            unsafe_allow_html=True
        )


        if st.button(
            "💻  GitHub",
            use_container_width=True,
            key="nav_github"
        ):

            st.session_state.page = "GitHub"
            st.rerun()


        if st.button(
            "📦  Repositories",
            use_container_width=True,
            key="nav_repositories"
        ):

            st.session_state.page = "Repositories"
            st.rerun()


        if st.button(
            "🗺️  Roadmap",
            use_container_width=True,
            key="nav_roadmap"
        ):

            st.session_state.page = "Roadmap"
            st.rerun()


        if st.button(
            "📚  Skills",
            use_container_width=True,
            key="nav_skills"
        ):

            st.session_state.page = "Skills"
            st.rerun()


        if st.button(
            "🚀  Projects",
            use_container_width=True,
            key="nav_projects"
        ):

            st.session_state.page = "Projects"
            st.rerun()


        # =================================================
        # CAREER
        # =================================================

        st.markdown(
            '<div class="sidebar-section">CAREER</div>',
            unsafe_allow_html=True
        )


        if st.button(
            "💼  Jobs",
            use_container_width=True,
            key="nav_jobs"
        ):

            st.session_state.page = "Jobs"
            st.rerun()


        if st.button(
            "🎯  Goals",
            use_container_width=True,
            key="nav_goals"
        ):

            st.session_state.page = "Goals"
            st.rerun()


        if st.button(
            "📄  Resume",
            use_container_width=True,
            key="nav_resume"
        ):

            st.session_state.page = "Resume"
            st.rerun()


        if st.button(
            "🏆  Achievements",
            use_container_width=True,
            key="nav_achievements"
        ):

            st.session_state.page = "Achievements"
            st.rerun()


        # =================================================
        # ACCOUNT
        # =================================================

        st.markdown(
            '<div class="sidebar-section">ACCOUNT</div>',
            unsafe_allow_html=True
        )


        if st.button(
            "👤  Profile",
            use_container_width=True,
            key="nav_profile"
        ):

            st.session_state.page = "Profile"
            st.rerun()


        if st.button(
            "⚙️  Career Profile",
            use_container_width=True,
            key="nav_career_profile"
        ):

            st.session_state.page = "Career Profile"
            st.rerun()


        if st.button(
            "📋  Job Analyzer",
            use_container_width=True,
            key="nav_job_analyzer"
        ):

            st.session_state.page = "Job Analyzer"
            st.rerun()


        # =================================================
        # LOGOUT
        # =================================================

        st.markdown("---")


        if st.button(
            "🚪  Logout",
            use_container_width=True,
            key="logout_button"
        ):

            st.session_state.logged_in = False
            st.session_state.user_id = None
            st.session_state.user = None
            st.session_state.page = "Dashboard"

            st.rerun()


# =========================================================
# PAGE ROUTER
# =========================================================

def route_page():

    page = st.session_state.page


    if page == "Dashboard":

        show_home()


    elif page == "GitHub":

        show_github_analyzer()


    elif page == "Repositories":

        show_repo_analyzer()


    elif page == "Roadmap":

        show_roadmap()


    elif page == "Skills":

        show_skill_gap()


    elif page == "Projects":

        show_projects()


    elif page == "Jobs":

        show_job_tracker()


    elif page == "Goals":

        show_goals()


    elif page == "Resume":

        show_resume()


    elif page == "Achievements":

        show_achievements()


    elif page == "Profile":

        show_profile()


    elif page == "Career Profile":

        show_career_profile()


    elif page == "Job Analyzer":

        show_job_analyzer()


    else:

        st.session_state.page = "Dashboard"

        show_home()


# =========================================================
# APPLICATION START
# =========================================================

if st.session_state.logged_in:

    show_sidebar()

    route_page()

else:

    show_auth()