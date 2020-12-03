from abc import ABCMeta, abstractmethod

class Video(metaclass=ABCMeta):
    @abstractmethod
    def get_info(self):
        pass

    @abstractmethod
    def get_comment_data(self):
        pass