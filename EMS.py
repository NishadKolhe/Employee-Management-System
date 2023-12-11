#Importing required modules required for the project.
from tkinter import *
from tkinter.messagebox import *
from tkinter.scrolledtext import *
from pymongo import *
import requests
import matplotlib.pyplot as plt

def addbtn():                       # Defining the function to handle the ADD button click      
	root.withdraw()             # Hide the main window 
	aw.deiconify()              # show the "Add" window
def viewbtn():                      # Defining the function to handle the VIEW button click
	root.withdraw()                     # Hide the main window 
	vw.deiconify()                    # show the "View" window
	vw_st_data.delete(1.0,END)        # Clear the scrolled text widget
	con = None
	try:                                                         # Connect to MongoDB and retrieve employee data
		con = MongoClient("mongodb://localhost:27017")
		db = con["IPEMS2023"]
		coll = db["emp"]
		data = coll.find().sort("_id",1)
		info = ""
		for d in data:                                                                                                          # Display employee data in the scrolled text widget
			info = info + "id: " + str(d["_id"]) + "  name: " + str(d["name"]) + "  salary: " + str(d["salary"]) + "\n"
		vw_st_data.insert(INSERT,info)
	except Exception as e:
		showerror("issue",e)
	finally:
		if con is not None:
			con.close()
def updatebtn():                    # Defining the function to handle the UPDATE button click
	root.withdraw()              # Hide the main window
	uw.deiconify()               # show the "Update" window
	
def deletebtn():                    # Defining the function to handle the DELETE button click
	root.withdraw()              # Hide the main window
	dw.deiconify()               # show the "Delete" window
def chartbtn():                     # Defining the function to handle the CHART button click
	name =[]
	salary = []
	con = None
	try:                                                         # Retrieve top 5 highest salaried employees and plot a chart
		con = MongoClient("mongodb://localhost:27017")
		db = con["IPEMS2023"]
		coll = db["emp"]
		data = coll.find().sort("salary",-1).limit(5)
		for d in data:
			name.append(d["name"])
			salary.append(d["salary"])
		plt.plot(name,salary,linewidth=4,marker="o",markersize=10,markerfacecolor="black")
		plt.title("Top 5 Highest salaried employees.")
		plt.grid()
		plt.xlabel("Names")
		plt.ylabel("Salaries")

		plt.show()
	except Exception as e:
		showerror("issue",e)
	finally:
		if con is not None:
			con.close()
			

def backbtnA():                       # Defining the function to handle the BACK button click in the ADD window
	aw.withdraw()                 # Hide the "Add" window
	root.deiconify()              # show the main window


def backbtnV():                       # Defining the function to handle the BACK button click in the VIEW window
	vw.withdraw()                 # Hide the "View" window
	root.deiconify()              # show the main window
 

def backbtnU():                       # Defining the function to handle the BACK button click in the UPDATE window
	uw.withdraw()                 # Hide the "Update" window
	root.deiconify()              # show the main window

def backbtnD():                       # Defining the function to handle the BACK button click in the DELETE window
	dw.withdraw()                 # Hide the "Delete" window
	root.deiconify()              # show the main window
 

def savebtnA():                       # Defining the function to handle the SAVE button click in the ADD window
	id = aw_ent_id.get()                                         # Get user input before saving to MongoDB
	name = aw_ent_name.get()                                     
	salary = aw_ent_salary.get()                                
	if len(id) == 0:                                             # Validating for Null input from user
		showerror("Error","Id cannot be empty.")
		aw_ent_id.focus()                                    
	else:
		try:                                                                   
			if id.isdigit():                             # Validating the datatype of input for id
				if int(id)>0:
					if len(name) >= 2:                                    # Validating length of the input for name 
						if name.replace(' ','').isalpha():            # Validating the datatype of input for name
							if len(salary) == 0:                  # Validating for Null input from user
								showerror("Error","Salary cannot be empty.")
								aw_ent_salary.focus()                          # Allowing user to resume without additional clicks
							else:
								if int(salary)>=8000:                          # Validating minimum amount for salary input
									con = None
									try:
										con = MongoClient("mongodb://localhost:27017")   # Establishing a connection to a MongoDB database using the MongoClient class
										db = con["IPEMS2023"]
										coll = db["emp"]
										id = int(aw_ent_id.get())
										name = aw_ent_name.get()
										salary = float(aw_ent_salary.get())
										count = coll.count_documents({"_id":id})
										if count == 1:                                              # Checking for repeated entries
											showerror(id,"Already exists.")
										else:
											info = {"_id":id,"name":name,"salary":salary}
											coll.insert_one(info)
											showinfo("Success","Record Created.")
									except Exception as e:
										print("Issue",e)
									finally:
										if con is not None:
											con.close()                                        # Closing the MongoDB connection 
										aw_ent_id.delete(0,END)												
										aw_ent_name.delete(0,END)
										aw_ent_salary.delete(0,END)
										aw_ent_id.focus()	
								else:
									showerror("Error","Salary should be minimum of Rs 8000.")
									aw_ent_salary.delete(0,END)
									aw_ent_salary.focus()
						else:
							showerror("Error","Name should contain only alphabets,minimum 2.")
							aw_ent_name.delete(0,END)
							aw_ent_name.focus()				
					else:
						showerror("Error","Name should contain only alphabets,minimum 2.")
						aw_ent_name.delete(0,END)
						aw_ent_name.focus()
				else:	
					showerror("Error","Id should have only positive integers(without spaces).")
					aw_ent_id.delete(0,END)
					aw_ent_id.focus()
			else:
				showerror("Error","Id should have only positive integers(without spaces).")
				aw_ent_id.delete(0,END)
				aw_ent_id.focus()
		except Exception as e:
			showerror("Issue",e)
