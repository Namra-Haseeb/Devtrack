import streamlit as st

from src.database import save_resume_data, get_resume_data


def show_resume():

    # =========================================================
    # PAGE HEADER
    # =========================================================

    st.title("📄 Resume Builder")
    st.write("Build and maintain your professional resume.")

    user_id = st.session_state.get("user_id")

    if not user_id:
        st.warning("Please login to manage your resume.")
        return

    # =========================================================
    # LOAD EXISTING DATA
    # =========================================================

    try:
        existing = get_resume_data(user_id)

    except TypeError:
        existing = get_resume_data()

    if not existing:
        existing = {}

    if not isinstance(existing, dict):
        try:
            existing = dict(existing)
        except Exception:
            existing = {}

    # =========================================================
    # PERSONAL INFORMATION
    # =========================================================

    st.header("👤 Personal Information")

    col1, col2 = st.columns(2)

    with col1:

        full_name = st.text_input(
            "Full Name",
            value=existing.get("full_name", ""),
            placeholder="Your full name",
        )

        email = st.text_input(
            "Email",
            value=existing.get("email", ""),
            placeholder="you@example.com",
        )

        phone = st.text_input(
            "Phone",
            value=existing.get("phone", ""),
            placeholder="+91 XXXXX XXXXX",
        )

    with col2:

        location = st.text_input(
            "Location",
            value=existing.get("location", ""),
            placeholder="Lucknow, India",
        )

        linkedin = st.text_input(
            "LinkedIn",
            value=existing.get("linkedin", ""),
            placeholder="LinkedIn profile URL",
        )

        github = st.text_input(
            "GitHub",
            value=existing.get("github", ""),
            placeholder="GitHub profile URL",
        )

    portfolio = st.text_input(
        "Portfolio Website",
        value=existing.get("portfolio", ""),
        placeholder="https://yourportfolio.com",
    )

    # =========================================================
    # PROFESSIONAL SUMMARY
    # =========================================================

    st.header("📝 Professional Summary")

    summary = st.text_area(
        "Summary",
        value=existing.get("summary", ""),
        height=130,
        placeholder=(
            "Write 2–4 lines describing your background, "
            "technical strengths, and career goals."
        ),
    )

    # =========================================================
    # EDUCATION
    # =========================================================

    st.header("🎓 Education")

    col1, col2 = st.columns(2)

    with col1:

        degree = st.text_input(
            "Degree",
            value=existing.get("degree", ""),
            placeholder="B.Tech Computer Science and Engineering",
        )

        university = st.text_input(
            "University",
            value=existing.get("university", ""),
            placeholder="Your University",
        )

    with col2:

        graduation_year = st.text_input(
            "Graduation Year",
            value=str(existing.get("graduation_year", "")),
            placeholder="2028",
        )

        cgpa = st.text_input(
            "CGPA",
            value=str(existing.get("cgpa", "")),
            placeholder="8.4",
        )

    education_details = st.text_area(
        "Education Details",
        value=existing.get("education_details", ""),
        height=100,
        placeholder=(
            "Relevant coursework, achievements, academic activities, etc."
        ),
    )

    # =========================================================
    # SKILLS
    # =========================================================

    st.header("💻 Skills")

    skills = st.text_area(
        "Technical Skills",
        value=existing.get("skills", ""),
        height=120,
        placeholder=(
            "Java, Python, SQL, JDBC, SQLite, Git, GitHub, "
            "Streamlit, Cloud Computing"
        ),
    )

    # =========================================================
    # EXPERIENCE
    # =========================================================

    st.header("💼 Experience")

    experience = st.text_area(
        "Experience",
        value=existing.get("experience", ""),
        height=170,
        placeholder=(
            "Company / Organization\n"
            "Role | Duration\n"
            "• Describe what you built or contributed to\n"
            "• Mention technologies used\n"
            "• Quantify results where possible"
        ),
    )

    # =========================================================
    # PROJECTS
    # =========================================================

    st.header("🚀 Projects")

    projects = st.text_area(
        "Projects",
        value=existing.get("projects", ""),
        height=200,
        placeholder=(
            "Project Name | Technologies\n"
            "• What the project does\n"
            "• Your contribution\n"
            "• Important technical features\n"
            "• GitHub link"
        ),
    )

    # =========================================================
    # ACHIEVEMENTS
    # =========================================================

    st.header("🏆 Achievements & Certifications")

    achievements = st.text_area(
        "Achievements",
        value=existing.get("achievements", ""),
        height=140,
        placeholder=(
            "• Hackathons\n"
            "• Certifications\n"
            "• Awards\n"
            "• Competition achievements\n"
            "• Leadership or technical accomplishments"
        ),
    )

    # =========================================================
    # SAVE RESUME
    # =========================================================

    st.divider()

    if st.button(
        "💾 Save Resume",
        type="primary",
        use_container_width=True,
    ):

        data = {
            "full_name": full_name,
            "email": email,
            "phone": phone,
            "location": location,
            "linkedin": linkedin,
            "github": github,
            "portfolio": portfolio,
            "summary": summary,
            "degree": degree,
            "university": university,
            "graduation_year": graduation_year,
            "cgpa": cgpa,
            "education_details": education_details,
            "skills": skills,
            "experience": experience,
            "projects": projects,
            "achievements": achievements,
        }

        try:

            save_resume_data(
                user_id=user_id,
                data=data,
            )

        except TypeError:

            save_resume_data(
                user_id,
                data,
            )

        st.success("Resume information saved successfully!")

        st.rerun()

    # =========================================================
    # RESUME PREVIEW
    # =========================================================

    st.divider()

    st.header("👀 Resume Preview")

    if not full_name:
        st.info("Fill in your information above to build your resume preview.")

    # ---------------------------------------------------------
    # NAME
    # ---------------------------------------------------------

    if full_name:
        st.title(full_name)
    else:
        st.subheader("Your Name")

    # ---------------------------------------------------------
    # CONTACT INFORMATION
    # ---------------------------------------------------------

    contact_parts = []

    if email:
        contact_parts.append(email)

    if phone:
        contact_parts.append(phone)

    if location:
        contact_parts.append(location)

    if contact_parts:
        st.write(" • ".join(contact_parts))

    links = []

    if linkedin:
        links.append(f"LinkedIn: {linkedin}")

    if github:
        links.append(f"GitHub: {github}")

    if portfolio:
        links.append(f"Portfolio: {portfolio}")

    if links:
        st.write(" | ".join(links))

    st.divider()

    # ---------------------------------------------------------
    # SUMMARY
    # ---------------------------------------------------------

    st.subheader("Professional Summary")

    if summary:
        st.write(summary)
    else:
        st.caption("Add your professional summary above.")

    # ---------------------------------------------------------
    # EDUCATION
    # ---------------------------------------------------------

    st.subheader("Education")

    education_title_parts = []

    if degree:
        education_title_parts.append(degree)

    if university:
        education_title_parts.append(university)

    if graduation_year:
        education_title_parts.append(graduation_year)

    if education_title_parts:
        st.write(" — ".join(education_title_parts))

    if cgpa:
        st.write(f"CGPA: {cgpa}")

    if education_details:
        st.write(education_details)

    if not education_title_parts and not education_details:
        st.caption("Add your education details above.")

    # ---------------------------------------------------------
    # SKILLS
    # ---------------------------------------------------------

    st.subheader("Skills")

    if skills:
        st.write(skills)
    else:
        st.caption("Add your technical skills above.")

    # ---------------------------------------------------------
    # EXPERIENCE
    # ---------------------------------------------------------

    st.subheader("Experience")

    if experience:
        st.write(experience)
    else:
        st.caption("Add your experience above.")

    # ---------------------------------------------------------
    # PROJECTS
    # ---------------------------------------------------------

    st.subheader("Projects")

    if projects:
        st.write(projects)
    else:
        st.caption("Add your projects above.")

    # ---------------------------------------------------------
    # ACHIEVEMENTS
    # ---------------------------------------------------------

    st.subheader("Achievements & Certifications")

    if achievements:
        st.write(achievements)
    else:
        st.caption("Add your achievements above.")

    # =========================================================
    # RESUME TIPS
    # =========================================================

    st.divider()

    st.info(
        """
💡 Resume Tips

• Keep your resume concise and achievement-focused.

• Mention technologies used in your projects.

• Add GitHub links to strong technical projects.

• Quantify achievements whenever possible.

• Keep your resume aligned with your target job role.
"""
    )