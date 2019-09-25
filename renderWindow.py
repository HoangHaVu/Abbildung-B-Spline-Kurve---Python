import os
import glfw
from OpenGL.GL import *

from scene import Scene


class RenderWindow:
    """GLFW Rendering window class"""

    def __init__(self, width, height):

        # save current working directory
        cwd = os.getcwd()

        # Initialize the library
        if not glfw.init():
            return

        # restore cwd
        os.chdir(cwd)

        # buffer hints
        glfw.window_hint(glfw.DEPTH_BITS, 32)

        # define desired frame rate
        self.frame_rate = 100

        # make a window
        self.width, self.height = width, height
        self.aspect = self.width / float(self.height)
        glfw.window_hint(glfw.RESIZABLE, False)
        self.window = glfw.create_window(self.width, self.height, "Abgabe 3",
                                         None, None)

        if not self.window:
            glfw.terminate()
            return

        # Make the window's context current
        glfw.make_context_current(self.window)

        # initialize GL
        glViewport(0, 0, self.width, self.height)
        glEnable(GL_DEPTH_TEST)
        glClearColor(1, 1, 1, 1)
        glMatrixMode(GL_PROJECTION)

        glMatrixMode(GL_MODELVIEW)

        # set window callbacks
        glfw.set_mouse_button_callback(self.window, self.onMouseButton)
        glfw.set_cursor_pos_callback(self.window, self.onMouseMove)
        glfw.set_key_callback(self.window, self.onKeyboard)

        # exit flag
        self.exit_now = False
        self.mousePosition = (0, 0)
        self.shiftPressed = False


        self.scene = Scene()


    def onMouseButton(self, win, button, action, mods):
        if button == glfw.MOUSE_BUTTON_LEFT:
            if action == glfw.RELEASE:
                self.scene.makePoint(self.mousePosition[0],
                                     self.mousePosition[1])

        elif button == glfw.MOUSE_BUTTON_RIGHT:
            if action == glfw.RELEASE:
                self.scene.pop_lastPoint()


    def onMouseMove(self, win, pos_x, pos_y):
        x = pos_x / self.width * 2 - 1
        y = (pos_y / self.width * 2 - 1) * -1
        self.mousePosition = (x, y)

    def onKeyboard(self, win, key, scan_code, action, mods):
        if key == glfw.KEY_LEFT_SHIFT or key == glfw.KEY_RIGHT_SHIFT:
            if action == glfw.PRESS:
                self.shiftPressed = True
                return

            if action == glfw.RELEASE:
                self.shiftPressed = False
                return

            return

        if key == glfw.KEY_BACKSPACE or key == glfw.KEY_DELETE:
            self.scene.deletePoints()

        if action != glfw.PRESS:
            return

        # ESC to quit
        if key == glfw.KEY_ESCAPE:
            self.exit_now = True
            return

        if key == glfw.KEY_M:
            if action == glfw.PRESS:
                if self.shiftPressed:
                    self.scene.add_curvePoint()
                else:
                    self.scene.remove_curvePoint()
            return

        if key == glfw.KEY_K:
            if action == glfw.PRESS:
                if self.shiftPressed:
                    self.scene.add_order()
                else:
                    self.scene.remove_order()
            return



    def run(self):
        # initializer timer
        glfw.set_time(0.0)
        time = 0.0

        while not glfw.window_should_close(self.window) and not self.exit_now:
            # update every x seconds
            now = glfw.get_time()
            if now - time > 1.0 / self.frame_rate:
                # update time
                time = now

                # clear
                glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

                self.scene.render()

                glfw.swap_buffers(self.window)

                # Poll for and process events
                glfw.poll_events()
        # end
        glfw.terminate()
