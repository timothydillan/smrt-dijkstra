"""This script stores the train logic class that contains all the program-related functions."""
# All things taken from the internet are put in REFERENCE_LIST.txt
# Initialize libraries needed for the program.
import tkinter as tk
from tkinter import ttk, messagebox
from variables import mrt_train_graph
from logic import TrainLogic

Trains = TrainLogic()


class MainController(tk.Tk):
    """
    This class is the main controller for the tkinter frames
    (Start Page, Traverse, Shortest Route) in the program.
    Acts as a superclass too, containing several variables that'll be used
    in each subclass (frames).
    """
    def __init__(self, *args, **kwargs):
        # Initialize a class that inherits the Tk module.
        tk.Tk.__init__(self, *args, **kwargs)
        # Create a frame container that'll be used to show
        # Multiple frames (pages) that is going to be used for the program.
        frame_containers = tk.Frame(self)
        frame_containers.pack(side="top", fill="both", expand=True)
        frame_containers.grid_rowconfigure(0, weight=1)
        frame_containers.grid_columnconfigure(0, weight=1)

        self.graph = mrt_train_graph
        self.station_names = tk.StringVar(value=[*self.graph.keys()])

        self.button_style = ttk.Style(self)
        self.button_style.theme_use('clam')
        self.button_style.configure('flat.TButton', borderwidth=0, background='#038579', foreground="#ffffff")
        self.frames = {}

        for pages in (StartPage, FindRouteLinkDelink, TraverseNeighbours):
            frames = pages(frame_containers, self)
            self.frames[pages] = frames
            frames.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, page):
        self.frames[page].tkraise()


class StartPage(tk.Frame):
    """
    This class is the main page of the program. Gives an option to the user
    to do several main operations (Traverse, Link, De-link, Find Route).
    """
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, background='#009688')
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        program_title = tk.Label(self, text="SMRT Smart Mapper", font="JetBrainsMono-Medium 30", background='#009688',
                                 foreground="#fff")
        program_title.pack(pady=35, padx=10)
        find_route_and_link_delink_btn = ttk.Button(self, text="Find Train Routes or Link/De-link Stations",
                                                    command=lambda: controller.show_frame(FindRouteLinkDelink),
                                                    style='flat.TButton')
        find_route_and_link_delink_btn.pack()
        traverse_neighbour_btn = ttk.Button(self, text="Traverse SSM Map and See Station Neighbours",
                                            command=lambda: controller.show_frame(TraverseNeighbours),
                                            style='flat.TButton')
        traverse_neighbour_btn.pack(pady=10)


class FindRouteLinkDelink(tk.Frame):
    """
    This class combines both the functionality of searching the shortest route and
    also lets the user link and or de-link stations at the same time.
    """
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        depart_stations = tk.Listbox(self, exportselection=0, listvariable=controller.station_names,
                                     font="Roboto-Light")
        arrive_stations = tk.Listbox(self, exportselection=0, listvariable=controller.station_names,
                                     font="Roboto-Light")
        results_list = tk.Listbox(self, font="Roboto-Light")

        def find_shortest_route():
            # Clear the output listbox when the method is called
            # so that the previous output does not overlap with the current one.
            results_list.delete('0', 'end')
            try:
                station_input = depart_stations.get(depart_stations.curselection())
                station_target = arrive_stations.get(arrive_stations.curselection())
                results_list.insert('end', f"Route to {station_target}:")
                shortest_route = Trains.dijkstra_algorithm(station_input, station_target)
                for routes in shortest_route[0]:
                    results_list.insert('end', routes)
                results_list.insert('end', shortest_route[1])
            except tk.TclError:
                # If the user did not pick any station, it'll raise a TclError exception.
                # So, we can handle it by using the try and except clause and show a warning
                # that the user has not picked any station yet.
                messagebox.showinfo("Warning", "You haven't picked a station yet!")

        def link_stations():
            try:
                station_input = depart_stations.get(depart_stations.curselection())
                station_target = arrive_stations.get(arrive_stations.curselection())
                messagebox.showinfo("Station Linking Information ", Trains.link_stations(station_input,
                                                                                         station_target))
            except tk.TclError:
                messagebox.showinfo("Warning", "You haven't picked a station yet!")

        def delink_stations():
            try:
                station_input = depart_stations.get(depart_stations.curselection())
                station_target = arrive_stations.get(arrive_stations.curselection())
                messagebox.showinfo("Station De-linking Information", Trains.delink_stations(station_input,
                                                                                             station_target))
            except tk.TclError:
                messagebox.showinfo("Warning", "You haven't picked a station yet!")

        # Buttons
        main_menu_btn = ttk.Button(self, text="Main Menu", command=lambda: controller.show_frame(StartPage),
                                   style='flat.TButton')
        shortest_route_btn = ttk.Button(self, text="Find Shortest Route", command=find_shortest_route,
                                        style='flat.TButton')
        link_btn = ttk.Button(self, text="Link Stations", command=link_stations, style='flat.TButton')
        delink_btn = ttk.Button(self, text="De-link Stations", command=delink_stations, style='flat.TButton')

        # Headers
        station_label = tk.Label(self, text="Departure Station", bg="#5e8ac3", font='Roboto-Medium', foreground='white')
        target_station_label = tk.Label(self, text="Arrival Station", bg="#2b3036", font='Roboto-Medium',
                                        foreground='white')
        results_label = tk.Label(self, text="Results", bg="#ab3750", font='Roboto-Medium', foreground='white')

        # ----------------------------
        # RENDERING LABELS AND BUTTONS
        # ----------------------------
        station_label.grid(row=0, column=0, sticky=tk.N + tk.S + tk.W + tk.E)
        depart_stations.grid(row=1, column=0, sticky=tk.N + tk.S + tk.W + tk.E)
        target_station_label.grid(row=0, column=1, sticky=tk.N + tk.S + tk.W + tk.E)
        arrive_stations.grid(row=1, column=1, sticky=tk.N + tk.S + tk.W + tk.E)
        results_label.grid(row=0, column=2, sticky=tk.N + tk.S + tk.W + tk.E)
        results_list.grid(row=1, sticky=tk.N + tk.S + tk.W + tk.E, column=2)

        shortest_route_btn.grid(row=2, column=0, columnspan=3, sticky=tk.N + tk.S + tk.W + tk.E)
        link_btn.grid(row=3, column=0, sticky=tk.N + tk.S + tk.W + tk.E)
        main_menu_btn.grid(row=3, column=1, sticky=tk.N + tk.S + tk.W + tk.E)
        delink_btn.grid(row=3, column=2, sticky=tk.N + tk.S + tk.W + tk.E)


