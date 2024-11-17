from abc import ABC, abstractmethod

class BaseCommand(ABC):
    def __init__(self, logger):
        self.logger = logger
    
    @abstractmethod
    def execute(self, args):
        pass