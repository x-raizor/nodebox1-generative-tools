from __future__ import division
import os
import sys
import noise
import random
import poisson_disk_sampling

svg = ximport("svg")
clr = ximport("colors")
noise = ximport("noise")
coreimage = ximport("coreimage")


# Nodebox UI controls
var("canvas_width", TEXT, "500")
var("canvas_height", TEXT, "500")
var("particle_size", NUMBER, 6, 2, 100)
var("particles_distance", NUMBER, 15, 5, 100)
var("particle_size_dispersion", NUMBER, 2, 0, 50)
var("use_perlin_noise_for_size", BOOLEAN, False)
var("perlin_noise_scale", NUMBER, 0.1, 0.01, 1)
var("use_images", BOOLEAN, False)
var("with_blend", BOOLEAN, False)
var("use_shapes", BOOLEAN, False)
var("print_state", BUTTON)


pathname = os.path.dirname(sys.argv[0])
images_list = files(pathname + "/../assets/petridish/*.jpg")
shapes_list = files(pathname + "/../assets/clouds/*.svg")

colors = [
    clr.hex("#85bf00"),
    clr.hex("#ffa000"),
    clr.hex("#ff4338"),
    clr.hex("#aa4d9d"),
    clr.hex("#00b9f2")
]


def particle_circle(x, y, width, height):
    ''' (float, float, float, float) -> void
        params: 
        x coordinate of center,
        y coordinate of center, 
        particle width,
        particle height 
    '''
    oval(x, y, width, height)


def particle_picture(_x, _y, _width, _height):
    ''' (float, float, float, float) -> void
        params: 
        x coordinate of center,
        y coordinate of center, 
        particle width,
        particle height 
    '''
    image_name = choice(images_list)
    if with_blend:
        layer = cnv.append(image_name, x = _x, y = _y, w = _width, h = _height)
        
        # Blending mode: https://www.nodebox.net/code/index.php/Core_Image#blend_modes
        layer.blend_darken()
    
        # Filters: https://www.nodebox.net/code/index.php/Core_Image#filters
        #layer.blur = 20 * random.random()
    else:
        image(image_name, _x, _y, width = _width, height = _height)


def drawpaths(paths=[], x=0, y=0, rotate=0, scale=1.0, origin=(0.5,0.5)):
    ''' Draws a group of paths that rotate and scale from the given origin.
    '''
    _ctx.transform(CORNER)
    _ctx.push()
    _ctx.translate(x, y)
    _ctx.rotate(rotate)
    _ctx.scale(scale)
    (x, y), (w, h) = bounds(paths)
    _ctx.translate((-x-w)*origin[0], (-y-h)*origin[1])
    for path in paths:
       # Use copies of the paths that adhere to the transformations.
       _ctx.drawpath(path.copy())
    _ctx.pop()


def bounds(paths=[]):
  ''' Returns (x, y), (width, height) bounds for a group of paths.
  '''
  if len(paths) == 0: 
    return (0,0), (0,0)
  l = t = float("inf")
  r = b = float("-inf")
  for path in paths:
    (x, y), (w, h) = path.bounds
    l = min(l, x)
    t = min(t, y)
    r = max(r, x+w)
    b = max(b, y+h)
  return (l, t), (r-l, b-t)
  
   
def particle_shape(_x, _y, _width, _height):
    ''' (float, float, float, float) -> void
        params: 
        x coordinate of center,
        y coordinate of center, 
        particle width,
        particle height 
    '''
    image_name = choice(shapes_list)
    data = open(image_name).read()
    paths = svg.parse(data)
    origin, (w, h) = bounds(paths)
    if w == 0:
        w = 1
    drawpaths(paths, x = _x, y = _y, rotate = 0, scale = _width / w)

    
    
def print_state():
    print particle_size, particles_distance, particle_size_dispersion, perlin_noise_scale
    regenerate()
    
    
def regenerate():
    for x, y in sample:
        fill(choice(colors))
        if use_perlin_noise_for_size:
            ratio = noise.generate(x, y, width = WIDTH, height = HEIGHT, scale = perlin_noise_scale)
            width = ratio * particle_size
        else:
            width = random.randint(particle_size - particle_size_dispersion,
                                particle_size + particle_size_dispersion)
        height = width
    
        if use_images:
            particle_picture(x, y, width, height)
        elif use_shapes: 
            particle_shape(x, y, width, height)
        else:
            particle_circle(x, y, width, height)

    if use_images and with_blend:
        cnv.draw(0, 0)


particle_size = int(particle_size)
particle_size_dispersion = int(particle_size_dispersion)
particles_distance = int(particles_distance)
canvas_width = int(canvas_width)
canvas_height = int(canvas_height)


obj = poisson_disk_sampling.pds(WIDTH, HEIGHT, particles_distance, 5)
sample = obj.rvs()

if use_images:
    cnv = coreimage.canvas(canvas_width, canvas_height)
    cnv.append(color(255))
else:
    size(canvas_width, canvas_height)
    background(255)

regenerate()


