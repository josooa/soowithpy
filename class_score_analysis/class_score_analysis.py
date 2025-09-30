def read_data(filename):
    # TODO) Read `filename` as a list of integers
    data = []
    f = open(filename, 'r')
    lines = f.readlines()[1:] # Skip the header line
    for line in lines:
        items = line.strip().split(',')
        if len(items) == 2:
             data.append((int(items[0]), int(items[1])))
    
    return data

def calc_weighted_average(data_2d, weight):
    # TODO) Calculate the weighted averages of each row of `data_2d`
    average = []
    for row in data_2d:
        average.append(float(row[0]) * weight[0] + float(row[1]) * weight[1])
    return average

def analyze_data(data_1d):
    # TODO) Calculate summary statistics of the given `data_1d`
    # Note) Please don't use NumPy and other libraries. Do it yourself.
    data_1d = sorted(data_1d)
    mean = sum(data_1d) / len(data_1d) if data_1d else 0
    var = sum((x - mean) ** 2 for x in data_1d) / len(data_1d) if data_1d else 0
    median = data_1d[len(data_1d) // 2] if data_1d else 0
    return mean, var, median, min(data_1d), max(data_1d)

if __name__ == '__main__':
    data = read_data('C:\\Users\\josoo\\soowithpy\\class_score_analysis\\data\\class_score_en.csv')
    if data and len(data[0]) == 2: # Check 'data' is valid
        average = calc_weighted_average(data, [40/125, 60/100])

        # Write the analysis report as a markdown file
        with open('C:\\Users\\josoo\\soowithpy\\class_score_analysis\\class_score_analysis.md', 'w') as report:
            report.write('### Individual Score\n\n')
            report.write('| Midterm | Final | Average |\n')
            report.write('| ------- | ----- | ----- |\n')
            for ((m_score, f_score), a_score) in zip(data, average):
                report.write(f'| {m_score} | {f_score} | {a_score:.3f} |\n')
            report.write('\n\n\n')

            report.write('### Examination Analysis\n')
            data_columns = {
                'Midterm': [m_score for m_score, _ in data],
                'Final'  : [f_score for _, f_score in data],
                'Average': average }
            for name, column in data_columns.items():
                mean, var, median, min_, max_ = analyze_data(column)
                report.write(f'* {name}\n')
                report.write(f'  * Mean: **{mean:.3f}**\n')
                report.write(f'  * Variance: {var:.3f}\n')
                report.write(f'  * Median: **{median:.3f}**\n')
                report.write(f'  * Min/Max: ({min_:.3f}, {max_:.3f})\n')