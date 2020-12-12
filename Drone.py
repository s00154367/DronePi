import MPU6050 
import time
import keyboard
import RPi.GPIO as GPIO

defaultXYZ = [0 , 0 , 1 , 0 , 0 , 0] # Calibration save Accel X,Y,Z Gyro X,Y,Z
defAltSpd = 50

GPIO.setmode(GPIO.BOARD)   

# Set up GPIO to L293d Mapping 
Motor1in1 = 16 #IN2  
Motor1in2 = 18 #IN1
Motor1E = 22 #EN1
Motor2in1 = 13 #IN3  
Motor2in2 = 11 #IN4
Motor2E = 15 #EN2

mpu = MPU6050.MPU6050()     # instantiate a MPU6050 class object
accel = [0]*3               # define an arry to store accelerometer data
gyro = [0]*3                # define an arry to store gyroscope data

GPIO.setwarnings(False)
GPIO.setup(Motor1in1,GPIO.OUT)
GPIO.setup(Motor1in2,GPIO.OUT)
GPIO.setup(Motor1E,GPIO.OUT)
GPIO.setup(Motor2in1,GPIO.OUT)
GPIO.setup(Motor2in2,GPIO.OUT)
GPIO.setup(Motor2E,GPIO.OUT)

    #Motor 1 X+
global m1p
global m1pwr
m1p = GPIO.PWM(Motor1E, 10000)
m1pwr = defAltSpd
m1p.start(m1pwr)
   
    #Motor 2 X-
global m2p
global m2pwr
m2p = GPIO.PWM(Motor2E, 10000)
m2pwr = defAltSpd
m2p.start(m2pwr)

    #Motor 3 Y+
global m3p
global m3pwr
m3p = GPIO.PWM(Motor3E, 10000)
m3pwr = defAltSpd
m3p.start(m3pwr)

    #Motor 4 Y-
global m4p
global m4pwr
m4p = GPIO.PWM(Motor4E, 10000)
m4pwr = defAltSpd
m4p.start(m4pwr)

def setup():
    mpu.dmp_initialize()    # initialize MPU6050
def getAlt():
    #Get and return the curent Altitude

def calibrate():
    #Set default values for the drone
    accel = mpu.get_acceleration()      # get accelerometer data
    gyro = mpu.get_rotation()
    defaultXYZ = [accel[0]/16384.0,accel[1]/16384.0,accel[2]/16384.0,gyro[0]/131.0, gyro[1]/131.0, gyro[2]/131.0]
def findDirection():
    #Find out which direct the Drone is facing
    accel = mpu.get_acceleration()      # get accelerometer data
    gyro = mpu.get_rotation()
    CurAccX = accel[0]/16384.0
    CurAccY = accel[1]/16384.0
    if CurAccX > defaultXYZ[0] and CurAccY > defaultXYZ[1]:
        print('Moving Forward')
    if CurAccX < defaultXYZ[0] and CurAccY < defaultXYZ[1]:
        print('Moving Backward')
    if CurAccX < defaultXYZ[0] and CurAccY > defaultXYZ[1]:
        print('Moving Left')
    if CurAccX > defaultXYZ[0] and CurAccY < defaultXYZ[1]:
        print('Moving Right')
def Stationary():
    defAlt = getAlt()
    curSpd = defAltSpd
    while True:
        if getAlt() > defAlt:
            curSpd += 5
        elif getAlt() < defAlt:
            curSpd -= 5
        elif getAlt() == defAlt:
            defAltSpd = curSpd
        motorX1(curSpd)
        motorY1(curSpd)
        motorX2(curSpd)
        motorY2(curSpd)
        
def MoveForward():
    motorX1(40)
    motorY1(40)
    motorX2(60)
    motorY2(60)
def MoveBackward():
    motorX1(60)
    motorY1(60)
    motorX2(40)
    motorY2(40)
    
def liftoff():
    motorX1(80)
    motorY1(80)
    motorX2(80)
    motorY2(80)
    
    time.sleep(5)
    
    motorX1(defAltSpd)
    motorY1(defAltSpd)
    motorX2(defAltSpd)
    motorY2(defAltSpd)
    
    
def motorX1(speed):
    #Turn X+ on to "speed"
    m1p.start(speed)
    GPIO.output(Motor1in1,GPIO.HIGH)
    GPIO.output(Motor1in2,GPIO.LOW)
    print('X+ Speed' + speed)
    
def motorX2(speed):
    #Turn X- on to "speed"
    m2p.start(speed)
    GPIO.output(Motor2in1,GPIO.HIGH)
    GPIO.output(Motor2in2,GPIO.LOW)
    print('X- Speed' + speed)
    
def motorY1(speed):
    #Turn Y+ on to "speed"
    m1p.start(speed)
    GPIO.output(Motor1in1,GPIO.HIGH)
    GPIO.output(Motor1in2,GPIO.LOW)
    print('Y+ Speed' + speed)
    
def motorY2(speed):
    #Turn Y- on to "speed"
    m1p.start(speed)
    GPIO.output(Motor1in1,GPIO.HIGH)
    GPIO.output(Motor1in2,GPIO.LOW)    
    print('Y- Speed' + speed)
        
def loop():
    
    while(True):
        accel = mpu.get_acceleration()      # get accelerometer data
        gyro = mpu.get_rotation()           # get gyroscope data
        '''
        print("a/g:%d\t%d\t%d\t%d\t%d\t%d "%(accel[0],accel[1],accel[2],gyro[0],gyro[1],gyro[2]))
        print("a/g:%.2f g\t%.2f g\t%.2f g\t%.2f d/s\t%.2f d/s\t%.2f d/s"%(accel[0]/16384.0,accel[1]/16384.0,
            accel[2]/16384.0,gyro[0]/131.0,gyro[1]/131.0,gyro[2]/131.0))
        time.sleep(1)
        '''
        findDirection()
        time.sleep(1)
        
        
        
if __name__ == '__main__':     # Program entrance
    print("Program is starting ... ")
    setup()
    calibrate()
    try:
        loop()
    except KeyboardInterrupt:  # Press ctrl-c to end the program.
        pass

