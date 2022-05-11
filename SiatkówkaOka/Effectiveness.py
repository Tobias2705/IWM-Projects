from matplotlib import pyplot as plt


def makeTable(TP, TN, FP, FN):
    _, ax = plt.subplots()
    ax.set_axis_off()
    ax.table(
        cellText=[[TP, FP], [FN, TN]],
        rowLabels=["Predicted positives", "Predicted negatives"],
        colLabels=["Actual positives", "Actual negatives"],
        rowColours=["lightgrey"] * 10,
        colColours=["lightgrey"] * 10,
        cellLoc='center',
        loc='upper left')

    ax.set_title('Confusion matrix', fontweight="bold")

    plt.show()


def checkEffectiveness(img, ho, isPrint=True, isTable=True):
    TP = 0
    FP = 0
    FN = 0
    TN = 0

    for i in range(len(img)):
        for j in range(len(img[0])):
            if img[i, j] == 1 and ho[i, j] == 1:
                TP += 1
            elif img[i, j] == 0 and ho[i, j] == 0:
                TN += 1
            elif img[i, j] == 0 and ho[i, j] == 1:
                FP += 1
            elif img[i, j] == 1 and ho[i, j] == 0:
                FN += 1

    sen = round(TP / (TP + FN), 4)
    spe = round(TN / (TN + FP), 4)
    acc = round((TP + TN) / (TP + FP + TN + FN), 4)
    avg = round((sen + spe) / 2, 4)

    if isPrint:
        print('Effectiveness for one image')
        print('Sensitivity: {}%'.format(round(sen * 100, 2)))
        print('Specificity: {}%'.format(round(spe * 100, 2)))
        print('Accuracy: {}%'.format(round(acc * 100, 2)))
        print('Specificity&Sensitivity Average: {}%'.format(round(avg * 100, 2)))
        if isTable:
            makeTable(TP, TN, FP, FN)
    print("<<")
    return [TP, TN, FP, FN, sen, spe, acc, avg]


def checkEffectiveness2(TP, FP, FN, TN, isPrint=True, isTable=True):
    sen = round(TP / (TP + FN), 4)
    spe = round(TN / (TN + FP), 4)
    acc = round((TP + TN) / (TP + FP + TN + FN), 4)
    avg = round((sen + spe) / 2, 4)

    if isPrint:
        print('Effectiveness for one image')
        print('Sensitivity: {}%'.format(round(sen * 100, 2)))
        print('Specificity: {}%'.format(round(spe * 100, 2)))
        print('Accuracy: {}%'.format(round(acc * 100, 2)))
        print('Specificity&Sensitivity Average: {}%'.format(round(avg * 100, 2)))
        if isTable:
            makeTable(TP, TN, FP, FN)
    print("<<")
    return [TP, TN, FP, FN, sen, spe, acc, avg]
