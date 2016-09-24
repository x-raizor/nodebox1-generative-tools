import os
import sys
import noise
import random
import poisson_disk_sampling

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
var("print_state", BUTTON)


pathname = os.path.dirname(sys.argv[0])
images_list = files(pathname + "/../assets/petridish/*.jpg")

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


def particle_picture(_x, _y, width, height):
    ''' (float, float, float, float) -> void
        params: 
        x coordinate of center,
        y coordinate of center, 
        particle width,
        particle height 
    '''
    image_name = choice(images_list)
    layer = cnv.append(image_name, x = _x, y = _y, w = width, h = height)
    
    # Blending mode: https://www.nodebox.net/code/index.php/Core_Image#blend_modes
    layer.blend_darken()
    
    # Filters: https://www.nodebox.net/code/index.php/Core_Image#filters
    #layer.blur = 20 * random.random()
    
    
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
        else:
            particle_circle(x, y, width, height)

    if use_images:
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


