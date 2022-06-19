import pyglet
from pyglet import shapes

window = pyglet.window.Window(800, 600)

car_x = 200
car_y = 200

@window.event
def on_key_press(symbol, modifiers):    
    global car_x
    global car_y

    LEFT = 65361
    TOP = 65362
    RIGHT = 65363
    BOTTOM = 65364
    SPEED = 10
    if symbol == LEFT:
        car_x -= SPEED
    if symbol == TOP:
        car_y += SPEED
    if symbol == RIGHT:
        car_x += SPEED
    if symbol == BOTTOM:
        car_y -= SPEED
    
    print(car_x)
    print(car_y)

@window.event
def on_draw():
    print("drawing")
    batch = pyglet.graphics.Batch()
    car = shapes.Rectangle(x=car_x, y=car_y, width=25, height=50, color=(255, 55, 55), batch=batch)
    goal = shapes.Rectangle(x=700, y=500, width=25, height=50, color=(55, 255, 55), batch=batch)
    window.clear()
    batch.draw()

pyglet.app.run()
