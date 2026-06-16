import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Website Traffic Dashboard", layout="wide")

st.title("Website Traffic Analysis Dashboard")


st.sidebar.header("About")
st.sidebar.write(
    "This dashboard helps analyze website traffic, highlight high-impact pages, and suggest optimizations."
)

# Upload dataset
file = st.file_uploader("Upload Excel or CSV", type=["csv"])

if file is not None:

    df = pd.read_csv(file)

    # ---------- Data Preprocessing ----------
    rows_before = len(df)
    df["session_duration"] = pd.to_numeric(df["session_duration"], errors="coerce")
    df["user_id"] = pd.to_numeric(df["user_id"], errors="coerce")
    df = df.dropna()
    rows_after = len(df)

    st.subheader("Dataset Preview")
    st.write(f"**Rows:** {rows_after}  |  **Columns:** {df.shape[1]}")
    st.write(f"**Dropped rows due to missing/invalid values:** {rows_before - rows_after}")
    st.dataframe(df.head())

    # ---------- KPIs ----------
    st.subheader("Key Metrics")

    total_page_views = len(df)
    unique_users = df["user_id"].nunique() if "user_id" in df.columns else None
    avg_session = df["session_duration"].mean()
    bounce_rate = (df["bounce"].value_counts(normalize=True).get(1, 0)) * 100

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Page Views", total_page_views)

    with col2:
        st.metric("Unique Users", unique_users)

    with col3:
        st.metric("Avg Session Duration", f"{round(avg_session, 2)} sec")

    col4, col5, col6 = st.columns(3)

    with col4:
        st.metric("Bounce Rate", f"{bounce_rate:.2f}%")

    with col5:
        st.metric("Unique Pages", df["page"].nunique())

    with col6:
        st.metric("Entry Pages", df["entry_page"].nunique())

    # ---------- Popular Pages ----------
    st.subheader("Most Popular Pages")

    popular_pages = df["page"].value_counts().reset_index()
    popular_pages.columns = ["Page","Visits"]

    fig1 = px.bar(popular_pages,
                  x="Page",
                  y="Visits",
                  title="Page Popularity")

    st.plotly_chart(fig1, use_container_width=True)

    # ---------- Entry Pages ----------
    st.subheader("Top Entry Pages")

    entry = df["entry_page"].value_counts().reset_index()
    entry.columns = ["Entry Page","Visits"]

    fig2 = px.bar(entry,
                  x="Entry Page",
                  y="Visits",
                  title="Entry Page Analysis")

    st.plotly_chart(fig2, use_container_width=True)

    # ---------- Exit Pages ----------
    st.subheader("Top Exit Pages")

    exit_page = df["exit_page"].value_counts().reset_index()
    exit_page.columns = ["Exit Page","Exits"]

    fig3 = px.bar(exit_page,
                  x="Exit Page",
                  y="Exits",
                  title="Exit Page Analysis")

    st.plotly_chart(fig3, use_container_width=True)

    # ---------- Traffic Source ----------
    st.subheader("Traffic Sources")

    source = df["traffic_source"].value_counts().reset_index()
    source.columns = ["Source","Users"]

    fig4 = px.pie(source,
                  names="Source",
                  values="Users",
                  title="Traffic Source Distribution")

    st.plotly_chart(fig4, use_container_width=True)

    # ---------- Session Duration ----------
    st.subheader("Session Duration Distribution")

    fig5 = px.histogram(df,
                        x="session_duration",
                        nbins=20,
                        title="Session Duration")

    st.plotly_chart(fig5, use_container_width=True)

    # ---------- Navigation Pattern ----------
    st.subheader("User Navigation Pattern")

    nav = df.groupby(["entry_page","exit_page"]).size().reset_index(name="count")

    fig6 = px.scatter(nav,
                      x="entry_page",
                      y="exit_page",
                      size="count",
                      title="Navigation Flow")

    st.plotly_chart(fig6, use_container_width=True)

    # ---------- Insights ----------
    st.subheader("Key Insights")

    top_pages = df["page"].value_counts().head(5)
    st.write("**Top 5 Pages by Views:**")
    st.write(top_pages)

    st.write("**Top entry page:**", df["entry_page"].value_counts().idxmax())
    st.write("**Top exit page:**", df["exit_page"].value_counts().idxmax())
    st.write("**Median session duration:**", round(df["session_duration"].median(), 2), "sec")

    # ---------- Recommendations ----------
    st.subheader("Optimization Recommendations")

    st.write("• Improve pages with high exit rates")
    st.write("• Optimize entry pages to guide users deeper into the site")
    st.write("• Reduce bounce rate with better content and faster load time")
    st.write("• Focus marketing on highest performing traffic sources")
