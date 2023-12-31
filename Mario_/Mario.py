import arcade
import arcade.gui
import random
import PIL

ScreenWidth = 1300
ScreenHeight = 800
ScreenTitle = "Super Python Mario"

PlayerScaling = 1.25
FlagScaling = 0.5
EnemyScaling = 1.25
TubeScaling = 0.5
ObstacleScaling = 0.2
BrickScaling = 0.025
QBlockScaling = 0.13
PowerUpScaling = 0.20

startbuttonX = ScreenWidth/2-60
startbuttonY = ScreenWidth/2
instbuttonX = ScreenWidth/2+60
instbuttonY = ScreenWidth/2

MarioMovementSpeed = 3
MarioJumpSpeed = 20
FrameUpdates = 3
GRAVITY = 0.95
RIGHT_FACING = 0
LEFT_FACING = 1

#******************************************************************************************************************************************
#******************************************************************************************************************************************
#******************************************************************************************************************************************

class StartUpView(arcade.View):
    def __init__(self, current_level = 0, mushroom = False):
        super().__init__()
        self.current_level = current_level
        self.mushroom = mushroom

    def on_show_view(self):
        arcade.set_background_color(arcade.color.WHEAT)
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        self.box = arcade.gui.UIBoxLayout(space_between=20)

        start_button = arcade.gui.UIFlatButton(text="Start Game", width=200)
        start_button.on_click = self.on_click_start_button
        self.box.add(start_button)

        instructions_button = arcade.gui.UIFlatButton(text="Instructions", width=200)
        instructions_button.on_click = self.on_click_instructions_button
        self.box.add(instructions_button)

        self.manager.add(arcade.gui.UIAnchorWidget(anchor_x="center_x",anchor_y="center_y",child=self.box))

    def on_draw(self):
        self.clear()
        arcade.draw_text("Super Python Mario", ScreenWidth / 2, ScreenHeight / 2 + 150, arcade.color.RADICAL_RED, font_size=50, anchor_x="center")
        self.manager.draw()
        arcade.draw_text("Credits:", ScreenWidth / 2, 100, arcade.color.RADICAL_RED, font_size=25, anchor_x="center")
        arcade.draw_text("Logan Camp, Mariah Kaim, and Noah Kenyon", ScreenWidth / 2, 60, arcade.color.RADICAL_RED, font_size=20, anchor_x="center")
   
    def on_click_start_button(self, event):
        StartMap = WorldMap(self.current_level, self.mushroom)
        self.window.show_view(StartMap)
    
    def on_click_instructions_button(self, event):
        instructions_view = InstructionView(self.current_level, self.mushroom)
        self.window.show_view(instructions_view)


#******************************************************************************************************************************************

class InstructionView(arcade.View):

    def __init__(self, current_level=0, mushroom = False):
        super().__init__()
        self.current_level = current_level
        self.mushroom = mushroom

    def on_show_view(self):
        arcade.set_background_color(arcade.color.WHEAT)

        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        back_button = arcade.gui.UIFlatButton(ScreenWidth/2-100, 100, text="back", width=200)
        back_button.on_click = self.on_click_back_button
        self.manager.add(back_button)

    def on_draw(self):
        self.clear()
        self.manager.draw()
        arcade.draw_text("Instructions", ScreenWidth / 2, ScreenHeight - 100, arcade.color.RADICAL_RED, font_size=40, anchor_x="center")
        arcade.draw_text("Move Right : Right Arror | D", ScreenWidth / 2, ScreenHeight - 155, arcade.color.BLACK, font_size=20, anchor_x="center")
        arcade.draw_text("Move Left : Left Arror | A", ScreenWidth / 2, ScreenHeight - 205, arcade.color.BLACK, font_size=20, anchor_x="center")
        arcade.draw_text("Jump : Up Arror | W | Space", ScreenWidth / 2, ScreenHeight - 255, arcade.color.BLACK, font_size=20, anchor_x="center")
        arcade.draw_text("________________________________________", ScreenWidth / 2, ScreenHeight - 275, arcade.color.WHITE, font_size=20, anchor_x="center")
        arcade.draw_text("Goal:", ScreenWidth / 2, ScreenHeight - 317, arcade.color.RADICAL_RED, font_size=20, anchor_x="center")
        arcade.draw_text("Reach the flag to clear a level", ScreenWidth / 2, ScreenHeight - 370, arcade.color.BLACK, font_size=20, anchor_x="center")
        arcade.draw_text("Beat Bowser to win the game", ScreenWidth / 2, ScreenHeight - 405, arcade.color.BLACK, font_size=20, anchor_x="center")

    def on_click_back_button(self, event):
        start_view = StartUpView(self.current_level, self.mushroom)
        self.window.show_view(start_view)

#******************************************************************************************************************************************

class PauseView(arcade.View):
    def __init__(self, game_view, current_level, mushroom):
        super().__init__()
        self.game_view = game_view
        self.current_level = current_level
        self.mushroom = mushroom
        self.active_view = current_level+1

    def on_show_view(self):
        arcade.set_background_color(arcade.color.WHEAT)

        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        self.box = arcade.gui.UIBoxLayout(space_between=20)

        play_button = arcade.gui.UIFlatButton(ScreenWidth/2-100, 100, text="Resume Game", width=200)
        play_button.on_click = self.on_click_play_button
        self.box.add(play_button)

        restart_button = arcade.gui.UIFlatButton(text="Restart", width=200)
        restart_button.on_click = self.on_click_restart_button
        self.box.add(restart_button)

        self.manager.add(arcade.gui.UIAnchorWidget(anchor_x="center_x",anchor_y="center_y",child=self.box))

    def on_draw(self):
        self.clear()
        self.manager.draw()
        arcade.draw_text("Paused", ScreenWidth / 2, ScreenHeight - 100, arcade.color.RADICAL_RED, font_size=40, anchor_x="center")
        
    def on_click_play_button(self, event):
        self.window.show_view(self.game_view)

    def on_click_restart_button(self, event):
        restart = GameView(self.current_level, self.mushroom, self.active_view)
        self.window.show_view(restart)

#******************************************************************************************************************************************

class LevCompView(arcade.View):
    def __init__(self, current_level, mushroom):
        super().__init__()
        if current_level == 42:
            self.current_level = 4
        self.current_level = current_level + 1
        self.mushroom = mushroom
    
    def on_show_view(self):
        arcade.set_background_color(arcade.color.WHEAT)

        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        self.box = arcade.gui.UIBoxLayout(space_between=20)

        main_menu_button = arcade.gui.UIFlatButton(ScreenWidth/2-100, 100, text="Main Menu", width=200)
        main_menu_button.on_click = self.on_click_main_menu_button
        self.box.add(main_menu_button)

        continue_button = arcade.gui.UIFlatButton(text="Continue", width=200)
        continue_button.on_click = self.on_click_continue_button
        self.box.add(continue_button)

        self.manager.add(arcade.gui.UIAnchorWidget(anchor_x="center_x",anchor_y="center_y",child=self.box))

    def on_draw(self):
        self.clear()
        self.manager.draw()
        arcade.draw_text("Level Complete!", ScreenWidth / 2, ScreenHeight - 100, arcade.color.RADICAL_RED, font_size=40, anchor_x="center")
        
    def on_click_main_menu_button(self, event):
        menu = StartUpView(self.current_level, self.mushroom)
        self.window.show_view(menu)

    def on_click_continue_button(self, event):
        WorldMap(self.current_level, self.mushroom)
        if self.current_level == 1:
            button = GameView(1, self.mushroom, active_level = 2)
            self.window.show_view(button)
        elif self.current_level == 2:
            button = GameView(2, self.mushroom, active_level = 3)
            self.window.show_view(button)
        elif self.current_level == 3:
            button = GameView(3, self.mushroom, active_level = 4)
            self.window.show_view(button)
        else:
            button = GameView(4, self.mushroom, active_level = 5)
            self.window.show_view(button)

#******************************************************************************************************************************************

class GameOverView(arcade.View):
    def __init__(self, current_level):
        super().__init__()
        self.current_level = current_level
        self.mushroom = False
    
    def on_show_view(self):
        arcade.set_background_color(arcade.color.WHEAT)

        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        self.box = arcade.gui.UIBoxLayout(space_between=20)

        main_menu_button = arcade.gui.UIFlatButton(ScreenWidth/2-100, 100, text="Main Menu", width=200)
        main_menu_button.on_click = self.on_click_main_menu_button
        self.box.add(main_menu_button)

        restart_button = arcade.gui.UIFlatButton(text="Restart", width=200)
        restart_button.on_click = self.on_click_restart_button
        self.box.add(restart_button)

        self.manager.add(arcade.gui.UIAnchorWidget(anchor_x="center_x",anchor_y="center_y",child=self.box))

    def on_draw(self):
        self.clear()
        self.manager.draw()
        arcade.draw_text("You Died...", ScreenWidth / 2, ScreenHeight - 100, arcade.color.RADICAL_RED, font_size=40, anchor_x="center")
        
    def on_click_main_menu_button(self, event):
        menu = StartUpView(self.current_level)
        self.window.show_view(menu)

    def on_click_restart_button(self, event):
        if self.current_level == 51:
            restart = BossView(self.mushroom)
            self.window.show_view(restart)
        else:
            restart = GameView(self.current_level, self.mushroom, self.current_level+1)
            self.window.show_view(restart)

#******************************************************************************************************************************************

