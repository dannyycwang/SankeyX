import streamlit as st
st.set_page_config(layout="wide")  # 一定要放在最前面

import pandas as pd
import plotly.graph_objects as go
import ast

# ----- Sidebar (精簡一點) -----
st.sidebar.title("SankeyX Panel")

# 上傳檔案
uploaded_file = st.sidebar.file_uploader("Upload CSV", type=["csv"])
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
else:
    st.info("Please upload a clickstream CSV file to begin.")
    st.stop()

# 控件
max_rows = df.shape[0]
num_sessions = st.sidebar.slider("N Sessions", 1, min(200, max_rows), 20)
max_steps = st.sidebar.slider("Max Steps (Clicks)", 1, 20, 5)  # 👈 新增這一個！
session_mode = st.sidebar.radio("Order", options=["first", "last"], index=0)
intent_types = ["All"] + sorted(df['Intent_type'].dropna().unique())
intent_filter = st.sidebar.selectbox("Intent Type", options=intent_types, index=0)
shap_mult = st.sidebar.slider("SHAP x", 1, 100, 10)
separate_mode = st.sidebar.checkbox("Separate Sessions", value=False)

st.sidebar.markdown("---")
st.sidebar.markdown("**Event Color**")
event_color_map = {
    1: st.sidebar.color_picker("Browse", "#1f77b4"),
    2: st.sidebar.color_picker("Detail", "#ffbe0b"),
    3: st.sidebar.color_picker("Add", "#43aa8b"),
    4: st.sidebar.color_picker("Remove", "#fb8500"),
    5: st.sidebar.color_picker("Purchase", "#3a86ff"),
}
intent_flow_color = st.sidebar.color_picker("Intent ➜ First Event", "#c8d6e5")

# ----- Main Title -----
st.title("SankeyX Clickstream Visualization")

# ---------- Data ----------
def safe_eval(val):
    try:
        return ast.literal_eval(val)
    except:
        return val

df['truncated_sequence'] = df['truncated_sequence'].apply(safe_eval)

if intent_filter != "All":
    filtered = df[df['Intent_type'] == intent_filter]
else:
    filtered = df

if session_mode == 'first':
    selected = filtered.head(num_sessions)
else:
    selected = filtered.tail(num_sessions)

# Colors
utility_dict = {
    (1, 1): 3,    # TP
    (1, 0): -1,   # FP
    (0, 1): -2.5, # FN
    (0, 0): 1e-6  # TN
}
outcome_color_map = {
    'TP':   '#06d6a0',
    'TN':   '#118ab2',
    'FP':   '#FF6B6B',
    'FN':   '#ffd166',
}
intent_color_map = {
    "Hesitant Buyer":         "#ffe066",
    "Comparative Buyer":      "#6c63ff",
    "Unclassified":           "#adb5bd",
    "Exploratory Buyer":      "#A3F7BF",
    "Intermittent Revisitor": "#9bf6ff",
    "Engaged Buyer":          "#ffb4a2",
    "Uncertain Buyer":        "#b983ff",
}
utility_node_color = "#457b9d"

# Sankey
records = []
for _, row in selected.iterrows():
    seq = list(row['truncated_sequence'])[-max_steps:]  # 👈 這裡改成 max_steps
    seq_len = len(seq)
    all_shap_values = [row.get(f'SHAP_{i}', 0.0) for i in range(1, 21)]
    shap_values = [v * shap_mult for v in (all_shap_values[-seq_len:] if seq_len > 0 else [])]
    y_pred = int(row['y_pred'])
    y_true = int(row['purchase'])
    intent = row['Intent_type']
    if y_pred == 1 and y_true == 1:
        outcome = 'TP'
    elif y_pred == 0 and y_true == 0:
        outcome = 'TN'
    elif y_pred == 1 and y_true == 0:
        outcome = 'FP'
    elif y_pred == 0 and y_true == 1:
        outcome = 'FN'
    utility = utility_dict[(y_pred, y_true)]
    records.append({
        'sequence': seq,
        'shap': shap_values,
        'y_pred': y_pred,
        'y_true': y_true,
        'outcome': outcome,
        'utility': utility,
        'intent': intent
    })

nodes = []
node_labels = []
node_colors = []
node_idx = {}

for out in ['TP', 'TN', 'FP', 'FN']:
    node_name = f'OUT_{out}'
    nodes.append(node_name)
    node_labels.append(out)
    node_colors.append(outcome_color_map[out])
    node_idx[node_name] = len(nodes) - 1

