import plotly.graph_objects as go

def build_sankey(records, event_color_map, outcome_color_map, intent_color_map, utility_node_color, intent_flow_color, separate_mode=True):
    nodes, node_labels, node_colors, node_idx = [], [], [], {}
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

    sources, targets, values, colors, link_labels = [], [], [], [], []

    for sidx, record in enumerate(records):
        seq = record['sequence']
        shap_seq = record['shap']
        filtered = [(e, s) for e, s in zip(seq, shap_seq) if e != 0]
        if not filtered: continue

        intent = record['intent']
        group_intent_node = f'GROUP_INTENT_{intent}'
        if group_intent_node not in node_idx:
            nodes.append(group_intent_node)
            node_labels.append(intent)
            node_colors.append(intent_color_map.get(intent, '#ffe066'))
            node_idx[group_intent_node] = len(nodes) - 1

        prev = None
        for step_idx, (event, shap) in enumerate(filtered):
            curr_node = f'{sidx}_step{step_idx}' if separate_mode else f'group_{step_idx}_{event}'
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
            colors.append('#888888' if last_shap >= 0 else '#ffb6c1')
            link_labels.append('')
            sources.append(node_idx[outcome_node])
            targets.append(node_idx['UTILITY'])
            values.append(abs(record['utility']))
            colors.append('#27ae60' if record['utility'] > 0 else '#e63946' if record['utility'] < 0 else '#bfc0c0')
            link_labels.append('')

    total_utility = sum([r['utility'] for r in records])
    node_labels[node_idx['UTILITY']] = f'Utility: {total_utility:.2f}'
    fig = go.Figure(go.Sankey(
        arrangement="snap",
        node=dict(
            pad=15, thickness=20, line=dict(color="black", width=0.5),
            label=node_labels, color=node_colors,
        ),
        link=dict(
            source=sources, target=targets, value=values,
            color=colors, label=link_labels
        )
    ))
    return fig

