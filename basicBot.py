 

from ev3dev2.motor import LargeMotor, MediumMotor, MotorSet, MoveTank, MoveSteering
from ev3dev2.motor import OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D
from ev3dev2.sensor.lego import TouchSensor, UltrasonicSensor, GyroSensor, ColorSensor
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4


class BasicBot(object):
    """This provides a higher-level interface to Lego robot we've been working
    with."""

    # ---------------------------------------------------------------------------
    # Setup methods, including constructor
    LEFT_MOTOR = 'leftMotor'
    RIGHT_MOTOR = 'rightMotor'
    SERVO_MOTOR = 'servoMotor'
    LEFT_TOUCH = 'left'
    RIGHT_TOUCH = 'right'

    def __init__(self, robotName):
        """Takes in a string, the name of the robot."""
        self.name = robotName
        self.stringToPort = {'outa': OUTPUT_A, 'outb': OUTPUT_B, 'outc': OUTPUT_C, 'outd': OUTPUT_D,
                             'in1': INPUT_1, 'in2': INPUT_2, 'in3': INPUT_3, 'in4': INPUT_4}
        self.setMotorPort(self.LEFT_MOTOR, 'outD')
        self.setMotorPort(self.RIGHT_MOTOR, 'outB')
        self.tankMovement = MoveTank(OUTPUT_D, OUTPUT_B)
        self.steerMovement = MoveSteering(OUTPUT_D, OUTPUT_B)
        self.servoMotor = None
        self.leftTouch = None
        self.rightTouch = None
        self.ultraSensor = None
        self.colorSensor = None
        self.gyroSensor = None

    def _convertPortString(self, strng):
        """Takes a string and converts it to the proper port descriptor."""
        try:
            port =  self.stringToPort[strng.lower()]
            return port
        except:
            print("Invalid port string:", strng)
            return None


    def setMotorPort(self, side, portString):
        """Takes in which side and which port, and changes the correct variable
        to connect to that port. Assumes port is a string 'outA', 'outB', 'outC', 'outD', which
        are then converted to the expected values."""
        port = self._convertPortString(portString)
        if side == self.LEFT_MOTOR:
            self.leftMotor = LargeMotor(port)
            self.leftMotor.stop_action = 'brake'
        elif side == self.RIGHT_MOTOR:
            self.rightMotor = LargeMotor(port)
            self.rightMotor.stop_action = 'brake'
        elif side == self.SERVO_MOTOR:
            self.servoMotor = MediumMotor(port)
        else:
            print("Incorrect motor description:", side)


    def setTouchSensor(self, side, portString):
        """Takes in which side and which port, and changes the correct
        variable to connect to that port."""
        port = self._convertPortString(portString)
        if side == self.LEFT_TOUCH:
            self.leftTouch = TouchSensor(port)
        elif side == self.RIGHT_TOUCH:
            self.rightTouch = TouchSensor(port)
        else:
            print("Incorrect touch sensor description:", side)


    def setColorSensor(self, portString):
        """Takes in the port for the color sensor and updates object"""
        port = self._convertPortString(portString)
        self.colorSensor = ColorSensor(port)


    def setUltrasonicSensor(self, portString):
        """Takes in the port for the ultrasonic sensor and updates object"""
        port = self._convertPortString(portString)
        self.ultraSensor = UltrasonicSensor(port)


    def setGyroSensor(self, portString):
        """Takes in the port for the gyro sensor and updates object"""
        port = self._convertPortString(portString)
        self.gyroSensor = GyroSensor(port)


    # ---------------------------------------------------------------------------
    # Methods to read sensor values

    def readTouch(self):
        """Reports the value of both touch sensors, OR just one if only one is connected, OR
        prints an alert and returns nothing if neither is connected.
        Note that the values are 1 if the sensor has been touched, and 0 otherwise."""
        if self.leftTouch is not None and self.rightTouch is not None:
            return self.leftTouch.is_pressed, self.rightTouch.is_pressed
        elif self.leftTouch is not None:
            return self.leftTouch.is_pressed, None
        elif self.rightTouch is not None:
            return None, self.rightTouch
        else:
            print("Warning, no touch sensor connected")
            return None, None

    def readUltra(self):
        """Reports the value of the ultrasonic sensor in centimeters, OR prints an alert
        and returns none if it is not connected."""
        if self.ultraSensor is not None:
            cmData = self.ultraSensor.distance_centimeters
            return cmData
        else:
            print("Warning, no ultrasonic sensor connected")
            return None

    def readReflect(self):
        """Reports the value of the color sensor's reflectance value. This value represents a percentage
        of the possible range of values, so is a number between 0.0 and 1.0 (or is it 0 to 100?)"""
        if self.colorSensor is not None:
            reflData = self.colorSensor.reflected_light_intensity
            return reflData
        else:
            print("Warning, no color sensor connected")
            return None


    def readAmbientLight(self):
        """Reports the ambient light value from the color sensor. This value represents a percentage
        of the possible range of values, so is a number between 0.0 and 1.0 (or is it 0 to 100?)"""
        if self.colorSensor is not None:
            ambientData = self.colorSensor.ambient_light_intensity
            return ambientData
        else:
            print("Warning, no color sensor connected")
            return None

    def readColor(self):
        """Reports the color detected by the color sensor, the integers between 0 and 7:
        0: No color, 1: Black, 2: Blue, 3: Green, 4: Yellow, 5: Red, 6: White, 7: Brown."""
        if self.colorSensor is not None:
            colorData = self.colorSensor.color
            return colorData
        else:
            print("Warning, no color sensor connected")
            return None

    def readRGBColor(self):
        """Reports the RGB values detected by the color sensor, in the range from
        0 to 255. Note that the reported value is between 1020, so this converts it to
        the typical RGB range."""
        if self.colorSensor is not None:
            color = self.colorSensor.rgb
            # redVal = int((self.colorSensor.red / 1020) * 255)
            # greenVal = int((self.colorSensor.green / 1020) * 255)
            # blueVal = int((self.colorSensor.blue / 1020) * 255)
            return color # (redVal, greenVal, blueVal)
        else:
            print("Warning, no color sensor connected")
            return None

    def readGyroAngle(self):
        """Reports the angle in degrees the Gyro sensor has detected that the robot has turned since
        starting up. """
        if self.gyroSensor is not None:
            angleData = self.gyroSensor.angle
            return angleData
        else:
            print("Warning, no gyro sensor connected")
            return None

    def calibrateWhite(self):
        """Calls the underlying calibrate_white method, which adjusts reported RGB colors
        so that they max out at the given color."""
        if self.colorSensor is not None:
            self.colorSensor.calibrate_white()
        else:
            print("Warning, no color sensor connected")
            return None


    # ---------------------------------------------------------------------------
    # Methods to move robot

    def forward(self, speed, runTime=None):
        """Takes in a speed between -100.0 and 100.0 inclusively, and an optional
        time to run (in seconds) and it sets the motors so the robot moves straight forward
        at that speed. This method blocks if a time is specified."""
        assert -100.0 <= speed <= 100.0
        assert self.leftMotor is not None
        assert self.rightMotor is not None
        if runTime is None:
            self.tankMovement.on(speed, speed)
        else:
            self.tankMovement.on_for_seconds(speed, speed, runTime)



    def backward(self, speed, runTime=None):
        """Takes in a speed between -100.0 and 100.0 inclusively, and an optional
        time to run (in seconds) and it sets the motors so the robot moves straight forward
        at that speed. This method blocks if a time is specified."""
        assert -100.0 <= speed <= 100.0
        assert self.leftMotor is not None
        assert self.rightMotor is not None
        self.forward(-speed, runTime)


    def turnLeft(self, speed, runTime=None):
        """Takes in a speed between -100.0 and 100.0 inclusively, and an optional time
        to run (in seconds) and it sets the motors so the robot turns left in place at
        the given speed. This method blocks if a time is specified until the movement 
        is complete."""
        assert -100.0 <= speed <= 100.0
        assert self.leftMotor is not None
        assert self.rightMotor is not None
        if runTime is None:
            self.steerMovement.on(-100, speed)
        else:
            self.steerMovement.on_for_seconds(-100, speed)

            
    def turnRight(self, speed, runTime=None):
        """Takes in a speed between -100.0 and 100.0 inclusively, and an optional time
        to run (in seconds) and it sets the motors so the robot turns right in place at
        the given speed. This method blocks if a time is specified until the movement 
        is complete."""
        assert -100.0 <= speed <= 100.0
        assert self.leftMotor is not None
        assert self.rightMotor is not None
        if runTime is None:
            self.steerMovement.on(100, speed)
        else:
            self.steerMovement.on_for_seconds(100, speed, runTime)


    def stop(self):
        """Turns off the motors and blocks until they have stopped moving."""
        assert self.leftMotor is not None
        assert self.rightMotor is not None
        self.tankMovement.off()


    def motorCurve(self, leftSpeed, rightSpeed, runTime=None):
        """Takes in two speeds, left motor and right motor speeds, both between
        -1.0 and 1.0 inclusively, and an optional time in seconds for the motors to run.
        It sets the speeds appropriately and runs just like the other movement methods,
        just with different speeds set on each motor. Blocks if a time is specified."""
        assert self.leftMotor is not None
        assert self.rightMotor is not None
        assert -100.0 <= leftSpeed <= 100.0
        assert -100.0 <= rightSpeed <= 100.0
        if runTime is None:
            self.tankMovement.on(leftSpeed, rightSpeed)
        else:
            self.tankMovement.on_for_seconds(leftSpeed, rightSpeed, runTime)


    def steerCurve(self, steerVal, speed, runTime=None):
        """Takes in a steering value that ranges from -100 (turn left on the spot), to 0, (go straight), to
        +100 (turn right on the spot), and it takes a speed for the overall movement (between -100.0 and 100.0).
        Also takes in an optional time in seconds for the motors to run."""
        assert self.leftMotor is not None
        assert self.rightMotor is not None
        assert -100.0 <= steerVal <= 100.0
        assert -100.0 <= speed <= 100.0
        if runTime is None:
            self.steerMovement.on(steerVal, speed)
        else:
            self.steerMovement.on_for_seconds(steerVal, speed, runTime)



            
# Sample of how to use this
if __name__ == "__main__":
    testRobot = BasicBot("Tonks")
    # ev3.Sound.speak("Moving")
    # ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.AMBER)
    # ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.GREEN)
    # testRobot.forward(75.0, 1.0)
    # testRobot.backward(75.0, 0.5)
    # testRobot.turnRight(40.0, 1.0)
    # testRobot.motorCurve(10.0, 60.0, 1.0)
    testRobot.steerCurve(-30, 50.0, 1.0)
    # ev3.Leds.all_off()