def savebtnU():                               # Defining the function to handle the SAVE button click in the UPDATE window
	id = uw_ent_id.get()
	name = uw_ent_name.get()
	salary = uw_ent_salary.get()
	if len(id) == 0:
		showerror("Error","Id cannot be empty.")
		uw_ent_id.focus()
	else:
		try:
			if id.isdigit():
				if int(id)>0:
					if len(name) >= 2:
						if name.replace(' ','').isalpha():
							if len(salary) == 0:
								showerror("Error","Salary cannot be empty.")
								aw_ent_salary.focus()
							else:
								if int(salary)>=8000:
									con = None
									try:
										con = MongoClient("mongodb://localhost:27017")
										db = con["IPEMS2023"]
										coll = db["emp"] 
										id = int(uw_ent_id.get())
										name = uw_ent_name.get()
										salary = float(uw_ent_salary.get())
										count = coll.count_documents({"_id":id})
										if count == 1:
											coll.delete_one({"_id":id})
											info = {"_id":id,"name":name,"salary":salary}
											coll.insert_one(info)
											showinfo("Success","Record Updated.")
										else:
											showerror(id,"Does not exists. ")
									except Exception as e:
										showerror("issue",e)
									finally:
										if con is not None:
											con.close()
										uw_ent_id.delete(0,END)
										uw_ent_name.delete(0,END)
										uw_ent_salary.delete(0,END)
										uw_ent_id.focus()
	
								else:
									showerror("Error","Salary has to be a minimum of Rs.8000")
									uw_ent_salary.delete(0,END)
									uw_ent_salary.focus()
						else:
							showerror("Error","Name should contain only alphabets,minimum 2.")
							uw_ent_name.delete(0,END)
							uw_ent_name.focus()
					else:
						showerror("Error","Name should contain only alphabets,minimum 2.")
						uw_ent_name.delete(0,END)
						uw_ent_name.focus()
				else:
					showerror("Error","Id should have only positive integers(without spaces).")
					uw_ent_id.delete(0,END)
					uw_ent_id.focus()
							
			else:
				showerror("Error","Id should have only positive integers(without spaces).")
				uw_ent_id.delete(0,END)
				uw_ent_id.focus()
		except Exception as e:
			showerror("Issue",e)
	

	
def deletebtnD():                   # Defining the function to handle the DELETE button click in the DELETE window
	id = dw_ent_id.get()
	if len(id) == 0:
		showerror("Error","Id cannot be empty.")
		dw_ent_id.focus()
	else:
		try:
			if id.isdigit():
				if int(id)>0:
					con = None
					try:
						con = MongoClient("mongodb://localhost:27017")
						db = con["IPEMS2023"]
						coll = db["emp"] 
						id = int(dw_ent_id.get())
						count = coll.count_documents({"_id":id})
						if count == 1:
							coll.delete_one({"_id":id})
							showinfo("Success","Record Deleted.")
						else:
							showerror(id,"Does not exists. ")
					except Exception as e:
						showerror("issue",e)
					finally:
						if con is not None:
							con.close()
						dw_ent_id.delete(0,END)
						dw_ent_id.focus()
				else:
					showerror("Error","Id should have only positive integers(without spaces).")
					dw_ent_id.delete(0,END)
					dw_ent_id.focus()
			else:
				showerror("Error","Id should have only positive integers(without spaces).")
				dw_ent_id.delete(0,END)
				dw_ent_id.focus()
		except Exception as e:
			showerror("Issue",e)


