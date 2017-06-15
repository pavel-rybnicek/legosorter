package neur.camera;

import java.awt.image.BufferedImage;
import java.io.ByteArrayInputStream;
import java.io.DataInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.net.Socket;
import java.net.UnknownHostException;

import javax.imageio.ImageIO;

/**
 * Trivial client for the date server.
 */
public class PiCamera implements ICamera
{
  private static final String serverAddress = "10.27.133.8";
  private static final int PORT = 8001;

  private Socket socket = null;

  @Override
  public void init() throws UnknownHostException, IOException
  {
    socket = new Socket(serverAddress, PORT);
    
  }

  @Override
  public void close() throws IOException
  {
    socket.close();
  }

  @Override
  public void checkFps()
  {
    // u raspberry kamery nemá smysl
    
  }

  @Override
  public BufferedImage getImage() throws IOException
  {
    socket.getOutputStream().write(13);

    InputStream in = socket.getInputStream();
    DataInputStream dis = new DataInputStream(in);

    int length = (int) dis.readInt();
    byte[] array = new byte[length];

    dis.readFully(array);

    BufferedImage img = ImageIO.read(new ByteArrayInputStream(array));

    return img;
  }

  @Override
  public BufferedImage cropImage(BufferedImage image)
  {
    int width = image.getWidth();
    int height = image.getHeight();

    BufferedImage imageCropped = image.getSubimage(250, 180,
       149, 149);
    return imageCropped;
  }
}
