import cv2

x_pos: int
y_pos: int


def pos(image_path):
    # Callback function for mouse events
    def mouse_callback(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:

            globals()['x_pos'] = x
            globals()['y_pos'] = y



    image = cv2.imread(image_path)

    # Create a window and set the mouse callback
    cv2.namedWindow("Select Position")
    cv2.setMouseCallback("Select Position", mouse_callback)

    # Display the image
    cv2.imshow("Select Position", image)

    # Wait for a key event
    cv2.waitKey(0)

    # Close the window
    cv2.destroyAllWindows()

    return (x_pos, y_pos)
