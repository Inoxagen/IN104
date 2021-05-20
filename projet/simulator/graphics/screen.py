import pygame as pg

from ..utils.pygame_utils import draw_text
from ..utils.vector import Vector, Vector2
#from ..utils.vector import Vector2, Vector
from .camera import Camera


class Screen:
    def __init__(self, screen_size, bg_color=(0, 0, 0), caption=None):
        self.screen_size = screen_size
        self._bg_color = bg_color

        self.camera = Camera(screen_size)

        # this is incremented at each frame
        self.frame = 0

        # this will store the last recorded mouse position
        self.mouse_position = Vector2(0, 0)

        # this will store which buttons have been pressed in the current frame
        # [LeftMouse, MiddleMouse, RightMouse, ScrollWheelUp, ScrollWheelDown,Left_Key,Right_Key,Up_Key,Down_Key,BarreEspace,Touche_O,Touche_C,Touche_X,Touche_V,Touche_TAB, Chiffre, Touche_Entrer]
        self._buttons = [False,False,False,False,False,False,False,False,False,False,False,True,False,True,False,-1,False]

        # this will be true when the user presses the exit button of the window
        self.should_quit = False

        # this is used to limit the
        # number of frames computed evey second
        self.clock = pg.time.Clock()

        pg.init()
        self._screen = pg.display.set_mode(
            (self.screen_size.get_x(), self.screen_size.get_y()))
        self.taille_police=14
        self._font = pg.font.SysFont('Arial', self.taille_police)

        if caption is not None:
            pg.display.set_caption(caption)

    def get_events(self):
        self.mouse_position = Vector2(*pg.mouse.get_pos())
        self._buttons[0]=False # Clic gauche   )
        self._buttons[3]=False # Molette haut   ) -> On écrase par False ou -1
        self._buttons[4]=False # Molette bas    )    a chaque tour
        self._buttons[12]=False # Touche x      )
        self._buttons[14]=False # Touche Tab    )    Pas besoin de memoire
        self._buttons[15]=-1    # Les chiffres  )    pour ces touches.
        self._buttons[16]=False #Touche Entrer  )

        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                self.should_quit = True
            elif event.type == pg.MOUSEBUTTONDOWN: #On clique avec la souris
                if event.button <= 5:
                    self._buttons[event.button - 1] = True
            elif event.type == pg.MOUSEBUTTONUP : #On retire le doigt de la souris
                if event.button <= 3:
                    self._buttons[event.button - 1] = False
            elif event.type == pg.KEYDOWN: #On se déplace avec ZQSD ou les fleches
                if event.key == pg.K_z or event.key == pg.K_DOWN:
                    self._buttons[7]=True
                if event.key == pg.K_q or event.key == pg.K_RIGHT:
                    self._buttons[5]=True
                if event.key == pg.K_s or event.key == pg.K_UP:
                    self._buttons[8]=True
                if event.key == pg.K_d or event.key == pg.K_LEFT:
                    self._buttons[6]=True
                if event.key == pg.K_SPACE:
                    self._buttons[9]= not self._buttons[9]
                if event.key == pg.K_o:
                    self._buttons[10]= not self._buttons[10]
                if event.key == pg.K_c:
                    self._buttons[11]= not self._buttons[11]
                if event.key == pg.K_x:
                    self._buttons[12]= True
                if event.key == pg.K_v:
                    self._buttons[13]= not self._buttons[13]
                if event.key == pg.K_TAB:
                    self._buttons[14]= True
                if pg.K_0 <= event.key and event.key <= pg.K_9 :
                    self._buttons[15]= event.key-pg.K_0
                if event.key == pg.K_RETURN:
                    self._buttons[16]= True
            elif event.type == pg.KEYUP:
                if event.key == pg.K_z or event.key == pg.K_DOWN:
                    self._buttons[7]=False
                if event.key == pg.K_q or event.key == pg.K_RIGHT:
                    self._buttons[5]=False
                if event.key == pg.K_s or event.key == pg.K_UP:
                    self._buttons[8]=False
                if event.key == pg.K_d or event.key == pg.K_LEFT:
                    self._buttons[6]=False
        self.frame += 1

    def draw(self, world,orbites=[]):
        self._screen.fill(self._bg_color)

        s = pg.Surface(self.screen_size, pg.SRCALPHA)

        self.__draw_orbite(s, orbites)
        if self.get_touche_c():
            self.__draw_world(s, world)
        self._screen.blit(s, s.get_rect())

        if sum(self._buttons[5:9])>0:
            self.__draw_viseur(s)

        x=0
        draw_text(self._screen, self._font, "Frame: %s" % self.frame,
                  Vector2(0, x), color=(0, 255, 255))
        x+=self.taille_police
        draw_text(self._screen, self._font, "Mouse position: %s" % self.mouse_position,
                  Vector2(0, x), color=(0, 255, 255))
        x+=self.taille_police
        draw_text(self._screen, self._font, "Buttons: %s" % self._buttons,
                  Vector2(0, x), color=(0, 255, 255))
        x+=self.taille_police
        draw_text(self._screen, self._font, "Should quit: %s" % self.should_quit,
                  Vector2(0, x), color=(0, 255, 255))
        x+=2*self.taille_police
        draw_text(self._screen, self._font, "Au clavier",
                  Vector2(0, x), color=(255, 255, 0))
        x+=self.taille_police
        draw_text(self._screen, self._font, "Déplacement avec [ZSQD] ou les [flèches] (logique inversée)",
                  Vector2(0, x), color=(255, 255, 255*(sum(self._buttons[5:9])>0)))
        x+=self.taille_police
        draw_text(self._screen, self._font, "La [barre espace] met en pause la simulation",
                  Vector2(0, x), color=(255, 255, 255*self._buttons[9]))
        x+=self.taille_police
        draw_text(self._screen, self._font, "[C] affiche des corps",
                  Vector2(0, x), color=(255, 255, 255*self._buttons[11]))
        x+=self.taille_police
        draw_text(self._screen, self._font, "[O] affichage des orbites",
                  Vector2(0, x), color=(255, 255, 255*self._buttons[10]))
        x+=self.taille_police
        draw_text(self._screen, self._font, "[X] supprime les orbites enregistrées",
                  Vector2(0, x), color=(255, 255, 255*self._buttons[12]))
        x+=self.taille_police
        draw_text(self._screen, self._font, "[V] imprime des commentaires",
                  Vector2(0, x), color=(255, 255, 255*self._buttons[13]))
        x+=self.taille_police
        draw_text(self._screen, self._font, "[Tab] passage en revue au corps suivant",
                  Vector2(0, x), color=(255, 255, 255*self._buttons[14]))
        x+=self.taille_police
        draw_text(self._screen, self._font, "[Chiffre] passage corps index le chiffre tapé (début à 1)",
                  Vector2(0, x), color=(255, 255, 0))
        x+=self.taille_police
        draw_text(self._screen, self._font, "[Entrer] ferme la simulation vers la suivante",
                  Vector2(0, x), color=(255, 255, 0))
        x+=2*self.taille_police
        draw_text(self._screen, self._font, "A la Souris",
                  Vector2(0, x), color=(255, 0, 255))
        x+=self.taille_police
        draw_text(self._screen, self._font, "[Clic gauche] caméra - séléction d'un astre à suivre",
                  Vector2(0, x), color=(255, 255*self._buttons[0], 255))
        x+=self.taille_police
        draw_text(self._screen, self._font, "[                    - coordonnées où poser la caméra",
                  Vector2(0, x), color=(255, 255*self._buttons[0], 255))
        x+=self.taille_police
        draw_text(self._screen, self._font, "[Clic droit] dépot de matière",
                  Vector2(0, x), color=(255, 255*self._buttons[2], 255))
        x+=self.taille_police
        draw_text(self._screen, self._font, "[Clic milieu] déplacement en poursuite du curseur",
                  Vector2(0, x), color=(255, 255*self._buttons[1], 255))
        x+=self.taille_police
        draw_text(self._screen, self._font, "[Mollette] réglage du zoom",
                  Vector2(0, x), color=(255, 255*(self._buttons[3]+self._buttons[4]>0), 255))

    def tick(self, fps):
        self.clock.tick(fps)
        return self.clock.get_time()

    def update(self):
        pg.display.update()

    def close(self):
        pg.display.quit()

    def __draw_world(self, s, world):
        for body in world.bodies():
            screen_pos = self.camera.to_screen_coords(body.position)
            pg.draw.circle(s, body.color,
                        (int(screen_pos.get_x()), int(screen_pos.get_y())),
                           int(body.draw_radius), 0)

    def __draw_orbite(self, s, orbites):
        for point in orbites:
            screen_pos = self.camera.to_screen_coords(point[0])
            pg.draw.circle(s, point[1],
                        (int(screen_pos.get_x()),int(screen_pos.get_y())),1,0)

    def __draw_viseur(self, s):
        screen_pos=self.camera.screen_size/2
        pg.draw.circle(s,(237, 123,9),(int(screen_pos.get_x()),int(screen_pos.get_y())),1,0)


    def draw_corner_text_info_corps(self,body):
        draw_text(self._screen, self._font, str(body),
                  Vector2(0, self.screen_size.get_y() - 2*self.taille_police-5), color=body.color)

    def draw_corner_text(self, s):
        draw_text(self._screen, self._font, s,
                  Vector2(0, self.screen_size.get_y() - self.taille_police-5), (255, 255, 255))

    def get_left_mouse(self): return self._buttons[0]
    def get_middle_mouse(self): return self._buttons[1]
    def get_right_mouse(self): return self._buttons[2]
    def get_wheel_up(self): return self._buttons[3]
    def get_wheel_down(self): return self._buttons[4]
    def get_left_key(self):return self.buttons[5]
    def get_right_key(self): return self.buttons[6]
    def get_up_key(self) : return self.buttons[7]
    def get_down_key(self):return self.buttons[8]
    def get_touche_espace(self):return self._buttons[9]
    def get_touche_o(self):return self._buttons[10]
    def get_touche_c(self):return self._buttons[11]
    def get_touche_x(self):return self._buttons[12]
    def get_touche_v(self):return self._buttons[13]
    def get_touche_Tab(self):return self._buttons[14]
    def get_chiffre(self):return self._buttons[15]
    def get_touche_entrer(self):return self._buttons[16]
