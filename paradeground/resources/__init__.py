import pyglet

#pyglet.resource.path = ["../resources"]
#pyglet.resource.reindex()

# image tools
def center_image(image):
    image.anchor_x = image.width/2
    image.anchor_y = image.height/2
    return image

def uncenter_image(image):
    image.anchor_x = 0
    image.anchor_y = 0
    return image
	
# IMAGES
# invisible specks
mote = pyglet.resource.image("mote.png")

# defaults
thirty = pyglet.resource.image("30.png")