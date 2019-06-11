class EngineException(Exception):
    name: str
    description: str

    def __init__(self, name: str, description: str=''):
        Exception.__init__(self, description)
        self.name = name
        self.description = description
