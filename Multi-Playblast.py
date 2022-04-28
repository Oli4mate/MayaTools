#---------------------#
#                     #
#   MULTI-PLAYBLAST   #
#        v1.1         #
#                     #
#     Python 3.0      #
#   For Maya 2022+    #
#      27-4-2022      #
#                     #
#   By Olivier Dral   #
#                     #
#---------------------#



import maya.cmds as cmds
import maya.mel as mel

#get offset preset for offsetting different playblasts
locationOffsetMultipliers = [ [-1.0,1.0] , [1.0,1.0] , [-1.0,-1.0] , [1.0,-1.0] ]

#get all cameras of all panels
panelList = cmds.getPanel(type="modelPanel")
camList = []
for m in panelList:
    camList.append(cmds.modelPanel(m,q=1,camera=1))



#UI CREATION
def UI():
    #initialize window
    toolWindow = cmds.window(title="Multi-Playblast",w=350,h=400,s=0)
    cmds.columnLayout()
    scrollParent = cmds.scrollLayout(w=350,h=400,verticalScrollBarAlwaysVisible=1,verticalScrollBarThickness=10)

    #create dropdowns to allow camera selection
    cmds.frameLayout("Camera / panel Layout", labelAlign="center",w=330)
    cmds.gridLayout(nc=2,cellWidth=165,cellHeight=50)
    cmds.optionMenu("topLeft")
    for i in camList:
        cmds.menuItem(label=i)
    cmds.optionMenu("topRight")
    for i in camList:
        cmds.menuItem(label=i)
    cmds.optionMenu("botLeft")
    for i in camList:
        cmds.menuItem(label=i)
    cmds.optionMenu("botRight")
    for i in camList:
        cmds.menuItem(label=i)



    #VIDEO SETTINGS
    cmds.setParent( '..' )
    cmds.frameLayout("Video Settings", labelAlign="center")
    cmds.rowColumnLayout( numberOfColumns=3, columnWidth=[(1, 100), (2, 20), (3, 210)])

    #resolution
    cmds.text("Resolution", align="right")
    cmds.separator(hr=0,height=20)
    cmds.intFieldGrp("resFloats",numberOfFields=2,value1=1920,value2=1080)

    #time range
    cmds.text("Frame Range", align="right")
    cmds.separator(hr=0,height=20)
    cmds.intFieldGrp("timeFloats",numberOfFields=2,value1=cmds.playbackOptions(q=1,min=1),value2=cmds.playbackOptions(q=1,max=1))



    #DISPLAY SETTINGS
    cmds.setParent( '..' )
    cmds.setParent( '..' )
    cmds.frameLayout("Display Settings", labelAlign="center")
    cmds.rowColumnLayout( numberOfColumns=3, columnWidth=[(1, 100), (2, 20), (3, 210)])

    #viewer mode: no change, poly only, poly + cv
    cmds.text("Display Mode", align="right")
    cmds.separator(hr=0,height=20)
    cmds.optionMenu("viewMode")
    cmds.menuItem(label="Current view")
    cmds.menuItem(label="Polygons only")
    cmds.menuItem(label="Polygons and control curves only")

    #textures on/off
    cmds.text("Textures", align="right")
    cmds.separator(hr=0,height=20)
    cmds.checkBox("textures",label="",v=1)

    #ao on/off
    cmds.text("Ambient Occlusion", align="right")
    cmds.separator(hr=0,height=20)
    cmds.checkBox("ao",label="",v=1)

    #motion blur on/off
    cmds.text("Motion Blur", align="right")
    cmds.separator(hr=0,height=20)
    cmds.checkBox("motionblur",label="",v=0)



    #HUD SETTINGS
    cmds.setParent( '..' )
    cmds.setParent( '..' )
    cmds.frameLayout("HUD Settings", labelAlign="center")
    cmds.rowColumnLayout( numberOfColumns=3, columnWidth=[(1, 100), (2, 20), (3, 210)])

    #grid on/off
    cmds.text("View Grid", align="right")
    cmds.separator(hr=0,height=20)
    cmds.checkBox("gridView",label="",v=1)

    #frame on/off
    cmds.text("View Frame Number", align="right")
    cmds.separator(hr=0,height=20)
    cmds.checkBox("frameView",label="",v=0)

    #axis on/off
    cmds.text("View Axis", align="right")
    cmds.separator(hr=0,height=20)
    cmds.checkBox("axisView",label="",v=1)



    #FILE SETTINGS
    cmds.setParent( '..' )
    cmds.frameLayout("File Settings", labelAlign="center")
    cmds.rowColumnLayout( numberOfColumns=3, columnWidth=[(1, 100), (2, 20), (3, 210)])

    #file name
    cmds.text("File Name", align="right")
    cmds.separator(hr=0,height=25)
    cmds.textField("fileName", text="Multi-Playblast")

    #file location
    cmds.text("Custom File Location", align="right")
    cmds.separator(hr=0,height=25)
    cmds.button("Browse", c='CustomDirSave(cmds.textField("fileName", q=1, text=1))')

    #override on/off
    cmds.text("Override File", align="right")
    cmds.separator(hr=0,height=20)
    cmds.checkBox("OverrideFile",label="",v=0)

    #file name and location text
    cmds.text("Default Directory: ", align="right")
    cmds.separator(hr=0,height=25)
    cmds.text("/movies/", align="left")



    #create bottom buttons and spawn window
    cmds.setParent( '..' )
    cmds.setParent( '..' )
    cmds.setParent( '..' )
    cmds.setParent( '..' )
    cmds.setParent( '..' )
    cmds.setParent( '..' )
    cmds.gridLayout(nc=2,cellWidth=175)
    cmds.button(w=175,label='Execute', command=('MultiRender(str("movies/" + cmds.textField("fileName",q=1,text=1)))'))
    cmds.button(w=175,label='Close', command=('cmds.deleteUI(\"' + toolWindow + '\", window=True)'))

    cmds.showWindow(toolWindow)

