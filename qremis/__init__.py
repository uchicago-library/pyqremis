from abc import ABCMeta


class QremisRecord:
    @classmethod
    def from_json_file(cls, f):
        pass

    @classmethod
    def from_json_str(cls, s):
        pass

    @classmethod
    def from_dict(cls, d):
        pass

    @classmethod
    def from_xml_file(cls, f):
        pass

    @classmethod
    def from_xml_str(cls, s):
        pass

    @classmethod
    def from_etree(cls, e):
        pass

    def __init__(self):
        self._object_list = []
        self._event_list = []
        self._agent_list = []
        self._rights_list = []
        self._relationship_list = []

    def get_object_list(self):
        return self._object_list

    def set_object_list(self, i):
        del self.object_list
        for x in i:
            self.add_object(x)

    def del_object_list(self):
        self._object_list = []

    def add_object(self, o):
        if not isinstance(o, Object):
            raise TypeError()
        self._object_list.append(o)

    def get_event_list(self):
        return self._event_list

    def set_event_list(self, i):
        del self.event_list
        for x in i:
            self.add_event(x)

    def del_event_list(self):
        self._event_list = []

    def add_event(self, e):
        if not isinstance(e, Event):
            raise TypeError()
        self._event_list.append(e)

    def get_agent_list(self):
        return self._event_list

    def set_agent_list(self, i):
        del self.agent_list
        for x in i:
            self.add_agent(i)

    def del_agent_list(self):
        self._agent_list = []

    def add_agent(self, a):
        if not isinstance(a, Agent):
            raise TypeError()
        self._agent_list.append(a)

    def get_rights_list(self):
        return self._rights_list

    def set_rights_list(self, i):
        del self.rights_list
        for x in i:
            self.add_rights(x)

    def del_rights_list(self):
        self._rights_list = []

    def add_rights(self, r):
        if not isinstance(r, Rights):
            raise TypeError()
        self._rights_list.append(r)

    def get_relationship_list(self):
        return self._relationship_list

    def set_relationship_list(self, i):
        del self.relationship_list
        for x in i:
            self.add_relationship(x)

    def del_relationship_list(self):
        self._relationship_list = []

    def add_relationship(self, r):
        if not isinstance(r, Relationship):
            raise TypeError()
        self._relationship_list.append(r)

    def to_dict(self):
        return {
            "qremis": {
                "object": [x.to_dict() for x in self.object_list],
                "event": [x.to_dict() for x in self.event_list],
                "agent": [x.to_dict() for x in self.agent_list],
                "rights": [x.to_dict() for x in self.rights_list],
                "relationship": [x.to_dict() for x in self.relationship_list]
            }
        }

    def to_etree(self):
        pass

    object_list = property(get_object_list, set_object_list, del_object_list)
    event_list = property(get_event_list, set_event_list, del_event_list)
    agent_list = property(get_agent_list, set_agent_list, del_agent_list)
    rights_list = property(get_rights_list, set_rights_list, del_rights_list)
    relationship_list = property(get_relationship_list, set_relationship_list, del_relationship_list)


class QremisElement(metaclass=ABCMeta):
    def to_dict(self):
        pass


class Qremis(QremisElement):
    pass


class Object(QremisElement):
    pass


class Event(QremisElement):
    pass


class Agent(QremisElement):
    pass


class Rights(QremisElement):
    pass


class Relationship(QremisElement):
    pass
