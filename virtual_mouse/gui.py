import cv2
import tkinter as tk
from PIL import Image, ImageTk

# Global variable to store user's selected camera
USER_CAMERA = None

# Function to get the list of available cameras
def get_cameras():
    index = 0
    arr = []
    while True:
        cap = cv2.VideoCapture(index, cv2.CAP_DSHOW)
        if not cap.read()[0]:
            break
        else:
            arr.append(index)
        cap.release()
        index += 1
    return arr

# Function to handle camera selection
def select_camera(index):
    global USER_CAMERA
    USER_CAMERA = index
    root.destroy()

# Mouse callback function to draw the rectangle
def draw_rectangle(event, x, y, flags, param):
    global top_left_pt, bottom_right_pt
    if event == cv2.EVENT_LBUTTONDOWN:
        top_left_pt = (x, y)
    elif event == cv2.EVENT_LBUTTONUP:
        bottom_right_pt = (x, y)


def main():
    global root
    # Initialize the main window
    root = tk.Tk()
    root.title("Camera Viewer")

    # Add buttons for available cameras
    cameras = get_cameras()
    for idx in cameras:
        button = tk.Button(root, text=f"Camera {idx}", command=lambda i=idx: select_camera(i))
        button.pack()

    if len(cameras) == 0:
        button = tk.Button(root, text="No camera for your computer please check your device", command=root.destroy)
        button.pack()

    root.mainloop()

    # After closing Tkinter window, show the video from the selected camera
    if USER_CAMERA is not None:
        cap = cv2.VideoCapture(USER_CAMERA, cv2.CAP_DSHOW)
        cv2.namedWindow("Camera Feed")
        cv2.setMouseCallback("Camera Feed", draw_rectangle)

        while True:
            ret, frame = cap.read()
            if ret:
                if top_left_pt is not None and bottom_right_pt is not None:
                    cv2.rectangle(frame, top_left_pt, bottom_right_pt, (0, 255, 0), 2)
                cv2.imshow("Camera Feed", frame)

                key = cv2.waitKey(1)
                if key & 0xFF == ord('q'): # Press 'q' to quit
                    break
                elif key & 0xFF == ord('d'): # Press 'd' for final decision
                    global final_selection
                    final_selection = True
                    break
            else:
                break

        cap.release()
        cv2.destroyAllWindows()

        if final_selection:
            print(f"Final Selection: Top Left: {top_left_pt}, Bottom Right: {bottom_right_pt}")


if __name__ == "__main__":
    main()
