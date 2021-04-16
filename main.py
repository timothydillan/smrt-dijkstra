"""This python script is the executable part of the SMRT program in which users can interact with"""
from logic import TrainLogic
Trains = TrainLogic()


def main():
    """This function shows the user the program's start menu."""
    while True:
        print("-----------------------------------------------------------")
        print("         Welcome to the SMRT Smart Mapper Program!         ")
        print("-----------------------------------------------------------")
        print("Menu:")
        print("S - Find Shortest Route")
        print("L - Link Stations")
        print("D - De-link Stations")
        print("T - Traverse SSM Map")
        print("M - See MRT Stations")
        print("E - Exit Program")
        user_choice = input("Choose: ").lower().strip()
        if user_choice == "s":
            shortest_path_to_station()
        elif user_choice == "m":
            print(*Trains.graph.keys(), sep='\n')
        elif user_choice == "l":
            link_stations()
        elif user_choice == "d":
            delink_stations()
        elif user_choice == "t":
            traverse_mrt()
        elif user_choice == "e":
            print("Bye! See you!")
            break
        else:
            print("Sorry, that choice is invalid.")

    exit(0)


def delink_stations():
    """
    This function lets the user de-link one station with another station,
    with the condition if the station that is going to be de-linked is already
    linked with the target station.
    """
    while True:
        station_input = input("\nWhat station would you like to de-link: ").title().strip()
        if station_input in Trains.graph:
            print("Linked Stations: ")
            print(*Trains.graph[station_input], sep=', ')
            station_target = input(f"What station would you like to de-link {station_input} to: ").title().strip()
            if station_target in Trains.graph:
                print(Trains.delink_stations(station_input, station_target))
                break
            else:
                print("Sorry, that choice is invalid.")
        else:
            print("Sorry, that choice is invalid.")


def link_stations():
    """This function lets the user link one station with another station."""
    while True:
        station_input = input("What station would you like to link: ").title().strip()
        if station_input in Trains.graph:
            station_target = input(f"What station would you like to link {station_input} with: ").title().strip()
            if station_target in Trains.graph:
                print(Trains.link_stations(station_input, station_target))
                break
            else:
                print("Sorry, that choice is invalid.")
        else:
            print("Sorry, that choice is invalid.")


def shortest_path_to_station():
    """This function lets the user to find the shortest route to a station from a starting station."""
    while True:
        station_input = input("Choose a station: ").title().strip()
        station_target = input("Where would you like to go: ").title().strip()
        if station_input in Trains.graph and station_target in Trains.graph:
            shortest_path = Trains.dijkstra_algorithm(station_input, station_target)
            print(f"\nRoute to {station_target}:")
            print(*shortest_path[0], sep='\n')
            print(f"{shortest_path[1]}\n")
            break
        else:
            print("Sorry, your choice is not valid.")


def traverse_mrt():
    """
    This function shows the user what stations can a station traverse to.
    Basically visiting every station from a starting station.
    """
    while True:
        station_input = input("Choose a starting station: ").title().strip()
        if station_input in Trains.graph:
            traversal_path = Trains.dfs_algorithm(station_input)
            print(*traversal_path, sep='\n')
            break
        print("Sorry, that choice is invalid.")


if __name__ == "__main__":
    main()
