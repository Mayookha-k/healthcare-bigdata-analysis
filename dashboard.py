"""
Hospital Patient Record Analysis - Dashboard
Big Data Processing project | NY State SPARCS inpatient discharges, 2010

Run:  .\\venv\\Scripts\\python.exe -m streamlit run dashboard.py

Pages: Overview | Diagnoses | Severity & Stay | Patients | Method
Navigation: a menu bar under the banner (always visible) AND the sidebar.
The sidebar has a button that shrinks it to an icon strip (it never disappears).
"""

from pathlib import Path

import altair as alt
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Hospital Patient Record Analysis",
                   page_icon="🏥", layout="wide",
                   initial_sidebar_state="expanded")

NAVY, BLUE, ORANGE, TEAL, LIGHT = "#16284a", "#2f6fd6", "#e07a1f", "#1f9d8f", "#f4f6f9"
INK, MUTED = "#1f2a3d", "#5b6678"

# ---- Selected Chart | Table (and Both | Charges | Stay) button colors ----
SWITCH_BG = NAVY          # background of the selected button
SWITCH_TEXT = "#ffffff"   # text color on the selected button
SWITCH_BORDER = NAVY      # border color of the selected button

DATA_DIR = Path(__file__).parent / "data" / "processed" / "cleaned"
SEVERITY_ORDER = ["Minor", "Moderate", "Major", "Extreme"]
AGE_ORDER = ["0 to 17", "0-17", "18 to 29", "18-29", "30 to 49", "30-49",
             "50 to 69", "50-69", "70 or Older", "70+"]
GENDER_NAMES = {"F": "Female", "M": "Male", "U": "Unknown"}

PAGES = [("Overview", ":material/grid_view:"),
         ("Diagnoses", ":material/monitor_heart:"),
         ("Severity & Stay", ":material/bar_chart:"),
         ("Patients", ":material/group:"),
         ("Method", ":material/hub:")]

# ----------------------------------------------------------------------------
# SIDEBAR STATE (expanded or shrunk to an icon strip)
# ----------------------------------------------------------------------------
if "side_collapsed" not in st.session_state:
    st.session_state["side_collapsed"] = False
collapsed = st.session_state["side_collapsed"]

SIDE_W = "76px" if collapsed else "250px"
COLLAPSED_CSS = """
section[data-testid="stSidebar"] button { justify-content:center !important; padding:.6rem 0 !important; }
section[data-testid="stSidebar"] button p { margin:0 !important; }
[data-testid="stSidebarUserContent"] { padding:1rem .4rem !important; }
""" if collapsed else ""

