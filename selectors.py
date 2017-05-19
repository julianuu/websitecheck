from abc import ABC, abstractmethod

class Selector(ABC):
    @abstractmethod
    def select():
        pass

def selectors_to_string(selectors):
    strings = [selector[0] for selector in selectors]
    return ",".join(strings)

def id(tag_id):
    def select_by_id(soup):
        return soup.find(id=tag_id)
    return ["id='" + tag_id + "'", select_by_idi]
