from trafficSimulator import *

sim = Simulation()

lane_space = 3.5
intersection_size = 12*5
length = 100


# SOUTH, EAST, NORTH, WEST

# Intersection in
for idx in range(2):
    idx_gap = idx * (2*length+intersection_size)
    sim.create_segment((idx_gap+lane_space/2, length+intersection_size/2), (idx_gap+lane_space/2, intersection_size/2))
    sim.create_segment((idx_gap+length+intersection_size/2, -lane_space/2), (idx_gap+intersection_size/2, -lane_space/2))    
    sim.create_segment((idx_gap-lane_space/2, -length-intersection_size/2), (idx_gap-lane_space/2, -intersection_size/2))
    sim.create_segment((idx_gap-length-intersection_size/2, lane_space/2), (idx_gap-intersection_size/2, lane_space/2))

# Intersection out
    sim.create_segment((idx_gap-lane_space/2, intersection_size/2), (idx_gap-lane_space/2, length+intersection_size/2))
    sim.create_segment((idx_gap+intersection_size/2, lane_space/2), (idx_gap+length+intersection_size/2, lane_space/2))
    sim.create_segment((idx_gap+lane_space/2, -intersection_size/2), (idx_gap+lane_space/2, -length-intersection_size/2))
    sim.create_segment((idx_gap-intersection_size/2, -lane_space/2), (idx_gap-length-intersection_size/2, -lane_space/2))
# Straight
    sim.create_segment((idx_gap+lane_space/2, intersection_size/2), (idx_gap+lane_space/2, -intersection_size/2))
    sim.create_segment((idx_gap+intersection_size/2, -lane_space/2), (idx_gap-intersection_size/2, -lane_space/2))
    sim.create_segment((idx_gap-lane_space/2, -intersection_size/2), (idx_gap-lane_space/2, intersection_size/2))
    sim.create_segment((idx_gap-intersection_size/2, lane_space/2), (idx_gap+intersection_size/2, lane_space/2))
# Right turn
    sim.create_quadratic_bezier_curve((idx_gap+lane_space/2, intersection_size/2), (idx_gap+lane_space/2, lane_space/2), (idx_gap+intersection_size/2, lane_space/2))
    sim.create_quadratic_bezier_curve((idx_gap+intersection_size/2, -lane_space/2), (idx_gap+lane_space/2, -lane_space/2), (idx_gap+lane_space/2, -intersection_size/2))
    sim.create_quadratic_bezier_curve((idx_gap-lane_space/2, -intersection_size/2), (idx_gap-lane_space/2, -lane_space/2), (idx_gap-intersection_size/2, -lane_space/2))
    sim.create_quadratic_bezier_curve((idx_gap-intersection_size/2, lane_space/2), (idx_gap-lane_space/2, lane_space/2), (idx_gap-lane_space/2, intersection_size/2))
# Left turn
    sim.create_quadratic_bezier_curve((idx_gap+lane_space/2, intersection_size/2), (idx_gap+lane_space/2, -lane_space/2), (idx_gap-intersection_size/2, -lane_space/2))
    sim.create_quadratic_bezier_curve((idx_gap+intersection_size/2, -lane_space/2), (idx_gap-lane_space/2, -lane_space/2), (idx_gap-lane_space/2, intersection_size/2))
    sim.create_quadratic_bezier_curve((idx_gap-lane_space/2, -intersection_size/2), (idx_gap-lane_space/2, lane_space/2), (idx_gap+intersection_size/2, lane_space/2))
    sim.create_quadratic_bezier_curve((idx_gap-intersection_size/2, lane_space/2), (idx_gap+lane_space/2, lane_space/2), (idx_gap+lane_space/2, -intersection_size/2))


vg = VehicleGenerator({
    'vehicle_rate':20,
    #down
    'vehicles': [
        (3, {'path': [0, 8, 6], 'v': 6.6}),#straight
        (1, {'path': [0, 12, 5, 20+3, 20+11, 20+5], 'v': 6.6}),#right/straight
        (1, {'path': [0, 12, 5, 20+3, 20+15, 20+4], 'v': 6.6}),#right/right
        (1, {'path': [0, 12, 5, 20+3, 20+19, 20+6], 'v': 6.6}),#right/left
        (3, {'path': [0, 16, 7], 'v': 6.6})#left
        ]
    })
