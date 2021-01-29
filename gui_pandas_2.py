import tkinter as tk
import pandas as pd
from tkinter import filedialog, messagebox, ttk
import matplotlib.pyplot as plt
import numpy as np

#Constants
my_blue = "#80c1ff"

class Page(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
    def show(self):
        self.lift()

class Page1(Page):
   def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

        frame = tk.LabelFrame(self, text="Excel Data")
        frame.place(height=250,width=800)

        file_frame=tk.LabelFrame(self, text="Open File")
        file_frame.place(height=100,width=600,rely=0.65,relx=0)

        button1 = tk.Button(file_frame,text = "Browse a File", command=lambda: File_dialog())
        button1.place(rely=0.65,relx=0.3)

        button2 = tk.Button(file_frame,text = "Load File",command = lambda: Load_excel_data())
        button2.place(rely=0.65,relx=0.5)

        button3 = tk.Button(file_frame,text = "Load Graphs",command = lambda: Load_graphs())
        button3.place(rely=0.65,relx=0.7)

        label_file=ttk.Label(file_frame,text="No File Selected")
        label_file.place(rely=0,relx=0)


        tv1 = ttk.Treeview(frame)
        tv1.place(relheight=1,relwidth=1)

        treescrolly = tk.Scrollbar(frame, orient="vertical",command=tv1.yview)
        treescrollx = tk.Scrollbar(frame, orient="horizontal",command=tv1.xview)
        tv1.configure(xscrollcommand=treescrollx.set, yscrollcommand = treescrolly.set)
        treescrollx.pack(side="bottom",fill="x")
        treescrolly.pack(side="right", fill="y")

        def File_dialog():
            filename=filedialog.askopenfilename(initialdir="/",
                                        title="Select a File",
                                        filetype=(("csv files", "*.csv"),("All Files", "*.*")))
            label_file["text"] = filename

        def Load_excel_data():
            file_path = label_file["text"]
            try:
                excel_filename = r"{}".format(file_path)
                if excel_filename[-4:] == ".csv":
                    df = pd.read_csv(excel_filename)
                else:
                    df = pd.read_excel(excel_filename)

            except ValueError:
                tk.messagebox.showerror("Information", "The file you have chosen is invalid")
                return None
            except FileNotFoundError:
                tk.messagebox.showerror("Information", f"No such file as {file_path}")
                return None

            clear_data()
            tv1["column"] = list(df.columns)
            tv1["show"] = "headings"
            for column in tv1["columns"]:
                tv1.heading(column, text=column) # let the column heading = column name

            df_rows = df.to_numpy().tolist() # turns the dataframe into a list of lists
            for row in df_rows:
                tv1.insert("", "end", values=row) # inserts each list into the treeview. For parameters see https://docs.python.org/3/library/tkinter.ttk.html#tkinter.ttk.Treeview.insert
            return None

        def Load_graphs():
            medical_file_path='medical_cost - medical_cost (1).csv'
            df = pd.read_csv(medical_file_path)

            child_list=df.loc[:,"children"].unique()
            child_dict = {}
            child_set=set(child_list)
            for each_child in child_set:
              children = df.loc[:,"children"]
              filter_df=(children==each_child)
              child_dict[each_child]=[df.loc[filter_df, 'ID'].count()]
            children1_graph = pd.DataFrame(child_dict).plot(kind='bar', edgecolor = 'white', color = ["#add1eb", "#6daedb", "#4b9ad2", "#2970a3", "#256593", "#1d4f72"])
            children1_graph.set_ylabel("Number of Families")
            children1_graph.set_xlabel("Number of Kids")

            smoker_costs = []
            non_smoker_costs = []
            smoker_type = df.loc[:,'smoker']
            f_smoker_df = smoker_type == 'yes'
            smoker_df = df.loc[f_smoker_df, :]
            f_non_smoker_df = smoker_type == 'no'
            non_smoker_df = df.loc[f_non_smoker_df, : ]
            smoker_charges = smoker_df.loc[:, 'charges']
            non_smoker_charges = non_smoker_df.loc[:, 'charges']
            for cost in smoker_charges:
                smoker_costs.append(cost)
            for cost in non_smoker_charges:
                non_smoker_costs.append(cost)
            average_smoker_costs = np.mean(smoker_costs)
            average_non_smoker_costs = np.mean(non_smoker_costs)
            print(average_smoker_costs)
            print(average_non_smoker_costs)
            average_smoking_costs_list = [average_smoker_costs, average_non_smoker_costs]
            smoke1_graph = pd.DataFrame(average_smoking_costs_list,['Smokers','Non-Smokers']).plot(kind = 'barh', color = '#6daedb')
            smoke1_graph.set_xlabel("Costs Paid To-Date (USD")
            smoke1_graph.set_ylabel("Smokers vs Non Smokers")
            smoke1_graph.get_legend().remove()

            mean_childs_cost_dict = {}
            childs_num = df.loc[:,'children']
            for i in range(6):
                f_childs_df = childs_num == i
                childs_df = df.loc[f_childs_df, :]
                childs_charges = childs_df.loc[:, 'charges']
                total_charges = 0
                patient_count = 0
                for charge in childs_charges:
                    total_charges += charge
                    patient_count += 1
                    mean_childs_cost_dict[i] = [total_charges/patient_count]
            mean_cost_df = mean_childs_cost_dict
            children_graph = pd.DataFrame(mean_cost_df).plot(kind = 'bar', edgecolor = 'white', color = ["#add1eb", "#6daedb", "#4b9ad2", "#2970a3", "#256593", "#1d4f72"])
            children_graph.set_xlabel("Number of Children (see legend)")
            children_graph.set_ylabel("Cost Paid To-Date (USD)")
            smoker_df = df.loc[:, 'smoker']
            filter_smoke = smoker_df == 'yes'
            filter_nonsmoker = smoker_df == 'no'
            bmi_smoker = df.loc[filter_smoke, 'bmi']
            charges_smoker = df.loc[filter_smoke, 'charges']
            bmi_nonsmoker = df.loc[filter_nonsmoker, 'bmi']
            charges_nonsmoker = df.loc[filter_nonsmoker, 'charges'] 
            plt.figure()
            plt.scatter(bmi_smoker, charges_smoker, color = '#173753')
            plt.scatter(bmi_nonsmoker, charges_nonsmoker, color = '#6daedb')
            plt.legend(['Smokers', 'Non-Smokers'])
            plt.show()

        def clear_data():
            tv1.delete(*tv1.get_children())

class Page2(Page):
   def __init__(self, *args, **kwargs):
       Page.__init__(self, *args, **kwargs)
       label = tk.Label(self, text="This is page 2")
       label.pack(side="top", fill="both", expand=True)

class Page3(Page):
   def __init__(self, *args, **kwargs):
       Page.__init__(self, *args, **kwargs)
       label = tk.Label(self, text="This is page 3")
       label.pack(side="top", fill="both", expand=True)

class MainView(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        p1 = Page1(self)
        p2 = Page2(self)
        p3 = Page3(self)

        buttonframe = tk.Frame(self)
        container = tk.Frame(self)
        buttonframe.pack(side="top", fill="x", expand=False)
        container.pack(side="top", fill="both", expand=True)

        p1.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p2.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p3.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

        b1 = tk.Button(buttonframe, text="Load CSV", command=p1.lift)
        b2 = tk.Button(buttonframe, text="Page 2", command=p2.lift)
        b3 = tk.Button(buttonframe, text="Page 3", command=p3.lift)

        b1.pack(side="left")
        b2.pack(side="left")
        b3.pack(side="left")

        p1.show()

if __name__ == "__main__":
    root = tk.Tk()
    main = MainView(root)
    main.pack(side="top", fill="both", expand=True)
    root.wm_geometry("600x400")
    root.mainloop()