class WinnerView(arcade.View):
    def __init__(self):
        super().__init__()
    
    def on_show_view(self):
        arcade.set_background_color(arcade.color.WHEAT)

        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        self.box = arcade.gui.UIBoxLayout(space_between=20)

        main_menu_button = arcade.gui.UIFlatButton(ScreenWidth/2-100, 100, text="Main Menu", width=200)
        main_menu_button.on_click = self.on_click_main_menu_button
        self.box.add(main_menu_button)

        continue_but = arcade.gui.UIFlatButton(text="Continue", width=200)
        continue_but.on_click = self.on_click_restart_button
        self.box.add(continue_but)

        self.manager.add(arcade.gui.UIAnchorWidget(anchor_x="center_x",anchor_y="center_y",child=self.box))

    def on_draw(self):
        self.clear()
        self.manager.draw()
        arcade.draw_text("!!You Win!!", ScreenWidth / 2, ScreenHeight - 100, arcade.color.RADICAL_RED, font_size=40, anchor_x="center")
        
    def on_click_main_menu_button(self, event):
        menu = StartUpView(6)
        self.window.show_view(menu)

    def on_click_restart_button(self, event):
        continue1 = WorldMap(6, True)
        self.window.show_view(continue1)

#******************************************************************************************************************************************

class WorldMap(arcade.View):
    def __init__(self, current_level, mushroom):
        super().__init__()
        self.current_level = current_level
        self.mushroom = mushroom

    def on_show_view(self):
        arcade.set_background_color(arcade.color.SKY_BLUE)
        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        button1 = arcade.gui.UIFlatButton(311,300,text= "1", width=25, height=25)
        button1.on_click = self.on_click_button_1
        self.manager.add(button1)

        button2 = arcade.gui.UIFlatButton(513,470,text= "2", width=25, height=25)
        button2.on_click = self.on_click_button_2
        self.manager.add(button2)

        button3 = arcade.gui.UIFlatButton(951,600,text= "3", width=25, height=25)
        button3.on_click = self.on_click_button_3
        self.manager.add(button3)

        button4 = arcade.gui.UIFlatButton(883,370,text= "4", width=25, height=25)
        button4.on_click = self.on_click_button_4
        self.manager.add(button4)

        button5 = arcade.gui.UIFlatButton(547,245,text= "5", width=25, height=25)
        button5.on_click = self.on_click_button_5
        self.manager.add(button5)

#LEVEL_SELECT *****************************************************************************************************************************

    def on_click_button_1(self, event):
        if self.current_level >= 0:
            self.active_level = 1
            button = GameView(0, self.mushroom, self.active_level)
            self.window.show_view(button)

    def on_click_button_2(self, event):
        if self.current_level >= 1:
            self.active_level = 2
            button = GameView(1, self.mushroom, self.active_level)
            self.window.show_view(button)
        
    def on_click_button_3(self, event):
        if self.current_level >= 2:
            self.active_level = 3
            button = GameView(2, self.mushroom, self.active_level)
            self.window.show_view(button)
        
    def on_click_button_4(self, event):
        if self.current_level >= 3:
            self.active_level = 4
            button = GameView(3, self.mushroom, self.active_level)
            self.window.show_view(button)
        
    def on_click_button_5(self, event):
        if self.current_level >= 4:
            self.active_level = 5
            button = GameView(4, self.mushroom, self.active_level)
            self.window.show_view(button)

#EXECUTE **********************************************************************************************************************************

    def on_draw(self):
        self.clear()
        arcade.draw_lrwh_rectangle_textured(50,50,ScreenWidth-100,ScreenHeight-100, arcade.load_texture("Images/map.png"))
        arcade.draw_text("Super Python Mario", ScreenWidth / 2, 700, arcade.color.RADICAL_RED, font_size=30, anchor_x="center")
        self.manager.draw()


#******************************************************************************************************************************************
#******************************************************************************************************************************************
#******************************************************************************************************************************************
#******************************************************************************************************************************************
#******************************************************************************************************************************************
#******************************************************************************************************************************************

#Game Class *******************************************************************************************************************************

class GameView(arcade.View):
    
    def __init__(self, current_level, mushroom, active_level, EnemySpeed = -2.5):
        super().__init__()
        self.clear()

        self.scene = None
        self.player_list = None

        self.mario_sprite = None
        self.flag_sprite = None
        self.mushPlat_sprite = None
        self.qblock_sprite = None
        self.mushroom_sprite = None
        
        self.physics_engine = None
        self.enemy_physics_engine = None
        self.powerup_physics_engine = None

        self.current_level = current_level
        self.active_level = active_level
        self.mushMove = random.choice([-3,3])
        self.EnemySpeed = EnemySpeed
        self.EnemySpeed2 = EnemySpeed
        self.switchPos = 0

        self.enemy_move = True
        self.powerup = False
        self.enColPos = True
        self.small = True
        self.colPos = True
        self.part = None
        self.mushroom = mushroom

        self.background = arcade.load_texture("Images/background.jpg")
        self.cavebackground = arcade.load_texture("Images/cave.png")
        self.background4 = arcade.load_texture("Images/waterbackground.jpeg")
        self.background42 = arcade.load_texture("Images/waterbackground.png")
        self.background5 = arcade.load_texture("Images/boss/castleoutside.png")

        if self.current_level == 0:
            self.lvl_1_setup()
        elif self.current_level == 1:
            self.lvl_2_setup()
        elif self.current_level == 2:
            self.lvl_3_setup()
        elif self.current_level == 3:
            self.lvl_41_setup()
        elif self.current_level == 42:
            self.lvl_42_setup()
        elif self.current_level == 4:
            self.lvl_5_setup()

    def on_show_view(self):
        self.background = arcade.load_texture("Images/background.jpg")
        self.cavebackground = arcade.load_texture("Images/cave.png")
        self.background4 = arcade.load_texture("Images/waterbackground.jpeg")
        self.background42 = arcade.load_texture("Images/waterbackground.png")
        self.background5 = arcade.load_texture("Images/boss/castleoutside.png")
        self.on_draw()

#MAKE LEVELS ******************************************************************************************************************************
#Level Setups *****************************************************************************************************************************

#lvl1 *************************************************************************************************************************************
    def lvl_1_setup(self):
        #Level 1: simple ground level with mushroom powerup and goomba enemy
        self.scene = arcade.Scene()
        self.player_list = arcade.SpriteList()
        self.scene.add_sprite_list("Enemies")
        self.scene.add_sprite_list("World", use_spatial_hash = True)

        self.mario_sprite = self.player_sprite = PlayerCharacter(self.mushroom)
        self.mario_sprite.center_x = 50
        self.mario_sprite.center_y = 27
        self.player_list.append(self.mario_sprite)

        self.rborder_sprite = arcade.Sprite("Images/border.png", PlayerScaling)
        self.rborder_sprite.center_x = ScreenWidth
        self.rborder_sprite.center_y = 0
        self.scene.add_sprite("World", self.rborder_sprite)
        self.lborder_sprite = arcade.Sprite("Images/border.png", PlayerScaling)
        self.lborder_sprite.center_x = -5
        self.lborder_sprite.center_y = 0
        self.scene.add_sprite("World", self.lborder_sprite)

        self.flag_sprite = arcade.Sprite("Images/flag.png", FlagScaling)
        self.flag_sprite.center_x = ScreenWidth - 50
        self.flag_sprite.center_y = 128
        self.scene.add_sprite("Flag",self.flag_sprite)

        for x in range(0, ScreenWidth+50, 50):
            ground = arcade.Sprite("Images/dblx5qhqm0l61.png", ObstacleScaling)
            ground.center_x = x
            ground.center_y = 25
            self.scene.add_sprite("World", ground)

        for x in range(600, 900, 42):
            blocks = arcade.Sprite("Images/Brick_Block.jpg", BrickScaling)
            blocks.center_x = x
            blocks.center_y = 200
            self.scene.add_sprite("World", blocks)

        self.qblock_sprite = arcade.Sprite("Images/question.jpg", QBlockScaling)
        self.qblock_sprite.center_x = 750
        self.qblock_sprite.center_y = 400
        self.scene.add_sprite("World", self.qblock_sprite)

        self.qblockTest_sprite = arcade.Sprite("Images/question.jpg", QBlockScaling)
        self.qblockTest_sprite.center_x = 750
        self.qblockTest_sprite.center_y = 399
        self.scene.add_sprite("qblockTest", self.qblockTest_sprite)

        self.goomba_sprite = arcade.Sprite("Images/mbad5.png", EnemyScaling)
        self.goomba_sprite.center_x = ScreenWidth/2
        self.goomba_sprite.center_y = 55
        self.scene.add_sprite("Enemies", self.goomba_sprite)

        self.physics_engine = arcade.PhysicsEnginePlatformer(self.mario_sprite, gravity_constant = GRAVITY, walls=self.scene["World"])
        self.enemy_physics_engine = arcade.PhysicsEnginePlatformer(self.goomba_sprite, gravity_constant = GRAVITY, walls=self.scene["World"])

