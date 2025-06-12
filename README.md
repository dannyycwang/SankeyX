# SankeyX
A new visualization tool for clickstream data and prediciton model
<img width="616" alt="image" src="https://github.com/user-attachments/assets/9a15f2f1-1f7b-4e56-8a89-3f531c273b2b" />


## Abstract
In this study, we propose a novel visualization framework called SankeyX that connects user interaction sequences, model predictions, SHAP-based feature attributions, and business utility into a unified Sankey-style diagram. It enables users to trace how behavioral patterns contribute to model outcomes and assess their financial impact by a utility matrix. In case study, We also demonstrate its ability to reveal dominant purchasing patterns by using real world dataset. This method bridges the gap between explainable AI and decision-making for clickstream prediction.

## Demonstration

![image](https://github.com/user-attachments/assets/d278702e-fe14-4103-8933-783a90ae7ed2)


## Dataset

Comes from Coveo dataset: https://github.com/coveooss/shopper-intent-prediction-nature-2020


# Clickstream SankeyX

**Advanced Clickstream Visualization & Explainability Tool**  
*Python 3.8+ | Plotly | pandas | MIT License*

---

## 🌟 Why Clickstream SankeyX?

- ⚡ **Visualize User Journeys**: Transform raw clickstream sequences into intuitive, interactive Sankey diagrams.
- 🔍 **Explain ML Decisions**: Integrate SHAP values, utility outcomes, and intent clustering for model explainability.
- 🧑‍💻 **Research-Grade**: Modular codebase for research, demos, and academic experiments.
- 🔧 **Fully Customizable**: Adapt color maps, event logic, and sequence filters to your dataset.
- 🚀 **Ready to Extend**: Clean module structure for integration with Jupyter, Streamlit, or web apps.

---

## 🚀 Key Features

- **Interactive Sankey Visualization**  
  Visualize thousands of user journeys with event- and intent-level color mapping.
- **ML Outcome Integration**  
  Map prediction outcomes (TP, TN, FP, FN) and utility scores directly in the Sankey graph.
- **SHAP Value Support**  
  Overlay feature importance (SHAP) values onto sequence flows.
- **Customizable Event & Intent Types**  
  Easily map new event types, user intents, or outcome logic for your business case.
- **Plug & Play Python API**  
  Modular structure for drop-in usage and fast experimentation.

---

## 🏗️ Project Structure

```text
clickstream_sankey/
    __init__.py
    data_utils.py      # Data loading & preprocessing
    sankey_builder.py  # Sankey graph construction
    config.py          # Color maps & constants
example_run.py         # Example usage script
requirements.txt       # Dependencies
README.md              # Documentation (this file)
