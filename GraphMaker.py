import matplotlib.pyplot as plt
import pandas as pd


def generateGraphs(inputCSV, shape="Rectangle"):

    df = pd.read_csv(inputCSV)

    # 1. Expand figure size (Width: 16 inches, Height: 5 inches)
    fig = plt.figure(figsize=(16, 9))

    numRows, numCols = 2, 3

    # Plot 1: Length
    plt.subplot(numRows, numCols, 1)
    plt.plot(df["Time_s"], df["Length_Sil"], "o", markersize=4, alpha=0.7)
    plt.title("Length vs Time Sil")
    plt.xlabel("Time Since Experiment Start (s)")
    plt.ylabel("Length")
    plt.grid(True)

    # Plot 2: Height
    plt.subplot(numRows, numCols, 2)
    plt.plot(df["Time_s"], df["Height_Sil"], "o", markersize=4, alpha=0.7)
    plt.title("Height vs Time Sil")
    plt.xlabel("Time Since Experiment Start (s)")
    plt.ylabel("Height")
    plt.grid(True)


    #Generates a new data frame with only the rows with values in Phosphor Columns
    dfPhosphor = df.copy()
    dfPhosphor = dfPhosphor[dfPhosphor["Width_Phos"] != -1]
    #dfPhosphor.to_csv("phos" + inputCSV)

    # Plot 3: Width
    plt.subplot(numRows, numCols, 3)
    plt.plot(dfPhosphor["Time_s"], dfPhosphor["Width_Phos"], "o", markersize=4, alpha=0.7)
    plt.title("Width vs TimePhos")
    plt.xlabel("Time Since Experiment Start (s)")
    plt.ylabel("Width")
    plt.grid(True)

    # Plot 4: Height
    plt.subplot(numRows, numCols, 4)
    plt.plot(dfPhosphor["Time_s"], dfPhosphor["Height_Phos"], "o", markersize=4, alpha=0.7)
    plt.title("Height vs Time Phos")
    plt.xlabel("Time Since Experiment Start (s)")
    plt.ylabel("Height")
    plt.grid(True)

    #Plot Volume over Time
    plt.subplot(numRows, numCols, 5)
    plt.plot(dfPhosphor["Time_s"], dfPhosphor["Volume"], "o", markersize=4, alpha=0.7)
    plt.title("Volume vs Time Phos")
    plt.xlabel("Time Since Experiment Start (s)")
    plt.ylabel("Volume")
    plt.grid(True)

    #Plot every dimension on the same graph

    plt.subplot(numRows, numCols, 6)
    plt.plot(dfPhosphor["Time_s"], dfPhosphor["Length_Sil"], "o", markersize=4, alpha=0.7, label="Length")
    plt.plot(dfPhosphor["Time_s"], dfPhosphor["Height_Sil"], "o", markersize=4, alpha=0.7, label="Height")
    plt.plot(dfPhosphor["Time_s"], dfPhosphor["Width_Phos"], "o", markersize=4, alpha=0.7, label="Width")
    plt.title("Dimensions vs Time")
    plt.xlabel("Time Since Experiment Start (s)")
    plt.grid(True)

    plt.legend(loc="lower left")


    # 2. Main Title & Automatic Padding Adjustment
    plt.suptitle("Attributes vs Time", fontsize=14, y=1.02)
    plt.tight_layout()

    # 3. Save with high resolution and clear bounds
    plt.savefig(inputCSV[:-4] + ".png", dpi=300, bbox_inches="tight")
    plt.show()


    


def main():
    generateGraphs("/Users/izalewski/Documents/TU-Dortmund ISP Research/fullRun.csv")

if __name__=="__main__":
    main()