nodes.append('UTILITY')
node_labels.append('Utility')
node_colors.append(utility_node_color)
node_idx['UTILITY'] = len(nodes) - 1

sources = []
targets = []
values = []
colors = []
link_labels = []

for sidx, record in enumerate(records):
    seq = record['sequence']
    shap_seq = record['shap']
    filtered = [(e, s) for e, s in zip(seq, shap_seq) if e != 0]
    if len(filtered) == 0:
        continue

    intent = record['intent']
    group_intent_node = f'GROUP_INTENT_{intent}'
    if group_intent_node not in node_idx:
        nodes.append(group_intent_node)
        node_labels.append(intent)
        node_colors.append(intent_color_map.get(intent, "#ffe066"))
        node_idx[group_intent_node] = len(nodes) - 1

    prev = None

    for step_idx, (event, shap) in enumerate(filtered):
        if separate_mode:
            curr_node = f'{sidx}_step{step_idx}'
        else:
            curr_node = f'group_{step_idx}_{event}'
        if curr_node not in node_idx:
            nodes.append(curr_node)
            node_labels.append('')
            node_colors.append(event_color_map.get(event, '#cccccc'))
            node_idx[curr_node] = len(nodes) - 1

        if step_idx == 0:
            sources.append(node_idx[group_intent_node])
            targets.append(node_idx[curr_node])
            values.append(1)
            colors.append(intent_flow_color)
            link_labels.append('')

        if prev is not None:
            sources.append(node_idx[prev])
            targets.append(node_idx[curr_node])
            values.append(abs(shap) + 0.1)
            colors.append('#888888' if shap >= 0 else '#ffb6c1')
            link_labels.append('')
        prev = curr_node

    outcome_node = f'OUT_{record["outcome"]}'
    if prev is not None:
        last_shap = filtered[-1][1]
        sources.append(node_idx[prev])
        targets.append(node_idx[outcome_node])
        values.append(abs(last_shap) + 0.1)
        if last_shap >= 0:
            colors.append('#888888')
        else:
            colors.append('#ffb6c1')
        link_labels.append('')
        sources.append(node_idx[outcome_node])
        targets.append(node_idx['UTILITY'])
        values.append(abs(record['utility']))
        if record['utility'] > 0:
            colors.append('#27ae60')
        elif record['utility'] < 0:
            colors.append('#e63946')
        else:
            colors.append('#bfc0c0')
        link_labels.append('')

total_utility = sum([r['utility'] for r in records])
node_labels[node_idx['UTILITY']] = f'Utility: {total_utility:.2f}'

fig = go.Figure(go.Sankey(
    arrangement="snap",
    node=dict(
        pad=15,
        thickness=20,
        line=dict(color="black", width=0.5),
        label=node_labels,
        color=node_colors,
    ),
    link=dict(
        source=sources,
        target=targets,
        value=values,
        color=colors,
        label=link_labels
    )
))

# Legend (event only, 下方置中)
# ...上面不變...

# Legend (event only, 下方置中)
event_legend_items = [
    ("Browse", event_color_map[1]),
    ("Detail", event_color_map[2]),
    ("Add", event_color_map[3]),
    ("Remove", event_color_map[4])
]
legend_x = 1.13
legend_y_start = 0.98
legend_box_height = 0.045
legend_box_width = 0.045
legend_dy = 0.09

fig.layout.shapes = []
fig.layout.annotations = []

for i, (text, color) in enumerate(event_legend_items):
    box_y_top = legend_y_start - legend_dy * i
    box_y_bottom = box_y_top - legend_box_height

    fig.add_shape(
        type="rect",
        xref="paper", yref="paper",
        x0=legend_x, x1=legend_x + legend_box_width,
        y0=box_y_bottom, y1=box_y_top,
        fillcolor=color,
        line=dict(width=1, color="#22334b"),
        layer='above'
    )
    fig.add_annotation(
        x=legend_x + legend_box_width / 2,
        y=box_y_bottom - 0.012,
        xref="paper", yref="paper",
        showarrow=False,
        font=dict(size=12, family="Arial", color="#22334b"),
        text=text,
        align='center',
        xanchor='center',
        yanchor='top',
        bgcolor="rgba(255,255,255,0)"
    )


fig.update_layout(
    title_text="SankeyX Clickstream Visualization",
    font_size=15,
    font_family="Arial",
    font_color="#222222",
    width=1400,
    height=700,
    plot_bgcolor="white",
    paper_bgcolor="white",
    margin=dict(l=20, r=200, t=70, b=40),  # 讓主畫面更寬
)

st.plotly_chart(fig, use_container_width=True)
