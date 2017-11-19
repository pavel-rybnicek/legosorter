package neur.nnet;

import java.awt.image.BufferedImage;
import java.util.HashMap;
import java.util.Iterator;
import java.util.Map;

import org.neuroph.core.NeuralNetwork;
import org.neuroph.imgrec.ImageRecognitionPlugin;

public class NeurophNNet implements INNet
{
  protected NeuralNetwork nnet = null;
  protected ImageRecognitionPlugin imageRecognition = null;

  @Override
  public void init(String nnetFile)
  {
    // load trained neural network saved with Neuroph Studio (specify some
    // existing neural network file here)
    nnet = NeuralNetwork.load(nnetFile);

    // get the image recognition plugin from neural network
    imageRecognition = (ImageRecognitionPlugin) nnet
        .getPlugin(ImageRecognitionPlugin.class);

  }

  @Override
  public String evaluateImage(BufferedImage image)
  {
    // image recognition is done here
    HashMap<String, Double> outputMap = imageRecognition
        .recognizeImage(image);

    String resultString = "";
    Double resultValue = new Double(0);

    Iterator<Map.Entry<String, Double>> it = outputMap.entrySet().iterator();
    while (it.hasNext())
    {
      Map.Entry<String, Double> pair = it.next();

      if (resultValue.compareTo(pair.getValue()) < 0)
      {
        resultValue = pair.getValue();
        resultString = pair.getKey();
      }
    }

    int resultValueInt = (int) (resultValue * 100);

    if (10 > resultValueInt)
    {
      resultString = "no";
    }
    else if (90 > resultValueInt)
    {
      resultString = "unknown";
    }

    return resultString + "_" + resultValueInt;
  }

}
