package neur.nxtpusher;

import java.io.IOException;

/**
 * Nedela vubec nic, vyuziva se pri sberu obrazku.
 */
public class VirtualPusher implements IPusher
{

  public void push(String eventName) throws Exception
  {
  }

  public void init()
  {
    System.out.println("Pouze virtuální pusher, fyzicky se netřídí");
  }

  public boolean checkClose() throws IOException
  {
    return false;
  }

  @Override
  public void close() throws IOException
  {
  }
  
    @Override
  public int getEventDelay(String eventName)
  {
    return 0;
  }
}