# My_battleship_AI_engine

A battleship game engine. Work based on the minimal engine at: https://github.com/benpastel/battleship_engine

Requirements:
  - python 3.7
  - numpy
  - a terminal with unicode support

```
  $python game.py
```

The game should look something like:
```
   | YOUR BOARD                   | ENEMY BOARD
---+------------------------------+------------------------------+
   | a  b  c  d  e  f  g  h  i  j | a  b  c  d  e  f  g  h  i  j |
---+------------------------------+------------------------------+
 0 |💥 💦  .  . 💦 💦 💦 💦 💦 💦 |💦  . 💦  . 💦  . 💦  . 💦 💦 |
 1 |💥  . 💦 💦 💥 💥 💥 💥 💥 💦 | . 💦  . 💦 💦 💦  . 💦  . 💥 |
 2 |🚢 💦 💥 💥 💥 💦 💦 💦 💦  . | .  . 💦  . 💦  . 💦  . 💦 💥 |
 3 | .  . 💦 💦 💦 💦  .  . 💦  . | . 💦  . 💦  . 💦  . 💦  . 💥 |
 4 |💦  .  .  . 💦  .  .  .  . 💦 |💦  . 💦  . 💦  . 💦  .  . 💦 |
 5 | . 💦  . 💦 💦 💦  .  . 💦 💥 | .  . 💦  . 💦 💦  .  . 💦 💦 |
 6 | .  . 💦 💦  . 💦 💦  . 💦 💥 |💥 💥 💥 💦  .  . 💦 💦  . 💥 |
 7 | . 💦 💥 💥 💦  .  .  . 💦 💥 | .  . 💦 💦 💥 💥 💥 💥 💦 💥 |
 8 | .  . 💦 💦  .  . 💦  . 💦 💥 | . 💥 💥 💥 💥 💥 💦  .  . 💦 |
 9 |💦  .  .  .  .  .  .  .  . 💦 | .  . 💦  . 💦  . 💦  .  . 💦 |
---+------------------------------+------------------------------+

A battleship of Player 2 is sunk!
A destroyer of Player 2 is sunk!
A cruiser of Player 2 is sunk!
A carrier of Player 2 is sunk!
A submarine of Player 2 is sunk!

Player 1 wins! Total moves: 58.
```
