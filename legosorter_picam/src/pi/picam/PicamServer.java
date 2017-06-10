package pi.picam;

import java.awt.image.BufferedImage;
import java.io.IOException;
import java.text.DateFormat;
import java.text.SimpleDateFormat;
import java.util.Date;

import com.hopding.jrpicam.RPiCamera;
import com.hopding.jrpicam.enums.Exposure;
import com.hopding.jrpicam.exceptions.FailedToRunRaspistillException;

public class PicamServer {

	public static void main(String[] args) throws FailedToRunRaspistillException, IOException, InterruptedException 
	{
		// Create a Camera that saves images to the Pi's Pictures directory.
		RPiCamera piCamera = new RPiCamera("/home/pi/Pictures");
		piCamera.takeStill("An Awesome Pic.jpg");	
		
		piCamera.setWidth(500).setHeight(500) // Set Camera to produce 500x500 images.
	    .setBrightness(75)                // Adjust Camera's brightness setting.
	    .setExposure(Exposure.AUTO)       // Set Camera's exposure.
	    .setTimeout(2)                    // Set Camera's timeout.
	    .setAddRawBayer(true);            // Add Raw Bayer data to image files created by Camera.
	// Sets all Camera options to their default settings, overriding any changes previously made.
	piCamera.setToDefaults();
	
	DateFormat dateFormat = new SimpleDateFormat("yyyy/MM/dd HH:mm:ss");
	
	Date date = new Date();
	System.out.println(dateFormat.format(date));
	BufferedImage image = piCamera.takeBufferedStill();
	date = new Date();
	System.out.println(dateFormat.format(date));
	 piCamera.takeBufferedStill();
	date = new Date();
	System.out.println(dateFormat.format(date));
	 piCamera.takeBufferedStill();
	date = new Date();
	System.out.println(dateFormat.format(date));
	}

}
