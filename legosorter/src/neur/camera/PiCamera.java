package neur.camera;

import java.awt.image.BufferedImage;
import java.io.ByteArrayInputStream;
import java.io.DataInputStream;
import java.io.File;
import java.io.IOException;
import java.io.InputStream;
import java.net.Socket;

import javax.imageio.ImageIO;

/**
 * Trivial client for the date server.
 */
public class PiCamera
{
  private static final String serverAddress = "10.27.133.8";
  private static final int PORT = 8001;

  /**
   * Runs the client as an application. First it displays a dialog box asking
   * for the IP address or hostname of a host running the date server, then
   * connects to it and displays the date that it serves.
   */
  public static void main(String[] args) throws IOException
  {
    Socket s = new Socket(serverAddress, PORT);
    getImage(s, "apokus0.png");
    getImage(s, "apokus1.png");
    getImage(s, "apokus2.png");
    getImage(s, "apokus3.png");
    getImage(s, "apokus4.png");
    getImage(s, "apokus5.png");
    getImage(s, "apokus6.png");
    getImage(s, "apokus7.png");
    getImage(s, "apokus8.png");
    getImage(s, "apokus9.png");

    s.close();

  }

  private static void getImage(Socket s, String filename) throws IOException
  {
    s.getOutputStream().write(13);

    InputStream in = s.getInputStream();
    DataInputStream dis = new DataInputStream(in);

    int length = (int) dis.readInt();
    byte[] array = new byte[length];

    dis.readFully(array);

    BufferedImage img = ImageIO.read(new ByteArrayInputStream(array));

    ImageIO.write(img, "PNG", new File(
        "C:/data/LEGO/legosorter/ColorsWhiteBackground/test/" + filename));
  }
}
