# coding=UTF-8
import nxt.locator
import nxt.motcont


MOTOR_ROTATION=36*5

def nxt_push(motorControl, classification):
    if not (0 <= classification < 7):
        raise ValueError ("Classification může být jen 0-5, zadáno %d" % classification)

    print('push %d' % classification)
    if 2 == classification:
        motorControl.cmd(nxt.PORT_B, 100, MOTOR_ROTATION)
    if 1 == classification:
        motorControl.cmd(nxt.PORT_B, -100, MOTOR_ROTATION)

def nxt_init():
  brick = nxt.locator.find_one_brick(debug=True)
  motorControl = nxt.motcont.MotCont(brick)
  motorControl.start()
  return brick, motorControl