# ----------------------------------------------------------------------------
# STYLE
# ----------------------------------------------------------------------------
st.markdown(f"""
<style>
  .stApp {{ background:{LIGHT}; color-scheme:light; }}

  /* Hide Streamlit's own top bar and its sidebar open/close buttons
     (we use our own button, so the sidebar can never vanish) */
  header[data-testid="stHeader"] {{ display:none !important; height:0 !important;
                                    min-height:0 !important; }}
  [data-testid="stToolbar"], [data-testid="stDecoration"], footer {{ display:none !important; }}
  [data-testid="stSidebarCollapseButton"], [data-testid="stSidebarHeader"],
  [data-testid="stExpandSidebarButton"], [data-testid="stSidebarCollapsedControl"] {{
      display:none !important; }}

  /* Remove the white strip at the very top of the page */
  [data-testid="stAppViewContainer"], [data-testid="stMain"] {{ padding-top:0 !important; }}
  [data-testid="stMainBlockContainer"], [data-testid="stAppViewBlockContainer"],
  .block-container {{ padding-top:0 !important; margin-top:0 !important; }}
  [data-testid="stElementContainer"]:has(style), .element-container:has(style) {{
      display:none !important; }}

  /* Sidebar: always visible, fixed width (wide or icon strip) */
  section[data-testid="stSidebar"] {{
      width:{SIDE_W} !important; min-width:{SIDE_W} !important; max-width:{SIDE_W} !important;
      transform:none !important; margin-left:0 !important; visibility:visible !important; }}

  /* Compact layout so everything fits on one screen */
  .block-container {{ padding:0 1.5rem .5rem 1.5rem !important; max-width:1400px; }}
  [data-testid="stMain"] [data-testid="stVerticalBlock"] {{ gap:.6rem; }}

  [data-testid="stMain"] p, [data-testid="stMain"] li,
  [data-testid="stMain"] label, [data-testid="stMain"] span {{ color:{INK}; }}

  /* Sidebar look */
  section[data-testid="stSidebar"] {{ background:{NAVY}; }}
  section[data-testid="stSidebar"] * {{ color:#e8eefc; }}
  .side-title {{ font-weight:700; font-size:1.1rem; margin:.4rem 0 0 0; }}
  .side-sub {{ font-size:.8rem; color:#9fb3d9 !important; margin-bottom:1rem; }}
  .side-logo {{ font-size:1.5rem; text-align:center; margin:.4rem 0 .8rem 0; }}
  section[data-testid="stSidebar"] button[data-testid="stBaseButton-secondary"],
  section[data-testid="stSidebar"] button[data-testid="stBaseButton-primary"] {{
      background:transparent; border:none; box-shadow:none; justify-content:flex-start;
      padding:.6rem .8rem; border-radius:6px; }}
  section[data-testid="stSidebar"] button[data-testid="stBaseButton-secondary"]:hover {{
      background:rgba(255,255,255,.08); }}
  section[data-testid="stSidebar"] button[data-testid="stBaseButton-primary"] {{
      background:rgba(255,255,255,.16); border-left:3px solid #6ea8ff; }}
  {COLLAPSED_CSS}

  /* Top menu bar (buttons in the main area) */
  [data-testid="stMain"] button[data-testid="stBaseButton-secondary"] {{
      background:#ffffff; border:1px solid #d5dbe6; border-radius:8px; min-height:2.2rem; }}
  [data-testid="stMain"] button[data-testid="stBaseButton-secondary"] * {{ color:{INK} !important; }}
  [data-testid="stMain"] button[data-testid="stBaseButton-primary"] {{
      background:{NAVY}; border:1px solid {NAVY}; border-radius:8px; min-height:2.2rem; }}
  [data-testid="stMain"] button[data-testid="stBaseButton-primary"] * {{ color:#ffffff !important; }}

  /* Banner (slim) */
  .banner {{ background:{NAVY}; margin:0 -1.5rem .2rem -1.5rem; padding:.8rem 2rem .7rem;
             border-bottom:3px solid {BLUE}; }}
  .banner .eyebrow {{ color:#8db4f0 !important; letter-spacing:.18em; font-size:.68rem; }}
  .banner h1, .banner h1 span {{ color:#ffffff !important; font-family:Georgia,serif;
                font-size:1.7rem; line-height:1.2; margin:.1rem 0 .2rem 0; padding:0; }}
  .banner p {{ color:#cdd9f2 !important; font-size:.85rem; margin:0; }}

  /* Headings, cards */
  h2.page {{ font-family:Georgia,serif; color:{NAVY} !important; margin:0; font-size:1.5rem;
             line-height:1.3; }}
  p.lead {{ color:{MUTED} !important; margin:0; font-size:.9rem; }}
  .kpi {{ background:#fff; border:1px solid #e3e8f0; border-top:3px solid {NAVY};
          border-radius:8px; padding:.6rem .9rem; min-height:100px;
          box-shadow:0 1px 2px rgba(16,32,64,.05); }}
  .kpi .l {{ color:{MUTED} !important; font-size:.8rem; line-height:1.25; min-height:2.1em; }}
  .kpi .v {{ color:{NAVY} !important; font-family:Georgia,serif; font-size:1.4rem;
             font-weight:700; margin:.15rem 0; white-space:nowrap; }}
  .kpi .s {{ color:{MUTED} !important; font-size:.74rem; line-height:1.3; }}
  div[data-testid="stVerticalBlockBorderWrapper"] {{
      background:#fff; border-radius:10px; box-shadow:0 1px 2px rgba(16,32,64,.05); }}

  /* Key findings */
  .finding, .finding div {{ color:{INK} !important; }}
  .finding {{ display:flex; gap:.7rem; padding:.45rem 0; border-bottom:1px solid #eef1f6;
              font-size:.88rem; }}
  .finding .n {{ background:#e6edfb; color:{NAVY} !important; border-radius:50%; min-width:26px;
                 height:26px; text-align:center; line-height:26px; font-weight:700;
                 font-size:.8rem; }}

  /* Switches (Both | Charges | Stay, Chart | Table) - covers every state.
     Normal buttons: white background + dark text. Selected button: SWITCH_ colors. */
  [data-testid="stSegmentedControl"], [data-testid="stButtonGroup"] {{ color-scheme:light; }}

  [data-testid="stSegmentedControl"] button,
  [data-testid="stButtonGroup"] button,
  [data-testid="stSegmentedControl"] [role="radio"],
  [data-baseweb="button-group"] button {{
      background:#ffffff !important; background-image:none !important;
      border:1px solid #d5dbe6 !important; box-shadow:none !important; }}
  [data-testid="stSegmentedControl"] button *,
  [data-testid="stButtonGroup"] button *,
  [data-testid="stSegmentedControl"] [role="radio"] *,
  [data-baseweb="button-group"] button * {{ color:{INK} !important; }}

  [data-testid="stSegmentedControl"] button[aria-checked="true"],
  [data-testid="stSegmentedControl"] button[aria-pressed="true"],
  [data-testid="stSegmentedControl"] button[data-testid$="Active"],
  [data-testid="stSegmentedControl"] [role="radio"][aria-checked="true"],
  [data-testid="stButtonGroup"] button[aria-checked="true"],
  [data-testid="stButtonGroup"] button[aria-pressed="true"],
  [data-testid="stButtonGroup"] button[data-testid$="Active"] {{
      background:{SWITCH_BG} !important; border-color:{SWITCH_BORDER} !important; }}
  [data-testid="stSegmentedControl"] button[aria-checked="true"] *,
  [data-testid="stSegmentedControl"] button[aria-pressed="true"] *,
  [data-testid="stSegmentedControl"] button[data-testid$="Active"] *,
  [data-testid="stSegmentedControl"] [role="radio"][aria-checked="true"] *,
  [data-testid="stButtonGroup"] button[aria-checked="true"] *,
  [data-testid="stButtonGroup"] button[aria-pressed="true"] *,
  [data-testid="stButtonGroup"] button[data-testid$="Active"] * {{
      color:{SWITCH_TEXT} !important; }}

  /* Method page */
  .flow {{ display:flex; align-items:stretch; gap:.5rem; flex-wrap:wrap; }}
  .flow .arrow {{ align-self:center; color:{BLUE} !important; font-size:1.4rem; font-weight:700; }}
  .step {{ background:#fff; border:1px solid #e3e8f0; border-top:3px solid {NAVY};
           border-radius:8px; padding:.7rem 1rem; flex:1; min-width:150px; }}
  .step b {{ color:{NAVY} !important; display:block; margin-bottom:.25rem; }}
  .step span {{ color:{MUTED} !important; font-size:.82rem; line-height:1.3; }}
  .note {{ background:#fff8e6; border-left:4px solid #f0b429; padding:.7rem 1rem;
           border-radius:6px; color:#5b4a14 !important; }}
  .note * {{ color:#5b4a14 !important; }}
</style>
""", unsafe_allow_html=True)


