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

    @property
    def available_18_sessions(self):
        return [a for a in self.sessions if a.is_18 and a.is_available]

    @property
    def is_18_session_available(self):
        return len(self.available_18_sessions) > 0


    @property
    def available_45_sessions(self):
        return [a for a in self.sessions if a.is_45 and a.is_available]


    @property
    def is_45_session_available(self):
        return len(self.available_45_sessions) > 0

    @property
    def detail_available_18_info_str(self):
        text = f"{self.pincode} {self.name} {self.address}\n"
        for a in self.available_18_sessions:
            text += a.display_info_str + "\n"
        return text

    @property
    def detail_available_45_info_str(self):
        text = f"{self.pincode} {self.name} {self.address}\n"
        for a in self.available_45_sessions:
            text += a.display_info_str + "\n"
        return text

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

    @property
    def slots_str(self):
        return ", ".join(self.slots)

    @property
    def is_available(self):
        return self.available_capacity > 0

    @property
    def is_18(self):
        return self.min_age_limit == 18

    @property
    def is_45(self):
        return self.min_age_limit == 45

    @property
    def display_info_str(self):
        text = f"{self.date}:  {self.vaccine} -> Available Slots:{self.available_capacity}\n"
        return text
