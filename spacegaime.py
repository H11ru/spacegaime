

import pygame
import math
import random
import numpy as np # For matrix operations


triangular_magic = 25872391 # ???
trhia_m_flag = 0b100 | 0b100000 # what did thsi do
nonrueguwh997h3qHARHHohfow = (76, 76, 76) # what was this color again?
# Initialize Pygame
pygame.init()

# Constants
WINDOW_SIZE = (960, 540) # This is a bapple
TILE_SIZE = 50
CAMERA_FRICTION = 0.8
MOVEMENT_SPEED_NORM = 5
MOVEMENT_SPEED_FAST = 2
MOVEMENT_SPEED_DBUG = 6
MOVEMENT_SPEED_SLOW = 0.25
RETURN_SPEED = 0.1 # Higher value = faster return to originf
MIN_DISTANCE = 1e-7

# Setup display
screen = pygame.Surface(WINDOW_SIZE)
# import a module to find the monitor size so we can scale up the window if the monitor supports it
import screeninfo
monitor = screeninfo.get_monitors()[0]  # Get the primary monitor
width, height = monitor.width, monitor.height

scale = min(width / WINDOW_SIZE[0], height / WINDOW_SIZE[1])
scale = int(scale)
if scale < 1:
    print("WHAT")
else:
    print("going with size", scale, "for the window")
    print("cant go with ", scale+1, "because that size, (" + str(WINDOW_SIZE[0] * (scale + 1)) + ", " + str(WINDOW_SIZE[1] * (scale + 1)) + ") is bigger than the monitor size (" + str(width) + ", " + str(height) + ")")

realscreen = pygame.display.set_mode((WINDOW_SIZE[0] * scale, WINDOW_SIZE[1] * scale), pygame.RESIZABLE)
clock = pygame.time.Clock()

# Camera state
fcamera = {
    'x': 0,
    'y': 0,
    'tx': 0, # Target x position
    'ty': 0, # Target y position
}

stars = [] # ((color, color, color), x, y, distance, size multiplier)
REPEAT_HIDER = 4 # Increase if you can easily see the stars repeating


# Star type configurations
STAR_TYPES = {
    'white_dwarf': {
        'count': 15,
        'color': (255, 255, 255),
        'distance_range': (195, 375), # Multiplied by 15
        'size_range': (0.1, 0.2)
    },
    'red_dwarf': {
        'count': 20,
        'color': (255, 160, 160),
        'distance_range': (180, 330), # Multiplied by 15
        'size_range': (0.1, 0.15)
    },
    'blue_giant': {
        'count': 3,
        'color': (150, 170, 255),
        'distance_range': (210, 600), # Multiplied by 15
        'size_range': (0.5, 0.7)
    },
    'red_giant': {
        'count': 4,
        'color': (255, 100, 100),
        'distance_range': (225, 570), # Multiplied by 15
        'size_range': (0.4, 0.6)
    },
    'yellow_star': {
        'count': 12,
        'color': (255, 255, 180),
        'distance_range': (195, 360), # Multiplied by 15
        'size_range': (0.2, 0.3)
    },
    'orange_star': {
        'count': 8,
        'color': (255, 200, 120),
        'distance_range': (210, 390), # Multiplied by 15
        'size_range': (0.25, 0.35)
    },
    'neutron_star': {
        'count': 2,
        'color': (200, 200, 255),
        'distance_range': (270, 675), # Multiplied by 15
        'size_range': (0.15, 0.2)
    },
    'binary_star': {
        'count': 1,
        'color': (255, 230, 180),
        'distance_range': (90, 300), # Multiplied by 15
        'size_range': (0.3, 0.4)
    }
}


THINGIE = 5

# thingie also skews the counts
for star_type in STAR_TYPES.values():
    star_type['count'] *= THINGIE

# Add black holeS
#stars.append(((0, 0, 0), random.uniform(0, WINDOW_SIZE[0]), random.uniform(0, WINDOW_SIZE[1]), 1, random.uniform(0.5, 0.7), 1)) # Old code. only adds on (sad)
# Add black holes to the star types
# Black hole config also needs adjustment
STAR_TYPES['black_hole'] = {
    'count': 1,
    'color': (0, 0, 0),
    'distance_range': (90, 135), # Multiplied by 15
    'size_range': (0.1, 0.2), # Larger size for black holes
    'one': 1

}

def generate_stars(star_type_config, repeat_hider):
    """Generate stars based on configuration"""
    generated_stars = []
    count = star_type_config['count']
    
    for i in range(repeat_hider ** 2 * count):
        # Generate stars in each repeat section
        screen_x = random.randint(0, repeat_hider)
        screen_y = random.randint(0, repeat_hider)
        in_screen_x = random.randint(0, WINDOW_SIZE[0] - 1)
        in_screen_y = random.randint(0, WINDOW_SIZE[1] - 1)
        
        field_x = screen_x * WINDOW_SIZE[0] + in_screen_x
        field_y = screen_y * WINDOW_SIZE[1] + in_screen_y
        
        distance = random.uniform(*star_type_config['distance_range'])
        true_x = field_x * distance
        true_y = field_y * distance
        
        generated_stars.append((
            star_type_config['color'],
            true_x,
            true_y,
            distance,
            random.uniform(*star_type_config['size_range'])
        ))
        if 'one' in star_type_config and star_type_config['one'] == 1:
            # If this is a black hole, add an extra parameter for the black hole
            generated_stars[-1] += (1,)
    
    return generated_stars

# Generate all types of stars
popped = STAR_TYPES.pop("binary_star") # Pop binary star
stars = []
for star_type, config in STAR_TYPES.items():
    stars.extend(generate_stars(config, REPEAT_HIDER))

# Sort all stars by distance
stars.sort(key=lambda star: star[3]) # Sort by distance
# Except...
# Move all black holes to the front
# EFfect:  make all stars N times fautehr
# chang eeahcx star to be 2x further away by multiplying distance by THINGIE
#stars = [(star[0], star[1] * THINGIE, star[2] * THINGIE, star[3] * THINGIE, star[4]) for star in stars] # remember, star[0] is color, star[1] is x, star[2] is y, star[3] is distance, star[4] is size multiplier
#black_holes = [star for star in stars if len(star) == 6] # Black holes have 6 elements
#stars = [star for star in stars if len(star) < 6] # Remove black holes from the main list
#stars = stars + black_holes # Append black holes at the end so they render last -- on top

# add the sun (its very close (like 0.2) and beeger)
# REmember: color, x, y, distance, size_multiplier
stars.append(((247, 238, 15), 150 +150 + 15000 + 150 + 150 + 150 +  random.uniform(0, WINDOW_SIZE[0] / 10), 150 + 150 + 150 + 150 + 150 + 150 + 150 + 150 + 150 + 15000 + random.uniform(0, WINDOW_SIZE[1] / 10), 58, 4))
# also, because this is after the black holes are moved to the front, the sun will never hide behind any other celestial body. makes sense given how its the closest one here

# ADd NH-4b
# its a star
# its blue
# and farther
# but like half the size o th sun visual
stars.append(((82, 164, 199), 150 + 150 + 15000 + 150 + 150 + 150 + random.uniform(0, WINDOW_SIZE[0] / 10), 150 + 150 + 150 + 150 + 150 + 150 + random.uniform(0, WINDOW_SIZE[1] / 10), 132, 6))

# bg. its a surface. and its also beeg. like (REPEAT_HIDER * WINDOW_SIZE[0], REPEAT_HIDER * WINDOW_SIZE[1]) big.
# its made up of noise. that repeats. and is really dark
# like the brighest pixel is like (2, 7, 4) or something
# so its like a nebula effect
founte = pygame.font.Font(None, 24)
# THis is made using a noise funcito nthat supports tiling argument (so it repeats cleanly)



# Generate binary stars specially
for bstar in range(popped['count'] * REPEAT_HIDER ** 2):
    # Generate stars in each repeat section
    screen_x = random.randint(0, REPEAT_HIDER)
    screen_y = random.randint(0, REPEAT_HIDER)
    in_screen_x = random.randint(0, WINDOW_SIZE[0] - 1)
    in_screen_y = random.randint(0, WINDOW_SIZE[1] - 1)
    
    field_x = screen_x * WINDOW_SIZE[0] + in_screen_x
    field_y = screen_y * WINDOW_SIZE[1] + in_screen_y
    
    distance = random.uniform(*popped['distance_range'])
    true_x = field_x * distance
    true_y = field_y * distance
    
    # SPECIAL BIT: generate its pair, at a random angle from the first star, and a random distance (40 - 60 px in that direction)
    angle = random.uniform(0, 2 * math.pi) # Random angle in radians
    pair_distance = random.uniform(40, 60) # Random distance for the pair
    pair_x = true_x + pair_distance * math.cos(angle)
    pair_y = true_y + pair_distance * math.sin(angle)
    # Add both stars to the list
    stars.append((popped['color'], true_x, true_y, distance, random.uniform(*popped['size_range'])))
    stars.append((popped['color'], pair_x, pair_y, distance, random.uniform(*popped['size_range'])))

def sample_gradient(t, colors):
    """Sample a color from a gradient defined by a list of colors."""
    if len(colors) < 2:
        return colors[0] if colors else (0, 0, 0)
    
    # Calculate the segment length
    segment_length = 1 / (len(colors) - 1)
    segment_index = min(int(t / segment_length), len(colors) - 2)
    
    # Interpolate between the two colors
    ratio = (t - segment_index * segment_length) / segment_length
    color1 = colors[segment_index]
    color2 = colors[segment_index + 1]
    
    return (
        int(color1[0] + (color2[0] - color1[0]) * ratio),
        int(color1[1] + (color2[1] - color1[1]) * ratio),
        int(color1[2] + (color2[2] - color1[2]) * ratio)
    )

# Generate background nebula surface
bg_width = REPEAT_HIDER * WINDOW_SIZE[0]
bg_height = REPEAT_HIDER * WINDOW_SIZE[1]
bg = pygame.Surface((bg_width, bg_height))

OVERRIDE_PARALLAX = False # Set to True to disable parallax effect for testing

