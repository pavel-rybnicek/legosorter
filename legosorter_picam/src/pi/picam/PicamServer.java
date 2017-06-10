package pi.picam;

import java.io.IOException;

import com.hopding.jrpicam.RPiCamera;
import com.hopding.jrpicam.exceptions.FailedToRunRaspistillException;

public class PicamServer {

	public static void main(String[] args) throws FailedToRunRaspistillException, IOException, InterruptedException 
	{
		// Create a Camera that saves images to the Pi's Pictures directory.
		RPiCamera piCamera = new RPiCamera("/home/pi/Pictures");
		piCamera.takeStill("An Awesome Pic.jpg");	
	}

}
