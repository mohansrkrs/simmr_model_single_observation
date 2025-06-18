# 🧪 Bayesian Mixing Model Demo (δ¹⁸O and δ²H)

An interactive [Streamlit](https://streamlit.io/) dashboard to demonstrate how stable isotope data (δ¹⁸O and δ²H) can be used to estimate fractional contributions from multiple sources using a Bayesian mixing model.

This tool simulates the functionality of the `simmr` model and allows to visualize posterior distributions of source contributions based on single isotope input (a very simpler model).

---

## 🚀 Features

- Input observed isotope values (δ¹⁸O and δ²H)
- Define source means and standard deviations
- Use Dirichlet priors to sample mixing proportions
- Compute posterior distributions using likelihood
- Visualize results with interactive KDE plots

---

## 🧮 Model Summary

We assume a mixture is formed from 3 sources with unknown proportions. For each sample of proportions drawn from a Dirichlet distribution:

- Expected δ¹⁸O and δ²H values are computed
- Likelihoods are calculated assuming normal distribution
- Posterior weights are obtained and visualized

---

## 📊 How to Use

1. Launch the app from Streamlit Cloud  
   👉 [App Link](https://your-username.streamlit.app/) *(update after deploying)*

2. Adjust inputs in the sidebar:
   - Observed mixture δ¹⁸O and δ²H
   - Source means for each isotope
   - Source standard deviations

3. View the posterior distributions of source contributions.

---

## 🛠️ Installation (Local)

```bash
git clone https://github.com/your-username/simmr-interactive.git
cd simmr-interactive
pip install -r requirements.txt
streamlit run streamlit_app.py
