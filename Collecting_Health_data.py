import glob
txtfiles = []
for file in glob.glob("venv/TempFolder/*.txt"):
    txtfiles.append(file)

print(txtfiles)
txtdata =[]
for textFile in txtfiles:
    try:
        file = open(textFile, "r")

        # Repeat for each song in the text file
        for line in file:
            # Let's split the line into an array called "fields" using the ";" as a separator:
            fields = line.split("|")

            # and let's extract the data:

            textNeed = fields[2]
            txtdata.append(textNeed)
    except:
        print("An exception occurred")

    # It is good practice to close the file at the end to free up resources
    file.close()
    print(textFile, "done")
print("process done ")
print(len(txtdata))
print("creating health data file ")
f = open("venv/Data/HealthData.txt", "w+")
for i in range(len(txtdata)):
    f.write("%s\n" % txtdata[i])
    # f.write("/n")
f.close()
