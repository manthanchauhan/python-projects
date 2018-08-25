import string
import tkinter
class ComplexNumber(object):
    def __init__(self, real, imaginary):
        self.real = real
        self.imaginary = imaginary
    def __add__(self, other):
        real = self.real + other.real
        imaginary = self.imaginary + other.imaginary
        c3 = ComplexNumber(real, imaginary)
        return c3
    def invert(self):
        real = self.real
        imag = self.imaginary
        imag = - imag
        real /= (self.real ** 2 + self.imaginary ** 2)
        imag /= (self.real ** 2 + self.imaginary ** 2)
        return ComplexNumber(real, imag) 
    def multiply(self, other):
        real = self.real * other.real - self.imaginary * other.imaginary
        imag = self.real * other.imaginary + self.imaginary * other.real
        return ComplexNumber(real, imag)
    def subtract(self, other):
        c = other.negation()
        c = self + c
        return c
    def divide(self, other):
        c = other.invert()
        c = self.multiply(c)
        return c
    def __str__(self):
        if self.real == 0 and self.imaginary == 0:
            s = '0'
        elif self.real == 0:
            s = str(self.imaginary) + 'i'
        elif self.imaginary == 0:
            s = str(self.real)
        else:
            s = str(self.real)
            if self.imaginary > 0:
                s = s + '+'
            else:
                s = s + '-'
            s = s + str(abs(self.imaginary))
            s = s + 'i'
        return s 
    def negation(self):
        real = -self.real
        imag = -self.imaginary
        return ComplexNumber(real, imag)
#some helping functions-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def inputComplexNumber(s):
    Iindex = s.find('i')
    if Iindex == -1:
        real = float(s)
        imag = 0
    elif s == 'i':
        return ComplexNumber(0, 1)
    else:
        try:
            imag = float(s[0:Iindex])
        except ValueError:
            signindex = s.find('+', 1)
            if signindex == -1:
                signindex = s.find('-', 1)
            imag = float(s[signindex + 1 : Iindex])
            if s[signindex] == '-':
                imag = - imag
            real = float(s[0:signindex])
            c = ComplexNumber(real, imag)
            return c
        real = 0
    c = ComplexNumber(real, imag)
    return c
def findresult(c1, operator, c2):
    if operator == '+':
        return c1 + c2
    elif operator == '-':
        return c1.subtract(c2)
    elif operator == '*':
        return c1.multiply(c2)
    elif operator == '/':
        return c1.divide(c2)
def keypress(key, input_screen):
    printables = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '.', 'i', '+', '-', '*', '/', '(', ')']
    if key in printables:
        index = len(input_screen.get())
        input_screen.insert(index, key)
    if key == '=':
        s = input_screen.get()
        index = len(s)
        input_screen.insert(index, ' = ')
        index1 = s.find('(')
        index2 = s.find(')')
        c1 = inputComplexNumber(s[index1 + 1: index2])
        index1 = s.find('(', index2 + 1)
        operator = s[index2 + 1:index1].split(' ')
        op = ''
        for char in operator:
            if char != '':
                op = char
                break
        index2 = s.find(')', index1 + 1)
        c2 = inputComplexNumber(s[index1 + 1: index2])
        c3 = findresult(c1, op, c2)
        index += 3
        input_screen.insert(index, c3.__str__())
    if key == 'AC':
        input_screen.delete(0, len(input_screen.get()))
#setting up the GUI here---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
parentWindow = tkinter.Tk(className='Complex Calculator')
topFrame = tkinter.Frame(parentWindow)
topFrame.pack()
bottomFrame = tkinter.Frame(parentWindow)
bottomFrame.pack(side='bottom')
label = tkinter.Label(topFrame, text='Enter text here', font=('Helvetica', 14, 'bold'), width=12, bg='green')
label.pack(side= tkinter.LEFT)
input_screen = tkinter.Entry(topFrame, width=55, bd=4, font=('Helvetica', 14, 'bold'))
input_screen.pack()
layers = 4
layer = tkinter.Frame(bottomFrame)
layer_list = [layer] * layers
for i in range(0, layers):
    layer_list[i] = tkinter.Frame(bottomFrame)
    layer_list[i].pack(side='top')
buttons = 20
button_list = [['7', 'blue'], ['8', 'blue'], ['9', 'blue'], ['/', 'green'], 
                ['AC', 'green'], ['4', 'blue'], ['5', 'blue'], ['6', 'blue'], 
                ['*', 'green'], ['=', 'green'], ['1', 'blue'], ['2', 'blue'], 
                ['3', 'blue'], ['+', 'green'],['(', 'red'], ['0', 'blue'], 
                ['.', 'green'], ['i', 'green'], ['-', 'green'], [')', 'red']]  
button_index = 0
buttons_to_place = buttons // layers
for i in range(0, layers):
    for j in range(0, buttons_to_place):
        button = tkinter.Button(layer_list[i], width=12, height=2, text=button_list[button_index][0], bg=button_list[button_index][1], font=('Helvetica 14 bold'), command= lambda k = (buttons_to_place * i + j): keypress(button_list[k][0], input_screen))
        button_index += 1
        button.pack(side=tkinter.LEFT)
parentWindow.mainloop()
#GUI setup ends here----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------