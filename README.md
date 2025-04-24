This is a project to test my capability to use Object Oriented programming, Pygame library, and a whole load of maths.

    STRUCTURE

    This package is built out of main.py. Imported, you'll find all the assets I've defined, balls, cushions, pockets ect.

    game_functions.py holds the basic functions of the game, for example 'check for wall colission', which measures each balls distance against a rail, and if it detects a colission, it reverses the appropriate velocity component. These functions are the 'physics engine' of the game, and are packaged together into 'modules' which make up the behaviours of the phases of the game. These macro scripts are held in game_modules.py

    Game Modules, named 'gm' holds 3 functions, which make up the 3 phases of the game:
        'gm.handle_aiming' which allows the user to adjust the white balls velocity components 

How to main method works:

    SETUP

    The program begins with creating all the assets we will use for the game. Currently, I use the approach where an asset(lets say a rail) will have a 'position' attribute. Here, when we supply a position (lets say top), the contrructor for this instance will run through a 'if' statement, and when its 'position' attribute meets the criteria, its specific spacial coordinates are set.

    This happens for the table, pockets, balls, rails, and triangle cushions around the corners.

    Then, these assets are grouped (ie each cushion will be added to a list 'cushions)

    Notice in the code, all fo the balls positions (and in once case, initial velocity components) are manuallly set. This is for the testing environment to allow ease of interactivity (You dont want to the chance invovled in a break if you're testing certain scenarios).

    Then we create the buttons, or UI for the game. This consists of the shoot button, power percentage indicator, and the guinelines for aiming.

    Finally, we create the 2 instances of a player class, and assign them an active and inactive player, which informs the system who the next turn belongs to.

    MAIN METHOD

        EVENT LOOP

        First, we check all the events (read: user input events) our system can recognise, which is just mouse button one down. We check against the 2 functions our user can complete with this, clicking the table and therefore aiming the shot, or using the buttons, using 'flags' in our settings object to decide whether the user can currently access them (for instance, dont let the player register another shot whilst the ball is moving)

        We also recosnigse mouse button up events, which we can see set the flags 'aiming' or 'deciding power' to false. This means when the player releases their mouse, their final states are stored.

        DRAW THE SCREEN

        This simple function draws every asset in every group.

        GM.HANDLE_AIMING

        This module handles all the processes involved when a player is aiming their shot. Looking through the methods called in this module, we can see we:
        
            - Replace the white if it was potten in the previous turn
            - decleare the startpoint of the guideline
            - order the balls from nearest to furtherest from the cue ball
            - find the endpoint of the guideline (when the player clicks)
            - adjust the cue balls velocity compinents based on guideline aim
            - draw the guideline
            - if the guideline intersects with a ball:
                - draw the 'ghost ball' where they meet
                - draw the paths of the target ball and ghost ball post colission
            - if the player clicks the cue:
                - adjust the power of the shot

        This method will be called on each frame, until the user clicks the shoot button, which sets the flag 'settings.deciding_shot = false' and 'settings.moving_balls = true'

        GM.MOVE_BALLS

        Now settings.moving_balls is true, the system recognises the user has finalised their aim and power. Now, the system enters a phase of 'simulation', where the balls are 'unfrozen', and if a ball has a velocity (initially only the cue ball), they move and interact with other balls, pockets and rails. Looking through this module, the following processes are called each frame:

            - each ball is checked against every other ball to determine if they have collided
            - if they have, apply the 2D coefficient of restitution equations to calculate ther new velocity components, and apply them to the ball
            - check for wall colissions, and adjust velocity as required
            - check for pocket colissions, and move ball to 'pocketed_balls' list if ball was pocketed
            - check for colission with 45 degree walls near pockets, and adjust velocity accordingly
            - apply friction, slowing the balls speed
            - update the balls x and y coordinates from velocity
            - check for no speed (once each ball in balls has stopped moving, this stage is over)

        This method moves all the balls based off user input in the aiming phase, and simulated the balls moving until they are all at rest, where the system can then evaluate what happened during this phase

        GM.EVALUATE_SHOT

        This phase evaluates what happened in the shot just taken. It uses variables saved in the previous phase (ie. first contact, balls pocketed, player teams, advantages ect.) to determine the success of the shot, which ultimatesly decides on who takes the next shot, if a player has won, or if a player has fowled.

        NOTE: This module is written poorly with no forward planning, and whilst it may currently work, requires refactoring to a simpler workflow.

