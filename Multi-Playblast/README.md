# Multi-Playblast
Multi-Playblast Tool for Maya 2022+ developed by Olivier Dral

The Multi-Playblast tool can be used to playblast 4 different cameras and combine them into 1 grid-view video. This can be useful for quickly getting a playblast of animation, with all relevant orthographic views and a perspective view. The tool also offers a big variety of display and HUD setting options.

Please note that the tool is still in development and receives active updates as it is being improved based on user feedback.

The tool is made to function for Maya 2022 or newer versions (because it uses Python 3), and uses the encoding of Quicktime.

## Installing the tool
1. Ensure that you are using Maya 2022.
2. Ensure that you have Quicktime available for Maya, you will know you have it available when in the normal Playblast menu, 'qt' is an option under 'Format'. If you do not have Quicktime for Maya, this tutorial explains how to get it: https://youtu.be/1RbUCo54MN8.
3. Download 'MultiPlayblast.py' from the Github repository.
4. Copy the 'MultiPlayblast.py' into your Maya scripts directory: MyDocuments\Maya\scripts\.
5. Open the script editor in Maya and put in the following text:
```
import MultiPlayblast

MultiPlayblast.UI()
```
6. Make this script into a button on a shelf by going to File > Save Script to Shelf.
7. Press the new made shelf button to use the tool.

## Using the Tool
1. Open the tool and create the camera layout you desire.
2. Set the various Video, Display, HUD, and File settings to your desire.
3. Saving Methods: For saving a file to a custom location, set 'Saving Method' to 'Custom Location'. This will then give you a pop-up to choose your file location and name when you press Execute, this will automatically give you a warning when you are about to override a file. For saving a file quickly to the project directory, just put in the file name, select if you want to override or not, and press Execute. This will create the file in the project/movies folder (project/images if you are using image sequence). This last method is recommended for quick iteration.

## Troubleshooting
If you have an issue, bug report, feedback, or feature suggestion, please let me know through an email at oli4dral@gmail.com.
