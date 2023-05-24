from random import randint
import pygame

def Couleur_alea(min = (50,50,50), max = (200,200,200)):
    return (randint(min[0],max[0]),randint(min[1],max[1]),randint(min[2],max[2]))

def gradientRect( window, left_colour, right_colour, target_rect ):
    """ Draw a horizontal-gradient filled rectangle covering <target_rect> """
    colour_rect = pygame.Surface( ( 2, 2 ) )                                   # tiny! 2x2 bitmap
    pygame.draw.line( colour_rect, left_colour,  ( 0,0 ), ( 0,1 ) )            # left colour line
    pygame.draw.line( colour_rect, right_colour, ( 1,0 ), ( 1,1 ) )            # right colour line
    colour_rect = pygame.transform.smoothscale( colour_rect, ( target_rect.width, target_rect.height ) )  # stretch!
    window.blit( colour_rect, target_rect )

def Fill(window, res, couleurs):
    window.fill( ( 0,0,0 ) )
    gradientRect( window, couleurs[0], couleurs[1], pygame.Rect( 0,0,res[0],res[1] ) )
    # pygame.display.flip() #deja dans la classe Interface