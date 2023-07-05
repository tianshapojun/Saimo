import trafficSimulator as ts

sim = ts.Simulation()

# Add road segments
sim.create_segment((-100, 10), (100, 10))
sim.create_segment((100, -10), (-100, -10))

# Add vehicle generator
sim.create_vehicle_generator(
    vehicle_rate=60,
    vehicles=[
        (10, {'path': [0], 'v': 16.6}),
        (1, {'path': [0], 'v': 16.6, 'l': 7}),

        (10, {'path': [1], 'v': 16.6}),
        (1, {'path': [1], 'v': 16.6, 'l': 7})
        ]
    )

# Show simulation visualization
win = ts.Window(sim)
win.show()
