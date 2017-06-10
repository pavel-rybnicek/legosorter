package neur;

import java.io.File;
import java.io.IOException;
import java.util.HashMap;
import java.util.Iterator;
import java.util.Map;

import org.neuroph.core.NeuralNetwork;
import org.neuroph.imgrec.ImageRecognitionPlugin;

public class Legosorter {
	private final static String  SORT_PATH = "C:/data/LEGO/legosorter/3/test";
	
	private final static String NET_PATH = "C:/data/LEGO/legosorter/neuroph/NeurophProject/Neural Networks";

	final static String NET_FILE = "GreenRedYellowWhite.nnet";

	public static void main(String[] args) throws IOException {
		testNet();
	}

	private static void testNet() throws IOException {
		String path = SORT_PATH;
		File folder = new File (path);
		
		    // load trained neural network saved with Neuroph Studio (specify some existing neural network file here)
		    NeuralNetwork nnet = NeuralNetwork.load(NET_PATH + "/" + NET_FILE); // load trained neural network saved with Neuroph Studio
		    // get the image recognition plugin from neural network
		    ImageRecognitionPlugin imageRecognition = (ImageRecognitionPlugin)nnet.getPlugin(ImageRecognitionPlugin.class); // get the image recognition plugin from neural network

	    for (final File fileEntry : folder.listFiles()) {
	
		         // image recognition is done here (specify some existing image file)
		        HashMap<String, Double> output = imageRecognition.recognizeImage(fileEntry);
		        System.out.println(fileEntry.getName() + " " + evaluate(output, fileEntry));
		}
	}
	
	private static String evaluate (HashMap<String, Double> map, File imgFile) throws IOException
	{
		String resultString = "";
		Double resultValue = new Double(0);
		
		Iterator<Map.Entry<String, Double>> it = map.entrySet().iterator();
	    while (it.hasNext()) {
	        Map.Entry<String, Double> pair = it.next();
	        
	        if (resultValue.compareTo(pair.getValue()) < 0)
	        {
	        	resultValue = pair.getValue();
	        	resultString = pair.getKey();
	        }
	    }
	    
	    int resultValueInt = (int) (resultValue*100);
	
	    if (90 > resultValueInt)
	    {
	    	resultString = "unknown";
	    }

	    renameImage (resultString, imgFile);
	    
	    return resultString + " " + resultValueInt;
	    		
	}
	
	private static void renameImage(String color, File imgFile) throws IOException {
		

	    	String fileName = imgFile.getName();
	    	String baseFileName = fileName.substring(fileName.indexOf("img"));
	    	
	    	imgFile.renameTo(new File(SORT_PATH + "/" + color + "_" + baseFileName));
	    
	}

}