# ----------------------------------------------------------------------------
# COMPATIBILITY HELPERS (so older Streamlit versions don't crash)
# ----------------------------------------------------------------------------
def show(chart):
    try:
        st.altair_chart(chart, width="stretch", theme=None)
    except TypeError:
        st.altair_chart(chart, use_container_width=True, theme=None)


def show_table(data, height=None):
    extra = {"height": int(height)} if height else {}
    try:
        st.dataframe(data, width="stretch", hide_index=True, **extra)
    except TypeError:
        st.dataframe(data, use_container_width=True, hide_index=True, **extra)


def switch(key, options):
    """Pill-style switch (like Both | Charges | Stay). Never returns None."""
    if hasattr(st, "segmented_control"):
        choice = st.segmented_control("switch", list(options), default=options[0],
                                      key=key, label_visibility="collapsed")
        return choice or options[0]
    return st.radio("switch", list(options), horizontal=True, key=key,
                    label_visibility="collapsed")


def go_to(page_name):
    st.session_state["page"] = page_name


def toggle_sidebar():
    st.session_state["side_collapsed"] = not st.session_state["side_collapsed"]


def smart_button(label, key, icon=None, kind="secondary", on_click=None, args=(), tip=None):
    """A full-width button that also works on older Streamlit versions."""
    kwargs = dict(key=key, type=kind, on_click=on_click, args=args)
    if tip:
        kwargs["help"] = tip
    tries = []
    if icon:
        tries += [{"icon": icon, "width": "stretch"}, {"icon": icon, "use_container_width": True}]
    tries += [{"use_container_width": True}, {}]
    for extra in tries:
        try:
            return st.button(label, **kwargs, **extra)
        except TypeError:
            continue


def nav_button(name, icon, active, prefix, compact=False):
    kind = "primary" if active else "secondary"
    label = "\u200b" if compact else name      # icon only when the sidebar is shrunk
    return smart_button(label, f"{prefix}_{name}", icon=icon, kind=kind,
                        on_click=go_to, args=(name,), tip=name if compact else None)


# ----------------------------------------------------------------------------
# LOAD DATA
# ----------------------------------------------------------------------------
def norm(text):
    return "".join(ch for ch in str(text).lower() if ch.isalnum())


WANTED = {
    "diagnosis": ["ccsdiagnosisdescription", "diagnosis", "diagnosisdescription", "ccsdiagnosis"],
    "severity": ["aprseverityofillnessdescription", "severity", "aprseverity", "severityofillness"],
    "mortality": ["aprriskofmortality", "riskofmortality", "mortality"],
    "admission": ["typeofadmission", "admissiontype", "admission"],
    "age": ["agegroup", "age"],
    "gender": ["gender", "sex"],
    "county": ["hospitalcounty", "county", "facilitycounty"],
    "hospital": ["facilityname", "hospital", "facility"],
    "stay": ["lengthofstay", "lengthofstaydays", "los", "stay"],
    "charges": ["totalcharges", "charges"],
    "costs": ["totalcosts", "costs"],
}


