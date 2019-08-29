import json
# added to put object in JSON


class Object(object):
    def __init__(self):
        self.name = "webrtcHacks TensorFlow Object Detection REST API"

    def toJson(self):
        return json.dumps(self.__dict__)
