import streamlit as st
from src.database import get_jobs, add_job, update_job_status, delete_job


def show_job_tracker():

    st.markdown("""
    <style>
        label, .stTextInput label, .stSelectbox label,
        .stTextArea label {
            color: #0f172a !important;
            font-size: 0.85rem !important;
            font-weight: 500 !important;
        }
        div[data-testid="stMarkdownContainer"] p { color: #0f172a !important; }
        .stMetric label { color: #94a3b8 !important; font-size: 0.72rem !important; }
        .stMetric [data-testid="stMetricValue"] { color: #1e3a8a !important; }
        div[data-testid="stForm"] { border: none !important; padding: 0 !important; }
    </style>
    """, unsafe_allow_html=True)

    user_id = st.session_state.get("github_username")

    if not user_id:
        st.markdown('<div class="page-title">Job Tracker</div>', unsafe_allow_html=True)
        st.warning("Please analyze your GitHub profile first.")
        if st.button("Go to Profile Analyzer"):
            st.session_state["page"] = "github"
            st.rerun()
        return

    jobs = get_jobs(user_id=user_id)

    st.markdown('<div class="page-title">Job Tracker</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="page-sub">Keep every application organized in one place</div>',
        unsafe_allow_html=True
    )

    # Stats row
    total = len(jobs)
    saved = len([j for j in jobs if j.get("status") == "Saved"])
    applied = len([j for j in jobs if j.get("status") == "Applied"])
    interviews = len([j for j in jobs if j.get("status") == "Interview"])
    offers = len([j for j in jobs if j.get("status") == "Offer"])

    c1, c2, c3, c4, c5 = st.columns(5)
    stats = [
        ("Total", total, "tracked", "#1e3a8a"),
        ("Saved", saved, "opportunities", "#2563eb"),
        ("Applied", applied, "sent", "#f97316"),
        ("Interviews", interviews, "scheduled", "#16a34a"),
        ("Offers", offers, "received", "#15803d"),
    ]
    for col, (label, val, sub, color) in zip([c1, c2, c3, c4, c5], stats):
        with col:
            st.markdown(f"""
            <div class="card" style="text-align:center; padding:1rem;">
                <div style="font-size:1.8rem; font-weight:700; color:{color};
                            letter-spacing:-0.5px">{val}</div>
                <div style="font-size:0.72rem; color:#94a3b8; text-transform:uppercase;
                            letter-spacing:0.06em; font-weight:500; margin-top:2px">{label}</div>
                <div style="font-size:0.72rem; color:#2563eb;
                            font-weight:500; margin-top:2px">{sub}</div>
            </div>
            """, unsafe_allow_html=True)

    st.divider()

    # Add job form
    st.markdown('<div class="sec-head">Add New Application</div>', unsafe_allow_html=True)

    with st.form("add_job_form"):
        col1, col2 = st.columns(2)
        with col1:
            company = st.text_input("Company", placeholder="e.g. Google")
            location = st.text_input("Location", placeholder="e.g. Remote / Bengaluru")
            job_url = st.text_input("Job URL", placeholder="https://...")
        with col2:
            role = st.text_input("Role", placeholder="e.g. Backend Developer Intern")
            status = st.selectbox(
                "Status",
                ["Saved", "Applied", "Interview", "Offer", "Rejected"]
            )
            notes = st.text_area(
                "Notes",
                placeholder="Any notes about this role...",
                height=100
            )

        submitted = st.form_submit_button(
            "Save Application",
            type="primary",
            use_container_width=True
        )

        if submitted:
            if not company or not role:
                st.error("Company and role are required.")
            else:
                add_job(
                    company=company,
                    role=role,
                    location=location,
                    status=status,
                    job_url=job_url,
                    notes=notes,
                    user_id=user_id
                )
                st.success("Application saved!")
                st.rerun()

    st.divider()

    # Applications list
    st.markdown('<div class="sec-head">Your Applications</div>', unsafe_allow_html=True)

    if not jobs:
        st.markdown("""
        <div class="card" style="text-align:center; padding:2.5rem;">
            <div style="font-size:1rem; font-weight:600; color:#cbd5e1; margin-bottom:0.4rem">
                No applications yet
            </div>
            <div style="font-size:0.85rem; color:#94a3b8">
                Add your first opportunity above
            </div>
        </div>
        """, unsafe_allow_html=True)
        return

    status_colors = {
        "Saved": "#2563eb",
        "Applied": "#f97316",
        "Interview": "#16a34a",
        "Offer": "#15803d",
        "Rejected": "#dc2626"
    }

    for job in jobs:
        status_color = status_colors.get(job.get("status", "Saved"), "#64748b")
        notes_html = (
            f'<div style="color:#64748b; font-size:0.8rem; margin-top:6px; '
            f'font-style:italic">{job.get("notes")}</div>'
            if job.get("notes") else ""
        )

        st.markdown(f"""
        <div class="card" style="margin-bottom:0.8rem;">
            <div style="display:flex; justify-content:space-between; align-items:flex-start;">
                <div>
                    <div style="font-weight:700; font-size:1rem; color:#0f172a">
                        {job.get('company', 'Unknown')}
                    </div>
                    <div style="color:#475569; font-size:0.85rem; margin-top:3px">
                        {job.get('role', '')}
                        &nbsp;·&nbsp;
                        {job.get('location') or 'Location not specified'}
                    </div>
                    {notes_html}
                </div>
                <div style="background:{status_color}18; color:{status_color};
                            padding:3px 12px; border-radius:4px; font-size:0.75rem;
                            font-weight:600; white-space:nowrap; border:1px solid {status_color}30;">
                    {job.get('status', '')}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        col1, col2, col3 = st.columns([2, 1, 1])

        with col1:
            new_status = st.selectbox(
                "Update status",
                ["Saved", "Applied", "Interview", "Offer", "Rejected"],
                index=["Saved", "Applied", "Interview",
                       "Offer", "Rejected"].index(job.get("status", "Saved")),
                key=f"status_{job['id']}",
                label_visibility="collapsed"
            )
            if new_status != job.get("status"):
                update_job_status(job["id"], new_status, user_id=user_id)
                st.rerun()

        with col2:
            if job.get("job_url"):
                st.link_button(
                    "View Job →",
                    job["job_url"],
                    use_container_width=True
                )

        with col3:
            if st.button("Delete", key=f"delete_{job['id']}", use_container_width=True):
                delete_job(job["id"], user_id=user_id)
                st.rerun()

    st.divider()

    st.markdown(f"""
    <div style="color:#94a3b8; font-size:0.8rem; text-align:center;">
        {total} applications tracked
        &nbsp;·&nbsp;
        Use Job Analyzer to check skill match before applying
    </div>
    """, unsafe_allow_html=True)