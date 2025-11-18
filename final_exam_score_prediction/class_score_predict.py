
import numpy as np
import matplotlib.pyplot as plt

if __name__ == '__main__':
    midterm_range = np.array([0, 125])
    final_range = np.array([0, 100])

    # Load score data
    class_kr = np.loadtxt('C:\\Users\\josoo\\soowithpy\\final_exam_score_prediction\\data\\class_score_kr.csv', delimiter=',')
    class_en = np.loadtxt('C:\\Users\\josoo\\soowithpy\\final_exam_score_prediction\\data\\class_score_en.csv', delimiter=',')
    data = np.vstack((class_kr, class_en))

    # Separate x(midterm) and y(final)
    x = data[:, 0]
    y = data[:, 1]

    # ---- Linear regression (manual least squares) ----
    x_mean = np.mean(x)
    y_mean = np.mean(y)

    numerator = np.sum((x - x_mean) * (y - y_mean))
    denominator = np.sum((x - x_mean) ** 2)

    slope = numerator / denominator
    intercept = y_mean - slope * x_mean

    line = [slope, intercept]


    # Predict scores
    final = lambda midterm: line[0] * midterm + line[1]
    while True:
        try:
            given = input('Q) Please input your midterm score (Enter or -1: exit)? ')
            if given == '' or float(given) < 0:
                break
            print(f'A) Your final score is expected to be {final(float(given)):.3f}.')
        except Exception as ex:
            print(f'Cannot answer the question. (message: {ex})')
            break

    # Plot scores and the estimated line
    plt.figure()
    plt.plot(data[:,0], data[:,1], 'r.', label='The given data')
    plt.plot(midterm_range, final(midterm_range), 'b-', label='Prediction')
    plt.xlabel('Midterm scores')
    plt.ylabel('Final scores')
    plt.xlim(midterm_range)
    plt.ylim(final_range)
    plt.grid()
    plt.legend()
    plt.show()
