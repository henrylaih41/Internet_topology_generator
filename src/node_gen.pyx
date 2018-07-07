import project_utility as pu
# By writing this function in cython, the generation time of node is reduce by a factor of 2
def get_distance(float x_pos,float ox_pos,float y_pos,float oy_pos):
    cdef float delta_x = abs(x_pos - ox_pos)
        # The Earth is round, so the distance between x coordinate will not exceed 18000 
        # (We've set the width of Earth to 36000)  
        # y cordinate is another case, since we have considered the polar area uncrossable.
    if (delta_x > 18000):
        delta_x = 36000 - delta_x
    return ((delta_x)**2 + (y_pos - oy_pos)**2)**0.5