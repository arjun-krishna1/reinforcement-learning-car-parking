# Pymunk physics engine
- http://www.pymunk.org/en/latest/overview.html
## Basic Classes
### Rigid Bodies (pymunk.Body)
- holds physical props of an obj
- mass, position, rotation, velocity, etc.
- doesn't have a shape by itself

### Collision Shapes (pymunk.Poly, pymunk.Segment)
- attach shapes to bodies

### pymunk.Space
- basic simulation unit in Pymunk
- add bodies, shapes to space
- update the space as a whole
- actual simulation is done here
- after objects are added, space time is moved forward in small constant time steps with the
- pymunk.Space.step() -> move time forward with a constant delta t(dt)
    - makes sim constant
- using a smaller dt value
- run python with optimizations on
    - python -o ....


## What do we wnat pymunk to do?
- define rectangle (car)
- define polygons (obstacles)
- update rectangle's steering velocity and acceleration at various times
- detect if collision, have position, velocity update automatically based on heading, velocity, acceleration, etc

## Examples
- `spiderweb.py`