@st.cache_data(show_spinner="Reading pipeline CSV files...")
def load_pipeline_csv():
    """Returns (DataFrame or None, message, meta)."""
    meta = {}
    if not DATA_DIR.exists():
        return None, f"Folder not found: {DATA_DIR}", meta
    files = sorted(DATA_DIR.rglob("*.csv"))
    if not files:
        return None, "No .csv files found in data/processed/cleaned", meta

    parts = []
    for f in files:
        try:
            if f.stat().st_size > 0:
                parts.append(pd.read_csv(f, low_memory=False))
        except Exception:
            pass
    if not parts:
        return None, "CSV files were empty", meta
    raw = pd.concat(parts, ignore_index=True)
    meta = {"csv_rows": len(raw), "columns": len(raw.columns), "files": len(files)}

    lookup = {norm(c): c for c in raw.columns}
    found = {}
    for key, options in WANTED.items():
        for opt in options:
            if opt in lookup:
                found[key] = lookup[opt]
                break

    missing = [k for k in ["diagnosis", "severity", "stay", "charges"] if k not in found]
    if missing:
        return None, ("Columns not recognised for: " + ", ".join(missing)
                      + ". Columns in your file: " + ", ".join(map(str, raw.columns))), meta

    df = pd.DataFrame({k: raw[v] for k, v in found.items()})
    for col in ["charges", "costs"]:
        if col in df:
            df[col] = pd.to_numeric(
                df[col].astype(str).str.replace(r"[^0-9.\-]", "", regex=True), errors="coerce")
    df["stay"] = pd.to_numeric(df["stay"].astype(str).str.extract(r"(\d+)")[0], errors="coerce")
    df = df.dropna(subset=["diagnosis", "severity", "charges", "stay"])
    if "gender" in df:
        df["gender"] = df["gender"].map(GENDER_NAMES).fillna(df["gender"])
    return df, f"{len(df):,} rows from {len(files)} CSV file(s)", meta


def order_by(labels, order):
    return sorted(labels, key=lambda x: order.index(x) if x in order else 99)


def pretty(text):
    """LIVEBORN -> Liveborn, but short codes like CHF stay as they are."""
    text = str(text)
    return text.title() if text.isupper() and len(text) > 4 else text


def build_tables(df):
    t = {"records": len(df)}

    diag = df["diagnosis"].value_counts().rename_axis("Diagnosis").reset_index(name="Patients")
    diag["Diagnosis"] = diag["Diagnosis"].map(pretty)
    t["diag_all"] = diag

    sev = df.groupby("severity").agg(Charges=("charges", "mean"), Stay=("stay", "mean"),
                                     Patients=("stay", "size"))
    sev = sev.reindex([s for s in SEVERITY_ORDER if s in sev.index])
    t["sev"] = sev.rename_axis("Severity").reset_index()

    if "admission" in df:
        adm = df.groupby("admission").agg(AvgDays=("stay", "mean"), Patients=("stay", "size"))
        t["adm"] = (adm.sort_values("AvgDays").rename_axis("Admission type").reset_index()
                    .rename(columns={"AvgDays": "Avg days"}))
    if "age" in df:
        a = df["age"].value_counts()
        t["age"] = a.reindex(order_by(a.index, AGE_ORDER)).rename_axis("Age group").reset_index(name="Patients")
    if "county" in df:
        t["county"] = df["county"].value_counts().head(10).rename_axis("County").reset_index(name="Discharges")
        t["county_count"] = df["county"].nunique()
    if "hospital" in df:
        t["hospital"] = df["hospital"].value_counts().head(10).rename_axis("Hospital").reset_index(name="Patients")
    if "gender" in df:
        t["gender"] = df["gender"].value_counts().rename_axis("Gender").reset_index(name="Patients")
    if "mortality" in df:
        m = df["mortality"].value_counts()
        m = m.reindex([s for s in SEVERITY_ORDER if s in m.index])
        t["mortality"] = m.rename_axis("Risk of mortality").reset_index(name="Patients")
    return t


def tables_from_presentation():
    diag = pd.DataFrame({
        "Diagnosis": ["Liveborn", "Mood Disorders", "CHF", "Septicemia", "Chest Pain",
                      "Coronary Atheroscler.", "Pneumonia", "Dysrhythmia"],
        "Patients": [27100, 9300, 9200, 9100, 9000, 8950, 8700, 8200]})
    return {
        "records": 382522, "diag_all": diag,
        "sev": pd.DataFrame({"Severity": SEVERITY_ORDER, "Charges": [16400, 24200, 40300, 109800],
                             "Stay": [3.2, 4.9, 7.5, 16.5], "Patients": [None] * 4}),
        "adm": pd.DataFrame({"Admission type": ["Newborn", "Not Avail.", "Elective", "Emergency", "Urgent", "Trauma"],
                             "Avg days": [4.3, 4.5, 4.8, 5.8, 6.1, 7.3], "Patients": [None] * 6}),
        "age": pd.DataFrame({"Age group": ["0-17", "18-29", "30-49", "50-69", "70+"],
                             "Patients": [49000, 42000, 82000, 102000, 108000]}),
        "county": pd.DataFrame({"County": ["Manhattan", "Kings", "Queens", "Nassau", "Bronx", "Suffolk",
                                           "Westchester", "Erie", "Monroe", "Onondaga"],
                                "Discharges": [65500, 42000, 31800, 31200, 30000, 24500, 19500, 19000, 16000, 11000]}),
    }