#lvl2 *************************************************************************************************************************************
    def lvl_2_setup(self):
        #Simple ground level with steps up, a flying enemy and a mushroom structure to jump off of 
        self.scene = arcade.Scene()
        self.player_list = arcade.SpriteList()
        self.scene.add_sprite_list("Enemies")
        self.scene.add_sprite_list("World", use_spatial_hash = True)

        self.mario_sprite = PlayerCharacter(self.mushroom)
        self.mario_sprite.center_x = 50
        self.mario_sprite.center_y = 27
        self.player_list.append(self.mario_sprite)

        self.rborder_sprite = arcade.Sprite("Images/border.png", PlayerScaling)
        self.rborder_sprite.center_x = ScreenWidth
        self.rborder_sprite.center_y = 0
        self.scene.add_sprite("World", self.rborder_sprite)
        self.lborder_sprite = arcade.Sprite("Images/border.png", PlayerScaling)
        self.lborder_sprite.center_x = -5
        self.lborder_sprite.center_y = 0
        self.scene.add_sprite("World", self.lborder_sprite)

        self.flag_sprite = arcade.Sprite("Images/flag.png", FlagScaling)
        self.flag_sprite.center_x = ScreenWidth - 55
        self.flag_sprite.center_y = 508
        self.scene.add_sprite("Flag",self.flag_sprite)

        ground = arcade.Sprite("Images/plat1.png", 1)
        ground.center_x = 500
        ground.center_y = 200
        self.scene.add_sprite("World", ground)

        ground = arcade.Sprite("Images/plat1.png", 1)
        ground.center_x = 500
        ground.center_y = 285
        self.scene.add_sprite("World", ground)

        ground = arcade.Sprite("Images/plat1.png", 1)
        ground.center_x = 300
        ground.center_y = 100
        self.scene.add_sprite("World", ground)

        ground = arcade.Sprite("Images/plat1.png", 1)
        ground.center_x = ScreenWidth - 88
        ground.center_y = 200
        self.scene.add_sprite("World", ground)
        ground = arcade.Sprite("Images/plat1.png", 1)
        ground.center_x = ScreenWidth - 88
        ground.center_y = 375
        self.scene.add_sprite("World", ground)

        self.mushPlat_sprite = arcade.Sprite("Images/mushroomPlat.png", 1)
        self.mushPlat_sprite.center_x = ScreenWidth - 450
        self.mushPlat_sprite.center_y = 50
        self.scene.add_sprite("MushPlat",self.mushPlat_sprite)

        for x in range(0, ScreenWidth+50, 50):
            ground = arcade.Sprite("Images/dblx5qhqm0l61.png", ObstacleScaling)
            ground.center_x = x
            ground.center_y = 25
            self.scene.add_sprite("World", ground)

        self.flyingTurt_sprite = arcade.Sprite("Images/flyingturtle1.png", 0.18)
        self.flyingTurt_sprite.center_x = ScreenWidth - 450
        self.flyingTurt_sprite.center_y = 520
        self.scene.add_sprite("Enemies", self.flyingTurt_sprite)

        self.physics_engine = arcade.PhysicsEnginePlatformer(self.mario_sprite, gravity_constant = GRAVITY, walls=self.scene["World"])
        self.enemy_physics_engine = arcade.PhysicsEnginePlatformer(self.flyingTurt_sprite, gravity_constant = 0, walls=self.scene["World"])

#lvl3 *************************************************************************************************************************************
    def lvl_3_setup(self):
        #Simple Cave Level with falling thwomps and a lifted flag
        self.scene = arcade.Scene()
        self.player_list = arcade.SpriteList()
        self.scene.add_sprite_list("Enemies")
        self.scene.add_sprite_list("World", use_spatial_hash = True)

        self.mario_sprite = self.player_sprite = PlayerCharacter(self.mushroom)
        self.mario_sprite.center_x = 50
        self.mario_sprite.center_y = 27
        self.player_list.append(self.mario_sprite)

        self.rborder_sprite = arcade.Sprite("Images/border.png", PlayerScaling)
        self.rborder_sprite.center_x = ScreenWidth
        self.rborder_sprite.center_y = 0
        self.scene.add_sprite("World", self.rborder_sprite)
        self.lborder_sprite = arcade.Sprite("Images/border.png", PlayerScaling)
        self.lborder_sprite.center_x = -5
        self.lborder_sprite.center_y = 0
        self.scene.add_sprite("World", self.lborder_sprite)

        self.flag_sprite = arcade.Sprite("Images/flag.png", FlagScaling)
        self.flag_sprite.center_x = ScreenWidth - 50
        self.flag_sprite.center_y = 450
        self.scene.add_sprite("Flag",self.flag_sprite)

        for x in range(0, ScreenWidth+50, 50):
            ground = arcade.Sprite("Images/ground_cave.png", 0.05)
            ground.center_x = x
            ground.center_y = 25
            self.scene.add_sprite("World", ground)

        plat = arcade.Sprite("Images/ground_cave.png", 0.05)
        plat.center_x = 1150
        plat.center_y = 225
        self.scene.add_sprite("World", plat)

        ground = arcade.Sprite("Images/ground_cave.png", 0.25)
        ground.center_x = ScreenWidth - 10
        ground.center_y = 205
        self.scene.add_sprite("World", ground)

        y = 25
        for x in range(110, 1160, 150):
            plat = arcade.Sprite("Images/ground_cave.png", 0.05)
            plat.center_x = x
            plat.center_y = y
            self.scene.add_sprite("World", plat)
            y += 25

        self.thwomp_sprite = arcade.Sprite("Images/Thwomp.png", 0.10)
        self.thwomp_sprite.center_x = 110
        self.thwomp_sprite.center_y = ScreenHeight+25
        self.scene.add_sprite("Enemies", self.thwomp_sprite)
        self.thwomp_sprite2 = arcade.Sprite("Images/Thwomp.png", 0.10)
        self.thwomp_sprite2.center_x = 260
        self.thwomp_sprite2.center_y = ScreenHeight+25
        self.scene.add_sprite("Enemies", self.thwomp_sprite2)
        self.thwomp_sprite3 = arcade.Sprite("Images/Thwomp.png", 0.10)
        self.thwomp_sprite3.center_x = 410
        self.thwomp_sprite3.center_y = ScreenHeight+25
        self.scene.add_sprite("Enemies", self.thwomp_sprite3)
        self.thwomp_sprite4 = arcade.Sprite("Images/Thwomp.png", 0.10)
        self.thwomp_sprite4.center_x = 560
        self.thwomp_sprite4.center_y = ScreenHeight+25
        self.scene.add_sprite("Enemies", self.thwomp_sprite4)
        self.thwomp_sprite5 = arcade.Sprite("Images/Thwomp.png", 0.10)
        self.thwomp_sprite5.center_x = 710
        self.thwomp_sprite5.center_y = ScreenHeight+25
        self.scene.add_sprite("Enemies", self.thwomp_sprite5)
        self.thwomp_sprite6 = arcade.Sprite("Images/Thwomp.png", 0.10)
        self.thwomp_sprite6.center_x = 860
        self.thwomp_sprite6.center_y = ScreenHeight+25
        self.scene.add_sprite("Enemies", self.thwomp_sprite6)
        self.thwomp_sprite7 = arcade.Sprite("Images/Thwomp.png", 0.10)
        self.thwomp_sprite7.center_x = 1010
        self.thwomp_sprite7.center_y = ScreenHeight+25
        self.scene.add_sprite("Enemies", self.thwomp_sprite7)

        self.physics_engine = arcade.PhysicsEnginePlatformer(self.mario_sprite, gravity_constant = GRAVITY, walls=self.scene["World"])
        self.enemy_physics_engine = arcade.PhysicsEnginePlatformer(self.thwomp_sprite, gravity_constant = 1, walls=self.scene["World"])
        self.enemy_physics_engine2 = arcade.PhysicsEnginePlatformer(self.thwomp_sprite2, gravity_constant = 1, walls=self.scene["World"])
        self.enemy_physics_engine3 = arcade.PhysicsEnginePlatformer(self.thwomp_sprite3, gravity_constant = 1, walls=self.scene["World"])
        self.enemy_physics_engine4 = arcade.PhysicsEnginePlatformer(self.thwomp_sprite4, gravity_constant = 1, walls=self.scene["World"])
        self.enemy_physics_engine5 = arcade.PhysicsEnginePlatformer(self.thwomp_sprite5, gravity_constant = 1, walls=self.scene["World"])
        self.enemy_physics_engine6 = arcade.PhysicsEnginePlatformer(self.thwomp_sprite6, gravity_constant = 0.95, walls=self.scene["World"])
        self.enemy_physics_engine7 = arcade.PhysicsEnginePlatformer(self.thwomp_sprite7, gravity_constant = 0.9, walls=self.scene["World"])

#lvl4 p1 **********************************************************************************************************************************
    def lvl_41_setup(self):
        #Tube to a water level
        self.part = 1
        self.scene = arcade.Scene()
        self.player_list = arcade.SpriteList()
        self.scene.add_sprite_list("Enemies")
        self.scene.add_sprite_list("World", use_spatial_hash = True)

        self.mario_sprite = self.player_sprite = PlayerCharacter(self.mushroom)
        self.mario_sprite.center_x = 50
        self.mario_sprite.center_y = 27
        self.player_list.append(self.mario_sprite)

        self.rborder_sprite = arcade.Sprite("Images/border.png", PlayerScaling)
        self.rborder_sprite.center_x = ScreenWidth
        self.rborder_sprite.center_y = 0
        self.scene.add_sprite("World", self.rborder_sprite)
        self.lborder_sprite = arcade.Sprite("Images/border.png", PlayerScaling)
        self.lborder_sprite.center_x = -5
        self.lborder_sprite.center_y = 0
        self.scene.add_sprite("World", self.lborder_sprite)

        self.tube_sprite = arcade.Sprite("Images/tube.png", 0.35)
        self.tube_sprite.center_x = ScreenWidth - 100
        self.tube_sprite.center_y = 95
        self.scene.add_sprite("World",self.tube_sprite)

        for x in range(0, ScreenWidth+50, 50):
            ground = arcade.Sprite("Images/dblx5qhqm0l61.png", ObstacleScaling)
            ground.center_x = x
            ground.center_y = 25
            self.scene.add_sprite("World", ground)

        self.physics_engine = arcade.PhysicsEnginePlatformer(self.mario_sprite, gravity_constant = GRAVITY, walls=self.scene["World"])

