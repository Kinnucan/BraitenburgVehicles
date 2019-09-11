

from basicBot import BasicBot
from ev3dev2.button import Button
from ev3dev2.led import Leds
from ev3dev2.sound import Sound

import time

def testButton(myRobot):
    bttn = Button()
    print("Starting while loop")
    while not bttn.left:
        print("Waiting...")
        time.sleep(0.1)

def testLed(myRobot):
    snd = Sound()
    snd.beep()
    leds = Leds()
    print("All off...")
    leds.all_off()
    time.sleep(2.0)
    snd.speak("Amber...", play_type=1)
    leds.set_color("LEFT", 'AMBER')
    leds.set_color("RIGHT", "AMBER")
    time.sleep(2.0)
    print("Left full on , right half red all green...")
    snd.play_file("GoatBah.wav", play_type=1)
    for i in range(6):
        x = i / 6
        print(i, x)
        leds.set_color("LEFT", (x, 1))
        leds.set_color("RIGHT", [0, 1.0])
        time.sleep(1.0)
    leds.all_off()
    starSong = [('C4', 'q'), ('C4', 'q'), ('G4', 'q'), ('G4', 'q'),
                ('A4', 'q'), ('A4', 'q'), ('G4', 'h'),
                ('F4', 'q'), ('F4', 'q'), ('E4', 'q'), ('E4', 'q'),
                ('D4', 'q'), ('D4', 'q'), ('C4', 'h')]
    snd.play_song(starSong)


def testColor(myRobot):
    myRobot.setColorSensor('in1')
    val = 100
    while True:
        val = myRobot.readReflect()
        print("Color", val)
        if val < 5:
            break
    myRobot.stop()
    print("Done")

def testWithCalibrate(myRobot):
    print("Place sensor close to brightest white")
    bttn = Button()
    bttn.wait_for_bump('enter')
    myRobot.calibrateWhite()
    testOtherColor(myRobot)


def testOtherColor(myRobot):
    myRobot.setColorSensor('in1')
    for i in range(100):
        # color = myRobot.readAmbientLight()
        # color = myRobot.readColor()
        color = myRobot.readRGBColor()
        print("Color =", color)
        time.sleep(0.5)


def testUltra(myRobot):
    myRobot.setUltrasonicSensor('in4')
    bttn = Button()

    while not bttn.any():
        ult = myRobot.readUltra()
        print("Ultra value:", ult)


def testGyro(myRobot):
    myRobot.setGyroSensor('in2')
    bttn = Button()

    while not bttn.any():
        print("turn robot...", myRobot.readGyroAngle())
    rot = myRobot.readGyroAngle()
    while abs(rot) > 10:
        print(".... rot = ", rot)
        if rot < 0:
            rotSpeed = 30
        else:
            rotSpeed = -30
        print("rotSpeed = ", rotSpeed)
        myRobot.turnRight(rotSpeed, 0.2)
        rot = myRobot.readGyroAngle()
    print("DONE")


if __name__ == '__main__':
    myRobot = BasicBot("Tonks")
    # testColor(myRobot)
    # testUltra(myRobot)
    # testGyro(myRobot)
    # testOtherColor(myRobot)
    # testButton(myRobot)
    # testLed(myRobot)
    testWithCalibrate(myRobot)