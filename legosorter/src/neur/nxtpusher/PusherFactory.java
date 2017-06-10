package neur.nxtpusher;

public class PusherFactory
{
  public enum PusherType
  {
    NXTPUSHER, NXTDOUBLEPUSHER;
  }
  
  
  public static IPusher getPusher (PusherType pusherType)
  {
    switch (pusherType)
    {
    case NXTPUSHER:
      return new NxtPusher ();
    case NXTDOUBLEPUSHER:
      return new NxtDoublePusher ();
    }
    
    return null;
  }

}
