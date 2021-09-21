# Pysweeper!
#### Video Demo:  <URL https://www.youtube.com/watch?v=lVo8Z0_m7XU>
#### Description:
Pysweeper recreates the game 'minesweeper' in Python using PyGame.
The goal of the game is to identify all 'mines' as quickly as possible and left click every square that is not a mine.
#### Controls
left click - select menu options, and click squares
right click - place 'flag' on square. A flag on a square indicates the player has identified a bomb on the square, clicks will not be allowed on this square as long as the flag remains.
Left and Right click at the same time - if a square has the correct amount of adjacent flags, all other adjacent squares will be clicked.
#### How To Play
To start Player's can choose from 3 different difficulties.
Once, a difficulty is selected click any square to start. Note the first square clicked will never be a mine.
squares will indicate the number of adjacent mines.
If a player deduces that a square must be a mine, right click it to place a flag on the square.
#### How to win
Successfully left click all squares without clicking a mine.
#### how to lose
If a square with a mine is left clicked, the mine squares will turn red and the player will be taken to a defeat screen.
