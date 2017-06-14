package neur.nxtpusher;

public class PusherFactory
{
  public enum PusherType
  {
    NXTPUSHER, NXTDOUBLEPUSHER, VIRTUAL_PUSHER;
  }
  
  
  public static IPusher getPusher (PusherType pusherType)
  {
    switch (pusherType)
    {
    case NXTPUSHER:
      return new NxtPusher ();
    case NXTDOUBLEPUSHER:
      return new NxtDoublePusher ();
    case VIRTUAL_PUSHER:
      return new VirtualPusher();
    }
    
    return null;
  }

}
