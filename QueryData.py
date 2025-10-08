class Event:
    def __init__(self, number, date, description, user, documents):   
        self.number = number
        self.date = date
        self.description = description  
        self.user = user
        self.documents = documents

    def __repr__(self):
        return f"Event{{number={self.number}, date={self.date}, description={self.description}, user={self.user}, documents={self.documents} }}"

class Subject:
    def __init__(self, code, description, principal):   
        self.code = code
        self.description = description
        self.principal = principal  

    def __repr__(self):
        return f"Subject{{ code={self.code}, description={self.description}, principal={self.principal} }}"

class Process:
    def __init__(self, number, author, defendant, subject, last_event, params):   
        self.number = number
        self.author = author
        self.defendant = defendant
        self.subject = subject
        self.last_event = last_event
        self.params = params
        self.subjects = []
        self.events = []

    def __repr__(self):
        return f"Process{{ number={self.number}, author={self.author}, defendant={self.defendant}, subject={self.subject}, last_event={self.last_event}, params={self.params} }}"

    def add_subject(self, subject):
        self.subjects.append(subject)

    def add_event(self, event):
        self.events.append(event)

class Party:
    def __init__(self, name, doc, params):
        self.name = name
        self.doc = doc
        self.params = params
        self.processes = []

    def __repr__(self):
        return f"Party{{ name={self.name}, doc={self.doc}, params={self.params} }}"
    
    def add_process(self, process):
        self.processes.append(process)
        
class Search:
    def __init__(self, name):
        self.name = name
        self.parties = []

    def __repr__(self):
        return f"Search{{ name={self.name} }}"

    def add_party(self, party):
        self.parties.append(party)


def serialize_to_dict(obj):
    if isinstance(obj, (Search, Party, Process, Subject, Event)):
        return obj.__dict__
    raise TypeError("Type not serializable")
