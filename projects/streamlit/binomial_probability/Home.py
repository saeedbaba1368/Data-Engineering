import streamlit as st
import pandas as pd
import plotly.express as px
from scipy.stats import binom

st.set_page_config(page_title="Dashboard", page_icon="🌍", layout="wide")
st.subheader("BINOMIAL PROBABILITY DISTRIBUTIONS OF RANDOM VARIABLE")

# all graphs we use custom css not streamlit
theme_plotly = None

# load Style css
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# sidebar
st.sidebar.image("logo1.png")

# Creating a DataFrame
df = pd.read_excel("student_scores.xlsx")

# Selecting scenario
selected_scenario = st.sidebar.selectbox("Select a scenario", df["Scenario"])

# Get scenario data
scenario_data = df[df["Scenario"] == selected_scenario]
num_trials = int(scenario_data["Number of Trials"])
prob_success = float(scenario_data["Probability of Success"])

# Input for number of successes
num_successes = st.sidebar.number_input(
    f"Enter Number of Successes (Max {num_trials})", min_value=0, max_value=num_trials
)

# Calculate binomial distribution
x = list(range(num_trials + 1))
probabilities = binom.pmf(x, num_trials, prob_success)

# Calculate predicted probability
predicted_probability = (
    binom.pmf(num_successes, num_trials, prob_success)
    if num_successes is not None
    else None
)

# Plotting the binomial distribution
fig = px.bar(
    x=x, y=probabilities, labels={"x": "Number of Successes", "y": "Probability"}
)
fig.update_layout(
    title=f"BINOMIAL DISTRIBUTION FOR {selected_scenario}",
    xaxis_title="Number of Successes",
    yaxis_title="Probability",
    plot_bgcolor="rgba(0, 0, 0, 0)",  # Set plot background color to transparent
    paper_bgcolor="rgba(0, 0, 0, 0)",  # Set paper background color to transparent
    xaxis=dict(
        showgrid=True, gridcolor="#cecdcd"
    ),  # Show x-axis grid and set its color
    yaxis=dict(
        showgrid=True, gridcolor="#cecdcd"
    ),  # Show y-axis grid and set its color
    font=dict(color="#cecdcd"),  # Set text color to black
    showlegend=True,
)
# Highlight user selected number of successes
if num_successes is not None:
    fig.add_vline(
        x=num_successes,
        line_dash="dash",
        line_color="red",
        annotation_text=f"Selected Success: {num_successes}",
        annotation_position="top right",
    )

# Display predicted probability
if predicted_probability is not None:
    st.success(
        f"**Predicted Probability of** {num_successes} Successes is : {predicted_probability:.4f}"
    )

with st.expander("Data Source"):
    st.write("Student Exam Data:")
    # st.image("log2.png")
    st.dataframe(df, use_container_width=True)

with st.expander("Data Collection"):
    st.warning(f"**Probability of Success in** {selected_scenario}: {prob_success}")
    st.info(f"**Number of Trials in** {selected_scenario}: {num_trials}")

st.plotly_chart(fig, use_container_width=True)
