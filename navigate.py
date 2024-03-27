from mandelbrotConfig import *

def printCommands():
    print()
    print("## COMMANDS ##")
    print("Command | Description |")
    print("--------|--------------")
    print("  help\t| Show Help Menu")
    print("  save\t| Save coordinates for plotting zooms")
    print("  +/-\t| zoom in or out by a factor of 2 on the initial image")
    print("  X\t| Toggles Cross Hairs")
    print("  dis\t| Toggles details printed on image")
    print("  iter\t| Sets the max iteration ")
    print("  res\t| Sets the resolution")
    print("  %N\t| Set the zoom for the initial image to N.")
    print("    \t|  -- Accepts:%0 %1, %16, %48, %128, %256, %512, %1024")
    print()

def printMoves():
    print()
    print("## MOVES ##")
    print()
    print("    W   ",end='\t'); print("\t   8   ")
    print("  Q   E ",end='\t'); print("\t 7   9 ")
    print(" A     D",end='\t'); print("\t4     6")
    print("  Z   C ",end='\t'); print("\t 1   3 ")
    print("    S   ",end='\t'); print("\t   2   ")
    print()
    
def printHelp():
    print()
    print("######################################################")
    print("################ Mandelbort Navigator ################")
    print("######################################################")
    print()
    print("                      HELP MENU")
    print()
    print("#################### COMMANDS #######################")
    print()
    print("Issue a command from the menu above. After issuing a command, you will be prompted to move. You can press Enter to print current position, issue a move and print, or enter another command and repeat. Commands cannot be combined with movements or other commands.")
    print()
    input("Press Enter to Continue...")
    print()
    print("##################### MOVEMENTS ######################")
    print()
    print("  Movements can be combined into one string AAAAASSS.\n")
    print("Leaving it blank will print images with any new commands queued. Capital letters move more than lowercase. (D = 1/16th of image, d = 1/32nd) The Key pad moves very little. (6 = 0.0001)")
    print()
    printMoves()
    print()
    print(" # Use the Cross Hairs to narrow in with the X command")
    print()
    printCommands()
    print()
    print("Press Enter to Continue")
    one=input()
    one = ''
    print("#######################################################")
    print()
    print()





def naviLoop(x, y):
    # Files
    zoomFileName = 'NaviSequence.csv'
    zoomFile = os.getcwd()+'/Navigator/'+zoomFileName


    #   Iterations
    MAX_ITER = 80
    #   Image size (pixels)
    WIDTH = 600
    HEIGHT = 400

    #zStart = 4
    zStart = 2
    zTimes = 2
    
    #   Cross Hairs
    crossHairs = True
    #crossHairs = False

    #   Details on image
    display = True
    #display = False

    # The amount you can move
    big = 1/16
    bigD = big / 2
    small = big / 4
    smallD = small / 2
    xMoves = {
        # Big movements
        'E': bigD, 'e': smallD,
        'Z': -bigD, 'z': -smallD,
        'Q': -bigD, 'q': -smallD,
        'C': bigD, 'c': smallD,
        'D': big,'d':small,
        'A':-big, 'a':-small,

        # micro movements
        '3': 0.0000000525,
        '7': -0.0000000525,
        '9': 0.0000000525,
        '4': -0.0000001,
        '1': -0.0000000525,
        '6': 0.0000001,
        '':0
        }
    yMoves = {
        # Big movements
        'Q': bigD, 'q': smallD,
        'E': bigD, 'e': smallD,
        'Z': -bigD, 'z': -smallD,
        'W': big, 'w':small,
        'S':-big, 's':-small,
        'C': -bigD, 'c': -smallD,

        # micro movements
        '8': 0.0000001,
        '7': 0.0000000525,
        '9': 0.0000000525,
        '2': -0.0000001,
        '1': -0.0000000525,
        '3': -0.0000000525,
        '':0
        }
    
    '''
    x = -0.34515740000000006
    y = -0.6422024999999997
    '''
  
    #printHelp()
    print("Generating Images for:",x,y)
    print()
    # printZooms:

    printZooms(x, y, WIDTH, HEIGHT, MAX_ITER, zStart, zTimes, crossHairs, display, directory = 'Navigator' )

    
    print("######################## Done #########################")
    print("#######################################################")
    print()
    # Main loop
    commandBool = False
    while True:
        if not commandBool:
            #printMoves()
            printCommands()
            print("#######################################################")
            print()
            print("Enter movement or command (help): ", end = '')
        else:
            print("Commands queued, enter movement or press enter to print: ",end='')
        entry = input()
