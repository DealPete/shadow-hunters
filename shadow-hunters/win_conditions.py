# win_conditions.py


def shadow(gc, player):

    # Shadows win if all hunters are dead or 3 neutrals are dead
    no_living_hunters = (
        len([p for p in gc.getLivePlayers() if p.character.alleg == 2]) == 0)
    neutrals_dead_3 = (
        len([p for p in gc.getDeadPlayers() if p.character.alleg == 1]) >= 3)
    return no_living_hunters or neutrals_dead_3


def hunter(gc, player):

    # Hunters win if all shadows are dead
    no_living_shadows = (
        len([p for p in gc.getLivePlayers() if p.character.alleg == 0]) == 0)
    return no_living_shadows


def allie(gc, player):

    # Allie wins if she is still alive when the game ends
    return (player in gc.getLivePlayers()) and gc.game_over


def bob(gc, player):

    # Bob wins if he has 5+ equipment cards
    return len(player.equipment) >= 5


def catherine(gc, player):

    # Catherine wins if she is the first to die or one of the last 2 remaining
    first_to_die = (player in gc.getDeadPlayers()) and (
        len(gc.getDeadPlayers()) == 1)
    last_two = (player in gc.getLivePlayers()) and (
        len(gc.getLivePlayers()) <= 2)
    return first_to_die or last_two

# previously unimplemented wincons start here

def agnes(gc, player):

    # Agnes wins if the player to her right wins.
    # or if she has used her special ability,
    # the player to her left.
    neighbours = gc.getAdjacentPlayers(player)
    if neighbours is not None:
        rightWinner = neighbours[1].win_cond and not player.modifiers['agnes_picked_left']
        leftWinner = neighbours[0].win_cond and player.modifiers['agnes_picked_left']
        return rightWinner or leftWinner
    else:
        return False


def bryan(gc, player):

    # Bryan wins if he kills a character with 13 or more HP.
    # or if he is at the Erstwhile Altar when the game ends.

    kill_big_guy = gc.lastKiller is player and gc.lastKilled.max_damage >= 13
    altar_at_end = player in gc.getPlayersAt("Erstwhile Altar") and gc.game_over

    return kill_big_guy or altar_at_end


def charles(gc, player):

    # Charles wins if he kills a character and three or more
    # characters are already dead.
    three_dead = len(gc.getDeadPlayers()) >= 3
    just_killed = gc.lastKiller is player
    return three_dead and just_killed

def daniel(gc, player):

    # Daniel wins if he is first to die or all the
    # Shadows are dead.

    first_to_die = (player in gc.getDeadPlayers()) and (
        len(gc.getDeadPlayers()) == 1)
    no_living_shadows = (
        len([p for p in gc.getLivePlayers() if p.character.alleg == 0]) == 0)
    return first_to_die or no_living_shadows


def david(gc, player):

    # David wins if he has three of four holy items.
    has_robe = player.hasEquipment("Holy Robe")
    has_rosary = player.hasEquipment("Silver Rosary")
    has_talisman = player.hasEquipment("Talisman")
    has_spear = player.hasEquipment("Spear of Longinus")
    return [has_robe, has_rosary, has_talisman, has_spear].count(True) >= 3
