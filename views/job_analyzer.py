import streamlit as st

from src.database import get_career_profile
from src.career import (
    get_role_skills,
    analyze_skill_gap,
    extract_skills_from_jd,
    get_skill_recommendation,
)


# ============================================================
# Helpers
# ============================================================

def get_current_user_id():
    return st.session_state.get("user_id")


def get_saved_profile(user_id):
    """
    Safely load the current user's career profile.
    """

    if not user_id:
        return None

    try:
        profile = get_career_profile(
            user_id=user_id
        )

        if profile:
            return profile

    except Exception:
        pass

    return None


def get_profile_skills(profile):
    """
    Extract the user's saved technologies safely.
    """

    if not profile:
        return []

    skills = profile.get(
        "target_technologies",
        []
    )

    if skills is None:
        return []

    if isinstance(skills, str):

        return [
            skill.strip()
            for skill in skills.split(",")
            if skill.strip()
        ]

    if isinstance(skills, (list, tuple, set)):

        return [
            str(skill).strip()
            for skill in skills
            if str(skill).strip()
        ]

    return []


def normalize_skills(skills):
    """
    Convert skills into a clean list.
    """

    if not skills:
        return []

    cleaned = []

    for skill in skills:

        skill = str(skill).strip()

        if skill and skill not in cleaned:
            cleaned.append(skill)

    return cleaned


def render_skill_list(
    title,
    skills,
    empty_message,
):

    st.subheader(title)

    if not skills:

        st.info(
            empty_message
        )

        return

    for skill in skills:

        st.write(
            f"• {skill}"
        )


# ============================================================
# Main page
# ============================================================

