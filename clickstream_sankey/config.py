# colors and settings
event_color_map = {
    1: '#1f77b4', 2: '#ffbe0b', 3: '#43aa8b', 4: '#fb8500', 5: '#3a86ff',
}
outcome_color_map = {
    'TP':   '#06d6a0', 'TN':   '#118ab2', 'FP':   '#FF6B6B', 'FN':   '#ffd166',
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
intent_flow_color = "#c8d6e5"

utility_dict = {
    (1, 1): 3, (1, 0): -1, (0, 1): -2.5, (0, 0): 1e-6
}

