"""
Players Class

This will hold all the logged in player information and player specific functions

Examples of functions, load and save
"""
#class name lowercase as file name is lowercase
class player(object)
    #class constructor
    def __init__(self):
        #setting the base private variables for a player
        self.type = "player"
        self.name =  None
        self.room = "Tavern"
        self.level = 1
        self.gold = 2
        self.inventory = "boomerang"

    #load a player from the datastore
    def load(id)
        #unused as of now
        
    #save a player to out datastore
    def save(id)
        #unused as of now
        
    #change a players password
    def change_password(id)
        #unused as of now
        
    #get a players name based on id
    def get_name(id)
    
    #get all of a players attributes based on id. returns an assoc array
    def get_attributes(id)
    
    #set a players attribute based on the attribute (unsure if this can be done in python probably not)
    def set_attribute(id, attribute, value)
    
"""
if set attribute will not work, and im not even sure we would want to do it. there will be getters and setters for all values that
need to be accessed outside of the class, there are a lot of things i believe wouldnt need to be
"""