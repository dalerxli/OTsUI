__author__ = 'landini'

try:
    import epz as tempEpz
    import inspect
    _,_,keys,_ = inspect.getargspec(tempEpz.CMD.__init__())
    if 'tag' not in keys:
        from libs.epz import epz as tempEpz
    epz = tempEpz
except:
    from libs import epz

# N set the triggers. The triggers are, in order, adc (deflection), dac (z position), time
# 1 = used, 0 = not used

#Triggers
# K = set adc (deflection) stop trigger (Volts)
# L = set dac (z position) stop trigger (Volts)
# M = set time stop trigger in microseconds
# P = set the setpoint for the feedback (-1, +1)
# Q = set the proportional gain for the feedback (0.0 to 1.0)
# R = set the integral gain for the feedback (0.0 to 1.0)
# S = set the differential gain for the feedback (0.0 to 1.0)
# B = set DAC output (Volts)
# D = set the piezo speed (Volt/s)
# C = set the piezo speed sign


'''
SET_DACSTEP:D
SET_NUMT6TRIG:T
SET_TIMETRIG:M
SET_DAC_SOFT:B
SET_DAC_HARD:U
SET_TRIGGERS:N
SET_ZTRIG:L
SET_FTRIG:K
SET_TIM8PER:8
SET_SETPOINT:P
SET_PGAIN:Q
SET_IGAIN:R
SET_DGAIN:S
START_MODSAFE:O
SET_DACMODE:F
SET_TESTPIN:H
INIT_SPI2:I
SET_RAMPSIGN:C
SET_USECIRCBUFF:G
SET_MODEDBG:E
SET_DACTO0:J
SET_DAC_2OR4:A
SWITCH_SPI2:g
KILL:k
'''


class Interpreter(object):

    def __init__(self,env,device=None,tag='CMD'):

        if device is not None:
            env.device = device
        self.cmd = epz.CMD(env,device,tag=tag)


    ## Start the SPI communication
    def startDev(self):

        self.cmd.send('SWITCH_SPI2',1)


    ## Close the communication between the PIC and the raspberry PI
    def stopDev(self):

        self.cmd.send('SWITCH_SPI2',0)


    ## Turns the DSPIC circula buffer on
    def circulaBufferOn(self):

        self.cmd.send('SET_USECIRCBUFF',1)


    ## Turns the DSPIC circula buffer off
    def circulaBufferOff(self):

        self.cmd.send('SET_USECIRCBUFF',0)


    ## Set the unipolar DAC mode
    def goUnipolar(self):

        self.cmd.send('SET_DACMODE',0)


    ## Set the bipolar DAC mode
    def goBipolar(self):

        self.cmd.send('SET_DACMODE',1)


    ## Kill the epizmq process on the target raspberry PI
    def killDev(self):

        self.cmd.send('KILL')


    ## Set the dac value
    # @param value The new dac value
    def setDacHard(self,value):

        self.cmd.send('SET_DAC_HARD',value)


    ## Change the dac value performing a ramp
    # @param value The new dac value
    def setDacSoft(self,value):

        self.cmd.send('SET_DAC_SOFT',value)


    ## Set the dac ramp parameters
    # @param dacStep The number of steps to perform every 'T6' microseconds
    # @param t6TickNum The number ofs 'T6'you have to wait before tacking another step
    def setRamp(self,dacStep,t6TicksTum):

        self.cmd.send('SET_DACSTEP',dacStep)
        self.cmd.send('SET_NUMT6TRIG',t6TicksTum)


    ## Set the ramp sign
    # @param value The wanted speed sign (0 = positive, 1 = negative)
    def setRampSign(self,value):

        self.cmd.send('SET_RAMPSIGN',value)


    ## Set the PI feedback integral gain
    # @param value The new integral gain
    def setI(self,value):

        self.cmd.send('SET_IGAIN',value)

    ## Set the PI feedback proportional gain
    # @param value The new proportional gain
    def setP(self,value):

        self.cmd.send('SET_PGAIN',value)


    ## Set the PI feedback set point
    # @param value The new set point in Volt
    def setSetPoint(self,value):

        self.cmd.send('SET_SETPOINT',value)


    ## Set the ADC stop trigger
    # @param value The stop trigger value in Volt for the deflection
    # @param sign 0 = greathern than, 1 = less than
    def setADCStopTrig(self,value,sign):

        self.cmd.send('SET_FTRIG',[value,sign])


    ## Set the DAC stop trigger
    # @param value The stop trigger value in Volt for the z position
    # @param sign 0 = greathern than, 1 = less than
    def setDACStopTrig(self,value,sign):

        self.cmd.send('SET_ZTRIG',[value,sign])


    ## Set the time stop trigger
    # @param value The time stop trigger value in microseconds
    # @param sign 0 = greathern than, 1 = less than
    def setTimeStopTrig(self,value,sign):

        self.cmd.send('SET_TIMETRIG',[value,sign])

    ## Set which trigger you want to use
    # @param t 1 = time trigger in use, 0 = time trigger not in use
    # @param d 1 = dac trigger in use, 0 = dac trigger not in use
    # @param a 1 = adc trigger in use, 0 = adc trigger not in use
    def setTriggersSwitch(self,t,d,a):

        self.cmd.send('SET_TRIGGERS',[a,d,t])


    ## Start a particular state in safe mode
    # @param state The state you want to start. 1
    def startSafeState(self,state,init):

        self.cmd.send('SET_MODSAFE',[state,init])


    ## Turns on the feedback
    def feedbackOn(self):

        self.cmd.send('SET_MODEDBG',2)


    ## Brings he system to the "rest" state
    def goToRest(self):

        self.startSafeState(0,1)