def parallax_stars(screen, camera):
    for star in stars:
        if len(star) == 6:
            """# Black hole rendering
            color, x, y, distance, size_multiplier, _ = star
            parallax_x = (x - camera['x']) / (distance if not OVERRIDE_PARALLAX else 1)
            parallax_y = (y - camera['y']) / (distance if not OVERRIDE_PARALLAX else 1)
            wrapped_x = parallax_x % (REPEAT_HIDER * WINDOW_SIZE[0]) - 50
            wrapped_y = parallax_y % (REPEAT_HIDER * WINDOW_SIZE[1]) - 50
              # Calculate base radius
            base_rad = int(TILE_SIZE * (size_multiplier / distance))
              # Create more efficient surface just big enough for the effect
            bh_size = base_rad * 4
            bh_surf = pygame.Surface((bh_size * 2, bh_size * 2), pygame.SRCALPHA)
            bh_surf.fill((0, 0, 0, 0))
            
            # Draw event horizon (pure black circle) first
            pygame.draw.circle(bh_surf, (0, 0, 0), (bh_size, bh_size), base_rad)
            
            # Draw accretion disk with proper brightness (brighter near center)
            disk_surf = pygame.Surface((bh_size * 2, bh_size * 2), pygame.SRCALPHA)
            disk_inner = pygame.draw.ellipse(disk_surf, (255, 255, 200, 200), # Hot white-yellow
                                          (bh_size - base_rad * 1.5, bh_size - base_rad * 0.4,
                                           base_rad * 3, base_rad * 0.8))
            disk_middle = pygame.draw.ellipse(disk_surf, (255, 150, 0, 160), # Orange
                                          (bh_size - base_rad * 2, bh_size - base_rad * 0.5,
                                           base_rad * 4, base_rad))
            disk_outer = pygame.draw.ellipse(disk_surf, (200, 50, 0, 100), # Dark red
                                          (bh_size - base_rad * 2.5, bh_size - base_rad * 0.6,
                                           base_rad * 5, base_rad * 1.2))
                                           
            # Simple glow effect (dimmer now)
            for i in range(3):
                alpha = int(100 * (1 - i/3))
                pygame.draw.circle(bh_surf, 
                                (100, 50, 0, alpha), 
                                (bh_size, bh_size), 
                                int(base_rad * (2.5 - i/3)))
            
            # Rotate slightly for perspective
            rotated = pygame.transform.rotate(disk_surf, 15)
            bh_surf.blit(rotated, (bh_size - rotated.get_width()//2, 
                                  bh_size - rotated.get_height()//2))
            
            # Draw event horizon (pure black circle)
            pygame.draw.circle(bh_surf, (0, 0, 0), (bh_size, bh_size), base_rad)
            
            # Draw the final surface
            screen.blit(bh_surf, 
                    (int(wrapped_x - bh_size), 
                     int(wrapped_y - bh_size)))
            continue"""
            # Draw a red circle
            color, x, y, distance, size_multiplier, _ = star
            parallax_x = (x - camera['x']) / (distance if not OVERRIDE_PARALLAX else 1)
            parallax_y = (y - camera['y']) / (distance if not OVERRIDE_PARALLAX else 1)
            wrapped_x = parallax_x % (REPEAT_HIDER * WINDOW_SIZE[0]) - 50
            wrapped_y = parallax_y % (REPEAT_HIDER * WINDOW_SIZE[1]) - 50
            # Draw the black hole as a red circle
            rad = int(TILE_SIZE * (size_multiplier / distance))
            pygame.draw.circle(screen, (32, 0, 0), (int(wrapped_x), int(wrapped_y)), (rad + 4) if rad > 0 else (rad + 5))
            pygame.draw.circle(screen, (48, 32, 0), (int(wrapped_x), int(wrapped_y)), (rad + 3) if rad > 0 else (rad + 4))
            pygame.draw.circle(screen, (128, 64, 32), (int(wrapped_x), int(wrapped_y)), (rad + 2) if rad > 0 else (rad + 3))
            pygame.draw.circle(screen, (230, 230, 230), (int(wrapped_x), int(wrapped_y)), (rad + 1) if rad > 0 else (rad + 2))
            pygame.draw.circle(screen, (0, 0, 0), (int(wrapped_x), int(wrapped_y)), rad if rad > 0 else 1)
            continue
        color, x, y, distance, size_multiplier = star
        # Calculate parallax effect based on distance, and wrap around based on repeat hider
        parallax_x = (x - camera['x']) / (distance if not OVERRIDE_PARALLAX else 1)
        parallax_y = (y - camera['y']) / (distance if not OVERRIDE_PARALLAX else 1)
        # The sun is special in that it does not wrap around
        # Wrap around the repeat hider texture
        if color == (247, 238, 15) or color == (82, 164, 199): # Sun color specifically (no other stars are this color)
            wrapped_x = parallax_x - 50 # directly
            wrapped_y = parallax_y - 50
        else:

            wrapped_x = parallax_x % (REPEAT_HIDER * WINDOW_SIZE[0]) - 50
            wrapped_y = parallax_y % (REPEAT_HIDER * WINDOW_SIZE[1]) - 50
        # this means if you fly off, it will never appear again unless go go back to the origin
        # Draw the star
        rad = int((TILE_SIZE * (size_multiplier / distance)) * (15 if not color in [(247, 238, 15),(82, 164, 199)] else 3)) # Make the sun bigger
        if rad < 2:
            # LQ
            pygame.draw.circle(screen, color, (int(wrapped_x), int(wrapped_y)), rad)
        elif rad < 8:
            # MQ
            # first draw a 1.4x scale 50% opacity circle
            # then a 0.7x scale full opacity circle
            
            beeg_surf = pygame.Surface((rad * 4, rad * 4), pygame.SRCALPHA)
            beeg_surf.fill((0, 0, 0, 0)) # Transparent background
            # Draw the larger circle with 50% opacity
            pygame.draw.circle(beeg_surf, (*color, 128), (2*rad, 2*rad), int(rad * 1.4))
            # Draw the smaller circle with full opacity
            pygame.draw.circle(beeg_surf, color, (2*rad, 2*rad), int(rad * 0.7))
            screen.blit(beeg_surf, (int(wrapped_x - 2*rad), int(wrapped_y - 2*rad)))
        else:
                        # HQ
            # Draw many circles with decreasing opacity using a for loop for bloom
            for i in range(3):
                bloom_surf = pygame.Surface((rad * 7, rad * 7), pygame.SRCALPHA)
                bloom_surf.fill((0, 0, 0, 0)) # Transparent background
                
                # Calculate size and opacity for each bloom layer
                layer_sizes = [rad * 2.5, rad * 2, rad * 1.5]
                # Make layer alpahs drop off using the square law not by halving because thats how light spreads out in 3d
                # so the first one is gona be at 50%, the second at 15% and the third at 7%
                layer_opacities = [128, 38, 18][::-1] # reverse symbol

                # sample the arrays
                bloom_size = layer_sizes[i]
                opacity = layer_opacities[i]
                
                # Draw bloom layer
                pygame.draw.circle(bloom_surf, 
                                (*color, opacity),
                                (rad * 3.5, rad * 3.5),
                                bloom_size)
                
                # Draw the bloom surface
                screen.blit(bloom_surf, 
                        (int(wrapped_x - rad * 3.5),
                        int(wrapped_y - rad * 3.5)))
            
            # Draw core of the star
            core_surf = pygame.Surface((rad * 2, rad * 2), pygame.SRCALPHA)
            core_surf.fill((0, 0, 0, 0))
            def clerp(color1, color2, t):
                """Linear interpolation between two colors."""
                return (
                    int(color1[0] + (color2[0] - color1[0]) * t),
                    int(color1[1] + (color2[1] - color1[1]) * t),
                    int(color1[2] + (color2[2] - color1[2]) * t)
                )
            pygame.draw.circle(core_surf, clerp(color, (255, 255, 255), 0.5), (rad, rad), rad * 0.7)
            screen.blit(core_surf, (int(wrapped_x - rad), int(wrapped_y - rad)))
        # SUN RAY
        if color == (247, 238, 15): # Sun color specifically
            """# DEBUG
            pygame.draw.line(screen, (255, 0, 255),
                (WINDOW_SIZE[0] // 2, WINDOW_SIZE[1] // 2),
                (int(wrapped_x), int(wrapped_y)), 1)"""
            # Idk, fancy tech ?
            # draw a box around the sun and put some green shapes around it for some cyber eye gui or something (wow)
            # Draw a box around the sun using green paint
            if random.randint(0, 19) == 2:
                wrapped_x += random.randint(-1, 1)
                wrapped_y += random.randint(-1, 1)
            critical_error = False
            if random.randint(0, 188) == 0 or emptimer > 0:
                critical_error = True
                wrapped_x += random.randint(-50, 50)
                wrapped_y += random.randint(-50, 50)
            two_half = 2.5 if not critical_error else random.uniform(-0.37, 14.82)
            five = 5 if not critical_error else random.uniform(-0.37, 14.82)
            eighty = 80 if not critical_error else random.uniform(-0.37, 14.82)
            four = 4 if not critical_error else random.uniform(-0.37, 14.82)
            one = 1 if not critical_error else random.uniform(-0.37, 14.82)
            zero = 0 if not critical_error else random.uniform(-0.37, 14.82)
            zero2 = 0 if not critical_error else random.uniform(-0.37, 14.82)
            zero3 = 0 if not critical_error else random.uniform(-0.37, 14.82)
            zero4 = 0 if not critical_error else random.uniform(-0.37, 14.82)
            zero5 = 0 if not critical_error else random.uniform(-0.37, 14.82)
            zero6 = 0 if not critical_error else random.uniform(-0.37, 14.82)
            zero7 = 0 if not critical_error else random.uniform(-0.37, 14.82)
            green = (0, 255, 0) if not critical_error else (255, 0, 0)
            # Draw some idk arrows from the sides of the box
            diff_sun_camera_x = (WINDOW_SIZE[0] // 2) - wrapped_x
            diff_sun_camera_y = (WINDOW_SIZE[1] // 2) - wrapped_y
            # div by 70, cap to -20px - 20px
            diff_sun_camera_x = max(-eighty, min(80, diff_sun_camera_x // four))
            diff_sun_camera_y = one * max(-80, min(80, diff_sun_camera_y // 4))

            # if critical error, randomly scrabmle the colors
            if not critical_error:
                green1, green2, green3, green4, green5, green8, green9, green10, green11 = [(0, 255, 0)] * 9
                green6_alpha, green7_alpha = (0, 255, 0, 128), (0, 255, 0, 128)
            else:
                if critical_error:
                    # First set base colors
                    green1, green2, green3, green4, green5, green8, green9, green10, green11 = [(255, 0, 0)] * 9
                    green6_alpha, green7_alpha = (255, 0, 0, 128), (255, 0, 0, 128)
                    
                    # Then randomly modify each variable directly
                    all_colors = [green1, green2, green3, green4, green5, green8, green9, green10, green11]
                    for i in range(len(all_colors)):
                        if random.randint(0, 9) < 3: # 30%
                            all_colors[i] = (0, 255, 0)
                        elif random.randint(0, 6) < 4:
                            all_colors[i] = (255, 0, 0) 
                        else:
                            all_colors[i] = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                    
                    # Unpack back to individual variables
                    green1, green2, green3, green4, green5, green8, green9, green10, green11 = all_colors
                    
                    # Handle alpha colors separately
                    bopewfko = [green6_alpha, green7_alpha]
                    for alpha_color in bopewfko:
                        if random.randint(0, 9) < 3: # 30%
                            alpha_color = (0, 255, 0, 128)
                        elif random.randint(0, 6) < 4:
                            alpha_color = (255, 0, 0, 128)
                        else:
                            alpha_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), 128)
                    # put
                    green6_alpha, green7_alpha = bopewfko
            pygame.draw.rect(screen, (0, 255, 0) if not critical_error else (255, 0, 0),
                (int(wrapped_x - rad * 2.5), int(wrapped_y - zero3 - rad * two_half), rad * 5 - zero5, rad * five), 2)
            # turn into arrows: they extend from the left or right side of the box dependign on which way and top and bottom
            if abs(diff_sun_camera_x) > 2:
                if diff_sun_camera_x > 0:
                    # Right side arrow: from the right side of the box, centered, draw a line of length diff_sun_camera_x, and add the head
                    pygame.draw.line(screen, green11,
                        (int(wrapped_x + rad * two_half), int(wrapped_y)),
                        (int(wrapped_x + rad * 2.5 + diff_sun_camera_x), int(wrapped_y)), 2)
                    # Draw arrow head   
                    pygame.draw.polygon(screen, green10,
                        [(int(wrapped_x + rad * 2.5 + diff_sun_camera_x), int(wrapped_y)),  
                        (int(wrapped_x + rad * two_half + diff_sun_camera_x - 5), int(wrapped_y - 5)),
                        (int(wrapped_x + rad * 2.5 + diff_sun_camera_x - 5), int(wrapped_y + 5))])
                else:
                    # Left side arrow: from the left side of the box, centered, draw a line of length diff_sun_camera_x, and add the head
                    pygame.draw.line(screen, green9,
                        (int(wrapped_x - rad * 2.5 * (1 + zero7)), int(wrapped_y + zero6)),
                        (int(wrapped_x - rad * two_half + diff_sun_camera_x), int(wrapped_y - zero3)), 2)
                    # Draw arrow head   
                    pygame.draw.polygon(screen, green8,
                        [(int(wrapped_x - rad * two_half + diff_sun_camera_x), int(wrapped_y)),  
                        (int(wrapped_x - rad * 2.5 + diff_sun_camera_x + five), int(wrapped_y - 5)),
                        (int(wrapped_x - rad * two_half + diff_sun_camera_x + 5), int(wrapped_y + five))])
            if abs(diff_sun_camera_y) > 2:
                if diff_sun_camera_y > 0:
                    # Bottom side arrow: from the bottom side of the box, centered, draw a line of length diff_sun_camera_y, and add the head
                    pygame.draw.line(screen, green4,
                        (int(wrapped_x), int(wrapped_y + rad * two_half)),
                        (int(wrapped_x), int(wrapped_y + rad * two_half + diff_sun_camera_y)), 2)
                    # Draw arrow head
                    pygame.draw.polygon(screen, green3,
                        [(int(wrapped_x), int(wrapped_y + rad * 2.5 + diff_sun_camera_y)),  
                        (int(wrapped_x - 5), int(wrapped_y + rad * 2.5 + diff_sun_camera_y - five)),
                        (int(wrapped_x + 5), int(wrapped_y + rad * 2.5 + diff_sun_camera_y - 5))])
                else:
                    # Top side arrow: from the top side of the box, centered, draw a line of length diff_sun_camera_y, and add the head
                    pygame.draw.line(screen,green2,
                        (int(wrapped_x), int(wrapped_y - rad * 2.5)),
                        (int(wrapped_x), int(wrapped_y - rad * 2.5 + diff_sun_camera_y)), 2)
                    # Draw arrow head   
                    pygame.draw.polygon(screen, green,
                        [(int(wrapped_x), int(wrapped_y - rad * 2.5 + diff_sun_camera_y)),  
                        (int(wrapped_x - 5), int(wrapped_y - rad * two_half + diff_sun_camera_y + five)),
                        (int(wrapped_x + 5), int(wrapped_y - rad * 2.5 + diff_sun_camera_y + five))])
            # Write "The sun : 3ly" in the top left corner
            GREEBLOR = "".join([chr(random.randint(0, 255)) for _ in range(15)])
            # Filter out illegal chars (all control chars except \n and spaces) and replace them with ÿ (for no particular reason)
            GREEBLOR = ''.join(c if c.isprintable() or c in ('\n', ' ') else 'ÿ' for c in GREEBLOR)
            # boop: slightly weird
            boop = "The sun : 3ly"
            # pick a random char and switch it with a different char
            boop_index1 = random.randint(0, len(boop) - 1)
            boop_index2 = random.randint(0, len(boop) - 1)
            while boop_index1 == boop_index2:
                boop_index2 = random.randint(0, len(boop) - 1)
            i1_char = boop[boop_index1]
            boop = boop[:boop_index1] + boop[boop_index2] + boop[boop_index1 + 1:]
            boop = boop[:boop_index2] + i1_char + boop[boop_index2 + 1:]
            normalish = "The sun : 3ly" if not random.randint(0, 11) == 3 else boop
            text = founte.render(normalish if not critical_error else GREEBLOR, True, green5)
            screen.blit(text, (wrapped_x - rad * 3, wrapped_y - rad * 2.5 - 20))
            # Transparant mesh
            box_shaped_surface = pygame.Surface((rad * 5, rad * 5), pygame.SRCALPHA)
            box_shaped_surface.fill((0, 0, 0, 0)) # Transparent background
            for verlines in range(0, rad * 5, 10):
                # insert zero vars in fun places so critical eror causes distortions
                pygame.draw.line(box_shaped_surface, green6_alpha, (verlines + zero, 0), (verlines + zero4, rad * 5), 1)
            for horilines in range(0, rad * 5, 10):
                pygame.draw.line(box_shaped_surface, green7_alpha, (0 + zero3, horilines + zero2), (rad * 5, horilines + zero5), 1)
            screen.blit(box_shaped_surface, (int(wrapped_x - rad * 2.5), int(wrapped_y - rad * 2.5)))

            # Garbage commands simulator
            if critical_error:
                for garbage in range(random.randint(3, 5)):
                    # Draw garbage red objects
                    garbage_x = wrapped_x + random.randint(-rad * 2, rad * 2)
                    garbage_y = wrapped_y + random.randint(-rad * 2, rad * 2)
                    typeoid = random.randint(0, 4)
                    if typeoid == 0:
                        # Draw a red circle
                        pygame.draw.circle(screen, (255, 0, 0), (int(garbage_x), int(garbage_y)), random.randint(5, 15))    
                    elif typeoid == 1:
                        # Draw a rectangle
                        pygame.draw.rect(screen, (255, 0, 0), (int(garbage_x - 10), int(garbage_y - 10), random.randint(20, 40), random.randint(20, 40)))
                    elif typeoid == 2:
                        # Draw a line
                        pygame.draw.line(screen, (255, 0, 0), (int(garbage_x - 10), int(garbage_y - 10)), (int(garbage_x + 10), int(garbage_y + 10)), random.randint(1, 3))
                    elif typeoid == 3:
                        # oh no. total chaos. its gonna draw a polygon made up of 23 random points and its gonna have edges
                        points = [(random.randint(int(garbage_x - -13), int(garbage_x + 50)), 
                                   random.randint(int(garbage_y - -24), int(garbage_y + 50))) for _ in range(23)]    
                        pygame.draw.polygon(screen, (255, 0, 0), points, random.randint(1, 3))
            # End of sun ra
            continue
        if color == (82, 164, 199): # NH-4b color specifically
            """# DEBUG
            pygame.draw.line(screen, (255, 0, 255),
                (WINDOW_SIZE[0] // 2, WINDOW_SIZE[1] // 2),
                (int(wrapped_x), int(wrapped_y)), 1)"""
            # Idk, fancy tech ?
            # draw a box around the sun and put some green shapes around it for some cyber eye gui or something (wow)
            # Draw a box around the sun using green paint
            if random.randint(0, 14) == 2:
                wrapped_x += random.randint(-1, 1)
                wrapped_y += random.randint(-1, 1)
            critical_error = False
            if random.randint(0, 118) == 0 or emptimer > 0:
                critical_error = True
                wrapped_x += random.randint(-50, 50)
                wrapped_y += random.randint(-50, 50)
            two_half = 2.5 if not critical_error else random.uniform(-0.37, 14.82)
            five = 5 if not critical_error else random.uniform(-0.37, 14.82)
            eighty = 80 if not critical_error else random.uniform(-0.37, 14.82)
            four = 4 if not critical_error else random.uniform(-0.37, 14.82)
            one = 1 if not critical_error else random.uniform(-0.37, 14.82)
            zero = 0 if not critical_error else random.uniform(-0.37, 14.82)
            zero2 = 0 if not critical_error else random.uniform(-0.37, 14.82)
            zero3 = 0 if not critical_error else random.uniform(-0.37, 14.82)
            zero4 = 0 if not critical_error else random.uniform(-0.37, 14.82)
            zero5 = 0 if not critical_error else random.uniform(-0.37, 14.82)
            zero6 = 0 if not critical_error else random.uniform(-0.37, 14.82)
            zero7 = 0 if not critical_error else random.uniform(-0.37, 14.82)
            green = (0, 255, 0) if not critical_error else (255, 0, 0)
            # Draw some idk arrows from the sides of the box
            diff_sun_camera_x = (WINDOW_SIZE[0] // 2) - wrapped_x
            diff_sun_camera_y = (WINDOW_SIZE[1] // 2) - wrapped_y
            # div by 70, cap to -20px - 20px
            diff_sun_camera_x = max(-eighty, min(80, diff_sun_camera_x // four))
            diff_sun_camera_y = one * max(-80, min(80, diff_sun_camera_y // 4))

            # if critical error, randomly scrabmle the colors
            if not critical_error:
                green1, green2, green3, green4, green5, green8, green9, green10, green11 = [(0, 255, 0)] * 9
                green6_alpha, green7_alpha = (0, 255, 0, 128), (0, 255, 0, 128)
            else:
                if critical_error:
                    # First set base colors
                    green1, green2, green3, green4, green5, green8, green9, green10, green11 = [(255, 0, 0)] * 9
                    green6_alpha, green7_alpha = (255, 0, 0, 128), (255, 0, 0, 128)
                    
                    # Then randomly modify each variable directly
                    all_colors = [green1, green2, green3, green4, green5, green8, green9, green10, green11]
                    for i in range(len(all_colors)):
                        if random.randint(0, 9) < 3: # 30%
                            all_colors[i] = (0, 255, 0)
                        elif random.randint(0, 6) < 4:
                            all_colors[i] = (255, 0, 0) 
                        else:
                            all_colors[i] = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                    
                    # Unpack back to individual variables
                    green1, green2, green3, green4, green5, green8, green9, green10, green11 = all_colors
                    
                    # Handle alpha colors separately
                    bopewfko = [green6_alpha, green7_alpha]
                    for alpha_color in bopewfko:
                        if random.randint(0, 9) < 3: # 30%
                            alpha_color = (0, 255, 0, 128)
                        elif random.randint(0, 6) < 4:
                            alpha_color = (255, 0, 0, 128)
                        else:
                            alpha_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), 128)
                    # put
                    green6_alpha, green7_alpha = bopewfko
            pygame.draw.rect(screen, (0, 255, 0) if not critical_error else (255, 0, 0),
                (int(wrapped_x - rad * 2.5), int(wrapped_y - zero3 - rad * two_half), rad * 5 - zero5, rad * five), 2)
            # turn into arrows: they extend from the left or right side of the box dependign on which way and top and bottom
            if abs(diff_sun_camera_x) > 2:
                if diff_sun_camera_x > 0:
                    # Right side arrow: from the right side of the box, centered, draw a line of length diff_sun_camera_x, and add the head
                    pygame.draw.line(screen, green11,
                        (int(wrapped_x + rad * two_half), int(wrapped_y)),
                        (int(wrapped_x + rad * 2.5 + diff_sun_camera_x), int(wrapped_y)), 2)
                    # Draw arrow head   
                    pygame.draw.polygon(screen, green10,
                        [(int(wrapped_x + rad * 2.5 + diff_sun_camera_x), int(wrapped_y)),  
                        (int(wrapped_x + rad * two_half + diff_sun_camera_x - 5), int(wrapped_y - 5)),
                        (int(wrapped_x + rad * 2.5 + diff_sun_camera_x - 5), int(wrapped_y + 5))])
                else:
                    # Left side arrow: from the left side of the box, centered, draw a line of length diff_sun_camera_x, and add the head
                    pygame.draw.line(screen, green9,
                        (int(wrapped_x - rad * 2.5 * (1 + zero7)), int(wrapped_y + zero6)),
                        (int(wrapped_x - rad * two_half + diff_sun_camera_x), int(wrapped_y - zero3)), 2)
                    # Draw arrow head   
                    pygame.draw.polygon(screen, green8,
                        [(int(wrapped_x - rad * two_half + diff_sun_camera_x), int(wrapped_y)),  
                        (int(wrapped_x - rad * 2.5 + diff_sun_camera_x + five), int(wrapped_y - 5)),
                        (int(wrapped_x - rad * two_half + diff_sun_camera_x + 5), int(wrapped_y + five))])
            if abs(diff_sun_camera_y) > 2:
                if diff_sun_camera_y > 0:
                    # Bottom side arrow: from the bottom side of the box, centered, draw a line of length diff_sun_camera_y, and add the head
                    pygame.draw.line(screen, green4,
                        (int(wrapped_x), int(wrapped_y + rad * two_half)),
                        (int(wrapped_x), int(wrapped_y + rad * two_half + diff_sun_camera_y)), 2)
                    # Draw arrow head
                    pygame.draw.polygon(screen, green3,
                        [(int(wrapped_x), int(wrapped_y + rad * 2.5 + diff_sun_camera_y)),  
                        (int(wrapped_x - 5), int(wrapped_y + rad * 2.5 + diff_sun_camera_y - five)),
                        (int(wrapped_x + 5), int(wrapped_y + rad * 2.5 + diff_sun_camera_y - 5))])
                else:
                    # Top side arrow: from the top side of the box, centered, draw a line of length diff_sun_camera_y, and add the head
                    pygame.draw.line(screen,green2,
                        (int(wrapped_x), int(wrapped_y - rad * 2.5)),
                        (int(wrapped_x), int(wrapped_y - rad * 2.5 + diff_sun_camera_y)), 2)
                    # Draw arrow head   
                    pygame.draw.polygon(screen, green,
                        [(int(wrapped_x), int(wrapped_y - rad * 2.5 + diff_sun_camera_y)),  
                        (int(wrapped_x - 5), int(wrapped_y - rad * two_half + diff_sun_camera_y + five)),
                        (int(wrapped_x + 5), int(wrapped_y - rad * 2.5 + diff_sun_camera_y + five))])
            # Write "The sun : 3ly" in the top left corner
            GREEBLOR = "".join([chr(random.randint(0, 255)) for _ in range(15)])
            # Filter out illegal chars (all control chars except \n and spaces) and replace them with ÿ (for no particular reason)
            GREEBLOR = ''.join(c if c.isprintable() or c in ('\n', ' ') else 'ÿ' for c in GREEBLOR)
            # boop: slightly weird
            boop = "NH-4b : 4.27ly"
            # pick a random char and switch it with a different char
            boop_index1 = random.randint(0, len(boop) - 1)
            boop_index2 = random.randint(0, len(boop) - 1)
            while boop_index1 == boop_index2:
                boop_index2 = random.randint(0, len(boop) - 1)
            i1_char = boop[boop_index1]
            boop = boop[:boop_index1] + boop[boop_index2] + boop[boop_index1 + 1:]
            boop = boop[:boop_index2] + i1_char + boop[boop_index2 + 1:]
            normalish = "NH-4b : 4.27ly" if not random.randint(0, 9) == 3 else boop
            text = founte.render(normalish if not critical_error else GREEBLOR, True, green5)
            screen.blit(text, (wrapped_x - rad * 3, wrapped_y - rad * 2.5 - 20))
            # Transparant mesh
            box_shaped_surface = pygame.Surface((rad * 5, rad * 5), pygame.SRCALPHA)
            box_shaped_surface.fill((0, 0, 0, 0)) # Transparent background
            for verlines in range(0, rad * 5, 10):
                # insert zero vars in fun places so critical eror causes distortions
                pygame.draw.line(box_shaped_surface, green6_alpha, (verlines + zero, 0), (verlines + zero4, rad * 5), 1)
            for horilines in range(0, rad * 5, 10):
                pygame.draw.line(box_shaped_surface, green7_alpha, (0 + zero3, horilines + zero2), (rad * 5, horilines + zero5), 1)
            screen.blit(box_shaped_surface, (int(wrapped_x - rad * 2.5), int(wrapped_y - rad * 2.5)))

            # Garbage commands simulator
            if critical_error:
                for garbage in range(random.randint(3, 5)):
                    # Draw garbage red objects
                    garbage_x = wrapped_x + random.randint(-rad * 2, rad * 2)
                    garbage_y = wrapped_y + random.randint(-rad * 2, rad * 2)
                    typeoid = random.randint(0, 4)
                    if typeoid == 0:
                        # Draw a red circle
                        pygame.draw.circle(screen, (255, 0, 0), (int(garbage_x), int(garbage_y)), random.randint(5, 15))    
                    elif typeoid == 1:
                        # Draw a rectangle
                        pygame.draw.rect(screen, (255, 0, 0), (int(garbage_x - 10), int(garbage_y - 10), random.randint(20, 40), random.randint(20, 40)))
                    elif typeoid == 2:
                        # Draw a line
                        pygame.draw.line(screen, (255, 0, 0), (int(garbage_x - 10), int(garbage_y - 10)), (int(garbage_x + 10), int(garbage_y + 10)), random.randint(1, 3))
                    elif typeoid == 3:
                        # oh no. total chaos. its gonna draw a polygon made up of 23 random points and its gonna have edges
                        points = [(random.randint(int(garbage_x - -13), int(garbage_x + 50)), 
                                   random.randint(int(garbage_y - -24), int(garbage_y + 50))) for _ in range(23)]    
                        pygame.draw.polygon(screen, (255, 0, 0), points, random.randint(1, 3))
            # End of sun ra
            continue
# Set up the camera

used_area_bounds_pluS_screen_size = (-WINDOW_SIZE[0] // TILE_SIZE - 5,
                                     -WINDOW_SIZE[1] // TILE_SIZE - 5,
                                     WINDOW_SIZE[0] // TILE_SIZE + 5,
                                     WINDOW_SIZE[1] // TILE_SIZE + 5)

test_texture = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
# Draw a uv map on the text texture
for x in range(TILE_SIZE):
    for y in range(TILE_SIZE):
        # Calculate UV coordinates
        u = x / TILE_SIZE
        v = y / TILE_SIZE
        # Set pixel color based on UV coordinates
        test_texture.set_at((x, y), (0, int(u * 255), int(v * 255), 255))

def get_barycentric(px, py, p1, p2, p3):
    """
    Calculate barycentric coordinates for point (px,py) relative to triangle (p1,p2,p3).
    Returns (u,v,w) where u+v+w=1 and u,v,w are the weights for p1,p2,p3 respectively.
    """
    # Convert to vectors
    v0 = (p2[0] - p1[0], p2[1] - p1[1]) # v0 = p2 - p1
    v1 = (p3[0] - p1[0], p3[1] - p1[1]) # v1 = p3 - p1
    v2 = (px - p1[0], py - p1[1])        # v2 = p - p1
    
    # Calculate dot products
    d00 = v0[0] * v0[0] + v0[1] * v0[1] # dot(v0,v0)
    d01 = v0[0] * v1[0] + v0[1] * v1[1] # dot(v0,v1)
    d11 = v1[0] * v1[0] + v1[1] * v1[1] # dot(v1,v1)
    d20 = v2[0] * v0[0] + v2[1] * v0[1] # dot(v2,v0)
    d21 = v2[0] * v1[0] + v2[1] * v1[1] # dot(v2,v1)
    
    # Calculate barycentric coordinates
    denom = d00 * d11 - d01 * d01
    if abs(denom) < 1e-7: # Check for divide-by-zero
        return (-1, -1, -1) # Invalid result
        
    v = (d11 * d20 - d01 * d21) / denom
    w = (d00 * d21 - d01 * d20) / denom
    u = 1.0 - v - w
    
    return (u, v, w)

def testdraw(surf, tex, quad_points):
    """
    Maps a texture onto an arbitrary quad using perspective-correct interpolation.
    Args:
        surf: Target surface to draw on
        tex: Source texture
        quad_points: List of 4 (x,y) points defining the quad corners, in order
    """
    # Round coordinates to prevent seams
    quad_points = [(round(x), round(y)) for x,y in quad_points]

    # Get bounding box
    min_x = min(p[0] for p in quad_points)
    max_x = max(p[0] for p in quad_points)
    min_y = min(p[1] for p in quad_points)
    max_y = max(p[1] for p in quad_points)

    width = max_x - min_x + 1
    height = max_y - min_y + 1
    temp = pygame.Surface((width, height), pygame.SRCALPHA)
    temp.fill((0, 0, 0, 0))

    # Define UV coordinates for each corner properly
    # Order matters: topleft, topright, bottomright, bottomleft
    src_points = [(0,0), (1,0), (1,1), (0,1)]
    
    # Convert to local space
    local_quad = [(x - min_x, y - min_y) for x,y in quad_points]

    # For each pixel in bounding box
    for y in range(height):
        for x in range(width):
            # Calculate barycentric coordinates for both triangles
            bary1 = get_barycentric(x, y, local_quad[0], local_quad[1], local_quad[2])
            bary2 = get_barycentric(x, y, local_quad[0], local_quad[2], local_quad[3])

            # Process pixel if it's in either triangle
            if min(bary1) >= -0.00001: # First triangle
                a,b,c = bary1
                # Correct UV interpolation
                u = a*src_points[0][0] + b*src_points[1][0] + c*src_points[2][0]
                v = a*src_points[0][1] + b*src_points[1][1] + c*src_points[2][1]
                
                # Clamp UV coordinates
                u = max(0, min(1, u))
                v = max(0, min(1, v))
                
                # Sample texture with proper bounds checking
                tex_x = int(u * (tex.get_width() - 1))
                tex_y = int(v * (tex.get_height() - 1))
                color = tex.get_at((tex_x, tex_y))
                temp.set_at((x, y), color)
                    
            elif min(bary2) >= -0.00001: # Second triangle
                a,b,c = bary2
                # Correct UV interpolation for second triangle
                u = a*src_points[0][0] + b*src_points[2][0] + c*src_points[3][0]
                v = a*src_points[0][1] + b*src_points[2][1] + c*src_points[3][1]
                
                # Clamp UV coordinates
                u = max(0, min(1, u))
                v = max(0, min(1, v))
                
                # Sample texture with proper bounds checking
                tex_x = int(u * (tex.get_width() - 1))
                tex_y = int(v * (tex.get_height() - 1))
                color = tex.get_at((tex_x, tex_y))
                temp.set_at((x, y), color)

    # Draw result
    surf.blit(temp, (min_x, min_y))




# Rectangle storage
rects = []

# idea to speed up "does a rect exist here" checks: sets are really really  really fast
# we can palce all the positions of rects in as et and then do hyper fast pos in rectsset checks
rectsset = set()
# Add initial rectangle at origin
#rects.append({'x': 24, 'y':  10})
#rects.append({'x': 24, 'y':  11})
def _add_rect(x, y):
    """Add a rectangle at the given grid position and expand bounds to include it with screen buffer"""
    rects.append({'x': x, 'y': y, 'type': 'block'})
    rectsset.add((x, y))

    # Update bounds - these represent the furthest points where blocks are visible
    # We need to account for:
    # 1. Grid position of block
    # 2. Screen size (so player can see blocks from WINDOW_SIZE distance away)
    # 3. Extra buffer for perspective/visual effects
    global used_area_bounds_pluS_screen_size
    min_x, min_y, max_x, max_y = used_area_bounds_pluS_screen_size

    # Expand bounds if new block is outside current bounds
    # The -/+ WINDOW_SIZE//TILE_SIZE terms ensure we include blocks visible from screen edges
    min_x = min(min_x, x - WINDOW_SIZE[0]//TILE_SIZE - 5) 
    min_y = min(min_y, y - WINDOW_SIZE[1]//TILE_SIZE - 5)
    max_x = max(max_x, x + WINDOW_SIZE[0]//TILE_SIZE + 5)
    max_y = max(max_y, y + WINDOW_SIZE[1]//TILE_SIZE + 5)

    used_area_bounds_pluS_screen_size = (min_x, min_y, max_x, max_y)

rects.append({'x': 0, 'y':  0, 'type': 'anchor'}) # Anch charm
rectsset.add((0, 0)) # Anchor rect for referein setnce
#_add_rect(24, 11)

"""# TEST: 200 rectangles
for tx in range(20):
    for ty in range(10):
        # Calculate position
        x = tx 
        y = ty 
        # Add rectangle
        _add_rect(x, y)"""

neighborscache = {} # Cache for neighbor calculations so they dont lag

def grid_pos_has_block(grid_x, grid_y, rects):
    """Check if there's already a block at the given grid position"""
    #return any(r['x'] == grid_x and r['y'] == grid_y for r in rects) # Old
    return (grid_x, grid_y) in rectsset # New
"""
# test endgame space base: 8000 blocks
while len(rects) < 8000:
    print(f"Progressez: {len(rects)/80}%") if len(rects) % 1000 == 0 else None
    # Randomly generate a position
    grid_x = random.randint(-100, 100)
    grid_y = random.randint(-50, 50)
    
    # Check if this position already has a block
    if not grid_pos_has_block(grid_x, grid_y, rects):
        #rects.append({'x': grid_x, 'y': grid_y})
        _add_rect(grid_x, grid_y)"""


def screen_to_grid(screen_x, screen_y, camera):
    """Convert screen coordinates to grid coordinates"""
    # First convert screen coords to world coords by adding camera position
    world_x = screen_x + camera['x']
    world_y = screen_y + camera['y']
    
    # Then convert to grid coords by dividing by TILE_SIZE and rounding
    grid_x = round(world_x / TILE_SIZE)
    grid_y = round(world_y / TILE_SIZE)
    
    return grid_x, grid_y

def grid_pos_has_block(grid_x, grid_y, rects):
    """Check if there's already a block at the given grid position"""
    #return any(r['x'] == grid_x and r['y'] == grid_y for r in rects)
    return (grid_x, grid_y) in rectsset # Use the set for fast lookup

camera = {'x': 0, 'y': 0} # Camera position in world coordinates

grid_surface = pygame.Surface([WINDOW_SIZE[0] + TILE_SIZE * 2,
                               WINDOW_SIZE[1] + TILE_SIZE * 2], pygame.SRCALPHA)
grid_surface.convert_alpha() # For whatever reason this bost fps
# Draw grid aligned to world coordinates
# Calculate grid bounds that cover the visible area
start_x = (camera['x'] // TILE_SIZE) * TILE_SIZE
end_x = start_x + WINDOW_SIZE[0] + TILE_SIZE + TILE_SIZE+ TILE_SIZE
start_y = (camera['y'] // TILE_SIZE) * TILE_SIZE  
end_y = start_y + WINDOW_SIZE[1] + TILE_SIZE+ TILE_SIZE+ TILE_SIZE

# Draw vertical lines
for x in range(int(start_x), int(end_x), TILE_SIZE):
    screen_x = x - camera['x']
    pygame.draw.line(grid_surface, (0, 255, 0, 16/2),
                    (screen_x , -1),
                    (screen_x , WINDOW_SIZE[1]-1+ TILE_SIZE+ TILE_SIZE), 9)
# Draw horizontal lines
for y in range(int(start_y), int(end_y), TILE_SIZE):
    screen_y = y - camera['y']
    pygame.draw.line(grid_surface, (0, 255, 0, 16/2),
                    (0, screen_y),
                    (WINDOW_SIZE[0] + TILE_SIZE+ TILE_SIZE, screen_y), 9)

# Draw vertical lines
for x in range(int(start_x), int(end_x), TILE_SIZE):
    screen_x = x - camera['x']
    pygame.draw.line(grid_surface, (0, 255, 0, 64/2),
                    (screen_x , -1),
                    (screen_x , WINDOW_SIZE[1]-1+ TILE_SIZE+ TILE_SIZE), 5)
# Draw horizontal lines
for y in range(int(start_y), int(end_y), TILE_SIZE):
    screen_y = y - camera['y']
    pygame.draw.line(grid_surface, (0, 255, 0, 64/2),
                    (0, screen_y),
                    (WINDOW_SIZE[0]+ TILE_SIZE+ TILE_SIZE, screen_y), 5)
# smooller bloom (same but darker and larger radius)
for x in range(int(start_x), int(end_x), TILE_SIZE):
    for y in range(int(start_y), int(end_y), TILE_SIZE):
        screen_x = x - camera['x'] + 1
        screen_y = y - camera['y'] + 1
        pygame.draw.circle(grid_surface, (0, 255, 0, 64/2), (screen_x, screen_y), 5)
        pygame.draw.circle(grid_surface, (0, 255, 0, 64/2), (screen_x-1, screen_y), 5)
        pygame.draw.circle(grid_surface, (0, 255, 0, 64/2), (screen_x, screen_y-1), 5)
        pygame.draw.circle(grid_surface, (0, 255, 0, 64/2), (screen_x-1, screen_y-1), 5)

# Draw vertical lines
for x in range(int(start_x), int(end_x), TILE_SIZE):
    screen_x = x - camera['x']
    pygame.draw.line(grid_surface, (0, 255, 0, 128/2),
                    (screen_x, -1),
                    (screen_x , WINDOW_SIZE[1]-1+ TILE_SIZE+ TILE_SIZE), 3)
# Draw horizontal lines
for y in range(int(start_y), int(end_y), TILE_SIZE):
    screen_y = y - camera['y']
    pygame.draw.line(grid_surface, (0, 255, 0, 128/2),
                    (0, screen_y),
                    (WINDOW_SIZE[0]+ TILE_SIZE+ TILE_SIZE, screen_y), 3)
    
# smooller bloom (same but darker and larger radiu
for x in range(int(start_x), int(end_x), TILE_SIZE):
    for y in range(int(start_y), int(end_y), TILE_SIZE):
        screen_x = x - camera['x'] + 1
        screen_y = y - camera['y'] + 1
        pygame.draw.circle(grid_surface, (0, 255, 0, 128/2), (screen_x, screen_y), 3)
        pygame.draw.circle(grid_surface, (0, 255, 0, 128/2), (screen_x-1, screen_y), 3)
        pygame.draw.circle(grid_surface, (0, 255, 0, 128/2), (screen_x, screen_y-1), 3)
        pygame.draw.circle(grid_surface, (0, 255, 0, 128/2), (screen_x-1, screen_y-1), 3)

for x in range(int(start_x), int(end_x), TILE_SIZE):
    screen_x = x - camera['x']
    pygame.draw.line(grid_surface, (0, 255, 0, 255/2), 
                    (screen_x, 0),
                    (screen_x, WINDOW_SIZE[1]+ TILE_SIZE+ TILE_SIZE), 1)
    #print("Screen x:", screen_x)
warning_thing = 0, ""
for y in range(int(start_y), int(end_y), TILE_SIZE):
    screen_y = y - camera['y']
    pygame.draw.line(grid_surface, (0, 255, 0, 255/2),
                    (0, screen_y),
                    (WINDOW_SIZE[0]+ TILE_SIZE+ TILE_SIZE, screen_y), 1)
# bloom at the intersections so it looks like its glowing
# because theres two beams itnersecting = more liguht
for x in range(int(start_x), int(end_x), TILE_SIZE):
    for y in range(int(start_y), int(end_y), TILE_SIZE):
        screen_x = x - camera['x'] + 1
        screen_y = y - camera['y'] + 1
        pygame.draw.circle(grid_surface, (0, 255, 0, 255/2), (screen_x, screen_y), 2)
        pygame.draw.circle(grid_surface, (0, 255, 0, 255/2), (screen_x-1, screen_y), 2)
        pygame.draw.circle(grid_surface, (0, 255, 0, 255/2), (screen_x, screen_y-1), 2)
        pygame.draw.circle(grid_surface, (0, 255, 0, 255/2), (screen_x-1, screen_y-1), 2)
# Blit the grid surface to the screen
def flood_fill(x, y):
    """Flood fill algorithm to remove all blocks not connected to the anchor"""
    if (x, y) in flooded or not grid_pos_has_block(x, y, rects):
        return
    flooded.add((x, y))
    # Check neighbors
    flood_fill(x + 1, y)
    flood_fill(x - 1, y)
    flood_fill(x, y + 1)
    flood_fill(x, y - 1)
    #print("Screen y:", screen_y)
emptimer = 0
running = True
times = [10] # placeholder
feetdash = 0
while running:
    feetdash += 1
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    emptimer -= 1
    if random.randint(1, 487) == 24:
        emptimer = 73
    # ...existing code...
    mouse_buttons = pygame.mouse.get_pressed()
    mouse_pos = list(pygame.mouse.get_pos())
    # Adjust mouse coordinates for screen scaling
    mouse_pos[0] = mouse_pos[0] / scale
    mouse_pos[1] = mouse_pos[1] / scale
    mouse_pos[0] -= TILE_SIZE / 2 # Center the mouse on the tile 
    mouse_pos[1] -= TILE_SIZE / 2 # Center the mouse on the tile
    # Convert mouse position to grid coordinates
    grid_x, grid_y = screen_to_grid(mouse_pos[0], mouse_pos[1], camera)
# ...existing code...
    
    # Fix the cache invalidation in both click handlers by converting grid coords to pixel coords:

# Left click handler:
    # Fix the cache key mismatch:

    # In the left click handler:
    if mouse_buttons[0]:  # Left mouse button Click4Bait
        if not grid_pos_has_block(grid_x, grid_y, rects):
            # only if adjacnt to an existing block: remmeber we dont need to check if its connected to anchor becuse any other block it could be next to is already connected
            if grid_pos_has_block(grid_x + 1, grid_y, rects) or \
               grid_pos_has_block(grid_x - 1, grid_y, rects) or \
               grid_pos_has_block(grid_x, grid_y + 1, rects) or \
               grid_pos_has_block(grid_x, grid_y - 1, rects):
                _add_rect(grid_x, grid_y)
                # Invalidate cache using GRID coordinates
                # cahce invalidation is spaghetti code
                neighborscache.clear()


    # And in the right click handler:
    if mouse_buttons[2]:  # Right mouse button
        if grid_x == 0 and grid_y == 0:
            # Cannot remove anchor
            pass
        else:
            if (grid_x, grid_y) in rectsset:
                if keys[pygame.K_LALT]:
                    rectsset.remove((grid_x, grid_y))
                    rects[:] = [r for r in rects if not (r['x'] == grid_x and r['y'] == grid_y)]
                    # Invalidate cache using GRID coordinates
                    # well the gen is so fast wthat we can just invalidate the entire cache anyway its too buggy
                    # Oops! all blocks not connected to the anchor by orhognally neiighbors died
                    # flood fill
                    flooded = set()
                    
                    # Start flood fill from the anchor position (0, 0)
                    flood_fill(0, 0)
                    # delete non floody
                    rects[:] = [r for r in rects if (r['x'], r['y']) in flooded or (r['x'] == 0 and r['y'] == 0)]
                    # sets and neighbor dat ais now garbage
                    rectsset.clear()  # Clear the set
                    for r in rects:
                        rectsset.add((r['x'], r['y']))
                    neighborscache.clear()  # Clear the entire cache since we removed a block
                else:
                    # only remove if it doesnt disconnect something else, by flood filling a copy wher eit doesnt exist and if something is left over, cancel
                    temp_rects = rects[:]
                    temp_rectsset = rectsset.copy()
                    # Remove the block from the temporary list
                    temp_rectsset.remove((grid_x, grid_y))
                    flooded = set()
                    oldoid_rectsset = rectsset.copy()  # Save the original set for comparison
                    rectsset = temp_rectsset  # Temporarily use the modified set
                    flood_fill(0, 0)
                    # Restore the original set
                    rectsset = oldoid_rectsset  # Restore the original set
                    # Print the flooded set for debugging
                    #print("Flooded set:", flooded)
                    # THign
                    flooded.add((grid_x, grid_y))  # Add the block being removed to the flooded set so that the comparison isnt BOKEN
                    # check if theres anythin thtas not flooded
                    if flooded == rectsset: # check if the sets are equal
                        # If not, we can remove the block
                        rectsset.remove((grid_x, grid_y))
                        rects[:] = [r for r in rects if not (r['x'] == grid_x and r['y'] == grid_y)]
                        # Invalidate cache using GRID coordinates
                        neighborscache.clear()
                    else:
                        # WARNING
                        warning_thing = 20, f"Didn't remove block because it would disconnect something. Hold ALT to remove it and anything connected anyway."

    # Draw the grid surface

    # Handle input
    
    MOVEMENT_SPEED = MOVEMENT_SPEED_NORM
    if pygame.key.get_mods() & pygame.KMOD_CTRL:
        # SPEED
        MOVEMENT_SPEED *= MOVEMENT_SPEED_SLOW
    if pygame.key.get_mods() & pygame.KMOD_SHIFT:
        # Shift: SPEED
        MOVEMENT_SPEED *= MOVEMENT_SPEED_FAST
    if pygame.key.get_mods() & pygame.KMOD_ALT:
        # DEBUG SPEED
        MOVEMENT_SPEED *= MOVEMENT_SPEED_DBUG
    # Holding F12 to go super speed
    if keys[pygame.K_F12]:
        MOVEMENT_SPEED *= 999

    if keys[pygame.K_F4]:
        # BRR!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        emp_timer = 999
    
    if keys[pygame.K_F9]: 
        # places random blocks on the screen
        rects.clear()
        for zx in range(-30, 31):
            for zy in range(-20, 21):
                if random.randint(0, 1) == 0:
                    rects.append({'x': zx, 'y': zy, 'type': 'block'})
        # FIX the anchor
        if any(r['x'] == 0 and r['y'] == 0 for r in rects):
            rects.remove({'x': 0, 'y': 0, 'type': 'block'})
        rects.append({'x': 0, 'y': 0, 'type': 'anchor'})
        # fix set
        rectsset.clear()  # Clear the set
        for r in rects:
            rectsset.add((r['x'], r['y']))
        # cache invalidation
        neighborscache.clear()

    if keys[pygame.K_w]:
        fcamera['ty'] -= MOVEMENT_SPEED
    if keys[pygame.K_s]:
        fcamera['ty'] += MOVEMENT_SPEED
    if keys[pygame.K_a]:
        fcamera['tx'] -= MOVEMENT_SPEED
    if keys[pygame.K_d]:
        fcamera['tx'] += MOVEMENT_SPEED

    # Camera return to origin
    if keys[pygame.K_SPACE] or feetdash == 1:
        # Go to origin
        fcamera["tx"] = -WINDOW_SIZE[0] // 2 + TILE_SIZE // 2
        fcamera["ty"] = -WINDOW_SIZE[1] // 2 + TILE_SIZE // 2

    # Apply camera physics
    fcamera["x"] = fcamera["x"] * CAMERA_FRICTION + fcamera["tx"] * (1 - CAMERA_FRICTION)
    fcamera["y"] = fcamera["y"] * CAMERA_FRICTION + fcamera["ty"] * (1 - CAMERA_FRICTION)

    camera = {
        # No need for velocity for drawing
        'x': round(fcamera['x']),
        'y': round(fcamera['y'])
    }

    # Clear screen
    t_pose = (0 - camera['x'], 0 - camera['y'])
    # Warp
    t_pose = (t_pose[0] % (REPEAT_HIDER * WINDOW_SIZE[0]), t_pose[1] % (REPEAT_HIDER * WINDOW_SIZE[1]))
    # Draw the background and loop it on the left, top, and left-top
    screen.blit(bg, t_pose)
    screen.blit(bg, (t_pose[0] - bg_width, t_pose[1])) # Left
    screen.blit(bg, (t_pose[0], t_pose[1] - bg_height)) # Top
    screen.blit(bg, (t_pose[0] - bg_width, t_pose[1] - bg_height)) # Top-Left

    
    def calculate_face_points(rect_points, type):
        """Get points for a specific face type"""
        outer, inner = rect_points['outer'], rect_points['inner']
        faces = {
            "top": [outer[0], outer[1], inner[1], inner[0]],
            "bottom": [outer[2], outer[3], inner[3], inner[2]],
            "left": [outer[0], outer[2], inner[2], inner[0]],
            "right": [outer[1], outer[3], inner[3], inner[1]]
        }
        return faces.get(type, [])

    def get_rect_points(rect, camera, factor=0.1):
        """Calculate base and perspective points for a rectangle"""
        # Round the input coordinates first
        rect_x = round(rect['x'])
        rect_y = round(rect['y'])
        cam_x = round(camera['x'])
        cam_y = round(camera['y'])
        
        base_points = [
            (round(rect_x - cam_x), round(rect_y - cam_y)), # topleft
            (round(rect_x - cam_x + TILE_SIZE - 1), round(rect_y - cam_y)), # topright
            (round(rect_x - cam_x), round(rect_y - cam_y + TILE_SIZE - 1)), # bottomleft
            (round(rect_x - cam_x + TILE_SIZE - 1), round(rect_y - cam_y + TILE_SIZE - 1)) # bottomright
        ]
        
        middle = (WINDOW_SIZE[0] // 2, WINDOW_SIZE[1] // 2)
        # Round the inner points too!
        inner_points = [(
            round(p[0] + (middle[0] - p[0]) * factor),
            round(p[1] + (middle[1] - p[1]) * factor)
        ) for p in base_points]
        
        return {
            'outer': base_points,
            'inner': inner_points,
            'screen_pos': (round(rect_x - cam_x + TILE_SIZE // 2), 
                        round(rect_y - cam_y + TILE_SIZE // 2))
        }

    def draw_cube_face(screen, points, face_type, colors):
        """Draw a single face of the cube"""
        if face_type == "front":
            x, y = points['screen_pos']
            pygame.draw.rect(screen, colors[face_type],
                            (x - TILE_SIZE//2, y - TILE_SIZE//2, TILE_SIZE, TILE_SIZE))
            pygame.draw.rect(screen, nonrueguwh997h3qHARHHohfow,
                            (x - TILE_SIZE//2 , y - TILE_SIZE//2, TILE_SIZE, TILE_SIZE),4) # Simple shrink
        else:
            face_points = calculate_face_points(points, face_type)
            if face_points:
                pygame.draw.polygon(screen, colors[face_type], face_points)
                #pygame.draw.polygon(screen, (0, 0, 0), face_points,2) # Draw outline to hide the horrible seams
                # OH no... the shrink isnt gonna be that easy here...
                # HOW DO WE SHRINK. THE POLY
                # we need to pull each point towards the center of the face by 1 px
                # so calculate the vector to the center and normalize it then apply them
                center = (
                    (face_points[0][0] + face_points[1][0] + face_points[2][0] + face_points[3][0]) // 4,
                    (face_points[0][1] + face_points[1][1] + face_points[2][1] + face_points[3][1]) // 4
                )
                for i in range(len(face_points)):
                    vec = (face_points[i][0] - center[0], face_points[i][1] - center[1])
                    length = (vec[0]**2 + vec[1]**2)**0.5
                    if length > 0:
                        vec = (vec[0] / length, vec[1] / length)
                    face_points[i] = (face_points[i][0] - vec[0], face_points[i][1] - vec[1])

                # draw outline
                pygame.draw.polygon(screen, nonrueguwh997h3qHARHHohfow, face_points,5) # Draw outline to hide the horrible seams


    # Pause tool
    if keys[pygame.K_F10]:
        # COMPLETELY pause
        while keys[pygame.K_F10]:
            for event in pygame.event.get(pygame.QUIT):
                running = False
            keys = pygame.key.get_pressed()
    if keys[pygame.K_F11]:
        # reload cache
        neighborscache.clear()
            


    parallax_stars(screen, camera)    # Draw all platforms as 3D cubes with perspective
    #d# Replace the existing face drawing code in the main loop with:
    # Sroot rects by distance to center of screen
    # OPTIMIZATION: dont sqrt, as comparison doesnt care about whther its squared or actual distance
    # /!\rects now uses grids, not pixels

    # POSITION ONE


    # Cache camera position and calculate camera center once
    camera_center_x = camera['x'] + WINDOW_SIZE[0]//2 - TILE_SIZE // 2
    camera_center_y = camera['y'] + WINDOW_SIZE[1]//2 - TILE_SIZE // 2
    camera_pos = (camera['x'], camera['y'])

    # Only resort if camera moved
    if camera_pos != getattr(get_rect_points, 'last_camera_pos', None):
        visible_blocks = []
        for rect in rects:
            px = rect['x'] * TILE_SIZE
            py = rect['y'] * TILE_SIZE
            if (px < camera['x'] - 6 * TILE_SIZE or 
                px > camera['x'] + WINDOW_SIZE[0] + 6 * TILE_SIZE or
                py < camera['y'] - 6 * TILE_SIZE or 
                py > camera['y'] + WINDOW_SIZE[1] + 6 * TILE_SIZE):
                continue
            visible_blocks.append({'x': px, 'y': py, 'type': rect['type']})
        
        # Sort only visible blocks
        rects_srooted = sorted(visible_blocks, 
            key=lambda r: ((r['x'] - camera_center_x)**2 + (r['y'] - camera_center_y)**2),
            reverse=True)
        get_rect_points.last_camera_pos = camera_pos
        get_rect_points.last_sorted = rects_srooted
    else:
        rects_srooted = get_rect_points.last_sorted

    lenghte = len(rects_srooted)
    curent = 0

    for rect in rects_srooted:
        # Rest of the cube rendering logic stays the same
        if (rect['x'] < camera['x'] - 6 * TILE_SIZE or rect['x'] > camera['x'] + WINDOW_SIZE[0] + 6 * TILE_SIZE or
            rect['y'] < camera['y'] - 6 * TILE_SIZE or rect['y'] > camera['y'] + WINDOW_SIZE[1] + 6 * TILE_SIZE):
            continue
        if not (rect['x'], rect['y']) in neighborscache:
            neighbors = {}
            neighbors["left"] = False
            neighbors["right"] = False
            neighbors["top"] = False
            neighbors["bottom"] = False

            # Convert pixel coordinates to grid coordinates for set lookups
            grid_x = rect['x'] // TILE_SIZE  # This is using PIXEL coordinates 
            grid_y = rect['y'] // TILE_SIZE  # while cache uses GRID coordinates

            # Check neighbors using grid coordinates
            if (grid_x - 1, grid_y) in rectsset:
                neighbors["left"] = True
            if (grid_x + 1, grid_y) in rectsset:
                neighbors["right"] = True
            if (grid_x, grid_y - 1) in rectsset:
                neighbors["top"] = True
            if (grid_x, grid_y + 1) in rectsset:
                neighbors["bottom"] = True

            # Save neighbors to cache using PIXEL coordinates
            neighborscache[(rect['x'], rect['y'])] = neighbors  # Mismatch here!

            # one for loop to test
            """for other in rects_srooted: # o(8000) = O(n)
                if other == rect:
                    continue
                if other['x'] == rect['x'] and other['y'] == rect['y'] + TILE_SIZE:
                    # This is above us, because moving them down by tile size equals this tile
                    neighbors["bottom"] = True
                elif other['x'] == rect['x'] and other['y'] == rect['y'] - TILE_SIZE:
                    neighbors["top"] = True
                elif other['x'] == rect['x'] + TILE_SIZE and other['y'] == rect['y']:
                    neighbors["right"] = True   
                elif other['x'] == rect['x'] - TILE_SIZE and other['y'] == rect['y']:
                    neighbors["left"] = True"""
            """# OMG THE SPEEDD!!!!!!!!!!!!!!
            # o(4) = O(1)
            # Convert pixel coordinates to grid coordinates for set lookups
            grid_x = rect['x'] // TILE_SIZE
            grid_y = rect['y'] // TILE_SIZE

            # Check neighbors using grid coordinates
            if (grid_x - 1, grid_y) in rectsset:
                neighbors["left"] = True
            if (grid_x + 1, grid_y) in rectsset:
                neighbors["right"] = True
            if (grid_x, grid_y - 1) in rectsset:
                neighbors["top"] = True
            if (grid_x, grid_y + 1) in rectsset:
                neighbors["bottom"] = True

            # Save neighbors to cache
            neighborscache[(rect['x'], rect['y'])] = neighbors"""
            #print("did some complciated math")
        else:
            # Use cached neighbors
            neighbors = neighborscache[(rect['x'], rect['y'])]
            #print("did some quickmäth")

        if keys[pygame.K_F7]:
            # print info about every tile's rounded divided by tile size pos and neighbor output
            print(f"Tile at ({round(rect['x'] / TILE_SIZE)}, {round(rect['y'] / TILE_SIZE)}) has neighbors: {neighbors}")
        if keys[pygame.K_F8]:
            # Print a bunch of spaices to make a spaice
            print("STUFF")


        # ROUND. ALL. POINTS of. the rect. including the inner and outer points nad everything esle. eveyrthing integers
        rect['x'] = round(rect['x'])
        rect['y'] = round(rect['y'])
        

        # if thee rect is on the left of the middle of the screen move the rect right 1 px
        
        curent += 1
        # Get rectangle points
        rect_points = get_rect_points(rect, camera, factor=0.1)
        
        # Define colors for each face
        """colors = {
            "front": (255, 255, 255), # White front face
            "top": (200, 200, 200),     # Light gray top face
            "bottom": (150, 250, 150), # Dark gray bottom face
            "left": (100, 100, 100),    # Darker gray left face
            "right": (50, 50, 50)       # Darkest gray right face
        }"""
        # Switc hto a less harsh color scheme, where the main color is (150, 150, 150) and the other colors are variations of it
        colors = {
            "block": {
                "front": (150, 150, 150), # Main color for front face
                "top": (180, 180, 180),     # Lighter gray for top face
                "bottom": (120, 120, 120), # Darker gray for bottom face
                "left": (100, 100, 100),    # Darker gray for left face
                "right": (80, 80, 80)       # Darkest gray for right face
            },
            "anchor": {
                "front": (255, 0, 0), # Red front face for anchor
                "top": (200, 0, 0),     # Darker red top face for anchor
                "bottom": (150, 0, 0), # Even darker red bottom face for anchor
                "left": (100, 0, 0),    # Darker red left face for anchor
                "right": (50, 0, 0)       # Darkest red right face for anchor
            }
        }
        if not "type" in rect:
            print("FATAL RECT EDETCTE:E: : FIRE OIN the " + str(rect))
            raise SystemError
        colors = colors[rect['type']]  # Use the type of the rect to get the correct color scheme


        # DEBUG: make all face colors a singl grey color, depending on the progress throug hthe array: last element is white, first is black
        graye = int(255 * (curent / lenghte))
        if keys[pygame.K_F1]: colors = {k: (graye, graye, graye) for k in colors.keys()}

        # Now that we know that the fect we are drawing is the furthest away ,we can just draw the sides in any order, because they will be overwrriten correctly
        # also, drwa the one facing the cmaera last so the side faces dont clip it
        # draw_cube_face(screen, rect_points, "left", colors)
        # draw_cube_face(screen, rect_points, "right", colors)
        # draw_cube_face(screen, rect_points, "top", colors)
        # draw_cube_face(screen, rect_points, "bottom", colors)
        # draw_cube_face(screen, rect_points, "front", colors)
        # ALso. only draw the face we can see them

        # Calcualte the position relative to the MIDDLE OF THE SCREEN
        pos_rel_camera_xenter = rect_points['screen_pos'][0] - ( WINDOW_SIZE[0] // 2) #+ 2*TILE_SIZE
        pos_rel_camera_yenter = rect_points['screen_pos'][1] - ( WINDOW_SIZE[1] // 2) #+ 2*TILE_SIZE

        BG = {"right": (0, 255, 0), "left": (0, 255, 0), "top": (0, 255, 0), "bottom": (0, 255, 0), "front": (0, 255, 0)}
        DG = {"right": (0, 128, 0), "left": (0, 128, 0), "top": (0, 128, 0), "bottom": (0, 128, 0), "front": (0, 128, 0)}

        # If the rel pos is above the camera pos, we can see the bottom face because its pointing at us
        # If the rel pos is to the left of the camera pos, we can see the right face because its pointing at us
        def _h():
            if not keys[pygame.K_F2]:
                if pos_rel_camera_xenter < 0 and not neighbors["right"]: # no point in drawing the left face if a neighbor will block it anyway
                    draw_cube_face(screen, rect_points, "right", colors)
                    """# same thing i guess?
                    rect_points_but_down_by_1_px = __import__("copy").deepcopy(rect_points)
                    rect_points_but_down_by_1_px['outer'][1] = (rect_points_but_down_by_1_px['outer'][1][0], rect_points_but_down_by_1_px['outer'][1][1] + 2) # Top left, top surface
                    rect_points_but_down_by_1_px['outer'][3] = (rect_points_but_down_by_1_px['outer'][3][0], rect_points_but_down_by_1_px['outer'][3][1] + 2) # Bottom left, top surface
                    rect_points_but_down_by_1_px['inner'][1] = (rect_points_but_down_by_1_px['inner'][1][0], rect_points_but_down_by_1_px['inner'][1][1] + 2) # Top left, bottom surface
                    rect_points_but_down_by_1_px['inner'][3] = (rect_points_but_down_by_1_px['inner'][3][0], rect_points_but_down_by_1_px['inner'][3][1] + 2) # Bottom left, bottom surface
                    draw_cube_face(screen, rect_points_but_down_by_1_px, "right", colors)
                    #print(rect_points, rect_points_but_down_by_1_px)"""

                # If the rel pos is to the right of the camera pos, we can see the left face because its pointing at us
                if pos_rel_camera_xenter > 0 and not neighbors["left"]: # no point in drawing the right face if a neighbor will block it anyway
                    draw_cube_face(screen, rect_points, "left", colors)

                    """# add extra security to DEBUG
                    rect_points_but_down_by_1_px = __import__("copy").deepcopy(rect_points)
                    # move the rect points down by 1 px so the left face is drawn correctly
                    rect_points_but_down_by_1_px['outer'][0] = (rect_points_but_down_by_1_px['outer'][0][0], rect_points_but_down_by_1_px['outer'][0][1] + 1) # Top left, top surface
                    rect_points_but_down_by_1_px['outer'][2] = (rect_points_but_down_by_1_px['outer'][2][0] - 1, rect_points_but_down_by_1_px['outer'][2][1] + 1) # Bottom left, top surface
                    rect_points_but_down_by_1_px['inner'][0] = (rect_points_but_down_by_1_px['inner'][0][0], rect_points_but_down_by_1_px['inner'][0][1] + 1) # Top left, bottom surface
                    rect_points_but_down_by_1_px['inner'][2] = (rect_points_but_down_by_1_px['inner'][2][0], rect_points_but_down_by_1_px['inner'][2][1] + 1) # Bottom left, bottom surface

                    draw_cube_face(screen, rect_points_but_down_by_1_px, "left", colors)"""
            else:
                # Draw them as dark or light green depending on whether or not they would be drawn
                if pos_rel_camera_xenter < 0:
                    draw_cube_face(screen, rect_points, "right", BG)
                else:
                    draw_cube_face(screen, rect_points, "right", DG)
                if pos_rel_camera_xenter > 0:
                    draw_cube_face(screen, rect_points, "left", BG)
                else:
                    draw_cube_face(screen, rect_points, "left", DG)
        def _v():
            if not keys[pygame.K_F2]:
                if pos_rel_camera_yenter < 0 and not neighbors["bottom"]: # no point in drawing the top face if a neighbor will block it anyway
                    draw_cube_face(screen, rect_points, "bottom", colors)
                # If the rel pos is below the camera pos, we can see the top face because its pointing at us
                if pos_rel_camera_yenter > 0 and not neighbors["top"]: # no point in drawing the bottom face if a neighbor will block it anyway
                    draw_cube_face(screen, rect_points, "top", colors)
            else:
                # Draw them as dark or light green depending on whether or not they would be drawn
                if pos_rel_camera_yenter < 0:
                    draw_cube_face(screen, rect_points, "bottom", BG)
                else:
                    draw_cube_face(screen, rect_points, "bottom", DG)
                if pos_rel_camera_yenter > 0:
                    draw_cube_face(screen, rect_points, "top", DG)
                else:
                    draw_cube_face(screen, rect_points, "top", BG)

        # If the block is more left / right than up / down, run v THEN h
        # else run h THEN v
        if not keys[pygame.K_F6]:
            if abs(pos_rel_camera_xenter) > abs(pos_rel_camera_yenter):
                _v()
                _h()
            else:
                _h()
                _v()
        # front face
        if not keys[pygame.K_F5]:
            draw_cube_face(screen, rect_points, "front", colors)

        # hack to fix seam:
        """# if this tile is within a tile_size of the center of the screen on the x-axis, draw a cube face thats wider than be
        tile_on_right = neighbors["right"]
        if abs(pos_rel_camera_xenter) < TILE_SIZE // 2 and tile_on_right:
            pygame.draw.rect(screen, colors['front'],
                            (rect_points['screen_pos'][0] - TILE_SIZE // 2,
                            rect_points['screen_pos'][1] - TILE_SIZE // 2,
                            TILE_SIZE * 2, TILE_SIZE))
        # Vertical seam too
        tile_below = neighbors["bottom"]
        if abs(pos_rel_camera_yenter) < TILE_SIZE // 2 and tile_below:
            pygame.draw.rect(screen, colors['front'],
                            (rect_points['screen_pos'][0] - TILE_SIZE // 2,
                            rect_points['screen_pos'][1] - TILE_SIZE // 2,
                            TILE_SIZE, TILE_SIZE * 2))"""
            
        # fill in stupid dot
        if keys[pygame.K_F3]:
            pygame.draw.rect(screen, colors['front'],
                            (rect_points['screen_pos'][0] + TILE_SIZE // 2 - 1,
                            rect_points['screen_pos'][1] + TILE_SIZE // 2 - 1,
                            4, 4))

        """pygame.draw.rect(screen, colors['front'],
                        (rect_points['screen_pos'][0] - TILE_SIZE // 2,
                        rect_points['screen_pos'][1] - TILE_SIZE // 2,
                        1, 1))
        
        # other one too
        pygame.draw.rect(screen, colors['front'],
                        (rect_points['screen_pos'][0] + TILE_SIZE // 2 - 1,
                        rect_points['screen_pos'][1] + TILE_SIZE // 2 + 1,
                        1, 1))"""
        # Fronk space should be squarey?
        # if the topleft and topright of the frott face dont have the same y, print
        if rect_points['outer'][0][1] != rect_points['outer'][1][1]:
            print("a front space is not square shaped:")
            __import__("pprint").pprint(rect_points['outer'])
        # also, the bottom left and bottom right should have the same y
        if rect_points['outer'][2][1] != rect_points['outer'][3][1]:
            print("a front space is not square shaped:")
            __import__("pprint").pprint(rect_points['outer'])
        # and top left and bottom left should have the same x
        if rect_points['outer'][0][0] != rect_points['outer'][2][0]:
            print("a front space is not square shaped:")
            __import__("pprint").pprint(rect_points['outer'])
        # aand the thing
        if rect_points['outer'][1][0] != rect_points['outer'][3][0]:
            print("a front space is not square shaped:")
            __import__("pprint").pprint(rect_points['outer'])

        # Draw the rel_pos
        #pygame.draw.circle(screen, (255, 0, 0), (WINDOW_SIZE[0] // 2 + pos_rel_camera_xenter,
        #                                            WINDOW_SIZE[1] // 2 + pos_rel_camera_yenter), 3)
        # and the thresholds
        # horizontal line for whether the rel  y is above or below 0
        #pygame.draw.line(screen, (255, 0, 0), 
        #                (0, WINDOW_SIZE[1] // 2),
        #                (WINDOW_SIZE[0], WINDOW_SIZE[1] // 2), 1)
        # vertical line for whether the rel x is left or right of 0
        #pygame.draw.line(screen, (255, 0, 0), 
        #                (WINDOW_SIZE[0] // 2, 0),
        #                (WINDOW_SIZE[0] // 2, WINDOW_SIZE[1]), 1)

    # POSITION TWO

    # EXTREMELY slowly move stars
    newstars = []
    for star in stars:
        if len(star) == 6:
            # its a black hole. they dont move
            newstars.append(star)
        else:
            color, x, y, distance, size = star
            # Move the star randomly
            x += random.uniform(-.001, .001) * distance # Scale movement by distance
            y += random.uniform(-.001, .001) * distance
            # Wrap correctly this time
            wrapped_x = x % (REPEAT_HIDER * WINDOW_SIZE[0] * distance) # MULTIPLYNG BY DISTANCE IS VERY IMPORTANT
            wrapped_y = y % (REPEAT_HIDER * WINDOW_SIZE[1] * distance)
            newstars.append((color, wrapped_x, wrapped_y, distance, size))
    stars = newstars

    # Hold Z to zoom
    if keys[pygame.K_z]:
        # get a rectangle of the screen around the mouse, make sur enot to grab outside it, then replace the screen with it
        # lets say, a WINDOW_SIZE[0] // 2 by WINDOW_SIZE[1] // 2 rectangle
        GROW_FACTOR = 4 # not 2
        # if its outside, just push it in
        mouse_x, mouse_y = pygame.mouse.get_pos()
        # clamp
        LEFT_BUFFER = WINDOW_SIZE[0] // (GROW_FACTOR * 2)
        TOP_BUFFER = WINDOW_SIZE[1] // (GROW_FACTOR * 2)
        mouse_x = max(LEFT_BUFFER, min(WINDOW_SIZE[0] - LEFT_BUFFER, mouse_x))
        mouse_y = max(TOP_BUFFER, min(WINDOW_SIZE[1] - TOP_BUFFER, mouse_y))
        zoom_rect = pygame.Rect(
            max(0, mouse_x - WINDOW_SIZE[0] // (GROW_FACTOR * 2)),
            max(0, mouse_y - WINDOW_SIZE[1] // (GROW_FACTOR * 2)),
            min(WINDOW_SIZE[0] // GROW_FACTOR, WINDOW_SIZE[0] - mouse_x + WINDOW_SIZE[0] // (GROW_FACTOR * 2)),
            min(WINDOW_SIZE[1] // GROW_FACTOR, WINDOW_SIZE[1] - mouse_y + WINDOW_SIZE[1] // (GROW_FACTOR * 2))
        )
        # Scale the zoom rect by GROW_FACTOR
        zoomed_surf = pygame.transform.scale(screen.subsurface(zoom_rect), (WINDOW_SIZE[0], WINDOW_SIZE[1]))
        # Fill the screen with black
        screen.fill((0, 0, 0))
        # Blit the zoomed surface to the screen
        screen.blit(zoomed_surf, (0, 0))

        # Shift to draw block grid
    if keys[pygame.K_LSHIFT]:

        #print("Drawing the grid")
        # Gee-pee-you
        # (GPU)
        # by making it convert alpha
        # i guess

        screen.blit(grid_surface, (-TILE_SIZE  -camera['x'] % (TILE_SIZE),-TILE_SIZE   -camera['y'] % (TILE_SIZE)))

    realscreen.blit(pygame.transform.scale(screen, (WINDOW_SIZE[0] * scale, WINDOW_SIZE[1] * scale)), (0, 0))
    # Draw stars
    realscreen.blit(founte.render("FPS: " + str(round(sum(times)/len(times))), True, (255, 255, 255)), (10, 10));times = times[max(0, len(times)-59):] + [(1000 / clock.tick(60))]

    # Help, if camera is far away from the blocks, then add a help mesasge. this is done using the used_area_bounds_pluS_screen_size
    if (fcamera['x'] < used_area_bounds_pluS_screen_size[0] * TILE_SIZE or 
        fcamera['x'] > used_area_bounds_pluS_screen_size[2] * TILE_SIZE or
        fcamera['y'] < used_area_bounds_pluS_screen_size[1] * TILE_SIZE or 
        fcamera['y'] > used_area_bounds_pluS_screen_size[3] * TILE_SIZE):
        #realscreen.blit(founte.render("You are too far away from the blocks!", True, (255, 0, 0)), (10, 30)) # Too aggressive
        realscreen.blit(founte.render("Lost in space? You can press SPACE to go back.", True, (255, 0, 0)), (10, 30)) # helöpfupl

    # warning thing
    if warning_thing[0] > 0:
        realscreen.blit(founte.render(warning_thing[1], True, (255, 0, 0)), (WINDOW_SIZE[0] // 2 - (founte.size(warning_thing[1])[0] // 2), WINDOW_SIZE[1] // 2 - founte.size(warning_thing[1])[1] // 2))
        warning_thing = (warning_thing[0] - 1, warning_thing[1])

    #print(times)
    pygame.display.flip()

pygame.quit()