import pyglet
from pyglet.sprite import Sprite
import random
import time
def define_entity(game):
    class Player(Sprite):
        def __init__(self, img, x=0, y=0, walkable=True, event_callback=None):
            super().__init__(img, x, y)
            self.walkable = walkable
            self.can_move = True
            self.event_callback = event_callback
            self.flags = {}
            self.last_move = time.time()
            self.sprites = {
                'up': pyglet.resource.image('player_up.png'),
                'down': pyglet.resource.image('player_down.png'),
                'left': pyglet.resource.image('player_left.png'),
                'right': pyglet.resource.image('player_right.png'),
                'facing': pyglet.resource.image('player_down.png')
            }
            self.sprite = self.sprites['facing']
        def setup_new(self):   
            #roll 4d6 drop lowest
            stats = []
            for i in range(4):
                rolls = [random.randint(1,6) for i in range(4)]
                rolls.remove(min(rolls))
                stats.append(sum(rolls))
            self.set_flags('strength', sum(stats))

            # set other dnd stats
            self.set_flags('dex', sum(stats))
            self.set_flags('con', sum(stats))
            self.set_flags('int', sum(stats))

            # set hp based on con
            self.set_flags('hp', self.get_flag('con') * 2)

            # set xp
            self.set_flags('xp', 0)
            self.set_flags('level', 1)

            # set gold
            self.set_flags('gold', 0)

            # set inventory
            self.set_flags('inventory', [])
            self.set_flags('equiped', [])
            self.set_flags('max_inventory', 10) 

            # set spells
            self.set_flags('spells', [])
            
            # set ac
            self.set_flags('ac', 10 + self.get_flag('dex'))

            # set attack
            # 1d20 + str
            self.set_flags('attack', random.randint(1,20)+self.get_flag('strength'))

            # set damage
            # 1d6 + str
            self.set_flags('base_damage', self.get_flag('strength'))
            self.set_flags('damage_mod',1)
            self.set_flags('damage_random_dice_sides', 6)



            # movement speed, use dex
            speed = self.get_flag('dex') * 0.1
            speed = max(15, speed)
            speed = min(1, speed)
            self.set_flags('movement_speed', speed)

        def calculate_damage(self):
            return random.randint(1,self.get_flag('damage_random_dice_sides')) + self.get_flag('base_damage') * self.get_flag('damage_mod')

        def does_attack_hit(self, target):
            return random.randint(1,20) + self.get_flag('attack') >= target.get_flag('ac')

        def set_can_move(self, can_move):
            self.can_movee = can_move

        def attack(self, target):
            if self.does_attack_hit(target):
                target.set_flags('hp', target.get_flag('hp') - self.calculate_damage())
                return True
            return False

        def __setstate__(self,state):
            self.x = state['x']
            self.y = state['y']
            self.flags = state['flags']

        def __getstate__(self):
            return {
                'x':self.x,
                'y':self.y,
                'flags':self.flags
            }
        def set_flags(self, key, value):
            self.flags[key] = value

        def get_flag(self, key):
            return self.flags.get(key)

        def trigger_event(self, player):
            if self.event_callback:
                self.event_callback(player)

        def on_world_update(self, dt):
            pass
        def on_key_press(self, symbol, modifiers):
            if symbol == pyglet.window.key.SPACE:
                self.trigger_event(self)

            if self.can_move == True:
                if symbol == pyglet.window.key.UP:
                    try:
                        game.tryMoveRealitive(self,x=0,y=32)
                        self.facing = 'up'
                        self.sprite = self.sprites['up']
                    except:
                        game.sounds.play('wall')

                if symbol == pyglet.window.key.DOWN:
                    try:
                        game.tryMoveRealitive(self,x=0,y=-32)
                        self.facing = 'down'
                        self.sprite = self.sprites['down']
                    except:
                        game.sounds.play('wall')

                if symbol == pyglet.window.key.LEFT:
                    try:
                        game.tryMoveRealitive(self,x=-32,y=0)
                        self.facing = 'left'
                        self.sprite = self.sprites['left']
                    except:
                        game.sounds.play('wall')
                
                if symbol == pyglet.window.key.RIGHT:
                    try:
                        game.tryMoveRealitive(self,x=32,y=0)
                        self.facing = 'right'
                        self.sprite = self.sprites['right']
                    except:
                        game.sounds.play('wall')

                

            if symbol == pyglet.window.key.ESCAPE:
                game.toggle_pause_menu()


            