"""
 Define Objects for all entities present in client APISETU.
 Eg:
"""
class BaseObject:
    def __init__(self, **kwargs):
        for k in kwargs:
            setattr(self, k, kwargs[k])

class StateObject(BaseObject):
    state_id: int
    state_name: str

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __repr__(self):
        # return f"State: {self.state_name}({self.state_id})"
        return "State: {}({})".format(self.state_name,self.state_id)


class DistrictObject(BaseObject):
    state_id: int
    district_id: int
    district_name: str

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __repr__(self):
        return "District: {}({})".format(self.district_name,self.district_id)


class CenterObject(BaseObject):
    center_id: int
    name: str
    address: str
    state_name: str
    district_name: str
    pincode: str
    _from: str
    to: str

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.sessions = [SessionObject(**s) for s in self.sessions]

    def __repr__(self):
        return "Center: {}({})".format(self.name,self.center_id,)


class SessionObject(BaseObject):
    session_id: int
    date: str
    available_capacity: int
    min_age_limit: int
    vaccine: str
    slots: list

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __repr__(self):
        return "Session: Date:{}, Vaccine {}, Availability {}".format(self.date,self.vaccine, self.available_capacity)

