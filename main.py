import _thread
import threading
import time
from tkinter import messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
NavigationToolbar2Tk)

import matplotlib.pyplot as plt

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from labellines import labelLine, labelLines

import TreeOrderingAlgoritms
import tkinter
import customtkinter
from PIL import Image, ImageTk, ImageOps
from TreeBuilder import TreeNode
import pubsub
from tkinter import ttk
import sys


class GUI():
    """The class contains all the functions and objects that build the GUI"""

    def __init__(self, window, tree_mode):
        self.window = window # this is the root window of the app, everything showed will be based on it
        self.tree_mode = tree_mode # this flag tells us if the mode is Ruskey's of Zaks
        self.main_window_init() # call function to initiate home screen

        # secluding to frames the screen
        self.frame_left = None
        self.middle_frame = None
        self.frame_right = None

        window.mainloop()

    def main_window_init(self):
        self.window.state('zoomed') # full-screen mode

        # building default screen
        self.window.title("rootOrder - Lexicographic Tree Ordering")
        self.main_window_frames()
        self.on_start_middle_frame_init()

    def main_window_frames(self):
        # this separate the screen to frames and initializes every frame separately

        self.frame_left = customtkinter.CTkFrame(master=self.window,
                                                 width=180, corner_radius=0)
        self.frame_left.grid(row=0, column=0, sticky="nswe")

        self.middle_frame = customtkinter.CTkFrame(master=self.window, width=1280)
        self.middle_frame.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)


        self.left_frame_init()

    def left_frame_init(self):

        # configure grid layout (1x11)
        self.frame_left.grid_rowconfigure(0, minsize=30)  # empty row with minsize as spacing
        self.frame_left.grid_rowconfigure(7, weight=1)  # empty row as spacing
        self.frame_left.grid_rowconfigure(8, minsize=60)  # empty row with minsize as spacing
        self.frame_left.grid_rowconfigure(11, minsize=30)  # empty row with minsize as spacing

        # Left menu title
        self.label_left_menu_title = customtkinter.CTkLabel(master=self.frame_left,
                                              text="Tree Ordering",
                                              font=("Roboto Medium", -16))  # font name and size in px
        self.label_left_menu_title.grid(row=1, column=0, pady=10, padx=10)

        # Manu buttons
        self.button_next_tree = customtkinter.CTkButton(master=self.frame_left,
                                                        text="Find The Next Tree In The Order",
                                                        command=self.on_next_tree_click_Ruskey)
        self.button_next_tree.grid(row=2, column=0, pady=10, padx=20)
        if self.tree_mode == "Ruskey":
            self.button_next_tree.configure(command=self.on_next_tree_click_Ruskey)
        if self.tree_mode == "Zaks":
            self.button_next_tree.configure(command=self.on_next_tree_click_zaks)


        self.button_tree_from_index = customtkinter.CTkButton(master=self.frame_left,
                                                              text="Find Tree From Index",
                                                command=self.on_tree_from_index_click_Ruskey)
        self.button_tree_from_index.grid(row=3, column=0, pady=10, padx=20)

        if self.tree_mode == "Ruskey":
            self.button_tree_from_index = customtkinter.CTkButton(master=self.frame_left,
                                                text="Find Tree From Index",
                                                command=self.on_tree_from_index_click_Ruskey)
            self.button_tree_from_index.grid(row=3, column=0, pady=10, padx=20)
        if self.tree_mode == "Zaks":
            self.button_tree_from_index = customtkinter.CTkButton(master=self.frame_left,
                                                text="Find Tree From Index",
                                                command=self.on_tree_from_index_click_Zaks)
            self.button_tree_from_index.grid(row=3, column=0, pady=10, padx=20)

        self.button_order_of_trees_from_rank = customtkinter.CTkButton(master=self.frame_left,
                                                                       text="Find All Trees",
                                                                       command=self.on_order_of_trees_from_rank_click_ruskey)
        self.button_order_of_trees_from_rank.grid(row=5, column=0, pady=10, padx=20)

        if self.tree_mode == "Ruskey":
            self.button_order_of_trees_from_rank = customtkinter.CTkButton(master=self.frame_left,
                                                                           text="Find All Trees",
                                                                           command=self.on_order_of_trees_from_rank_click_ruskey)
            self.button_order_of_trees_from_rank.grid(row=5, column=0, pady=10, padx=20)

        if self.tree_mode == "Zaks":
            self.button_order_of_trees_from_rank = customtkinter.CTkButton(master=self.frame_left,
                                                                           text="Find All Trees",
                                                                           command=self.on_order_of_trees_from_rank_click_zaks)
            self.button_order_of_trees_from_rank.grid(row=5, column=0, pady=10, padx=20)




        self.button_index_from_tree = customtkinter.CTkButton(master=self.frame_left,
                                                              text="Find Index From Tree",
                                                              command=self.index_from_tree_click_ruskey)
        if self.tree_mode == "Ruskey":
            self.button_index_from_tree.configure(command=self.index_from_tree_click_ruskey)
        if self.tree_mode == "Zaks":
            self.button_index_from_tree.configure(command=self.index_from_tree_click_zaks)



        self.button_index_from_tree.grid(row=4, column=0, pady=10, padx=20)

        self.button_compare = customtkinter.CTkButton(master=self.frame_left,
                                                                       text="Compare The Methods",
                                                                       command=self.on_compare_click)
        self.button_compare.grid(row=6, column=0, pady=10, padx=20)



        self.button_more_information = customtkinter.CTkButton(master=self.frame_left,
                                                text="More Information",
                                                command=self.on_more_information_click)
        self.button_more_information.grid(row=7, column=0, pady=10, padx=20)

       #  determines the mode of the tree
        self.label_tree_type_mode = customtkinter.CTkLabel(master=self.frame_left, text="Tree Type Mode:")
        self.label_tree_type_mode.grid(row=17, column=0, pady=10, padx=20, sticky="w")



        self.optionmenu_trees = customtkinter.CTkOptionMenu(master=self.frame_left,
                                                            values=["", "Zaks", "Ruskey"],
                                                            command=self.change_sequence_type_mode)

        if self.tree_mode == "Zaks":
            self.optionmenu_trees = customtkinter.CTkOptionMenu(master=self.frame_left,
                                                                values=["Zaks", "Ruskey"],
                                                                command=self.change_sequence_type_mode)

        if self.tree_mode == "Ruskey":
            self.optionmenu_trees = customtkinter.CTkOptionMenu(master=self.frame_left,
                                                                values=["Ruskey", "Zaks"],
                                                                command=self.change_sequence_type_mode)

        self.optionmenu_trees.grid(row=18, column=0, pady=0, padx=20, sticky="w")


        # Handles the abillity to switch light and dark mode visibility

        self.label_mode = customtkinter.CTkLabel(master=self.frame_left, text="Appearance Mode:")
        self.label_mode.grid(row=19, column=0, pady=10, padx=20, sticky="w")

        self.optionmenu_1 = customtkinter.CTkOptionMenu(master=self.frame_left,
                                                        values=["Light", "Dark"],
                                                        command=self.change_appearance_mode)
        self.optionmenu_1.grid(row=20, column=0, pady=0, padx=20, sticky="w")

        # creating spacing

        self.label_space_below = customtkinter.CTkLabel(master=self.frame_left, text="")
        self.label_space_below.grid(row=21, column=0, pady=10, padx=20, sticky="w")



    def on_start_middle_frame_init(self):
        # initialize the middle frame default view
        
        #arranging the left frame to fit
        self.frame_left.grid_rowconfigure(3, minsize=10)  # empty row with minsize as spacing
        self.frame_left.grid_rowconfigure(4, minsize=10)  # empty row with minsize as spacing

        self.main_title_label = customtkinter.CTkLabel(master=self.middle_frame,
                                                       text="Welcome To rootOrder - A lexicographical "
                                                            "Tree Ordering Program",
                                                       font=("Roboto Medium", -22, "bold"),
                                                       text_color=("#72CF9F", "#11B384"))
        self.main_title_label.grid(row=1, column=1, pady=40, padx=180)

        self.program_explaination_label = customtkinter.CTkLabel(master=self.middle_frame,
                                                                 text="This program is based on algorithms by F. "
                                                                      "Ruskey, T.C. Hu and S. Zaks.\n"
                                                                      " It crates trees according to lexicografical "
                                                                      "order and "
                                                                      "orders given trees in lexicographical order.\n"
                                                                      "We invite you to explore this fascinating "
                                                                      "subject and "
                                                                      "experiment with our work.")  # ,

        self.program_explaination_label.grid(row=2, column=1, pady=10, padx=180)

        self.middle_frame.grid_rowconfigure(3, weight=1)  # empty row as spacing

        self.related_content_frame = customtkinter.CTkFrame(master=self.middle_frame, width=1180, height=550,
                                                            fg_color=("#11B384", "gray28"))

        self.related_content_frame.grid(row=9, column=1, sticky="nswe", padx=20, pady=20)

        zaks_image_path = "images/Zaks.jpg"
        img = Image.open(zaks_image_path)
        img = img.resize((250, 350))
        img = ImageOps.grayscale(img)

        image_zaks = ImageTk.PhotoImage(img)

        zaks_photo_label = customtkinter.CTkLabel(master=self.related_content_frame, image=image_zaks, text="")
        zaks_photo_label.image = image_zaks
        zaks_photo_label.place(relx=0.2, rely=0.05, relwidth=0.6, relheight=0.8)

        ruskey_image_path = "images/Ruskey.jpg"
        img = Image.open(ruskey_image_path)
        img = img.resize((350, 350))
        
        image_ruskey = ImageTk.PhotoImage(img)

        ruskey_photo_label = customtkinter.CTkLabel(master=self.related_content_frame, image=image_ruskey, text="")
        ruskey_photo_label.image = image_ruskey
        ruskey_photo_label.place(relx=0.1, rely=0.05, relwidth=0.2, relheight=0.8)

        hu_image_path = "images/hu.jpg"
        img = Image.open(hu_image_path)
        img = img.resize((250, 350))
        img = ImageOps.grayscale(img)
        
        image_hu = ImageTk.PhotoImage(img)

        hu_photo_label = customtkinter.CTkLabel(master=self.related_content_frame, image=image_hu, text="")
        hu_photo_label.image = image_hu
        hu_photo_label.place(relx=0.7, rely=0.05, relwidth=0.2, relheight=0.8)

        icon_image_path = "images/icon4.png"
        img = Image.open(icon_image_path)
        image_icon = ImageTk.PhotoImage(img)
        self.window.iconphoto(False, image_icon)

        self.middle_frame.grid_rowconfigure(9, minsize=60)  # empty row with minsize as spacing


    def on_next_tree_click_Ruskey(self):
        # This option creates the screen where the user can enter a tree sequence and find the next tree in the order 
        # Algorithm is B
        self.main_window_frames()
        self.clear_mid_frame()
        self.main_title_label = customtkinter.CTkLabel(master=self.middle_frame,
                                                       text="Find The Next Tree In The Order - Ruskey and Hu's Method",
                                                       font=("Roboto Medium", -22, "bold"),
                                                       text_color=("#72CF9F", "#11B384"))
        self.main_title_label.place(relx=0.1, rely=0.0, relwidth=0.8, relheight=0.1)

        self.program_explaination_label = customtkinter.CTkLabel(master=self.middle_frame,
                                                                 text="Please enter tree sequence to find the next tree in the order")
        self.program_explaination_label.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.1)

        self.tree_sequence_input = customtkinter.CTkEntry(master=self.middle_frame,
                                                          placeholder_text="example: 1,3,4,4,2",
                                                          width=340, height=40)
        self.tree_sequence_input.place(relx=0.2, rely=0.3, relwidth=0.6, relheight=0.1)


        self.button_next = customtkinter.CTkButton(master=self.middle_frame, text="Submit",
                                                   command=self.ruskey_next_tree_thread)

        self.button_next.place(relx=0.2, rely=0.7, relwidth=0.6, relheight=0.1)


    def ruskey_next_tree_thread(self):
        def subscriber(arg):
            # get data from publisher
            current_tree = arg['progress']
            text = self.tree_visualizator(current_tree, "Ruskey")
            # GUI setup
            self.tree_label.insert(tkinter.END, "=>\t{}\n{}".format(text, current_tree))

            # show results
            self.window.update()

        sequence = self.tree_sequence_input.get()
        print(sequence)
        if sequence == '':
            sequence = "1,3,4,4,2"



        try:

            sequence = list(sequence.split(","))
            sequence = list(int(i) for i in sequence)

            if not(self.ruskey_isFeasible(sequence, len(sequence))):

                messagebox.showerror("please check the input", "The sequence should represent a feasible tree.")
        except:
            messagebox.showerror("please check the input", "Please make sure the sequence is valid.")

        self.result_popup = customtkinter.CTk()
        self.result_popup.state("zoomed")
        self.result_popup.title("Result")

        self.tree_label = tkinter.Text(self.result_popup)
        self.tree_label.place(relx=0.1, rely=0.05, relwidth=0.8, relheight=0.8)


        # create CTk scrollbar
        self.ctk_textbox_scrollbar = customtkinter.CTkScrollbar(self.result_popup, command=self.tree_label.yview)
        self.ctk_textbox_scrollbar.place(relx=0.09, rely=0.05, relwidth=0.01, relheight=0.8)

        self.ctk_textbox_scrollbar_horizontal = customtkinter.CTkScrollbar(self.result_popup,
                                                                           command=self.tree_label.xview)
        self.ctk_textbox_scrollbar_horizontal.place(relx=0.1, rely=0.85, relwidth=0.8, relheight=0.02)

        try:
            if self.appearance_mode == "Dark":
                self.tree_label.config(background="#474747", foreground="#11B384")
        except:
            self.tree_label.config(background="#11B384")

        text = self.tree_visualizator(sequence, "Ruskey")

        self.tree_label.insert(tkinter.END, "{}".format(text))
        self.tree_label.insert(tkinter.END, "\n{}".format(sequence))

        # run tree building in thread
        self.t1 = threading.Thread(target=self.ruskey_next_tree_visual(sequence, subscriber))
        self.t1.start()

    def zaks_next_tree_thread(self):
        def subscriber(arg):
            # get data from publisher
            current_tree = arg['progress']
            text = self.tree_visualizator(current_tree, "X")
            # GUI setup

            self.tree_label.insert(tkinter.END, "=>\t{}\n{}".format(text, current_tree))

            # show results
            self.window.update()

        sequence = self.tree_sequence_input.get()
        print(sequence)

        type = "Z"
        if sequence == '':
            sequence = "1,2,3,5,7,8,9"


        try:

            sequence = list(sequence.split(","))
            sequence = list(int(i) for i in sequence)

            if type == "Z":
                if not (self.zaks_isFeasible_z(sequence, len(sequence))):
                    messagebox.showerror("please check the input", "The sequence should represent a feasible tree.")
        except:
            messagebox.showerror("please check the input", "Please make sure the sequence is valid.")

        self.result_popup = customtkinter.CTk()
        self.result_popup.state("zoomed")
        self.result_popup.title("Result")

        self.label_text = tkinter.StringVar(value="")
        text = self.tree_visualizator(sequence, type)
        print(type)
        self.label_text.set(text)
        self.tree_label = tkinter.Text(self.result_popup)
        self.tree_label.insert(tkinter.END, "{}".format(text))
        self.tree_label.insert(tkinter.END, "\n{}".format(sequence))

        self.tree_label.place(relx=0.1, rely=0.05, relwidth=0.8, relheight=0.9)

        # create CTk scrollbar
        self.ctk_textbox_scrollbar = customtkinter.CTkScrollbar(self.result_popup, command=self.tree_label.yview)
        self.ctk_textbox_scrollbar.place(relx=0.09, rely=0.05, relwidth=0.01, relheight=0.9)

        self.ctk_textbox_scrollbar_horizontal = customtkinter.CTkScrollbar(self.result_popup,
                                                                           command=self.tree_label.xview)
        self.ctk_textbox_scrollbar_horizontal.place(relx=0.1, rely=0.95, relwidth=0.8, relheight=0.02)

        try:
            if self.appearance_mode == "Dark":
                self.tree_label.config(background="#474747", foreground="#11B384")
        except:

            self.tree_label.config(background="#11B384")
        
        # run tree building in thread
        self.t1 = threading.Thread(target=self.zaks_next_tree_visual(sequence, type, subscriber))
        self.t1.start()




    def on_next_tree_click_zaks(self):
        self.main_window_frames()
        self.clear_mid_frame()
        self.main_title_label = customtkinter.CTkLabel(master=self.middle_frame,
                                                       text="Find The Next Tree In The Order - Zaks' Method",
                                                       font=("Roboto Medium", -22, "bold"),
                                                       text_color=("#72CF9F", "#11B384"))
        self.main_title_label.place(relx=0.1, rely=0.0, relwidth=0.8, relheight=0.1)

        self.program_explaination_label = customtkinter.CTkLabel(master=self.middle_frame,
                                                                 text="Please enter tree sequence to find the next tree in the order")
        self.program_explaination_label.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.1)

        self.tree_sequence_input = customtkinter.CTkEntry(master=self.middle_frame,
                                                          placeholder_text="example: 1,2,3,5,7,8,9",
                                                          width=340, height=40)
        self.tree_sequence_input.place(relx=0.2, rely=0.3, relwidth=0.6, relheight=0.1)


        self.button_next = customtkinter.CTkButton(master=self.middle_frame, text="Submit",
                                                   command=self.zaks_next_tree_thread)
        # self.tree_sequence_input.get()))

        self.button_next.place(relx=0.2, rely=0.7, relwidth=0.6, relheight=0.1)


    def on_tree_from_index_click_Ruskey(self):
        self.main_window_frames()
        self.clear_mid_frame()
        self.main_title_label = customtkinter.CTkLabel(master=self.middle_frame,
                                                       text="Find Tree From Index - Ruskey and Hu's Method",
                                                       font=("Roboto Medium", -22, "bold"),
                                                       text_color=("#72CF9F", "#11B384"))
        self.main_title_label.place(relx=0.1, rely=0.0, relwidth=0.8, relheight=0.1)

        self.program_explaination_label = customtkinter.CTkLabel(master=self.middle_frame,
                                                                 text="Please enter tree index in the order in "
                                                                        "order to get the tree")
        self.program_explaination_label.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.1)



        self.tree_sequence_input = customtkinter.CTkEntry(master=self.middle_frame,
                                                          placeholder_text="example: 12",
                                                          width=340, height=40)
        self.tree_sequence_input.place(relx=0.2, rely=0.25, relwidth=0.6, relheight=0.1)

        self.rank_explaination_label = customtkinter.CTkLabel(master=self.middle_frame,
                                                                       text="Enter the tree's number of nodes of the order.")
        self.rank_explaination_label.place(relx=0.2, rely=0.45, relwidth=0.6, relheight=0.1)

        self.rank_input = customtkinter.CTkEntry(master=self.middle_frame,
                                                          placeholder_text="example: 6",
                                                          width=340, height=40)
        self.rank_input.place(relx=0.2, rely=0.6, relwidth=0.6, relheight=0.1)

        self.button_next = customtkinter.CTkButton(master=self.middle_frame, text="Submit",
                                                   command=self.ruskey_tree_from_index_thread)


        self.button_next.place(relx=0.2, rely=0.8, relwidth=0.6, relheight=0.1)

    def ruskey_tree_from_index_thread(self):
        def subscriber(arg):
            # get data from publisher
            current_tree = arg['progress']
            text = self.tree_visualizator(current_tree, "Ruskey")
            # GUI setup

            self.tree_label.insert(tkinter.END, "=>\t{}\n{}".format(text, current_tree))

            # show results
            self.window.update()

            # run tree building in thread

        self.result_popup = customtkinter.CTk()
        self.result_popup.state("zoomed")
        self.result_popup.title("Result")

        self.tree_label = tkinter.Text(self.result_popup)
        self.tree_label.place(relx=0.1, rely=0.05, relwidth=0.8, relheight=0.9)
        # self.tree_label.configure(font=(14, "bold"))
        # self.tree_label.grid(row=0, column=0, sticky="nsew")

        try:
            if self.appearance_mode == "Dark":
                self.tree_label.config(background="#474747", foreground="#11B384")
        except:

            self.tree_label.config(background="#11B384")

        # create CTk scrollbar
        self.ctk_textbox_scrollbar = customtkinter.CTkScrollbar(self.result_popup, command=self.tree_label.yview)
        self.ctk_textbox_scrollbar.place(relx=0.09, rely=0.05, relwidth=0.01, relheight=0.9)

        self.ctk_textbox_scrollbar_horizontal = customtkinter.CTkScrollbar(self.result_popup,
                                                                               command=self.tree_label.xview)
        self.ctk_textbox_scrollbar_horizontal.place(relx=0.1, rely=0.95, relwidth=0.8, relheight=0.02)

        rank = self.tree_sequence_input.get()
        n = self.rank_input.get()
        print("rank={}, n={}".format(rank, n))

        if rank=='' and n =='':
            rank = 12
            n = 6
        try:
            if rank=='' or n=='': 
                raise Exception
        except:
            messagebox.showerror("please check the input","The number of the inner nodes and the rank should be natural numbers only." )
        
        
        if int(rank)>25 or int(rank)==int(n):
            messagebox.showerror("please check the input", "The number you've entered is too big.")

        else:
            self.t1 = threading.Thread(target=self.visual_tree_from_index_ruskey(n, rank, subscriber))
            self.t1.start()

    def on_tree_from_index_click_Zaks(self):
        self.main_window_frames()
        self.clear_mid_frame()
        self.main_title_label = customtkinter.CTkLabel(master=self.middle_frame,
                                                       text="Find Tree From Index - Zaks' Method",
                                                       font=("Roboto Medium", -22, "bold"),
                                                       text_color=("#72CF9F", "#11B384"))
        self.main_title_label.place(relx=0.1, rely=0.0, relwidth=0.8, relheight=0.1)

        self.program_explaination_label = customtkinter.CTkLabel(master=self.middle_frame,
                                                                 text="Please enter tree index in the order in "
                                                                      "order to get the tree")
        self.program_explaination_label.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.1)

        self.tree_sequence_input = customtkinter.CTkEntry(master=self.middle_frame,
                                                          placeholder_text="example: 12",
                                                          width=340, height=40)
        self.tree_sequence_input.place(relx=0.2, rely=0.3, relwidth=0.6, relheight=0.1)



        self.rank_explaination_label = customtkinter.CTkLabel(master=self.middle_frame,
                                                                       text="Enter the number of the "
                                                                            "internal nodes of the tree in the order.")
        self.rank_explaination_label.place(relx=0.2, rely=0.5, relwidth=0.6, relheight=0.1)

        self.rank_input = customtkinter.CTkEntry(master=self.middle_frame,
                                                          placeholder_text="example: 5",
                                                          width=340, height=40)
        self.rank_input.place(relx=0.2, rely=0.65, relwidth=0.6, relheight=0.1)




        self.button_next = customtkinter.CTkButton(master=self.middle_frame, text="Submit",
                                                   command=self.zaks_tree_from_index_thread)
        # self.tree_sequence_input.get()))

        self.button_next.place(relx=0.2, rely=0.85, relwidth=0.6, relheight=0.1)

    def zaks_tree_from_index_thread(self):
        def subscriber(arg):

            # get data from publisher
            current_tree = arg['progress']
            text = self.tree_visualizator(current_tree, "Z")

            # GUI setup
            self.tree_label.insert(tkinter.END, "\t =>\t{}\n{}".format(text, current_tree))

            # show results
            self.window.update()

            # run tree building in thread

        rank = self.tree_sequence_input.get()
        n = self.rank_input.get()

        if rank=='' and n=='':
            rank=12
            n=5

        try:
            if rank=='' or n=='' or int(rank)==int(n):
                raise Exception
        except:
            messagebox.showerror("please check the input", "The number of the nodes and the rank should be natural numbers only.")

        self.result_popup = customtkinter.CTk()
        self.result_popup.state("zoomed")
        self.result_popup.title("Result")

        self.tree_label = tkinter.Text(self.result_popup)
        self.tree_label.place(relx=0.1, rely=0.05, relwidth=0.8, relheight=0.9)

        try:
            if self.appearance_mode == "Dark":
                self.tree_label.config(background="#474747", foreground="#11B384")
        except:

            self.tree_label.config(background="#11B384")

        # create CTk scrollbar
        self.ctk_textbox_scrollbar = customtkinter.CTkScrollbar(self.result_popup, command=self.tree_label.yview)
        self.ctk_textbox_scrollbar.place(relx=0.09, rely=0.05, relwidth=0.01, relheight=0.9)

        self.ctk_textbox_scrollbar_horizontal = customtkinter.CTkScrollbar(self.result_popup,
                                                                               command=self.tree_label.xview)
        self.ctk_textbox_scrollbar_horizontal.place(relx=0.1, rely=0.95, relwidth=0.8, relheight=0.02)

        if int(rank)>25 or int(rank)==int(n):
            messagebox.showerror("please check the input", "The number you've entered is too big.")

        else:
            self.t1 = threading.Thread(target=self.visual_tree_from_index_zaks(n, rank, subscriber))
            self.t1.start()

    def on_order_of_trees_from_rank_click_zaks(self):
        self.main_window_frames()
        self.clear_mid_frame()
        self.main_title_label = customtkinter.CTkLabel(master=self.middle_frame,
                                                       text="Find All Trees - Zaks' Method",
                                                       font=("Roboto Medium", -22, "bold"),
                                                       text_color=("#72CF9F", "#11B384"))
        self.main_title_label.place(relx=0.1, rely=0.0, relwidth=0.8, relheight=0.1)

        self.program_explaination_label = customtkinter.CTkLabel(master=self.middle_frame,
                                                                 text="Please enter number of nodes in the tree "
                                                                      "to get the all the trees in the order")
        self.program_explaination_label.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.1)

        self.tree_rank_input = customtkinter.CTkEntry(master=self.middle_frame,
                                                          placeholder_text="example: 5",
                                                          width=340, height=40)
        self.tree_rank_input.place(relx=0.2, rely=0.3, relwidth=0.6, relheight=0.1)



        self.button_next = customtkinter.CTkButton(master=self.middle_frame, text="Submit",
                                                   command=self.zaks_many_trees_from_index_thread)

        self.button_next.place(relx=0.2, rely=0.5, relwidth=0.6, relheight=0.1)

    def zaks_many_trees_from_index_thread(self):
        def subscriber(arg):
            # get data from publisher
            current_tree = arg['progress']
            text = self.tree_visualizator(current_tree, "Z")
            # GUI setup

            self.tree_label.insert(tkinter.END, "=>\t{}\n{}".format(text, current_tree))

            # show results
            self.window.update()

            # run tree building in thread

        n = self.tree_rank_input.get()

        if n=='':
            n=5

        try:
            int(n)
        except:
            messagebox.showerror("please check the input","The number of the nodes should be a natural number only." )

        if int(n)>25:
            messagebox.showerror("please check the input", "The number you've entered is too big.")

        else:

            self.result_popup = customtkinter.CTk()
            self.result_popup.state("zoomed")
            self.result_popup.title("Result")

            self.tree_label = tkinter.Text(self.result_popup)
            self.tree_label.place(relx=0.1, rely=0.05, relwidth=0.8, relheight=0.9)

            try:
                if self.appearance_mode == "Dark":
                    self.tree_label.config(background="#474747", foreground="#11B384")
            except:

                self.tree_label.config(background="#11B384")

            # create CTk scrollbar
            self.ctk_textbox_scrollbar = customtkinter.CTkScrollbar(self.result_popup, command=self.tree_label.yview)
            self.ctk_textbox_scrollbar.place(relx=0.09, rely=0.05, relwidth=0.01, relheight=0.9)

            self.ctk_textbox_scrollbar_horizontal = customtkinter.CTkScrollbar(self.result_popup,
                                                                                command=self.tree_label.xview)
            self.ctk_textbox_scrollbar_horizontal.place(relx=0.1, rely=0.95, relwidth=0.8, relheight=0.02)

            alg = TreeOrderingAlgoritms.LexicographicTreeOrdering(None)
            amount = int(alg.catalan(int(n)))
            for i in range(amount):
                self.tree_label.insert(tkinter.END, "\n\n")
                print(i,amount)
                self.t1 = threading.Thread(target=self.visual_tree_from_index_zaks(int(n), int(i), subscriber))
                self.t1.start()


    def on_order_of_trees_from_rank_click_ruskey(self):
        self.main_window_frames()
        self.clear_mid_frame()
        self.main_title_label = customtkinter.CTkLabel(master=self.middle_frame,
                                                       text="Find All Trees - Ruskey and Hu's Method",
                                                       font=("Roboto Medium", -22, "bold"),
                                                       text_color=("#72CF9F", "#11B384"))
        self.main_title_label.place(relx=0.1, rely=0.0, relwidth=0.8, relheight=0.1)

        self.program_explaination_label = customtkinter.CTkLabel(master=self.middle_frame,
                                                                 text="Please enter number of nodes in the tree "
                                                                        "to get the all the trees in the order")
        self.program_explaination_label.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.1)


        self.tree_rank_input = customtkinter.CTkEntry(master=self.middle_frame,
                                                          placeholder_text="example: 6",
                                                          width=340, height=40)
        self.tree_rank_input.place(relx=0.2, rely=0.3, relwidth=0.6, relheight=0.1)

        self.button_next = customtkinter.CTkButton(master=self.middle_frame, text="Submit",
                                                   command=self.ruskey_many_trees_from_index_thread)

        self.button_next.place(relx=0.2, rely=0.5, relwidth=0.6, relheight=0.1)


    def ruskey_many_trees_from_index_thread(self):
        def subscriber(arg):
            # get data from publisher
            current_tree = arg['progress']
            text = self.tree_visualizator(current_tree, "Ruskey")
            # GUI setup

            self.tree_label.insert(tkinter.END, "=>\t{}\n{}".format(text, current_tree))

            # show results
            self.window.update()

            # run tree building in thread

        n = self.tree_rank_input.get()


        if n=='':
            n=6

        try:
            int(n)
        except:
            messagebox.showerror("please check the input","The depth should be a natural number only." )


        if int(n)>25:
            messagebox.showerror("please check the input", "The number you've entered is too big.")

        else:
            self.result_popup = customtkinter.CTk()
            self.result_popup.state("zoomed")
            self.result_popup.title("Result")

            self.tree_label = tkinter.Text(self.result_popup)
            self.tree_label.place(relx=0.1, rely=0.05, relwidth=0.8, relheight=0.9)


            try:
                if self.appearance_mode == "Dark":
                    self.tree_label.config(background="#474747", foreground="#11B384")
            except:

                self.tree_label.config(background="#11B384")

            # create CTk scrollbar
            self.ctk_textbox_scrollbar = customtkinter.CTkScrollbar(self.result_popup, command=self.tree_label.yview)
            self.ctk_textbox_scrollbar.place(relx=0.09, rely=0.05, relwidth=0.01, relheight=0.9)

            self.ctk_textbox_scrollbar_horizontal = customtkinter.CTkScrollbar(self.result_popup,
                                                                                command=self.tree_label.xview)
            self.ctk_textbox_scrollbar_horizontal.place(relx=0.1, rely=0.95, relwidth=0.8, relheight=0.02)

            alg = TreeOrderingAlgoritms.LexicographicTreeOrdering(None)
            amount = int(alg.catalan(int(n)))
            for i in range(amount):
                self.tree_label.insert(tkinter.END, "\n\n")
                print(i,amount)
                self.t1 = threading.Thread(target=self.visual_tree_from_index_ruskey(int(n), int(i), subscriber))
                self.t1.start()


    def index_from_tree_click_zaks(self):
        self.main_window_frames()
        self.clear_mid_frame()
        self.main_title_label = customtkinter.CTkLabel(master=self.middle_frame,
                                                       text="Find Index From Tree - Zaks' Method",
                                                       font=("Roboto Medium", -22, "bold"),
                                                       text_color=("#72CF9F", "#11B384"))
        self.main_title_label.place(relx=0.1, rely=0.0, relwidth=0.8, relheight=0.1)

        self.program_explaination_label = customtkinter.CTkLabel(master=self.middle_frame,
                                                                 text="Please enter a sequence of a tree in the order "
                                                                      "to get the index of it in the order")
        self.program_explaination_label.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.1)

        self.tree_sequence_input = customtkinter.CTkEntry(master=self.middle_frame,
                                                      placeholder_text="example: 1,2,3,5,6,11,12",
                                                      width=340, height=40)
        self.tree_sequence_input.place(relx=0.2, rely=0.3, relwidth=0.6, relheight=0.1)

        self.button_next = customtkinter.CTkButton(master=self.middle_frame, text="Submit",
                                                   command=self.zaks_index_from_tree_thread)
        # self.tree_sequence_input.get()))

        self.button_next.place(relx=0.2, rely=0.5, relwidth=0.6, relheight=0.1)


    def index_from_tree_click_ruskey(self):
        self.main_window_frames()
        self.clear_mid_frame()
        self.main_title_label = customtkinter.CTkLabel(master=self.middle_frame,
                                                       text="Find Index From Tree - Ruskey and Hu's Method",
                                                       font=("Roboto Medium", -22, "bold"),
                                                       text_color=("#72CF9F", "#11B384"))
        self.main_title_label.place(relx=0.1, rely=0.0, relwidth=0.8, relheight=0.1)

        self.program_explaination_label = customtkinter.CTkLabel(master=self.middle_frame,
                                                                 text="Please enter a sequence of a tree in the order "
                                                                      "to get the index of it in the order")
        self.program_explaination_label.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.1)


        self.tree_sequence_input = customtkinter.CTkEntry(master=self.middle_frame,
                                                      placeholder_text="example: 3,5,5,4,2,3,3,2",
                                                      width=340, height=40)
        self.tree_sequence_input.place(relx=0.2, rely=0.3, relwidth=0.6, relheight=0.1)

        self.button_next = customtkinter.CTkButton(master=self.middle_frame, text="Submit",
                                                   command=self.ruskey_index_from_tree_thread)

        self.button_next.place(relx=0.2, rely=0.5, relwidth=0.6, relheight=0.1)


    def zaks_index_from_tree_thread(self):
        def subscriber(arg):

            # get data from publisher
            current_rank = arg['progress']


            # show results
            self.window.update()

            # run tree building in thread

        sequence = self.tree_sequence_input.get()

        if sequence == '':
            sequence = "1,2,3,5,6,11,12"

        try:

            sequence = list(sequence.split(","))
            sequence = list(int(i) for i in sequence)

            if type == "Z":
                if not (self.zaks_isFeasible_z(sequence, len(sequence))):
                    messagebox.showerror("please check the input", "The sequence should represent a feasible tree.")
            if type == "X":
                if not (self.zaks_isFeasible_x(sequence)):
                    messagebox.showerror("please check the input", "The sequence should represent a feasible tree.")
        except:
            messagebox.showerror("please check the input", "Please make sure the sequence is valid.")

        self.result_popup = customtkinter.CTk()
        self.result_popup.state("zoomed")
        self.result_popup.title("Result")

        self.tree_label = tkinter.Text(self.result_popup)
        self.tree_label.place(relx=0.1, rely=0.05, relwidth=0.8, relheight=0.9)

        try:
            if self.appearance_mode == "Dark":
                self.tree_label.config(background="#474747", foreground="#11B384")
        except:

            self.tree_label.config(background="#11B384")

        # create CTk scrollbar
        self.ctk_textbox_scrollbar = customtkinter.CTkScrollbar(self.result_popup, command=self.tree_label.yview)
        self.ctk_textbox_scrollbar.place(relx=0.09, rely=0.05, relwidth=0.01, relheight=0.9)

        self.ctk_textbox_scrollbar_horizontal = customtkinter.CTkScrollbar(self.result_popup,
                                                                               command=self.tree_label.xview)
        self.ctk_textbox_scrollbar_horizontal.place(relx=0.1, rely=0.95, relwidth=0.8, relheight=0.02)

        text = self.tree_visualizator(sequence, "Z")
        # GUI setup
        self.tree_label.insert(tkinter.END, "=>\t{}".format((text)))


        self.t1 = threading.Thread(target=self.visual_index_from_tree_zaks(sequence, subscriber))
        self.t1.start()

    def ruskey_index_from_tree_thread(self):
        def subscriber(arg):

            # get data from publisher
            current_rank = arg['progress']
            text = self.tree_visualizator(current_rank, "Ruskey")
            # rank = int(current_rank[0])
            # GUI setup

            self.tree_label.insert(tkinter.END, "=>\t{}".format(text))

            # show results
            self.window.update()

            # run tree building in thread

        sequence = self.tree_sequence_input.get()

        if sequence == '':
            sequence = "3,5,5,4,2,3,3,2"

        try:

            sequence = list(sequence.split(","))
            sequence = list(int(i) for i in sequence)
            print(sequence)

            if (self.ruskey_isFeasible(sequence, len(sequence))) == False:
                messagebox.showerror("please check the input", "The sequence should represent a feasible tree.")
        except:
            messagebox.showerror("please check the input", "Please make sure the sequence is valid.")

        self.result_popup = customtkinter.CTk()
        self.result_popup.state("zoomed")
        self.result_popup.title("Result")

        self.tree_label = tkinter.Text(self.result_popup)
        self.tree_label.place(relx=0.1, rely=0.05, relwidth=0.8, relheight=0.9)


        try:
            if self.appearance_mode == "Dark":
                self.tree_label.config(background="#474747", foreground="#11B384")
        except:

            self.tree_label.config(background="#11B384")

        # create CTk scrollbar
        self.ctk_textbox_scrollbar = customtkinter.CTkScrollbar(self.result_popup, command=self.tree_label.yview)
        self.ctk_textbox_scrollbar.place(relx=0.09, rely=0.05, relwidth=0.01, relheight=0.9)

        self.ctk_textbox_scrollbar_horizontal = customtkinter.CTkScrollbar(self.result_popup,
                                                                               command=self.tree_label.xview)
        self.ctk_textbox_scrollbar_horizontal.place(relx=0.1, rely=0.95, relwidth=0.8, relheight=0.02)

        self.t1 = threading.Thread(target=self.visual_index_from_tree_ruskey(sequence, subscriber))
        self.t1.start()


    def on_compare_click(self):
        self.main_window_frames()
        self.clear_mid_frame()

        self.main_title_label = customtkinter.CTkLabel(master=self.middle_frame,
                                                       text="Enter a number of internal nodes to see a comparison of\n the run "
                                                            "times between the algorithms of Ruskey and Zaks.\n "
                                                            "The output graph will show how much time it took to \n"
                                                            "generate all the trees in the order for each number of \n"
                                                            "internal leaves up to the number you have entered.",
                                                       font=("Roboto Medium", -22, "bold"),
                                                       text_color=("#72CF9F", "#11B384"))
        self.main_title_label.place(relx=0.1, rely=0.05, relwidth=0.8, relheight=0.3)


        self.internal_nodes_input = customtkinter.CTkEntry(master=self.middle_frame,
                                                          placeholder_text="example: 5",
                                                          width=340, height=40)
        self.internal_nodes_input.place(relx=0.2, rely=0.4, relwidth=0.6, relheight=0.1)



        self.button_next = customtkinter.CTkButton(master=self.middle_frame, text="Submit",
                                                   command=self.algorithm_comparison_thread)


        self.button_next.place(relx=0.2, rely=0.6, relwidth=0.6, relheight=0.1)

        self.progress_label = customtkinter.CTkLabel(master=self.middle_frame,
                                                       text="Progress Bar:")
        self.progress_label.place(relx=0.2, rely=0.8, relwidth=0.6, relheight=0.1)

        self.progress_bar_shadow = customtkinter.CTkLabel(master=self.middle_frame, text="", bg_color="#72CF9F")
        self.progress_bar_shadow.place(relx=0.2, rely=0.9, relwidth=0.00, relheight=0.03)

        self.progress_bar = customtkinter.CTkLabel(master=self.middle_frame, text="", bg_color="#11B384")
        self.progress_bar.place(relx=0.2, rely=0.9, relwidth=0.00, relheight=0.05)

    def algorithm_comparison_thread(self):
        def subscriber_ruskey(arg):

            self.window.update()

        def subscriber_zaks(arg):

                self.window.update()

        input_nodes = self.internal_nodes_input.get()
    

        if input_nodes=='':
            input_nodes=5

        input_nodes = int(input_nodes)

        if input_nodes>15:
            messagebox.showerror("please check the input", "The number you've entered is too big.")

        self.tree_label = tkinter.Text(self.window)

        alg = TreeOrderingAlgoritms.LexicographicTreeOrdering(None)
        
        time_table_ruskey = [0] * input_nodes
        for j in range(input_nodes):
            time_table_ruskey[j] = time.time_ns()
            amount = int(alg.catalan(j))
            print(amount)
            for i in range(amount):
                self.tree_label.insert(tkinter.END, "\n\t\t{}\n".format(i))
                print(i, amount)
                alg = TreeOrderingAlgoritms.LexicographicTreeOrdering(subscriber_ruskey)

                next_seq = alg.Unrank(int(input_nodes)+1, int(i))

            time_table_ruskey[j] = time.time_ns() - time_table_ruskey[j]

            self.progress_bar.place(relx=0.2, rely=0.9, relwidth=(j/(2.5*input_nodes))*0.8, relheight=0.05)
            self.window.update()

        alg = TreeOrderingAlgoritms.LexicographicTreeOrdering(None)
        

        time_table_zaks = [0] * input_nodes

        for j in range(input_nodes):
            amount = int(alg.catalan(j))
            print(amount)
            time_table_zaks[j] = time.time_ns()
            for i in range(amount):
                self.tree_label.insert(tkinter.END, "\n\t\t{}\n".format(i))
                print(i, amount)



                alg = TreeOrderingAlgoritms.LexicographicTreeOrdering(subscriber_zaks)
                next_seq = alg.unrank_zaks(int(input_nodes), int(i))

            time_table_zaks[j] = time.time_ns() - time_table_zaks[j]
            self.progress_bar.place(relx=0.2, rely=0.9, relwidth=( (j+input_nodes) / (2.5 * input_nodes)) * 0.8, relheight=0.05)
            self.window.update()

        self.result_popup = customtkinter.CTk()
        self.result_popup.state("zoomed")
        self.result_popup.title("Result")

        # the figure that will contain the plot
        fig = Figure(figsize=(8, 8),
                     dpi=100)

        num_array = list(range(1, int(input_nodes)+1))

        # adding the subplot
        plot1 = fig.add_subplot(111)

        # plotting the graph
        plot1.plot(num_array, time_table_ruskey, label='Ruskey')
        plot1.plot(num_array, time_table_zaks, label='Zaks')

        avg_zaks = sum(time_table_zaks)/len(time_table_zaks)
        avg_ruskey = sum(time_table_ruskey)/len(time_table_ruskey)

        print("ruskey: {}, Zaks: {}".format(avg_ruskey, avg_zaks))

        plot1.set_xlabel('number of internal nodes')
        plot1.set_ylabel('runtime (in seconds)')

        # displaying the title
        plot1.set_title("Ruskey And Zaks Runtimes As A Function Of The Number Of Internal Nodes")

        labelLines(plot1.get_lines(), zorder=2.5)



        # creating the Tkinter canvas
        # containing the Matplotlib figure
        canvas = FigureCanvasTkAgg(fig,
                                   master=self.result_popup)
        canvas.draw()

        # placing the canvas on the Tkinter window
        canvas.get_tk_widget().pack()

        # creating the Matplotlib toolbar
        toolbar = NavigationToolbar2Tk(canvas,
                                       self.result_popup)
        toolbar.update()

        # placing the toolbar on the Tkinter window
        canvas.get_tk_widget().pack()


    def on_more_information_click(self):
        self.main_window_frames()
        self.clear_mid_frame()
        self.main_title_label_e = customtkinter.CTkLabel(master=self.middle_frame,
                                                       text="Welcome To rootOrder - A lexicographical "
                                                            "Tree Ordering Program",
                                                       font=("Roboto Medium", -24, "bold"),
                                                       text_color=("#72CF9F", "#11B384"))
        self.main_title_label_e.grid(row=1, column=1, pady=40, padx=180)

        self.program_explaination_label = customtkinter.CTkLabel(master=self.middle_frame,
                                                                 text="This program is based on algorithms by F. "
                                                                      "Ruskey, T.C. Huo and S. Zaks.\n"
                                                                      " It crates trees according to lexicografical "
                                                                      "order and "
                                                                      "orders given trees in lexicographical order.\n"
                                                                      "We invite you to explore this fascinating "
                                                                      "subject and "
                                                                      "experiment with our work.")  # ,

        self.program_explaination_label.grid(row=2, column=1, pady=10, padx=180)

        self.middle_frame.grid_rowconfigure(3, weight=1)  # empty row as spacing

        self.related_content_frame = customtkinter.CTkFrame(master=self.middle_frame, width=1080, height=350,
                                                            fg_color=("#11B384", "gray28"))

        self.related_content_frame.grid(row=9, column=1, sticky="nswe", padx=20, pady=20)

        zaks_image_path = "images/Zaks.jpg"
        img = Image.open(zaks_image_path)
        img = img.resize((250, 350))
        img = ImageOps.grayscale(img)

        image_zaks = ImageTk.PhotoImage(img)

        zaks_photo_label = customtkinter.CTkLabel(master=self.related_content_frame, image=image_zaks, text="")
        zaks_photo_label.image = image_zaks
        zaks_photo_label.place(relx=0.2, rely=0.05, relwidth=0.6, relheight=0.8)

        hu_image_path = "images/hu.jpg"
        img = Image.open(hu_image_path)
        img = img.resize((250, 350))
        img = ImageOps.grayscale(img)
        image_hu = ImageTk.PhotoImage(img)

        hu_photo_label = customtkinter.CTkLabel(master=self.related_content_frame, image=image_hu, text="")
        hu_photo_label.image = image_hu
        hu_photo_label.place(relx=0.7, rely=0.05, relwidth=0.2, relheight=0.8)

        icon_image_path = "images/icon4.png"
        img = Image.open(icon_image_path)
        img = img.resize((250, 350))
        image_icon = ImageTk.PhotoImage(img)
        self.window.iconphoto(False, image_icon)

    def ruskey_next_tree_visual(self, sequence, subscriber):

        t1 = time.time_ns()

        alg = TreeOrderingAlgoritms.LexicographicTreeOrdering(subscriber)

        next_seq = alg.NextTree(sequence)
        text = self.tree_visualizator(next_seq, "Ruskey")

        print(time.time_ns() - t1)

        try:
            self.t1.join()
        except:
            print("")

    def zaks_next_tree_visual(self, sequence, type, subscriber):
        t1 = time.time_ns()
        alg = TreeOrderingAlgoritms.LexicographicTreeOrdering(subscriber)

        next_seq = alg.NextTreeZaks(sequence)
        print(next_seq)
        text = self.tree_visualizator(next_seq, "Z")
        self.tree_label.insert(tkinter.END, "=>{}\n{}".format(text, next_seq))

        print(time.time_ns() - t1)

        try:
            self.t1.join()
        except:
            print("")

    def visual_tree_from_index_ruskey(self, rank, index, subscriber):
        t1 = time.time_ns()
        alg = TreeOrderingAlgoritms.LexicographicTreeOrdering(subscriber)

        next_seq = alg.Unrank(int(rank), int(index))
        print(next_seq)
        text = self.tree_visualizator(next_seq, "Ruskey")
        self.tree_label.insert(tkinter.END, "=>{}\n{}".format(text, next_seq))

        print(time.time_ns() - t1)

        try:
            self.t1.join()
        except:
            print("")

    def visual_tree_from_index_zaks(self, rank, index, subscriber):
        t1 = time.time_ns()

        alg = TreeOrderingAlgoritms.LexicographicTreeOrdering(subscriber)

        if rank=='' or index=='':
             raise Exception("One or more of the inputs is empty")
        print(rank, index)
        next_seq = alg.unrank_zaks(int(rank), int(index))

        print(time.time_ns() - t1)

        try:
            self.t1.join()
        except:
            print("")

    def visual_index_from_tree_zaks(self, sequence, subscriber):
        t1 = time.time_ns()
        alg = TreeOrderingAlgoritms.LexicographicTreeOrdering(subscriber)
        result = alg.rank_zaks(sequence, len(sequence))
        self.tree_label.insert(tkinter.END, "\n{}\n{}".format(int(result), sequence))

        print(time.time_ns() - t1)

        try:
            self.t1.join()
        except:
            print("")

    def visual_index_from_tree_ruskey(self, sequence, subscriber):
        t1 = time.time_ns()
        alg = TreeOrderingAlgoritms.LexicographicTreeOrdering(subscriber)
        result = alg.Rank(sequence)
        self.tree_label.insert(tkinter.END, "\n{}".format(int(result)))
        print(time.time_ns() - t1)

        try:
            self.t1.join()
        except:
            print("")

    def tree_visualizator(self, sequence, type):
        tree = TreeNode()
        res = None
        text = ""
        if not isinstance(sequence, list):
            sequence = list(sequence.split(","))
            sequence = list(int(i) for i in sequence)
        print(sequence)

        if type == "X":
            res = tree.create_tree(sequence, len(sequence)-1)

            text = res.treeString()

        elif type == "Z":
            x = [0]*len(sequence)*2
            x_sequence = tree.z_to_x(x, sequence)
            print(x_sequence)
            res = tree.create_tree(x_sequence, len(x_sequence)-1)
            text = res.treeString()

        elif type == "Ruskey":
            letters = []
            for i in range(len(sequence)):
                letters.append(chr(ord("a") + i))
            seq_set = zip(letters, sequence)
            seq_set = list(seq_set)
            res = tree.SequenceToTree(seq_set)
            text = res.treeString()

        return text


    def clear_mid_frame(self):
        self.middle_frame.destroy()
        self.middle_frame = customtkinter.CTkFrame(master=self.window, width=1080)
        self.middle_frame.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)

    def button_event(self):
        print("Button pressed")

    def change_appearance_mode(self, new_appearance_mode):
        self.appearance_mode = new_appearance_mode
        customtkinter.set_appearance_mode(new_appearance_mode)
        self.window.state("zoomed")

    def change_sequence_type_mode(self, new_tree_type_mode):
        self.tree_mode = new_tree_type_mode
        self.__init__(self.window, self.tree_mode)


    def zaks_isFeasible_z(self, z, n):
        if (len(z) != n):
            return False
        j = 0
        cnt = 0
        for i in range(0, 2 * n):
            if (j < n and z[j] == (i + 1)):
                cnt += 1
                j += 1
            else:
                cnt -= 1
            if (cnt < 0):
                return False
        return True

    def zaks_isFeasible_x(self, x):
        counter = 0
        for i in x:
            if i==0:
                counter-=1
            elif i==1:
                counter+=1
            else:
                raise Exception

        if counter == 0:
            return True
        else:
            return False

    def ruskey_isFeasible(self, l, n):
        temp_n = n
        temp_l = l
        if (len(l) != n):
            return False
        while True:
            next_temp_l = list()
            i = 0
            flag = True
            while (i < temp_n):
                if (i != temp_n - 1):
                    if (flag and temp_l[i] == temp_l[i + 1]):
                        next_temp_l.append(temp_l[i] - 1)
                        i += 2
                        flag = False
                    else:
                        next_temp_l.append(temp_l[i])
                        i += 1
                else:
                    next_temp_l.append(temp_l[i])
                    i += 1
            if (len(next_temp_l) == 1 and next_temp_l[0] == 0):
                return True
            elif (len(next_temp_l) == len(temp_l)):
                return False
            temp_l = next_temp_l.copy()
            temp_n = len(temp_l)
            next_temp_l = list()



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    customtkinter.set_appearance_mode("system")  # Modes: system (default), light, dark
    customtkinter.set_default_color_theme("green")  # Themes: blue (default), dark-blue, green
    window = customtkinter.CTk()  # create CTk window like you do with the Tk window

    GUI(window, "Binary")
