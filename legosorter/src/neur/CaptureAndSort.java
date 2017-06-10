package neur;

import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;
import java.util.Date;

import javax.imageio.ImageIO;

import neur.camera.CameraFactory;
import neur.camera.CameraFactory.Cam;
import neur.camera.ICamera;
import neur.nnet.INNet;
import neur.nnet.NNetFactory;
import neur.nnet.NNetFactory.NNetType;
import neur.nxtpusher.PushQueue;

public class CaptureAndSort
{
  private final static String OUTPUT_PATH = "C:/data/LEGO/legosorter/ColorsWhiteBackground/test";

  private final static String NET_PATH = "C:/data/LEGO/legosorter/neuroph/NeurophProject/Neural Networks";

  final static String NET_FILE = "ColorsWhiteBackgroundSmes.nnet";

  final static Cam cameraType = Cam.GENIUS;

  private static boolean exit = false;

  private static ICamera camera = null;

  private static INNet nnet = null;
  
  private static PushQueue pushQueue = new PushQueue();

  public static void main(String[] args) throws Exception
  {
    // spustime frontu mechanickeho trideni
    (new Thread(pushQueue)).start();

    // inicializujeme neuronovou sit
    nnet = NNetFactory.getNNet(NNetType.NEUROPH);
    nnet.init(NET_PATH + "/" + NET_FILE);

    // inicializujeme kameru
    camera = CameraFactory.getCamera(cameraType);
    camera.init();

    // spustime hlavni smycku
    try
    {
      processImages();
    } finally
    {
      camera.close();
      System.out.println("Kamera - končím.");
    }
  }

  private static void processImages() throws Exception
  {
    long i = new Date().getTime();

    while (!exit)
    {
      if (i % 100 == 0)
      {
        camera.checkFps();
      }

      BufferedImage image = camera.getImage();

      BufferedImage imageCropped = camera.cropImage(image);

      String result = nnet.evaluateImage(imageCropped);

      i++;
      
      String eventName = result.substring(0, result.indexOf('_'));

      if ("no".equals(eventName) || "unknown".equals(eventName))
      {
        continue;
      }

      pushQueue.addEvent(eventName);

      saveImage(result, i, imageCropped);
    }
  }

  private static void saveImage(String color, long i, BufferedImage image)
      throws IOException
  {

    String fileName = color + "_img" + i + ".png";

    System.out.println(fileName);

    ImageIO.write(image, "PNG", new File(OUTPUT_PATH + "/" + fileName));
  }

  public static boolean isExit()
  {
    return exit;
  }

  public static void setExit(boolean exit)
  {
    CaptureAndSort.exit = exit;
  }

}