root = Tk()                         # Creating the main window.
root.title("E.M.S")
root.geometry("500x600+50+50")
f = ("Simsun",30,"bold")
v = ("Simsun",15,"bold","italic")
root.configure(bg = "White")

btn_add = Button(root,text = "Add",font = f,width = 8,bg = "#75b5c6",fg = "White",command = addbtn)        # Creating the ADD button in main window.
btn_add.pack(pady=10)
btn_view = Button(root,text = "View",font = f,width = 8,bg = "#75b5c6",fg = "White",command = viewbtn)     # Creating the VIEW button in main window.
btn_view.pack(pady=10)
btn_update = Button(root,text = "Update",font = f,width = 8,bg = "#75b5c6",fg = "White",command = updatebtn)      # Creating the UPDATE button in main window.
btn_update.pack(pady=10)
btn_delete = Button(root,text = "Delete",font = f,width = 8,bg = "#75b5c6",fg = "White",command = deletebtn)      # Creating the DELETE button in main window.
btn_delete.pack(pady=10)
btn_charts = Button(root,text = "Charts",font = f,width = 8,bg = "#75b5c6",fg = "White",command = chartbtn)       # Creating the CHART button in main window.
btn_charts.pack(pady=10) 
lab_city = Label(root,text = "City -",font = v)                             # Creating a label for displaying 'City'.
lab_city.place(x = 5,y = 500) 
lab_loc = Label(root,text = "Location-",font = v)                           # Creating a label for displaying 'Location'.
lab_loc.place(x = 5,y = 530)
lab_temp = Label(root,text = "Temp:",font = v)                              # Creating a label for displaying temperature.
lab_temp.place(x = 370,y = 500)
try:                                                                        # Getting the information about the city and location from IP Address
	wa = "https://ipinfo.io/"
	res = requests.get(wa)                                              # Sending request to ipinfo.io
	print(res)                                                          # Printing the response received from external site.
	data = res.json()                                                   # extracting dataset from response
	city = data["city"]                                                 # extracting data related to city from dataset
	loc = data["loc"]                                                   # extracting data related to location from dataset
	lab_city_info = Label(root,text = city,font = v,fg = "#da757b")     # Creating a label for displaying the city.
	lab_city_info.place(x= 77,y = 500)
	lab_loc_info = Label(root,text = loc,font = v,fg = "#da757b")       # Creating a label for displaying location.
	lab_loc_info.place(x = 108, y = 530)
	a1 = "https://api.openweathermap.org/data/2.5/weather?"             # Modifying the web address as per city.
	a2 = "q=" + city
	a3 = "&appid=" + "c6e315d09197cec231495138183954bd"
	a4 = "&units=" + "metric"
	wa = a1+a2+a3+a4
	res = requests.get(wa)                                              # Sending request to openweathermap.org
	print(res)                                                          # Printing the response received from external website
	data = res.json()                                                   # Extracting dataset from response
	temp = data["main"]["temp"]                                         # extracting data related to temperature from from dataset
	lab_temp_info = Label(root,text = temp,font = v,fg = "#da757b")     # Creating a label for displaying temperature.
	lab_temp_info.place(x= 430,y = 500)
except Exception as e:
	print("Issue ",e)


# Defining functions for handling button events in the main window via keyboard
def f1(event):
	addbtn()
btn_add.bind('<Return>',f1)

def f2(event):
	viewbtn()
btn_view.bind('<Return>',f2)

def f3(event):
	updatebtn()
btn_update.bind('<Return>',f3)

def f4(event):
	deletebtn()
btn_delete.bind('<Return>',f4)

def f5(event):
	chartbtn()
btn_charts.bind('<Return>',f5)



# Create a separate window for Add operations.

aw = Toplevel(root)
aw.title("Add Emp")
aw.geometry("500x600+50+50")
aw.configure(bg = "White")

aw_lab_id = Label(aw,text = "Enter id. ",font = f,bg = "White",fg = "#3a424c")
aw_lab_id.pack(pady=10)
aw_ent_id = Entry(aw,font = f,bd = 2)
aw_ent_id.pack(pady=10)
aw_lab_name = Label(aw,text = "Enter name. ",font = f,bg = "White",fg = "#3a424c")
aw_lab_name.pack(pady=10)
aw_ent_name = Entry(aw,font = f,bd = 2)
aw_ent_name.pack(pady=10)
aw_lab_salary = Label(aw,text = "Enter salary. ",font = f,bg = "White",fg = "#3a424c")
aw_lab_salary.pack(pady=10)
aw_ent_salary = Entry(aw,font = f,bd = 2)
aw_ent_salary.pack(pady=10)
aw_btn_save = Button(aw,text = "Save",font = f,width = 8,bg = "#75b5c6",fg = "White",command = savebtnA)       # Creating save button on Add window
aw_btn_save.pack(pady=10)
aw_btn_back = Button(aw,text = "Back",font = f,width = 8,bg = "#75b5c6",fg = "White",command = backbtnA)       # Creating back button on Add window
aw_btn_back.pack(pady=10)

