"""
CSCI-603: Graphs
Author: Sean Strout @ RIT CS
Modified By : FNU Swati
            : Akhil Pawar

This is the implementation of the traversal algorithms used:
    1. findPathDFS: Traverse from start to end and adds the items in dictionary
"""



def __findPathDFS(current,paintballDict,visited,numberOfCowsPaintedOnColorDIct):
    """
    Private recursive helper function that traverse on graph
    :param current (Vertex): The current vertex in the traversal
    :param paintballDict: The dictionary of all the paintballs
    :param visited (set of Vertex): the vertices already visited
    :param paintballDict: The dictionary of all the paintballs
    :param numberOfCowsPaintedOnColorDIct: The dictionary which maps the cows to all the colors on them.
    :return: numberOfCowsPaintedOnColorDIct :The dictionary which maps the cows to all the colors on them.
    """

    # A successful base case is when we traverse to the end vertex.

    for neighbor in current.getConnections():
        if neighbor not in visited:

            if neighbor.id  not in paintballDict.keys():
                print("   ",neighbor.id," is painted ",current.id )
                if neighbor.id in numberOfCowsPaintedOnColorDIct :
                    (numberOfCowsPaintedOnColorDIct[neighbor.id]).append(current.id)
                else:
                    numberOfCowsPaintedOnColorDIct[neighbor.id] = [current.id]

            else:
                visited.add(neighbor)
                print("   ",neighbor.id ," is triggered by ", current.id , "paint ball.")

                __findPathDFS(neighbor, paintballDict,visited,numberOfCowsPaintedOnColorDIct)


    return (numberOfCowsPaintedOnColorDIct)


def findPathDFS(start,paintballDict):
    """
    Traverse from start vertext of the graph till every vertex
    :param paintballDict : paint ball dictionary which has all the colors in it(that is: start vertex)
    :param end (Vertex): the destination vertex
    :return: numberOfCowsPaintedOnColorDIct :The dictionary which maps the cows to all the colors on them.
    """
    visited = set()
    visited.add(start)
    numberOfCowsPaintedOnColorDIct = {}

    # print(start.id , " ball is triggered")
    return __findPathDFS(start,paintballDict,visited,numberOfCowsPaintedOnColorDIct)

