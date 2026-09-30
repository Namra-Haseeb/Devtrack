import streamlit as st

from src.database import (
    get_career_profile,
    save_career_profile,
    get_user_by_id,
    update_user_github_username,
)

from src.career import (
    get_available_roles,
    get_role_description,
    get_role_skills,
    analyze_skill_gap,
    get_skill_recommendation,
    calculate_role_readiness,
)


# ============================================================
# Helpers
# ============================================================

def get_current_user_id():
    return st.session_state.get("user_id")


def get_saved_profile(user_id):
    """
    Get the user's career profile.

    First try user_id because this is the safest lookup.
    Then fall back to GitHub username for older records.
    """

    profile = None

    if user_id:
        try:
            profile = get_career_profile(user_id=user_id)
        except Exception:
            profile = None

    if profile:
        return profile

    github_username = st.session_state.get("github_username")

    if not github_username and user_id:

        try:
            user = get_user_by_id(user_id)

            if user:
                github_username = (
                    user.get("github_username")
                    or user.get("username")
                )

        except Exception:
            github_username = None

    if github_username:

        try:
            profile = get_career_profile(
                username=github_username
            )
        except Exception:
            profile = None

    return profile


def normalize_role_name(role):
    """
    Keep compatibility with older saved role names.
    """

    if not role:
        return ""

    role = role.strip()

    aliases = {
        "Java Developer": "Backend Java Developer",
        "Backend Developer": "Backend Java Developer",
        "Python Developer": "Backend Python Developer",
        "Full Stack": "Full Stack Developer",
        "Data Scientist": "Data Analyst",
        "ML Engineer": "ML Engineer",
        "Cloud Engineer": "Cloud Engineer",
        "Frontend Developer": "Frontend Developer",
    }

    return aliases.get(role, role)


def get_profile_skills(profile):
    """
    Safely extract skills from the saved profile.
    """

    if not profile:
        return []

    technologies = profile.get(
        "target_technologies",
        []
    )

    if technologies is None:
        return []

    if isinstance(technologies, str):

        if not technologies.strip():
            return []

        return [
            item.strip()
            for item in technologies.split(",")
            if item.strip()
        ]

    if isinstance(technologies, (list, tuple, set)):

        return [
            str(item).strip()
            for item in technologies
            if str(item).strip()
        ]

    return []


# ============================================================
# Recommendation helper
# ============================================================

def render_recommendations(missing_skills):
    """
    Render recommendations safely.

    get_skill_recommendation() can return a string.
    Do NOT assume recommendation is a dictionary.
    """

    st.subheader("Recommended next skills")

    if not missing_skills:

        st.success(
            "You currently have all the core skills "
            "listed for this role."
        )

        return

    recommendations = []

    for skill in missing_skills:

        try:
            recommendation = get_skill_recommendation(
                skill
            )
        except Exception:
            recommendation = None

        if isinstance(recommendation, str):

            recommendation_text = recommendation.strip()

        elif isinstance(recommendation, dict):

            recommendation_text = (
                recommendation.get("description")
                or recommendation.get("recommendation")
                or recommendation.get("text")
                or ""
            )

        else:

            recommendation_text = ""

        recommendations.append(
            (
                skill,
                recommendation_text
            )
        )

    for skill, recommendation_text in recommendations:

        with st.container(border=True):

            st.markdown(
                f"### 📚 {skill}"
            )

            if recommendation_text:

                st.write(
                    recommendation_text
                )

            else:

                st.write(
                    f"Focus on learning and practicing "
                    f"{skill}."
                )


# ============================================================
# Skill readiness
# ============================================================