# ----------------------------------------------------------------------------
# CHART + TABLE HELPERS
# ----------------------------------------------------------------------------
def kpi(label, value, sub):
    return (f'<div class="kpi"><div class="l">{label}</div>'
            f'<div class="v">{value}</div><div class="s">{sub}</div></div>')


def style_chart(chart, height):
    return (chart.properties(height=height, padding={"right": 45, "top": 8})
            .configure(background="#ffffff")
            .configure_view(strokeWidth=0)
            .configure_axis(gridColor="#eef1f6", domainColor="#c9d1de", labelColor=MUTED,
                            titleColor=MUTED, labelFontSize=12, tickColor="#c9d1de")
            .configure_legend(labelColor=INK, titleColor=MUTED, orient="top", title=None))


def bar_chart(data, cat, val, horizontal=True, color=NAVY, height=200, fmt=",.0f"):
    order = list(data[cat])
    tip = [alt.Tooltip(f"{cat}:N"), alt.Tooltip(f"{val}:Q", format=fmt)]
    if horizontal:
        x = alt.X(f"{val}:Q", title=None)
        y = alt.Y(f"{cat}:N", sort=order, title=None, axis=alt.Axis(labelLimit=280))
        label_kw = dict(align="left", dx=5)
    else:
        x = alt.X(f"{cat}:N", sort=order, title=None, axis=alt.Axis(labelAngle=0))
        y = alt.Y(f"{val}:Q", title=None)
        label_kw = dict(baseline="bottom", dy=-4)
    base = alt.Chart(data).encode(x=x, y=y, tooltip=tip)
    bars = base.mark_bar(color=color, cornerRadius=3)
    labels = base.mark_text(color=INK, fontSize=11, **label_kw).encode(
        text=alt.Text(f"{val}:Q", format=fmt))
    return style_chart(bars + labels, height)


def card_title(title, subtitle=""):
    st.markdown(f"**{title}**")
    if subtitle:
        st.caption(subtitle)


def page_header(title, lead):
    st.markdown(f'<h2 class="page">{title}</h2><p class="lead">{lead}</p>', unsafe_allow_html=True)


def with_share(data, col):
    out = data.copy()
    out["Share (%)"] = out[col] / out[col].sum() * 100
    return out


def fmt_table(data, formats):
    out = data.dropna(axis=1, how="all").reset_index(drop=True)
    for col, pattern in formats.items():
        if col in out:
            out[col] = out[col].map(lambda v, p=pattern: p.format(v) if pd.notna(v) else "–")
    return out


def chart_card(key, title, subtitle, chart, table, height=200):
    """White card with a Chart / Table switch next to the title. Used for every chart."""
    with st.container(border=True):
        t1, t2 = st.columns([3, 2])
        with t1:
            card_title(title, subtitle)
        with t2:
            view = switch(f"view_{key}", ("Chart", "Table"))
        if view == "Chart":
            show(chart)
        else:
            show_table(table, height=height + 30)


# ----------------------------------------------------------------------------
# DATA + SIDEBAR
# ----------------------------------------------------------------------------
df, status, meta = load_pipeline_csv()
USING_REAL = df is not None

if "page" not in st.session_state:
    st.session_state["page"] = "Overview"

with st.sidebar:
    # Our own shrink / expand button (the sidebar never disappears)
    smart_button("\u200b" if collapsed else "Collapse menu", "side_toggle",
                 icon=":material/menu:" if collapsed else ":material/menu_open:",
                 on_click=toggle_sidebar,
                 tip="Expand the menu" if collapsed else "Shrink the menu")
    if collapsed:
        st.markdown('<div class="side-logo">🏥</div>', unsafe_allow_html=True)
    else:
        st.markdown('<p class="side-title">🏥 Analytics Dashboard</p>'
                    '<p class="side-sub">Inpatient discharges, 2010</p>', unsafe_allow_html=True)
    for name, icon in PAGES:
        nav_button(name, icon, st.session_state["page"] == name, "side", compact=collapsed)
    st.markdown("---")
    if collapsed:
        st.caption("✅" if USING_REAL else "⚠️")
    elif USING_REAL:
        st.caption("✅ Data source: pipeline CSV  \n" + status)
    else:
        st.caption("⚠️ Showing numbers from the presentation.  \n" + status)

