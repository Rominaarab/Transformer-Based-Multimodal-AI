"""Compute permutation SHAP for a fitted classifier with a probability callable."""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import shap


def explain_probability(predict_positive, train_features, test_features, output_dir):
    """Pass numeric DataFrames and a callable returning P(response) per row.

    For a multimodal model the callable must rebuild its modality tensors in
    the original feature order and invoke the frozen model in evaluation mode.
    Fit preprocessing and the model before calling this function.
    """
    if not train_features.columns.is_unique or not train_features.columns.equals(test_features.columns):
        raise ValueError("Train and test must have the same ordered, unique feature names.")
    if train_features.empty or test_features.empty:
        raise ValueError("SHAP needs nonempty training and held-out feature matrices.")
    if not np.isfinite(train_features.to_numpy()).all() or not np.isfinite(test_features.to_numpy()).all():
        raise ValueError("SHAP requires finite numeric features after preprocessing.")
    if not train_features.index.intersection(test_features.index).empty:
        raise ValueError("Use disjoint patient IDs for training and held-out explanations.")

    def predict(values):
        frame = pd.DataFrame(values, columns=train_features.columns)
        scores = np.asarray(predict_positive(frame), dtype=float)
        if scores.shape != (len(frame),) or not np.isfinite(scores).all():
            raise ValueError("Return one finite positive-class probability per input row.")
        if ((scores < 0) | (scores > 1)).any():
            raise ValueError("Positive-class probabilities must be between zero and one.")
        return scores

    background = train_features.sample(n=min(len(train_features), 32), random_state=42)
    explainer = shap.Explainer(predict, background, algorithm="permutation", seed=42)
    values = explainer(test_features, max_evals=5 * (2 * test_features.shape[1] + 1))
    np.testing.assert_allclose(
        values.base_values + values.values.sum(axis=1), predict(test_features),
        atol=1e-5, rtol=1e-5,
    )

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    importance = pd.Series(
        np.abs(values.values).mean(axis=0), index=test_features.columns, name="mean_abs_shap"
    ).sort_values(ascending=False)
    importance.to_csv(output_dir / "shap_importance.csv", index_label="feature")
    shap.plots.beeswarm(values, show=False)
    plt.savefig(output_dir / "shap_beeswarm.png", dpi=200, bbox_inches="tight")
    plt.close()
    return values
