import queue

from rotem_compressor.data_models.tree_node import Node


class TreeBuilder:
    def __init__(self, dictionary_size):
        self.dictionary_size = dictionary_size

    def get_frequencies(self, data):
        frequencies = [0] * self.dictionary_size
        for char in data:
            frequencies[char] += 1
        return frequencies

    def construct_tree(self, data):
        frequencies = self.get_frequencies(data)
        priority_queue = queue.PriorityQueue()
        for char, frequency in enumerate(frequencies):
            if frequency > 0:
                priority_queue.put((frequency, Node(None, None, char)))
        while priority_queue.qsize() > 1:
            left_frequency, left = priority_queue.get()
            right_frequency, right = priority_queue.get()
            priority_queue.put((left_frequency + right_frequency, Node(left, right, None)))
        return priority_queue.get()[1]