sim.add_vehicle_generator(vg)

'''
vg = VehicleGenerator({
    'vehicle_rate':20,
    #right
    'vehicles': [
        (1, {'path': [1, 9, 7], 'v': 6.6}),#straight
        (1, {'path': [1, 13, 6], 'v': 6.6}),#right
        (1, {'path': [1, 17,4], 'v': 6.6})#left
        ]
    })
sim.add_vehicle_generator(vg)
'''

vg = VehicleGenerator({
    'vehicle_rate':20,
    #up
    'vehicles': [
        (3, {'path': [2,10,4], 'v': 6.6}),#straight
        (3, {'path': [2,14,7], 'v': 6.6}),#right
        (1, {'path': [2,18,5, 20+3, 20+11, 20+5], 'v': 6.6}),#left/straight
        (1, {'path': [2,18,5, 20+3, 20+15, 20+4], 'v': 6.6}),#left/right
        (1, {'path': [2,18,5, 20+3, 20+19, 20+6], 'v': 6.6})#left/left
        ]
    })
sim.add_vehicle_generator(vg)

vg = VehicleGenerator({
    'vehicle_rate':20,
    #left
    'vehicles': [
        (1, {'path': [3,11,5, 20+3, 20+11, 20+5], 'v': 6.6}),#straight/straight
        (1, {'path': [3,11,5, 20+3, 20+15, 20+4], 'v': 6.6}),#straight/right
        (1, {'path': [3,11,5, 20+3, 20+19, 20+6], 'v': 6.6}),#straight/left
        (3, {'path': [3,15,4], 'v': 6.6}),#right
        (3, {'path': [3,19,6], 'v': 6.6})#left
        ]
    })
sim.add_vehicle_generator(vg)

#cross_two
vg = VehicleGenerator({
    'vehicle_rate':20,
    #down
    'vehicles': [
        (3, {'path': [20+0, 20+8, 20+6], 'v': 6.6}),#straight
        (3, {'path': [20+0, 20+12, 20+5], 'v': 6.6}),#right
        (1, {'path': [20+0, 20+16, 20+7,1,9,7], 'v': 6.6}),#left/straight
        (1, {'path': [20+0, 20+16, 20+7,1,13,6], 'v': 6.6}),#left/right
        (1, {'path': [20+0, 20+16, 20+7,1,17,4], 'v': 6.6})#left/left
        ]
    })
sim.add_vehicle_generator(vg)

vg = VehicleGenerator({
    'vehicle_rate':20,
    #right
    'vehicles': [
        (1, {'path': [20+1, 20+9, 20+7,1,9,7], 'v': 6.6}),#straight/straight
        (1, {'path': [20+1, 20+9, 20+7,1,13,6], 'v': 6.6}),#straight/right
        (1, {'path': [20+1, 20+9, 20+7,1,17,4], 'v': 6.6}),#straight/left
        (3, {'path': [20+1, 20+13, 20+6], 'v': 6.6}),#right
        (3, {'path': [20+1, 20+17, 20+4], 'v': 6.6})#left
        ]
    })
sim.add_vehicle_generator(vg)

vg = VehicleGenerator({
    'vehicle_rate':20,
    #up
    'vehicles': [
        (3, {'path': [20+2, 20+10, 20+4], 'v': 6.6}),#straight
        (1, {'path': [20+2, 20+14, 20+7,1,9,7], 'v': 6.6}),#right/straight
        (1, {'path': [20+2, 20+14, 20+7,1,13,6], 'v': 6.6}),#right/right
        (1, {'path': [20+2, 20+14, 20+7,1,17,4], 'v': 6.6}),#right/left
        (3, {'path': [20+2, 20+ 18, 20+5], 'v': 6.6}),#left
        ]
    })
sim.add_vehicle_generator(vg)

win = Window(sim)
win.run()
win.show()