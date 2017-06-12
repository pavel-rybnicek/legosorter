package neur.camera;

public class CameraFactory
{
  public enum Cam
  {
    GENIUS, RASPBERRY;
  }
  
  
  public static ICamera getCamera (Cam cameraType)
  {
    switch (cameraType)
    {
    case GENIUS:
      return new WebcamCamera ();
     
    case RASPBERRY:
      return new PiCamera();
    }
    
    return null;
  }

}