class TraverseNeighbours(tk.Frame):
    """
    This class lets the user to be able to traverse the SMRT Map from a given station,
    and also lets the user to check out the neighboring stations of a station.
    """

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        stations = tk.Listbox(self, exportselection=0, listvariable=controller.station_names, font="Roboto-Light")
        results_list = tk.Listbox(self, font="Roboto-Light")

        def traverse_mrt():
            results_list.delete('0', 'end')
            try:
                station_input = stations.get(stations.curselection())
                for all_stations in Trains.dfs_algorithm(station_input):
                    results_list.insert('end', all_stations)
            except tk.TclError:
                messagebox.showinfo("Warning", "You haven't picked a station yet!")

        def show_neighbours():
            results_list.delete('0', 'end')
            try:
                station_input = stations.get(stations.curselection())
                results_list.insert('end', f"Neighbours of {station_input}:")
                for all_stations in controller.graph[station_input]:
                    results_list.insert('end', all_stations)
            except tk.TclError:
                messagebox.showinfo("Warning", "You haven't picked a station yet!")

        # Buttons
        main_menu_btn = ttk.Button(self, text="Main Menu", command=lambda: controller.show_frame(StartPage),
                                   style='flat.TButton')
        traverse_btn = ttk.Button(self, text="Traverse SMRT Map", command=traverse_mrt, style='flat.TButton')
        neighbour_btn = ttk.Button(self, text="Show Neighbour", command=show_neighbours, style='flat.TButton')

        # Headers
        station_label = tk.Label(self, text="MRT Stations", bg="#5e8ac3", font='Roboto-Medium', foreground='white')
        results_label = tk.Label(self, text="Results", bg="#ab3750", font='Roboto-Medium', foreground='white')

        # ----------------------------
        # RENDERING LABELS AND BUTTONS
        # ----------------------------
        station_label.grid(row=0, column=0, sticky=tk.N + tk.S + tk.W + tk.E)
        stations.grid(row=1, column=0, sticky=tk.W + tk.E)
        results_label.grid(row=0, column=1, sticky=tk.N + tk.S + tk.W + tk.E)
        results_list.grid(row=1, sticky=tk.N + tk.S + tk.W + tk.E, column=1)

        traverse_btn.grid(row=2, column=0, sticky=tk.N + tk.S + tk.W + tk.E)
        neighbour_btn.grid(row=2, column=1, sticky=tk.N + tk.S + tk.W + tk.E)
        main_menu_btn.grid(row=3, column=0, columnspan=2, sticky=tk.N + tk.S + tk.W + tk.E)


def main():
    smrt_program = MainController()
    smrt_program.title("SMRT Smart Mapper")
    smrt_program.mainloop()


if __name__ == "__main__":
    main()
