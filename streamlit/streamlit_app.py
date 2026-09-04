import os
from datetime import date, datetime, timedelta

import pandas as pd
import plotly.express as px
import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))
load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

API_URL = os.getenv("API_URL", "http://localhost:8000/api")

def get_error_detail(response, fallback):
    if response is None:
        return str(fallback)
    try:
        detail = response.json().get("detail")
        if detail:
            return str(detail)
    except ValueError:
        pass
    return response.text or str(fallback)


def fetch_overview(start_date, end_date, pipeline=None, feature=None):
    response = requests.get(
        f"{API_URL}/overview",
        params={
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
            "pipeline": pipeline or None,
            "feature": feature or None,
        },
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


def fetch_heatmap(start_date, end_date, pipeline=None):
    response = requests.get(
        f"{API_URL}/heatmap",
        params={"start_date": start_date.isoformat(), "end_date": end_date.isoformat(), "pipeline": pipeline or None},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()

st.set_page_config(page_title="Test Report Analyzer", page_icon="", layout="wide")
st.markdown(
    """
    <style>
    :root { --ink: #f7f7fb; --muted: #a4a6b5; --panel: #20212b; --panel-deep: #12131a; --line: #353744; --accent: #ff4d52; --success: #2ac985; }
    .stApp { background: #101118; color: var(--ink); }
    [data-testid="stSidebar"] { background: #20212b; border-right: 1px solid var(--line); }
    [data-testid="stSidebar"] > div:first-child { padding-top: 1.3rem; }
    [data-testid="stSidebar"] * { color: var(--ink); }
    [data-testid="stHeader"] { background: rgba(16,17,24,.92); }
    [data-testid="stMetric"] { background: var(--panel); border: 1px solid var(--line); border-radius: 12px; padding: 1rem; }
    [data-testid="stMetricValue"] { color: var(--ink); }
    .input-hero { display: flex; align-items: center; gap: .8rem; margin: .5rem 0 1.5rem; }
    .input-hero-icon { font-size: 2.2rem; line-height: 1; }
    .input-hero h1 { margin: 0; font-size: 2.2rem; }
    .input-hero p { color: var(--muted); margin: .25rem 0 0; }
    .connection-card { background: #171821; border: 1px solid var(--line); border-radius: 10px; padding: .8rem; margin: .5rem 0 1rem; }
    .connection-status { color: var(--success); font-weight: 700; margin-top: .45rem; }
    .section-label { color: var(--muted); font-size: .82rem; text-transform: uppercase; letter-spacing: .08em; margin: 1rem 0 .4rem; }
    div[data-testid="stForm"] { background: #171821; border: 1px solid var(--line); border-radius: 12px; padding: 1.25rem; }
    div[data-testid="stFileUploader"] { background: #20212b; border: 1px dashed #555867; border-radius: 10px; padding: .4rem; }
    div.stButton > button[kind="primary"], div[data-testid="stFormSubmitButton"] button { background: var(--accent); border: 0; color: white; font-weight: 700; min-height: 2.8rem; }
    div.stButton > button[kind="primary"]:hover, div[data-testid="stFormSubmitButton"] button:hover { background: #ff686c; color: white; }
    </style>
    """,
    unsafe_allow_html=True,
)

if "next_screen" in st.session_state:
    st.session_state.screen = st.session_state.pop("next_screen")

with st.sidebar:
    st.markdown("### 🧪 Intelligent Test")
    st.caption("Report Analyzer & Insights Engine")
    st.markdown(
        f'<div class="connection-card"><b>⚙ Connection</b><br><small>Backend: {API_URL}</small>'
        '<div class="connection-status">● Ready to connect</div></div>',
        unsafe_allow_html=True,
    )
    if st.button("Verify backend", key="verify_backend"):
        try:
            requests.get(f"{API_URL}/health", timeout=3).raise_for_status()
            st.success("Backend is reachable")
        except requests.RequestException as error:
            st.error(f"Backend unavailable: {error}")
    st.markdown('<div class="section-label">Screen</div>', unsafe_allow_html=True)
    screen = st.radio("Screen", ["Input", "Dashboard"], key="screen")

if screen == "Input":
    st.markdown(
        '<div class="input-hero"><span class="input-hero-icon">📥</span><div><h1>Input</h1>'
        '<p>Configure the analysis and upload CI/CD test reports.</p></div></div>',
        unsafe_allow_html=True,
    )
    with st.form("input_configuration_form", clear_on_submit=False):
        input_columns = st.columns(3)
        with input_columns[0]:
            source = st.text_input("Source", "Jenkins", key="input_source")
        with input_columns[1]:
            pipeline_upload = st.text_input("Pipeline", "main", key="input_pipeline")
        with input_columns[2]:
            build_number = st.text_input("Build ID", "1", key="input_build_number")
        input_columns = st.columns(2)
        with input_columns[0]:
            report_type = st.selectbox("Report type", ["junit", "allure", "extent"], key="input_report_type")
        with input_columns[1]:
            rag_window_days = st.slider("RAG window (days)", min_value=1, max_value=365, value=30, key="rag_window_input")
        uploaded_files = st.file_uploader("Upload reports", type=["xml"], accept_multiple_files=True, key="input_reports")
        submit = st.form_submit_button("🚀  Ingest & Analyze", type="primary", use_container_width=True)

    if submit:
        if not uploaded_files:
            st.error("Upload at least one report before starting analysis.")
        else:
            ingested_count = 0
            upload_errors = []
            for uploaded_file in uploaded_files:
                payload = {
                    "source": source,
                    "pipeline": pipeline_upload,
                    "build_number": build_number,
                    "report_type": report_type,
                    "timestamp": datetime.utcnow().isoformat(),
                }
                try:
                    response = requests.post(
                        f"{API_URL}/upload-report",
                        data=payload,
                        files={"file": (uploaded_file.name, uploaded_file.getvalue(), "application/xml")},
                        timeout=60,
                    )
                    response.raise_for_status()
                    result = response.json()
                    ingested_count += result.get("ingested_records", 0)
                    if result.get("warning"):
                        upload_errors.append(f"{uploaded_file.name}: {result['warning']}")
                except requests.RequestException as error:
                    upload_errors.append(f"{uploaded_file.name}: {get_error_detail(error.response, error)}")
            for upload_error in upload_errors:
                st.warning(upload_error)
            if ingested_count:
                st.session_state.rag_window_days = rag_window_days
                st.session_state.next_screen = "Dashboard"
                st.rerun()

if screen == "Input":
    st.info("After ingestion, the dashboard opens automatically. You can also select Dashboard from the sidebar.")
    st.stop()

st.header("Dashboard")
st.caption("Filter one quality overview to compare features, success, recurring errors, and hotspots.")
st.subheader("Filters")
filter_columns = st.columns([1.2, 1.2, 1.5, 1.5])
with filter_columns[0]:
    date_preset = st.selectbox("Duration", ["Last 7 days", "Last 30 days", "This month", "Custom"])
with filter_columns[1]:
    pipeline_filter = st.text_input("Pipeline", placeholder="All pipelines")

today = date.today()
if date_preset == "Last 7 days":
    start_date, end_date = today - timedelta(days=6), today
elif date_preset == "This month":
    start_date, end_date = today.replace(day=1), today
elif date_preset == "Custom":
    with filter_columns[2]:
        selected_dates = st.date_input("Date range", value=(today - timedelta(days=29), today))
    if isinstance(selected_dates, tuple) and len(selected_dates) == 2:
        start_date, end_date = selected_dates
    else:
        start_date, end_date = today - timedelta(days=29), today
else:
    start_date, end_date = today - timedelta(days=29), today

try:
    overview = fetch_overview(start_date, end_date, pipeline_filter)
except requests.RequestException as error:
    st.error(f"Could not load filtered overview: {get_error_detail(error.response, error)}")
    overview = {"summary": {}, "features": [], "error_categories": [], "hotspots": [], "flaky_tests": []}

features = overview.get("features", [])
feature_names = [item["feature"] for item in features]
with filter_columns[2 if date_preset != "Custom" else 3]:
    feature_filter = st.selectbox("Feature", ["All features"] + feature_names)

if feature_filter != "All features":
    try:
        overview = fetch_overview(start_date, end_date, pipeline_filter, feature_filter)
    except requests.RequestException as error:
        st.error(f"Could not apply feature filter: {get_error_detail(error.response, error)}")

summary = overview.get("summary", {})
st.caption(f"Showing {start_date.isoformat()} through {end_date.isoformat()}")
metric_columns = st.columns(4)
metric_columns[0].metric("Executions", summary.get("total_executions", 0))
metric_columns[1].metric("Unique tests", summary.get("unique_test_cases", 0))
metric_columns[2].metric("Passed", summary.get("passed_executions", 0))
metric_columns[3].metric("Failed", summary.get("failed_executions", 0))
metric_columns = st.columns(4)
metric_columns[0].metric("Pass rate", f"{summary.get('pass_rate', 0):.2f}%")
metric_columns[1].metric("Fail rate", f"{summary.get('fail_rate', 0):.2f}%")
metric_columns[2].metric("Runs", summary.get("run_count", 0), help=f"{summary.get('passed_runs', 0)} passed, {summary.get('failed_runs', 0)} failed")
metric_columns[3].metric("Skipped", summary.get("skipped_executions", 0))

st.header("Quality overview")
feature_data = overview.get("features", [])
if feature_data:
    feature_frame = pd.DataFrame(feature_data)
    feature_frame["pass_rate"] = (feature_frame["passed"] / feature_frame["total"].replace(0, 1) * 100).round(2)
    feature_frame["fail_rate"] = (feature_frame["failed"] / feature_frame["total"].replace(0, 1) * 100).round(2)
    feature_chart_data = feature_frame.melt(
        id_vars=["feature", "pass_rate", "fail_rate"],
        value_vars=["passed", "failed"],
        var_name="status",
        value_name="test_cases",
    )
    feature_chart_data["rate"] = feature_chart_data.apply(
        lambda row: row["pass_rate"] if row["status"] == "passed" else row["fail_rate"],
        axis=1,
    )
    feature_chart = px.bar(
        feature_chart_data,
        x="test_cases",
        y="feature",
        color="status",
        orientation="h",
        color_discrete_map={"passed": "#16a34a", "failed": "#dc2626"},
        labels={"test_cases": "Test cases", "feature": "Feature", "status": "Result"},
        hover_data={"test_cases": True, "rate": ":.2f", "pass_rate": False, "fail_rate": False},
        text=feature_chart_data["rate"].map(lambda rate: f"{rate:.2f}%"),
    )
    feature_chart.update_traces(textposition="inside", insidetextanchor="middle")
    feature_chart.update_layout(height=max(300, len(feature_data) * 48), margin=dict(l=10, r=10, t=20, b=20))
    st.plotly_chart(feature_chart, use_container_width=True)
    feature_rate_table = feature_frame[["feature", "passed", "pass_rate", "failed", "fail_rate"]].rename(
        columns={
            "feature": "Feature",
            "passed": "Passed",
            "pass_rate": "Pass rate %",
            "failed": "Failed",
            "fail_rate": "Fail rate %",
        }
    )
    st.dataframe(feature_rate_table, use_container_width=True, hide_index=True)
else:
    st.info("No test results found for the selected filters.")

success_column, hotspot_column = st.columns([1, 1])
with success_column:
    st.subheader("Success rate per test case")
    result_data = {"result": ["Passed", "Failed", "Skipped"], "count": [summary.get("passed_executions", 0), summary.get("failed_executions", 0), summary.get("skipped_executions", 0)]}
    pie_chart = px.pie(result_data, names="result", values="count", color="result", color_discrete_map={"Passed": "#16a34a", "Failed": "#dc2626", "Skipped": "#f59e0b"}, hole=0.45)
    pie_chart.update_traces(textinfo="label+percent", hovertemplate="%{label}: %{value} test cases (%{percent})<extra></extra>")
    pie_chart.update_layout(height=330, margin=dict(l=10, r=10, t=20, b=20), showlegend=True)
    st.plotly_chart(pie_chart, use_container_width=True)

with hotspot_column:
    st.subheader("Feature hotspots")
    hotspots = overview.get("hotspots", [])
    if hotspots:
        hotspot_frame = pd.DataFrame(hotspots).rename(columns={"feature": "Feature", "failed_tests": "Failed", "total_tests": "Total", "failure_rate": "Failure rate %"})
        st.dataframe(hotspot_frame, use_container_width=True, hide_index=True)
    else:
        st.info("No hotspots found for the selected filters.")

st.subheader("Failure-density heatmap")
try:
    heatmap_data = fetch_heatmap(start_date, end_date, pipeline_filter)
except requests.RequestException as error:
    heatmap_data = []
    st.info(f"Heatmap unavailable: {get_error_detail(error.response, error)}")
if heatmap_data:
    heatmap_frame = pd.DataFrame(heatmap_data)
    heatmap_chart = px.density_heatmap(
        heatmap_frame,
        x="date",
        y="module_name",
        z="failure_density",
        histfunc="sum",
        color_continuous_scale=["#dcfce7", "#fbbf24", "#dc2626"],
        labels={"date": "Date", "module_name": "Feature", "failure_density": "Failed tests"},
    )
    heatmap_chart.update_layout(height=420, margin=dict(l=10, r=10, t=20, b=20))
    st.plotly_chart(heatmap_chart, use_container_width=True)
else:
    st.info("No daily failure density data for the selected filters.")

st.header("Errors and categories")
error_categories = overview.get("error_categories", [])
if error_categories:
    error_frame = pd.DataFrame(error_categories)[["category", "occurrences", "test_case_count", "run_count"]].rename(columns={"category": "Category", "occurrences": "Occurrences", "test_case_count": "Test cases", "run_count": "Runs"})
    st.dataframe(error_frame, use_container_width=True, hide_index=True)
    for error in error_categories:
        with st.expander(f"{error['category']} - {error['occurrences']} occurrences"):
            st.write(f"Affected test cases: {', '.join(error['test_cases']) or 'None'}")
            st.write(f"Runs: {', '.join(error['runs']) or 'None'}")
            st.write("Examples:")
            for example in error["examples"]:
                st.code(example)
else:
    st.info("No grouped errors found for the selected filters.")

st.header("AI root-cause analysis")
rag_test_name = st.text_input("Test name to investigate", placeholder="Verify Login with Invalid Credentials")
if st.button("Analyze with RAG", type="primary"):
    if not rag_test_name.strip():
        st.error("Enter a test name before analyzing.")
    else:
        try:
            rag_response = requests.get(
                f"{API_URL}/root-cause/{requests.utils.quote(rag_test_name.strip(), safe='')}",
                params={"window_days": st.session_state.get("rag_window_days", 30)},
                timeout=90,
            )
            rag_response.raise_for_status()
            rag_result = rag_response.json()
            st.success(f"RAG analysis completed using the last {st.session_state.get('rag_window_days', 30)} days.")
            st.write(rag_result.get("root_cause", "No root cause returned."))
            st.caption(rag_result.get("evidence", ""))
            st.write(rag_result.get("recommendation", ""))
        except requests.RequestException as error:
            st.error(f"RAG analysis failed: {get_error_detail(error.response, error)}")

st.header("Send notifications")
email_column, slack_column = st.columns(2)
with email_column:
    with st.form("email_notification_form"):
        st.subheader("Email overview")
        email_recipient = st.text_input("Recipient email", placeholder="recipient@example.com")
        email_submitted = st.form_submit_button("Send email", type="primary")
        if email_submitted:
            if not email_recipient.strip():
                st.error("Enter a recipient email address.")
            else:
                try:
                    email_response = requests.post(
                        f"{API_URL}/notify/email",
                        params={
                            "subject": "Test Quality Overview",
                            "html_body": f"<h1>Test Quality Overview</h1><p>Pass rate: {summary.get('pass_rate', 0):.2f}%</p><p>Fail rate: {summary.get('fail_rate', 0):.2f}%</p><p>Failed executions: {summary.get('failed_executions', 0)}</p><p>Failed runs: {summary.get('failed_runs', 0)}</p>",
                            "to_address": email_recipient.strip(),
                        },
                        timeout=30,
                    )
                    email_response.raise_for_status()
                    st.success("Email sent successfully.")
                except requests.RequestException as error:
                    st.error(f"Email could not be sent: {get_error_detail(error.response, error)}")

with slack_column:
    with st.form("slack_notification_form"):
        st.subheader("Slack overview")
        flaky_tests = overview.get("flaky_tests", [])
        flaky_summary = "\n".join(f"• {item['test_name']}: {item['flaky_score']:.2f}%" for item in flaky_tests[:5]) or "• No flaky tests"
        hotspot_summary = "\n".join(f"• {item['feature']}: {item['failure_rate']:.2f}% ({item['failed_tests']} failed)" for item in overview.get("hotspots", [])[:5]) or "• No hotspots"
        default_slack_message = f"*Test Quality Overview*\n• Pass rate: {summary.get('pass_rate', 0):.2f}%\n• Fail rate: {summary.get('fail_rate', 0):.2f}%\n• Executions: {summary.get('total_executions', 0)}\n• Unique tests: {summary.get('unique_test_cases', 0)}\n• Runs: {summary.get('run_count', 0)} ({summary.get('passed_runs', 0)} passed / {summary.get('failed_runs', 0)} failed)\n\n*Flaky tests*\n{flaky_summary}\n\n*Hotspots*\n{hotspot_summary}"
        slack_message = st.text_area("Message", value=default_slack_message, height=260)
        slack_submitted = st.form_submit_button("Send to Slack", type="primary")
        if slack_submitted:
            if not slack_message.strip():
                st.error("Enter a message before sending.")
            else:
                try:
                    slack_response = requests.post(f"{API_URL}/notify/slack", params={"message": slack_message.strip()}, timeout=30)
                    slack_response.raise_for_status()
                    st.success("Slack notification sent successfully.")
                except requests.RequestException as error:
                    st.error(f"Slack notification could not be sent: {get_error_detail(error.response, error)}")
