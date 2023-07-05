from trafficSimulator import *
from torch import nn
import torch
import time

class MLP(nn.Module):
    def __init__(self, dim1, hidden_dim, dim2, dropout=0.):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(dim1, hidden_dim),
            nn.GELU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_dim, hidden_dim),
            nn.Linear(hidden_dim, hidden_dim),
            nn.Linear(hidden_dim, dim2),
            nn.Dropout(dropout)
        )

    def forward(self, x):
        return self.net(x)
    

model = MLP(3,100,3)
'''
nb = 700
input = torch.rand(nb,3)
t1 = time.time()
output=model(input)
print('OneEpoch:',time.time()-t1)

t2 = time.time()
for i in range(nb):
    output = model(input[i])
print('Separate:',time.time()-t2)

hhh
'''

sim = Simulation(model)

lane_space = 3.5
intersection_size = 12*5
length = 100
width = 5
height = 5

# SOUTH, EAST, NORTH, WEST

# Intersection in
for idx in range(width):
    for idy in range(height):
        idx_gap = idx * (2*length+2*intersection_size)
        idy_gap = idy * (2*length+2*intersection_size)
        sim.create_segment((idx_gap+lane_space/2, idy_gap+length+intersection_size/2), (idx_gap+lane_space/2, idy_gap+intersection_size/2))
        sim.create_segment((idx_gap+length+intersection_size/2, idy_gap-lane_space/2), (idx_gap+intersection_size/2, idy_gap-lane_space/2))    
        sim.create_segment((idx_gap-lane_space/2, idy_gap-length-intersection_size/2), (idx_gap-lane_space/2, idy_gap-intersection_size/2))
        sim.create_segment((idx_gap-length-intersection_size/2, idy_gap+lane_space/2), (idx_gap-intersection_size/2, idy_gap+lane_space/2))

# Intersection out
        sim.create_segment((idx_gap-lane_space/2, idy_gap+intersection_size/2), (idx_gap-lane_space/2, idy_gap+length+intersection_size/2))
        sim.create_segment((idx_gap+intersection_size/2, idy_gap+lane_space/2), (idx_gap+length+intersection_size/2, idy_gap+lane_space/2))
        sim.create_segment((idx_gap+lane_space/2, idy_gap-intersection_size/2), (idx_gap+lane_space/2, idy_gap-length-intersection_size/2))
        sim.create_segment((idx_gap-intersection_size/2, idy_gap-lane_space/2), (idx_gap-length-intersection_size/2, idy_gap-lane_space/2))
# Straight
        sim.create_segment((idx_gap+lane_space/2, idy_gap+intersection_size/2), (idx_gap+lane_space/2, idy_gap-intersection_size/2))
        sim.create_segment((idx_gap+intersection_size/2, idy_gap-lane_space/2), (idx_gap-intersection_size/2, idy_gap-lane_space/2))
        sim.create_segment((idx_gap-lane_space/2, idy_gap-intersection_size/2), (idx_gap-lane_space/2, idy_gap+intersection_size/2))
        sim.create_segment((idx_gap-intersection_size/2, idy_gap+lane_space/2), (idx_gap+intersection_size/2, idy_gap+lane_space/2))
# Right turn
        sim.create_quadratic_bezier_curve((idx_gap+lane_space/2, idy_gap+intersection_size/2), (idx_gap+lane_space/2, idy_gap+lane_space/2), (idx_gap+intersection_size/2, idy_gap+lane_space/2))
        sim.create_quadratic_bezier_curve((idx_gap+intersection_size/2, idy_gap-lane_space/2), (idx_gap+lane_space/2, idy_gap-lane_space/2), (idx_gap+lane_space/2, idy_gap-intersection_size/2))
        sim.create_quadratic_bezier_curve((idx_gap-lane_space/2, idy_gap-intersection_size/2), (idx_gap-lane_space/2, idy_gap-lane_space/2), (idx_gap-intersection_size/2, idy_gap-lane_space/2))
        sim.create_quadratic_bezier_curve((idx_gap-intersection_size/2, idy_gap+lane_space/2), (idx_gap-lane_space/2, idy_gap+lane_space/2), (idx_gap-lane_space/2, idy_gap+intersection_size/2))
# Left turn
        sim.create_quadratic_bezier_curve((idx_gap+lane_space/2, idy_gap+intersection_size/2), (idx_gap+lane_space/2, idy_gap-lane_space/2), (idx_gap-intersection_size/2, idy_gap-lane_space/2))
        sim.create_quadratic_bezier_curve((idx_gap+intersection_size/2, idy_gap-lane_space/2), (idx_gap-lane_space/2, idy_gap-lane_space/2), (idx_gap-lane_space/2, idy_gap+intersection_size/2))
        sim.create_quadratic_bezier_curve((idx_gap-lane_space/2, idy_gap-intersection_size/2), (idx_gap-lane_space/2, idy_gap+lane_space/2), (idx_gap+intersection_size/2, idy_gap+lane_space/2))
        sim.create_quadratic_bezier_curve((idx_gap-intersection_size/2, idy_gap+lane_space/2), (idx_gap+lane_space/2, idy_gap+lane_space/2), (idx_gap+lane_space/2, idy_gap-intersection_size/2))


for i in range(width*height):
    idx = 20*i
    vg = VehicleGenerator({
    'vehicle_rate':20,
    #down
    'vehicles': [
        (1, {'path': [idx+0, idx+8, idx+6], 'v': 6.6}),#straight
        (1, {'path': [idx+0, idx+12, idx+5], 'v': 6.6}),#right
        (1, {'path': [idx+0, idx+16, idx+7], 'v': 6.6})#left
        ]
    })
    sim.add_vehicle_generator(vg)

    vg = VehicleGenerator({
    'vehicle_rate':20,
    #right
    'vehicles': [
        (1, {'path': [idx+1, idx+9, idx+7], 'v': 6.6}),#straight
        (1, {'path': [idx+1, idx+13, idx+6], 'v': 6.6}),#right
        (1, {'path': [idx+1, idx+17,idx+4], 'v': 6.6})#left
        ]
    })
    sim.add_vehicle_generator(vg)

    vg = VehicleGenerator({
    'vehicle_rate':20,
    #up
    'vehicles': [
        (1, {'path': [idx+2,idx+10,idx+4], 'v': 6.6}),#straight
        (1, {'path': [idx+2,idx+14,idx+7], 'v': 6.6}),#right
        (1, {'path': [idx+2,idx+18,idx+5], 'v': 6.6})#left
        ]
    })
    sim.add_vehicle_generator(vg)

    vg = VehicleGenerator({
    'vehicle_rate':20,
    #left
    'vehicles': [
        (1, {'path': [idx+3,idx+11,idx+5], 'v': 6.6}),#straight
        (1, {'path': [idx+3,idx+15,idx+4], 'v': 6.6}),#right
        (1, {'path': [idx+3,idx+19,idx+6], 'v': 6.6})#left
        ]
    })
    sim.add_vehicle_generator(vg)

win = Window(sim)
win.run()
win.show()
