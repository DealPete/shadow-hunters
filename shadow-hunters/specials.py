# specials.py

# Neutrals


def allie(gc, player, turn_pos):
    # ANY TIME
    if turn_pos == 'now':
        if not player.modifiers['special_used']:

            # Tell
            gc.tell_h("{} ({}) used their special ability: {}", [
                      player.user_id, player.character.name,
                      player.character.special_desc])

            # Full heal
            player.setDamage(0, player)

            # Update modifiers
            player.modifiers['special_used'] = True


def bob(gc, player, turn_pos):
    if not player.modifiers['special_used']:
        if 4 <= len(gc.players) <= 6:
            player.modifiers['steal_for_damage'] = True
        else:
            # Update modifiers
            player.modifiers['steal_all_on_kill'] = True


def catherine(gc, player, turn_pos):
    # START OF TURN
    if turn_pos == 'start' and (not player.modifiers['special_used']):

        # Tell
        gc.tell_h("{} ({}) used their special ability: {}", [
                  player.user_id, player.character.name,
                  player.character.special_desc])

        # Catherine is *required* to heal at the beginning of the turn
        player.moveDamage(1, player)

# Hunters


def george(gc, player, turn_pos):
    # START OF TURN
    if turn_pos == 'start':
        if not player.modifiers['special_used']:
            player.modifiers['special_used'] = True

            # Tell
            gc.tell_h("{} ({}) used their special ability: {}", [
                      player.user_id, player.character.name,
                      player.character.special_desc])

            # Present player with list of attack options
            target_Player = player.choosePlayer()

            # Roll and give damage to target
            roll_result = player.rollDice('4')
            target_Player.moveDamage(-1 * roll_result, player)
            gc.tell_h("{}'s Hammer gave {} {} damage!", [
                      player.user_id, target_Player.user_id, roll_result])


def fuka(gc, player, turn_pos):
    # START OF TURN
    if turn_pos == 'start':
        if not player.modifiers['special_used']:
            player.modifiers['special_used'] = True

            # Tell
            gc.tell_h("{} ({}) used their special ability: {}", [
                      player.user_id, player.character.name,
                      player.character.special_desc])

            # Enter set damage to 7 sequence
            # Select a player to use special on (includes user)
            player.gc.ask_h(
                'confirm', {'options': ["Use special ability"]},
                player.user_id)
            data = {'options': [
                t.user_id for t in gc.getLivePlayers()]}
            target = player.gc.ask_h(
                'select', data, player.user_id)['value']

            # Set selected player to 7 damage
            target_Player = [
                p for p in gc.getLivePlayers() if p.user_id == target][0]
            target_Player.setDamage(7, player)
            gc.tell_h("{} gave a killing cure to {}!", [
                      player.user_id, target_Player.user_id])


def franklin(gc, player, turn_pos):

    if turn_pos == 'start':
        if not player.modifiers['special_used']:
            player.modifiers['special_used'] = True

            # Tell
            gc.tell_h("{} ({}) used their special ability: {}", [
                      player.user_id, player.character.name,
                      player.character.special_desc])

            # Present player with list of attack options
            target_Player = player.choosePlayer()

            # Roll and give damage to target
            roll_result = player.rollDice('6')
            target_Player.moveDamage(-1 * roll_result, player)
            gc.tell_h("{}'s Lightning gave {} {} damage!", [
                      player.user_id, target_Player.user_id, roll_result])


def ellen(gc, player, turn_pos):
    # START OF TURN
    if turn_pos == 'start':
        if not player.modifiers['special_used']:
            player.modifiers['special_used'] = True

            # Tell
            gc.tell_h("{} ({}) used their special ability: {}", [
                      player.user_id, player.character.name,
                      player.character.special_desc])

            # Choose a player to cancel their special
            target_Player = player.choosePlayer()

            # Cancel special
            target_Player.resetModifiers()
            target_Player.modifiers['special_used'] = True
            target_Player.special = lambda gc, player, turn_pos: gc.tell_h(
                "Your special ability was voided by {}.", [player.user_id],
                player.socket_id)
            msg = "{} voided {}'s special ability for the rest of the game!"
            gc.tell_h(msg, [player.user_id, target_Player.user_id])

# Shadows


def valkyrie(gc, player, turn_pos):
    if not player.modifiers['special_used']:
        player.modifiers['attack_dice_type'] = "4"
        player.modifiers['special_active'] = True


def vampire(gc, player, turn_pos):
    if not player.modifiers['special_used']:
        player.modifiers['damage_dealt_fn'] = lambda player: player.moveDamage(2, player)
        player.modifiers['special_active'] = True


def werewolf(gc, player, turn_pos):
    if not player.modifiers['special_used']:
        player.modifiers['counterattack'] = True
        player.modifiers['special_active'] = True


