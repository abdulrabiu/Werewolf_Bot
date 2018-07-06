import roles_n_rules.commands as ctory
import management.db as db
import random
from management.db import db_get, db_set
from main_classes import Mailbox
from config import game_master

def see(user_id,victim_id):
    """This function allows the user to see a given player of their choice.
    The function assumes the player is a participant and has the correct role, so make sure to have filtered this out already.  
    The function returns a Mailbox.  

    user_id -> the player who casts the spell
    victim_id -> the player who is being searched"""

    uses = int(db_get(user_id,'uses'))
    if uses < 1:
        return Mailbox().respond("I am sorry! You currently don't have the ability to see this player!",True)
    db_set(user_id,'uses',uses - 1)

    victim_emoji = db_get(victim_id,"emoji")
    victim_fakerole = db_get(victim_id,"fakerole")
    victim_role = db_get(victim_id,"role")

    user_channel = int(db_get(user_id,"channel"))
    user_role = db_get(victim_id,"role")

    # Follow this procedure if the user has been enchanted.
    if int(db_get(user_id,"echanted")) == 1 and random.random() < 0.6:
        answer = Mailbox().msg("{} - <@{}> has the role of the `Flute Player`!".format(victim_emoji,victim_id),user_channel)
        answer.log("<@{0}> has attempted to see the role of <@{1}>. However, their enchantment effect worked, showing <@{1}> as the **Flute Player!**".format(user_id,victim_id))

        # Easter egg
        if victim_role == "Flute Player":
            answer.log("I mean, <@{}> *is* a **Flute Player**, so it wouldn't really matter. But hey! They don't need to know. 😉")
        
        return answer

    answer = Mailbox().msg("{} - <@{}> has the role of the `{}`!".format(victim_emoji,victim_id,victim_fakerole),user_channel)
    
    if victim_fakerole != victim_role:
        answer.log("<@{}>, the town's **{}**, has attempted to see <@{}>, the **{}**. ".format(user_id,user_role,victim_id,victim_role))
        return answer.log_add("However, they were disguised and appeared to be the **{}**!".format(victim_fakerole))

    return answer.log("<@{}>, a **{}**, has seen the role of <@{}>, who had the role of the **{}**!".format(user_id,user_role,victim_id,victim_role))
    
def disguise(user_id,victim_id,role):
    """This fuction is taking the tanner's action of disguising people.
    The function assumes the player is a participant and has the correct role, so make sure to have filtered this out already.  
    The function returns a Mailbox.  

    user_id -> the player who casts the spell
    victim_id -> the player upon whom the spell is cast
    role -> the role the player should be disguised as"""

    uses = int(db_get(user_id,'uses'))
    if uses < 1:
        return Mailbox().respond("I am sorry! You currently don't have the ability to disguise anyone!",True)
    db_set(user_id,'uses',uses - 1)

    user_channel = int(db_get(user_id,'channel'))
    user_role = db_get(user_id,'role')
    victim_role = db_get(user_id,'role')

    db_set(victim_id,'fakerole',role)
    answer = Mailbox().msg("You have successfully disguised <@{}> as the **{}**!".format(victim_id,role),user_channel)
    
    if uses - 1 > 0:
        answer.msg("You can disguise **{}** more players!".format(uses-1),user_channel,True)
    else:
        answer.msg("That\'s it for today! You can\'t disguise any more players.",user_channel,True)
    
    return answer.log("**{}** <@{}> has disguised <@{}>, the **{}**, as the **{}**!".format(user_role,user_id,victim_id,victim_role,role))

def nightly_kill(user_id,victim_id):
    """This function adds a kill to the kill queue based on the user's role.
    This function is applicable for roles like the assassin, the lone wolf, the priest, the thing and the white werewolf.
    Evaluating whether the kill should actually be applied isn't needed, as this is evaluated at the start of the day.  
    The function assumes the player is a participant and has the correct role, so make sure to have filtered this out already.  
    The function returns a Mailbox.  
    
    user_id -> the player who will initiate the attack
    victim_id -> the player who shall be \"attacked\""""

    uses = int(db_get(user_id,'uses'))
    if uses < 1:
        return Mailbox().respond("I am sorry! You currently don't have this ability available!",True)
    db_set(user_id,'uses',uses - 1)

    user_role = db_get(user_id,'role')
    user_channel = int(db_get(user_id,'channel'))

    # Add kill to the kill queue
    db.add_kill(victim_id,user_role,user_id)

    answer = Mailbox().msg(ctory.kill_acceptance(victim_id),user_channel)
    return answer.log("The **{}** <@{}> has chosen to pay a visit to <@{}> tonight.".format(user_role,user_id,victim_id))
