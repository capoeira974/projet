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
import socket
import select

#Connexion serveur
if len(sys.argv)==1:

    print("Connecter en tant que server")
    main_connexion=socket.socket(socket.AF_INET,socket.SOCK_STREAM,0) # SOCK_STREAM pour le protocole TCP
    main_connexion.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    main_connexion.bind(('',7777)) 
    main_connexion.listen(1)
    player_connect=[]
    sockselect,x,y=select.select(player_connect+[main_connexion],[],[])
    for i in sockselect:
        if i == main_connexion:
            new_player,ip_port_player =main_connexion.accept()
            player_connect.append(new_player)
            print("un joueur qui s est connecte")

#connexion client
elif len(sys.argv)==2: # argv[0]=projet.py arv[1]= nom 
    print("Connecter en tant que client")
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM,0) # SOCK_STREAM pour le protocole TCP
    s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    s.connect((sys.argv[1],7777))



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

if len(sys.argv)==1:
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

    #Share ball data between server/ client
    if len(sys.argv) == 1:
        data= str(ball_coords.x)+","+str(ball_coords.y)
        #print(data)
        new_player.send(data)
        resume=1
        while resume:
            accuse=new_player.recv(100)
            if accuse==data:
                resume=0

    if len(sys.argv) == 2:       
        data = s.recv(100)
        if data !="":
            #print(data)
            x,y=data.split(",")
            #print(type(x)) 
            x=int(x)
            y=int(y)
            ball_coords.x=x
            ball_coords.y=y
            s.send(data)

        


    # voir la position de la balle -- print(all_coords)
    # Rebondir la balle sur le mur
    if ball_coords.left < 0 or ball_coords.right >= width:
        ball_speed[0] = -ball_speed[0]
    if ball_coords.top < 0 or ball_coords.bottom >= height:
        ball_speed[1] = -ball_speed[1]

    # Move racket
    racket_coords = racket_coords.move(racket_speed)


    # Position de la raquette : server
    if len(sys.argv)==1:
        if racket_coords.left < 0:
            racket_coords.left = 0
        elif racket_coords.right >= width:
            racket_coords.right = width-1
        if racket_coords.top < 0:
            racket_coords.top = 0
        elif racket_coords.bottom >= height:
            racket_coords.bottom = height-1
        # Position de la racket en fonction de la balle ?
        if ball_coords.left <= 0:
            if ball_coords.bottom <= racket_coords.top or ball_coords.top >= racket_coords.bottom:
                print("lost!")
                throw()
    # Posiition de la raquette  : client
    elif len(sys.argv)==2:
        if racket_coords.right < width:
            racket_coords.right = width
        elif racket_coords.left >= width:
            racket_coords.left = width+1
        if racket_coords.top < 0:
            racket_coords.top = 0
        elif racket_coords.bottom >= height:
            racket_coords.bottom = height-1
        # Position de la racket en fonction de la balle ?
        if ball_coords.right >= width:
            if ball_coords.bottom <= racket_coords.top or ball_coords.top >= racket_coords.bottom:
                print("lost!")
                throw()
    
    


    if len(sys.argv)==1:
        # Afficher l'ensemble
        screen.fill(clay)
        screen.blit(ball, ball_coords)
        screen.blit(racket, racket_coords)
        pygame.display.flip()
        # Attendre 10ms, Depuis il n'y a pas besoin plus que  100Hz rpour raffraichir :)
        pygame.time.delay(10)
    
    elif len(sys.argv)==2:
        # Afficher l'ensemble
        screen.fill(clay)
        #screen.blit(ball,(x,y))
        screen.blit(ball,ball_coords)
        screen.blit(racket, racket_coords)
        pygame.display.flip()
       
        pygame.time.delay(10)