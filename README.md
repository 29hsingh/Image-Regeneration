# Image-Regeneration
Regenerating RGB and bitmap images using evolutionary algorithm / Data Science
There are two different programs, rgb_img.py takes rgb image and regenerate image in rgb profile, bitmap_img.py takes rgb image and regenrates the bitmap image.
Analytics-> evolution graph and final regenerated image is shown after the execution of program, state at any other generation can be seen by modifying parameter of analytics() function.
Feed an image to the algorithm, it will gragually evolve the the image from completely random rgb values, in each generation it compares the fittest condidate (of that generation ) with the real images and finds its path by improving the score and passing the fittest genes to the next generation.
