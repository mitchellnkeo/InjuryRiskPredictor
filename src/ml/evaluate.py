"""
Model Evaluation Module for Injury Risk Predictor

Provides comprehensive evaluation metrics and visualizations.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, confusion_matrix, classification_report,
    roc_curve, precision_recall_curve
)
from typing import Dict, Tuple, Optional
import os


def calculate_metrics(y_true, y_pred, y_proba=None) -> Dict[str, float]:
    """
    Calculate comprehensive evaluation metrics.
    
    Args:
        y_true: True labels
        y_pred: Predicted labels
        y_proba: Predicted probabilities (for ROC-AUC)
    
    Returns:
        Dictionary of metrics
    """
    metrics = {
        'accuracy': accuracy_score(y_true, y_pred),
        'precision': precision_score(y_true, y_pred, zero_division=0),
        'recall': recall_score(y_true, y_pred, zero_division=0),
        'f1': f1_score(y_true, y_pred, zero_division=0)
    }
    
    if y_proba is not None:
        # For binary classification, use probability of positive class
        if y_proba.ndim > 1:
            y_proba_pos = y_proba[:, 1]
        else:
            y_proba_pos = y_proba
        
        try:
            metrics['roc_auc'] = roc_auc_score(y_true, y_proba_pos)
        except ValueError:
            metrics['roc_auc'] = 0.0  # Handle case with only one class
    
    return metrics


def evaluate_model(model, X, y, model_name="Model") -> Dict[str, float]:
    """
    Evaluate a model and return metrics.
    
    Args:
        model: Trained model (must have predict and predict_proba methods)
        X: Feature matrix
        y: True labels
        model_name: Name of the model (for display)
    
    Returns:
        Dictionary of evaluation metrics
    """
    y_pred = model.predict(X)
    
    # Get probabilities if available
    y_proba = None
    if hasattr(model, 'predict_proba'):
        try:
            y_proba = model.predict_proba(X)
        except:
            pass
    
    metrics = calculate_metrics(y, y_pred, y_proba)
    metrics['model_name'] = model_name
    
    return metrics


def create_confusion_matrix(y_true, y_pred, model_name="Model", 
                           save_path=None) -> np.ndarray:
    """
    Create and optionally save confusion matrix visualization.
    
    Args:
        y_true: True labels
        y_pred: Predicted labels
        model_name: Name of the model
        save_path: Path to save figure (optional)
    
    Returns:
        Confusion matrix array
    """
    cm = confusion_matrix(y_true, y_pred)
    
    fig, ax = plt.subplots(figsize=(8, 6))
    im = ax.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
    ax.figure.colorbar(im, ax=ax)
    
    # Add text annotations
    thresh = cm.max() / 2.
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            ax.text(j, i, format(cm[i, j], 'd'),
                   ha="center", va="center",
                   color="white" if cm[i, j] > thresh else "black")
    
    ax.set(xticks=np.arange(cm.shape[1]),
           yticks=np.arange(cm.shape[0]),
           xticklabels=['Not Injured', 'Injured'],
           yticklabels=['Not Injured', 'Injured'],
           title=f'Confusion Matrix - {model_name}',
           ylabel='True Label',
           xlabel='Predicted Label')
    
    plt.tight_layout()
    
    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    plt.close()
    
    return cm


def plot_roc_curve(y_true, y_proba, model_name="Model", save_path=None):
    """
    Plot ROC curve.
    
    Args:
        y_true: True labels
        y_proba: Predicted probabilities
        model_name: Name of the model
        save_path: Path to save figure (optional)
    """
    if y_proba.ndim > 1:
        y_proba_pos = y_proba[:, 1]
    else:
        y_proba_pos = y_proba
    
    fpr, tpr, thresholds = roc_curve(y_true, y_proba_pos)
    roc_auc = roc_auc_score(y_true, y_proba_pos)
    
    plt.figure(figsize=(8, 6))
    plt.plot(fpr, tpr, color='darkorange', lw=2, 
             label=f'ROC curve (AUC = {roc_auc:.2f})')
    plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--', label='Random')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title(f'ROC Curve - {model_name}')
    plt.legend(loc="lower right")
    plt.grid(True, alpha=0.3)
    
    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    plt.close()


def plot_precision_recall_curve(y_true, y_proba, model_name="Model", save_path=None):
    """
    Plot Precision-Recall curve.
    
    Args:
        y_true: True labels
        y_proba: Predicted probabilities
        model_name: Name of the model
        save_path: Path to save figure (optional)
    """
    if y_proba.ndim > 1:
        y_proba_pos = y_proba[:, 1]
    else:
        y_proba_pos = y_proba
    
    precision, recall, thresholds = precision_recall_curve(y_true, y_proba_pos)
    
    plt.figure(figsize=(8, 6))
    plt.plot(recall, precision, color='blue', lw=2)
    plt.xlabel('Recall')
    plt.ylabel('Precision')
    plt.title(f'Precision-Recall Curve - {model_name}')
    plt.grid(True, alpha=0.3)
    
    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    plt.close()


def compare_models(model_results: Dict[str, Dict[str, float]]) -> pd.DataFrame:
    """
    Create comparison table of multiple models.
    
    Args:
        model_results: Dictionary of model_name -> metrics_dict
    
    Returns:
        DataFrame with model comparison
    """
    comparison_data = []
    
    for model_name, metrics in model_results.items():
        comparison_data.append({
            'Model': model_name,
            'Accuracy': metrics.get('accuracy', 0),
            'Precision': metrics.get('precision', 0),
            'Recall': metrics.get('recall', 0),
            'F1-Score': metrics.get('f1', 0),
            'ROC-AUC': metrics.get('roc_auc', 0)
        })
    
    df = pd.DataFrame(comparison_data)
    df = df.round(3)
    df = df.sort_values('ROC-AUC', ascending=False)
    
    return df


def print_evaluation_report(y_true, y_pred, y_proba=None, model_name="Model"):
    """
    Print comprehensive evaluation report.
    
    Args:
        y_true: True labels
        y_pred: Predicted labels
        y_proba: Predicted probabilities (optional)
        model_name: Name of the model
    """
    print(f"\n{'='*60}")
    print(f"Evaluation Report: {model_name}")
    print(f"{'='*60}")
    
    metrics = calculate_metrics(y_true, y_pred, y_proba)
    
    print(f"\nMetrics:")
    print(f"  Accuracy:  {metrics['accuracy']:.3f}")
    print(f"  Precision: {metrics['precision']:.3f}")
    print(f"  Recall:    {metrics['recall']:.3f}")
    print(f"  F1-Score:  {metrics['f1']:.3f}")
    if 'roc_auc' in metrics:
        print(f"  ROC-AUC:   {metrics['roc_auc']:.3f}")
    
    print(f"\nClassification Report:")
    print(classification_report(y_true, y_pred, target_names=['Not Injured', 'Injured']))
    
    cm = confusion_matrix(y_true, y_pred)
    print(f"\nConfusion Matrix:")
    print(f"                Predicted")
    print(f"              Not Inj  Injured")
    print(f"Actual Not Inj   {cm[0,0]:4d}    {cm[0,1]:4d}")
    print(f"       Injured    {cm[1,0]:4d}    {cm[1,1]:4d}")
    
    print(f"\n{'='*60}\n")
