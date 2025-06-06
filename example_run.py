from clickstream_sankey.data_utils import load_and_preprocess
from clickstream_sankey.config import (
    event_color_map, outcome_color_map, intent_color_map, 
    utility_node_color, intent_flow_color, utility_dict
)
from clickstream_sankey.sankey_builder import build_sankey

# Step 1: 載入資料
df = load_and_preprocess('shap_sampled_200.csv')

# Step 2: 篩選 (如需)
num_sessions = 10
session_mode = 'first'
intent_filter = None
if intent_filter:
    filtered = df[df['Intent_type'] == intent_filter]
else:
    filtered = df
selected = filtered.head(num_sessions) if session_mode == 'first' else filtered.tail(num_sessions)

# Step 3: 轉 record 結構
records = []
for _, row in selected.iterrows():
    seq = list(row['truncated_sequence'])[-5:]
    seq_len = len(seq)
    all_shap_values = [row.get(f'SHAP_{i}', 0.0) for i in range(1, 21)]
    shap_values = [v * 10 for v in (all_shap_values[-seq_len:] if seq_len > 0 else [])]
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

# Step 4: 畫 Sankey
fig = build_sankey(
    records, event_color_map, outcome_color_map, intent_color_map,
    utility_node_color, intent_flow_color, separate_mode=True
)

fig.show()
