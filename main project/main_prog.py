
######## Importing modules for Tkinter ###########
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk

######## Importing modules for mediapipe ############
import cv2
import numpy as np
import time
import PoseModule as pm


########### Accessing Video ###########

cam=1
def camselect(file1=NONE, file2=NONE):
    global cap

    if cam:
        cap = cv2.VideoCapture(0)

    else:
        cap = cv2.VideoCapture(file1)



camselect()

detector = pm.PoseDetector()


ptime = 0  # variable for fps
im1=0
file2 = NONE

def test2():
    global ptime


    if im1 :

        img = cv2.imread(file2)

    else:
        success, img = cap.read()
    
        img = cv2.flip(img, 1)
  
    # img = cv2.resize(img, (960, 640))  # width, height

    img = detector.findPose(img, False)
    lmlist = detector.findPosition(img, False)
    # img = cv2.resize(img, (960, 640))  # width, height


    ###### main processing ######
    if len(lmlist) != 0:
        AngL = detector.findAngle(img, 16, 14, 12)
        AngR = detector.findAngle(img, 11, 13, 15)
        AngLs = detector.findAngle(img, 11, 12, 14)
        AngRs = detector.findAngle(img, 13, 11, 12)

        perLs = np.interp(AngLs, (20, 190), (0, 100))
        perRs = np.interp(AngRs, (20, 190), (0, 100))

        img = cv2.resize(img, (960, 640))  # width, height

        perL = 0
        perR = 0
        if AngR < 90 and AngL > 120:

            perL = np.interp(AngL, (20, 190), (0, 100))
            perR = np.interp(AngR, (11, 20), (200, 0))
            cv2.putText(img, 'Left Dab', (20, 500),
                        cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)

        if AngR > 120 and AngL < 90:

            perL = np.interp(AngL, (11, 20), (200, 0))
            perR = np.interp(AngR, (20, 190), (0, 100))
            cv2.putText(img, 'right Dab', (20, 500),
                        cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)

        # print(perL, perLs, perRs, perR)
        total = perL+perLs+perRs+perR
        ptotal = np.interp(total, (0, 500), (0, 100))
        cv2.putText(img, f'{str(int(ptotal))}%', (850, 100),
                    cv2.FONT_HERSHEY_COMPLEX, 1, (255, 128, 0), 2)

        if ptotal < 50:

            ackText = 'Very Poor'

        elif ptotal < 70:

            ackText = 'Almost There'

        else:

            ackText = 'YAY ! You\'ve got it'

        cv2.putText(img, ackText, (20, 200),
                    cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)

    else:
        img = cv2.resize(img, (960, 640))  # width, height
        cv2.putText(img, 'Come on Dear! Do the Dab', (30, 400),
                    cv2.FONT_HERSHEY_PLAIN, 4, (0, 255, 0), 4)

    ########## fps calculation ########
    ctime = time.time()
    fps = 1/(ctime-ptime)
    ptime = ctime
    cv2.putText(img, f'FPS = {str(int(fps))}', (20, 20),
                cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 0, 0), 2)

    cv2.putText(img, ' COPYRIGHT CLAIMS BY IRTAZA AHMED KASHIF ', (300, 20),
                cv2.FONT_HERSHEY_COMPLEX, 0.6, (0, 0, 0), 2)

    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # rgb = cv2.resize(rgb, (960, 640))  # width, height

    return rgb


################################### Tkinter Code ##########################################


def imageselect():
    global file2
    global im1
    global cam
    file2 = filedialog.askopenfilename()
    im1 = 1
    cam = 0




def openfile():
    global im1
    global cam
    file1 = filedialog.askopenfilename()
    cam = 0
    camselect(file1)
    im1=0


def openV1():  # code for opening first video
    global im1
    global cam
    file1 = 'assets/video1.mp4'
    cam = 0
    camselect(file1)
    im1 =0


def camvideo():
    global im1
    global cam
    im1=0
    cam = 1
    camselect(cam)


def close():
    window.destroy()


# Window Creation
window = Tk()
window.configure(bg='#856ff8')
window.title("Dab Check")
width = window.winfo_screenwidth()+10
height = window.winfo_screenheight()+10
window.geometry("%dx%d" % (width, height))
window.minsize(width, height)
window.maxsize(width, height)


################ Design ################
mainlabel = Label(window, text="Dab Check", font=(
    "Raleway", 20, "bold", "italic"), bg="#e7e6d1", fg='blue')
mainlabel.pack()


f1 = Frame(window, bg='cyan')
f1.pack(side=LEFT, fill='y', anchor='nw')

explore_video  = Button(f1, text="Browse Video", bg='#e7e6d1', fg='magenta', font=(
    "Calibri", 14, "bold"), command=openfile).pack(padx=50)

explore_image = Button(f1, text="Browse Image", bg='#e7e6d1', fg='magenta', font=(
    "Calibri", 14, "bold"), command=imageselect).pack(padx=50)

livecam = Button(f1, text="Open Web Cam", bg='#e7e6d1', fg='magenta', font=(
    "Calibri", 14, "bold"), command=camvideo).pack()

v1 = Button(f1, text="Test Video 1", bg='#e7e6d1', fg='magenta', font=(
    "Calibri", 14, "bold"), command=openV1).pack(padx=50)


Exit_Application = Button(f1, text="Exit the Application", bg='#e7e6d1', fg='magenta', font=(
    "Calibri", 14, "bold"), command=close).pack(pady=200)


############### Video Player #######################


label1 = Label(window, width=960, height=640)
label1.place(x=240, y=50)


def select_img():
    image = Image.fromarray(test2())
    finalImage = ImageTk.PhotoImage(image)
    label1.configure(image=finalImage)
    label1.image = finalImage
    window.after(1, select_img)


select_img()


window.mainloop()