def render_skill_readiness(
    role,
    known_skills,
):
    """
    Display role readiness using the current career helpers.
    """

    if not role:
        return

    required_skills = get_role_skills(role)

    if not required_skills:
        st.warning(
            "No skill requirements are available "
            "for this role yet."
        )
        return

    if not known_skills:
        known_skills = []

    gap = analyze_skill_gap(
        required_skills,
        known_skills,
    )

    matched_skills = gap.get(
        "matched",
        []
    )

    missing_skills = gap.get(
        "missing",
        []
    )

    total_required = len(
        required_skills
    )

    if total_required > 0:

        readiness = round(
            (
                len(matched_skills)
                / total_required
            )
            * 100
        )

    else:

        readiness = 0

    # --------------------------------------------------------
    # Readiness header
    # --------------------------------------------------------

    st.divider()

    st.subheader("🎯 Your starting point")

    st.metric(
        "Role readiness",
        f"{readiness}%",
    )

    st.progress(
        readiness / 100
    )

    # --------------------------------------------------------
    # Skill counts
    # --------------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Skills you have",
            len(matched_skills),
        )

    with col2:

        st.metric(
            "Skills to learn",
            len(missing_skills),
        )

    # --------------------------------------------------------
    # Skills already known
    # --------------------------------------------------------

    if matched_skills:

        st.subheader(
            "✅ Skills you already have"
        )

        st.write(
            ", ".join(
                str(skill)
                for skill in matched_skills
            )
        )

    # --------------------------------------------------------
    # Missing skills
    # --------------------------------------------------------

    if missing_skills:

        st.subheader(
            "📌 Skills you need to learn"
        )

        st.write(
            ", ".join(
                str(skill)
                for skill in missing_skills
            )
        )

    # --------------------------------------------------------
    # Recommendations
    # --------------------------------------------------------

    render_recommendations(
        missing_skills
    )


# ============================================================
# Main Career Profile page
# ============================================================

