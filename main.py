import tkinter as tk
import json
from functools import partial
from os import listdir
from PIL import ImageTk, Image 
from graph_generator import make_graph

# ******************** OPTIONS ********************

#Visual
windowsTitle = "Elegant labeling"
inputFrameWidth = 225
inputFrameHeight = 480
outputFrameWidth = 640
outputFrameHeight = 480

#Logic
minNumberOfVertices = 2
maxNumberOfVertices = 9
defaultNumberOfVertices = 5

#Folders
graphsJSONsFolderName = "graphs"
graphsResultsFolderName = "graphs_results"

# ****************** OPTIONS END ******************

#Define root
root = tk.Tk()

#Define tkinter variables
numberOfVertices = tk.IntVar()
edgesSelectorMatrix = []

#Define frames
inputFrame = tk.Frame(root, width=inputFrameWidth, height=inputFrameHeight, padx=5, pady=5, borderwidth=2, relief=tk.RIDGE)
inputFrame.grid_propagate(False)
outputFrame = tk.Frame(root, width=outputFrameWidth, height=outputFrameHeight)
verticesInputFrame = tk.Frame(inputFrame, width=inputFrameWidth)
edgesInputTextFrame = tk.Frame(inputFrame, width=inputFrameWidth)
edgesInputSetFrame = tk.Frame(inputFrame, width=inputFrameWidth)

#Define commands

def edgeSelectorCommand(x, y):
    edgesSelectorMatrix[x][y].set(edgesSelectorMatrix[y][x].get())

def generateEdgesSelectorsTableCommand(n):
    generateGraphButton.place(relx=0.5, y=(n*19)+101, anchor=tk.CENTER)

    for v in edgesSelectorsTable:
        for e in v: e.grid_forget()

    edgesSelectorsTable.clear()
    edgesSelectorMatrix.clear()

    for y in range(0, n+1):
        edgesSelectorsTable.append([])
        if y > 0: edgesSelectorMatrix.append([])
        for x in range(0, n+1):
            if y == 0 and x == 0: edgesSelectorsTable[-1].append(tk.Label(edgesInputSetFrame, text=" ", anchor=tk.W, padx=0, pady=0, borderwidth=0))
            elif y == 0: edgesSelectorsTable[-1].append(tk.Label(edgesInputSetFrame, text=str(x), anchor=tk.W, padx=5, pady=0, borderwidth=0))
            elif x == 0: edgesSelectorsTable[-1].append(tk.Label(edgesInputSetFrame, text=str(y), anchor=tk.W, padx=3, pady=0, borderwidth=0))
            else:
                edgesSelectorMatrix[-1].append(tk.BooleanVar())
                if y == x: edgesSelectorsTable[-1].append(tk.Checkbutton(edgesInputSetFrame, variable=edgesSelectorMatrix[-1][-1], state=tk.DISABLED, padx=0, pady=0, borderwidth=0))
                else: edgesSelectorsTable[-1].append(tk.Checkbutton(edgesInputSetFrame, variable=edgesSelectorMatrix[-1][-1], padx=0, pady=0, borderwidth=0, command=partial(edgeSelectorCommand, x-1, y-1)))
            edgesSelectorsTable[-1][-1].grid(row=y, column=x, sticky=tk.W)

def generateGraphCommand():
    #Graph result image global holder
    global graphResultImage

    #Create graph matrix dictionary
    graphDict = {}
    for y in range(0, numberOfVertices.get()):
        vName = "x" + str(y+1)
        graphDict[vName] = []
        for x in range(0, numberOfVertices.get()):
            eName = "x" + str(x+1)
            if edgesSelectorMatrix[y][x].get() == True: graphDict[vName].append(vName + eName)

    #Get number of last saved graph
    graphNumber = 1
    graphsJSONsFileNames = listdir(graphsJSONsFolderName)
    if graphsJSONsFileNames: graphNumber = max([int(name[5:][:-5]) for name in graphsJSONsFileNames]) + 1

    #Set filenames
    beeProgramFileName = "bee_program" + str(graphNumber) + ".bee"
    graphJSONFileName = "graph" + str(graphNumber) + ".json"
    beeResultFileName = "bee_result" + str(graphNumber) + ".txt"
    graphResultFileName = "graph_result" + str(graphNumber) + ".png"

    #Save graph JSON file
    with open(graphsJSONsFolderName + "/" + graphJSONFileName, "w") as JSONFile: json.dump(graphDict, JSONFile)

    #Generate graph result
    make_graph(beeProgramFileName, graphJSONFileName, beeResultFileName, graphResultFileName)

    #Display graph result image
    graphResultImage = ImageTk.PhotoImage(Image.open(graphsResultsFolderName + "/" + graphResultFileName))
    imageCanvas.create_image(0, 0, image=graphResultImage, anchor=tk.NW)

#Define widgets
numberOfVerticesText = tk.Label(verticesInputFrame, text="Number of vertices:")
numberOfVerticesMenu = tk.OptionMenu(verticesInputFrame, numberOfVertices, *range(minNumberOfVertices, maxNumberOfVertices+1), command=generateEdgesSelectorsTableCommand)
edgesInputText = tk.Label(edgesInputTextFrame, text="Select edges")
edgesSelectorsTable = []
generateGraphButton = tk.Button(inputFrame, text="Generate graph", command=generateGraphCommand)
imageCanvas = tk.Canvas(outputFrame, width=outputFrameWidth, height=outputFrameHeight)

#Generate base elements
def generateBaseElements():
    #root
    inputFrame.grid(row=0, column=0, sticky=tk.NW)
    outputFrame.grid(row=0, column=1, sticky=tk.NW)

    #inputFrame
    verticesInputFrame.grid(row=0, column=0, sticky=tk.NW)
    edgesInputTextFrame.grid(row=1, column=0, sticky=tk.NW)
    edgesInputSetFrame.grid(row=2, column=0, sticky=tk.NW)

    #outputFrame
    imageCanvas.grid(row=0, column=0)

    #verticesInputFrame
    numberOfVerticesText.grid(row=0, column=0)
    numberOfVerticesMenu.grid(row=0, column=1)

    #edgesInputTextFrame
    edgesInputText.grid(row=0, column=0, pady=6)

#Set default values
def setDefaultValues():
    numberOfVertices.set(defaultNumberOfVertices)

def main():
    root.title("Elegant labeling")
    root.geometry(str(inputFrameWidth + outputFrameWidth) + "x" + str(max(inputFrameHeight, outputFrameHeight)))
    root.resizable(False, False)
    generateBaseElements()
    setDefaultValues()
    generateEdgesSelectorsTableCommand(defaultNumberOfVertices)

    root.mainloop()

if __name__ == "__main__":
    main()