import matplotlib.pyplot as plt
import pandas as pd

numRows = 1
numCols = 3


def generateGraphs(inputCSV):
    
    df = pd.read_csv(inputCSV)


    plt.subplot(numRows,numCols, 1)
    plt.plot(df["Time_s"], df["Area_Sil"], "o")

    plt.title("Area")
    plt.xlabel("Time Since Experiment Start")
    plt.ylabel("Area")  
    plt.grid()
    
    plt.subplot(numRows,numCols, 2)
    plt.plot(df["Time_s"], df["Length_Sil"], "o")

    plt.title("Length")
    plt.xlabel("Time Since Experiment Start")
    plt.ylabel("Length")   
    plt.grid()

    plt.subplot(numRows,numCols, 3)
    plt.plot(df["Time_s"], df["Length_Sil"], "o")

    plt.title("Length")
    plt.xlabel("Time Since Experiment Start")
    plt.ylabel("Length")   
    plt.grid()

    plt.subplots_adjust(left=0.2, wspace=0.3)
    plt.suptitle("Attributes vs Time for Silhouette Camera")
    plt.show()



def main():
    generateGraphs("/Users/izalewski/Documents/TU-Dortmund ISP Research/test.csv")

if __name__=="__main__":
    main()



