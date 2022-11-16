import random
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from tkinter import *
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler


window = Tk()
window.title("Sorting Visualizer")
window.geometry("800x600")
animating = False
canvas = None

# NOTE: Python version >=3.3 is required, due to "yield from" feature.

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

# Get user input to determine range of integers (1 to N) and desired
# sorting method (algorithm).
# N = int(input("Enter number of integers: "))
N = 30
# method_msg = "Enter sorting method:\n(b)ubble\n(i)nsertion\n(m)erge \
#     \n(q)uick\n(s)election\n"
# method = input(method_msg)
# method = 'b'

# Build and randomly shuffle list of integers.
A = [x + 1 for x in range(N)]
def arrayReset(A):
	random.seed(time.time())
	random.shuffle(A)
restart = False
iteration = 0
def visualize(N, method):
	global animating, restart
	animating = True
	if (not restart):
		restart = True
		arrayReset(A)
	else:
		arrayReset(A)
		anim.pause()
		plt.close()
		return
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


	# Initialize figure and axis.
	fig, ax = plt.subplots()
	
	# ax.set_title(title)
	plt.title(title)

	# Initialize a bar plot. Note that matplotlib.pyplot.bar() returns a
	# list of rectangles (with each bar in the bar plot corresponding
	# to one rectangle), which we store in bar_rects.
	bar_rects = plt.bar(range(len(A)), A, align="center")

	# Set axis limits. Set y axis upper limit high enough that the tops of
	# the bars won't overlap with the text label.
	# ax.set_xlim(0, N)
	# ax.set_ylim(0, (N+4))
	plt.ylim(0,(N+4))

	# Place a text label in the upper-left corner of the plot to display
	# number of operations performed by the sorting algorithm (each "yield"
	# is treated as 1 operation).
	text = plt.text(0.02, 0.95, "", transform=ax.transAxes)

	updateOrCreateCanvas(fig)


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

	def handleClose():
		anim.pause()
		plt.close(fig)
		global animating
		animating = False
		print("I was called")
		onClosing()


	def update_fig(A, rects):
		for rect, val in zip(rects, A):
			rect.set_height(val)
		global iteration
		iteration += 1
		text.set_text("# of operations: {}".format(iteration))
		global stop
		if (stop):
			handleClose()


	# global anim
	anim = animation.FuncAnimation(fig, func=update_fig,
		fargs=([bar_rects]), frames=generator, interval=1,
		repeat=False)
	print("I am done")


#adding tkinter:

def updateOrCreateCanvas(fig):
	global canvas
	if (canvas != None):
		print("\a")
		print("helloooooooooooooooooo")
		canvas.get_tk_widget().pack_forget()
		fig.clear()
		time.sleep(10)
	
	canvas = FigureCanvasTkAgg(fig, master = window)
	canvas.draw()

	toolbar = NavigationToolbar2Tk(canvas,window,  pack_toolbar=False)
	toolbar.update()

	canvas.mpl_connect("key_press_event", lambda event: print(f"you pressed {event.key}"))
	canvas.mpl_connect("key_press_event", key_press_handler)

	toolbar.pack(side=BOTTOM, fill=X)
	canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
	# return canvas


stop = False
def onClosing():
	global animating
	if (animating):
		# print("I was called")
		# anim.pause()
		# time.sleep(1)
		# window.destroy()
		global stop
		stop = True
	else:
		print("Hey man")
		window.destroy()

button = Button(master=window, text="BubbleSort", command= lambda: visualize(N, 'b') )
button.pack(side=BOTTOM)
window.protocol("WM_DELETE_WINDOW", onClosing)
print("\a")
window.mainloop()
