import random
import time
# N = 100
# A = [str(x + 1) +"\n" for x in range(N)]
# random.seed(time.time())
# random.shuffle(A)
def readFile(fileName):
    with open(f"files/{fileName}", "r") as f:
        lst = [int(x) for x in f.readlines()]
    return lst


def fillFile(n, filename):
    if (filename == None):
        filename = input("Please enter a filename: ")
    filename = f"files/{filename}"
    lst = [str(random.randint(1,n)) + '\n' for x in range(n)]
    with open(filename, "w") as f:
        f.writelines(lst)
    return lst

# fillFile(50, "50.txt")

def generateNewFile(filename):
    size = int(filename[:-4])
    generatedData = fillFile(size,filename)
    print(generatedData)
