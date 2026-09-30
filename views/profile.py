import streamlit as st

from src.database import (
    get_user_by_id,
    update_user_github_username,
)


def show_profile():
    st.title("👤 Profile")
    st.caption("Manage your DevTrack account and GitHub connection.")

    user_id = st.session_state.get("user_id")

    if not user_id:
        st.warning("Please log in first.")
        return

    user = get_user_by_id(user_id)

    if not user:
        st.error("User profile could not be loaded.")
        return

    st.subheader("Account Information")

    name = user.get("name", "")
    email = user.get("email", "")

    col1, col2 = st.columns(2)

    with col1:
        st.text_input(
            "Name",
            value=name,
            disabled=True,
        )

    with col2:
        st.text_input(
            "Email",
            value=email,
            disabled=True,
        )

    st.divider()

    st.subheader("GitHub Connection")

    current_username = user.get(
        "github_username",
        "",
    ) or ""

    github_username = st.text_input(
        "GitHub Username",
        value=current_username,
        placeholder="e.g. octocat",
        help="Enter your GitHub username.",
    )

    if st.button(
        "Save GitHub Username",
        type="primary",
    ):
        github_username = github_username.strip()

        if not github_username:
            st.warning(
                "Please enter a GitHub username."
            )
            return

        try:
            update_user_github_username(
                user_id,
                github_username,
            )

            st.session_state["github_username"] = (
                github_username
            )

            st.success(
                "GitHub username saved successfully!"
            )

        except Exception as e:
            st.error(
                f"Could not save GitHub username: {e}"
            )

    st.divider()

    st.subheader("Account")

    st.write(
        "Your DevTrack account is ready. "
        "Connect GitHub to unlock your developer dashboard."
    )