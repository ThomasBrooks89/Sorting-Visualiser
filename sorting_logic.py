from dataclasses import dataclass, field
import random

@dataclass
class NextStep:
    array: list[int] 
    highlights: list[tuple[int, str]]  # list of tuples - (index to be highlighted, colour to highlight it)
    actions: list[str]
    stats: list[str] = field(default_factory = list)  # list of strings of whatever stat/info is to be shown
    

def generate_array(min, max):
    array = [x for x in range(min, (max + 1))]
    random.shuffle(array)
    return array


def send_finished_array(array):  # completely fakes the 'checking' to 'make sure' the list is sorted at the end
    for i in range(len(array)):
        highlights = [(x, "green2") for x in range(i)]
        highlights.append((i, "yellow"))
        yield NextStep(array[:], highlights, [], [f"Confirmed Correct: {i}"])
    highlights[-1] = ((len(array) - 1, "green2"))
    yield NextStep(array[:], highlights, ["finished"], ["Confirmed correct: Full array!"])


def selection_sort(array):
    comparisons = 0
    swaps = 0
    
    for i in range(len(array)):

        smallest_idx, smallest_value = i, array[i]
        highlights = [(x, "green4") for x in range(i)]  # all the 'sorted' values
        highlights.append((i, "white"))  # so that highlights[-2] can be "current smallest"
        highlights.append((i, "deepskyblue2"))  # the index currently being checked
        yield NextStep(array[:], highlights, ["pass_done"], [f"Comparisons: {comparisons}", f"Swaps: {swaps}", f"Smallest value: {smallest_value}", f"Smallest index: {smallest_idx}", f"Sorted Elements: {i}/{len(array)}"])

        for j, value in enumerate(array[i:], start=i):
            comparisons += 1
            if value < smallest_value:
                smallest_idx = j
                smallest_value = value

            highlights[-2] = (smallest_idx, "yellow")
            highlights[-1] = (j, "deepskyblue2")
            yield NextStep(array[:], highlights, [], [f"Comparisons: {comparisons}", f"Swaps: {swaps}", f"Smallest value: {smallest_value}", f"Smallest index: {smallest_idx}", f"Sorted Elements: {i}/{len(array)}"])

        array[smallest_idx], array[i] = array[i], array[smallest_idx]
        swaps += 1
        highlights[-2] = (smallest_idx, "yellow")
        highlights[-1] = (i, "green2")  # to signify the swap
        yield NextStep(array[:], highlights, ["swap"], [f"Comparisons: {comparisons}", f"Swaps: {swaps}", f"Smallest value: {smallest_value}", f"Smallest index: {smallest_idx}", f"Sorted Elements: {i}/{len(array)}"])
    yield from send_finished_array(array)


def bubble_sort(array):
    end_idx = len(array) - 1
    comparisons = 0
    swaps = 0

    for _ in range(len(array)):
        highlights = [(x, "green4") for x in range(end_idx + 1, len(array))]
        yield NextStep(array[:], highlights, ["pass_done"], [f"Comparisons: {comparisons}", f"Swaps: {swaps}", "Currently comparing: 0 & 1", f"Sorted elements: 0/{len(array)}"])

        highlights.append(None) # dummy values to get overwritten in next loop
        highlights.append(None)

        for i in range(end_idx):
            comparisons += 1
            # highlight the two elements being compared
            highlights[-1] = ((i, "deepskyblue2"))
            highlights[-2] = ((i+1, "deepskyblue2"))
            yield NextStep(array[:], highlights, [], [f"Comparisons: {comparisons}", f"Swaps: {swaps}", f"Currently comparing: {i} & {i+1}", f"Sorted elements: {len(array) - end_idx - 1}/{len(array)}"])

            # need to be swapped
            if array[i+1] < array[i]:
                swaps += 1

                highlights[-1] = (i+1, "yellow")  # show the smaller value in yellow
                yield NextStep(array[:], highlights, [], [f"Comparisons: {comparisons}", f"Swaps: {swaps}", f"Currently comparing: {i} & {i+1}", f"Sorted elements: {len(array) - end_idx - 1}/{len(array)}"])

                array[i], array[i+1] = array[i+1], array[i]  # swap them

                highlights[-2] = (i, "yellow")  # show the smaller value, now in the i pos, in yellow
                highlights[-1] = (i+1, "white")
                yield NextStep(array[:], highlights, ["swap"], [f"Comparisons: {comparisons}", f"Swaps: {swaps}", f"Currently comparing: {i} & {i+1}", f"Sorted elements: {len(array) - end_idx - 1}/{len(array)}"])

            else:  # no need for swap
                highlights[-1] = ((i, "yellow"))  # show the smaller value already in the lower pos
                highlights[-2] = ((i+1, "white"))
                yield NextStep(array[:], highlights, [], [f"Comparisons: {comparisons}", f"Swaps: {swaps}", f"Currently comparing: {i} & {i+1}", f"Sorted elements: {len(array) - end_idx - 1}/{len(array)}"])
        end_idx -= 1
    yield from send_finished_array(array)


def insertion_sort(array):
    comparisons, swaps = 0,0
    for i in range(1, len(array)):
        highlights = [(x, "gray71") for x in range(i, len(array))]
        highlights.append(None)  # placeholders for the element being bubbled

        curr_i = i
        while curr_i > 0:
            comparisons += 1

            highlights[-1] = ((curr_i, "yellow"))
            yield NextStep(array[:], highlights, [], [f"Comparisons: {comparisons}", f"Swaps: {swaps}", f"Bars placed: {i}/{len(array)}", f"Currently placing: {array[curr_i]}"])

            if array[curr_i] < array[curr_i - 1]:
                swaps += 1
                array[curr_i], array[curr_i - 1] = array[curr_i - 1], array[curr_i]
                curr_i -= 1
            else:
                highlights[-1] = ((curr_i, "green2"))
                yield NextStep(array[:], highlights, ["pass_done"], [f"Comparisons: {comparisons}", f"Swaps: {swaps}", f"Bars placed: {i}/{len(array)}", f"Currently placing: {array[curr_i]}"])
                break

    yield from send_finished_array(array)


def shell_sort(array):
    comparisons, swaps = 0, 0

    # first make the gap sequence list with 2**k - 1
    gaps = [1]
    k = 2
    while True:
        gaps.append((2**k) - 1)
        if gaps[-1] > (len(array) // 2):
            break
        k += 1

    for step in gaps[::-1]:
        for i in range(0+step, len(array), step):
            highlights = [(x, "gray86") for x in range(len(array)) if x % step != 0]
            highlights.append(None)  # placeholders for the element being bubbled

            curr_i = i
            while curr_i > 0:
                comparisons += 1

                highlights[-1] = ((curr_i, "yellow"))
                yield NextStep(array[:], highlights, [], [f"Comparisons: {comparisons}", f"Swaps: {swaps}", f"Current gap: {step}", f"Gaps: {gaps[::-1]}"])

                if array[curr_i] < array[curr_i - step]:
                    swaps += 1
                    array[curr_i], array[curr_i - step] = array[curr_i - step], array[curr_i]
                    curr_i -= step
                else:
                    highlights[-1] = ((curr_i, "green2"))
                    yield NextStep(array[:], highlights, ["pass_done"], [f"Comparisons: {comparisons}", f"Swaps: {swaps}", f"Current gap: {step}", f"Gaps: {gaps[::-1]}"])
                    break
    yield from send_finished_array(array)








        
if __name__ == "__main__":
    array = generate_array(1, 100)
    #for step in selection_sort(array):
        #print(step.array)
    print(array)
    print(shell_sort(array))


