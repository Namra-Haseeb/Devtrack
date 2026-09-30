import streamlit as st

from src.database import (
    get_achievements,
    add_achievement,
    delete_achievement,
)


def show_achievements():

    st.title("🏆 Keep track of what you've accomplished")

    st.write(
        "Store your certifications, hackathons, awards, internships "
        "and milestones in one professional portfolio."
    )

    user_id = st.session_state.get("user_id")

    if not user_id:
        st.warning("Please login to manage your achievements.")
        return

    achievements = get_achievements(user_id)

    if not achievements:
        achievements = []

    # -----------------------------
    # Statistics
    # -----------------------------

    total_achievements = len(achievements)

    categories = set()

    for achievement in achievements:
        category = achievement.get("category", "")

        if category:
            categories.add(category.strip())

    total_categories = len(categories)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Achievements",
            total_achievements,
            "Total milestones",
        )

    with col2:
        st.metric(
            "Categories",
            total_categories,
            "Achievement types",
        )

    with col3:
        st.metric(
            "Portfolio",
            "Active",
            "Your progress",
        )

    st.divider()

    # -----------------------------
    # Add Achievement
    # -----------------------------

    with st.expander("➕ Add an achievement"):

        title = st.text_input(
            "Achievement Title",
            placeholder="Example: Smart India Hackathon 2025",
        )

        category = st.selectbox(
            "Category",
            [
                "Certification",
                "Hackathon",
                "Award",
                "Internship",
                "Competition",
                "Course",
                "Milestone",
                "Other",
            ],
        )

        achievement_date = st.date_input(
            "Date"
        )

        description = st.text_area(
            "Description",
            height=120,
            placeholder=(
                "Describe what you achieved, your role, "
                "or what you learned."
            ),
        )

        proof_url = st.text_input(
            "Certificate / Proof Link",
            placeholder="Optional URL",
        )

        add_button = st.button(
            "Add Achievement",
            type="primary",
            use_container_width=True,
        )

        if add_button:

            if not title.strip():

                st.error(
                    "Please enter an achievement title."
                )

            else:

                add_achievement(
                    title=title.strip(),
                    category=category,
                    achievement_date=str(
                        achievement_date
                    ),
                    description=description.strip(),
                    proof_url=proof_url.strip(),
                    user_id=user_id,
                )

                st.success(
                    "Achievement added successfully!"
                )

                st.rerun()

    st.divider()

    # -----------------------------
    # Achievement List
    # -----------------------------

    st.subheader(
        "🏆 Achievements and accomplishments"
    )

    if not achievements:

        st.info(
            "🏆 Your achievements will appear here.\n\n"
            "Add hackathons, certifications, awards, "
            "internships and other accomplishments to "
            "build your professional history."
        )

    else:

        for achievement in achievements:

            achievement_id = achievement.get("id")

            title = achievement.get(
                "title",
                "Achievement",
            )

            category = achievement.get(
                "category",
                "Other",
            )

            achievement_date = achievement.get(
                "achievement_date",
                "",
            )

            description = achievement.get(
                "description",
                "",
            )

            proof_url = achievement.get(
                "proof_url",
                "",
            )

            with st.container(border=True):

                st.subheader(
                    f"🏆 {title}"
                )

                if category:
                    st.caption(
                        f"🏷️ {category}"
                    )

                if achievement_date:
                    st.caption(
                        f"📅 {achievement_date}"
                    )

                if description:
                    st.write(
                        description
                    )

                if proof_url:

                    st.link_button(
                        "🔗 View Proof",
                        proof_url,
                    )

                delete_button = st.button(
                    "🗑️ Delete",
                    key=(
                        f"delete_achievement_"
                        f"{achievement_id}"
                    ),
                )

                if delete_button:

                    delete_achievement(
                        achievement_id,
                        user_id,
                    )

                    st.success(
                        "Achievement deleted."
                    )

                    st.rerun()

    st.divider()

    # -----------------------------
    # Closing section
    # -----------------------------

    st.subheader(
        "📖 Progress is more than a number"
    )

    st.write(
        "Your projects, GitHub activity, certifications, "
        "hackathons and other achievements together tell "
        "the story of how you are developing as a "
        "software engineer."
    )