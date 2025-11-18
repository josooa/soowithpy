import numpy as np
import matplotlib.pyplot as plt
from sklearn import metrics
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, balanced_accuracy_score
from matplotlib.lines import Line2D  # For the custom legend

def load_wdbc_data(filename):
    class WDBCData:
        data = []          # will become numpy array shape (n_samples, 30)
        target = []        # will become numpy array shape (n_samples,)
        target_names = ['malignant', 'benign']
        feature_names = ['mean radius', 'mean texture', 'mean perimeter', 'mean area', 'mean smoothness', 'mean compactness', 'mean concavity', 'mean concave points', 'mean symmetry', 'mean fractal dimension',
                         'radius error', 'texture error', 'perimeter error', 'area error', 'smoothness error', 'compactness error', 'concavity error', 'concave points error', 'symmetry error', 'fractal dimension error',
                         'worst radius', 'worst texture', 'worst perimeter', 'worst area', 'worst smoothness', 'worst compactness', 'worst concavity', 'worst concave points', 'worst symmetry', 'worst fractal dimension']
    wdbc = WDBCData()
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            items = line.split(',')
            # items[1] is label: 'M' or 'B'
            label = items[1].upper()
            # Map: 0 for malignant (M), 1 for benign (B/others)
            if label == 'M':
                wdbc.target.append(0)
            else:
                wdbc.target.append(1)
            # items[2:] are 30 attributes as strings -> convert to float
            attrs = [float(x) for x in items[2:2+30]]
            wdbc.data.append(attrs)
    wdbc.data = np.array(wdbc.data, dtype=float)
    wdbc.target = np.array(wdbc.target, dtype=int)
    return wdbc

if __name__ == '__main__':
    # Load a dataset
    wdbc = load_wdbc_data('wdbc_classification\data\wdbc.data')

    # Split to train/test to get a realistic evaluation
    X_train, X_test, y_train, y_test = train_test_split(
        wdbc.data, wdbc.target, test_size=0.25, random_state=42, stratify=wdbc.target)

    # Scale features
    scaler = StandardScaler()
    X_train_s = scaler.fit_transform(X_train)
    X_test_s = scaler.transform(X_test)
    X_all_s = scaler.transform(wdbc.data)

    # Train a stronger model (Random Forest)
    model = RandomForestClassifier(n_estimators=200, random_state=42, n_jobs=-1)
    model.fit(X_train_s, y_train)

    # Test the model
    predict_test = model.predict(X_test_s)
    accuracy = balanced_accuracy_score(y_test, predict_test)

    # Visualize the confusion matrix (test set)
    cm = confusion_matrix(y_test, predict_test, labels=[0, 1])
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=wdbc.target_names)
    plt.figure(figsize=(5, 4))
    disp.plot(cmap='Blues', values_format='d', colorbar=False)
    plt.title(f'Confusion Matrix (Balanced Acc: {accuracy:.3f})')
    plt.tight_layout()

    # Also prepare a scatter visualization using two features (example: feature 0 vs 1)
    cmap = np.array([(1, 0, 0), (0, 1, 0)])  # red for malignant(0), green for benign(1)
    clabel = [Line2D([0], [0], marker='o', lw=0, label=wdbc.target_names[i], color=cmap[i]) for i in range(len(cmap))]

    # Predict on all data for edgecolors to indicate model output
    predict_all = model.predict(X_all_s)

    for (x, y) in [(0, 1)]:  # try other pairs like (2,3) or [(i, i+1) for i in range(0,30,2)]
        plt.figure()
        plt.title(f'My Classifier (Balanced Acc on test: {accuracy:.3f})')
        plt.scatter(wdbc.data[:, x], wdbc.data[:, y], c=cmap[wdbc.target], edgecolors=cmap[predict_all], alpha=0.8)
        plt.xlabel(wdbc.feature_names[x])
        plt.ylabel(wdbc.feature_names[y])
        plt.legend(handles=clabel, framealpha=0.5)
    plt.show()