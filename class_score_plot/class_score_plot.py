import matplotlib.pyplot as plt
import numpy as np
def read_data(filename):
    data = []
    with open(filename, 'r') as f:
        for line in f.readlines():
            if not line.startswith('#'): # If 'line' is not a header
                data.append([int(word) for word in line.split(',')])
    return data

if __name__ == '__main__':
    fig, axes = plt.subplots(2, 1, figsize=(8, 10))

    # Load score data
    class_kr = read_data('C:\\Users\\josoo\\soowithpy\\class_score_plot\\data\\class_score_kr.csv')
    class_en = read_data('C:\\Users\\josoo\\soowithpy\\class_score_plot\\data\\class_score_en.csv')

    # Prepare midterm, final, and total scores
    midterm_kr, final_kr = zip(*class_kr)
    total_kr = [40/125*midterm + 60/100*final for (midterm, final) in class_kr]
    midterm_en, final_en = zip(*class_en)
    total_en = [40/125*midterm + 60/100*final for (midterm, final) in class_en]

    # Plot midterm/final scores as points (scatter plot)
    axes[0].scatter(midterm_kr, final_kr, label='Korean', color='red')
    axes[0].scatter(midterm_en, final_en, label='English', color='blue', marker='x')
    axes[0].set_xlabel('Midterm Score')
    axes[0].set_ylabel('Final Score')
    axes[0].legend()

    # Plot total scores as a histogram
    all_scores = total_kr + total_en
    min_score = int(min(all_scores))
    max_score = int(max(all_scores))
    bins = np.arange(min_score, max_score + 5, 5)
    axes[1].hist(total_kr, bins=bins, alpha=0.5, label='Korean', color='red')
    axes[1].hist(total_en, bins=bins, alpha=0.5, label='English', color='blue')
    axes[1].set_xlabel('Total Score')
    axes[1].set_ylabel('Number of Students')
    axes[1].legend()

    plt.tight_layout()
    plt.show()