# Sudoku

A sudoku Game created using python.
It uses a **internet connection** as it depends on an API to get random boards. 
The user can play 3 different levels against time. And if the user wishes to see the solution they can see the solution as well.
The game is built fully using pygame.
For solving the sudoku board backtracking algorithm for solving the board is used.

HOT keys :-
  KEYS | FUNCTION
  -----|----------
  **Q** | quit program
  **SPACE** | confirm the selected operation
  **ESC** | reject the selected operation
  **1 to 9** | To put the number in the selected cell of sudoku board


## Functionalities

* __The User can click in generate to generate random Sudoku puzzle__

![Generate](gifs/generate.gif)

<br />
<br />


* __The User can change the difficulty level__
  * E - Easy
  * M - Medium
  * H - Hard

![Level Change](gifs/level.gif)

<br />
<br />

* __The game can be paused__

![Pause Game](gifs/pause.gif)

<br />
<br />

* __A single cell can be cleared__ 

![Clear A cell](gifs/remove.gif)

<br />
<br />

* __All the cells can be cleared__

![Clear all cells](gifs/reset.gif)

<br />
<br />

* __If an unfilled board is checked it shows "All cells are not Filled"__

![Unfilled Check](gifs/check.gif)

<br />
<br />

* __If all the cells are filled and the puzzle is not solver it hightlights the error in red color__

![Check with Errors](gifs/check1.gif)

<br />
<br />

* __If the puzzle is solved it shows the puzzle was solved__

![Puzzle Solver](gifs/check3.gif)
