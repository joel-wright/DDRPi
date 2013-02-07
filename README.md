DDRPi
=====

DDRPi Controller Software.

The code lives! We can now switch between plugins, and play a game of Tetris :)

Main system controls:

        Select - Enter/Exit Menu Mode
        Start  - Start running the currently selected plugin
        LB/RB  - Switch between plugins in menu mode

Tetris Controls
---------------

The obvious direction controls are as you'd expect (we ignore up of course). The
other buttons are as follows:

        Start - Pause/Resume (also start a new game when on has ended)
        A/B   - Rotate right/left
        Y     - Drop the current piece
        X     - Start a new game when paused

Pong Controls
-------------

The position of the bats are controlled using either axis as follows:

        Up/Down    - Up and down obviously
        Left/Right - Dependends on the player (player2's controls are inverted
                     so that the game can be played form either end of the floor
                     with the two players facing each other)
        Start      - Pause/Resume and start a new game if one has ended
        X          - Start a new game when paused

Running a simple test
---------------------

You can run a simple test by checking out the repository and using the floor
simulator found in the "tests" folder.

1. Check out the repository
2. Create a pipe for testing using mkfifo:

        mkfifo <pipe_name>
    
3. Make sure debugging is set to True in config.yaml and configure the pipe
4. Copy config.yaml into the tests folder
5. Start the floorSimulator:

        cd tests
        python ./floorSimulator.py
    
6. Start the main DDRPi app:

        python ./DDRPi.py
    
You should now see the inintial menu screen. A preview of each plugin is shown
by pressing the buffer buttons. When you see the plugin you want, press start
and the plugin will start running.

Debugging
---------

Debug logging can be configured in the config.yaml file, and a specific plugin
can be loaded at startup by specifying its class name at the command line.
