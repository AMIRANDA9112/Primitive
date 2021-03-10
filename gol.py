def _highlight(results):
    from kivy.graphics import Color, Rectangle, Canvas
    from kivy.core.window import Window
    if not hasattr(Window, "_telenium_canvas"):
        Window._telenium_canvas = Canvas()
    _canvas = Window._telenium_canvas

    Window.canvas.remove(_canvas)
    Window.canvas.add(_canvas)

    _canvas.clear()
    with _canvas:
        Color(1, 0, 0, 0.5)
        for widget, bounds in results:
            left, bottom, right, top = bounds
            Rectangle(pos=(left, bottom), size=(right-left, top-bottom))

