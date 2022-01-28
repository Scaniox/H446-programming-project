import re

class Config():
    def __init__(self):
        self.a = 7
        self.b = 2
        self.c = False
        self.d = 'another string '

    def save(self):
        self_file = open(__file__, "r")
        self_file_str = self_file.read()
        self_file.close()

        for identifier, val in self.__dict__.items():
            self_file_str = re.sub(f" self\.{identifier} = .+\n", \
                                   f" self.{identifier} = {repr(val)}\n", \
                                   self_file_str)

        self_file = open(__file__, "w")
        self_file.write(self_file_str)
        self_file.close()


c1 = Config()
print(c1.__dict__)
c1.a = 7
c1.c = False
c1.d = "another string "
print(c1.__dict__)
c1.save()
