import random
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import figure
from tkinter import *
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler




# NOTE: Python version >=3.3 is required, due to "yield from" feature.

# Get user input to determine range of integers (1 to N) and desired
# sorting method (algorithm).
# N = int(input("Enter number of integers: "))

# method_msg = "Enter sorting method:\n(b)ubble\n(i)nsertion\n(m)erge \
#     \n(q)uick\n(s)election\n"
# method = input(method_msg)

def sort(method, N):
	global A
	def swap(A, i, j):
		"""Helper function to swap elements i and j of list A."""

		if i != j:
			A[i], A[j] = A[j], A[i]

	def bubblesort(A):
		"""In-place bubble sort."""

		if len(A) == 1:
			return

		swapped = True
		for i in range(len(A) - 1):
			if not swapped:
				break
			swapped = False
			for j in range(len(A) - 1 - i):
				if A[j] > A[j + 1]:
					swap(A, j, j + 1)
					swapped = True
				yield A

	def insertionsort(A):
		"""In-place insertion sort."""

		for i in range(1, len(A)):
			j = i
			while j > 0 and A[j] < A[j - 1]:
				swap(A, j, j - 1)
				j -= 1
				yield A

	def mergesort(A, start, end):
		"""Merge sort."""

		if end <= start:
			return

		mid = start + ((end - start + 1) // 2) - 1
		yield from mergesort(A, start, mid)
		yield from mergesort(A, mid + 1, end)
		yield from merge(A, start, mid, end)
		yield A

	def merge(A, start, mid, end):
		"""Helper function for merge sort."""
		
		merged = []
		leftIdx = start
		rightIdx = mid + 1

		while leftIdx <= mid and rightIdx <= end:
			if A[leftIdx] < A[rightIdx]:
				merged.append(A[leftIdx])
				leftIdx += 1
			else:
				merged.append(A[rightIdx])
				rightIdx += 1

		while leftIdx <= mid:
			merged.append(A[leftIdx])
			leftIdx += 1

		while rightIdx <= end:
			merged.append(A[rightIdx])
			rightIdx += 1

		for i, sorted_val in enumerate(merged):
			A[start + i] = sorted_val
			yield A

	def quicksort(A, start, end):
		"""In-place quicksort."""

		if start >= end:
			return

		pivot = A[end]
		pivotIdx = start

		for i in range(start, end):
			if A[i] < pivot:
				swap(A, i, pivotIdx)
				pivotIdx += 1
			yield A
		swap(A, end, pivotIdx)
		yield A

		yield from quicksort(A, start, pivotIdx - 1)
		yield from quicksort(A, pivotIdx + 1, end)

	def selectionsort(A):
		"""In-place selection sort."""
		if len(A) == 1:
			return

		for i in range(len(A)):
			# Find minimum unsorted value.
			minVal = A[i]
			minIdx = i
			for j in range(i, len(A)):
				if A[j] < minVal:
					minVal = A[j]
					minIdx = j
				yield A
			swap(A, i, minIdx)
			yield A
	
	# Get appropriate generator to supply to matplotlib FuncAnimation method.
	if method == "b":
		title = "Bubble sort"
		generator = bubblesort(A)
	elif method == "i":
		title = "Insertion sort"
		generator = insertionsort(A)
	elif method == "m":
		title = "Merge sort"
		generator = mergesort(A, 0, N - 1)
	elif method == "q":
		title = "Quicksort"
		generator = quicksort(A, 0, N - 1)
	else:
		title = "Selection sort"
		generator = selectionsort(A)

	return generator,title


def resetArray( N):
	# Build and randomly shuffle list of integers.
	global A
	A = [x + 1 for x in range(N)]
	random.seed(time.time())
	random.shuffle(A)

def createOrResetCanvas(fig):
	global canvas
	if (canvas == None):
		#Create a new canvas if it doesn't exist
		canvas = FigureCanvasTkAgg(fig, master = window)

		canvas.mpl_connect("key_press_event", lambda event: print(f"you pressed {event.key}"))
		canvas.mpl_connect("key_press_event", key_press_handler)
		toolbar = NavigationToolbar2Tk(canvas,window, pack_toolbar=False)
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
	# fig, ax = plt.subplots()
	ax = fig.add_subplot()
	ax.set_title(title)
	# plt.title(title)
	

	# Initialize a bar plot. Note that matplotlib.pyplot.bar() returns a
	# list of rectangles (with each bar in the bar plot corresponding
	# to one rectangle), which we store in bar_rects.
	
	bar_rects = ax.bar(range(len(A)), A, align="center") #plt.bar(x,height, width=0.8, bottom=None, *, align="center", data=None, **kwargs)

	# Set axis limits. Set y axis upper limit high enough that the tops of
	# the bars won't overlap with the text label.
	# ax.set_xlim(0, N)
	ax.set_ylim(0, (N+4))

	# Place a text label in the upper-left corner of the plot to display
	# number of operations performed by the sorting algorithm (each "yield"
	# is treated as 1 operation).
	text = ax.text(0.02, 0.95, "", transform=ax.transAxes)
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
	def update_fig(A, rects, iteration):
		for rect, val in zip(rects, A):
			rect.set_height(val)
		# global iteration
		iteration[0] += 1
		text.set_text("# of operations: {}".format(iteration))

	global anim
	anim = animation.FuncAnimation(fig, func=update_fig,
		fargs=( bar_rects,iteration), frames=generator, interval=1,
		repeat=False)

def visualize(method, N):
	global fig
	global canvas
	#reseting the array
	resetArray( N)
	
	#getting the correct sort function
	generator,title = sort(method, N)


	#creating the figure and bar graph that we will later animate
	fig,ax,bar_rects, text = createPlot(fig,title)


	#creating the canvas and putting the graph on it:
	createOrResetCanvas(fig)

	#animating the graph
	graphAnimation(text, bar_rects, fig, generator)


def onClosing():
	'''Event handler to close the window gracefully'''
	global canvas
	# canvas.
	# window.quit()
	window.destroy()


#main program:
window = Tk()
window.title("Sorting Visualizer")
window.geometry("600x600")
window.protocol("WM_DELETE_WINDOW", onClosing)
canvas = None

method = 'b'
N = 30
A = []
fig = None
button = Button(master=window, text="BubbleSort", command= lambda: visualize('b',N))
button.pack(side=BOTTOM)

# visualize('b',N)

window.mainloop()