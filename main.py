from tkinter import *
import tkinter.messagebox as tmsg
from PIL import ImageTk, Image
import numpy as np
import cv2
import os
import socket
from datetime import datetime

dim = (640, 480)
video = cv2.VideoCapture(1)
Lower = [-1, -1, -1]
Upper = [-1, -1, -1]

userpath = os.environ['USERPROFILE'] + "\\videos\\Invisible Cloak\\"
try:
    os.mkdir(userpath)
except:
    pass

def open_help():
    help = Toplevel()
    help.title("Help")
    help.iconbitmap("icon.ico")
    help.geometry("500x500")
    help.minsize(500, 500)
    help.maxsize(1366, 768)
    t = ""
    with open("help.txt") as f:
        t = f.read()
    Scroll = Scrollbar(help)
    Scroll.pack(side=RIGHT, fill=Y)
    l1 = Text(help, yscrollcommand=Scroll.set, padx=5, pady=5, font=("Arial", "15"))
    l1.insert(1.0, t)
    l1.config(state="disabled")
    Scroll.config(command=l1.yview)
    l1.pack(expand=True, fill=BOTH)
    help.mainloop()

def clear_status():
    status_var.set("")
    opt_ch.set("")
    con_add.set("")
    con_port.set("")
    user_name.set("")
    is_rec.set("")
    save_loc.set("")


def create_f5():
    Button(f5, text="Change Background", command=click_bg).pack(side="left", padx=5)
    Button(f5, text="Show Background", command=show_bg).pack(side="left", padx=5)
    Button(f5, text="Calibrate", command=calibration).pack(side="left", padx=5)
    Button(f5, text="Start Magic", command=start_magic).pack(side="left", padx=5)
    Button(f5, text="Stop Magic", command=stop_magic).pack(side="left", padx=5)
    Checkbutton(f5, text="Record The Output", variable=rec, onvalue=1, offvalue=0, bg="yellow").pack(side="left",
                                                                                                     padx=5)


def stop_magic():
    status_var.set("Status : Connected")
    save_loc.set("Save Location : " + userpath)
    is_rec.set("")
    video.release()
    cv2.destroyAllWindows()


def check_host():
    #  Checking For WebCam
    if ch.get() == "Webcam":
        try:
            video.open(int(address.get()))
            if not video.isOpened():
                tmsg.showerror("Error", "Can't Open WebCam\nMake Sure That WebCam Is Connected")
                return 0
        except ValueError:
            tmsg.showerror("Error", "Please Enter A Valid WebCam ID")
            return 0
    #  Checking For Streaming
    elif ch.get() == "Stream":
        host = True if os.system("ping -n 1 " + address.get()) is 0 else False  # Checking The IP return 1 is exist
        if address.get() == "":
            tmsg.showerror("Error", "Enter The IP Address")
            return 0
        elif host != 1:
            tmsg.showerror("Error", "Enter A Valid IP Address")
            return 0
        try:
            if port.get() == "":
                tmsg.showerror("Error", "Port Can't Be Blank")
                return 0
            elif 0 <= int(port.get()) <= 65535:
                a_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                location = (address.get(), int(port.get()))
                result_of_check = a_socket.connect_ex(location)
                if result_of_check != 0:
                    tmsg.showerror("Error", "Port Is Not Open\nMake Sure Entered Port Is Right")
                    return 0
                a_socket.close()
            else:
                tmsg.showerror("Error", "Port Is Not Valid\nValid Range For Ports : 0-65535")
                return 0
        except ValueError:
            tmsg.showerror("Error", "Port Should Be A  Number")
            return 0
    else:
        tmsg.showwarning("Error", "Please Any Option")
        return 0
    return 1


def Empty(x):
    print(x)
    pass


def clear_widget(fr):
    for items in fr.winfo_children():
        items.destroy()


def disconnect():
    clear_widget(f5)
    clear_status()
    status_var.set("Status : Idle")
    video.release()
    cv2.destroyAllWindows()


def show_bg():
    try:
        status_var.set("Status : Showing Background")
        status.update()
        img = cv2.imread(userpath + "background.png")
        img = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
        cv2.imshow("Background", img)
    except:
        ans = tmsg.askyesno("Error", "Background Not Captured Yet\nDo You Want To Capture It Now")
        if ans == YES:
            click_bg()
    status_var.set("Status : Connected")


