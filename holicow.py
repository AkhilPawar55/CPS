"""
holicow.py - Lab 9
Author: FNU Swati
       Akhil Pawar

"""

import sys
import os.path
from Graph import Graph
from searchAlgos import  findPathDFS

class holicow:
    """
    The complete play field is represented in this class, as a graph
    of paintballs connected to cows and other paintballs in radius.
    :slot: graph (Graph): The graph of field
    :slot: mergeDict (dict): A dictionary of all the paintballs and cows read from file
    :slot: paintballDict (dict): A dictionary of paintballs
    :slot: cowsDict (dict): A dictionary of all cows
    """

    __slots__ = 'graph','mergeDict','paintballDict','cowsDict'

    def __init__(self,filename):
        """
        Construct the field graph
        :param filename (str): The input file
        :return: None
        """

        self.graph = Graph()
        self.mergeDict = {}
        self.paintballDict = {}
        self.cowsDict = {}


        self.readFile(filename)

        # print(mergeDict)
        # Get the x and y coordinates of all the balls
        for colors in self.paintballDict:
            # print(colors)
            coordinates = (self.paintballDict[colors])
            XCoordinateOfBall = coordinates[0]
            YCoordinateOfBall = coordinates[1]
            radiusOfParentBall = coordinates[2]

            # print(item)
            #Check all the items in mergeDicts(paintablls,cows) who are in radius of the current ball
            #and add an edge between the two
            for items in self.mergeDict:

                if items != colors:

                    coordinates = (self.mergeDict[items])
                    # print(items)
                    XCoordinate = coordinates[0]
                    YCoordinate = coordinates[1]
                    inRadius = self.checkIfInRadius(XCoordinateOfBall, YCoordinateOfBall, radiusOfParentBall, XCoordinate,YCoordinate)
                    if inRadius:
                        self.graph.addEdge(colors, items)

                    if items not in self.graph:
                        self.graph.addVertex(items)

            if colors not in self.graph:
                self.graph.addVertex(colors)

        #Print Graph
        for connections in self.graph:
            print(connections)



    def readFile(self,filename):

        """
        This method reads the file and add it into dictionary(name : coordinates)
        :param filename (str): The input file
        :return: None
        """

        # paintballLocation = {}
        mergeDict = {}
        with open(filename) as f:
            for line in f:
                if len(line) > 0 and line[0] != '#':
                    values = line.split()
                    paintOrCow = values[0]
                    if values[0] == "cow":
                        nameOfCow = values[1]
                        xCordinate = values[2]
                        yCoordinate = values[3]
                        self.cowsDict[nameOfCow] = [xCordinate,yCoordinate]
                        self.mergeDict[nameOfCow] = [xCordinate,yCoordinate]

                    elif values[0] == "paintball":
                        paintBallName = values[1]
                        xCordinateOfball = values[2]
                        yCoordinateOfBall = values[3]
                        radiusOfSplash = values[4]
                        self.paintballDict[paintBallName] = [xCordinateOfball,yCoordinateOfBall,radiusOfSplash]
                        self.mergeDict[paintBallName] = [xCordinateOfball,yCoordinateOfBall,radiusOfSplash]


        # print(paintballLocation)
        # print(cowLocation)


    def mainLoop(self):

        """
        This method simulates the field
        :param None
        :return: colorToNumberOfCows : A dictionary that map color to the nummber of cows painted with it.
        :return: cowMapping : A dictionary that maps, all the items with the current paintball triggered.
        """


        #cowToColorDict : A dictionary that maps cows, with all the colors on it after simulation.
        cowToColorDict = {}
        #cowMapping : A dictionary that maps, all the items with the current paintball triggered.
        cowMapping = {}
        # colorToNumberOfCows : A dictionary that map color to the nummber of cows painted with it.
        colorToNumberOfCows = {}

        for colors in self.graph:

            if colors.id in self.paintballDict.keys():
                print("Triggering ", colors.id, " paint ball.")
                cowToColorDict= findPathDFS(colors,self.paintballDict)
                #If no item in dictionary , means no cow is pained
                if len(cowToColorDict)<1:
                    print("    No cows were painted")
                #Mapping cowToColorDict with current color
                cowMapping[colors.id] = cowToColorDict
                count = 0
                #calculating the number of cows painted on triggering of current paintball
                for  keys in cowToColorDict:

                    count += (len(cowToColorDict[keys]))

                colorToNumberOfCows[colors.id] = count


            # print(cowToColorDict)
            # print(colorToNumberOfCows)
            #     # print(len(cowToColorDict.values()))
            # print(cowMapping)



        return (colorToNumberOfCows,cowMapping)




    def calculateREsult(self,colorToNumberOfCows,cowMapping):

        """
        This method calculates and prints the final result
        :param colorToNumberOfCows :  A dictionary that map color to the nummber of cows painted with it.
        :param cowMapping : A dictionary that maps, all the items with the current paintball triggered.
        :return: None
        """
        #Find the key which has maximum value attached to it.
        maximumColorValue = max(colorToNumberOfCows, key=colorToNumberOfCows.get)
        if colorToNumberOfCows[maximumColorValue] == 0:
            print("No cows were Painted by any starting paintball !")
        else:
            print("Triggering the",maximumColorValue,"paint ball is the best choice with", colorToNumberOfCows[maximumColorValue] , "total paint on the cows:")
            localDict = cowMapping[maximumColorValue]
            for keys in self.cowsDict:

                if keys in localDict:
                    print(keys,"'s colors: ",localDict[keys])
                else:
                    print(keys,"'s colors: []")




    def checkIfInRadius(self,XCoordinateOfBall,YCoordinateOfBall,radiusOfParentBall,XCoordinatetoCheck,YCoordinatetoCheck ):


        """
        Given the X and y coordinates, this radius check if an item(Ball or cow) is in the radius or not)
        :param XCoordinateOfBall: X coordinate of ball
        :param YCoordinateOfBall: Y coordinate of ball
        :param radiusOfParentBall: radius Of Ball
        :param XCoordinatetoCheck: X Coordinate of item to check
        :param YCoordinatetoCheck: Y Coordinate of item to check
        :return: True: If in radius, False Otherwise
        """


        yDifferenceSquare = (int(YCoordinateOfBall)-int(YCoordinatetoCheck))**2
        xDifferenceSquare = (int(XCoordinateOfBall)-int(XCoordinatetoCheck))**2
        radiusSquare = (int(radiusOfParentBall))**2
        if radiusSquare >= yDifferenceSquare + xDifferenceSquare:
            inradius = True
        else:
            inradius = False
        return inradius




def main():
    """
    The main function, takes the filename as command line argument.
    :return: None
    """
    if len(sys.argv) < 2:
        print("Usage : python3 holicow.py")
        sys.exit()

    if os.path.exists(sys.argv[1]):

        filename = sys.argv[1]
        # print(filename)
    else:
        print("File not found")
        sys.exit()
    print("Field Of Dreams")
    print("-----------------------")
    Holicow = holicow(filename)


    print("\nBeginning simulation ... ")
    bestChoicedict,cowMapping = Holicow.mainLoop()


    print("\nResults:")
    Holicow.calculateREsult(bestChoicedict,cowMapping)





if __name__ == '__main__':

    main()