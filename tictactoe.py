from minimax_visualizer import run_game

def terminal_handle():
    ans = input("Do you want to use alpha-beta prunning (y/n): ")

    if ans == 'y':
        run_game(use_pruning=True)
    else:
        run_game(use_pruning=False)


if __name__ == '__main__':
    terminal_handle()
