"""
A simple MUD game. Players can talk to each other, examine
their surroundings and move between rooms.

Some ideas for things to try adding:
    * More rooms to explore
    * Items to look at in rooms e.g. 'look fireplace' -> 'You see a roaring, glowing fire'
    * Items to pick up e.g. 'take rock' -> 'You pick up the rock'
    * Monsters to fight
    * Loot to collect
    * Saving players accounts between sessions
    * A password login
    * A shop from which to buy items

"""

# import the MUD server class
from mudserver import MudServer
# import time for the "100% CPU hack"
import time
# import re to allow for regex matching
import re

# structure defining the rooms in the game. Try adding more rooms to the game!
rooms = {
    "Tavern": {
        "description": "You're in a cozy tavern warmed by an open fire.",
        "exits": { "outside": "Outside" },
    },
    "Outside": {
        "description": "You're standing outside a tavern. It's raining.",
        "exits": { "inside": "Tavern", "down": "Down the hill" },
    },
    "Down the hill": {
        "description": "You are on a winding road that leads down a hill.\nOff in the distance you can see the dock to the ships and hear seagulls cackling overhead.",
        "exits": { "up": "Outside", "down": "Dock" },
    },
    "Dock": {
        "description": "You are standing on the bustling dock of Port Royal!",
        "exits": { "up": "Down the hill" },
    }
}

# stores the players in the game
players = {}

# start the server
mud = MudServer()

