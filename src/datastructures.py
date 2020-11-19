from random import randint

class Notifications:
    def __init__(self):
        self.current_queue = [    
                {
            "title": "Website Re-Design Plan",
            "startDate": "21-11-2020",
            "id": 0,
            "location": "Room 1"
        },   
        {
            "title": "Install New Router in Dev Room",
            "startDate": "23-11-2020",
            "id": 2,
            "location": "Room 2"
        },
        {
            "title": "Book Flights to San Fran for Sales Trip",
            "startDate": "27-11-2020",
            "id": 1,
            "location": "Room 1"
        },
        # CLEAR BELOW AFTER TONIGHT!!! PLEASEEEE 
        {
            "title": "Website Re-Design Plan 1",
            "startDate": "21-11-2020",
            
            "id": 0,
            "location": "Room 1"
        },
        {
            "title": "Website Re-Design Plan 2",
            "startDate": "21-11-2020",
            
            "id": 0,
            "location": "Room 1"
        },
        {
            "title": "Website Re-Design Plan 3 ",
            "startDate": "21-11-2020",
            
            "id": 0,
            "location": "Room 1"
        },
        {
            "title": "Website Re-Design Plan 4",
            "startDate": "21-11-2020",
            
            "id": 0,
            "location": "Room 1"
        }
            ]

    def enqueue(self, item):
        self.current_queue.insert(0, item)
        pass

    def dequeue(self):
        return self.current_queue.pop() 

    def get_queue(self):
        return self.current_queue

    def size(self):
        return len(self.current_queue) 