def click_bg():
    if check_host():
        status_var.set("Status : Changing Background")
        window = Toplevel()
        window.iconbitmap("icon.ico")
        window.title("Click Background")
        window.geometry("660x550")
        window.minsize(660, 550)
        window.maxsize(660, 550)
        window.configure(bg="black")
        url = 0
        if ch.get() == "Webcam":
            url = int(address.get())
        elif ch.get() == "Stream":
            url = str(
                "http://" + user_var.get() + ":" + pass_var.get() + "@" + address.get() + ":" + port.get() + para.get())
        vc = video
        vc.open(url)

        def save_img():
            status_var.set("Status : Connected")
            cv2.imwrite(userpath + 'background.png', frame)
            tmsg.showinfo("Successful", "Background Captured Successfully")
            window.destroy()

        def quit_window():
            status_var.set("Status : Connected")
            window.destroy()

        l1 = Label(window, pady=10, bg="black")
        l1.pack()
        local_frame = Frame(window, padx=5, pady=5, bg="black")
        Button(local_frame, text="Click This Background", command=save_img).pack(side="left")
        Button(local_frame, text="Exit", command=quit_window, padx=5).pack(side="left", padx=20)
        local_frame.pack(anchor="w", fill="x", padx=220)
        while True:
            ret_v, frame = vc.read()
            frame = cv2.flip(frame, 1)
            img = vc.read()[1]
            img = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
            img = cv2.flip(img, 1)
            img1 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img = ImageTk.PhotoImage(Image.fromarray(img1))
            l1['image'] = img
            window.update()


