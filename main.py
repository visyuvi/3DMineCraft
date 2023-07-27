# import libraries
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

# create an instance of the  ursina app
app = Ursina()

# define game variables
selected_block = "grass"

# create player
player = FirstPersonController(
    mouse_sensitivity=Vec2(100, 100),
    position=(0, 5, 0)
)

block_textures = {
    "grass": load_texture("assets/textures/groundEarth.png"),
    "dirt": load_texture("assets/textures/groundMud.png"),
    "stone": load_texture("assets/textures/wallStone.png"),
    "bedrock": load_texture("assets/textures/stone07.png")
}


class Block(Entity):
    def __init__(self, position, block_type):
        super().__init__(
            position=position,
            model="assets/models/block_model",
            scale=1,
            origin_y=-0.5,
            texture=block_textures.get(block_type),
            collider="box"
        )
        self.block_type = block_type


mini_block = Entity(
    parent=camera,
    model="assets/models/block_model",
    scale=0.2,
    texture=block_textures.get(selected_block),
    position=(0.35, -0.25, 0.5),
    rotation=(-15, -30, -5)
)

# create the ground
for x in range(-10, 10):
    for z in range(-10, 10):
        block = Block((x, 0, z), "bedrock")


def input(key):
    global selected_block
    # place block
    if key == "left mouse down":
        hit_info = raycast(camera.world_position, camera.forward, distance=10)
        if hit_info.hit:
            block = Block(hit_info.entity.position + hit_info.normal, selected_block)

    # delete block
    if key == "right mouse down" and mouse.hovered_entity:
        if not mouse.hovered_entity.block_type == "bedrock":
            destroy(mouse.hovered_entity)

    # change block type
    if key == "1":
        selected_block = "grass"
    if key == "2":
        selected_block = "dirt"
    if key == "3":
        selected_block = "stone"


def update():
    mini_block.texture = block_textures.get(selected_block)

# run the app
app.run()
