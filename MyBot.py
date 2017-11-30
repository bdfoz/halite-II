"""
Welcome to your first Halite-II bot!

This bot's name is Settler. It's purpose is simple (don't expect it to win complex games :) ):
1. Initialize game
2. If a ship is not docked and there are unowned planets
2.a. Try to Dock in the planet if close enough
2.b If not, go towards the planet

Note: Please do not place print statements here as they are used to communicate with the Halite engine. If you need
to log anything use the logging module.
"""
# Let's start by importing the Halite Starter Kit so we can interface with the Halite engine
import hlt
# Then let's import the logging module so we can print out information
import logging
import time

# GAME START
# Here we define the bot's name as Settler and initialize the game, including communication with the Halite engine.
game = hlt.Game("Settler")
# Then we print our start message to the logs
logging.info("Starting my Settler bot!")
turn = 0

while True:
    start = time.perf_counter()
    turn += 1
    logging.info(turn)
    # TURN START
    # Update the map for the new turn and get the latest version
    game_map = game.update_map()

    # Here we define the set of commands to be sent to the Halite engine at the end of the turn
    command_queue = []

    ships = game_map.get_me().all_ships() #variable ships set to list of all ships
    goal_planets = game_map.all_planets() #variable planets set to list of all planets

#---NEW STUFF that does a bunch of nonsense
    for ship in ships:
        t_end = time.perf_counter() - start
        logging.info(t_end)
        if t_end > 1.5:
            break
        planet_dist = game_map.nearby_planets_by_distance(ship) #returns dictionary of {    distance: planet}
    
        more_planets = []
        for x in sorted(planet_dist):
            more_planets.append(planet_dist[x])

        #sends ships to the next planet if it's past turn 8 and the original goal planet is 100 percent full (all docking spots taken)
        if turn > 8:
            b = 0
            while more_planets[b][0].is_percent_full(100):
                b += 1
            else:
                planet = more_planets[b][0]
        else:
            planet = goal_planets[ship.id % len(goal_planets)]



#---NEW STUFF that does a bunch of nonsense

            #IF GOAL_PLANETS IS CHANGED TO PLANETS_BY_DIST, THE SHIPS JUST SPAZZ OUT
        #planet = goal_planets[ship.id % len(goal_planets)] #ship.id prevents sudden change of direction when ships len changes

                # If we can dock, let's (try to) dock. If two ships try to dock at once, neither will be able to.
        if ship.can_dock(planet):
                    # We add the command by appending it to the command_queue
            command_queue.append(ship.dock(planet))
        elif planet.owner != ship.owner and planet.owner != None:
            navigate_command = ship.navigate(ship.closest_point_to(planet.all_docked_ships()[0]), game_map, speed=hlt.constants.MAX_SPEED)
            if navigate_command:
                command_queue.append(navigate_command)
        else:
                    # If we can't dock, we move towards the closest empty point near this planet (by using closest_point_to)
                    # with constant speed. Don't worry about pathfinding for now, as the command will do it for you.
                    # We run this navigate command each turn until we arrive to get the latest move.
                    # Here we move at half our maximum speed to better control the ships. NOT ANY MORE, SON!
                    # In order to execute faster we also choose to ignore ship collision calculations during navigation.
                    # This will mean that you have a higher probability of crashing into ships, but it also means you will
                    # make move decisions much quicker. As your skill progresses and your moves turn more optimal you may
                    # wish to turn that option off.
            navigate_command = ship.navigate(ship.closest_point_to(planet), game_map, speed=hlt.constants.MAX_SPEED)
                    # If the move is possible, add it to the command_queue (if there are too many obstacles on the way
                    # or we are trapped (or we reached our destination!), navigate_command will return null;
                    # don't fret though, we can run the command again the next turn)
            if navigate_command:
                command_queue.append(navigate_command)
        continue
        logging.infO(t_end)


        # Send our set of commands to the Halite engine for this turn
    game.send_command_queue(command_queue)
    # TURN END
# GAME END