#lvl4 p2 **********************************************************************************************************************************
    def lvl_42_setup(self):
        #Water level started from tube
        self.part = 2
        self.scene = arcade.Scene()
        self.player_list = arcade.SpriteList()
        self.scene.add_sprite_list("Enemies")
        self.scene.add_sprite_list("World", use_spatial_hash = True)

        self.mario_sprite = self.player_sprite = PlayerCharacter(self.mushroom)
        self.mario_sprite.center_x = 95
        self.mario_sprite.center_y = ScreenHeight - 25
        self.player_list.append(self.mario_sprite)

        self.tube_sprite = arcade.Sprite("Images/tubeflip.png", 0.35)
        self.tube_sprite.center_x = 100
        self.tube_sprite.center_y = ScreenHeight - 10
        self.scene.add_sprite("World",self.tube_sprite)

        for y in range(0, ScreenHeight, 100):
            self.rborder_sprite = arcade.Sprite("Images/border.png", PlayerScaling)
            self.rborder_sprite.center_x = ScreenWidth
            self.rborder_sprite.center_y = y
            self.scene.add_sprite("World", self.rborder_sprite)
            self.lborder_sprite = arcade.Sprite("Images/border.png", PlayerScaling)
            self.lborder_sprite.center_x = -5
            self.lborder_sprite.center_y = y
            self.scene.add_sprite("World", self.lborder_sprite)
        for x in range(0, ScreenWidth, 100):
            self.uborder_sprite = arcade.Sprite("Images/topborder.png", PlayerScaling)
            self.uborder_sprite.center_x = x
            self.uborder_sprite.center_y = ScreenHeight + 5
            self.scene.add_sprite("World", self.uborder_sprite)

        for x in range(225, ScreenWidth-225, 450):
            for y in range(150, ScreenHeight+50, 50):
                ground = arcade.Sprite("Images/ground_cave.png", 0.05)
                ground.center_x = x
                ground.center_y = y
                self.scene.add_sprite("World", ground)
        for x in range(450, ScreenWidth, 450):
            for y in range(0, ScreenHeight-100, 50):
                ground = arcade.Sprite("Images/ground_cave.png", 0.05)
                ground.center_x = x
                ground.center_y = y
                self.scene.add_sprite("World", ground)
                var = x
        for x in range(var, ScreenWidth+50, 50):
            ground = arcade.Sprite("Images/ground_cave.png", 0.05)
            ground.center_x = x
            ground.center_y = 25
            self.scene.add_sprite("World", ground)

        self.urchin = arcade.Sprite("Images/urchin.png", 0.25*EnemyScaling)
        self.urchin.center_x = 337
        self.urchin.center_y = ScreenHeight - 100
        self.scene.add_sprite("Enemies", self.urchin)
        self.urchin2 = arcade.Sprite("Images/urchin.png", 0.25*EnemyScaling)
        self.urchin2.center_x = 563
        self.urchin2.center_y = 100
        self.scene.add_sprite("Enemies", self.urchin2)
        self.urchin3 = arcade.Sprite("Images/urchin.png", 0.25*EnemyScaling)
        self.urchin3.center_x = 787
        self.urchin3.center_y = ScreenHeight - 100
        self.scene.add_sprite("Enemies", self.urchin3)

        self.flag_sprite = arcade.Sprite("Images/flag.png", FlagScaling)
        self.flag_sprite.center_x = ScreenWidth - 50
        self.flag_sprite.center_y = 128
        self.scene.add_sprite("Flag",self.flag_sprite)

        self.waterphysics_engine = arcade.PhysicsEnginePlatformer(self.mario_sprite, gravity_constant = 0.05, walls=self.scene["World"])
        self.waterphysics_engine.enable_multi_jump(float('inf'))

        self.enemy_physics_engine = arcade.PhysicsEnginePlatformer(self.urchin, gravity_constant = 0, walls=self.scene["World"])
        self.enemy_physics_engine2 = arcade.PhysicsEnginePlatformer(self.urchin2, gravity_constant = 0, walls=self.scene["World"])
        self.enemy_physics_engine3 = arcade.PhysicsEnginePlatformer(self.urchin3, gravity_constant = 0, walls=self.scene["World"])

#lvl5 *************************************************************************************************************************************
    def lvl_5_setup(self):
        #Walk up to boss level
        self.scene = arcade.Scene()
        self.player_list = arcade.SpriteList()
        self.scene.add_sprite_list("Enemies")
        self.scene.add_sprite_list("World", use_spatial_hash = True)

        self.mario_sprite = self.player_sprite = PlayerCharacter(self.mushroom)
        self.mario_sprite.center_x = 50
        self.mario_sprite.center_y = 27
        self.player_list.append(self.mario_sprite)

        self.rborder_sprite = arcade.Sprite("Images/border.png", PlayerScaling)
        self.rborder_sprite.center_x = ScreenWidth
        self.rborder_sprite.center_y = 0
        self.scene.add_sprite("World", self.rborder_sprite)
        self.lborder_sprite = arcade.Sprite("Images/border.png", PlayerScaling)
        self.lborder_sprite.center_x = -5
        self.lborder_sprite.center_y = 0
        self.scene.add_sprite("World", self.lborder_sprite)

        self.tube_sprite = arcade.Sprite("Images/tube.png", 0.35)
        self.tube_sprite.center_x = ScreenWidth - 100
        self.tube_sprite.center_y = 95
        self.scene.add_sprite("World",self.tube_sprite)

        sign = arcade.Sprite("Images/boss/turtsign.png", 0.15)
        sign.center_x = ScreenWidth - 100
        sign.center_y = 85
        self.scene.add_sprite("World", sign)

        for x in range(0, ScreenWidth+50, 50):
            ground = arcade.Sprite("Images/dblx5qhqm0l61.png", ObstacleScaling)
            ground.center_x = x
            ground.center_y = 25
            self.scene.add_sprite("World", ground)

        self.physics_engine = arcade.PhysicsEnginePlatformer(self.mario_sprite, gravity_constant = GRAVITY, walls=self.scene["World"])

#******************************************************************************************************************************************
#EXECUTE **********************************************************************************************************************************
#Draw *************************************************************************************************************************************

    def on_draw(self):
        self.clear()

        #draw level 1
        if self.current_level == 0:
            arcade.draw_lrwh_rectangle_textured(0, 0, ScreenWidth, ScreenHeight, self.background)
        #draw level 2
        elif self.current_level == 1:
            arcade.draw_lrwh_rectangle_textured(0, 0, ScreenWidth, ScreenHeight, self.background)
        #draw level 3
        elif self.current_level == 2:
            arcade.draw_lrwh_rectangle_textured(0, 0, ScreenWidth, ScreenHeight, self.cavebackground)
        #draw level 4.1
        elif self.current_level == 3:
            arcade.draw_lrwh_rectangle_textured(0, 0, ScreenWidth, ScreenHeight, self.background4)
        #draw level 4.2
        elif self.current_level == 42:
            arcade.draw_lrwh_rectangle_textured(0, 0, ScreenWidth, ScreenHeight, self.background42)
        #draw level 5
        elif self.current_level == 4:
            arcade.draw_lrwh_rectangle_textured(0, 0, ScreenWidth, ScreenHeight, self.background5)

        #draw all
        self.scene.draw()
        self.player_list.draw()

