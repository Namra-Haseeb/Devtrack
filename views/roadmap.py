import streamlit as st

from src.career import get_roadmap
from src.database import get_career_profile, get_user_by_id


# ============================================================
# STYLE
# ============================================================

def apply_style():
    st.markdown(
        """
        <style>
        .stApp {
            color: #0F172A !important;
        }

        h1, h2, h3, h4, h5, h6 {
            color: #0F172A !important;
        }

        p, label, span {
            color: #0F172A !important;
        }

        [data-testid="stCaptionContainer"] p {
            color: #0F172A !important;
        }

        [data-testid="stCheckbox"] label p {
            color: #0F172A !important;
        }

        [data-testid="stMetricLabel"] {
            color: #0F172A !important;
        }

        [data-testid="stMetricValue"] {
            color: #0F172A !important;
        }

        [data-testid="stExpander"] summary p {
            color: #0F172A !important;
        }

        [data-testid="stAlert"] p {
            color: #0F172A !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# USER ID
# ============================================================

def get_current_user_id():

    user_id = st.session_state.get("user_id")

    if user_id is not None:
        return user_id

    return st.session_state.get("current_user_id")


# ============================================================
# CAREER PROFILE
# ============================================================

def get_saved_profile():

    user_id = get_current_user_id()

    # Try user ID
    if user_id is not None:

        try:
            profile = get_career_profile(
                user_id=user_id
            )

            if profile:
                return profile

        except Exception:
            pass

    # Try GitHub username connected to account
    if user_id is not None:

        try:

            user = get_user_by_id(user_id)

            if user:

                github_username = user.get(
                    "github_username"
                )

                if github_username:

                    profile = get_career_profile(
                        username=github_username
                    )

                    if profile:
                        return profile

        except Exception:
            pass

    # Try session username
    github_username = st.session_state.get(
        "github_username"
    )

    if github_username:

        try:

            profile = get_career_profile(
                username=github_username
            )

            if profile:
                return profile

        except Exception:
            pass

    return None


# ============================================================
# ROLE NORMALIZATION
# ============================================================

def normalize_role(role):

    if not role:
        return ""

    role = str(role).strip()

    aliases = {
        "Java Developer": "Backend Java Developer",
        "Backend Developer": "Backend Java Developer",
        "Python Developer": "Backend Python Developer",
        "Fullstack Developer": "Full Stack Developer",
        "Full-Stack Developer": "Full Stack Developer",
        "Machine Learning Engineer": "ML Engineer",
    }

    return aliases.get(role, role)


# ============================================================
# CONVERT ANY WEEK FORMAT INTO SAFE FORMAT
# ============================================================

def convert_week(week, number):

    # --------------------------------------------------------
    # Dictionary
    # --------------------------------------------------------

    if isinstance(week, dict):

        title = week.get(
            "title",
            f"Week {number}"
        )

        description = week.get(
            "description",
            ""
        )

        tasks = week.get(
            "tasks",
            []
        )

        if isinstance(tasks, str):
            tasks = [tasks]

        elif isinstance(tasks, tuple):
            tasks = list(tasks)

        elif not isinstance(tasks, list):
            tasks = []

        return (
            str(title),
            str(description),
            [str(x) for x in tasks]
        )

    # --------------------------------------------------------
    # Tuple
    # --------------------------------------------------------

    if isinstance(week, tuple):

        values = list(week)

        if len(values) == 0:

            return (
                f"Week {number}",
                "",
                []
            )

        title = str(values[0])

        description = ""

        tasks = []

        if len(values) == 2:

            if isinstance(
                values[1],
                (list, tuple)
            ):

                tasks = list(values[1])

            else:

                description = str(values[1])

        elif len(values) >= 3:

            description = str(values[1])

            if isinstance(
                values[2],
                (list, tuple)
            ):

                tasks = list(values[2])

            else:

                tasks = [values[2]]

        return (
            title,
            description,
            [str(x) for x in tasks]
        )

    # --------------------------------------------------------
    # List
    # --------------------------------------------------------

    if isinstance(week, list):

        values = list(week)

        if len(values) == 0:

            return (
                f"Week {number}",
                "",
                []
            )

        title = str(values[0])

        description = ""

        tasks = []

        if len(values) == 2:

            if isinstance(
                values[1],
                (list, tuple)
            ):

                tasks = list(values[1])

            else:

                description = str(values[1])

        elif len(values) >= 3:

            description = str(values[1])

            if isinstance(
                values[2],
                (list, tuple)
            ):

                tasks = list(values[2])

            else:

                tasks = [values[2]]

        return (
            title,
            description,
            [str(x) for x in tasks]
        )

    # --------------------------------------------------------
    # String
    # --------------------------------------------------------

    if isinstance(week, str):

        return (
            f"Week {number}",
            "",
            [week]
        )

    # --------------------------------------------------------
    # Unknown
    # --------------------------------------------------------

    return (
        f"Week {number}",
        "",
        []
    )


# ============================================================
# MAIN ROADMAP
# ============================================================

def show_roadmap():

    apply_style()

    # --------------------------------------------------------
    # HEADER
    # --------------------------------------------------------

    st.title("🗺️ Learning Roadmap")

    st.caption(
        "Your personalized learning path based on "
        "your selected target role."
    )

    st.divider()

    # --------------------------------------------------------
    # PROFILE
    # --------------------------------------------------------

    profile = get_saved_profile()

    if not profile:

        st.warning(
            "No career profile was found for this account."
        )

        st.write(
            "Please open Career Profile, choose your "
            "target role, and save it first."
        )

        if st.button("👤 Open Career Profile"):

            st.session_state.page = "career_profile"

            st.rerun()

        return

    # --------------------------------------------------------
    # ROLE
    # --------------------------------------------------------

    if isinstance(profile, dict):

        role = profile.get(
            "target_role",
            ""
        )

    else:

        try:
            role = profile["target_role"]

        except Exception:
            role = ""

    role = normalize_role(role)

    if not role:

        st.warning(
            "No target role has been selected."
        )

        st.write(
            "Go to Career Profile and select "
            "the role you want to prepare for."
        )

        if st.button("👤 Choose Target Role"):

            st.session_state.page = "career_profile"

            st.rerun()

        return

    # --------------------------------------------------------
    # ROADMAP
    # --------------------------------------------------------

    raw_roadmap = get_roadmap(role)

    if not raw_roadmap:

        st.warning(
            f"No roadmap is available for {role}."
        )

        return

    # --------------------------------------------------------
    # NORMALIZE ROADMAP
    # --------------------------------------------------------

    roadmap = []

    for index, week in enumerate(raw_roadmap):

        converted = convert_week(
            week,
            index + 1
        )

        roadmap.append(converted)

    # --------------------------------------------------------
    # TARGET ROLE
    # --------------------------------------------------------

    st.subheader("🎯 Target Role")

    st.write(role)

    st.caption(
        "Your roadmap is generated from the target role "
        "saved in Career Profile."
    )

    st.divider()

    # --------------------------------------------------------
    # TOTAL TASKS
    # --------------------------------------------------------

    total_tasks = 0

    completed_tasks = 0

    for week_index, week_data in enumerate(
        roadmap
    ):

        title, description, tasks = week_data

        for task_index in range(len(tasks)):

            total_tasks += 1

            key = (
                f"roadmap_{role}_"
                f"{week_index}_"
                f"{task_index}"
            )

            if st.session_state.get(
                key,
                False
            ):

                completed_tasks += 1

    # --------------------------------------------------------
    # OVERALL PROGRESS
    # --------------------------------------------------------

    if total_tasks > 0:

        overall_progress = (
            completed_tasks / total_tasks
        )

    else:

        overall_progress = 0

    st.subheader("📊 Overall Progress")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Completed",
            completed_tasks
        )

    with col2:

        st.metric(
            "Remaining",
            total_tasks - completed_tasks
        )

    with col3:

        st.metric(
            "Progress",
            f"{overall_progress * 100:.0f}%"
        )

    st.progress(
        overall_progress
    )

    st.divider()

    # --------------------------------------------------------
    # WEEKS
    # --------------------------------------------------------

    st.subheader("📚 Your Learning Roadmap")

    for week_index, week_data in enumerate(
        roadmap
    ):

        # IMPORTANT:
        # week_data is ALWAYS a tuple created by
        # convert_week(), so we do NOT call .get()
        # on it.

        title = week_data[0]

        description = week_data[1]

        tasks = week_data[2]

        # ----------------------------------------------------
        # WEEK PROGRESS
        # ----------------------------------------------------

        week_completed = 0

        for task_index in range(
            len(tasks)
        ):

            key = (
                f"roadmap_{role}_"
                f"{week_index}_"
                f"{task_index}"
            )

            if st.session_state.get(
                key,
                False
            ):

                week_completed += 1

        if len(tasks) > 0:

            week_progress = (
                week_completed / len(tasks)
            )

        else:

            week_progress = 0

        # ----------------------------------------------------
        # WEEK EXPANDER
        # ----------------------------------------------------

        with st.expander(
            f"Week {week_index + 1}: "
            f"{title} "
            f"({week_completed}/{len(tasks)} completed)",
            expanded=(week_index == 0)
        ):

            if description:

                st.write(
                    description
                )

            st.progress(
                week_progress
            )

            if tasks:

                for task_index, task in enumerate(
                    tasks
                ):

                    key = (
                        f"roadmap_{role}_"
                        f"{week_index}_"
                        f"{task_index}"
                    )

                    st.checkbox(
                        task,
                        key=key
                    )

            else:

                st.info(
                    "No tasks available for this week."
                )

    # --------------------------------------------------------
    # COMPLETION
    # --------------------------------------------------------

    st.divider()

    if total_tasks > 0:

        if completed_tasks == total_tasks:

            st.success(
                "🎉 You completed the entire roadmap!"
            )

        elif completed_tasks > 0:

            st.info(
                f"You completed {completed_tasks} "
                f"of {total_tasks} tasks. Keep going!"
            )

        else:

            st.info(
                "Start with Week 1 and complete "
                "the tasks one by one."
            )

    # --------------------------------------------------------
    # SKILL GAP
    # --------------------------------------------------------

    st.divider()

    st.subheader("🔎 What's Next?")

    st.write(
        "Check your Skill Gap to see which skills "
        "you already have and which ones you should learn."
    )

    if st.button("📚 Open Skill Gap"):

        st.session_state.page = "skills"

        st.rerun()

