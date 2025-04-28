# Randomized Ball-dropping Game

This is a client-server arcade-style game developed as a final project for CS 35201. 
Players control a bucket that must catch balls dropping from random points in the sky. 
The game demonstrates basic real-time networking between a client and server using Python and Pygame.

## Team Members

- Brandon Angell  
- Kent Ogasawara

## Game Description

This project uses a client-server architecture:

- **Server Side**
  - Displays the game window and visuals
  - Manages game state (ball positions, bucket location, scoring)

- **Client Side**
  - Handles user input (arrow keys)
  - Sends input data to the server
  - Receives updated game state from the server

## Controls

- WASD – Move the bucket left, right, up and, down

## Requirements

- Python 3.12.3
- Pygame library
- Network connectivity between client and server


