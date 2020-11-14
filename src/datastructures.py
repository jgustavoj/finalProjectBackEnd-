from random import randint

class Notifications:
    def __init__(self):
        self.current_queue = []

    def enqueue(self, item):
        self.current_queue.insert(0, item)
        pass

    def dequeue(self):
        return self.current_queue.pop() 

    def get_queue(self):
        return self.current_queue

    def size(self):
        return len(self.current_queue) 