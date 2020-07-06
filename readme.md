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


The motion of the objects is calculated via Euler ~~Runge-Kutte~~ Method, and the metric r is the Euler Distance metric.

F(x,v) = F_G + F_E


The visualisation of the objects motion is implemented via the [Pygame](https://www.pygame.org/wiki/about) module. The motion of objects will be in two-dimensions.



## Things to implement ##
 - Multi-dimensional motion (objects moves in more than two-dimensions)




## Related Project Ideas ##
 - Objects (balls) tethered together by a string. If one ball moves, then it drags along the other tethered objects.
 - Velocity field visualisation.
 - Bouncing particles in a box.