page = st.session_state["page"]
T = build_tables(df) if USING_REAL else tables_from_presentation()

sev, diag_all = T["sev"], T["diag_all"]
minor, extreme = sev.iloc[0], sev.iloc[-1]
cost_x = extreme["Charges"] / minor["Charges"]
stay_x = extreme["Stay"] / minor["Stay"]
top_diag = diag_all.iloc[0]
second_diag = diag_all.iloc[1] if len(diag_all) > 1 else top_diag
diag_ratio = top_diag["Patients"] / second_diag["Patients"]

# ----------------------------------------------------------------------------
# BANNER + TOP MENU BAR (always visible)
# ----------------------------------------------------------------------------
st.markdown(f"""
<div class="banner">
  <div class="eyebrow">HEALTHCARE ANALYTICS · BIG DATA PROCESSING</div>
  <h1>Hospital Patient Record Analysis</h1>
  <p>Diagnoses, illness severity, cost and length of stay across {T['records']:,}
     New York State inpatient discharges (SPARCS, 2010).</p>
</div>
""", unsafe_allow_html=True)

for col, (name, icon) in zip(st.columns(len(PAGES)), PAGES):
    with col:
        nav_button(name, icon, page == name, "top")

# ----------------------------------------------------------------------------
# PAGE 1: OVERVIEW
# ----------------------------------------------------------------------------
if page == "Overview":
    page_header("Overview", "Headline numbers and the main relationship in the data.")

    cards = [
        kpi("Discharges analysed", f"{T['records']:,}", "<b>Sample</b> loaded by the pipeline"),
        kpi(f"Avg charges, {extreme['Severity']} severity", f"${extreme['Charges']:,.0f}",
            f"<b>{cost_x:.1f}×</b> a {minor['Severity']} case"),
        kpi(f"Avg stay, {extreme['Severity']} severity", f"{extreme['Stay']:.1f} d",
            f"<b>{stay_x:.1f}×</b> a {minor['Severity']} case"),
        kpi("Most common diagnosis", f"{top_diag['Patients']:,}",
            f"<b>{top_diag['Diagnosis']}</b>, {diag_ratio:.1f}× the next"),
    ]
    county_ok = "county" in T and len(T["county"]) > 1
    if county_ok:
        c1, c2 = T["county"].iloc[0], T["county"].iloc[1]
        cards.append(kpi("Busiest county", f"{c1['Discharges']:,}",
                         f"<b>{c1['County']}</b>, {c1['Discharges'] / c2['Discharges']:.1f}× {c2['County']}"))
    for col, html in zip(st.columns(len(cards)), cards):
        col.markdown(html, unsafe_allow_html=True)

    rel = pd.DataFrame({"Severity": sev["Severity"],
                        "Charges": sev["Charges"] / minor["Charges"],
                        "Stay": sev["Stay"] / minor["Stay"]})
    left, right = st.columns([2, 1])

    with left:
        with st.container(border=True):
            card_title("Cost and length of stay rise with severity",
                       f"Both measures shown relative to a {minor['Severity']} case "
                       f"({minor['Severity']} = 1×) so they fit one scale.")
            s1, s2 = st.columns(2)
            with s1:
                measure = switch("measure", ("Both", "Charges", "Stay"))
            with s2:
                view = switch("view_overview", ("Chart", "Table"))

            if view == "Chart":
                long = rel.melt("Severity", var_name="Measure", value_name="Times")
                if measure != "Both":
                    long = long[long["Measure"] == measure]
                base = alt.Chart(long).encode(
                    x=alt.X("Severity:N", sort=list(sev["Severity"]), title=None,
                            axis=alt.Axis(labelAngle=0)),
                    y=alt.Y("Times:Q", title=f"× a {minor['Severity']} case"),
                    color=alt.Color("Measure:N", scale=alt.Scale(domain=["Charges", "Stay"],
                                                                 range=[NAVY, ORANGE])),
                    tooltip=["Severity", "Measure", alt.Tooltip("Times:Q", format=".1f")])
                lines = base.mark_line(point=alt.OverlayMarkDef(size=70), strokeWidth=3)
                labels = base.mark_text(dy=-12, fontSize=11).encode(text=alt.Text("Times:Q", format=".1f"))
                show(style_chart(lines + labels, 230))
            else:
                t = sev.rename(columns={"Charges": "Avg charges ($)", "Stay": "Avg stay (days)"}).copy()
                t[f"Charges (× {minor['Severity']})"] = rel["Charges"]
                t[f"Stay (× {minor['Severity']})"] = rel["Stay"]
                keep = {"Both": list(t.columns),
                        "Charges": ["Severity", "Avg charges ($)", f"Charges (× {minor['Severity']})"],
                        "Stay": ["Severity", "Avg stay (days)", f"Stay (× {minor['Severity']})"]}[measure]
                show_table(fmt_table(t[keep], {
                    "Patients": "{:,.0f}", "Avg charges ($)": "${:,.0f}", "Avg stay (days)": "{:.1f}",
                    f"Charges (× {minor['Severity']})": "{:.1f}×",
                    f"Stay (× {minor['Severity']})": "{:.1f}×"}), height=260)

    with right:
        with st.container(border=True):
            card_title("Key findings", "Associations in one year of sampled data.")
            findings = [
                f"<b>{top_diag['Diagnosis']} leads.</b> {top_diag['Patients']:,} discharges, "
                f"{diag_ratio:.1f}× {second_diag['Diagnosis']}.",
                f"<b>Severity goes with cost.</b> {extreme['Severity']} cases average "
                f"{cost_x:.1f}× the charges of {minor['Severity']}.",
                f"<b>Severity goes with stay.</b> {extreme['Severity']} cases stay {stay_x:.1f}× longer "
                f"({extreme['Stay']:.1f} vs {minor['Stay']:.1f} days).",
            ]
            if "age" in T:
                a = T["age"].sort_values("Patients", ascending=False).iloc[0]
                findings.append(f"<b>Age matters.</b> {a['Age group']} is the largest patient group.")
            if county_ok:
                findings.append(f"<b>Location matters.</b> {c1['County']} has the most discharges.")
            st.markdown("".join(f'<div class="finding"><div class="n">{i}</div><div>{f}</div></div>'
                                for i, f in enumerate(findings, 1)), unsafe_allow_html=True)

