package neur.nxtpusher;

/**
 * Sample to spin motors and output Tachometer counts. This sample shows how to
 * control which NXT to connect to and switch on full logging.
 * 
 * @author Lawrie Griffiths and Brian Bagnall
 *
 */
public class PushEvent implements Comparable<PushEvent>
{
  private long time;
  
  private String eventName;

  public long getTime()
  {
    return time;
  }

  public void setTime(long time)
  {
    this.time = time;
  }

  public String getEventName()
  {
    return eventName;
  }

  public void setEventName(String eventName)
  {
    this.eventName = eventName;
  }

  /**
   * @param time
   * @param eventName
   */
  public PushEvent(long time, String eventName)
  {
    super();
    this.time = time;
    this.eventName = eventName;
  }

  @Override
  public int compareTo(PushEvent o)
  {
    return (int) (this.getTime() - o.getTime());
  }
  
  
  
}