System to Regulate Traffic Lights at 4-way Stop ( Specification Vs Design Vs Implementation) 

Specification:

1.  Using Traffic and Pedestrian Lights at the 4-way crossing, actively manage both vehicle and pedestrian traffic
2.  at most one set of lights facing cross streets   at an intersection is green for Vehicular traffic
3.  Safely move pedestrian traffic across the intersections while allowing movable vehicle traffic in other directions
4.  Safely pass right, left and through-pass vehicle traffic at the intersection


Design:

1. Synch the timing of color changes timing of lights facing the opposite directions (i.e. light facing north and south should be the same color at the same time)
2. When north/south facing lights are green or yellow then east/west facing lights should be red ( and v.v.)
3. Transition of colors should be green for x seconds then yellow for y seconds then red for z seconds then back to green
4. Anticipate all secure and unsecure states and implement mechanisms (traffic light sequences) to ensure a secure state
