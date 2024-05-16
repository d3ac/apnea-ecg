import matlab
import matlab.engine
import step2
import  os
import step4

path = 'data'

eng = matlab.engine.start_matlab()
a = eng.step1(path + '\\')
print(a)

step2.step2()

a = eng.step3()
print(a)

step4.step4()