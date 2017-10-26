package neur.nxtpusher;

import java.io.IOException;

import lejos.nxt.Motor;
import lejos.nxt.SensorPort;
import lejos.nxt.TouchSensor;
import lejos.nxt.remote.NXTCommand;
import lejos.pc.comm.NXTCommLogListener;
import lejos.pc.comm.NXTCommandConnector;
import lejos.pc.comm.NXTConnector;
import neur.CaptureAndSort;

/**
 *
 */
public class NxtDoublePusher implements IPusher
{
  private final int STEP = 4*36;
  
  private NXTConnector conn = null;

  private TouchSensor touchSensor = null;
  
    private final String PUSHER1 = "blue";
    private final String PUSHER2 = "white";
    private final String PUSHER3 = "green";
    private final String PUSHER4 = "yellow";
    private final String PUSHER5 = "red";
    private final String PUSHER6 = "black";

  public void push(String eventName) throws Exception
  {
    switch (eventName)
    {
    case PUSHER1:
      Motor.A.rotate(STEP);
      break;

    case PUSHER2:
      Motor.A.rotate(-STEP);
      break;

    case PUSHER3:
      Motor.B.rotate(STEP);
      break;

    case PUSHER4:
      Motor.B.rotate(-STEP);
      break;

    case PUSHER5:
      Motor.C.rotate(STEP);
      break;

    case PUSHER6:
      Motor.C.rotate(-STEP);
      break;
    }

  }

  public void init()
  {
    conn = new NXTConnector();
    conn.addLogListener(new NXTCommLogListener()
    {
      public void logEvent(String message)
      {
        System.out.println(message);
      }

      public void logEvent(Throwable throwable)
      {
        System.err.println(throwable.getMessage());
      }
    });
    conn.setDebug(true);
    if (!conn.connectTo("usb://"))
    {
      System.err.println("Failed to connect");
      System.exit(1);
    }
    NXTCommandConnector.setNXTCommand(new NXTCommand(conn.getNXTComm()));

    touchSensor = new TouchSensor(SensorPort.S1);
  }

  public boolean checkClose() throws IOException
  {
    boolean pressed = touchSensor.isPressed();
    if (pressed)
    {
      CaptureAndSort.setExit(true);
    }
    
    return pressed;
  }

  @Override
  public void close() throws IOException
  {
      conn.close();
  }


  @Override
  public int getEventDelay(String eventName)
  {
    int delay = 0;
    
    switch (eventName)
    {
    case PUSHER1:
    case PUSHER2:
      delay = 700;
      break;

    case PUSHER3:
    case PUSHER4:
      delay = 1800;
      break;

    case PUSHER5:
    case PUSHER6:
      delay = 2800;
      break;
    }

    return delay;
  }
}