import random
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import figure
from tkinter import *
from tkinter.ttk import *
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
import os
import handlFiles



# NOTE: Python version >=3.3 is required, due to "yield from" feature.

# Get user input to determine range of integers (1 to N) and desired
# sorting method (algorithm).
# N = int(input("Enter number of integers: "))

# method_msg = "Enter sorting method:\n(b)ubble\n(i)nsertion\n(m)erge \
#     \n(q)uick\n(s)election\n"
# method = input(method_msg)

def sort(method, size):
	global array
	def swap(array, i, j):
		"""Helper function to swap elements i and j of list A."""

		if i != j:
			array[i], array[j] = array[j], array[i]

	def bubblesort(array):
		"""In-place bubble sort."""

		if len(array) == 1:
			return

		swapped = True
		for i in range(len(array) - 1):
			if not swapped:
				break
			swapped = False
			for j in range(len(array) - 1 - i):
				if array[j] > array[j + 1]:
					swap(array, j, j + 1)
					swapped = True
					yield array

	def insertionsort(array):
		"""In-place insertion sort."""

		for i in range(1, len(array)):
			j = i
			while j > 0 and array[j] < array[j - 1]:
				swap(array, j, j - 1)
				j -= 1
				yield array

	def mergesort(array, start, end):
		"""Merge sort."""

		if end <= start:
			return

		mid = start + ((end - start + 1) // 2) - 1
		yield from mergesort(array, start, mid)
		yield from mergesort(array, mid + 1, end)
		yield from merge(array, start, mid, end)
		# yield A

	def merge(array, start, mid, end):
		"""Helper function for merge sort."""
		
		merged = []
		leftIdx = start
		rightIdx = mid + 1

		while leftIdx <= mid and rightIdx <= end:
			if array[leftIdx] < array[rightIdx]:
				merged.append(array[leftIdx])
				leftIdx += 1
			else:
				merged.append(array[rightIdx])
				rightIdx += 1

		while leftIdx <= mid:
			merged.append(array[leftIdx])
			leftIdx += 1

		while rightIdx <= end:
			merged.append(array[rightIdx])
			rightIdx += 1

		for i, sorted_val in enumerate(merged):
			array[start + i] = sorted_val
			yield array

	def quicksort(array, start, end):
		"""In-place quicksort."""

		if start >= end:
			return

		pivot = array[end]
		pivotIdx = start

		for i in range(start, end):
			if array[i] < pivot:
				swap(array, i, pivotIdx)
				pivotIdx += 1
				yield array
		swap(array, end, pivotIdx)
		yield array

		yield from quicksort(array, start, pivotIdx - 1)
		yield from quicksort(array, pivotIdx + 1, end)

	def selectionsort(array):
		"""In-place selection sort."""
		if len(array) == 1:
			return

		for i in range(len(array)):
			# Find minimum unsorted value.
			minVal = array[i]
			minIdx = i
			for j in range(i, len(array)):
				if array[j] < minVal:
					minVal = array[j]
					minIdx = j
				# yield A
			swap(array, i, minIdx)
			yield array
		
			
	# Get appropriate generator to supply to matplotlib FuncAnimation method.
	if method == "b":
		title = "Bubble sort"
		generator = bubblesort(array)
	elif method == "i":
		title = "Insertion sort"
		generator = insertionsort(array)
	elif method == "m":
		title = "Merge sort"
		generator = mergesort(array, 0, size - 1)
	elif method == "q":
		title = "Quicksort"
		generator = quicksort(array, 0, size - 1)
	else:
		title = "Selection sort"
		generator = selectionsort(array)

	return generator,title


# def resetArray( N):
# 	# Build and randomly shuffle list of integers.
# 	global A
# 	A = [x + 1 for x in range(N)]
# 	random.seed(time.time())
# 	random.shuffle(A)

def createOrResetCanvas(fig):
	global canvas
	if (canvas == None):
		matplotlibFrame = Frame(window)
		matplotlibFrame.grid()
		#Create a new canvas if it doesn't exist
		canvas = FigureCanvasTkAgg(fig, master = matplotlibFrame)

		canvas.mpl_connect("key_press_event", lambda event: print(f"you pressed {event.key}"))
		canvas.mpl_connect("key_press_event", key_press_handler)
		toolbar = NavigationToolbar2Tk(canvas,matplotlibFrame, pack_toolbar=False)
		toolbar.update()
		toolbar.pack(side=BOTTOM, fill=X)

		canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

	canvas.draw() #draw or redraw the canvas. Not using pack_forget as we can reuse the same canvas through this, and therefore, we don't need to worry about memory leaks or toolbars stacking over each other.

def createPlot(fig,title):

	if (fig != None):
		#if fig exists, it means this function is called again and we need to clear the figure, so it can be re-initialized
		fig.clear()

	if (fig == None):
		# Initialize figure and axis if they don't exist.
		fig = figure.Figure() #using plt.subplots hijacks the terminal if we close the window in the middle of sorting

	ax = fig.add_subplot()
	ax.set_title(title)	

	# Initialize a bar plot. Note that matplotlib.pyplot.bar() returns a
	# list of rectangles (with each bar in the bar plot corresponding
	# to one rectangle), which we store in bar_rects.
	
	bar_rects = ax.bar(range(len(array)), array, align="center") #plt.bar(x,height, width=0.8, bottom=None, *, align="center", data=None, **kwargs)
	for bar in bar_rects:
		bar.set_animated(True)
	# Set axis limits. Set y axis upper limit high enough that the tops of
	# the bars won't overlap with the text label.
	# ax.set_xlim(-1, N )
	ax.set_ylim(0, (max(array)*1.1))

	# Place a text label in the upper-left corner of the plot to display
	# number of operations performed by the sorting algorithm (each "yield"
	# is treated as 1 operation).
	text = ax.text(0.02, 0.95, "", transform=ax.transAxes)
	text.set_animated(True)
	return (fig, ax, bar_rects, text)

def graphAnimation(text, bar_rects,fig, generator):
	# Define function update_fig() for use with matplotlib.pyplot.FuncAnimation().
	# To track the number of operations, i.e., iterations through which the
	# animation has gone, define a variable "iteration". This variable will
	# be passed to update_fig() to update the text label, and will also be
	# incremented in update_fig(). For this increment to be reflected outside
	# the function, we make "iteration" a list of 1 element, since lists (and
	# other mutable objects) are passed by reference (but an integer would be
	# passed by value).
	# NOTE: Alternatively, iteration could be re-declared within update_fig()
	# with the "global" keyword (or "nonlocal" keyword).
	iteration = [0]

	def update_fig(array, rects, iteration):
		changes =[]
		for rect, val in zip(rects, array):
			if (rect.get_height()!= val):
				rect.set_height(val)
				changes.append(rect)
		# global iteration
		iteration[0] += 1
		text.set_text("# of memory swaps: {}".format(iteration[0]))
		return rects


	global anim
	anim = animation.FuncAnimation(fig, func=update_fig,
		fargs=( bar_rects,iteration), frames=generator, interval=0,
		repeat=False, blit=True)

def visualize(method, size):
	global fig
	global canvas

	# #reseting the array
	# resetArray( N)
	
	#getting the correct sort function
	generator,title = sort(method, size)


	#creating the figure and bar graph that we will later animate
	fig,ax,bar_rects, text = createPlot(fig,title)


	#creating the canvas and putting the graph on it:
	createOrResetCanvas(fig)

	#animating the graph
	graphAnimation(text, bar_rects, fig, generator)
	
def runProgram(fileSelected, sortingMethod):
	method = sortingMethod.get()[0].lower()
	fileName = fileSelected.get()

	global array
	array = handlFiles.readFile(fileName)
	size = len(array)
	if (size <= 0):
		print("The file you selected was empty, or was not read properly")
		return
	visualize(method,size)


#main program:
window = Tk()
window.title("Sorting Visualizer")
window.geometry("600x600")
canvas = None
# method = 'b'
array = []
fig = None
#sorting dropdown
options = ["Bubble Sort","Insertion Sort", "Merge Sort", "Quick Sort", "Selection Sort"] 
sortingMethod = StringVar()
sortingMethod.set(options[0])
dropDown = OptionMenu(window, sortingMethod, options[0], *options)
# dropDown.pack()
dropDown.grid()

#files drop down
filenames  = os.listdir("files")
fileSelected = StringVar()
fileSelected.set(filenames[0])
fileDropDown = OptionMenu(window, fileSelected, filenames[0], *filenames)
# fileDropDown.pack()
fileDropDown.grid()


runButton = Button(master=window, text="Run", command= lambda: runProgram(fileSelected, sortingMethod))
# runButton.pack(side=BOTTOM)
runButton.grid(ipadx=30, ipady = 3)

#Creating a button to reset the file:
newDataButton = Button(master = window, text="Generate New Data", command= lambda: handlFiles.generateNewFile(fileSelected.get()))
# newDataButton.pack()
newDataButton.grid(ipadx= 12.5, ipady = 3)

window.mainloop()