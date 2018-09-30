# rr-solver

Python solver for Ricochet Robot

This project's dreamed endgame is to create a RicochetRobotAsAService,
and link it with a mobile app (if I can find some leverage to motivate my
fellow mobile dev to do it for me) to easily find out whether the fuzzy feeling
that "there's better" is real or not.

At the moment, with pypy + python3.5, it solves the 17 goals in about 4mn30 and 6Go of RAM.

To run it:

```shell
python main.py
```

You can give a seed to the random module:

```shell
python main.py 3345
```
