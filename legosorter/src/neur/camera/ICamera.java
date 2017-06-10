package neur.camera;

import java.awt.image.BufferedImage;

public interface ICamera
{
  public void init ();
  
  public void close ();
  
  public void checkFps ();
  
  public BufferedImage getImage ();
  
  public BufferedImage cropImage (BufferedImage image);
}
