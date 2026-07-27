---

# Multi-Omics Causal Transformer for Non-Small Cell Lung Cancer (NSCLC)

This repository contains an end-to-end PyTorch-based pipeline that integrates multi-omics data (RNA-seq, miRNA, lncRNA, circRNA, pathway scores, and clinical metadata) using a **Causal Multi-Omics Transformer** architecture for predicting treatment response, survival outcomes, and cancer staging in Non-Small Cell Lung Cancer (NSCLC).

---

## 📌 Overview

Multi-omics integration is crucial for understanding complex cancer phenotypes and predicting clinical outcomes. This project implements a comprehensive deep learning pipeline featuring:

* **Automated Data Acquisition:** Downloads TCGA LUAD datasets (RNA-seq, miRNA, lncRNA) and GEO immunotherapy cohort data (`GSE135222`).
* **Data Preprocessing & Quality Control:** Implements variance filtering, KNN imputation, and gene/sample-wise Z-score normalization.
* **Pathway Enrichment:** Runs Gene Set Variation Analysis (**GSVA**) via R integration (`rpy2`) with fallback to mean expression scoring across key metabolic, immune checkpoint, and m6A regulator pathways.
* **Causal Multi-Omics Transformer:**
* **Modality Encoders:** Dedicated linear and transformer-based encoders tailored to specific omics inputs.
* **Cross-Modal Attention:** Captures inter-modality dependencies across omics features.
* **Causal Inference Module:** Estimates causal adjacency matrices and inter-modal intervention effects.


* **Multi-Task Learning:** Simultaneously predicts immunotherapy response, overall survival time, and disease stage.

---

## 🏗️ Model Architecture

```
[ RNA-seq ] ───► Modality Encoder (RNA) ──────┐
[ lncRNA  ] ───► Modality Encoder (RNA) ──────┤
[ miRNA   ] ───► Modality Encoder (RNA) ──────┼──► Cross-Modal ──► Causal Inference ──► Multi-Task Heads
[ circRNA ] ───► Modality Encoder (RNA) ──────┤    Attention         & Feature Fusion     ├─ Classification (Stage)
[ Pathways] ───► Modality Encoder (Generic) --┤                                           ├─ Response Prediction
[ Clinical] ───► Modality Encoder (Clinical) -┘                                           └─ Survival Time

```

---

## 🚀 Quick Start

### 1. Run in Google Colab

You can run the entire pipeline with GPU acceleration directly in Google Colab:

### 2. Local Setup

1. **Clone the repository:**
```bash
git clone https://github.com/Rominaarab/Machine-learning.git
cd Machine-learning

```


2. **System Prerequisites (R Environment for GSVA):**
```bash
sudo apt-get update
sudo apt-get install -y r-base r-base-dev

```


3. **Install Python Dependencies:**
```bash
pip install torch torchvision torchaudio \
            pandas numpy scikit-learn \
            matplotlib seaborn plotly \
            openpyxl requests rpy2

```


4. **Required Data Files:**
Ensure the following supplementary local files are placed in your working directory if running locally:
* `Suppl Table S2 circRNA data gene level.xlsx` (circRNA expression table)
* `clinical.tsv` (Clinical metadata for GSE135222)



---

## 📂 Pipeline Workflow

1. **Data Acquisition:** Downloads and parses TCGA-LUAD RNA-seq, miRNA, lncRNA, and GSE135222 datasets.
2. **Preprocessing:** Applies quality checks, drops non-informative genes, imputes missing values via KNN, and normalizes feature matrices.
3. **GSVA Pathway Analysis:** Computes activity scores for user-defined pathways:
* *Glycolysis*
* *Arginine, Tryptophan, & Glutamine Metabolism*
* *m6A Regulators*
* *Immune Checkpoints*


4. **Dataset Construction:** Merges overlapping sample identifiers across modalities into a unified PyTorch `Dataset` and `DataLoader`.
5. **Model Training & Evaluation:** Trains the `CausalMultiOmicsTransformer` using AdamW and validation-loss early stopping, followed by ROC-AUC and performance plotting.

---

## 📊 Evaluation & Visualization

The pipeline includes built-in functions for performance tracking and diagnostic plots:

* **Training vs. Validation Loss/Accuracy Curves** (`plot_training_history`)
* **Receiver Operating Characteristic (ROC-AUC)** curves for clinical response prediction.

---

## 🛠️ Tech Stack

* **Deep Learning:** PyTorch
* **Machine Learning & Data Processing:** Scikit-Learn, Pandas, NumPy, OpenPyXL
* **R Integration:** `rpy2` (Bioconductor GSVA)
* **Visualization:** Matplotlib, Seaborn, Plotly

---

## 👤 Author

**Romina Arab**

* GitHub: [@Rominaarab](https://www.google.com/search?q=https://github.com/Rominaarab)

---
