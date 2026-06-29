# ⚽ World Cup 2026 Group Stage Analytics Pipeline

An end-to-end Data Science and Machine Learning project that scrapes, processes, and analyzes team performance data from the World Cup 2026 Group Stage using automated web scraping and unsupervised learning.

---

## 🚀 Project Overview

This repository contains a full pipeline designed to extract statistical data for all 48 competing national teams from **FotMob**, perform advanced feature engineering to develop custom football metrics, and segment teams using tactical clustering.

### Key Features
*   **Automated Web Scraping:** Navigates and extracts data across 28 distinct statistical sub-cards using `Selenium` and `BeautifulSoup`.
*   **Feature Engineering:** Creates custom performance indicators including *Attack Efficiency*, *Defensive Stability*, a *Wastefulness Index*, and a comprehensive *Power Score*.
*   **Machine Learning (Clustering):** Uses `K-Means` clustering to group national teams into 5 distinct tactical profiles based on underlying metrics (xG, possession, defensive intensity).
*   **Data Visualization:** Includes automated scripts to generate correlation heatmaps, possession vs. goals scatter plots, and distribution charts.

---

## 🛠️ Tech Stack

*   **Language:** Python 3.x
*   **Scraping & Automation:** Selenium, BeautifulSoup4
*   **Data Manipulation:** Pandas, NumPy
*   **Machine Learning:** Scikit-Learn (StandardScaler, KMeans)
*   **Visualization:** Matplotlib, Seaborn

---

## 📊 Engineered Metrics Explained

The project goes beyond surface-level stats by introducing engineered metrics:
*   **Power Score:** A master composite weight combining expected goals (xG), defensive stability, and points to rank team dominance (Spain, Canada, and England topped this index).
*   **Attack Efficiency:** Measures the ratio of actual goals scored to Expected Goals ($Goals / xG$).
*   **Wastefulness Index:** Quantifies high possession rates that fail to convert into high-quality scoring opportunities.

---


