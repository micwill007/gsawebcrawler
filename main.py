from modules import *
from tkinter import *

################################

#   GSA Advantage Web Crawler

  #################################

def callback():
  a = e.get()

  if (var.get()):
    search.search(a)

  if (var2.get()):
    scrape.scrape(a)

# init tkinter
master = Tk()

# text areas
S = Label(master, height = 6, background = "lightblue", text='grab an https proxy from the site below. Make sure to filter by United States and choose an anonymous, not elite proxy.')
S.pack()

# text areas
T = Label(master, height = 6, background = "grey", text='https://free-proxy-list.net/')
T.pack()

# text areas
X = Label(master, height = 6, background = "orange", text='Format is: "ipaddress:port" EX: 216.56.58.2:8000')
X.pack()

e = Entry(master)
e.insert(0, "Please enter a proxy")
e.pack()

# buttons
var = IntVar()
c = Checkbutton(master, text="search", variable=var)
c.pack(side=LEFT)

var2 = IntVar()
c2 = Checkbutton(master, text="scrape", variable=var2)
c2.pack(side=LEFT)

e.focus_set()

b = Button(master, text="Run", width=10, command=callback)
b.pack()

mainloop()