def start_magic():
    bg = cv2.imread(userpath + "background.png")
    if bg is None:
        ans = tmsg.askyesno("Error", "Background Not Captured Yet\nDo You Want To Capture It Now")
        if ans == YES:
            click_bg()
    else:
        status_var.set("Status : Doing Magic")
        background = cv2.resize(bg, dim, interpolation=cv2.INTER_AREA)
        video.release()
        vc = video
        url = "None"
        if ch.get() == "Webcam":
            url = int(address.get())
        elif ch.get() == "Stream":
            url = str(
                "http://" + user_var.get() + ":" + pass_var.get() + "@" + address.get() + ":" + port.get() + para.get())
        vc.open(url)
        size = (640, 480)
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        if ch.get() == "Webcam":
            st = "WebCam_" + str(address.get())
        else:
            st = "IP_WebCam_"
        if int(rec.get()) == 1:
            is_rec.set("Recording")
            out = cv2.VideoWriter(f'{userpath}{st}_{datetime.now().strftime("%d-%m-%Y_%H-%M-%S")}.avi', fourcc, 10,
                                  size)
        while True:
            return_value, frame = vc.read()
            frame = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)
            frame = cv2.flip(frame, 1)
            img_in = vc.read()[1]
            img_in = cv2.resize(img_in, dim, interpolation=cv2.INTER_AREA)
            img_in = cv2.flip(img_in, 1)
            cv2.putText(img_in, 'Input', (5, 25), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
            img1 = cv2.cvtColor(img_in, cv2.COLOR_BGR2RGB)
            img_in = ImageTk.PhotoImage(Image.fromarray(img1))
            input_frame['image'] = img_in
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            mask = cv2.inRange(hsv, np.array(Lower), np.array(Upper))

            # kernel = np.ones((10, 10), np.uint8)
            # mask = cv2.erode(mask, kernel, iterations=10)
            # mask = cv2.dilate(mask, kernel, iterations=15)

            frame = np.array(frame)
            temp = cv2.bitwise_and(background, background, mask=mask)
            mask = cv2.bitwise_not(mask)
            frame = cv2.bitwise_and(frame, frame, mask=mask)
            frame = cv2.add(frame, temp)
            frame = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)
            if int(rec.get()) == 1:
                out.write(frame)
            img2 = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)
            img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)
            cv2.putText(img2, 'Output', (5, 25), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
            img_out = ImageTk.PhotoImage(Image.fromarray(img2))
            output_frame['image'] = img_out
            root.update()


def calibration():
    if check_host():
        if ch.get() == "Webcam":
            url = int(address.get())
        else:
            url = str(
                "http://" + user_var.get() + ":" + pass_var.get() + "@" + address.get() + ":" + port.get() + para.get())
        status_var.set("Status : Calibrating")
        vc = video
        vc.open(url)
        tmsg.showinfo("How To Calibrate", "Press esc Button To Exit Calibrate HSV Window")
        cv2.namedWindow('Calibrate HSV')
        cv2.createTrackbar('L_HUE', 'Calibrate HSV', 0, 179, Empty)
        cv2.createTrackbar('L_SAT', 'Calibrate HSV', 0, 255, Empty)
        cv2.createTrackbar('L_VAL', 'Calibrate HSV', 0, 255, Empty)
        cv2.createTrackbar('U_HUE', 'Calibrate HSV', 0, 179, Empty)
        cv2.createTrackbar('U_SAT', 'Calibrate HSV', 0, 255, Empty)
        cv2.createTrackbar('U_VAL', 'Calibrate HSV', 0, 255, Empty)
        cv2.setTrackbarPos('U_HUE', 'Calibrate HSV', 179)
        cv2.setTrackbarPos('U_SAT', 'Calibrate HSV', 255)
        cv2.setTrackbarPos('U_VAL', 'Calibrate HSV', 255)
        while cv2.waitKey(1)==-1:
            global Lower, Upper
            return_value, frame = vc.read()
            frame = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)
            frame = np.flip(frame, 1)
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            # Displaying Input Form
            img_in = vc.read()[1]
            img_in = cv2.resize(img_in, dim, interpolation=cv2.INTER_AREA)
            img_in = cv2.flip(img_in, 1)
            cv2.putText(img_in, 'Input', (5, 25), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
            img1 = cv2.cvtColor(img_in, cv2.COLOR_BGR2RGB)
            img_in = ImageTk.PhotoImage(Image.fromarray(img1))
            input_frame['image'] = img_in
            root.update()
            # Setting The HSV Values
            L_HUE = cv2.getTrackbarPos('L_HUE', 'Calibrate HSV')
            L_SAT = cv2.getTrackbarPos('L_SAT', 'Calibrate HSV')
            L_VAL = cv2.getTrackbarPos('L_VAL', 'Calibrate HSV')
            U_HUE = cv2.getTrackbarPos('U_HUE', 'Calibrate HSV')
            U_SAT = cv2.getTrackbarPos('U_SAT', 'Calibrate HSV')
            U_VAL = cv2.getTrackbarPos('U_VAL', 'Calibrate HSV')
            Lower = [L_HUE, L_SAT, L_VAL]
            Upper = [U_HUE, U_SAT, U_VAL]
            # Displaying The Calibrated Output
            mask = cv2.inRange(hsv, np.array(Lower), np.array(Upper))
            img2 = cv2.resize(mask, dim, interpolation=cv2.INTER_AREA)
            img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)
            cv2.putText(img2, 'Calibrating', (5, 25), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
            img_out = ImageTk.PhotoImage(Image.fromarray(img2))
            output_frame['image'] = img_out
            if cv2.waitKey(1) == 27:
                status_var.set("Status : Connected")
                cv2.destroyWindow('Calibrate HSV')
                break
    status_var.set("Status : Connected")
    cv2.destroyWindow('Calibrate HSV')


def display_input(cap):
    while True:
        img_in = cap.read()[1]
        img_in = cv2.resize(img_in, dim, interpolation=cv2.INTER_AREA)
        img_in = cv2.flip(img_in, 1)
        cv2.putText(img_in, 'Input', (5, 25), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
        img1 = cv2.cvtColor(img_in, cv2.COLOR_BGR2RGB)
        img_in = ImageTk.PhotoImage(Image.fromarray(img1))
        input_frame['image'] = img_in
        root.update()


def connect_webcam():
    if check_host():
        create_f5()
        clear_status()
        status_var.set("Status : Connected")
        opt_ch.set("Current Source : WebCam")
        save_loc.set("Save Location : " + userpath)
        con_add.set("Connected ID : " + address.get())
        video.open(int(address.get()))
        display_input(video)
    else:
        clear_status()
        status_var.set("Status : Idle")


def connect_stream():
    if check_host():
        url = str(
            "http://" + user_var.get() + ":" + pass_var.get() + "@" + address.get() + ":" + port.get() + para.get())
        video.open(url)
        if video.isOpened():
            clear_status()
            status_var.set("Status : Connected")
            opt_ch.set("Current Source : IP Webcam")
            save_loc.set("Save Location : " + userpath)
            con_add.set("Connected IP : " + address.get())
            con_port.set("Port : " + port.get())
            if user_var.get() != "":
                user_name.set("User : " + user_var.get())
            create_f5()
            display_input(video)
        else:
            tmsg.showerror("Error", "Wrong Credentials Or Parameter")
    else:
        clear_status()
        status_var.set("Status : Idle")


def connect():
    disconnect()
    cho = ch.get()
    if cho == "Webcam":
        connect_webcam()
    elif cho == "Stream":
        connect_stream()
    else:
        tmsg.showwarning("Error", "Please Choose One Option Before Connecting")


def clear(fr):
    address.set("")
    port.set("")
    user_var.set("")
    pass_var.set("")
    para.set("")
    for items in fr.winfo_children():
        items.destroy()


def refresh():
    clear(f3)
    cho = ch.get()
    if cho == "Webcam":
        Label(f3, text="Webcam ID : ", bg="pink", pady=5, padx=5).pack(side="left")
        Entry(f3, width=20, textvariable=address).pack(pady=5, side="left")
    elif cho == "Stream":
        Label(f3, text="Enter The IP Address : ", pady=5, bg="pink", padx=5).pack(side="left")
        Entry(f3, width=20, textvariable=address).pack(pady=5, side="left")
        Label(f3, text="Port : ", bg="pink", padx=5, pady=5).pack(side="left")
        Entry(f3, width=20, textvariable=port).pack(pady=5, side="left")
        Label(f3, text="Any Parameter : ", bg="pink", padx=5, pady=5).pack(side="left")
        Entry(f3, width=20, textvariable=para).pack(pady=5, side="left")
        Label(f3, text="Username : ", pady=5, bg="pink", padx=5).pack(side="left")
        Entry(f3, width=20, textvariable=user_var).pack(pady=5, side="left")
        Label(f3, text="Password : ", bg="pink", padx=5, pady=5).pack(side="left")
        Entry(f3, width=20, textvariable=pass_var, show="*").pack(pady=5, side="left")


def exit_win():
    ans = tmsg.askyesno("Confirm Exit", "Are you sure you want to exit?")
    if ans == YES:
        disconnect()
        root.destroy()


root = Tk()
root.title("Invisible Cloak")
root.iconbitmap("icon.ico")
root.state("zoomed")
root.geometry("900x600")
root.minsize(800, 600)
root.maxsize(1366, 768)
root.configure(bg="gray")

f0 = Frame(root, bg="black", borderwidth=5, relief=SUNKEN)
Label(f0, text="Invisible Cloak", font=("3Dumb", 22, "bold"), bg="black", fg="orange").pack()
f0.pack(fill="x")

option_frame = Frame(root, pady=2, bg="pink")
ch = StringVar()
ch.set("None")
Radiobutton(option_frame, text="Webcam", padx=14, variable=ch, value="Webcam", bg="pink").pack(side="left")
Radiobutton(option_frame, text="Stream Webcam", padx=14, variable=ch, value="Stream", bg="pink").pack(side="left")
option_frame.pack(anchor="w", fill="x")

address = StringVar()
port = StringVar()
para = StringVar()
user_var = StringVar()
pass_var = StringVar()
f3 = Frame(root, bg="pink", padx=10)
f3.pack(anchor="w", fill="x")

f4 = Frame(root, bg="orange", pady=5, padx=5)
Button(f4, text="Connect", command=connect).pack(side="left", padx=5)
Button(f4, text="Disconnect", command=disconnect).pack(side="left", padx=5)
Button(f4, text="Refresh", command=refresh).pack(side="left", padx=5)
Button(f4, text="Help", command=open_help).pack(side="left", padx=5)
Button(f4, text="Exit", command=exit_win).pack(side="left", padx=5)
f4.pack(fill="x")

rec = IntVar()
rec.set(0)
f5 = Frame(root, bg="yellow", pady=5, padx=5, height=30)
f5.pack(fill="x")

f1 = Frame(root, bg="black", padx=5)
input_frame = Label(f1, pady=5, bg="black", fg="white")
input_frame.pack(side="left")
output_frame = Label(f1, pady=5, bg="black", fg="white")
output_frame.pack()
f1.pack(anchor="w", fill="x")

status_var = StringVar()
opt_ch = StringVar()
con_add = StringVar()
con_port = StringVar()
user_name = StringVar()
is_rec = StringVar()
save_loc = StringVar()

status_var.set("Status : Idle")
status_fr = Frame(root, bg="black")
status = Label(status_fr, textvariable=status_var, bg="black", fg="white", padx=20)
status.pack(side="left")
option_choose = Label(status_fr, textvariable=opt_ch, bg="black", fg="white", padx=20)
option_choose.pack(side="left")
con_to = Label(status_fr, textvariable=con_add, bg="black", fg="white", padx=20)
con_to.pack(side="left")
conn_port = Label(status_fr, textvariable=con_port, bg="black", fg="white", padx=20)
conn_port.pack(side="left")
con_user = Label(status_fr, textvariable=user_name, bg="black", fg="white", padx=20)
con_user.pack(side="left")
isrec = Label(status_fr, textvariable=is_rec, bg="black", fg="white", padx=20)
isrec.pack(side="right")
sv_lo = Label(status_fr, textvariable=save_loc, bg="black", fg="white", padx=20)
sv_lo.pack(side="right")
status_fr.pack(side="bottom", fill="x")

root.mainloop()
video.release()
cv2.destroyAllWindows()
