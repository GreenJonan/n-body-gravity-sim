# N-Body Gravity Simulation #


## MacOsX Download Link ##
[Google Drive](https://drive.google.com/file/d/1bYIQkuSph9HRsOmxqMfeMI0dqJ7aLsib/view?usp=sharing)


## About ##
This project is a numerical simulation of the motion of objects given Newtonian forces acting on them.
The project is implemented in Python.

### Forces ###
The following forces that act on the bodies are,

 - [x] Gravity 
 - [x] Electric
 - [x] Linear Momentum Collision
 - [x] Crude all-body Drag


The forces in general are inverse square laws,

that is, $F = k \* b1 \* b2 / r^2 $
where k force coefficient, b1 & b2 depend on objects 1 & 2, and r is the distance between the two objects.


The objects obeys Newton's laws, which means F = ma

The force an object experiences, depends on the sum of all the forces felt between itself and all the other objects. 
This may also be expressed in terms of the idea of fields, in that  the sum of forces an object experiences is found by computing the interaction between the field and the object. The field is constructed indepently of the object, say object 1, and in general is given by F/b1.


The motion of the objects is calculated via ~~Euler~~ Runge-Kutte-4 Method, and the metric r is the Euclidean distance metric.

Please refer to [OrbitRungeKutta4.pdf](http://spiff.rit.edu/richmond/nbody/OrbitRungeKutta4.pdf) for more information.

F(x,v) = F_G + F_E


All objects are updated one by one. That is update a body, then the next body is updated using the new information of the body previously updated, not it's origin position.



## Graphics ##

The visualisation of the objects motion is implemented via the [Pygame](https://www.pygame.org/wiki/about) module. The motion of objects will be in two-dimensions.

Each body can move in an arbitrary number of dimensions, however, each position vector is projected onto a two-dimensional plane. These planes currently can only be the co-ordinate axes.
Each body is assumed to be a 'sphere', and as such is drawn as a coloured circle.

The projection of the bodies has a particular 'focus', this is the point in space which is the centre of the screen. By default it is the co-ordinate origin. The second option is the centre of mass of the system. The final options are each body in order of body_id / order added to 'Universe'.


Currently, all objects/shapes are passed to pygame to draw, and are drawn only if they intersect the rectangle of the screen, i.e. they are visible.



Objects can retail their spatial history in the form of trails. Activating this requires trailHistory:True in the input .sys file, and the trail number for each body object must be large enough that the trails are visible. The trails will be computed with their positions relative to the central object in which they are activated.



## Collisions ##


When objects collide they bounce off each other via the principle of conservation of momenta. Their velcotities remain constant along the plane between the two balls, and is updated along the line connecting their centres.
Momentum is updated per pair of collisions, rather than consider the net collisions on one body. Say BodyA hits BodyB and BodyC, but BodyB does not hit BodC. We update the velcoties via principle of conservation of momentum first with A,B, and then with B,C. Consequently this means B will be knocked further away from A than C, even though the momentum should be evenly exchanged between the two.
An alterante method is to update the velocity of B,C using conservation of momentum and then adjust A by once again applying the conservation of momentum. However, this method is not symmetric with whether A hits B&C, or B&C hit A, this is because of the finite step iteration of the program, in that it adjusted A, then B, then C, rather than all of them at once.



## Controls ##
 - Press the Space Bar to pause/resume the simulation.
 - Left arrow key - cycle between object in focus.
 - Right arrow key - same as left arrow key but in reverse.
 - Up arrow key - Zoom into the screen (x2).
 - Down arrow key - Zoom out of the screen (x2).
 - Return - Return to default zoom settings.
 - 't' to enable and disable trails. 
 - 'c' to dynamically adjust the momenta of bodies.
 - 'p' to pan the camera around, left click and drag.




## .sys files ##
These are the files which the program reads, parses and constucts a system of bodies. These are custom file types that are text documents.
They are constructed by nested objects with attibutes. Consider the following example,

`
Object {
    attribute: value
    attribute2:sub_object {
        subsub_object{}
    }
}
`

In addition, they support maths operations, variables and for loops.

For the more information about the objects, attributes, and syntax, please look at about.txt in the systems directory.





## Future Ideas ##
 - [ ] Select arbitrary plane to project object motion onto.
 - [ ] Ability to dynamically change time step intervals.
 - [x] Arbitrarily change zoom levels.
 - [x] Add elastic & not elastic collision between bodies. Each body has an elastic co-efficient, amount of energy conserved between collisions is (b1.e * b2.e ) * (b1.E0 + b2.E0).
 - [x] Apply conservation of momentum.
 - [x] Ability to load arbitrary mass/charge systems  ==>  need to implement a parser.
 - [x] Trails - lifetime trails & previous N steps.
 - [ ] Multithreading.




## Related Project Ideas ##
 - Objects (balls) tethered together by a string. If one ball moves, then it drags along the other tethered objects.
 - Velocity field visualisation.
 - Bouncing particles in a box.
 - Object simulation with hooke's law connection objects, that is everything as a mass spring system.