#Events ***********************************************************************************************************************************

    def on_tube_event(self):
        if self.current_level == 4:
            button = BossView(self.mushroom)
            self.window.show_view(button)
        else:
            button = GameView(42, self.mushroom, active_level = 4)
            self.window.show_view(button)
    
    def on_flag_collision(self):
        self.mario_sprite.change_x = 0
        LevComp = LevCompView(self.current_level, self.mushroom)
        self.window.show_view(LevComp)

    def on_lvl2mushroom_collision(self):
        if self.physics_engine.gravity_constant == 2*GRAVITY:
            self.mario_sprite.change_y = 40
            self.mario_sprite.change_x = 5
        else:
            self.mario_sprite.change_y = 30
            self.mario_sprite.change_x = 3

    def on_lvl1qblock_collision(self):
        self.colPos = False
        self.qblockTest_sprite.kill()
        self.qblock_sprite.texture = arcade.load_texture("Images/flatblock.jpg")
        self.mushroom_sprite = arcade.Sprite("Images/mushroom.png", PowerUpScaling)
        self.mushroom_sprite.center_x = 750
        self.mushroom_sprite.center_y = 455
        self.scene.add_sprite("Mushroom", self.mushroom_sprite)
        self.powerup_physics_engine = arcade.PhysicsEnginePlatformer(self.mushroom_sprite, gravity_constant = 0.2*GRAVITY, walls=self.scene["World"])
        self.powerup = True
        self.mushroom_sprite.change_y = 5
        self.mushroom_sprite.change_x = self.mushMove
    
    def check_enemy_collision(self):
        #level 1 check
        if self.current_level == 0:
            if self.mario_sprite.center_y > 100:
                self.mario_sprite.change_y = 10
                self.goomba_sprite.kill()
            else:
                if self.small:
                    self.mario_sprite.change_x = 0
                    self.enemy_move = False
                    self.mushroom = False
                    self.mario_sprite.kill()
                    arcade.pause(0.05)
                    GameOver = GameOverView(self.current_level)
                    self.window.show_view(GameOver)
                elif not self.small:
                    self.enColPos = False
                    self.mario_sprite.change_y = -100
                    self.EnemySpeed = -self.EnemySpeed
                    self.goomba_sprite.change_x = 10*self.EnemySpeed
                    self.mario_sprite.idle_texture_pair = load_texture_pair("/Users/logancamp/Passion/Coding Projects/Mario/Images/babymario2.png")
                    self.mario_sprite.jump_texture_pair = load_texture_pair("/Users/logancamp/Passion/Coding Projects/Mario/Images/babymario3.png")
                    self.mario_sprite.fall_texture_pair = load_texture_pair("/Users/logancamp/Passion/Coding Projects/Mario/Images/babymario2.png")
                    self.mario_sprite.walk_texture_pair = load_texture_pair("/Users/logancamp/Passion/Coding Projects/Mario/Images/babymario4.png")
                    IM = PIL.Image.open("Images/babymario2.png", "r").convert("RGBA")
                    self.mario_sprite.hit_box = arcade.calculate_hit_box_points_simple(IM)
                    self.mushroom = False
                    self.small = True

        #level 2 check
        elif self.current_level == 1:
            if self.mario_sprite.center_y > self.flyingTurt_sprite.center_y:
                self.mario_sprite.change_y = 20
                self.mario_sprite.change_x = 3
                self.flyingTurt_sprite.kill()
            else:
                if self.small:
                    self.mario_sprite.change_x = 0
                    self.mario_sprite.change_y = 0
                    self.enemy_move = False
                    self.mushroom = False
                    self.mario_sprite.kill()
                    arcade.pause(0.05)
                    GameOver = GameOverView(self.current_level)
                    self.window.show_view(GameOver)
                else:
                    self.enColPos = False
                    self.mario_sprite.center_y -= 100
                    self.mario_sprite.change_x = 100
                    self.EnemySpeed *= -1
                    self.flyingTurt_sprite.center_y += 100
                    self.mario_sprite.idle_texture_pair = load_texture_pair("Images/babymario2.png")
                    self.mario_sprite.jump_texture_pair = load_texture_pair("Images/babymario3.png")
                    self.mario_sprite.fall_texture_pair = load_texture_pair("Images/babymario2.png")
                    self.mario_sprite.walk_texture_pair = load_texture_pair("Images/babymario4.png")
                    IM = PIL.Image.open("Images/babymario2.png", "r").convert("RGBA")
                    self.mario_sprite.hit_box = arcade.calculate_hit_box_points_simple(IM)
                    self.mushroom = False
                    self.small = True

        #level 3 check
        elif self.current_level == 2:
            self.mario_sprite.change_x = 0
            self.mario_sprite.change_y = 0
            self.enemy_move = False
            self.mushroom = False
            self.mario_sprite.kill()
            GameOver = GameOverView(self.current_level)
            self.window.show_view(GameOver)

        #level 4 check
        elif self.current_level == 3:
            if self.small:
                self.mario_sprite.change_x = 0
                self.enemy_move = False
                self.mushroom = False
                self.mario_sprite.kill()
                arcade.pause(0.05)
                GameOver = GameOverView(self.current_level)
                self.window.show_view(GameOver)
            else:
                self.enColPos = False
                self.mario_sprite.change_y = -100
                self.mario_sprite.idle_texture_pair = load_texture_pair("Images/babymario2.png")
                self.mario_sprite.jump_texture_pair = load_texture_pair("Images/babymario3.png")
                self.mario_sprite.fall_texture_pair = load_texture_pair("Images/babymario2.png")
                self.mario_sprite.walk_texture_pair = load_texture_pair("Images/babymario4.png")
                IM = PIL.Image.open("Images/babymario2.png", "r").convert("RGBA")
                self.mario_sprite.hit_box = arcade.calculate_hit_box_points_simple(IM)
                self.mushroom = False
                self.small = True

    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE or key == arcade.key.UP or key == arcade.key.W:
            if self.current_level != 42:
                if self.physics_engine.can_jump():
                    self.mario_sprite.change_y = MarioJumpSpeed
            else:
                if self.waterphysics_engine.can_jump():
                    self.mario_sprite.change_y = 3

        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.mario_sprite.change_x = MarioMovementSpeed

        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.mario_sprite.change_x = -MarioMovementSpeed

        elif key == arcade.key.DOWN or key == arcade.key.S:
            if not self.mushroom and self.current_level != 42:
                self.physics_engine.gravity_constant = 1.5*GRAVITY
            else:
                if self.current_level != 42:
                    self.physics_engine.gravity_constant = 2*GRAVITY
                    self.mario_sprite.fall_texture_pair = load_texture_pair("Images/smash.png")
            if ((self.active_level == 4 and self.part == 1) or self.active_level == 5) and (self.mario_sprite.center_x > self.tube_sprite.center_x-25 and self.mario_sprite.center_x < self.tube_sprite.center_x+25):
                self.on_tube_event()
    
    def on_key_release(self, key, modifier):
        if key == arcade.key.RIGHT or key == arcade.key.D:
            self.mario_sprite.change_x = 0
        
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.mario_sprite.change_x = 0
        
        elif key == arcade.key.ESCAPE:
            Pause = PauseView(self, self.current_level, self.mushroom)
            self.window.show_view(Pause)
        
        elif key == arcade.key.DOWN or key == arcade.key.S:
            if self.current_level != 42:
                self.physics_engine.gravity_constant = GRAVITY
            if self.mushroom:
                self.mario_sprite.fall_texture_pair = load_texture_pair("Images/mario2.png")

#Update ***********************************************************************************************************************************

    def on_update(self, delta_time):
        #level 1 update
        if self.current_level == 0:
            if self.goomba_sprite.center_x < 300:
                self.EnemySpeed = 2.5
            elif self.goomba_sprite.center_x > 1050:
                self.EnemySpeed = -2.5
            if self.enemy_move == True:
                self.goomba_sprite.change_x = self.EnemySpeed
            else:
                self.goomba_sprite.change_x = 0

            self.enemy_physics_engine.update()
            self.physics_engine.update()

            if self.mario_sprite.collides_with_sprite(self.qblockTest_sprite) and self.colPos:
                if self.current_level == 0:
                    self.on_lvl1qblock_collision()

            if self.powerup:
                self.powerup_physics_engine.update()
                self.mushroom_sprite.change_x = self.mushMove
                if self.mushroom_sprite.center_x < 50 or self.mushroom_sprite.center_x > ScreenWidth-100:
                    self.mushMove = -self.mushMove
                    self.mushroom_sprite.change_x = self.mushMove
                if self.mario_sprite.collides_with_sprite(self.mushroom_sprite):
                    self.mushroom_sprite.kill()
                    self.mushroom_sprite.center_y = -50
                    self.mario_sprite.idle_texture_pair = load_texture_pair("Images/mario2.png")
                    self.mario_sprite.jump_texture_pair = load_texture_pair("Images/mario3.png")
                    self.mario_sprite.fall_texture_pair = load_texture_pair("Images/mario2.png")
                    self.mario_sprite.walk_texture_pair = load_texture_pair("Images/mario4.png")
                    self.mario_sprite.change_y = 5
                    self.mario_sprite.change_y = 0
                    IM = PIL.Image.open("Images/mario2.png", "r").convert("RGBA")
                    self.mario_sprite.hit_box = arcade.calculate_hit_box_points_simple(IM)
                    self.mushroom = True
                    self.small = False

            if self.mario_sprite.collides_with_sprite(self.flag_sprite):
                self.on_flag_collision()

        #level 2 update
        elif self.current_level == 1:
            if self.mario_sprite.collides_with_sprite(self.mushPlat_sprite):
                self.on_lvl2mushroom_collision()

            if self.flyingTurt_sprite.center_y < 200:
                self.EnemySpeed = 2.5
                self.flyingTurt_sprite.texture = arcade.load_texture("Images/flyingturtle3.png")
            elif self.flyingTurt_sprite.center_y > ScreenHeight - 100:
                self.EnemySpeed = -2.5
                self.flyingTurt_sprite.texture = arcade.load_texture("Images/flyingturtle1.png")
            if self.enemy_move == True:
                self.flyingTurt_sprite.change_y = self.EnemySpeed
            else:
                self.flyingTurt_sprite.change_y = 0

            if self.mario_sprite.collides_with_sprite(self.flag_sprite):
                self.on_flag_collision()

            self.enemy_physics_engine.update()
            self.physics_engine.update()

        #level 3 update
        elif self.current_level == 2:
            if self.mario_sprite.center_x > self.thwomp_sprite.center_x:
                self.enemy_physics_engine.update()
            if self.mario_sprite.center_x > self.thwomp_sprite2.center_x:
                self.enemy_physics_engine2.update()
            if self.mario_sprite.center_x > self.thwomp_sprite3.center_x:
                self.enemy_physics_engine3.update()
            if self.mario_sprite.center_x > self.thwomp_sprite4.center_x:
                self.enemy_physics_engine4.update()
            if self.mario_sprite.center_x > self.thwomp_sprite5.center_x:
                self.enemy_physics_engine5.update()
            if self.mario_sprite.center_x > self.thwomp_sprite6.center_x:
                self.enemy_physics_engine6.update()
            if self.mario_sprite.center_x > self.thwomp_sprite7.center_x:
                self.enemy_physics_engine7.update()
            
            if self.mario_sprite.collides_with_sprite(self.flag_sprite):
                self.on_flag_collision()

            self.physics_engine.update()

        #level 4.1 update
        elif self.current_level == 3:
            self.physics_engine.update()

        #level 4.2 update
        elif self.current_level == 42:
            if self.mario_sprite.collides_with_sprite(self.flag_sprite):
                    self.on_flag_collision()

            if self.urchin.center_y < 150:
                self.EnemySpeed = 2.5
            elif self.urchin.center_y > ScreenHeight - 150:
                self.EnemySpeed = -2.5
            if self.enemy_move == True:
                self.urchin.change_y = self.EnemySpeed
                self.urchin3.change_y = self.EnemySpeed
            else:
                self.urchin.change_y = 0

            if self.urchin2.center_y < 150:
                self.EnemySpeed2 = 2.5
            elif self.urchin2.center_y > ScreenHeight - 150:
                self.EnemySpeed2 = -2.5
            if self.enemy_move == True:
                self.urchin2.change_y = self.EnemySpeed2
            else:
                self.urchin2.change_y = 0

            self.waterphysics_engine.update()
            self.enemy_physics_engine.update()
            self.enemy_physics_engine2.update()
            self.enemy_physics_engine3.update()

            if self.mario_sprite.center_y < -200 or self.mario_sprite.collides_with_list(self.scene.get_sprite_list("Enemies")):
                self.enemy_move = False
                self.mushroom = False
                self.mario_sprite.kill()
                GameOver = GameOverView(self.current_level)
                self.window.show_view(GameOver)

        #level 5 update
        elif self.current_level == 4:
            self.physics_engine.update()

        #update all
        if self.enColPos:
            if self.mario_sprite.collides_with_list(self.scene.get_sprite_list("Enemies")):
                self.check_enemy_collision()
        
        if self.enColPos == False:
            self.switchPos += 1
            if self.switchPos == 5:
                self.enColPos = True
                self.switchPos = 0

        self.player_list.update_animation()

