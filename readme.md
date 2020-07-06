# N-Body Gravity Simulation #

## About ##
This project is a numerical simulation of the motion of objects given Newtonian forces acting on them.
The project is implemented in Python.

### Forces ###
The following forces that act on the bodies are,

 - [x] Gravity 
 - [x] Electric
 - [ ] Collision
 - [ ] Resistance


The forces in general are inverse square laws,

that is, $F = k \* b1 \* b2 / r^2 $
where k force coefficient, b1 & b2 depend on objects 1 & 2, and r is the distance between the two objects.


The objects obeys Newton's laws, which means F = ma

The force an object experiences, depends on the sum of all the forces felt between itself and all the other objects. 
This may also be expressed in terms of the idea of fields, in that  the sum of forces an object experiences is found by computing the interaction between the field and the object. The field is constructed indepently of the object, say object 1, and in general is given by F/b1.


The motion of the objects is calculated via ~~Euler~~ Runge-Kutte-4 Method, and the metric r is the Euclidean distance metric.

Please refer to [OrbitRungeKutta4.pdf](./OrbitRungeKutta4.pdf) for more information.

F(x,v) = F_G + F_E


All objects are updated one by one. That is update a body, then the next body is updated using the new information of the body previously updated, not it's origin position.



## Graphics ##

The visualisation of the objects motion is implemented via the [Pygame](https://www.pygame.org/wiki/about) module. The motion of objects will be in two-dimensions.

Each body can move in an arbitrary number of dimensions, however, each position vector is projected onto a two-dimensional plane. These planes currently can only be the co-ordinate axes.
Each body is assumed to be a 'sphere', and as such is drawn as a coloured circle.

The projection of the bodies has a particular 'focus', this is the point in space which is the centre of the screen. By default it is the co-ordinate origin. The second option is the centre of mass of the system. The final options are each body in order of body_id / order added to 'Universe'.


Currently, all objects/shapes are passed to pygame to draw, whether or not they are visible on the screen.




## Controls ##
 - Press the Space Bar to pause/resume the simulation.
 - Left arrow key - cycle between object in focus.
 - Right arrow key - same as left arrow key but in reverse.
 - Up arrow key - Zoom into the screen (x2).
 - Down arrow key - Zoom out of the screen (x2).
 - Enter - Return to default zoom settings.



## Future Ideas ##
 - Select arbitrary plane to project object motion onto.
 - Ability to change time step intervals.
 - Arbitrarily change zoom levels.
 - Add elastic & not elastic collision between bodies. Each body has an elastic co-efficient, amount of energy conserved between collisions is (b1.e * b2.e ) * (b1.E0 + b2.E0).
 - Apply conservation of momentum.
 - Ability to load arbitrary mass/charge systems  ==>  need to implement a parser.
 - Trails - lifetime trails & previous N steps.



## Related Project Ideas ##
 - Objects (balls) tethered together by a string. If one ball moves, then it drags along the other tethered objects.
 - Velocity field visualisation.
 - Bouncing particles in a box.


