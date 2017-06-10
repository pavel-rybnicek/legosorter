package neur.nnet;

import java.awt.image.BufferedImage;

public interface INNet
{
  public void init(String nnetFile);

  public String evaluateImage(BufferedImage image);
}
