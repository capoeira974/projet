#!/usr/bin/python

# Copyright (c) 2017 Samuel Thibault <samuel.thibault@ens-lyon.org>
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
# 
# THIS SOFTWARE IS PROVIDED BY Samuel Thibault ``AS IS'' AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE REGENTS OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
# OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
# OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGE.

import sys
import pygame

# Screen setup

width = 800
height = 600

clay = (0xFF, 0x40, 0)

ball_speed = [ -2, -2 ]
racket_speed = [ 0, 0 ]

# Pygame initialization
pygame.init()
screen = pygame.display.set_mode( (width, height) )

# Load resources
ball = pygame.image.load("image/ball.png")
ball_coords = ball.get_rect()

racket = pygame.image.load("image/racket.png")
racket_coords = racket.get_rect()

# Throw ball from center
def throw():
    ball_coords.left = 2*width/3
    ball_coords.top = height/2

throw()

while True:
    for e in pygame.event.get():
        # Check for exit
        if e.type == pygame.QUIT:
            sys.exit()

        # Check for racket movements
        elif e.type == pygame.KEYDOWN:
            if e.key == pygame.K_UP:
                racket_speed[1] = -4
                pass
            elif e.key == pygame.K_DOWN:
                racket_speed[1] = 4
                pass

        elif e.type == pygame.KEYUP:
            if e.key == pygame.K_UP:
                racket_speed[1] = 0
                pass
            elif e.key == pygame.K_DOWN:
                racket_speed[1] = 0
                pass

        #else:
        #    print(e)

    # Move ball
    ball_coords = ball_coords.move(ball_speed)
    # voir la position de la balle -- print(all_coords)
    # Bounce ball on walls
    if ball_coords.left < 0 or ball_coords.right >= width:
        ball_speed[0] = -ball_speed[0]
    if ball_coords.top < 0 or ball_coords.bottom >= height:
        ball_speed[1] = -ball_speed[1]

    # Move racket
    racket_coords = racket_coords.move(racket_speed)
    # Clip racket on court
    if racket_coords.left < 0:
        racket_coords.left = 0
    elif racket_coords.right >= width:
        racket_coords.right = width-1
    if racket_coords.top < 0:
        racket_coords.top = 0
    elif racket_coords.bottom >= height:
        racket_coords.bottom = height-1

    # Racket reached racket position?
    if ball_coords.left <= 0:
        if ball_coords.bottom <= racket_coords.top or ball_coords.top >= racket_coords.bottom:
            print("lost!")
            throw()

    # Display everything
    screen.fill(clay)
    screen.blit(ball, ball_coords)
    screen.blit(racket, racket_coords)
    pygame.display.flip()

    # sleep 10ms, since there is no need for more than 100Hz refresh :)
    pygame.time.delay(10)