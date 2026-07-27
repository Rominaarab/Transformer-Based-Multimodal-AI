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

# **Demo file**

---

# Causal Multi-Omics Transformer (CMO-Transformer) - Demo & Validation Suite

This repository serves as a **lightweight demo and validation environment** for the **Causal Multi-Omics Transformer (CMO-Transformer)** project. It includes synthetic multi-omics data generation, model architecture prototyping, baseline benchmarking against established single-cell and traditional ML architectures, interpretability tools, and clinical utility decision-curve analysis.

---

## 📌 Project Overview

This demo repository allows researchers and developers to run, inspect, and benchmark the complete pipeline without requiring massive TCGA or GEO datasets. It demonstrates how multi-modal omics data (m6A regulators, lncRNAs, miRNAs, circRNAs, metabolic pathways, and immune checkpoints) interact through cross-attention and causal inference modules.

### Key Demo Capabilities:

* **Synthetic Data Engine:** Generates realistic, correlated multi-omics matrices ($N=500$ default) reflecting realistic non-small cell lung cancer (NSCLC) response distributions.
* **Architectural Benchmarking:** Evaluates the **CMO-Transformer** against baseline model architectures:
* *GeneformerLite* (Transformer)
* *scBERTMini* (Transformer with `[CLS]` token)
* *GNNOmics* (Graph Convolutional Network)
* *Random Forest & Logistic Regression*


* **Interpretability & Causal Discovery:** Extracts and visualizes cross-modal attention maps and learned inter-modality causal adjacency matrices.
* **Decision Curve & Clinical Utility Analysis:** Evaluates net clinical benefit across decision thresholds.
* **Cloud-Ready Configuration:** Built with optional AWS SageMaker and S3 integration support (`boto3` / `sagemaker`).

---

## 🏗️ Model & Pipeline Architecture

```
                                  [ MULTI-OMICS INPUTS ]
  ┌──────────┬──────────┬──────────┬──────────┬─────────────┬──────────┐
  │   m6A    │  lncRNA  │  miRNA   │ circRNA  │  Metabolic  │  Immune  │
  └────┬─────┴────┬─────┴────┬─────┴────┬─────┴──────┬──────┴────┬─────┘
       │          │          │          │            │           │
       ▼          ▼          │          ▼            ▼           ▼
  ┌────────────────────────────────────────────────────────────────────┐
  │                   Modality-Specific Encoders                        │
  └─────────────────────────────────┬──────────────────────────────────┘
                                    │
                                    ▼
  ┌────────────────────────────────────────────────────────────────────┐
  │               Multi-Layer Cross-Modal Attention                    │
  └─────────────────────────────────┬──────────────────────────────────┘
                                    │
                                    ▼
  ┌────────────────────────────────────────────────────────────────────┐
  │                 Causal Inference Adjacency Module                  │
  └─────────────────────────────────┬──────────────────────────────────┘
                                    │
                                    ▼
  ┌────────────────────────────────────────────────────────────────────┐
  │               Fused Representation & Classifier                    │
  └─────────────────────────────────┬──────────────────────────────────┘
                                    │
                                    ▼
                     [ Immunotherapy Response (0 / 1) ]

```

---

## 🚀 Quick Start

### 1. Requirements & Dependencies

The codebase requires Python **3.10+** and key PyTorch/Scikit-learn libraries:

```bash
pip install torch torchvision torchaudio \
            pandas numpy scikit-learn \
            matplotlib seaborn tqdm \
            boto3 sagemaker shap

```

### 2. Execution

To run the demo pipeline end-to-end:

```bash
python main.py

```

*(Or execute all cells in your Colab/Jupyter Notebook interface)*

---

## 📊 Evaluation & Comparative Results

The demo suite runs automated cross-model evaluation on the synthetic test set:

| Model Architecture | Accuracy | F1 Macro / Score | AUROC / ROC-AUC |
| --- | --- | --- | --- |
| **CMO-Transformer** | **0.7800** | **0.8736** (F1) | **0.5981** |
| **GNN-Model** | 0.8000 | 0.4444 (F1 Macro) | 0.5769 |
| **Random Forest** | 0.8000 | 0.8889 (F1) | 0.5397 |
| **scBERT** | 0.2000 | 0.1667 (F1 Macro) | 0.5450 |
| **Logistic Regression** | 0.7800 | 0.8721 (F1) | 0.5013 |
| **Geneformer** | 0.7500 | 0.4286 (F1 Macro) | 0.4106 |

---

## 🖼️ Generated Outputs & Artifacts

All outputs and diagnostic figures are automatically saved to `results/` and `models/`:

* `eda_dashboard.png`: Feature distributions, heatmaps, and PCA projection.
* `training_history.png`: Training vs. Validation loss and accuracy curves over epochs.
* `evaluation_results.png`: ROC curve, Precision-Recall curve, Confusion Matrix, and Probability distributions.
* `model_comparison.png`: Performance bar-chart comparing CMO-Transformer against all baselines.
* `causal_relationships.png`: Learned inter-modal causal adjacency matrix.
* `feature_importance.png`: Modality and gene-level importance rankings.
* `clinical_utility.png`: Decision Curve Analysis (DCA) and net benefit chart.
* `results_summary.json` & `complete_results.pkl`: Structured metric dumps.

---

## 📂 Codebase Structure

```text
├── data/                    # Generated synthetic input files
├── models/                  # Saved model checkpoints (best_model.pth)
├── results/                 # Evaluation graphics, JSON summaries, and pickles
├── main.py / notebook       # Demo script & execution logic
└── README.md                # Project documentation

```

---

## 👤 Author

**Romina Arab**

* GitHub: [@Rominaarab](https://www.google.com/search?q=https://github.com/Rominaarab)

---