# ----------------------------------------------------------------------------
# PAGE 2: DIAGNOSES
# ----------------------------------------------------------------------------
elif page == "Diagnoses":
    page_header("Diagnoses", "Which conditions send the most patients to hospital.")
    left, right = st.columns([3, 1])

    with left:
        with st.container(border=True):
            card_title("Most common diagnoses", "Number of discharges per diagnosis.")
            c1, c2, c3 = st.columns([1, 1, 2])
            with c1:
                view = switch("view_diag", ("Chart", "Table"))
            with c2:
                if len(diag_all) > 5:
                    top_n = st.slider("Show top", 5, min(20, len(diag_all)), min(10, len(diag_all)))
                else:
                    top_n = len(diag_all)
            with c3:
                search = st.text_input("Search", placeholder="🔍 Search a diagnosis, e.g. pneumonia",
                                       label_visibility="collapsed")
            data = diag_all
            if search:
                data = data[data["Diagnosis"].str.contains(search, case=False, na=False)]
            data = data.head(top_n).copy()

            if data.empty:
                st.info("No diagnosis matches your search.")
            elif view == "Chart":
                show(bar_chart(data, "Diagnosis", "Patients", height=max(120, 22 * len(data))))
            else:
                shown = data.copy()
                shown["Share (%)"] = data["Patients"] / diag_all["Patients"].sum() * 100
                shown.insert(0, "Rank", range(1, len(shown) + 1))
                show_table(fmt_table(shown, {"Patients": "{:,.0f}", "Share (%)": "{:.1f}%"}), height=280)
            if not data.empty:
                st.download_button("⬇ Download this table (CSV)", data.to_csv(index=False),
                                   file_name="top_diagnoses.csv", mime="text/csv")

    with right:
        st.markdown(kpi("Top diagnosis", f"{top_diag['Patients']:,}", f"<b>{top_diag['Diagnosis']}</b>"),
                    unsafe_allow_html=True)
        st.markdown(kpi("Runner-up", f"{second_diag['Patients']:,}", f"<b>{second_diag['Diagnosis']}</b>"),
                    unsafe_allow_html=True)
        st.markdown(kpi("Distinct diagnoses", f"{len(diag_all):,}", "Categories in the data"),
                    unsafe_allow_html=True)

# ----------------------------------------------------------------------------
# PAGE 3: SEVERITY & STAY
# ----------------------------------------------------------------------------
elif page == "Severity & Stay":
    page_header("Severity & Stay", "How illness severity and admission type affect cost and days in hospital.")
    sev_tbl = sev.rename(columns={"Charges": "Avg charges ($)", "Stay": "Avg stay (days)"})
    extra = ["Patients"] if "Patients" in sev_tbl else []
    H = 150
    a, b = st.columns(2)
    with a:
        chart_card("sev_charges", "Average charges by severity", "APR illness severity, US dollars.",
                   bar_chart(sev, "Severity", "Charges", horizontal=False, fmt="$,.0f", height=H),
                   fmt_table(sev_tbl[["Severity", "Avg charges ($)"] + extra],
                             {"Avg charges ($)": "${:,.0f}", "Patients": "{:,.0f}"}), height=H)
    with b:
        chart_card("sev_stay", "Average stay by severity", "Days in hospital.",
                   bar_chart(sev, "Severity", "Stay", horizontal=False, color=BLUE, fmt=".1f", height=H),
                   fmt_table(sev_tbl[["Severity", "Avg stay (days)"] + extra],
                             {"Avg stay (days)": "{:.1f}", "Patients": "{:,.0f}"}), height=H)
    c, d = st.columns(2)
    with c:
        if "adm" in T:
            chart_card("adm", "Average stay by admission type",
                       "Small groups (e.g. Trauma) can look extreme.",
                       bar_chart(T["adm"], "Admission type", "Avg days", color=BLUE, height=H, fmt=".1f"),
                       fmt_table(T["adm"], {"Avg days": "{:.1f}", "Patients": "{:,.0f}"}), height=H)
    with d:
        if "mortality" in T:
            chart_card("mortality", "Patients by risk of mortality", "APR risk-of-mortality category.",
                       bar_chart(T["mortality"], "Risk of mortality", "Patients",
                                 horizontal=False, color=TEAL, height=H),
                       fmt_table(with_share(T["mortality"], "Patients"),
                                 {"Patients": "{:,.0f}", "Share (%)": "{:.1f}%"}), height=H)

