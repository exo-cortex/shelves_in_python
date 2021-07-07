#shelf design in python

This project is my attempt of designing a big shelf that fits all the stuff lying around without a fixed place. 
By defining the parameters wood thickness, width, height, depth, number of compartments (vertical and horizontal) it shall ouput all needed parts plus prices.
Ideally it shall also output a 3D render of the finished object.

## Algorithm

- set: {THICKNESS, HEIGHT, WIDTH}

- define list of compartment heights, extend to fill total HEIGHT  
- for each horizontal compartment define list of compartment widths, extend lists to fill total WIDTH
- from compartment heights and widths make list of horizontal and vertical board dimensions + positions