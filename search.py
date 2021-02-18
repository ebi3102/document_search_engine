from tkinter import *
from tkinter import ttk
import json
import processor as pc

window = Tk()
window.title("Welcome to Document Search Engine")
window.geometry('1000x1000')
scrollbar = Scrollbar(window)

Query = StringVar()


def search():
    data = open('inverted-index.json')
    data = data.read()
    inverted_index = json.loads(data)

    data2 = open('terms-idf.json')
    data2 = data2.read()
    idf_dic = json.loads(data2)

    query = Query.get()

    res = pc.search_engine(query, inverted_index, idf_dic)

    row = 6
    if len(res) != 0:
        for doc in res:
            text = "Document Name: " + doc[0]
            result_doc = Label(window, text=text, font=("bold", 12)).grid(row=row, column=2)
            row += 1
            text2 = "Cosine similarity between query and document is " + str(doc[1])
            result_cos = Label(window, text=text2, font=12).grid(row=row, column=2)
            row += 4
    else:
        text = "Your query there isn't in our documents "
        result_doc = Label(window, text=text, font=("bold", 12)).grid(row=row, column=2)

    text = "End Search"
    resulted = Label(window, text=text, font=("bold", 20)).grid(row=row+1, column=2)


a = Label(window, text="Please Enter your query", font=("bold", 20)).grid(row=2, column=2)
b = Label(window, text=" ").grid(row=1, column=1)
c = Label(window, text=" ").grid(row=3, column=3)
a1 = Entry(window, textvar=Query).grid(row=4, column=5)


btn = ttk.Button(window, text="Search", command=search).grid(row=4, column=6)
window.mainloop()
