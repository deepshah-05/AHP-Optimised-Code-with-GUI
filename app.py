import tkinter as tk
from ahpy import ahpy
import matplotlib.pyplot as plt

if __name__ == "__main__":
    alternative_entries_list = []
    criteria_entries = {}
    alternative_values = {}
    criteria_values = {}
    entry_row = 3 

    root=tk.Tk()
    root.geometry("600x400")

    criteria_var        = tk.StringVar()
    alternatives_var    = tk.StringVar()

    def submit():
        parameters = criteria_var.get().split(" ")
        alternatives = alternatives_var.get().split(" ")
        
        criteria_comparisons = {}
        comparisons = [] 

        print("Parameters".center(25, "-"))
        for (criterion1, criterion2), entry in criteria_entries.items():
            print(str((criterion1, criterion2)) + ":\t"+ entry.get())
            criteria_comparisons[(criterion1, criterion2)] = float(eval(entry.get()))

        print("Parameter Comparisons".center(25, "-"))

        for idx, param_comp in enumerate(alternative_entries_list):
            print(parameters[idx].center(10, "#"))
            parameter_comparison = {}
            for (criterion1, criterion2), entry in param_comp.items():
                print(str((criterion1, criterion2)) + ":\t"+ entry.get())
                parameter_comparison[(criterion1, criterion2)] = float(eval(entry.get()))
            comparisons.append(parameter_comparison)


        print("parameters")
        print(parameters)
        print("criteria_comparisons Dict")
        print(criteria_comparisons)
        print("alternatives")
        print(comparisons)
        

        criterias = []
        try:
            for i in range(len(parameters)):
                print("Checking")
                print(parameters[i])
                print( comparisons[i])
                parameter_criteria = ahpy.Compare(parameters[i], comparisons[i], precision=3, random_index='saaty')
                criterias.append(parameter_criteria)
        except:
            print("error!")
            return

        criteria = ahpy.Compare('Criteria', criteria_comparisons, precision=3, random_index='saaty')
        criteria.add_children(criterias)

        result = criteria.target_weights
        print(result)

        x = list(result.keys())
        y = list(result.values())

        plt.bar(x, y, color='maroon', width=0.4)
        plt.xlabel("Alternatives")
        plt.ylabel("Results")
        plt.title("Analytic Hierarchy Process")
        plt.show()
        report = criteria.report(show=True)
        print(report)    
        criteria_var.set("")
        alternatives_var.set("")

    def generate_alt_entries():
        global entry_row 
        alternatives = alternatives_var.get().strip().split(" ")
        parameters = criteria_var.get().strip().split(" ")

        for parameter in parameters:
            label = tk.Label(root, text = 'Parameter: ' + str(parameter), font = ('calibre', 10, 'bold'))
            label.grid(row=entry_row,column=0)
            entry_row += 1
            parameter_comparison = {}

            for i in range(0, len(alternatives)):
                for j in range(i+1, len(alternatives)):
                    key = (alternatives[i], alternatives[j],)
                    print(key)
                    entry =  tk.Entry(root, bd=5)
                    label = tk.Label(root, text = 'Value for ' + str(key), font = ('calibre',10,'bold'))
                    parameter_comparison[key] = entry

                    label.grid(row=entry_row,column=0)
                    entry.grid(row =entry_row ,column= 1)
                    entry_row +=1
            
            alternative_entries_list.append(parameter_comparison)

        sub_btn = tk.Button(root,text = 'Submit', command = submit)
        sub_btn.grid(row=entry_row,column=0)


    def generate_crit_entries():
        global entry_row 
        criteria = criteria_var.get().strip().split(" ")
        for i in range(0, len(criteria)):
            for j in range(i+1, len(criteria)):
                key = (criteria[i], criteria[j],)
                print(key)
                entry =  tk.Entry(root, bd=5)
                label = tk.Label(root, text = 'Value for ' + str(key), font = ('calibre',10,'bold'))
                criteria_entries[key] = entry

                label.grid(row=entry_row,column=0)
                entry.grid(row =entry_row ,column= 1)
                
                entry_row +=1
        
        generate_alt_entries_btn=tk.Button(root,text = 'Add Alternative Values', command = generate_alt_entries)
        generate_alt_entries_btn.grid(row=entry_row,column=0)
        entry_row +=1


    name_label = tk.Label(root, text = 'Criteria', font=('calibre',10, 'bold'))
    name_entry = tk.Entry(root,textvariable = criteria_var, font=('calibre',10,'normal'))
    generate_crit_entries_btn=tk.Button(root,text = 'Add Criteria Values', command = generate_crit_entries)
    
    passw_label = tk.Label(root, text = 'Alternatives', font = ('calibre',10,'bold'))
    passw_entry = tk.Entry(root, textvariable = alternatives_var, font = ('calibre',10,'normal'))


    name_label.grid(row=0,column=0)
    name_entry.grid(row=0,column=1)
    passw_label.grid(row=1,column=0)
    passw_entry.grid(row=1,column=1)
    generate_crit_entries_btn.grid(row=2,column=0)

    root.mainloop()
