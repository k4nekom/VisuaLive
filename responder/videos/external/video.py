from abc import ABCMeta, abstractmethod

class Video(metaclass=ABCMeta):
    @abstractmethod
    def get_data(self):
        pass

    # コメント末尾が w 草 かどうかを判定する関数
    def has_kusa(self, comment):
        if comment[-1] == 'w':
            return True
        
        if comment[-1] == 'W':
            return True
        
        if comment[-1] == 'ｗ':
            return True


        if comment[-1] == 'W':
            return True
        
        if comment[-1] == '草':
            return True

        return False