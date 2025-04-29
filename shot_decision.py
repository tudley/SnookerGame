import shot_functions as sf

def evaluate_shot(settings, players, balls, choice_button, choice_button2):
    """Evaluate the outcome of the player's shot after balls have stopped moving."""

    print('Evaluating shot...')
    
    # 1. Reset player fouls
    settings.active_player.foul1 = False
    settings.active_player.foul2 = False
    settings.active_player.foul3 = False
    settings.active_player.foul4 = False

    # 2. Check immediate fouls (potting white or no contact)
    sf.check_foul1(settings)
    sf.check_foul4(settings)

    if settings.active_player.foul1 or settings.active_player.foul4:
        sf.give_advantage(settings)
        sf.swap_active_player(players, settings)
        sf.end_evaluation(settings)
        return

    # 3. If player has no team assigned yet
    if settings.active_player.team is None:
        if len(settings.balls_pocketed_in_turn) > 0:
            colours = set(ball.name for ball in settings.balls_pocketed_in_turn)

            if len(colours) == 1:
                # Only one colour potted → Auto-assign team
                sf.auto_assign_teams(settings)
                sf.end_evaluation(settings)
                return

            else:
                # Mixed colours → Let player choose team manually
                sf.assign_teams(settings, choice_button2, choice_button)
                return

        else:
            # No balls potted → Swap players
            sf.swap_active_player(players, settings)
            sf.end_evaluation(settings)
            return

    # 4. Player has a team assigned
    else:
        sf.check_if_player_has_potted_all_their_balls(settings, balls)
        foul2 = sf.check_foul2(settings)
        foul3 = sf.check_foul3(settings)

        if foul2 or foul3:
            sf.give_advantage(settings)
            sf.swap_active_player(players, settings)
            sf.end_evaluation(settings)
            return

        # 5. Special case: player is on black
        if settings.active_player.team == 'black':
            colours_potted = set(ball.name for ball in settings.balls_pocketed_in_turn)

            if 'black' in colours_potted:
                if len(colours_potted) == 1:
                    settings.active_player.win = True
                    print(f"{settings.active_player.name} has won the game!")
                else:
                    settings.active_player.gameover = True
                    print(f"{settings.active_player.name} potted black incorrectly and loses!")
                sf.end_evaluation(settings)
                return

        # 6. Normal play evaluation
        if len(settings.balls_pocketed_in_turn) > 0:
            # Potted at least one ball → Player continues
            sf.end_evaluation(settings)
            return
        else:
            # No balls potted
            if settings.active_player.advantage:
                # Player had advantage → Keep playing, use up advantage
                settings.active_player.advantage = False
                sf.end_evaluation(settings)
                return
            else:
                # No advantage → Swap players
                sf.swap_active_player(players, settings)
                sf.end_evaluation(settings)
                return