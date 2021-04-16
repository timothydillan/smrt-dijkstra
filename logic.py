"""This script stores the train logic class that contains all the program-related functions."""
# All things taken from the internet are put in REFERENCE_LIST.txt
import copy
from variables import mrt_train_graph


class TrainLogic:
    """
    The TrainLogic class contains functions that are needed
    for the program.

    Attributes:
        graph (dict): This dictionary is basically an "adjacency list" (well, it's a adjacency dictionary)
        that represents a weighted graph of the SMRT Map. Every interchange has a weight of 2, and every normal
        station has a weight of 1.
    """

    def __init__(self):
        self.graph = mrt_train_graph

    def dfs_algorithm(self, start_station):
        """
        This method shows a traversal path of a starting station.

        Args:
            start_station (str): The station that the program will show the traversal path of.

        Returns:
            path (list): The traversal path of the starting station.
        """
        stations = []
        visited_stations = []
        path = []
        # Start by inserting the starting station into the stack.
        stations.append(start_station)
        while stations:
            # While the stations stack is not empty,
            # Pop the last station that is in the stack (LIFO)
            next_station = stations.pop()
            if next_station not in visited_stations:
                # If the popped station is not in the visited station list,
                # we append the station to the visited station list.
                path.append(f"--> {next_station}")
                visited_stations.append(next_station)
                # and then we visit the adjacent station and push that station
                # into the stack.
                for neighbours in self.graph[next_station]:
                    stations.append(neighbours)
        # After there are no more stations that can be visited
        # from the starting station, we return the visited station list.
        path[0] = f"Start: {start_station}"
        return path

    def dijkstra_algorithm(self, start_station, target_station):
        """
        This method finds the shortest path of a starting station to a target station.
        NOTICE: This code is taken from Youtube, with some modifications made to fit into this program.

        Args:
            start_station (str): The station that the user wants to go from.
            target_station (str): The station that the user wants to go to.

        Returns:
            2D List of Shortest Path and Weight (list): Returns the shortest path list (path) and the weight
            to get there (shortest_distance[target_station]).
        """
        # Store the minimum weight to reach a target station.
        shortest_distance = {}
        # Keep track of the path that leads us to a certain node/station.
        predecessor = {}
        # Initialize a stack that's basically the graph so that we're able to use it for processing purposes.
        # As assignment statements in Python do not copy objects,
        # for mutable collections, a copy is needed so that the original collection is not modified.
        # In this case, we're using a shallow copy i.e. creating a new object with the same exact content.
        unseen_stations = copy.copy(self.graph)
        infinity = float('inf')
        # Similar to the predecessor, this list is used to
        # trace back the path that leads to the target goal station.
        path = []
        # For every station in the weighted train graph,
        for stations in unseen_stations:
            # Append all the stations into the shortest_distance dictionary with the value of infinity.
            shortest_distance[stations] = infinity
            # print(shortest_distance[stations])
        # Make sure that the weight from the starting station is 0.
        shortest_distance[start_station] = 0

        while unseen_stations:
            # Declare a minimum node
            minimum_node = None
            # For every stations that is not yet visited,
            for current_node in unseen_stations:
                if minimum_node is None:
                    # If the minimum node is empty, assign it to the starting node.
                    minimum_node = current_node
                # Check if the current tentative weight of the node is less than the
                # tentative weight of the minimum node.
                elif shortest_distance[current_node] < shortest_distance[minimum_node]:
                    # If it is, then assign the current node to the minimum node.
                    # This helps on determining the lowest/shortest path to the goal.
                    minimum_node = current_node
            # For every neighbouring station and their weight from the minimum station,
            for child_nodes, weight in self.graph[minimum_node].items():
                # Calculate the distance of each neighbouring station from the starting station.
                # If the sum is lower than the tentative weight of the neighbouring child nodes,
                if weight + shortest_distance[minimum_node] < shortest_distance[child_nodes]:
                    # Update the weight between each neighbouring stations, and
                    shortest_distance[child_nodes] = weight + shortest_distance[minimum_node]
                    # Update the predecessor/the path it took to the neighbouring stations.
                    predecessor[child_nodes] = minimum_node
            # Pop the minimum node because we don't need to iterate over the same stations again
            # and so that the loop will eventually end.
            unseen_stations.pop(minimum_node)

        # Declare a past station that'll be used to make a path.
        past_stations = target_station
        while past_stations != start_station:
            try:
                # Insert the past station to the path list, and it should be at
                # index 0 so that the shortest path is showed in the correct order.
                # EXAMPLE: START: Toa Payoh -> TARGET: Bishan
                # Bishan has the predecessor station Braddel. After inserting this,
                # The loop breaks and then the program inserts the starting station to the path.
                path.insert(0, f"--> {past_stations}")
                # Assign the predecessor of the current past station to the past station i.e. recursive assignment.
                past_stations = predecessor[past_stations]
            except KeyError:
                # Return an empty list (need to do this as we're supposed to return a list).
                # This is mainly used for the de-linking part, to "dynamically" figure out
                # whether a train station can be de-linked.
                return
        # If the loop finishes, insert the starting station to the first index to complete the path.
        path.insert(0, f"Start: {start_station}")
        # After the operation is done, return a 2D list,
        # containing the shortest path route and the weight of the route.
        return [path, f"Weight of Path: {shortest_distance[target_station]}"]

    def link_stations(self, station_input, station_target):
        """
        This method lets a user to link a station with another station.

        Args:
            station_input (str): The station that the user wants to link with another station.
            station_target (str): The station that the user wants to link with the input station.

        Returns:
            A message whether the linking operation was successfully executed or failed.
        """
        if station_input != station_target:
            if station_target not in self.graph[station_input]:
                start_interchange_station = [weight for weight in self.graph[station_input].values()].count(2) >= 3
                target_interchange_station = [weight for weight in self.graph[station_target].values()].count(2) >= 3
                # Check if the station input or the target station is an interchange. As almost all interchange
                # stations have three or more stations connected, we can easily detect if a station is an
                # interchange station. Punggol is an exception, it only has two stations neighbouring the
                # station, so we need to hard-code that into the if condition checking.
                if (start_interchange_station or target_interchange_station) or (station_input == "Punggol" or station_target == "Punggol"):
                    # We then find the key, aka. station input inside the mrt graph, and then we add a connection
                    # between the station input and the target, and set the weight to two (since it's an interchange).
                    self.graph[station_input][station_target] = 2
                    self.graph[station_target][station_input] = 2
                    return f"{station_input.title()} has been linked to {station_target.title()}!"
                # If the station input nor the station target is an interchange,
                # we link the stations with a weight of one.
                self.graph[station_input][station_target] = 1
                self.graph[station_target][station_input] = 1
                return f"{station_input.title()} has been linked to {station_target.title()}!"
            return f"Sorry, {station_target} is already linked to {station_input}!"
        return "Sorry, you can't link the same station!"

    def delink_stations(self, station_input, station_target):
        """
        This method lets a user to delink a station with another station,
        with the condition that the other station is linked with the input station.

        Args:
            station_input (str): The station that the user wants to delink with another station.
            station_target (str): The station that the user wants to delink with the input station.

        Returns:
            A message whether the linking operation was successfully executed or failed.
        """
        if station_input != station_target:
            if station_target in self.graph[station_input]:
                # When de-linking we need to make sure that we de-link the connection from both
                # the station input and the target.
                del self.graph[station_input][station_target]
                del self.graph[station_target][station_input]
                # After de-linking the station, we check if using the dijkstra's algorithm
                # we still can reach the station. This is a "ghetto" method, but it
                # ensures that no station is left standalone or unreachable.
                if not self.dijkstra_algorithm("Toa Payoh", station_target):
                    # So if we can't reach the station after de-linking it (starting station doesn't matter),
                    # we re-link the station again and show a message that the station can't be de-linked.
                    self.link_stations(station_input, station_target)
                    return f"{station_input.title()} can't be de-linked with {station_target.title()}!"
                return f"{station_input.title()} has been de-linked with {station_target.title()}!"
            return "Sorry, you can't de-link a station that isn't linked!"
        return "Sorry, you can't de-link the same station!"
