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

def sort(method, size, a, b):

	global array
	def swap(array, i, j):
		"""Helper function to swap elements i and j of list A."""

		if i != j:
			array[i], array[j] = array[j], array[i]

	def bubblesort(array):
		if len(array) == 1:
			return

		swapped = True
		for i in range(len(array) - 1):
			if not swapped:
				yield (array, [-1, -1], [0, len(array) -1] )
				break
			swapped = False
			for j in range(len(array) - 1 - i):
				if array[j] > array[j + 1]:
					swap(array, j, j + 1)
					swapped = True
				yield (array, [j, j+1], [len(array) - i, len(array)-1] )
			# yield (array, [-1, -1], [len(array) - i, len(array) -1] )

	def insertionsort(array):
		for i in range(1, len(array)):
			j = i
			while j > 0 and array[j] < array[j - 1]:
				swap(array, j, j - 1)
				j -= 1
				yield (array, [j, j+1], [j+2,j+2])
			yield (array, [j, j+1], [0, i])

	def mergesort(array, start, end):

		if end <= start:
			return

		mid = start + ((end - start + 1) // 2) - 1
		yield from mergesort(array, start, mid)
		yield from mergesort(array, mid + 1, end)
		yield from merge(array, start, mid, end)
		yield array, [-1], [start,end]

	def merge(array, start, mid, end):
		
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
			yield(array, [leftIdx, rightIdx], -1)

		while leftIdx <= mid:
			merged.append(array[leftIdx])
			leftIdx += 1
		yield(array, [leftIdx, rightIdx], -1)

		while rightIdx <= end:
			merged.append(array[rightIdx])
			rightIdx += 1
		yield(array, [leftIdx, rightIdx], -1)

		for i, sorted_val in enumerate(merged):
			array[start + i] = sorted_val
		yield (array, [-1], [start, end])

	def quicksort(array, start, end):

		if start >= end:
			return

		pivot = array[end]
		pivotIdx = start

		for i in range(start, end):
			if array[i] < pivot:
				swap(array, i, pivotIdx)
				pivotIdx += 1
				yield (array, [i, end], [end+1, 0])
		swap(array, end, pivotIdx)
		yield (array, [-1], [pivotIdx, pivotIdx])

		yield from quicksort(array, start, pivotIdx - 1)
		yield from quicksort(array, pivotIdx + 1, end)
		yield (array, [-1], [start, end])

	def quicksortCoarse(array, start, end):

		if end - start <= 10:
			insertionsort(array)

		pivot = array[end]
		pivotIdx = start

		for i in range(start, end):
			if array[i] < pivot:
				swap(array, i, pivotIdx)
				pivotIdx += 1
				yield (array, [i, end], [end+1, 0])
		swap(array, end, pivotIdx)
		yield (array, [-1], [pivotIdx, pivotIdx])

		yield from quicksort(array, start, pivotIdx - 1)
		yield from quicksort(array, pivotIdx + 1, end)
		yield (array, [-1], [start, end])

	def selectionsort(array):
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

	def heapify(array, n, i):
		# Find largest among root and children
		largest = i
		left = 2 * i + 1
		right = 2 * i + 2
	
		if left < n and array[i] < array[left]:
			yield (array, [i, left], [left+1, left])		
			largest = left
	
		if right < n and array[largest] < array[right]:
			yield (array, [largest, right], [right+1,right])			
			largest = right
	
		# If root is not largest, swap with largest and continue heapifying
		if largest != i:
			swap(array, i, largest)
			# yield (array, [-1], -1)
			yield from heapify(array, n, largest)
		
	def heapSort(array):
		n = len(array)

		# Build max heap
		for i in range(n//2, -1, -1):
			yield from heapify(array, n, i)

		for i in range(n-1, 0, -1):
			# Swap
			swap(array, 0, i)

			# Heapify root element
			yield from heapify(array, i, 0)
			yield (array, [-1], [i, len(array)-1])
		yield (array, [-1], [0, len(array)-1])
		
	def countSort(array):
		size = len(array)
		output = [0] * size
		maxElem = max(array) + 1
		# Initialize count array
		count = [0] * maxElem

		# Store the count of each elements in count array
		for i in range(0, size):
			count[array[i]] += 1

		# Store the cummulative count
		for i in range(1, maxElem):
			count[i] += count[i - 1]

		# Find the index of each element of the original array in count array
		# place the elements in output array
		i = size - 1
		while i >= 0:
			output[count[array[i]] - 1] = array[i]
			count[array[i]] -= 1
			i -= 1

		# Copy the sorted elements into original array
		for i in range(0, size):
			array[i] = output[i]
			yield (array, [-1], [0, i])


	def countSortModified(array, a, b):
		yield from countSort(array)
		count = 0
		for elem in array:
			if (elem >= a and elem < b):
				count +=1
			if (elem > b):
				break
		yield(array, [-1], -1, [a,b,count])

			
	def bucketSort(array):
		bucket = []

		# Create empty buckets
		for i in range(len(array)):
			bucket.append([])

		# Insert elements into their respective buckets
		for j in array:
			index_b = int(10 * j)
			print(index_b)
			bucket[index_b].append(j)

		# Sort the elements of each bucket
		for i in range(len(array)):
			bucket[i] = sorted(bucket[i])

		# Get the sorted elements
		k = 0
		for i in range(len(array)):
			for j in range(len(bucket[i])):
				array[k] = bucket[i][j]
				k += 1
				yield (array, [-1], [0,k-1])

		
	
	def radixSort(array):

		def countingSort(array, place):
			size = len(array)
			output = [0] * size
			count = [0] * 10

			# Calculate count of elements
			for i in range(0, size):
				index = array[i] // place
				count[index % 10] += 1

			# Calculate cumulative count
			for i in range(1, 10):
				count[i] += count[i - 1]

			# Place the elements in sorted order
			i = size - 1
			while i >= 0:
				index = array[i] // place
				output[count[index % 10] - 1] = array[i]
				count[index % 10] -= 1
				i -= 1

			for i in range(0, size):
				array[i] = output[i]
				yield (array, [-1], [0, i])


		# Get maximum element
		max_element = max(array)

		# Apply counting sort to sort elements based on place value.
		place = 1
		while max_element // place > 0:
			yield from countingSort(array, place)
			place *= 10

	# Get appropriate generator to supply to matplotlib FuncAnimation method.
	if (method == "Bubble Sort"):
		complexity = ["O(n^2)", "O(1)"]
		title = "Bubble sort"
		generator = bubblesort(array)

	elif method == "Insertion Sort":
		title = "Insertion sort"
		generator = insertionsort(array)
		complexity = ["O(n^2)", "O(1)"]

	elif method == "Merge Sort":
		title = "Merge sort"
		generator = mergesort(array, 0, size - 1)
		complexity = ["O(n log n)", "O(n)"]

	elif method == "Quick Sort":
		title = "Quicksort"
		generator = quicksort(array, 0, size - 1)
		complexity = ["O(n^2)", "O(n)"]

	elif method == "Quick Sort Coarse (7.4.5)":
		title = "Quick Sort Coarse (7.4.5)"
		generator = quicksortCoarse(array, 0, size - 1)
		complexity = ["O(n^2)", "O(n)"]

	elif method == "Count Sort":
		title = "Count Sort"
		generator = countSort(array)
		complexity = ["O(n + k)", "O(k)"]

	elif method == "Heap Sort":
		title = "Heap Sort"
		generator = heapSort(array)
		complexity = ["O(n log n)", "O(1)"]

	elif method == "Bucket Sort":
		for i in range(len(array)):
			while (array[i] >= 1):
				array[i] = round((array[i]/10), 3)
		title = "Bucket Sort"
		generator = bucketSort(array)
		complexity = ["O(n^2)", "O(n)"]

	elif method == "Count Sort Modified (8.1.4)":
		title = "Count Sort Modified (8.1.4)"
		generator = countSortModified(array, a, b)
		complexity = ["O(n + k)", "O(k)"]

	elif method == "Radix Sort":
		title = "Radix Sort"
		generator = radixSort(array)
		complexity = ["O(nk)", "O(n + k)"]
	# else:
	# 	title = "Selection sort"
	# 	generator = selectionsort(array)

	return generator,title, complexity


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
		matplotlibFrame.grid(row=3, column=2, columnspan=10)
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
		fig = figure.Figure(figsize=(8, 6)) #using plt.subplots hijacks the terminal if we close the window in the middle of sorting

	ax = fig.add_subplot()
	ax.set_title(title)	

	# Initialize a bar plot. Note that matplotlib.pyplot.bar() messed with the animation
	
	bar_rects = ax.bar(range(len(array)), array, align="center", color="c") #plt.bar(x,height, width=0.8, bottom=None, *, align="center", data=None, **kwargs)

	# Set axis limits. Set y axis upper limit high enough that the tops of
	# the bars won't overlap with the text label.
	# ax.set_xlim(-1, N )
	ax.set_ylim(0, (max(array)*1.2))

	labels = ax.bar_label(bar_rects, label_type="center")

	# Place a text label in the upper-left corner of the plot 
	time = ax.text(0.02, 0.95, "", transform=ax.transAxes)
	timeComplexity = ax.text(0.02, 0.9, "", transform = ax.transAxes)
	spaceComplexity = ax.text(0.02, 0.85, "", transform = ax.transAxes)
	inRangeText = ax.text(0.02, 0.8, "", transform = ax.transAxes)
	text = [time, timeComplexity, spaceComplexity, inRangeText]
	
	return (fig, ax, bar_rects, labels, text)

def graphAnimation(text, bar_rects, labels, complexity,  fig, generator):
	# Define function update_fig() for use with matplotlib.pyplot.FuncAnimation().
	
	iteration = [0]
	timeStart = [time.time()]
	text[1].set_text(f"Time Complexity: {complexity[0]}")
	text[2].set_text(f"Space Complexity: {complexity[1]}")

	def update_fig(generatorOutput, rects, labels, timeStart):

		if (len(generatorOutput) == 4):
			array, memoryAccess, sortedTillNow, _ = generatorOutput
		else:
			array, memoryAccess, sortedTillNow= generatorOutput

		i = 0
		for rect, val, label in zip(rects, array, labels):
			if (sortedTillNow != -1 and i< sortedTillNow[0]):
				rect.set_color("c")
			if (memoryAccess[0] != -1 and (i == memoryAccess[0] or i == memoryAccess[1])):
				rect.set_color("r")
			label.set_text(val)
			rect.set_height(val)
			i+=1

		if (sortedTillNow != -1):
			if sortedTillNow[1] == len(array):
				sortedTillNow[1] -=1

			for i in range(sortedTillNow[0], sortedTillNow[1]+1):
				rects[i].set_color('g')

		if (len(generatorOutput) == 4):
			text[3].set_text(f"{generatorOutput[3][2]} Number(s) in range {generatorOutput[3][0]} and {generatorOutput[3][1]}")

		# iteration[0] += 1
		text[0].set_text("Time elapsed: {0:.3f}".format((time.time() - timeStart[0])))
		# return rects


	global anim
	anim = animation.FuncAnimation(fig, func=update_fig,
		fargs=( bar_rects, labels, timeStart), frames=generator, interval=0,
		repeat=False)

def visualize(method, size,a,b):
	global fig
	global canvas
	
	#getting the correct sort function
	generator,title, complexity = sort(method, size, int(a) ,int(b))


	#creating the figure and bar graph that we will later animate
	fig,ax,bar_rects, labels, text = createPlot(fig,title)


	#creating the canvas and putting the graph on it:
	createOrResetCanvas(fig)

	#animating the graph
	graphAnimation(text, bar_rects, labels, complexity, fig, generator)
	
def runProgram(fileSelected, sortingMethod, inputArray):
	method = sortingMethod.get()
	fileName = fileSelected.get()
	a=b = -1


	if (sortingMethod.get() == "Count Sort Modified (8.1.4)"):
		a = inputArray[0].get()
		b = inputArray[1].get()
		
	global array
	array = handlFiles.readFile(fileName)
	size = len(array)
	if (size <= 0):
		print("The file you selected was empty, or was not read properly")
		return
	visualize(method,size, a,b)


#main program:
#creating window
window = Tk()
window.title("Sorting Visualizer")
window.geometry("1300x750")


canvas = None
array = []
fig = None

# Setting row column lengths height
window.rowconfigure(0, {'minsize': 30})
window.rowconfigure(2, {'minsize': 30})
window.columnconfigure(0, {'minsize': 60})

#sorting dropdown
options = ["Bubble Sort","Insertion Sort", "Merge Sort", "Quick Sort","Heap Sort", "Quick Sort Coarse (7.4.5)","Count Sort", "Radix Sort", "Bucket Sort", "Count Sort Modified (8.1.4)"] 
sortingMethod = StringVar()
sortingMethod.set(options[0])
dropDown = OptionMenu(window, sortingMethod,options[0],*options)

sortLabel = Label(window,text = "Select Sorting Method", font=('Arial 12'))
sortLabel.grid(row=1, column=1)
dropDown.grid(row=1, column=2, columnspan=3)

#files drop down
filenames  = os.listdir("files")
fileSelected = StringVar()
fileSelected.set(filenames[0])
fileDropDown = OptionMenu(window, fileSelected, filenames[0], *filenames, )
fileLabel = Label(window, text="Select Data Size: ", font=("arial 12"))
fileLabel.grid(row=1, column=6)
fileDropDown.grid(row=1, column= 7)

#a and b inputs:
aLabel = Label(window, text="Input value for a: ", font=("Arial 12"))
bLabel = Label(window, text="Input value for b: ", font=("Arial 12"))
a = Entry(window)
b = Entry(window)

aLabel.grid(row=1, column=9)
a.grid(row=1, column=10)
bLabel.grid(row=1, column=11)
b.grid(row=1, column=12)

# Run button
runButton = Button(master=window, text="Run", command= lambda: runProgram(fileSelected, sortingMethod, [a, b]))
runButton.grid(ipadx=30, ipady = 3, row=1, column=5)

#Creating a button to reset the file:
newDataButton = Button(master = window, text="Generate New Data", command= lambda: handlFiles.generateNewFile(fileSelected.get()))
newDataButton.grid(ipadx= 12.5, ipady = 3 , row=1, column=8)

window.mainloop()