# ----------------------------------------------------------------------------
# PAGE 4: PATIENTS
# ----------------------------------------------------------------------------
elif page == "Patients":
    page_header("Patients", "Who the patients are and where they are treated.")
    a, b = st.columns(2)
    with a:
        if "age" in T:
            chart_card("age", "Patient volume by age group", "Hospitalisation rises with age.",
                       bar_chart(T["age"], "Age group", "Patients", horizontal=False, height=170),
                       fmt_table(with_share(T["age"], "Patients"),
                                 {"Patients": "{:,.0f}", "Share (%)": "{:.1f}%"}), height=170)
    with b:
        if "county" in T:
            chart_card("county", "Top 10 counties by volume", "Discharges per county.",
                       bar_chart(T["county"], "County", "Discharges", color=BLUE, height=210),
                       fmt_table(with_share(T["county"], "Discharges"),
                                 {"Discharges": "{:,.0f}", "Share (%)": "{:.1f}%"}), height=210)
    c, d = st.columns([1, 2])
    with c:
        if "gender" in T:
            donut = alt.Chart(T["gender"]).mark_arc(innerRadius=50).encode(
                theta="Patients:Q",
                color=alt.Color("Gender:N", scale=alt.Scale(
                    domain=["Female", "Male", "Unknown"], range=[NAVY, ORANGE, "#9aa5b8"])),
                tooltip=["Gender", alt.Tooltip("Patients:Q", format=",")])
            chart_card("gender", "Patients by gender", "", style_chart(donut, 190),
                       fmt_table(with_share(T["gender"], "Patients"),
                                 {"Patients": "{:,.0f}", "Share (%)": "{:.1f}%"}), height=190)
    with d:
        if "hospital" in T:
            chart_card("hospital", "Top 10 hospitals by patient count", "",
                       bar_chart(T["hospital"], "Hospital", "Patients", color=TEAL, height=210),
                       fmt_table(with_share(T["hospital"], "Patients"),
                                 {"Patients": "{:,.0f}", "Share (%)": "{:.1f}%"}), height=210)

# ----------------------------------------------------------------------------
# PAGE 5: METHOD
# ----------------------------------------------------------------------------
else:
    page_header("Method", "How the data went from a raw file to this dashboard.")

    flow = [("Raw CSV", "Real hospital discharge data"),
            ("HDFS", "Distributed storage layer"),
            ("PySpark Clean", "Parse, filter, de-duplicate"),
            ("PySpark Analyze", "Aggregations and trend extraction"),
            ("Dashboard", "Charts and tables in Streamlit")]
    st.markdown('<div class="flow">' + '<div class="arrow">→</div>'.join(
        f'<div class="step"><b>{n}</b><span>{d}</span></div>' for n, d in flow) + '</div>',
        unsafe_allow_html=True)

    left, right = st.columns([1, 1])
    with left:
        with st.container(border=True):
            card_title("Tech stack")
            st.markdown("- **Language:** Python 3.11\n- **Processing:** Apache Spark (PySpark)\n"
                        "- **Storage:** Hadoop HDFS\n- **Dashboard:** Streamlit, pandas, Altair")
    with right:
        with st.container(border=True):
            card_title("Data cleaning steps")
            st.markdown("1. **Column selection:** relevant fields kept from the original columns.\n"
                        "2. **Currency parsing:** charges and costs converted from text to numbers.\n"
                        "3. **Length-of-stay parsing:** numeric day counts from coded values such as “120+”.\n"
                        "4. **Invalid row removal:** records with missing key fields removed.\n"
                        "5. **De-duplication:** duplicate records removed to avoid double-counting.")

    st.markdown("""<div class="note"><b>Limitations.</b> Data is a sample of the full state file ·
    some severity values are missing · stays marked “120+” are capped at 120 days ·
    charges are not the same as actual costs.</div>""", unsafe_allow_html=True)
