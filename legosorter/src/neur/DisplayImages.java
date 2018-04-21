package neur;

import java.awt.BorderLayout;
import java.awt.image.BufferedImage;

import javax.swing.ImageIcon;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.WindowConstants;

import neur.camera.CameraFactory;
import neur.camera.CameraFactory.Cam;
import neur.camera.ICamera;

/**
 * Zobrazuje aktuální obrázek z kamery.
 * 
 */
public class DisplayImages
{
  private ICamera camera = null;

  private Cam cameraType = Cam.RASPBERRY;

  public static void main(String[] args) throws Exception
  {
    new DisplayImages();
  }

  public DisplayImages() throws Exception
  {
    // inicializujeme kameru
    camera = CameraFactory.getCamera(cameraType);
    camera.init();

    try
    {
      JFrame editorFrame = new JFrame("Image Demo");
      editorFrame.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE);
        editorFrame.setVisible(true);

      BufferedImage image = null;
      BufferedImage imageCropped = null;

      for (;;)
      {
        image = camera.getImage();
        // subimage pro bílou plochu je (70, 0, 500, 110);
        imageCropped = image.getSubimage(250, 180, 149, 149);
        ImageIcon imageIcon = new ImageIcon(imageCropped);
        JLabel jLabel = new JLabel();
        jLabel.setIcon(imageIcon);
        editorFrame.getContentPane().removeAll();
        editorFrame.getContentPane().add(jLabel, BorderLayout.CENTER);

        editorFrame.pack();
      }
    }
    finally
    {
    camera.close();
    }
  }
}