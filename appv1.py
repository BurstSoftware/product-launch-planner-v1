import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
from datetime import datetime, timedelta

# Set page config
st.set_page_config(page_title="Product Launch Planner", layout="wide")

# Initialize session state for tasks, budget, and feedback
if "tasks" not in st.session_state:
    st.session_state.tasks = {
        "Development": {"Complete prototype": False, "Test product": False},
        "Marketing": {"Create campaign": False, "Schedule ads": False},
        "Operations": {"Set up logistics": False, "Train team": False}
    }
if "budget" not in st.session_state:
    st.session_state.budget = pd.DataFrame(
        columns=["Category", "Item", "Cost"],
        data=[
            ["Marketing", "Ad Campaign", 5000],
            ["Development", "Prototype", 10000],
            ["Operations", "Logistics", 3000]
        ]
    )
if "feedback" not in st.session_state:
    st.session_state.feedback = []

# Title and description
st.title("🚀 Product Launch Planner")
st.markdown("Plan and manage your product or service launch with tasks, budgets, timelines, and feedback.")

# Layout with tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Tasks", "Budget", "Timeline", "Marketing", "Feedback"])

# Tab 1: Task Checklist
with tab1:
    st.header("Task Checklist")
    for phase, tasks in st.session_state.tasks.items():
        st.subheader(phase)
        for task, status in tasks.items():
            st.session_state.tasks[phase][task] = st.checkbox(task, value=status)

    # Progress calculation
    total_tasks = sum(len(tasks) for tasks in st.session_state.tasks.values())
    completed_tasks = sum(
        sum(1 for status in tasks.values() if status)
        for tasks in st.session_state.tasks.values()
    )
    progress = (completed_tasks / total_tasks) * 100 if total_tasks > 0 else 0
    st.progress(progress / 100)
    st.write(f"Progress: {progress:.1f}%")

# Tab 2: Budget Tracking
with tab2:
    st.header("Budget Tracking")
    st.dataframe(st.session_state.budget, use_container_width=True)

    # Add new budget item
    with st.form("budget_form"):
        col1, col2, col3 = st.columns(3)
        with col1:
            category = st.selectbox("Category", ["Marketing", "Development", "Operations"])
        with col2:
            item = st.text_input("Item")
        with col3:
            cost = st.number_input("Cost", min_value=0.0, step=100.0)
        submit = st.form_submit_button("Add Item")
        if submit and item:
            new_item = pd.DataFrame([[category, item, cost]], columns=["Category", "Item", "Cost"])
            st.session_state.budget = pd.concat([st.session_state.budget, new_item], ignore_index=True)
            st.success("Item added!")

    # Budget summary
    total_budget = st.session_state.budget["Cost"].sum()
    st.metric("Total Budget", f"${total_budget:,.2f}")

# Tab 3: Timeline Visualization
with tab3:
    st.header("Launch Timeline")
    # Sample Gantt chart data
    today = datetime.today()
    timeline_data = [
        dict(Task="Prototype Development", Start=today, Finish=today + timedelta(days=30), Phase="Development"),
        dict(Task="Marketing Campaign", Start=today + timedelta(days=20), Finish=today + timedelta(days=50), Phase="Marketing"),
        dict(Task="Logistics Setup", Start=today + timedelta(days=40), Finish=today + timedelta(days=60), Phase="Operations"),
        dict(Task="Launch Day", Start=today + timedelta(days=60), Finish=today + timedelta(days=60), Phase="Milestone")
    ]
    df_timeline = pd.DataFrame(timeline_data)
    
    # Create Gantt chart
    fig = ff.create_gantt(
        df_timeline,
        colors={"Development": "rgb(31, 119, 180)", "Marketing": "rgb(255, 127, 14)", "Operations": "rgb(44, 160, 44)", "Milestone": "rgb(214, 39, 40)"},
        index_col="Phase",
        show_colorbar=True,
        title="Product Launch Timeline"
    )
    st.plotly_chart(fig, use_container_width=True)

# Tab 4: Marketing Integration
with tab4:
    st.header("Marketing Campaigns")
    st.write("Integrate with AI Advertising Writer for campaign content.")
    campaign_idea = st.text_area("Enter campaign idea or prompt for AI Advertising Writer")
    if st.button("Generate Campaign Content"):
        # Placeholder for AI Advertising Writer integration
        st.info("This would call the AI Advertising Writer to generate content based on your input. Sample output:")
        st.write(f"**Generated Ad Copy**: Unleash the future with our new product! {campaign_idea} Join the revolution on launch day!")
    st.write("Additional marketing tools (e.g., email scheduling, social media) can be linked here.")

# Tab 5: Post-Launch Feedback
with tab5:
    st.header("Post-Launch Feedback")
    with st.form("feedback_form"):
        feedback = st.text_area("Collect feedback from customers or team")
        rating = st.slider("Rating (1-5)", 1, 5, 3)
        submit_feedback = st.form_submit_button("Submit Feedback")
        if submit_feedback and feedback:
            st.session_state.feedback.append({"Feedback": feedback, "Rating": rating, "Date": datetime.now()})
            st.success("Feedback submitted!")

    # Display feedback
    if st.session_state.feedback:
        feedback_df = pd.DataFrame(st.session_state.feedback)
        st.dataframe(feedback_df, use_container_width=True)
        avg_rating = feedback_df["Rating"].mean()
        st.metric("Average Rating", f"{avg_rating:.1f}/5")

# Footer
st.markdown("---")
st.write("Built with Streamlit | Enhances startup growth planning | Complements Competitive Analysis Dashboard")
