import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import norm

# Set Streamlit page config
st.set_page_config(layout="wide", page_title="Bayesian Mixing Model")

# Global font settings for matplotlib
plt.rcParams.update({
    'font.size': 14,
    'axes.labelsize': 16,
    'axes.titlesize': 18,
    'legend.fontsize': 14,
    'xtick.labelsize': 13,
    'ytick.labelsize': 13
})

st.title("🌊 Bayesian Mixing Model (δ¹⁸O & δ²H) - Interactive")

# --- Sidebar Inputs ---

st.sidebar.header("🔢 Input Observed Mixture (δ Values)")

obs_o18 = st.sidebar.number_input("Observed δ¹⁸O", value=-6.0, step=0.1, format="%.2f")
obs_h2  = st.sidebar.number_input("Observed δ²H", value=-40.0, step=0.5, format="%.1f")

st.sidebar.markdown("---")
st.sidebar.header("📈 Measurement Uncertainty (Standard Deviation)")

sd_o18 = st.sidebar.number_input("σ(δ¹⁸O)", value=0.5, min_value=0.01, step=0.1, format="%.2f")
sd_h2  = st.sidebar.number_input("σ(δ²H)", value=2.0, min_value=0.1, step=0.5, format="%.1f")

st.sidebar.markdown("---")
st.sidebar.header("🧪 Source Isotope Values")

source_labels = ['S1', 'S2', 'S3']
sources_mean_o18 = []
sources_mean_h2 = []

for i in range(3):
    with st.sidebar.expander(f"Source {source_labels[i]}"):
        o18 = st.number_input(f"{source_labels[i]} δ¹⁸O", value=[-8.0, -5.5, -7.0][i], step=0.1, format="%.2f", key=f"o18_{i}")
        h2  = st.number_input(f"{source_labels[i]} δ²H", value=[-60.0, 30.0, -55.0][i], step=1.0, format="%.1f", key=f"h2_{i}")
        sources_mean_o18.append(o18)
        sources_mean_h2.append(h2)

# --- Bayesian Mixing Model Calculation ---

alpha = [1, 1, 1]  # Uniform prior
n_samples = 5000

# Generate random proportions
proportions = np.random.dirichlet(alpha, size=n_samples)

# Predict isotope values
pred_o18 = proportions @ np.array(sources_mean_o18)
pred_h2  = proportions @ np.array(sources_mean_h2)

# Compute likelihoods and posterior weights
likelihoods = norm.pdf(obs_o18, loc=pred_o18, scale=sd_o18) * \
              norm.pdf(obs_h2,  loc=pred_h2,  scale=sd_h2)

posterior_weights = likelihoods / np.sum(likelihoods)

# Create DataFrame for plotting
df = pd.DataFrame(proportions, columns=source_labels)
df['weights'] = posterior_weights

# --- Plotting ---
st.subheader("🎯 Posterior Distributions of Source Contributions")

fig, ax = plt.subplots(figsize=(12, 5))

for source in source_labels:
    sns.kdeplot(data=df, x=source, weights='weights', label=source, fill=True, common_norm=False, ax=ax)

ax.set_xlabel("Proportion")
ax.set_ylabel("Density")
ax.set_title("Posterior Distribution for Each Source", fontsize=16)
ax.legend()

st.pyplot(fig)

# Optional summary table
st.subheader("📊 Posterior Mean Source Contributions")
summary = df[source_labels].multiply(df['weights'], axis=0).sum().reset_index()
summary.columns = ['Source', 'Posterior Mean Proportion']
st.table(summary.style.format({'Posterior Mean Proportion': '{:.3f}'}))
