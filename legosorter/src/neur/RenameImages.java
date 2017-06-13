package neur;

import java.io.File;
import java.io.IOException;

public class RenameImages {

	private final static String LEARN_ROOT = "C:/data/LEGO/legosorter/picam_colors/train";

	public static void main(String[] args) throws IOException {
	  
		renameImages();
	}

	private static void renameImages() throws IOException {
		String path = LEARN_ROOT;

		File folder = new File(path);

		for (final File subdir : folder.listFiles()) {
			for (final File fileEntry : subdir.listFiles()) {

				String subdirName = subdir.getName();
				String fileName = fileEntry.getName();
				String baseFileName = fileName.substring(fileName.indexOf("img"));

				String newFileName = subdirName + "_" + baseFileName;
				
				String newFilePath = path + "/" + subdirName + "/";

				if (!fileName.equals(newFileName)) {
					forceRename(fileEntry, new File(newFilePath + newFileName));
				}

			}
		}
	}

	private static void forceRename(File source, File target) throws IOException {
		if (target.exists())
			target.delete();
		source.renameTo(target);
	}
}