#******************************************************************************************************************************************
#******************************************************************************************************************************************
#******************************************************************************************************************************************
#******************************************************************************************************************************************
#******************************************************************************************************************************************
#******************************************************************************************************************************************

#Boss Level Class *************************************************************************************************************************

class BossView(arcade.View):
    def __init__(self, mushroom, part = 0, EnemySpeed = 2.5):
        super().__init__()
        self.clear()

        self.mushroom = mushroom
        self.part = part
        self.mario_sprite = None
        self.player_list = None

        self.scene = None
        self.player_list = None
        self.mario_sprite = None
        self.flag_sprite = None

        self.enemy_move = True
        self.small = not mushroom
        self.bowserAnimation = True
        self.bowsershell = False
        
        self.physics_engine = None
        self.enemy_physics_engine = None

        self.EnemySpeed = EnemySpeed
        self.EnemySpeed2 = EnemySpeed
        self.time = 0
        self.time2 = 0
        self.lifecount = 0

        self.background1 = arcade.load_texture("Images/boss/castle_outside.png")
        self.background2 = arcade.load_texture("Images/boss/insidecastle.png")
        self.background3 = arcade.load_texture("Images/boss/fightbackground.png")

        if self.part == 0:
            self.setupOutside()
        elif self.part == 1:
            self.setupInside()
        else:
            self.setupBossFight()
    
    def on_show_view(self):
        self.background1 = arcade.load_texture("Images/boss/castle_outside.png")
        self.background2 = arcade.load_texture("Images/boss/insidecastle.png")
        self.background3 = arcade.load_texture("Images/boss/fightbackground.png")
        self.on_draw()

# set-up part 1 ***************************************************************************************************************************

    def setupOutside(self):
        self.scene = arcade.Scene()
        self.player_list = arcade.SpriteList()
        self.scene.add_sprite_list("Enemies")
        self.scene.add_sprite_list("Sign")
        self.scene.add_sprite_list("World", use_spatial_hash = True)
        self.scene.add_sprite_list("World2", use_spatial_hash = True)

        self.mario_sprite = self.player_sprite = PlayerCharacter(self.mushroom)
        self.mario_sprite.center_x = 100
        self.mario_sprite.center_y = 90
        self.player_list.append(self.mario_sprite)

        self.lborder_sprite = arcade.Sprite("Images/border.png", PlayerScaling)
        self.lborder_sprite.center_x = -5
        self.lborder_sprite.center_y = 0
        self.scene.add_sprite("World", self.lborder_sprite)

        self.tube_sprite = arcade.Sprite("Images/tube.png", 0.35)
        self.tube_sprite.center_x = 100
        self.tube_sprite.center_y = 75
        self.scene.add_sprite("World",self.tube_sprite)

        sign = arcade.Sprite("Images/boss/arrowsign.png", 0.75)
        sign.center_x = ScreenWidth - 400
        sign.center_y = 88
        self.scene.add_sprite("Sign", sign)

        for x in range(0, ScreenWidth+200, 50):
            ground = arcade.Sprite("Images/boss/darkbrick.png", ObstacleScaling)
            ground.center_x = x
            ground.center_y = 25
            self.scene.add_sprite("World", ground)
            border = arcade.Sprite("Images/topborder.png", ObstacleScaling)
            border.center_x = x
            border.center_y = -200
            self.scene.add_sprite("World2", border)
            border = arcade.Sprite("Images/topborder.png", ObstacleScaling)
            border.center_x = x
            border.center_y = -195
            self.scene.add_sprite("bouncer", border)

        for y in range(250, ScreenHeight+50, 50):
            ground = arcade.Sprite("Images/boss/darkbrick.png", ObstacleScaling)
            ground.center_x = ScreenWidth
            ground.center_y = y
            self.scene.add_sprite("World", ground)

        self.fireball = arcade.Sprite("Images/boss/fireball2.png", 0.2*EnemyScaling)
        self.fireball.center_x = ScreenWidth/2
        self.fireball.center_y = -45
        self.scene.add_sprite("Enemies", self.fireball)
        self.fireball2 = arcade.Sprite("Images/boss/fireball2.png", 0.12*EnemyScaling)
        self.fireball2.center_x = ScreenWidth/2 - 15
        self.fireball2.center_y = -20
        self.scene.add_sprite("Enemies", self.fireball2)
        self.fireball3 = arcade.Sprite("Images/boss/fireball2.png", 0.12*EnemyScaling)
        self.fireball3.center_x = ScreenWidth/2 - 30
        self.fireball3.center_y = 5
        self.scene.add_sprite("Enemies", self.fireball3)

        self.enemy_physics_engine3 = arcade.PhysicsEnginePlatformer(self.fireball3, gravity_constant = 0.5*GRAVITY, walls=self.scene["World2"])
        self.enemy_physics_engine2 = arcade.PhysicsEnginePlatformer(self.fireball2, gravity_constant = 0.5*GRAVITY, walls=self.scene["World2"])
        self.enemy_physics_engine = arcade.PhysicsEnginePlatformer(self.fireball, gravity_constant = 0.5*GRAVITY, walls=self.scene["World2"])
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.mario_sprite, gravity_constant = GRAVITY, walls=self.scene["World"])

# set-up part 2 ***************************************************************************************************************************

    def setupInside(self):
        self.scene = arcade.Scene()
        self.player_list = arcade.SpriteList()
        self.scene.add_sprite_list("Other")
        self.scene.add_sprite_list("World", use_spatial_hash = True)
        self.scene.add_sprite_list("Enemies")

        self.mario_sprite = self.player_sprite = PlayerCharacter(self.mushroom)
        self.mario_sprite.center_x = 50
        self.mario_sprite.center_y = 50
        self.player_list.append(self.mario_sprite)

        self.goomba_sprite = arcade.Sprite("Images/boss/spiny.png", 0.2*EnemyScaling)
        self.goomba_sprite.center_x = ScreenWidth/2-100
        self.goomba_sprite.center_y = (ScreenHeight-183)/3 + 12
        self.scene.add_sprite("Other", self.goomba_sprite)

        self.sign = arcade.Sprite("Images/boss/lavasign.png", 0.25)
        self.sign.center_x = ScreenWidth/2+100
        self.sign.center_y = 80
        self.scene.add_sprite("Other", self.sign)

        self.door_sprite = arcade.Sprite("Images/boss/doors.png", 0.25)
        self.door_sprite.center_x = ScreenWidth/2
        self.door_sprite.center_y = ScreenHeight - 100
        self.scene.add_sprite("Other", self.door_sprite)

        for x in range(int(self.door_sprite.center_x - 80), int(self.door_sprite.center_x + 100), 30):
            ground = arcade.Sprite("Images/boss/whitebrick.png", 0.03)
            ground.center_x = x
            ground.center_y = ScreenHeight - 183
            self.scene.add_sprite("World", ground)

        self.rborder_sprite = arcade.Sprite("Images/border.png", PlayerScaling)
        self.rborder_sprite.center_x = ScreenWidth+5
        self.rborder_sprite.center_y = 0
        self.scene.add_sprite("World", self.rborder_sprite)
        self.lborder_sprite = arcade.Sprite("Images/border.png", PlayerScaling)
        self.lborder_sprite.center_x = -5
        self.lborder_sprite.center_y = 0
        self.scene.add_sprite("World", self.lborder_sprite)

        for x in range(0, ScreenWidth+50, 25):
            ground = arcade.Sprite("Images/boss/whitebrick.png", 0.05)
            ground.center_x = x
            ground.center_y = 25
            self.scene.add_sprite("World", ground)
            if x > ScreenWidth/5 and x < ScreenWidth/2:
                ground = arcade.Sprite("Images/boss/whitebrick.png", 0.03)
                ground.center_x = x
                ground.center_y = (ScreenHeight-183)/3 + 2
                self.scene.add_sprite("World", ground)

        ground = arcade.Sprite("Images/boss/whitebrick.png", 0.03)
        ground.center_x = ScreenWidth/2 + 100
        ground.center_y = ((ScreenHeight+55)/3)
        self.scene.add_sprite("World", ground)

        for x in range(int(ScreenWidth/2)+200, ScreenWidth-300, 25):
            ground = arcade.Sprite("Images/boss/whitebrick.png", 0.03)
            ground.center_x = x
            ground.center_y = ((ScreenHeight-183)/3) + 205
            self.scene.add_sprite("World", ground)

        self.lava = arcade.Sprite("Images/boss/lava.png", 3.3)
        self.lava.center_x = ScreenWidth/2
        self.lava.center_y = -500
        self.scene.add_sprite("Enemies", self.lava)

        self.physics_engine = arcade.PhysicsEnginePlatformer(self.mario_sprite, gravity_constant = GRAVITY, walls=self.scene["World"])
        self.enemy_physics_engine = arcade.PhysicsEnginePlatformer(self.lava, gravity_constant = 0)
        self.goomba_physics_engine = arcade.PhysicsEnginePlatformer(self.goomba_sprite, gravity_constant = GRAVITY, walls=self.scene["World"])

