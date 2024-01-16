import random
from random import shuffle
from time import perf_counter
import csv

class Node:
    def __init__(self, val=None):
        if val is not None:
            self.value = val
            self.next = Node()
        else:
            self.value = None
            self.next = None

    def append(self, val):
        if self.value is not None:
            self.next.append(val)
        else:
            self.value = val
            self.next = Node()

    def __str__(self):
        return str(self.value)

class LinkedList:
    def __init__(self, values):
        self.head = Node()
        self.curr = self.head
        self.len = 0
        try:
            self.concat(values)
        except TypeError:
            self.append(values)

    def append(self, val):
        self.len += 1
        self.head.append(val)

    def concat(self, values):
        for item in values:
            self.append(item)

    def __iter__(self):
        return self

    def __next__(self):
        if self.curr.value is not None:
            out = self.curr.value
            self.curr = self.curr.next
            return out
        else:
            self.curr = self.head
            raise StopIteration

    def __str__(self):
        out = '['
        for item in self:
            out += str(item) + ', '
        return out[:-2] + ']'

    def __len__(self):
        return self.len

    def __getitem__(self, item):
        if isinstance(item, slice):
            start, stop, step = item.indices(self.len)
            indices = range(start, stop, step)
            return [self[i] for i in indices]
        elif item in range(-self.len, self.len):
            curr = self.head
            item %= self.len
            for _ in range(item):
                curr = curr.next
            return curr.value
        else:
            raise IndexError(f'Index {item} is out of range for list of length {self.len}.')


    def __setitem__(self, key, value):
        if key in range(-self.len, self.len):
            curr = self.head
            key %= self.len
            for _ in range(key):
                curr = curr.next
            curr.value = value
        else:
            raise IndexError(f'Index {key} is out of range for list of length {self.len}.')

    def __delitem__(self, key):
        if key in range(-self.len, self.len):
            curr = self.head  # Initialize current node to head
            prev = None  # Initialize previous node as None (no node before head)
            key %= self.len  # Handle negative exponents
            for _ in range(key):
                prev = curr  # Advance through the list, updating prev and curr
                curr = curr.next
            if prev is not None:
                prev.next = curr.next  # Remove curr from the chain
                curr.next = None
            else:
                self.head = self.head.next  # Handle the case where we are removing the first node in the list
                self.curr = self.head  # Make sure we don't break the iterator we set up earlier
                curr.next = None
            self.len -= 1  # Decrement len since we removed a node from the chain.
        else:
            raise IndexError(f'Index {key} is out of range for list of length {self.len}.')

    def insert(self, key, item):
        if key in range(-self.len, self.len):
            curr = self.head  # Initialize current node to head
            prev = None  # Initialize previous node as None (no node before head)
            key %= self.len  # Handle negative exponents
            newnode = Node(item)  # Create a new node to store the new item.
            for _ in range(key):
                prev = curr  # Advance through the list, updating prev and curr
                curr = curr.next
            if prev is not None:
                prev.next = newnode  # Insert a new node into the chain
                newnode.next = curr
            else:
                self.head = newnode  # Handle the case where we are replacing the first node in the list
                self.curr = self.head   # Make sure we don't break the iterator we set up earlier
                newnode.next = curr
            self.len += 1  # Increment len since we added a node to the chain.
        elif key == self.len:
            self.append(item)  # If we are adding a node at the end, simply use append.
        else:
            raise IndexError(f'Index {key} is out of range for list of length {self.len}.')


    # Takes two indices and swaps the values
    def swap(self, key1, key2):
        item = self[key1]
        self[key1] = self[key2]
        self[key2] = item


    def sorted(self):
        curr = self.head
        for _ in range(self.len - 1):
            if curr.value > curr.next.value:
                return False
            curr = curr.next
        return True


    def max_idx(self):
        curr = self.head
        max_idx = 0
        for _ in range(self.len):
            if curr.value > self[max_idx]:
                max_idx = _
            curr = curr.next
        return max_idx


    def min_idx(self):
        curr = self.head
        min_idx = 0
        for _ in range(self.len):
            if curr.value < self[min_idx]:
                min_idx = _
            curr = curr.next
        return min_idx


    # Sorts the list using bubble sort
    def bubble_sort(self):
        for i in range(self.len - 1):
            curr = self.head
            for j in range(self.len - i - 1):
                if curr.value > curr.next.value:
                    self.swap(j, j + 1)
                curr = curr.next
        

def main():
    with open("bubble_sort.csv", "w", newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(["List Length", "Already Sorted Time (s)", "Almost Sorted Time (s)", "Completely Random Time (s)"])

            for length in range(1, 501):
                # Already sorted
                alr_sorted = LinkedList(list(range(length)))
                time_start = perf_counter()
                alr_sorted.bubble_sort()
                time_taken_alr_sorted = perf_counter() - time_start

                # Almost sorted
                almost_sorted = LinkedList(list(range(length)))
                shuffle(almost_sorted[0:length // 10])
                time_start = perf_counter()
                almost_sorted.bubble_sort()
                time_taken_almost_sorted = perf_counter() - time_start

                # Completely random
                random_list = LinkedList(random.sample(range(length), length))
                time_start = perf_counter()
                random_list.bubble_sort()
                time_taken_random = perf_counter() - time_start

                csvwriter.writerow([length, time_taken_alr_sorted, time_taken_almost_sorted, time_taken_random])


if __name__ == '__main__':
    main()