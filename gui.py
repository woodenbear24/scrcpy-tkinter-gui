from lib import *

applist = []
devices = []
cmd = "Empty"


def create_interface():
    """Creates the main window and interface elements."""
    main_window = tk.Tk()
    main_window.title("Scrcpy Gui test")
    main_window.geometry("500x500")
    main_window.iconbitmap("icon.ico")
    # main_window.protocol("WM_DELETE_WINDOW", minimize_to_tray(main_window))

    # Use PanedWindow to create a left-right layout, resizable areas
    paned_window = tk.PanedWindow(main_window, orient=tk.HORIZONTAL)
    paned_window.pack(fill=tk.BOTH, expand=True)

    # Left frame to hold button and list
    left_frame = Frame(paned_window)
    paned_window.add(left_frame)

    # Button at the top of the left frame
    list_top_button = Button(left_frame, text="Refresh", command=lambda: Refresh_List(entry0, listbox))
    list_top_button.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)  # 靠顶部, 水平填充

    # Create listbox with scrollbar
    list_scrollbar = Scrollbar(left_frame, orient=tk.VERTICAL)
    list_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Sample list data
    listbox = Listbox(left_frame, yscrollcommand=list_scrollbar.set)
    for item in applist:
        listbox.insert(tk.END, item)
    listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)  # 填充剩余空间

    list_scrollbar.config(command=listbox.yview)

    # Right frame for inputs and button
    right_frame = Frame(paned_window)
    paned_window.add(right_frame)
    right_frame.grid_columnconfigure(0, weight=1)  # Allow column to expand
    right_frame.grid_columnconfigure(1, weight=1)
    right_frame.grid_columnconfigure(2, weight=0)
    # 绑定点击事件
    listbox.bind("<ButtonRelease-1>", lambda event: Select_List(listbox, entry1, event))
    listbox.bind("<Return>", lambda event: Select_List(listbox, entry1, event))

    label1 = tk.Label(right_frame, text="Device:")
    label1.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
    entry0 = ttk.Combobox(right_frame, values=devices, state="readonly")
    entry0.grid(row=0, column=1, sticky=tk.EW, padx=5, pady=5)
    entry0.bind("<ButtonRelease-1>", lambda event: Refresh_Devices(entry0, event))

    # First input field
    label1 = tk.Label(right_frame, text="App Name:")
    label1.grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
    entry1 = Entry(right_frame)
    entry1.grid(row=1, column=1, sticky=tk.EW, padx=5, pady=5)

    # Second input field
    label2 = tk.Label(right_frame, text="Bitrate(M):")
    label2.grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
    entry2 = Entry(right_frame)
    entry2.grid(row=2, column=1, sticky=tk.EW, padx=5, pady=5)

    # Third input field
    label3 = tk.Label(right_frame, text="Video Codec:")
    label3.grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
    entry3 = ttk.Combobox(right_frame, values=("h264", "h265", "av1"))
    entry3.grid(row=3, column=1, sticky=tk.EW, padx=5, pady=5)

    # Fourth input field
    label4 = tk.Label(right_frame, text="Other Args:")
    label4.grid(row=4, column=0, sticky=tk.W, padx=5, pady=5)
    entry4 = Entry(right_frame)
    entry4.grid(row=4, column=1, sticky=tk.EW, padx=5, pady=5)

    # Button
    button0 = Button(right_frame, text="Load Setting", command=lambda: Setting(entry2, entry3, entry4, 0))
    button0.grid(row=5, column=0, sticky=tk.EW, columnspan=2, padx=20, pady=1)
    button1 = Button(right_frame, text="Save Setting", command=lambda: Setting(entry2, entry3, entry4, 1))
    button1.grid(row=6, column=0, sticky=tk.EW, columnspan=2, padx=20, pady=1)
    button2 = Button(right_frame, text="Execute", command=lambda: cmd_generate(entry0, entry1, entry2, entry3, entry4))
    button2.grid(row=7, column=0, sticky=tk.EW, columnspan=2, padx=20, pady=1)

    # init
    Refresh_Devices(entry0, None)
    Refresh_List(entry0, listbox)
    Setting(entry2, entry3, entry4, 0)

    main_window.mainloop()


if __name__ == "__main__":
    create_interface()
