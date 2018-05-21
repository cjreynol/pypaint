from tkinter import (Button, Canvas, Frame, Label, Scale, Tk, 
                        ALL, BOTH, HORIZONTAL, LEFT, RIGHT, ROUND, RAISED)

from pypaint.drawing_type import DrawingType


class PaintView:
    """
    Manages the Tkinter window and its widgets.
    """

    WINDOW_TITLE = "PyPaint"

    FRAME_BORDER_WIDTH = 2
    FRAME_WIDTH = 120
    TOOL_LABEL_TEXT = "Current Tool:\n"

    THICKNESS_LABEL_TEXT = "Thickness"
    THICKNESS_MIN = 1
    THICKNESS_MAX = 10

    CANVAS_HEIGHT = 600
    CANVAS_WIDTH = 800

    ERASER_COLOR= "#ffffff"

    PEN_BUTTON_TEXT = "Pen"
    RECT_BUTTON_TEXT = "Rectangle"
    OVAL_BUTTON_TEXT = "Oval"
    LINE_BUTTON_TEXT = "Line"
    ERASER_BUTTON_TEXT = "Eraser"
    CLEAR_BUTTON_TEXT = "Clear"

    LINE_WIDTH = 5

    def __init__(self):
        """
        Create the Tkinter window, then create and place the widgets in it.
        """
        self.root = self._create_root()
        self._initialize_widgets()
        self._place_widgets()

    def _create_root(self):
        """
        Return the root window with the proper attributes set.
        """
        root = Tk()
        root.title(self.WINDOW_TITLE)
        return root

    def _initialize_widgets(self):
        """
        Instantiate the widgets for the GUI.
        """
        self.canvas = Canvas(self.root, width = self.CANVAS_WIDTH, 
                                height = self.CANVAS_HEIGHT)
        self.toolbar = Frame(self.root, width = self.FRAME_WIDTH, 
                                relief = RAISED, bd = self.FRAME_BORDER_WIDTH)
        self.current_tool_label = Label(self.toolbar, 
                                            text = self.TOOL_LABEL_TEXT)
        self.pen_button = Button(self.toolbar, text = self.PEN_BUTTON_TEXT)
        self.rect_button = Button(self.toolbar, text = self.RECT_BUTTON_TEXT)
        self.oval_button = Button(self.toolbar, text = self.OVAL_BUTTON_TEXT)
        self.line_button = Button(self.toolbar, text = self.LINE_BUTTON_TEXT)
        self.eraser_button = Button(self.toolbar, 
                                        text = self.ERASER_BUTTON_TEXT)
        self.clear_button = Button(self.toolbar, 
                                    text = self.CLEAR_BUTTON_TEXT)
        self.thickness_label = Label(self.toolbar, 
                                        text = self.THICKNESS_LABEL_TEXT)
        self.thickness_scale = Scale(self.toolbar, from_ = self.THICKNESS_MIN, 
                                        to = self.THICKNESS_MAX, 
                                        orient = HORIZONTAL)

    def _place_widgets(self):
        """
        Use a geometry manager to put the widgets in the root window.
        """
        self.canvas.pack(side = RIGHT, fill = BOTH, expand = True)
        self.toolbar.pack(side = LEFT, fill = BOTH, expand = True)
        self.current_tool_label.pack()
        for button in [self.pen_button, self.rect_button, self.oval_button, 
                        self.line_button, self.eraser_button, 
                        self.clear_button]:
            button.pack()
        self.thickness_label.pack()
        self.thickness_scale.pack()

    def bind_canvas_callback(self, event_id, callback):
        """
        Register the callback for the given event.
        """
        self.canvas.bind(event_id, callback)

    def bind_tool_button_callbacks(self, pen, rect, oval, line, eraser, clear):
        """
        Register the callbacks for the toolbar buttons.
        """
        self.pen_button["command"] = pen
        self.rect_button["command"] = rect
        self.oval_button["command"]= oval
        self.line_button["command"] = line
        self.eraser_button["command"]= eraser
        self.clear_button["command"]= clear

    def bind_thickness_scale_callback(self, callback):
        """
        Register the callback for the thickness scale.
        """
        self.thickness_scale["command"] = callback

    def bind_quit_callback(self, callback):
        """
        Set the callback for when the window closes.
        """
        self.root.protocol("WM_DELETE_WINDOW", callback)

    def start(self):
        """
        Start the GUI's update loop.
        """
        self.root.mainloop()

    def draw_shape(self, drawing):
        """
        Determine and call the appropriate drawing function based on the 
        shape type.

        Used when drawings are received over the network.
        """
        if drawing.shape == DrawingType.PEN:
            self.draw_line(drawing.coords, drawing.thickness)
        elif drawing.shape == DrawingType.RECT:
            self.draw_rect(drawing.coords, drawing.thickness)
        elif drawing.shape == DrawingType.OVAL:
            self.draw_oval(drawing.coords, drawing.thickness)
        elif drawing.shape == DrawingType.LINE:
            self.draw_line(drawing.coords, drawing.thickness)
        elif drawing.shape == DrawingType.ERASER:
            self.draw_eraser_line(drawing.coords, drawing.thickness)
        elif drawing.shape == DrawingType.CLEAR:
            self.clear_canvas()
        else:
            raise RuntimeError("Unexpected shape type {}".format(drawing.shape))

    def draw_rect(self, coords, thickness):
        """
        Draw a rectangle using the opposite corner pairs specified in coords.
        """
        return self.canvas.create_rectangle(*coords, width = thickness)

    def draw_oval(self, coords, thickness):
        """
        Draw an oval using the corners specificed in coords.
        """
        return self.canvas.create_oval(*coords, width = thickness)

    def draw_line(self, coords, thickness):
        """
        Draw a line with the start/end pairs specified in coords.
        """
        return self.canvas.create_line(*coords, width = thickness, 
                                        capstyle = ROUND)

    def draw_eraser_line(self, coords, thickness):
        """
        Draw a line that is white, to "erase" previous drawings.
        """
        return self.canvas.create_line(*coords, width = thickness,
                                        capstyle = ROUND, 
                                        fill = self.ERASER_COLOR)

    def clear_drawing_by_id(self, drawing_id):
        """
        Delete the drawing with the given id from the canvas.
        """
        self.canvas.delete(drawing_id)

    def clear_canvas(self):
        """
        Clear the canvas of all drawings.
        """
        self.canvas.delete(ALL)

    def update_tool_text(self, text):
        """
        Update the toolbar label text with its default text + the given text.
        """
        self.current_tool_label["text"] = self.TOOL_LABEL_TEXT + text
