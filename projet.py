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

serveur=1
client=2
point = 0
point_rival=0
#Connexion serveur
if len(sys.argv)==serveur:

    print("Connecter en tant que server")
    main_connexion=socket.socket(socket.AF_INET,socket.SOCK_STREAM,0) # SOCK_STREAM pour le protocole TCP
    main_connexion.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    main_connexion.bind(('',7777)) 
    main_connexion.listen(1)
    player_connect=[]
    sockselect,x,y=select.select(player_connect+[main_connexion],[],[])
    for i in sockselect:
        if i == main_connexion:
            sock,ip_port_player =main_connexion.accept()
            player_connect.append(sock)
            print("un joueur qui s est connecte")

#connexion client
elif len(sys.argv)==client: # argv[0]=projet.py arv[1]= nom 
    print("Connecter en tant que client")
    sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM,0) # SOCK_STREAM pour le protocole TCP
    sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    sock.connect((sys.argv[1],7777))

# Screen setup

width = 800
height = 600

racket_rival_x=width-1
racket_rival_y=0

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
def throw(facteur):
    ball_coords.left = facteur*width/3
    ball_coords.top = height/2

def score(facteur,point):
    font=pygame.font.SysFont("Arial",24,bold=True)
    text=font.render(str(point),1,(0,0,255))
    screen.blit(text,(facteur*width/3,50))

def gestion(serveurbis,clientbis):
    if len(sys.argv) == serveurbis:
        data= str(ball_coords.x)+","+str(ball_coords.y)+","+str(racket_coords.x)+","+str(racket_coords.y)
        sock.send(data)
        resume=1
        while resume:
            accuse=sock.recv(100)
            if accuse==data:
                #print("ACK")
                resume=0

    if len(sys.argv) == clientbis:       
        data = sock.recv(100)
        
        if data !="":
            if data =="lost":
                print("WIN")
                global point
                point = point + 1
                pointdata=str(point)
                sock.send(pointdata)
                
            else:
                global racket_rival_x,racket_rival_y
                x,y,a,b=data.split(",")
                racket_rival_x=int(a)
                racket_rival_y=int(b)
                ball_coords.x=int(x)
                ball_coords.y=int(y)
                sock.send(data)
                
        else:
            print("no data")

if len(sys.argv)==serveur:
    throw(serveur)

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
    #print(ball_coords.x)

    if ball_coords.x < width/2:
        #print("serveur qui gere...")
        gestion(1,2)
        

    elif ball_coords.x >= width/2:
        #print("client qui gere...")
        gestion(2,1)


    # voir la position de la balle -- print(all_coords)
    # Rebondir la balle sur le mur
    if ball_coords.left < 0 or ball_coords.right >= width:
        ball_speed[0] = -ball_speed[0]
    if ball_coords.top < 0 or ball_coords.bottom >= height:
        ball_speed[1] = -ball_speed[1]

    # Move racket
    racket_coords = racket_coords.move(racket_speed)
    # Position de la raquette : server
    if len(sys.argv)==serveur:
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
                sock.send("lost")
                resume =1
                while resume:
                    point_rival=sock.recv(100)
                    if point_rival!="":
                        print(point_rival)
                        point_rival=int(point_rival)
                        resume=0
                throw(serveur)

               
    # Posiition de la raquette  : client
    elif len(sys.argv)==client:
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
                sock.send("lost")
                resume =1
                while resume:
                    point_rival=sock.recv(100)
                    if point_rival!="":
                        resume=0
                        print(point_rival)
                        point_rival=int(point_rival)
                throw(client)
                

        
    if len(sys.argv)==serveur:
        # Afficher l'ensemble
        screen.fill(clay)
        screen.blit(ball, ball_coords)
        screen.blit(racket, racket_coords)
        screen.blit(racket,(racket_rival_x,racket_rival_y))
        score(serveur,point)
        score(client,point_rival)
        pygame.display.flip()
        # Attendre 10ms, Depuis il n'y a pas besoin plus que  100Hz rpour raffraichir :)
        pygame.time.delay(10)
    
    elif len(sys.argv)==client:
        # Afficher l'ensemble
        screen.fill(clay)
        screen.blit(ball,ball_coords)
        screen.blit(racket, racket_coords)
        screen.blit(racket,(racket_rival_x,racket_rival_y))
        score(client,point)
        score(serveur,point_rival)
        pygame.display.flip()
        pygame.time.delay(10)