# main game loop. We loop forever (i.e. until the program is terminated)
while True:


    # 'update' must be called in the loop to keep the game running and give
    # us up-to-date information
    mud.update()


    # go through any newly connected players
    for id in mud.get_new_players():

        # add the new player to the dictionary, noting that they've not been
        # named yet.
        # The dictionary key is the player's id number. Start them off in the
        # 'Tavern' room.
        # Try adding more player stats - level, gold, inventory, etc
        players[id] = {
            "name": None,
            "room": "Tavern",
            "level": 1,
            "gold": 2,
            "inventory": "boomerang",
        }

        # send the new player a prompt for their name
        mud.send_message(id,"What is your name?")


    # go through any recently disconnected players
    for id in mud.get_disconnected_players():

        # if for any reason the player isn't in the player map, skip them and
        # move on to the next one
        if id not in players: continue

        # go through all the players in the game
        for pid,pl in players.items():
            # send each player a message to tell them about the diconnected player
            mud.send_message(pid,"%s quit the game" % players[id]["name"])

        # remove the player's entry in the player dictionary
        del(players[id])


    # go through any new commands sent from players
    for id,command,params in mud.get_commands():

        # if for any reason the player isn't in the player map, skip them and
        # move on to the next one
        if id not in players: continue

        # if the player hasn't given their name yet, use this first command as their name
        if players[id]["name"] is None:

            players[id]["name"] = command

            # go through all the players in the game
            for pid,pl in players.items():
                # send each player a message to tell them about the new player
                mud.send_message(pid,"%s entered the game" % players[id]["name"])

            # send the new player a welcome message
            mud.send_message(id,"Welcome to the game, %s. Type 'help' for a list of commands. Have fun!" % players[id]["name"])
            mud.send_message(id,"You are level: %s" % players[id]["level"])
            mud.send_message(id,"You have %s gold." % players[id]["gold"])
            mud.send_message(id,"Inventory: %s" % players[id]["inventory"])

            # send the new player the description of their current room
            mud.send_message(id,rooms[players[id]["room"]]["description"])

        # each of the possible commands is handled below. Try adding new commands
        # to the game!

        # 'help' command
        elif command == "help":

            # send the player back the list of possible commands
            mud.send_message(id,"Commands:")
            mud.send_message(id,"  say <message>              - Says something out loud, e.g. 'say Hello'")
            mud.send_message(id,"  look                       - Examines the surroundings, e.g. 'look'")
            mud.send_message(id,"  go <exit>                  - Moves through the exit specified, e.g. 'go outside'")
            mud.send_message(id,"  emote <action>             - Perform an action or emotion, e.g. 'emote laughs'")
            mud.send_message(id,"  shout <message>            - Shout to all players")
            mud.send_message(id,"  whisper <player> <message> - private whisper to a specific player")

        # 'emote' command
        elif command == "emote" or command == "e":
            # go through every player in the game
            for pid,pl in players.items():
                # if they're in the same room as the player
                if players[pid]["room"] == players[id]["room"]:
                    # send them the emote
                    mud.send_message(pid, "%s %s" % (players[id]["name"],params) )

        # 'say' command
        elif command in ("say", "s"):

            # go through every player in the game
            for pid,pl in players.items():
                # if they're in the same room as the player
                if players[pid]["room"] == players[id]["room"]:
                    # send them a message telling them what the player said
                    mud.send_message(pid,"%s says: %s" % (players[id]["name"],params) )

        # 'shout' command
        elif command in ("shout", "sh"):

            # go through every player in the game
            for pid,pl in players.items():
                # send them a message telling them what the player said
                mud.send_message(pid,"%s shouts from somewhere far off: %s" % (players[id]["name"],params) )


        # # 'whisper' command
        elif command in ("whisper", "w"):
            #verify that there is a player to send and there is a message
            matchobj = re.match('([^\s]+) (.*)', params)
            # if there is a match go ahead and proceed with the command, else print out usage to the player
            if matchobj:
                #split the params to get the target player and the message sent
                [target, message] = params.split(' ', 1 );
                found = False
                # go through every player in the game
                for pid,pl in players.items():
                    # if the target is logged in
                    if players[pid]["name"] == target:
                        found = True
                        # send them a message telling them what the player said
                        mud.send_message(pid, "%s whispers: %s" % (target, message))
                        #send ack to player sending message
                        mud.send_message(id, "You whisper '%s' to %s" % (message, target))
                if found is False:
                    mud.send_message(id, "%s not found" % (target))
            else:
                mud.send_message(id, "Usage: whisper <player> <message>")

        # 'look' command
        elif command in ("look", "l"):

            # store the player's current room
            rm = rooms[players[id]["room"]]

            # send the player back the description of their current room
            mud.send_message(id, rm["description"])

            playershere = []
            # go through every player in the game
            for pid,pl in players.items():
                # if they're in the same room as the player
                if players[pid]["room"] == players[id]["room"]:
                    # add their name to the list
                    playershere.append(players[pid]["name"])

            # send player a message containing the list of players in the room
            mud.send_message(id, "Players here: %s" % ", ".join(playershere))

            # send player a message containing the list of exits from this room
            mud.send_message(id, "Exits are: %s" % ", ".join(rm["exits"]))

        # 'go' command
        elif command in ("go", "g"):

            # store the exit name
            ex = params.lower()

            # store the player's current room
            rm = rooms[players[id]["room"]]

            # if the specified exit is found in the room's exits list
            if ex in rm["exits"]:

                # go through all the players in the game
                for pid,pl in players.items():
                    # if player is in the same room and isn't the player sending the command
                    if players[pid]["room"] == players[id]["room"] and pid!=id:
                        # send them a message telling them that the player left the room
                        mud.send_message(pid,"%s left via exit '%s'" % (players[id]["name"],ex))

                # update the player's current room to the one the exit leads to
                players[id]["room"] = rm["exits"][ex]
                rm = rooms[players[id]["room"]]

                # go through all the players in the game
                for pid,pl in players.items():
                    # if player is in the same (new) room and isn't the player sending the command
                    if players[pid]["room"] == players[id]["room"] and pid!=id:
                        # send them a message telling them that the player entered the room
                        mud.send_message(pid,"%s arrived via exit '%s'" % (players[id]["name"],ex))

                # send the player a message telling them where they are now
                mud.send_message(id,"You arrive at '%s'" % players[id]["room"])

            # the specified exit wasn't found in the current room
            else:
                # send back an 'unknown exit' message
                mud.send_message(id, "Unknown exit '%s'" % ex)

        # some other, unrecognised command
        else:
            # send back an 'unknown command' message
            mud.send_message(id, "Unknown command '%s'" % command)

    # a hack to "fix" the 100% CPU issue        
    time.sleep(0.05)
