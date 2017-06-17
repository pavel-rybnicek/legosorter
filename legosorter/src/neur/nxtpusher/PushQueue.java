package neur.nxtpusher;

import java.io.IOException;
import java.util.Date;
import java.util.concurrent.ConcurrentSkipListSet;

import neur.nxtpusher.PusherFactory.PusherType;

public class PushQueue implements Runnable
{
  private int WINDOW_SIZE = 50;
  
  private PusherType pusherType = PusherType.NXTDOUBLEPUSHER;

  private static ConcurrentSkipListSet<PushEvent> queue = new ConcurrentSkipListSet<PushEvent>();
  
  private IPusher pusher = null;

  private void processQueue() throws Exception
  {
    while (!pusher.checkClose())
    {
      PushEvent firstEvent = queue.pollFirst();

      if (null == firstEvent)
      {
        Thread.sleep(WINDOW_SIZE);
        continue;
      }

      long currentTime = new Date().getTime();

      long timeToNextEvent = firstEvent.getTime() - currentTime;

      if (timeToNextEvent < 0)
      {
        continue;
      }

      if (timeToNextEvent > WINDOW_SIZE)
      {
        Thread.sleep(WINDOW_SIZE);
        queue.add(firstEvent);
        continue;
      }

      pusher.push(firstEvent.getEventName());
    }
    
    System.out.println("PushQueue - končím");
  }

  public void addEvent(String eventName)
  {
    PushEvent event = new PushEvent(new Date().getTime() + pusher.getEventDelay(eventName), eventName);
    queue.add(event);
  }

  @Override
  public void run()
  {
    try
    {
      pusher = PusherFactory.getPusher(pusherType);
      pusher.init();

      processQueue();
    } catch (Exception e)
    {
      e.printStackTrace();
    }
    finally
    {
      try
      {
        pusher.close();
      } catch (IOException e)
      {
        e.printStackTrace();
      }
    }

  }

}