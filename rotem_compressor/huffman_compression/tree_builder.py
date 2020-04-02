import queue

from rotem_compressor.data_models.tree_node import Node


class TreeBuilder:
    def __init__(self, dictionary_size):
        self.dictionary_size = dictionary_size

    def _get_frequencies(self, data):
        frequencies = [0] * self.dictionary_size
        for char in data:
            frequencies[char] += 1
        return frequencies

    def __put_in_queue_by_frequency(self, frequencies, priority_queue):
        for char, frequency in enumerate(frequencies):
            if frequency > 0:
                priority_queue.put((frequency, Node(None, None, char)))

    def construct_tree(self, data):
        frequencies = self._get_frequencies(data)
        priority_queue = queue.PriorityQueue()
        self.__put_in_queue_by_frequency(frequencies, priority_queue)
        while priority_queue.qsize() > 1:
            left_frequency, left = priority_queue.get()
            right_frequency, right = priority_queue.get()
            priority_queue.put((left_frequency + right_frequency, Node(left, right, None)))
        return priority_queue.get()[1]