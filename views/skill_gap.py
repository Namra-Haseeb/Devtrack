import streamlit as st

from src.career import (
    get_role_skills,
    get_role_description,
    analyze_skill_gap,
    combine_skills,
    get_skill_recommendation,
)

from src.database import (
    get_career_profile,
    get_user_by_id,
)


# ============================================================
# PAGE STYLE
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
            color: #0F172A;
        }

        [data-testid="stMetricLabel"] {
            color: #0F172A !important;
        }

        [data-testid="stMetricValue"] {
            color: #0F172A !important;
        }

        [data-testid="stCaptionContainer"] p {
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
# CURRENT USER
# ============================================================

def get_current_user_id():

    return (
        st.session_state.get("user_id")
        or st.session_state.get("current_user_id")
    )


# ============================================================
# CAREER PROFILE
# ============================================================

def get_saved_profile():

    user_id = get_current_user_id()

    # --------------------------------------------------------
    # 1. User ID
    # --------------------------------------------------------

    if user_id is not None:

        try:

            profile = get_career_profile(
                user_id=user_id
            )

            if profile:
                return profile

        except Exception:
            pass

    # --------------------------------------------------------
    # 2. GitHub username from user account
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # 3. Session username
    # --------------------------------------------------------

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

def normalize_role_name(role):

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
# SAFE LIST
# ============================================================

def safe_list(value):

    if value is None:
        return []

    if isinstance(value, list):
        return value

    if isinstance(value, tuple):
        return list(value)

    if isinstance(value, set):
        return list(value)

    if isinstance(value, str):

        if not value.strip():
            return []

        return [value.strip()]

    return []


# ============================================================
# NORMALIZE RECOMMENDATION
# ============================================================

def normalize_recommendation(recommendation):

    # --------------------------------------------------------
    # String
    # --------------------------------------------------------

    if isinstance(recommendation, str):

        return {
            "skill": recommendation,
            "description": "",
            "priority": "",
        }

    # --------------------------------------------------------
    # Dictionary
    # --------------------------------------------------------

    if isinstance(recommendation, dict):

        skill = (
            recommendation.get("skill")
            or recommendation.get("name")
            or recommendation.get("title")
            or recommendation.get("technology")
            or "Recommended Skill"
        )

        description = (
            recommendation.get("description")
            or recommendation.get("reason")
            or recommendation.get("details")
            or ""
        )

        priority = (
            recommendation.get("priority")
            or recommendation.get("level")
            or ""
        )

        return {
            "skill": str(skill),
            "description": str(description),
            "priority": str(priority),
        }

    # --------------------------------------------------------
    # Tuple / List
    # --------------------------------------------------------

    if isinstance(recommendation, (tuple, list)):

        values = list(recommendation)

        if not values:
            return None

        skill = str(values[0])

        description = ""

        if len(values) > 1:
            description = str(values[1])

        priority = ""

        if len(values) > 2:
            priority = str(values[2])

        return {
            "skill": skill,
            "description": description,
            "priority": priority,
        }

    return None


# ============================================================
# MAIN PAGE
# ============================================================

def show_skill_gap():

    apply_style()

    # --------------------------------------------------------
    # HEADER
    # --------------------------------------------------------

    st.title("📚 Skill Gap")

    st.caption(
        "See what skills you already have "
        "and what you should learn next."
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
            "Please open Career Profile, select your "
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
        role = profile.get("target_role", "")
    else:
        try:
            role = profile["target_role"]
        except Exception:
            role = ""

    role = normalize_role_name(role)

    if not role:

        st.warning(
            "No target role has been selected."
        )

        st.write(
            "Choose your target role in Career Profile "
            "before using Skill Gap."
        )

        if st.button("👤 Choose Target Role"):

            st.session_state.page = "career_profile"
            st.rerun()

        return

    # --------------------------------------------------------
    # ROLE INFORMATION
    # --------------------------------------------------------

    st.subheader("🎯 Target Role")

    st.write(role)

    description = get_role_description(role)

    if description:

        st.caption(description)

    st.divider()

    # --------------------------------------------------------
    # REQUIRED SKILLS
    # --------------------------------------------------------

    required_skills = safe_list(
        get_role_skills(role)
    )

    # --------------------------------------------------------
    # PROFILE SKILLS
    # --------------------------------------------------------

    profile_skills = []

    if isinstance(profile, dict):

        profile_skills = safe_list(
            profile.get("target_technologies", [])
        )

    # --------------------------------------------------------
    # SESSION GITHUB SKILLS
    # --------------------------------------------------------

    github_skills = safe_list(
        st.session_state.get(
            "github_skills",
            []
        )
    )

    # --------------------------------------------------------
    # COMBINE
    # --------------------------------------------------------

    combined_skills = combine_skills(
        profile_skills,
        github_skills
    )

    combined_skills = safe_list(
        combined_skills
    )

    # --------------------------------------------------------
    # SKILLS
    # --------------------------------------------------------

    st.subheader("🧠 Your Skills")

    st.write(
        "Skills currently connected to your DevTrack profile:"
    )

    if combined_skills:

        skill_columns = st.columns(
            min(len(combined_skills), 4)
        )

        for index, skill in enumerate(
            combined_skills
        ):

            with skill_columns[
                index % len(skill_columns)
            ]:

                st.info(str(skill))

    else:

        st.info(
            "No skills have been added yet."
        )

    st.divider()

    # --------------------------------------------------------
    # ROLE READINESS
    # --------------------------------------------------------

    gap = analyze_skill_gap(
        required_skills,
        combined_skills
    )

    if not isinstance(gap, dict):

        gap = {}

    matched_skills = safe_list(
        gap.get("matched", [])
    )

    missing_skills = safe_list(
        gap.get("missing", [])
    )

    readiness = gap.get(
        "readiness",
        gap.get(
            "score",
            0
        )
    )

    try:
        readiness = float(readiness)
    except Exception:
        readiness = 0

    # --------------------------------------------------------
    # READINESS
    # --------------------------------------------------------

    st.subheader("📊 Role Readiness")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Readiness",
            f"{readiness:.0f}%"
        )

    with col2:
        st.metric(
            "Skills Required",
            len(required_skills)
        )

    with col3:
        st.metric(
            "Skills You Have",
            len(matched_skills)
        )

    with col4:
        st.metric(
            "Skills To Learn",
            len(missing_skills)
        )

    st.progress(
        min(max(readiness / 100, 0), 1)
    )

    st.divider()

    # --------------------------------------------------------
    # SKILLS YOU HAVE
    # --------------------------------------------------------

    st.subheader("✅ Skills You Have")

    if matched_skills:

        for skill in matched_skills:
            st.success(str(skill))

    else:

        st.info(
            "None of the core skills for this role "
            "have been matched yet."
        )

    # --------------------------------------------------------
    # SKILLS TO LEARN
    # --------------------------------------------------------

    st.subheader("📚 Skills To Learn")

    if missing_skills:

        for skill in missing_skills:

            st.warning(str(skill))

    else:

        st.success(
            "You currently match all core skills "
            "for this role."
        )

    # --------------------------------------------------------
    # RECOMMENDATIONS
    # --------------------------------------------------------

    st.divider()

    st.subheader("💡 Recommended Next Steps")

    try:

        recommendations = get_skill_recommendation(
            role,
            missing_skills
        )

    except TypeError:

        try:

            recommendations = get_skill_recommendation(
                missing_skills
            )

        except Exception:

            recommendations = []

    except Exception:

        recommendations = []

    recommendations = safe_list(
        recommendations
    )

    normalized_recommendations = []

    for recommendation in recommendations:

        normalized = normalize_recommendation(
            recommendation
        )

        if normalized:
            normalized_recommendations.append(
                normalized
            )

    if normalized_recommendations:

        for recommendation in normalized_recommendations:

            skill = recommendation["skill"]
            description = recommendation["description"]
            priority = recommendation["priority"]

            st.markdown(
                f"### 📘 {skill}"
            )

            if priority:
                st.write(
                    f"Priority: {priority}"
                )

            if description:
                st.write(description)

            st.divider()

    elif missing_skills:

        for skill in missing_skills:

            st.write(
                f"📘 Focus on **{skill}** next."
            )

    else:

        st.info(
            "Keep practicing your current skills "
            "and continue building projects."
        )

    # --------------------------------------------------------
    # ROADMAP
    # --------------------------------------------------------

    st.divider()

    st.subheader("🗺️ Learning Roadmap")

    st.write(
        "Follow the personalized roadmap for "
        f"{role}."
    )

    if st.button("🗺️ Open Learning Roadmap"):

        st.session_state.page = "roadmap"
        st.rerun()