def f6(event):                            # Defining function to handle the save event in Add window via keyboard
	savebtnA()
aw_btn_save.bind('<Return>',f6)

def f7(event):                            # Defining function to handle the back event in add window via keyboard
	backbtnA()
aw_btn_back.bind('<Return>',f7)


aw.withdraw()


# Create a separate window for View operations.

vw = Toplevel(root)
vw.title("View Emp")
vw.geometry("600x600+50+50")
vw.configure(bg = "White")

vw_st_data = ScrolledText(vw,width = 50,height = 10,font = v)
vw_st_data.pack(pady = 10)
vw_btn_back = Button(vw,text = "Back",font = f,width = 8,bg = "#75b5c6",fg = "White",command = backbtnV)      # Creating back button on View window
vw_btn_back.pack(pady = 10)
vw.withdraw()


# Create a separate window for Update operations.

uw = Toplevel(root)
uw.title("Update Emp")
uw.geometry("500x600+50+50")
uw.configure(bg = "White")

uw_lab_id = Label(uw,text = "Enter id.",font = f,bg = "White",fg = "#3a424c")
uw_lab_id.pack(pady = 10)
uw_ent_id = Entry(uw,font = f,bd = 2)
uw_ent_id.pack(pady = 10)
uw_lab_name = Label(uw,text = "Enter name.",font = f,bg = "White",fg = "#3a424c")
uw_lab_name.pack(pady = 10)
uw_ent_name = Entry(uw,font = f,bd = 2)
uw_ent_name.pack(pady = 10)
uw_lab_salary = Label(uw,text = "Enter salary.",font = f,bg = "White",fg = "#3a424c")
uw_lab_salary.pack(pady = 10)
uw_ent_salary = Entry(uw,font = f,bd = 2)
uw_ent_salary.pack(pady = 10)
uw_btn_save = Button(uw,text = "Save",font = f,width = 8,bg = "#75b5c6",fg = "White",command = savebtnU)      # Creating save button on Update window
uw_btn_save.pack(pady = 10)
uw_btn_back = Button(uw,text = "Back",font = f,width = 8,bg = "#75b5c6",fg = "White",command = backbtnU)       # Creating back button on Update window
uw_btn_back.pack(pady = 10)

def f8(event):                             # Defining function to handle the save event in update window via keyboard
	savebtnU()
uw_btn_save.bind('<Return>',f8)

def f9(event):                              # Defining function to handle the back event in update window via keyboard
	backbtnU()
uw_btn_back.bind('<Return>',f9)

uw.withdraw()


# Create a separate window for Delete operations.

dw = Toplevel(root)
dw.title("Delete Emp")
dw.geometry("500x600+50+50")
dw.configure(bg = "White")

dw_lab_id = Label(dw,text = "Enter id.",font = f,bg = "White",fg = "#3a424c")
dw_lab_id.pack(pady = 10)
dw_ent_id = Entry(dw,font = f,bd = 2)
dw_ent_id.pack(pady = 10)
dw_btn_delete = Button(dw,text = "Delete",font = f,width = 8,bg = "#75b5c6",fg = "White",command = deletebtnD)        # Creating delete button on Delete window
dw_btn_delete.pack(pady = 10)
dw_btn_back = Button(dw,text = "Back",font = f,width = 8,bg = "#75b5c6",fg = "White",command = backbtnD)              # Creating back button on Delete window
dw_btn_back.pack(pady = 10)

def f10(event):                    # Defining function to handle the delete event in delete window via keyboard
	deletebtnD()
dw_btn_delete.bind('<Return>',f10)

def f11(event):                     # Defining function to handle the back event in delete window via keyboard
	backbtnD()
dw_btn_back.bind('<Return>',f11)
dw.withdraw()


def f12():        # Defining function to handle the window close event and confirm whether the user wants to exit
	answer = askyesno(title='confirmation',message = "Do you want to exit?")    # Displaying a confirmation dialog with "Yes" and "No" options.
	if answer:                                                                 # # If the user chooses "Yes," close the main window
		root.destroy()

root.protocol("WM_DELETE_WINDOW",f12)
root.mainloop()