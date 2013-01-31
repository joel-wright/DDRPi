DDRPi
=====

DDRPi Controller Software.

Nothing much to look at yet, but hopefully this will change very soon :)

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
    
6. Move the (currently broken) tetris plugin out of the "plugins" folder
7. Start the main DDRPi app:

    python ./DDRPi.py
    
You should now see random patterns on a simulated dance floor that corresponds
to your config file... Have fun :)


