import streamlit as st

from src.database import (
    get_projects,
    add_project,
    update_project,
    delete_project
)


# =========================================================
# STYLE
# =========================================================

def project_style():

    st.markdown(
        """
        <style>

        h1,h2,h3,h4,p,span,label {
            color:#0F172A !important;
        }

        .project-card {

            padding:20px;
            border-radius:16px;
            background:#ffffff;
            border:1px solid #e2e8f0;
            margin-bottom:15px;

        }

        .small-text {

            color:#475569;
            font-size:14px;

        }

        </style>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# PAGE
# =========================================================

def show_projects():

    project_style()


    user_id = st.session_state.get(
        "user_id"
    )


    if not user_id:

        st.warning(
            "Please login first."
        )

        return



    projects = get_projects(
        user_id=user_id
    )


    # =====================================================
    # HEADER
    # =====================================================

    st.caption(
        "PROJECTS"
    )

    st.title(
        "Build projects that prove your skills"
    )

    st.write(
        "Track your projects, technologies, "
        "progress and links in one place."
    )



    # =====================================================
    # STATS
    # =====================================================


    total = len(projects)


    completed = len(
        [
            p for p in projects
            if p.get("status") == "Completed"
        ]
    )


    progress_projects = len(
        [
            p for p in projects
            if p.get("status") == "In Progress"
        ]
    )


    if total:

        avg_progress = int(
            sum(
                p.get(
                    "progress",
                    0
                )
                for p in projects
            )
            /
            total
        )

    else:

        avg_progress = 0



    col1,col2,col3,col4 = st.columns(4)


    with col1:

        st.metric(
            "Projects",
            total,
            "Total projects"
        )


    with col2:

        st.metric(
            "Completed",
            completed,
            "Finished projects"
        )


    with col3:

        st.metric(
            "In Progress",
            progress_projects,
            "Currently building"
        )


    with col4:

        st.metric(
            "Avg Progress",
            f"{avg_progress}%",
            "Across projects"
        )



    st.divider()



    # =====================================================
    # ADD PROJECT
    # =====================================================


    st.subheader(
        "➕ Add a new project"
    )


    with st.form(
        "add_project_form"
    ):


        name = st.text_input(
            "Project name"
        )


        description = st.text_area(
            "Description"
        )


        technologies = st.text_input(
            "Technologies",
            placeholder="Java, Spring Boot, SQLite"
        )


        status = st.selectbox(
            "Status",
            [
                "Planning",
                "In Progress",
                "Completed"
            ]
        )


        progress = st.slider(
            "Progress",
            0,
            100,
            0
        )


        github = st.text_input(
            "GitHub URL"
        )


        live = st.text_input(
            "Live URL"
        )



        submit = st.form_submit_button(
            "Save Project"
        )


        if submit:


            if not name:

                st.error(
                    "Project name required."
                )

            else:

                add_project(

                    name=name,

                    description=description,

                    status=status,

                    progress=progress,

                    technologies=technologies,

                    github_url=github,

                    live_url=live,

                    user_id=user_id
                )


                st.success(
                    "Project added!"
                )


                st.rerun()



    st.divider()



    # =====================================================
    # PROJECT LIST
    # =====================================================


    st.subheader(
        "Your Projects"
    )


    if not projects:


        st.info(
            """
            No projects yet.

            Add your first project above and start
            building your developer portfolio.
            """
        )


        return



    for project in projects:


        with st.container():


            st.markdown(
                f"""
                ### {project.get("name","Untitled")}

                {project.get("description","")}

                **Technologies:** 
                {project.get("technologies","")}

                **Status:** 
                {project.get("status","")}

                **Progress:** 
                {project.get("progress",0)}%

                """,
            )


            st.progress(
                int(
                    project.get(
                        "progress",
                        0
                    )
                )
                /
                100
            )


            col1,col2 = st.columns(2)


            with col1:

                if project.get(
                    "github_url"
                ):

                    st.link_button(
                        "GitHub",
                        project["github_url"]
                    )


            with col2:

                if st.button(
                    "Delete",
                    key=f"delete_{project['id']}"
                ):

                    delete_project(
                        project["id"],
                        user_id=user_id
                    )

                    st.rerun()