# Z Shooter
## Description and Motivation
This project will be a simple Pygame program about surviving a zombie outbreak.
It will include a wave system, a high score system, zombies, and a player character to take them on.
It will have a top-down perspective, with simple but colorful graphics.
The concept of a Call of Duty-esque zombie shooter seemed like something we would both enjoy working on.

## Prior Art
As mentioned above, this project is heavily inspired by the Call of Duty series staple Zombies mode. However, this game will have an interesting top-down perspective,
with the addition of unique weapons and the mentioned high score board. Of course, there are similar flash games on the internet of the same concept: top down zombie shooter.
This game will be unique in having various zombie types, similar to Left 4 Dead 2.

## Core User Workflows
- The player will be focused on fighting zombies and buying new equipment and ammunition. 
- If the player is hit by a zombie, they take damage. If their hit points gets to or below zero, they die, and the main game loop ends.
- After they die, they are prompted to enter their name, with the following stored into a table: how long they survived and how many kills they got.
- Once they enter in their name, they can view other scores on the board.

## Tuesday-Thursday Daily Goals
### *Tuesday*
By the end of Tuesday, we plan to have the player movement and zombies added. Matthew will be focused on that. Andy will be working the spawn system, the balancing, and
the store.
### *Wednesday*
By the end of Wednesday, we hope to have the zombie AI finished, and the main loop complete with the high score system. Matthew will be focused on that AI, while Andy will
be working on the high score system.
### *Thursday*
Thursday will be about finalizing the game, and adding any additional content that seems appropriate, with the possiblity of more than one map, and adding zombie variants.
This day will also include fixing as many bugs as we can. Matthew will focus on this general debug and adding a new map, while Andy will focus on adding new zombies.

## How Will You Utilize The Content Covered This Unit
Classes are at the core of Pygame, so they will be used heavily for sprite work. This includes the player object, the zombies, the walls, the bullets, and anything else
that will be rendered onscreen.
We plan to use a database to store the scores of players who enter in their information. This information will include their name, how long they survived, and how many kills
they got. Each row on the table will be an entry to the score board.