def ultra_soul(gc, player, turn_pos):
    # START OF TURN
    if turn_pos == 'start' and (not player.modifiers['special_used']):
        # No need to bother every turn if there's nobody at UG
        targets = gc.getPlayersAt("Underworld Gate")
        targets = [t for t in targets if t != player]
        if len(targets) > 0:
            # Present player with list of attack options
            gc.tell_h("{} ({}) used their special ability: {}", [
                      player.user_id, player.character.name,
                      player.character.special_desc])
            gc.tell_h("{} is choosing a target...", [player.user_id])
            opts = [p.user_id for p in targets if p != player]
            opts.append('Decline')
            data = {'options': opts}
            target = player.gc.ask_h(
                'select', data, player.user_id)['value']
            if target != 'Decline':
                target_Player = [
                    p for p in gc.getLivePlayers() if p.user_id == target][0]
                target_Player.moveDamage(-3, player)
                gc.tell_h("{}'s Murder Ray gave {} {} damage!",
                          [player.user_id, target, 3])
            else:
                gc.tell_h(
                    "{} declined to use their Murder Ray.", [player.user_id])

# previously unimplemented character specials start here

def agnes(gc, player, turn_pos):
    # START OF TURN
    if turn_pos == 'start' and not player.modifiers['special_used']:
        gc.ask_h('confirm', {'options': ["Switch your pick to the left"]},
                 player.user_id)
        player.modifiers['agnes_picked_left'] = True
        gc.tell_h("{} ({}) used their special ability: {}", [
                  player.user_id, player.character.name,
                  player.character.special_desc])
        player.modifiers['special_used'] = True


def bryan(gc, player, turn_pos):
    # passive ability, must reveal if he kills a small character
    if turn_pos == 'death' and (not player.modifiers['special_used']):
        if gc.last_killer is player and gc.last_killed.character.max_damage < 13:

            gc.tell_h("{} ({}) triggered their special ability: {}", [
                      player.user_id, player.character.name,
                      player.character.special_desc])

            player.reveal()
            gc.update_h()
            player.modifiers['special_used'] = True


def charles(gc, player, turn_pos):
    # not once per game, trigger availability
    if not player.modifiers['special_used'] and player.state == 1:
        player.modifiers['prompt_for_second_attack'] = True
        player.modifiers['special_used'] = True


def daniel(gc, player, turn_pos):
    if turn_pos == "death" and not player.modifiers['special_used']:
        if len(gc.getDeadPlayers()) > 0 and not (player in gc.getDeadPlayers()):
            gc.tell_h("{} ({}) triggered their special ability: {}", [
                      player.user_id, player.character.name,
                      player.character.special_desc])
            player.reveal()
            gc.update_h()
            player.modifiers['special_used'] = True


def david(gc, player, turn_pos):
    # once per game grab an item from discard
    if turn_pos == 'end' and not player.modifiers['special_used']:
        discard_equipment = gc.white_cards.listEquipmentInDiscard()
        discard_equipment += gc.black_cards.listEquipmentInDiscard()
        if len(discard_equipment) > 0:
            player.gc.tell_h("You may use {}'s special ability to grab an item.",
                             [player.character.name], player.socket_id)

            discard_equipment.append('Decline')
            data = {'options': discard_equipment}
            selection = player.gc.ask_h('select', data, player.user_id)['value']
            if selection != 'Decline':
                target = gc.white_cards.takeFromDiscard(selection)
                if target is None:
                    target = gc.black_cards.takeFromDiscard(selection)

                player.equipment.append(target)

                gc.tell_h("{} ({}) used their special ability: {}", [
                          player.user_id, player.character.name,
                          player.character.special_desc])

                gc.tell_h("{} added {} to their arsenal!",
                          [player.user_id, target.title])

                gc.update_h()

                player.modifiers['special_used'] = True
        else:
            player.gc.tell_h("No equipment in discard.", [], player.socket_id)

def emi(gc, player, turn_pos):
    # passive, can move to adjacent space
    if not player.modifiers['special_used']:
        player.modifiers['moves_adjacent'] = True

def gregor(gc, player, turn_pos):
    # end of turn, can give himself Guardian Angel
    if turn_pos == 'end' and not player.modifiers['special_used']:
        player.modifiers['guardian_angel'] = True
        gc.tell_h("{} ({}) used their special ability: {}", [
                  player.user_id, player.character.name,
                  player.character.special_desc])
        player.modifiers['special_active'] = True
        player.modifiers['special_used'] = True

def wight(gc, player, turn_pos):
    if turn_pos == 'end' and not player.modifiers['special_used']:
        # take additional turns = # dead players
        extra_turns = len(gc.getDeadPlayers())
        gc.ask_h('confirm', {'options': ["Use special for {} Extra Turns".format(extra_turns)]},
                 player.user_id)
        for i in range(extra_turns):
            gc.turn_order.insert(gc.turn_order.index(player), player)

        gc.tell_h("{} ({}) used their special ability: {}", [
                  player.user_id, player.character.name,
                  player.character.special_desc])

        player.modifiers['special_used'] = True

def unknown(gc, player, turn_pos):
    # passive ability, tells lies
    if not player.modifiers['special_used']:
        player.modifiers['tells_lies'] = True