# set-up part 3 ***************************************************************************************************************************

    def setupBossFight(self):
        self.scene = arcade.Scene()
        self.player_list = arcade.SpriteList()
        self.scene.add_sprite_list("Enemies")
        self.scene.add_sprite_list("World", use_spatial_hash = True)

        self.mario_sprite = self.player_sprite = PlayerCharacter(self.mushroom)
        self.mario_sprite.center_x = 0
        self.mario_sprite.center_y = 50
        self.player_list.append(self.mario_sprite)

        self.bowser_sprite = self.player_sprite = BowserCharacter()
        self.bowser_sprite.center_x = ScreenWidth/2 + 200
        self.bowser_sprite.center_y = 50
        self.player_list.append(self.bowser_sprite)

        self.pbut = arcade.Sprite("Images/boss/pbut.png", 0.1)
        self.pbut.center_x = random.randint(ScreenWidth/2-100,ScreenWidth-100)
        self.pbut.center_y = 70
        self.scene.add_sprite("Other", self.pbut)

        for y in range(0, ScreenHeight+50, 50):
            self.rborder_sprite = arcade.Sprite("Images/boss/whitebrick.png", 0.05)
            self.rborder_sprite.center_x = ScreenWidth
            self.rborder_sprite.center_y = y
            self.scene.add_sprite("World", self.rborder_sprite)
        for y in range(200, ScreenHeight+50, 50):
            self.lborder_sprite = arcade.Sprite("Images/boss/whitebrick.png", 0.05)
            self.lborder_sprite.center_x = 0
            self.lborder_sprite.center_y = y
            self.scene.add_sprite("World", self.lborder_sprite)
        for x in range(0, ScreenWidth+50, 50):
            ground = arcade.Sprite("Images/boss/whitebrick.png", 0.05)
            ground.center_x = x
            ground.center_y = 25
            self.scene.add_sprite("World", ground)
            ground = arcade.Sprite("Images/boss/whitebrick.png", 0.05)
            ground.center_x = x
            ground.center_y = ScreenHeight - 25
            self.scene.add_sprite("World", ground)

        self.physics_engine = arcade.PhysicsEnginePlatformer(self.mario_sprite, gravity_constant = GRAVITY, walls=self.scene["World"])
        self.enemy_physics_engine = arcade.PhysicsEnginePlatformer(self.bowser_sprite, gravity_constant = GRAVITY, walls=self.scene["World"])

#*******************************************************************************************************************************************
#*******************************************************************************************************************************************

    def on_draw(self):
        self.clear()
        #draw part 1
        if self.part == 0:
            arcade.draw_lrwh_rectangle_textured(0, 0, ScreenWidth, ScreenHeight, self.background1)
        #draw part 2
        elif self.part == 1:
            arcade.draw_lrwh_rectangle_textured(0, 0, ScreenWidth, ScreenHeight, self.background2)
        #draw part 3
        else:
            arcade.draw_lrwh_rectangle_textured(0, 0, ScreenWidth, ScreenHeight, self.background3)
        
        #draw all
        self.scene.draw()
        self.player_list.draw()

#*******************************************************************************************************************************************
#*******************************************************************************************************************************************

    def on_next_part(self):
        self.part += 1
        if self.part < 3:
            part = BossView(self.mushroom, self.part)
            self.window.show_view(part)

    def check_enemy_collision(self):
        #check part 1
        if self.part == 0:
            if self.small:
                self.mario_sprite.change_x = 0
                self.enemy_move = False
                self.mushroom = False
                self.mario_sprite.kill()
                arcade.pause(0.05)
                GameOver = GameOverView(51)
                self.window.show_view(GameOver)
            else:
                self.enColPos = False
                self.mario_sprite.change_y = -100
                self.EnemySpeed = -self.EnemySpeed
                self.fireball.change_x = 10*self.EnemySpeed
                self.mario_sprite.idle_texture_pair = load_texture_pair("Images/babymario2.png")
                self.mario_sprite.jump_texture_pair = load_texture_pair("Images/babymario3.png")
                self.mario_sprite.fall_texture_pair = load_texture_pair("Images/babymario2.png")
                self.mario_sprite.walk_texture_pair = load_texture_pair("Images/babymario4.png")
                IM = PIL.Image.open("Images/babymario2.png", "r").convert("RGBA")
                self.mario_sprite.hit_box = arcade.calculate_hit_box_points_simple(IM)
                self.mushroom = False
                self.small = True

        #check part 2
        elif self.part == 1:
            self.mario_sprite.change_x = 0
            self.enemy_move = False
            self.mushroom = False
            self.mario_sprite.kill()
            arcade.pause(0.05)
            GameOver = GameOverView(51)
            self.window.show_view(GameOver)
    
        #check part 3
        else:
            if not self.bowsershell:
                self.mario_sprite.change_y = 10
                self.bowser_sprite.kill()
                self.bowser_sprite.center_y = -100
                button = WinnerView()
                self.window.show_view(button)
            else:
                if self.small:
                    self.mario_sprite.change_x = 0
                    self.enemy_move = False
                    self.mushroom = False
                    self.mario_sprite.kill()
                    arcade.pause(0.05)
                    GameOver = GameOverView(51)
                    self.window.show_view(GameOver)
                else:
                    self.enColPos = False
                    self.mario_sprite.change_y = -100
                    self.EnemySpeed = -self.EnemySpeed
                    self.goomba_sprite.change_x = 10*self.EnemySpeed
                    self.mario_sprite.idle_texture_pair = load_texture_pair("Images/babymario2.png")
                    self.mario_sprite.jump_texture_pair = load_texture_pair("Images/babymario3.png")
                    self.mario_sprite.fall_texture_pair = load_texture_pair("Images/babymario2.png")
                    self.mario_sprite.walk_texture_pair = load_texture_pair("Images/babymario4.png")
                    IM = PIL.Image.open("Images/babymario2.png", "r").convert("RGBA")
                    self.mario_sprite.hit_box = arcade.calculate_hit_box_points_simple(IM)
                    self.mushroom = False
                    self.small = True

    def on_pbut_press(self):
        self.bowsershell = False
        self.pbut.center_y = -50
        self.pbut.kill()
        self.bowser_sprite.change_x = 0
        self.bowser_sprite.idle_texture_pair = load_texture_pair("Images/boss/idle.png")
        self.bowser_sprite.walk_texture_pair = load_texture_pair("Images/boss/walk.png")
        self.bowser_sprite.scale = EnemyScaling
        IM = PIL.Image.open("Images/boss/idle.png", "r").convert("RGBA")
        self.bowser_sprite.hit_box = arcade.calculate_hit_box_points_simple(IM)

#*******************************************************************************************************************************************
#*******************************************************************************************************************************************

    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE or key == arcade.key.UP or key == arcade.key.W:
            if self.part == 1 and self.mario_sprite.center_x > self.door_sprite.center_x - 50 and self.mario_sprite.center_x < self.door_sprite.center_x + 50 and self.mario_sprite.center_y > ScreenHeight-183:
                self.on_next_part()
            if self.physics_engine.can_jump():
                self.mario_sprite.change_y = MarioJumpSpeed
            if key != arcade.key.SPACE and self.part == 2:
                self.on_next_part()

        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.mario_sprite.change_x = MarioMovementSpeed

        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.mario_sprite.change_x = -MarioMovementSpeed

        elif key == arcade.key.DOWN or key == arcade.key.S:
            if not self.mushroom:
                self.physics_engine.gravity_constant = 1.5*GRAVITY
            else:
                self.physics_engine.gravity_constant = 2*GRAVITY
                self.mario_sprite.fall_texture_pair = load_texture_pair("Images/smash.png")
    
    def on_key_release(self, key, modifier):
        if key == arcade.key.RIGHT or key == arcade.key.D:
            self.mario_sprite.change_x = 0
        
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.mario_sprite.change_x = 0
        
        elif key == arcade.key.ESCAPE:
            Pause = PauseView(self, self.part, self.mushroom)
            self.window.show_view(Pause)
        
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.physics_engine.gravity_constant = GRAVITY
            if self.mushroom:
                self.mario_sprite.fall_texture_pair = load_texture_pair("Images/mario2.png")

