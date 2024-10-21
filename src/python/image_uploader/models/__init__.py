import json
from abc import ABC, abstractmethod


class DBModel(ABC):

    @abstractmethod
    def table_name(self):
       pass

    @abstractmethod
    def partition_key(self):
       pass

