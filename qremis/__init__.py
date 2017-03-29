from functools import partial


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


def lowerFirst(s):
    if not s:
        return s
    return s[0].lower() + s[1:]


class QremisElement:
    def __init__(self, *args, **kwargs):
        # Be sure we can build a valid element
        mandatory_fields = set(x for x in self._spec if self._spec[x]['mandatory'] is True)
        provided_fields = set(lowerFirst(x.__class__.__name__) for x in args)
        provided_fields = provided_fields.union(set([x for x in kwargs]))
        if not mandatory_fields.issubset(provided_fields):
            raise ValueError(
                "The following are required for init, but were not present: {}".format(
                    ", ".join(mandatory_fields - provided_fields)
                )
            )
        for x in provided_fields:
            if x not in self._spec:
                raise TypeError("Erroneous field!")

        # Dynamically build getters, setters, dellers, adders from spec
        for x in self._spec:
            setattr(self, "get_{}".format(x), partial(self.get_field, x))
            setattr(self, "set_{}".format(x),
                    partial(self.set_field, x, _type=self._spec[x]['type'],
                            repeatable=self._spec[x]['repeatable']))
            setattr(self, "del_{}".format(x), partial(self.del_field, x))
            if self._spec[x]['repeatable']:
                setattr(self, "add_{}".format(x), partial(self.add_to_field, x, _type=self._spec[x]['type']))

            # Set the object properties
            # TODO: Unbreak? Remove?
            # I think this has something to do with attribute search order?
            setattr(self, "{}".format(x), property(fget=getattr(self, "get_{}".format(x)),
                                                   fset=getattr(self, "set_{}".format(x)),
                                                   fdel=getattr(self, "del_{}".format(x))))

        # Build the element with the init args
        self._fields = {}
        for x in args:
            if not isinstance(x, QremisElement):
                raise ValueError("Only QremisElement instance are accepted as args")
            if self._spec[lowerFirst(x.__class__.__name__)]['repeatable']:
                getattr(self, "add_{}".format(lowerFirst(x.__class__.__name__)))(x)
            else:
                getattr(self, "set_{}".format(lowerFirst(x.__class__.__name__)))(x)
        for x in kwargs:
            if self._spec[x]['repeatable']:
                getattr(self, "add_{}".format(x))(kwargs[x])
            else:
                getattr(self, "set_{}".format(x))(kwargs[x])

    def set_field(self, fieldname, fieldvalue, _type=None, repeatable=False):
        if repeatable:
            try:
                self.add_to_field(fieldname, fieldvalue, _type=_type)
            except TypeError:  # Maybe its an iter of values
                for x in fieldvalue:
                    self.add_to_field(fieldname, x, _type=_type)
        else:
            if _type is not None:
                if not isinstance(fieldvalue, _type):
                    raise TypeError()
            self._fields[fieldname] = fieldvalue

    def add_to_field(self, fieldname, fieldvalue, _type=None):
        if _type is not None:
            if not isinstance(fieldvalue, _type):
                raise TypeError()
        if fieldname not in self._fields:
            self._fields[fieldname] = []
        self._fields[fieldname].append(fieldvalue)

    def get_field(self, fieldname):
        return self._fields[fieldname]

    def del_field(self, fieldname, index=None):
        # Dynamically removes empty fields
        if index:
            del self._fields[fieldname][index]
            if len(self._fields[fieldname]) == 0:
                del self._fields[fieldname]
        else:
            del self._fields[fieldname]

    def to_dict(self):
        r = {}
        return r


class ObjectIdentifier(QremisElement):
    _spec = {
        'objectIdentifierType': {'repeatable': False, 'mandatory': True, 'type': str},
        'objectIdentifierValue': {'repeatable': False, 'mandatory': True, 'type': str}
    }


class Object(QremisElement):
    _spec = {
        'objectIdentifier': {'repeatable': True, 'mandatory': True, 'type': ObjectIdentifier}
    }


class Event(QremisElement):
    pass


class Agent(QremisElement):
    pass


class Rights(QremisElement):
    pass


class Relationship(QremisElement):
    pass


class Qremis(QremisElement):
    _spec = {
        'object': {'repeatable': True, 'mandatory': False, 'type': Object},
        'event': {'repeatable': True, 'mandatory': False, 'type': Event},
        'agent': {'repeatable': True, 'mandatory': False, 'type': Agent},
        'rights': {'repeatable': True, 'mandatory': False, 'type': Rights},
        'relationship': {'repeatable': True, 'mandatory': False, 'type': Relationship}
    }
