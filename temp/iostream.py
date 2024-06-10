from sys import stdin
import sys,os
def format_error(s):
    return "\033[1;31m"+s
class IO:
    def __init__(self):
        self.tie = 1
        self.endl = 0
        self.precision = float('inf')
        self.sep = ''
def endl():
    return '\n'
class cin(IO):
    def __rshift__(self, other):
        try:
            try:
                other._type
            except Exception as e:
                err,err_obj,err_ = sys.exc_info()
                file =  os.path.split(err_.tb_frame.f_code.co_filename)[1]
                quit(format_error("Code terminated successfully:\n"
                                  "\tat line "+str(err_.tb_lineno)+
                                  ":\n\t\t"+type(e).__name__+": Cin works with only iostream data-structures"))

            s = ""
            while 1:
                temp = stdin.read(1)
                if((temp == " " and s == " ") or (temp == "\n" and s == "\n")):
                    continue
                if ((temp == ' ' or temp == '\n')):
                    break
                s += temp
            other.value = Int(s).value
            return self
        except ValueError:
            raise AssertionError("Error: Cin works with only variables!")
        except AttributeError:
            raise AssertionError("Error: Cin works with only variables!")
class cin2(IO):
    def __rshift__(self, other):
        try:
            s = ""
            while 1:
                temp = stdin.read(1)
                if((temp == " " and s == " ") or (temp == "\n" and s == "\n")):
                    continue
                if ((temp == ' ' or temp == '\n')):
                    break
                s += temp
            other = int(s)
            return self
        except ValueError:
            raise AssertionError("Error: Cin works with only variables!")
        except AttributeError:
            raise AssertionError("Error: Cin works with only variables!")

class cout(IO):
    # def __init__(self):
    #     super(IO)

    def __lshift__(self, other):
        try:
            if (not self.endl):
                print(other, end=self.sep)
            return self
        except ValueError:
            assert "Error: Cout works with only variables!"

class Int(object):
    def __init__(self, value="0",base = 10):
        self.value = value
        self.base = base
        self._type = 'int'
    def __eq__(self, other):
        return self.value == other.value

    def __str__(self):
        return self.value

    def __add__(self, other):
        return Int(value = str(int(self.value) + int(other.value)),base = 10)
    def __mul__(self, other):
        return str(int(self.value) * int(other.value))

def swap(a,b):
    a,b=b,a

cin = cin()
cin2 = cin2()
cout = cout()
endl = endl()
if __name__ == "__main__":
    a = Int()
    b = Int()
    c = Int()
    cin >> a >> b >> c
    cout << a+b+c << endl