# Commands
        if entry.upper() == "HELP":
            printHelp();continue

        # Save Coords for Zooms
        if entry.upper() == "SAVE":
            saveStatsCsv(x, y, zStart, WIDTH, HEIGHT, MAX_ITER, crossHairs, display, zoomFile)
            continue


        # Set Iterations
        if entry.upper() == "ITER":
            MAX_ITER = setMaxIter(MAX_ITER)
            print(" --Max Iterations set to: "+str(MAX_ITER))
            commandBool=True;continue

         # Set Resolution
        if entry.upper() == "RES":
            WIDTH, HEIGHT = setResolution(WIDTH)
            print(" --Resolution set to: "+str(WIDTH)+"x"+str(HEIGHT))
            commandBool=True;continue
        # Increase Zoom
        
        if entry == "+":
            zStart /= 2
            print(" --Zoom Start Value changed to: "+str(1 / zStart))
            commandBool=True;continue
        if entry == "-":
            if zStart < 1:
                zStart *= 2
                print(" --Zoom Start Value changed to: "+str(1 / zStart))
                commandBool=True;continue
            else: print(" --Zoom already at 1");continue
        # Toggle Cross Hairs
        if entry.upper() =='X':
            if crossHairs == False:
                crossHairs = True
                print(" --Enabling Cross Hairs")
                commandBool=True;continue
            else:
                crossHairs = False
                print(" --Disabling Cross Hairs")
                commandBool=True;continue
        # Toggle Display
        if entry.upper() =='DIS':
            if display == False:
                display = True
                print(" --Enabling Display")
                commandBool=True;continue
            else:
                display = False
                print(" --Disabling Display")
                commandBool=True;continue
        # Set zoom value
        if entry == "%0":
            zStart = 4
            print(" --Zoom Start Value set to: "+str(int(1 / zStart))+"x")
            commandBool=True;continue
        if entry == "%1":
            zStart = 1
            print(" --Zoom Start Value set to: "+str(int(1 / zStart))+"x")
            commandBool=True;continue
        if entry == "%16":
            zStart = 1/16
            print(" --Zoom Start Value set to: "+str(int(1 / zStart))+"x")
            commandBool=True;continue
        if entry == "%48":
            zStart = 1/48
            print(" --Zoom Start Value set to: "+str(int(1 / zStart))+"x")
            commandBool=True;continue
        if entry == "%128":
            zStart = 1/128
            print(" --Zoom Start Value set to: "+str(int(1 / zStart))+"x")
            commandBool=True;continue
        if entry == "%256":
            zStart = 1/256
            print(" --Zoom Start Value set to: "+str(int(1 / zStart))+"x")
            commandBool=True;continue
        if entry == "%512":
            zStart = 1/512
            print(" --Zoom Start Value set to: "+str(int(1 / zStart))+"x")
            commandBool=True;continue
        if entry == "%1024":
            zStart = 1/1024
            print(" --Zoom Start Value set to: "+str(int(1 / zStart))+"x")
            commandBool=True;continue
        
            
        xChange = 0
        yChange = 0
        
        for i in entry:
            if i in xMoves:
                xChange += xMoves[i]
            if i in yMoves:
                yChange -= yMoves[i]
        x += xChange * zStart
        y += yChange * zStart
        commandBool = False
        print("Generating Images for:",x,y)
        print()
        if xChange or yChange: print("Change in X: "+str(xChange)+\
                          "\nChange in Y: "+str(yChange))
        
        # Print it
        printZooms(x, y, WIDTH, HEIGHT, MAX_ITER, zStart, zTimes, crossHairs, display, directory = 'Navigator')
        filePath = os.getcwd()+"/Navigator/"
        displayImage(filePath, WIDTH, HEIGHT)
        print("######################## Done #########################")
        print("#######################################################")
        print()
        print()






'''
 Resolution: 600x400
  Zoom: 128.0x
  Iterations: 240
Center Coordinates: X:-0.7692813199999996 Y:0.1069251250000002



  Zoom: 2097152.0x
  Iterations: 750

Center Coordinates: X:-0.7692847770693966 Y:0.1070103894443514

'''

if __name__ == "__main__":


    # Cool Locations:

    # X:-0.7806635625 Y:-0.14670003249999977
    # X: -1.1883  Y: 0.242
    # X: -0.749  Y: 0.149 
    # X:-0.34515734750000004 Y:-0.6422024474999997
    # X:-0.11640740000000008 Y:-0.6497024999999994
    # X:-0.7692813199999996 Y:0.1069251250000002


    # Set initial coords

    # x= -0.7692813199999996
    # y= 0.1069251250000002

    x = -0.7692813199999996
    y = 0.1069251250000002

    naviLoop(x,y)










