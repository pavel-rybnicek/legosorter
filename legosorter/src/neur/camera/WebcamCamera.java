package neur.camera;

import java.awt.image.BufferedImage;
import java.util.List;

import com.github.sarxos.webcam.Webcam;

public class WebcamCamera implements ICamera
{
  Webcam webcam = null;

  @Override
  public void close()
  {
    webcam.close();

  }

  @Override
  public void init()
  {
    List<Webcam> webcams = Webcam.getWebcams();

    webcam = webcams.get(1);

    webcam.open();
  }

  @Override
  public void checkFps()
  {
    double fps = webcam.getFPS();
    
    System.out.println("FPS: " + fps);
    
    if (Double.compare(fps, 20) < 0 && Double.compare(fps, 0) > 0)
    {
      throw new RuntimeException ("Nizká framerate, patrně špatné světlo.");
    } 
    
  }

  @Override
  public BufferedImage getImage()
  {
    return webcam.getImage();
  }

  @Override
  public BufferedImage cropImage(BufferedImage image)
  {
    int width = image.getWidth();
    int height = image.getHeight();

    BufferedImage imageCropped = image.getSubimage(width / 3, height / 3,
        width / 3, height / 3);
    
    return imageCropped;
  }

}
