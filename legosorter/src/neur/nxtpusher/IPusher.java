package neur.nxtpusher;

import java.io.IOException;

public interface IPusher
{
  public void init();
  
  public void close() throws IOException;

  public boolean checkClose() throws IOException;
  
  public void push(String eventName) throws Exception;
  
  public int getEventDelay (String eventName);
}
