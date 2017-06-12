package neur.camera;

import java.awt.image.BufferedImage;
import java.io.IOException;
import java.net.UnknownHostException;

public interface ICamera
{
  public void init () throws UnknownHostException, IOException;
  
  public void close () throws IOException;
  
  public void checkFps ();
  
  public BufferedImage getImage () throws IOException;
  
  public BufferedImage cropImage (BufferedImage image);
}
