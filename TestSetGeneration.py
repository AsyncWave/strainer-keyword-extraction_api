import pandas as pd
import Methods as m

textPool = []

dataSet = pd.read_csv('venv/Data/News_Category_Description.csv', names=['ID', 'text'], header=1)
print("file read ")
for text in dataSet["text"]:

    print(text)
    approval = input("ok: ")
    if approval == "y":
        processedText = m.test_data_cleaning(text)
        textPool.append(processedText)
        print(len(textPool))
        if len(textPool) == 100:
            break

## cleaning test

# for text in dataSet["text"]:
#     processedText = m.test_data_cleaning(text)
#     textPool.append(processedText)
#
# print(len(textPool))
dataFrame = pd.DataFrame(textPool, columns=['text'])
dataFrame.to_csv('TestSet3.csv')