def show_career_profile():

    st.title("Career Profile")

    st.write(
        "Define where you want to go and let DevTrack "
        "build your development path around it."
    )

    user_id = get_current_user_id()

    if not user_id:

        st.warning(
            "Please login to create your career profile."
        )

        return

    profile = get_saved_profile(
        user_id
    )

    # --------------------------------------------------------
    # Existing values
    # --------------------------------------------------------

    existing_role = ""

    existing_experience = ""

    existing_technologies = []

    existing_bio = ""

    existing_company = ""

    existing_github = ""

    if profile:

        existing_role = normalize_role_name(
            profile.get(
                "target_role",
                ""
            )
        )

        existing_experience = profile.get(
            "experience_level",
            ""
        )

        existing_technologies = get_profile_skills(
            profile
        )

        existing_bio = profile.get(
            "bio",
            ""
        )

        existing_company = profile.get(
            "target_company",
            ""
        )

        existing_github = profile.get(
            "github_username",
            ""
        )

        if not existing_github:

            existing_github = profile.get(
                "username",
                ""
            )

    # --------------------------------------------------------
    # Role list
    # --------------------------------------------------------

    try:

        available_roles = get_available_roles()

    except Exception:

        available_roles = [
            "Backend Java Developer",
            "Backend Python Developer",
            "Full Stack Developer",
            "Data Analyst",
            "ML Engineer",
            "Cloud Engineer",
            "Frontend Developer",
        ]

    available_roles = [
        normalize_role_name(role)
        for role in available_roles
    ]

    available_roles = list(
        dict.fromkeys(
            available_roles
        )
    )

    role_options = [
        "Select a target role..."
    ] + available_roles

    if existing_role in available_roles:

        default_role_index = (
            role_options.index(
                existing_role
            )
        )

    else:

        default_role_index = 0

    # --------------------------------------------------------
    # Career direction form
    # --------------------------------------------------------

    st.subheader(
        "Define your career direction"
    )

    st.write(
        "DevTrack uses this information to personalize "
        "your skills, roadmap and job analysis."
    )

    target_role = st.selectbox(
        "Target Role",
        role_options,
        index=default_role_index,
    )

    experience_options = [
        "Entry Level",
        "Intermediate",
        "Advanced",
    ]

    if existing_experience in experience_options:

        experience_index = (
            experience_options.index(
                existing_experience
            )
        )

    else:

        experience_index = 0

    experience_level = st.selectbox(
        "Experience Level",
        experience_options,
        index=experience_index,
    )

    technology_options = [
        "Java",
        "Python",
        "Spring Boot",
        "SQL",
        "REST APIs",
        "Git",
        "Data Structures",
        "PostgreSQL",
        "Docker",
        "AWS",
        "React",
        "JavaScript",
        "TypeScript",
        "Machine Learning",
        "Pandas",
        "NumPy",
        "Power BI",
    ]

    selected_technologies = st.multiselect(
        "Technologies you already know",
        technology_options,
        default=[
            tech
            for tech in existing_technologies
            if tech in technology_options
        ],
    )

    bio = st.text_area(
        "Short Bio",
        value=existing_bio,
        placeholder=(
            "Example: B.Tech CSE student interested "
            "in backend development and cloud computing."
        ),
    )

    target_company = st.text_input(
        "Target Company",
        value=existing_company,
        placeholder=(
            "Optional — example: Microsoft, "
            "Flipkart, EY"
        ),
    )

    github_username = st.text_input(
        "GitHub Username",
        value=existing_github,
        placeholder="Optional",
    )

    st.caption(
        "You can save your career profile even if "
        "you haven't connected GitHub yet."
    )

    save_button = st.button(
        "💾 Save Career Profile",
        type="primary",
        use_container_width=True,
    )

    if save_button:

        if target_role == "Select a target role...":

            st.error(
                "Please select a target role before saving."
            )

        else:

            clean_github_username = (
                github_username.strip()
            )

            # ----------------------------------------------
            # Save GitHub username
            # ----------------------------------------------

            if clean_github_username:

                try:

                    update_user_github_username(
                        user_id,
                        clean_github_username,
                    )

                    st.session_state[
                        "github_username"
                    ] = clean_github_username

                except Exception:
                    pass

            # ----------------------------------------------
            # Save career profile
            # ----------------------------------------------

            save_career_profile(
                github_username=(
                    clean_github_username
                    if clean_github_username
                    else None
                ),
                target_role=target_role,
                experience_level=experience_level,
                target_technologies=(
                    selected_technologies
                ),
                user_id=user_id,
                bio=bio.strip(),
                target_company=target_company.strip(),
            )

            # ----------------------------------------------
            # Verify saved profile
            # ----------------------------------------------

            profile = get_saved_profile(
                user_id
            )

            if profile:

                st.success(
                    "Career profile saved successfully!"
                )

            else:

                st.warning(
                    "The profile was submitted, but "
                    "DevTrack could not immediately reload it."
                )

    # --------------------------------------------------------
    # Stop here if no valid role
    # --------------------------------------------------------

    current_role = normalize_role_name(
        target_role
        if target_role != "Select a target role..."
        else existing_role
    )

    if not current_role:

        st.info(
            "Select a target role above to see your "
            "personalized career direction and readiness."
        )

        return

    # --------------------------------------------------------
    # Target role
    # --------------------------------------------------------

    st.divider()

    st.subheader(
        "🎯 Your Target"
    )

    st.header(
        current_role
    )

    role_description = get_role_description(
        current_role
    )

    if role_description:

        st.write(
            role_description
        )

    # --------------------------------------------------------
    # Core skills
    # --------------------------------------------------------

    st.subheader(
        "Core skills for this role"
    )

    role_skills = get_role_skills(
        current_role
    )

    if role_skills:

        st.write(
            " • ".join(
                str(skill)
                for skill in role_skills
            )
        )

    # --------------------------------------------------------
    # Readiness
    # --------------------------------------------------------

    known_skills = list(
        selected_technologies
    )

    # Also include skills stored in profile.
    for skill in existing_technologies:

        if skill not in known_skills:

            known_skills.append(
                skill
            )

    render_skill_readiness(
        current_role,
        known_skills,
    )

    # --------------------------------------------------------
    # Footer
    # --------------------------------------------------------

    st.divider()

    st.caption(
        "DevTrack uses your selected role and skills "
        "to personalize your development roadmap."
    )