#CUSTOM LOCATION SAVE
def CustomDirSave(Filename):
    #open directory file dialog with .avi as options
    DIRECTORY = cmds.fileDialog2(fileMode=0, fileFilter="Video Files (*.avi)", setProjectBtnEnabled=1, dialogStyle=0)
    #use directory location as input for playblast
    MultiRender(DIRECTORY[0])

#CREATE PLAYBLAST - with as input the location and file name
def MultiRender(DIR):

    #set all of the base-values based on ui input
    FORMAT = "avi"
    START_POINT = cmds.intFieldGrp("timeFloats", q=1, v1=1)
    END_POINT = cmds.intFieldGrp("timeFloats", q=1, v2=1)
    RESOLUTION_X = cmds.intFieldGrp("resFloats",q=1,v1=1)
    RESOLUTION_Y = cmds.intFieldGrp("resFloats",q=1,v2=1)
    GRID = cmds.checkBox("gridView",q=1,v=1)
    FRAME = cmds.checkBox("frameView",q=1,v=1)
    AXIS = cmds.checkBox("axisView",q=1,v=1)
    AO = cmds.checkBox("ao",q=1,v=1)
    MB = cmds.checkBox("motionblur",q=1,v=1)
    TEX = cmds.checkBox("textures",q=1,v=1)
    XtoY = RESOLUTION_Y / RESOLUTION_X
    MODE = cmds.optionMenu("viewMode",q=1,sl=1)
    OVERRIDE = cmds.checkBox("OverrideFile",q=1,v=1)



    #get all 4 modelling viewports that exist
    panelLocations = [cmds.optionMenu("topLeft",sl=1,q=1) , cmds.optionMenu("topRight",sl=1,q=1) , cmds.optionMenu("botLeft",sl=1,q=1) , cmds.optionMenu("botRight",sl=1,q=1)]
    playblastList = []
    imageplaneList = []
    ViewportDefaults = [[],[],[],[]]
    i = 0
    
    #get starting ao, motionblur, axisview and frameview settings
    FrameDefault = mel.eval("optionVar -q currentFrameVisibility;")
    AxisDefault = mel.eval("optionVar -q viewAxisVisibility;")
    AODefault = cmds.getAttr("hardwareRenderingGlobals.ssaoEnable")
    MBDefault = cmds.getAttr("hardwareRenderingGlobals.motionBlurEnable")



    #loop through the modelling viewports
    for P in panelLocations:

        #take base viewport settings
        ViewportDefaults[i].append(cmds.modelEditor(panelList[P-1], q=1, dtx=1))
        ViewportDefaults[i].append(cmds.modelEditor(panelList[P-1], q=1, ca=1))
        ViewportDefaults[i].append(cmds.modelEditor(panelList[P-1], q=1, cv=1))
        ViewportDefaults[i].append(cmds.modelEditor(panelList[P-1], q=1, df=1))
        ViewportDefaults[i].append(cmds.modelEditor(panelList[P-1], q=1, dim=1))
        ViewportDefaults[i].append(cmds.modelEditor(panelList[P-1], q=1, dc=1))
        ViewportDefaults[i].append(cmds.modelEditor(panelList[P-1], q=1, dy=1))
        ViewportDefaults[i].append(cmds.modelEditor(panelList[P-1], q=1, fl=1))
        ViewportDefaults[i].append(cmds.modelEditor(panelList[P-1], q=1, fo=1))
        ViewportDefaults[i].append(cmds.modelEditor(panelList[P-1], q=1, gr=1))
        ViewportDefaults[i].append(cmds.modelEditor(panelList[P-1], q=1, hs=1))
        ViewportDefaults[i].append(cmds.modelEditor(panelList[P-1], q=1, ha=1))
        ViewportDefaults[i].append(cmds.modelEditor(panelList[P-1], q=1, hu=1))
        ViewportDefaults[i].append(cmds.modelEditor(panelList[P-1], q=1, ikh=1))
        ViewportDefaults[i].append(cmds.modelEditor(panelList[P-1], q=1, imp=1))
        ViewportDefaults[i].append(cmds.modelEditor(panelList[P-1], q=1, j=1))
        ViewportDefaults[i].append(cmds.modelEditor(panelList[P-1], q=1, lt=1))
        ViewportDefaults[i].append(cmds.modelEditor(panelList[P-1], q=1, lc=1))
        ViewportDefaults[i].append(cmds.modelEditor(panelList[P-1], q=1, m=1))
        ViewportDefaults[i].append(cmds.modelEditor(panelList[P-1], q=1, mt=1))
        ViewportDefaults[i].append(cmds.modelEditor(panelList[P-1], q=1, ncl=1))
        ViewportDefaults[i].append(cmds.modelEditor(panelList[P-1], q=1, npa=1))
        ViewportDefaults[i].append(cmds.modelEditor(panelList[P-1], q=1, nr=1))
        ViewportDefaults[i].append(cmds.modelEditor(panelList[P-1], q=1, nc=1))
        ViewportDefaults[i].append(cmds.modelEditor(panelList[P-1], q=1, ns=1))
        ViewportDefaults[i].append(cmds.modelEditor(panelList[P-1], q=1, pv=1))
        ViewportDefaults[i].append(cmds.modelEditor(panelList[P-1], q=1, pl=1))
        ViewportDefaults[i].append(cmds.modelEditor(panelList[P-1], q=1, ps=1))
        ViewportDefaults[i].append(cmds.modelEditor(panelList[P-1], q=1, pm=1))
        ViewportDefaults[i].append(cmds.modelEditor(panelList[P-1], q=1, str=1))
        ViewportDefaults[i].append(cmds.modelEditor(panelList[P-1], q=1, sds=1))
        ViewportDefaults[i].append(cmds.modelEditor(panelList[P-1], q=1, tx=1))

        #set new loop count
        i = i + 1

        #set correct HUD settings
        if AXIS == 0:
            mel.eval("setViewAxisVisibility 0;")
        else:
            mel.eval("setViewAxisVisibility 1;")

        cmds.setAttr("hardwareRenderingGlobals.lineAAEnable", 1);
        cmds.setAttr("hardwareRenderingGlobals.multiSampleEnable", 1);
        cmds.setAttr("hardwareRenderingGlobals.ssaoEnable", AO);
        cmds.setAttr("hardwareRenderingGlobals.motionBlurEnable", MB);

        #set viewport settings
        if MODE == 1:
            cmds.modelEditor(panelList[P-1], e=1, displayTextures=TEX, gr=GRID)
        elif MODE == 2:
            cmds.modelEditor(panelList[P-1], e=1, dtx=TEX, ca=0, cv=0, df=0, dim=0, dc=0, dy=0, fl=0, fo=0, gr=GRID, hs=0, ha=0, hu=0, ikh=0, imp=0, j=0, lt=0, lc=0, m=0, mt=0, ncl=0, npa=0, nr=0, nc=0, ns=0, pv=0, pl=0, ps=0, pm=1, str=0, sds=0, tx=0)
        elif MODE == 3:
            cmds.modelEditor(panelList[P-1], e=1, dtx=TEX, ca=0, cv=0, df=0, dim=0, dc=0, dy=0, fl=0, fo=0, gr=GRID, hs=0, ha=0, hu=0, ikh=0, imp=0, j=0, lt=0, lc=0, m=0, mt=0, ncl=0, npa=0, nr=0, nc=1, ns=0, pv=0, pl=0, ps=0, pm=1, str=0, sds=0, tx=0)

        #make all temporary playblasts and save their locations into a list
        playblastList.append(cmds.playblast(width=RESOLUTION_X/2,height=RESOLUTION_Y/2,editorPanelName=panelList[P-1],forceOverwrite=1,format=FORMAT,viewer=0,filename="movies\playblast_prerender_" + str(i) + "." + FORMAT))

        i = i - 1

        #reset viewport settings
        if MODE == 1:
            cmds.modelEditor(panelList[P-1], e=1, displayTextures=ViewportDefaults[i][0], gr=ViewportDefaults[i][9])
        elif MODE == 2:
            cmds.modelEditor(panelList[P-1], e=1, dtx=ViewportDefaults[i][0], ca=ViewportDefaults[i][1], cv=ViewportDefaults[i][2], df=ViewportDefaults[i][3], dim=ViewportDefaults[i][4], dc=ViewportDefaults[i][5], dy=ViewportDefaults[i][6], fl=ViewportDefaults[i][7], fo=ViewportDefaults[i][8], gr=ViewportDefaults[i][9], hs=ViewportDefaults[i][10], ha=ViewportDefaults[i][11], hu=ViewportDefaults[i][12], ikh=ViewportDefaults[i][13], imp=ViewportDefaults[i][14], j=ViewportDefaults[i][15], lt=ViewportDefaults[i][16], lc=ViewportDefaults[i][17], m=ViewportDefaults[i][18], mt=ViewportDefaults[i][19], ncl=ViewportDefaults[i][20], npa=ViewportDefaults[i][21], nr=ViewportDefaults[i][22], nc=ViewportDefaults[i][23], ns=ViewportDefaults[i][24], pv=ViewportDefaults[i][25], pl=ViewportDefaults[i][26], ps=ViewportDefaults[i][27], pm=ViewportDefaults[i][28], str=ViewportDefaults[i][29], sds=ViewportDefaults[i][30], tx=ViewportDefaults[i][31])
        elif MODE == 3:
            cmds.modelEditor(panelList[P-1], e=1, dtx=ViewportDefaults[i][0], ca=ViewportDefaults[i][1], cv=ViewportDefaults[i][2], df=ViewportDefaults[i][3], dim=ViewportDefaults[i][4], dc=ViewportDefaults[i][5], dy=ViewportDefaults[i][6], fl=ViewportDefaults[i][7], fo=ViewportDefaults[i][8], gr=ViewportDefaults[i][9], hs=ViewportDefaults[i][10], ha=ViewportDefaults[i][11], hu=ViewportDefaults[i][12], ikh=ViewportDefaults[i][13], imp=ViewportDefaults[i][14], j=ViewportDefaults[i][15], lt=ViewportDefaults[i][16], lc=ViewportDefaults[i][17], m=ViewportDefaults[i][18], mt=ViewportDefaults[i][19], ncl=ViewportDefaults[i][20], npa=ViewportDefaults[i][21], nr=ViewportDefaults[i][22], nc=ViewportDefaults[i][23], ns=ViewportDefaults[i][24], pv=ViewportDefaults[i][25], pl=ViewportDefaults[i][26], ps=ViewportDefaults[i][27], pm=ViewportDefaults[i][28], str=ViewportDefaults[i][29], sds=ViewportDefaults[i][30], tx=ViewportDefaults[i][31])

        i = i + 1

    #reset counter
    i = 0

    print(ViewportDefaults)

    #loop through the temporary playblasts
    for P in playblastList:

        #create image planes
        currentImagePlane = cmds.imagePlane(camera=camList[0])
        imageplaneList.append(currentImagePlane)

        #apply correct settings to image panes to support video files
        cmds.setAttr(currentImagePlane[1] + '.useFrameExtension', 1)
        cmds.setAttr(currentImagePlane[1] + '.frameIn', START_POINT)
        cmds.setAttr(currentImagePlane[1] + '.type', 2)
        cmds.setAttr(currentImagePlane[1] + '.depth', 0.1)

        #set offset
        camX = cmds.getAttr(camList[0] + "Shape.horizontalFilmAperture")
        camY = cmds.getAttr(camList[0] + "Shape.verticalFilmAperture")
        cmds.setAttr(currentImagePlane[1] + '.sizeX', camX / 2)
        cmds.setAttr(currentImagePlane[1] + '.sizeY', camX / 2 * XtoY)
        cmds.setAttr(currentImagePlane[1] + '.offsetX', (camX / 4) * locationOffsetMultipliers[i][0])
        cmds.setAttr(currentImagePlane[1] + '.offsetY', (camY / 4 * XtoY) * locationOffsetMultipliers[i][1])

        #import playblast video to image plane
        cmds.setAttr(currentImagePlane[1] + '.imageName', P, type = 'string')

        #increase loop count
        i += 1



    #set HUD settings for final playblast
    if FRAME == 0:
        mel.eval("setCurrentFrameVisibility 0;")
    else:
        mel.eval("setCurrentFrameVisibility 1;")

    mel.eval("setViewAxisVisibility 0;")



    #clear selection to not get boundry lines around last edited image plane
    cmds.select(clear=1)
    cmds.modelEditor(panelList[0], e=1, imp=1)

    #make final playblast using the preset file name and location
    cmds.playblast(startTime=START_POINT, endTime=END_POINT, filename=DIR,width=RESOLUTION_X,height=RESOLUTION_Y, clearCache=1,editorPanelName=panelList[0],forceOverwrite=OVERRIDE,format="movie",viewer=1)

    #reset values
    if FrameDefault == 0:
        mel.eval("setCurrentFrameVisibility 0;")
    elif FrameDefault == 1:
        mel.eval("setCurrentFrameVisibility 1;")
        
    if AxisDefault == 0:
        mel.eval("setViewAxisVisibility 0;")
    elif AxisDefault == 1:
        mel.eval("setViewAxisVisibility 1;")
        
    cmds.setAttr("hardwareRenderingGlobals.ssaoEnable", AODefault)
    cmds.setAttr("hardwareRenderingGlobals.motionBlurEnable", MBDefault)



    #remove the imageplanes
    for imgP in imageplaneList:
        print(imgP)
        cmds.delete(imgP)

    #remove temporary playblasts
    for P in playblastList:
        cmds.sysFile(P,delete=1)



#spawn UI
UI()
