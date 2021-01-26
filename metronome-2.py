import time
import arcade
import math


SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600

SPRITE_SCALING_CONSTANT = 0.5

click_sound = arcade.load_sound("resources/click-sound.ogg")
phbbbt_sound = arcade.load_sound("resources/metronome_phbbbt.ogg")
tempo_up_sprite = arcade.Sprite("resources/tempo_up_button.png", SPRITE_SCALING_CONSTANT)
tempo_down_sprite = arcade.Sprite("resources/tempo_down_button.png", SPRITE_SCALING_CONSTANT)
play_sprite = arcade.Sprite("resources/metronome_play_button.png", SPRITE_SCALING_CONSTANT)
stop_sprite = arcade.Sprite("resources/metronome_stop_button.png", SPRITE_SCALING_CONSTANT)
halves_sprite = arcade.Sprite("resources/metronome_halves.png", SPRITE_SCALING_CONSTANT)
quarters_sprite = arcade.Sprite("resources/metronome_quarters.png", SPRITE_SCALING_CONSTANT)
eighths_sprite = arcade.Sprite("resources/metronome_eighths.png", SPRITE_SCALING_CONSTANT)
sixteenths_sprite = arcade.Sprite("resources/metronome_sixteenths.png", SPRITE_SCALING_CONSTANT)

SUBDIVISION_BUTTONS_Y = 100

class Metronome(arcade.View):

    def __init__(self):
        super().__init__()



        self.button_list = None
        self.tempo_up_button = None
        self.temp_down_button = None
        self.play_button = None
        self.stop_button = None
        self.halves_button = None
        self.quarters_button = None
        self.eighths_button = None
        self.sixteenths_button = None
        self.tempo = None
        self.buttons_pressed = []
        self.is_on_button = None
        self.t_0 = 0
        self.elapsed_time = 0
        self.click_t_0 = 0
        self.click_elapsed_time = 0
        self.is_playing = False
        self.current_subdivision = 1

    def on_show(self):

        arcade.set_background_color(arcade.color.BLUE_YONDER)


    def setup(self):

        self.button_list = arcade.SpriteList()

        self.tempo_up_button = tempo_up_sprite
        self.tempo_up_button.position = SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 100
        self.button_list.append(self.tempo_up_button)

        self.temp_down_button = tempo_down_sprite
        self.temp_down_button.position = SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 100
        self.button_list.append(self.temp_down_button)

        self.play_button = play_sprite
        self.play_button.position = 100, SCREEN_HEIGHT - 100
        self.button_list.append(self.play_button)

        self.stop_button = stop_sprite
        self.stop_button.position = SCREEN_WIDTH - 100, SCREEN_HEIGHT - 100
        self.button_list.append(self.stop_button)

        self.halves_button = halves_sprite
        self.halves_button.position = 100, SUBDIVISION_BUTTONS_Y
        self.button_list.append(self.halves_button)

        self.quarters_button = quarters_sprite
        self.quarters_button.position = 225, SUBDIVISION_BUTTONS_Y
        self.button_list.append(self.quarters_button)

        self.eighths_button = eighths_sprite
        self.eighths_button.position = 350, SUBDIVISION_BUTTONS_Y
        self.button_list.append(self.eighths_button)

        self.sixteenths_button = sixteenths_sprite
        self.sixteenths_button.position = 475, SUBDIVISION_BUTTONS_Y
        self.button_list.append(self.sixteenths_button)


        self.buttons_pressed = []
        self.is_on_button = []


        self.t_0 = time.time()

        self.elapsed_time = (time.time() - self.t_0)

        self.tempo = 60

    def on_draw(self):
        arcade.start_render()

        self.button_list.draw()

        arcade.draw_text(f"Quarter Note = {math.floor(self.tempo)}", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 25, arcade.color.WHITE, 24, anchor_x="center", anchor_y="center")
        arcade.draw_text(f"Current Subdivision = {self.current_subdivision}", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 25, arcade.color.WHITE, 18, anchor_x="center", anchor_y="center")

    def on_update(self, delta_time):
        self.elapsed_time = (time.time() - self.t_0)

        if self.is_playing:
            if self.elapsed_time >= (60 / math.floor(self.tempo) / self.current_subdivision):
                arcade.play_sound(click_sound)
                print(self.elapsed_time)
                self.t_0 = time.time()


        if len(self.buttons_pressed) > 0:
            self.click_elapsed_time = (time.time() - self.click_t_0)
            if 2 > self.click_elapsed_time > 0.5:
                if self.tempo_up_button in self.buttons_pressed:
                    self.tempo += .1
                elif self.temp_down_button in self.buttons_pressed:
                    self.tempo -= .1
            elif self.click_elapsed_time > 2:
                if self.tempo_up_button in self.buttons_pressed:
                    self.tempo += 1
                elif self.temp_down_button in self.buttons_pressed:
                    self.tempo -= 1


    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.buttons_pressed = arcade.get_sprites_at_point((x, y), self.button_list)

            if len(self.buttons_pressed) > 0:

                self.click_t_0 = time.time()
                self.click_elapsed_time = (time.time() - self.click_t_0)

            if self.tempo_up_button in self.buttons_pressed:
                self.tempo += 1
            elif self.temp_down_button in self.buttons_pressed:
                self.tempo -= 1


    def on_mouse_release(self, x: float, y: float, button: int,
                         modifiers: int):

        self.is_on_button = arcade.get_sprites_at_point((x, y), self.button_list)

        if len(self.is_on_button) > 0:

            if self.play_button in self.buttons_pressed and self.play_button in self.is_on_button:
                self.is_playing = True
            elif self.stop_button in self.buttons_pressed and self.stop_button in self.is_on_button:
                self.is_playing = False
            elif self.halves_button in self.buttons_pressed and self.halves_button in self.is_on_button:
                self.current_subdivision = 0.5
            elif self.quarters_button in self.buttons_pressed and self.quarters_button in self.is_on_button:
                self.current_subdivision = 1
            elif self.eighths_button in self.buttons_pressed and self.eighths_button in self.is_on_button:
                self.current_subdivision = 2
            elif self.sixteenths_button in self.buttons_pressed and self.sixteenths_button in self.is_on_button:
                self.current_subdivision = 4

        if len(self.buttons_pressed) > 0:
            self.buttons_pressed = []
            self.click_elapsed_time = 0

    def on_key_press(self, key: int, modifiers: int):
        if key == arcade.key.A:
            game_view = Subdivision_Menu(self)
            self.window.show_view(game_view)


class Subdivision_Menu(arcade.View):

    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view

    def on_show(self):

        arcade.set_background_color(arcade.color.ALIZARIN_CRIMSON)

    def on_draw(self):

        arcade.start_render()

    def on_key_press(self, key: int, modifiers: int):

        if key == arcade.key.S:
            game_view = Metronome()
            #game_view.setup()
            self.window.show_view(game_view)



def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, "Metronome")
    start_view = Metronome()
    start_view.setup()
    window.show_view(start_view)

    arcade.run()

if __name__ == "__main__":
    main()
