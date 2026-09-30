import streamlit as st

from src.database import (
    get_goals,
    add_goal,
    update_goal,
    delete_goal,
)


# =========================================================
# GOALS PAGE STYLING
# =========================================================

st.markdown(
    """
    <style>

    /* =========================================
       MAIN CONTENT TEXT
       ========================================= */

    section.main,
    section.main * {
        color: #0F172A !important;
    }

    /* Headings */
    section.main h1,
    section.main h2,
    section.main h3,
    section.main h4,
    section.main h5,
    section.main h6 {
        color: #0F172A !important;
    }

    /* Markdown */
    section.main [data-testid="stMarkdownContainer"],
    section.main [data-testid="stMarkdownContainer"] * {
        color: #0F172A !important;
    }

    /* Paragraphs */
    section.main p {
        color: #0F172A !important;
    }

    /* Captions */
    section.main [data-testid="stCaptionContainer"],
    section.main [data-testid="stCaptionContainer"] * {
        color: #334155 !important;
    }

    /* Metrics */
    section.main [data-testid="stMetric"],
    section.main [data-testid="stMetric"] * {
        color: #0F172A !important;
    }

    section.main [data-testid="stMetricLabel"],
    section.main [data-testid="stMetricLabel"] * {
        color: #0F172A !important;
    }

    section.main [data-testid="stMetricValue"],
    section.main [data-testid="stMetricValue"] * {
        color: #0F172A !important;
    }

    /* Widget labels */
    section.main [data-testid="stWidgetLabel"],
    section.main [data-testid="stWidgetLabel"] * {
        color: #0F172A !important;
    }

    section.main label {
        color: #0F172A !important;
    }

    /* Input text */
    section.main input,
    section.main textarea {
        color: #0F172A !important;
    }

    /* Selectbox text */
    section.main [data-baseweb="select"],
    section.main [data-baseweb="select"] * {
        color: #0F172A !important;
    }

    /* =========================================
       BUTTON TEXT
       ========================================= */

    section.main button {
        color: #0F172A !important;
    }

    /* =========================================
       GOAL CONTAINERS
       ========================================= */

    section.main [data-testid="stVerticalBlockBorderWrapper"] {
        background: #FFFFFF !important;
        border-color: #E2E8F0 !important;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# CURRENT USER
# =========================================================

def get_current_user():

    return st.session_state.get(
        "user_id"
    )


# =========================================================
# MAIN PAGE
# =========================================================

def show_goals():

    user_id = get_current_user()

    if not user_id:

        st.warning(
            "Please login to manage goals."
        )

        return


    # =====================================================
    # HEADER
    # =====================================================

    st.markdown(
        "## 🎯 Goals"
    )

    st.markdown(
        "Turn your plans into measurable progress."
    )

    st.markdown(
        "Set career and development goals, track your progress "
        "and keep yourself moving forward."
    )

    st.write("")


    # =====================================================
    # LOAD GOALS
    # =====================================================

    goals = get_goals(
        user_id=user_id
    )

    if goals is None:
        goals = []


    # =====================================================
    # STATISTICS
    # =====================================================

    total_goals = len(
        goals
    )


    active_goals = len(
        [
            g for g in goals
            if g.get("status") == "Active"
        ]
    )


    completed_goals = len(
        [
            g for g in goals
            if g.get("status") == "Completed"
        ]
    )


    if total_goals:

        average_progress = int(
            sum(
                g.get("progress", 0)
                for g in goals
            )
            /
            total_goals
        )

    else:

        average_progress = 0


    # =====================================================
    # STATS
    # =====================================================

    col1, col2, col3, col4 = st.columns(4)


    with col1:

        st.metric(
            "Total Goals",
            total_goals
        )

        st.caption(
            "Goals created"
        )


    with col2:

        st.metric(
            "Active",
            active_goals
        )

        st.caption(
            "Goals in progress"
        )


    with col3:

        st.metric(
            "Completed",
            completed_goals
        )

        st.caption(
            "Finished goals"
        )


    with col4:

        st.metric(
            "Average",
            f"{average_progress}%"
        )

        st.caption(
            "Overall progress"
        )


    st.divider()


    # =====================================================
    # CREATE GOAL
    # =====================================================

    st.markdown(
        "### ＋ Create a new goal"
    )


    with st.form(
        "create_goal_form"
    ):

        title = st.text_input(
            "Goal title",
            placeholder="Example: Learn Spring Boot"
        )


        description = st.text_area(
            "Description",
            placeholder="Describe your goal"
        )


        category = st.selectbox(
            "Category",
            [
                "Career",
                "Learning",
                "Project",
                "Personal"
            ]
        )


        target_date = st.text_input(
            "Target date",
            placeholder="Example: December 2026"
        )


        progress = st.slider(
            "Progress",
            0,
            100,
            0
        )


        save = st.form_submit_button(
            "Save Goal"
        )


        if save:

            if title.strip():

                add_goal(
                    title=title,
                    description=description,
                    category=category,
                    target_date=target_date,
                    progress=progress,
                    user_id=user_id
                )

                st.success(
                    "Goal created successfully."
                )

                st.rerun()

            else:

                st.error(
                    "Please enter a goal title."
                )


    st.divider()


    # =====================================================
    # GOALS LIST
    # =====================================================

    st.markdown(
        "### Your Goals"
    )


    st.caption(
        "Goals and milestones"
    )


    if not goals:

        st.info(
            """
            🚀 No goals yet.

            Create your first goal and start tracking your progress.
            """
        )


    else:

        for goal in goals:

            with st.container(
                border=True
            ):

                # -----------------------------------------
                # GOAL TITLE
                # -----------------------------------------

                st.markdown(
                    f"### {goal.get('title', 'Untitled Goal')}"
                )


                # -----------------------------------------
                # DESCRIPTION
                # -----------------------------------------

                st.write(
                    goal.get(
                        "description",
                        ""
                    )
                )


                # -----------------------------------------
                # PROGRESS
                # -----------------------------------------

                current_progress = goal.get(
                    "progress",
                    0
                )

                try:

                    current_progress = int(
                        current_progress
                    )

                except Exception:

                    current_progress = 0


                current_progress = max(
                    0,
                    min(
                        100,
                        current_progress
                    )
                )


                st.progress(
                    current_progress / 100
                )


                # -----------------------------------------
                # META
                # -----------------------------------------

                st.caption(
                    f"Category: {goal.get('category', '')} "
                    f"| Status: {goal.get('status', '')} "
                    f"| Progress: {current_progress}%"
                )


                # -----------------------------------------
                # ACTIONS
                # -----------------------------------------

                col1, col2 = st.columns(2)


                with col1:

                    if st.button(
                        "Mark Completed",
                        key=f"complete_{goal['id']}"
                    ):

                        update_goal(
                            goal_id=goal["id"],
                            title=goal.get(
                                "title",
                                ""
                            ),
                            description=goal.get(
                                "description",
                                ""
                            ),
                            category=goal.get(
                                "category",
                                ""
                            ),
                            target_date=goal.get(
                                "target_date",
                                ""
                            ),
                            progress=100,
                            status="Completed",
                            user_id=user_id
                        )

                        st.rerun()


                with col2:

                    if st.button(
                        "Delete",
                        key=f"delete_{goal['id']}"
                    ):

                        delete_goal(
                            goal["id"],
                            user_id
                        )

                        st.rerun()


    st.divider()


    # =====================================================
    # FOOTER
    # =====================================================

    st.markdown(
        "### DevTrack Journey"
    )


    st.write(
        """
        Small milestones create long-term progress.

        Connect your goals with your roadmap,
        projects, GitHub activity and job applications
        to build a complete picture of your development.
        """
    )