#*******************************************************************************************************************************************
#*******************************************************************************************************************************************
  
    def on_update(self, delta_time):
        #update part 1
        if self.part == 0:
            if self.mario_sprite.center_x > ScreenWidth + 50:
                self.on_next_part()
            
            if self.mario_sprite.collides_with_list(self.scene.get_sprite_list("Enemies")):
                self.check_enemy_collision()

            if self.fireball.center_x < 440:
                self.fireball.scale = 0.2*EnemyScaling
                self.fireball3.scale = 0.12*EnemyScaling
                self.EnemySpeed = 2
            elif self.fireball.center_x > 1100:
                self.fireball3.scale = 0.2*EnemyScaling
                self.fireball.scale = 0.12*EnemyScaling
                self.EnemySpeed = -2
            self.fireball.change_x = self.EnemySpeed
            self.fireball2.change_x = self.EnemySpeed
            self.fireball3.change_x = self.EnemySpeed
            if self.fireball.collides_with_list(self.scene.get_sprite_list("bouncer")):
                self.fireball.change_y = 20
            if self.fireball2.collides_with_list(self.scene.get_sprite_list("bouncer")):    
                self.fireball2.change_y = 20
            if self.fireball3.collides_with_list(self.scene.get_sprite_list("bouncer")):    
                self.fireball3.change_y = 20

            self.enemy_physics_engine3.update()
            self.enemy_physics_engine.update()
            self.enemy_physics_engine2.update()

        #update part 2
        elif self.part == 1:
            if self.time == 70:
                self.lava.change_y = 1
                self.time = 0
            self.time += 1

            if self.goomba_sprite.center_x < ScreenWidth/2-350:
                self.EnemySpeed = 2
                self.goomba_sprite.texture = arcade.load_texture("Images/boss/spiny.png", flipped_horizontally=True)
            elif self.goomba_sprite.center_x > ScreenWidth/2-50:
                self.EnemySpeed = -2
                self.goomba_sprite.texture = arcade.load_texture("Images/boss/spiny.png")
            if self.enemy_move == True:
                self.goomba_sprite.change_x = self.EnemySpeed
            else:
                self.goomba_sprite.change_x = 0

            if self.mario_sprite.collides_with_list(self.scene.get_sprite_list("Enemies")) or self.mario_sprite.collides_with_sprite(self.goomba_sprite):
                self.check_enemy_collision()

            self.enemy_physics_engine.update()
            self.goomba_physics_engine.update()

        #update part 3
        else:
            if not self.bowsershell:
                if self.mario_sprite.center_x > 60:
                    for y in range(50, 200, 50):
                        self.lborder_sprite = arcade.Sprite("Images/boss/whitebrick.png", 0.05)
                        self.lborder_sprite.center_x = 0
                        self.lborder_sprite.center_y = y
                        self.scene.add_sprite("World", self.lborder_sprite)
                        if self.bowserAnimation:
                            if self.time == 120:
                                self.bowser_sprite.change_x = -10
                                self.mario_sprite.change_x = 0
                                self.bowser_sprite.change_x = 0
                                self.bowser_sprite.scale *= 2
                                self.bowser_sprite.change_y = 20
                                self.bowser_sprite.scale /= 10
                                self.bowser_sprite.idle_texture_pair = load_texture_pair("Images/boss/shell.png")
                                self.bowser_sprite.walk_texture_pair = load_texture_pair("Images/boss/shell2.png")                            
                                IM = PIL.Image.open("Images/boss/shell2.png", "r").convert("RGBA")
                                self.bowser_sprite.hit_box = arcade.calculate_hit_box_points_simple(IM)
                                self.time = 0
                                self.bowsershell = True
                                self.bowserAnimation = False
                            self.time += 1

            if self.bowsershell:
                if self.bowser_sprite.center_x < 100:
                    self.EnemySpeed = 5.5
                elif self.bowser_sprite.center_x > ScreenWidth-100:
                    self.EnemySpeed = -5.5
                if self.enemy_move == True:
                    self.bowser_sprite.change_x = self.EnemySpeed
                else:
                    self.bowser_sprite.change_x = 0

            if self.mario_sprite.collides_with_sprite(self.bowser_sprite):
                self.check_enemy_collision()

            if self.mario_sprite.collides_with_sprite(self.pbut):
                self.on_pbut_press()

            self.enemy_physics_engine.update()
        
        #update all
        self.physics_engine.update()
        self.player_list.update_animation()


#******************************************************************************************************************************************
#******************************************************************************************************************************************
#******************************************************************************************************************************************
#******************************************************************************************************************************************
#******************************************************************************************************************************************
#******************************************************************************************************************************************

#Mario Animation **************************************************************************************************************************

def load_texture_pair(filename):
    #loads a texured pair list for animation
    return [arcade.load_texture(filename), arcade.load_texture(filename, flipped_horizontally=True)]

class PlayerCharacter(arcade.Sprite):
    def __init__(self, mushroom):
        super().__init__()
        self.mushroom = mushroom
        self.character_face_direction = RIGHT_FACING
        self.scale = PlayerScaling

        # Load textures for idle standing
        if self.mushroom:
            self.idle_texture_pair = load_texture_pair("Images/mario2.png")
            self.jump_texture_pair = load_texture_pair("Images/mario3.png")
            self.fall_texture_pair = load_texture_pair("Images/mario2.png")
            self.walk_texture_pair = load_texture_pair("Images/mario4.png")
            IM = PIL.Image.open("Images/mario2.png", "r").convert("RGBA")
            self.hit_box = arcade.calculate_hit_box_points_simple(IM)
        else:
            self.idle_texture_pair = load_texture_pair("Images/babymario2.png")
            self.jump_texture_pair = load_texture_pair("Images/babymario3.png")
            self.fall_texture_pair = load_texture_pair("Images/babymario2.png")
            self.walk_texture_pair = load_texture_pair("Images/babymario4.png")
            IM = PIL.Image.open("Images/babymario2.png", "r").convert("RGBA")
            self.hit_box = arcade.calculate_hit_box_points_simple(IM)
        
        # Set the initial texture
        self.texture = self.idle_texture_pair[0]


    def update_animation(self, delta_time: float = 1 / 60):

        # Flip to face left or right
        if self.change_x < 0 and self.character_face_direction == RIGHT_FACING:
            self.character_face_direction = LEFT_FACING
        elif self.change_x > 0 and self.character_face_direction == LEFT_FACING:
            self.character_face_direction = RIGHT_FACING

        # Jumping animation
        if self.change_y > 0:
            self.texture = self.jump_texture_pair[self.character_face_direction]
            return
        elif self.change_y < 0:
            self.texture = self.fall_texture_pair[self.character_face_direction]
            return

        # Idle animation
        if self.change_x == 0:
            self.texture = self.idle_texture_pair[self.character_face_direction]
            return

        # Walking animation
        if self.center_x % 20 == 0:
            self.texture = self.walk_texture_pair[self.character_face_direction]
        elif self.center_x % 20 == 1:
            self.texture = self.idle_texture_pair[self.character_face_direction]

#******************************************************************************************************************************************
#******************************************************************************************************************************************
#******************************************************************************************************************************************
#******************************************************************************************************************************************
#******************************************************************************************************************************************
#******************************************************************************************************************************************

class BowserCharacter(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.character_face_direction = RIGHT_FACING
        self.scale = EnemyScaling

        # Load textures for idle standing
        self.idle_texture_pair = load_texture_pair("Images/boss/idle.png")
        self.jump_texture_pair = load_texture_pair("Images/boss/angry.png")
        self.fall_texture_pair = load_texture_pair("Images/boss/idle.png")
        self.walk_texture_pair = load_texture_pair("Images/boss/walk.png")
    
        # Set the initial texture
        self.texture = self.idle_texture_pair[0]

    def update_animation(self, delta_time: float = 1 / 60):

        # Flip to face left or right
        if self.change_x < 0 and self.character_face_direction == RIGHT_FACING:
            self.character_face_direction = LEFT_FACING
        elif self.change_x > 0 and self.character_face_direction == LEFT_FACING:
            self.character_face_direction = RIGHT_FACING

        # Jumping animation
        if self.change_y > 0:
            self.texture = self.jump_texture_pair[self.character_face_direction]
            return
        elif self.change_y < 0:
            self.texture = self.fall_texture_pair[self.character_face_direction]
            return

        # Idle animation
        if self.change_x == 0:
            self.texture = self.idle_texture_pair[self.character_face_direction]
            return

        # Walking animation
        if self.center_x % 20 == 0:
            self.texture = self.walk_texture_pair[self.character_face_direction]
        elif self.center_x % 20 == 1:
            self.texture = self.idle_texture_pair[self.character_face_direction]


#******************************************************************************************************************************************
#******************************************************************************************************************************************
#******************************************************************************************************************************************
#******************************************************************************************************************************************
#******************************************************************************************************************************************
#******************************************************************************************************************************************

def main():
     window = arcade.Window(ScreenWidth, ScreenHeight, ScreenTitle)
     start_view = StartUpView()
     window.show_view(start_view)
     start_view.on_show_view()
     arcade.run()

if __name__ == "__main__":
    main()