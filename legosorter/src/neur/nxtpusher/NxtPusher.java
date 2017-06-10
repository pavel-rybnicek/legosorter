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
public class NxtPusher implements IPusher
{

  private NXTConnector conn = null;

  private TouchSensor touchSensor = null;
  
  private final String PUSHER1 = "green";
  private final String PUSHER2 = "blue";
  private final String PUSHER3 = "red";

  public void push(String eventName) throws Exception
  {
    switch (eventName)
    {
    case PUSHER1:
      Motor.A.rotate(360);
      break;

    case PUSHER2:
      Motor.B.rotate(360);
      break;

    case PUSHER3:
      Motor.C.rotate(360);
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
      delay = 800;
      break;

    case PUSHER2:
      delay = 1800;
      break;

    case PUSHER3:
      delay = 2800;
      break;
    }

    return delay;
  }
}