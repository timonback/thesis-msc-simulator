class Request:
    id = 0

    def __init__(self, incoming_time: int, duration: float, memory: int):
        self.id = Request.id
        self.start = incoming_time
        self.duration = duration
        self.memory = memory

        Request.id = Request.id + 1

    @property
    def end(self) -> float:
        return self.start + self.duration

    def __repr__(self):
        return 'Request[id={id}]'.format(id=self.id)

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, Request):
            return False
        return self.id == o.id