def show_job_analyzer():

    # --------------------------------------------------------
    # Page heading
    # --------------------------------------------------------

    st.caption(
        "JOB DESCRIPTION ANALYZER"
    )

    st.title(
        "See how well you match a job"
    )

    st.write(
        "Paste a job description and DevTrack "
        "will compare its requirements with "
        "your current skills."
    )

    # --------------------------------------------------------
    # Login check
    # --------------------------------------------------------

    user_id = get_current_user_id()

    if not user_id:

        st.warning(
            "Please login to use the Job Description Analyzer."
        )

        return

    # --------------------------------------------------------
    # Career profile
    # --------------------------------------------------------

    profile = get_saved_profile(
        user_id
    )

    profile_skills = get_profile_skills(
        profile
    )

    target_role = ""

    if profile:

        target_role = profile.get(
            "target_role",
            ""
        )

    # --------------------------------------------------------
    # Job details
    # --------------------------------------------------------

    st.divider()

    st.caption(
        "JOB DETAILS"
    )

    job_title = st.text_input(
        "Job Title",
        placeholder=(
            "Example: Java Backend Developer Intern"
        ),
    )

    company = st.text_input(
        "Company",
        placeholder=(
            "Example: Flipkart"
        ),
    )

    job_description = st.text_area(
        "Job Description",
        height=300,
        placeholder=(
            "Paste the complete job description here...\n\n"
            "Example:\n"
            "We are looking for a Java developer with "
            "knowledge of Spring Boot, REST APIs, SQL, "
            "Git and Docker."
        ),
    )

    analyze_button = st.button(
        "🔍 Analyze Job Match",
        type="primary",
        use_container_width=True,
    )

    # --------------------------------------------------------
    # Analyze
    # --------------------------------------------------------

    if analyze_button:

        if not job_description.strip():

            st.error(
                "Please paste a job description first."
            )

            return

        # Extract skills from JD
        try:

            job_skills = extract_skills_from_jd(
                job_description
            )

        except Exception:

            job_skills = []

        job_skills = normalize_skills(
            job_skills
        )

        user_skills = normalize_skills(
            profile_skills
        )

        # ----------------------------------------------------
        # Match calculation
        # ----------------------------------------------------

        if job_skills:

            gap = analyze_skill_gap(
                job_skills,
                user_skills,
            )

            matched_skills = normalize_skills(
                gap.get(
                    "matched",
                    []
                )
            )

            missing_skills = normalize_skills(
                gap.get(
                    "missing",
                    []
                )
            )

            total_skills = len(
                job_skills
            )

            if total_skills:

                match_percentage = round(
                    (
                        len(matched_skills)
                        / total_skills
                    )
                    * 100
                )

            else:

                match_percentage = 0

        else:

            matched_skills = []

            missing_skills = []

            match_percentage = 0

        # ----------------------------------------------------
        # Save result in session
        # ----------------------------------------------------

        st.session_state[
            "job_analysis_result"
        ] = {
            "job_title": job_title.strip(),
            "company": company.strip(),
            "job_skills": job_skills,
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
            "match_percentage": match_percentage,
            "job_description": job_description.strip(),
            "target_role": target_role,
        }

        st.rerun()

    # ========================================================
    # Results
    # ========================================================

    result = st.session_state.get(
        "job_analysis_result"
    )

    if not result:

        st.divider()

        st.info(
            "↗ Your job match will appear here.\n\n"
            "Paste a job description above and click "
            "Analyze Job Match to see the skills you "
            "already have and the ones you should develop."
        )

        return

    # --------------------------------------------------------
    # Result header
    # --------------------------------------------------------

    st.divider()

    st.subheader(
        "📊 Job Match"
    )

    result_title = result.get(
        "job_title",
        ""
    )

    result_company = result.get(
        "company",
        ""
    )

    if result_title:

        st.write(
            f"**Role:** {result_title}"
        )

    if result_company:

        st.write(
            f"**Company:** {result_company}"
        )

    # --------------------------------------------------------
    # Match percentage
    # --------------------------------------------------------

    match_percentage = result.get(
        "match_percentage",
        0
    )

    st.metric(
        "Skill Match",
        f"{match_percentage}%",
    )

    st.progress(
        match_percentage / 100
    )

    # --------------------------------------------------------
    # Explanation
    # --------------------------------------------------------

    if match_percentage >= 80:

        st.success(
            "Most of the skills detected in this job "
            "description are already connected to your profile."
        )

    elif match_percentage >= 50:

        st.warning(
            "You have several matching skills, but there "
            "are still some important areas to develop."
        )

    else:

        st.info(
            "This job requires several skills that are "
            "not currently connected to your profile."
        )

    # --------------------------------------------------------
    # Three statistics
    # --------------------------------------------------------

    matched_skills = result.get(
        "matched_skills",
        []
    )

    missing_skills = result.get(
        "missing_skills",
        []
    )

    job_skills = result.get(
        "job_skills",
        []
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Skills Detected",
            len(job_skills),
        )

    with col2:

        st.metric(
            "Skills You Have",
            len(matched_skills),
        )

    with col3:

        st.metric(
            "Skills to Learn",
            len(missing_skills),
        )

    # --------------------------------------------------------
    # Matching skills
    # --------------------------------------------------------

    st.divider()

    render_skill_list(
        "✅ Skills You Have",
        matched_skills,
        "No matching skills were detected.",
    )

    # --------------------------------------------------------
    # Missing skills
    # --------------------------------------------------------

    st.divider()

    render_skill_list(
        "📚 Skills You Should Develop",
        missing_skills,
        "No additional skills were detected.",
    )

    # --------------------------------------------------------
    # Recommendations
    # --------------------------------------------------------

    if missing_skills:

        st.divider()

        st.subheader(
            "💡 Recommended Next Steps"
        )

        for skill in missing_skills:

            try:

                recommendation = (
                    get_skill_recommendation(
                        skill
                    )
                )

            except Exception:

                recommendation = None

            with st.container(
                border=True
            ):

                st.markdown(
                    f"**{skill}**"
                )

                if isinstance(
                    recommendation,
                    str
                ):

                    if recommendation.strip():

                        st.write(
                            recommendation.strip()
                        )

                    else:

                        st.write(
                            f"Start learning {skill} "
                            "through documentation, "
                            "guided practice and projects."
                        )

                elif isinstance(
                    recommendation,
                    dict
                ):

                    recommendation_text = (
                        recommendation.get(
                            "description"
                        )
                        or recommendation.get(
                            "recommendation"
                        )
                        or recommendation.get(
                            "text"
                        )
                    )

                    if recommendation_text:

                        st.write(
                            recommendation_text
                        )

                    else:

                        st.write(
                            f"Start learning {skill} "
                            "through documentation, "
                            "guided practice and projects."
                        )

                else:

                    st.write(
                        f"Start learning {skill} "
                        "through documentation, "
                        "guided practice and projects."
                    )

    # --------------------------------------------------------
    # Target role
    # --------------------------------------------------------

    saved_role = result.get(
        "target_role",
        ""
    )

    if saved_role:

        st.divider()

        st.subheader(
            "🎯 Your Career Direction"
        )

        st.write(
            f"Your current target role is **{saved_role}**."
        )

        st.caption(
            "This job analysis compares the job description "
            "with the skills currently stored in your "
            "Career Profile."
        )

    # --------------------------------------------------------
    # Reset analysis
    # --------------------------------------------------------

    st.divider()

    if st.button(
        "🔄 Analyze Another Job",
        use_container_width=True,
    ):

        st.session_state.pop(
            "job_analysis_result",
            None,
        )

        st.rerun()