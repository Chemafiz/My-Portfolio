import cv2
import pickle
import pygame
import sys
from pygame.locals import *
from brush import Brush
from window import Menu


def main():
    menu = Menu((800, 600), (255, 255, 255), 60, "Digits predict")
    menu.reset_button = pygame.image.load(r"C:\Users\Laptop\Desktop\Python projects\rozpoznawanie liczb\reset_button.jpg")
    menu.predict_button = pygame.image.load(r"C:\Users\Laptop\Desktop\Python projects\rozpoznawanie liczb\predict_button.jpg")
    menu.reset_button_pos = (25, 50)
    menu.predict_button_pos = (25, 200)

    pygame.init()
    pygame.font.init()
    pygame.display.set_caption(menu.title)
    clock = pygame.time.Clock()
    window = pygame.display.set_mode(menu.window_size)

    my_font = pygame.font.SysFont('Calibri', 30, bold=pygame.font.Font.bold)
    text1 = my_font.render("PREDICTED", False, (0, 0, 0))
    text2 = my_font.render("DIGIT:", False, (0, 0, 0))
    prediction_text = my_font.render("", False, (0, 0, 0))

    brush = Brush(30)
    state = False
    predict = False
    loaded_model = pickle.load(open('model.pickle', 'rb'))
    while True:
        window.fill(menu.background_color)
        mouse_position =  pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and mouse_position[0] > 230:
                state = True
            elif event.type == pygame.MOUSEBUTTONDOWN \
                    and menu.reset_button_pos[0] <= mouse_position[0] <= (menu.reset_button_pos[0] + 150) \
                    and menu.reset_button_pos[1] <= mouse_position[1] <= (menu.reset_button_pos[1] + 100):
                brush.pixels.clear()
                prediction_text = my_font.render("", False, (0, 0, 0))
            elif event.type == pygame.MOUSEBUTTONDOWN \
                    and menu.predict_button_pos[0] <= mouse_position[0] <= (menu.predict_button_pos[0] + 150) \
                    and menu.predict_button_pos[1] <= mouse_position[1] <= (menu.predict_button_pos[1] + 100):
                predict = True
            if event.type == pygame.MOUSEBUTTONUP:
                state = False

        if state:
            brush.draw(mouse_position)
        brush.print_brush(window)
        pygame.draw.line(window, (0, 0, 0), (200, 0), (200, 600), 4)
        if predict:
            prediction_text = digit_recognition(window, loaded_model, my_font)
            predict = False

        pygame.draw.line(window, (0, 0, 0), (200, 0), (200, 600), 4)
        window.blit(menu.reset_button, menu.reset_button_pos)
        window.blit(menu.predict_button, menu.predict_button_pos)
        window.blit(text1, (25, 400))
        window.blit(text2, (60, 425))
        window.blit(prediction_text, (90, 450))

        pygame.display.update()
        clock.tick(menu.fps)


def digit_recognition(window, loaded_model, my_font):
    rect = pygame.Rect(215, 0, 585, 600)
    sub = window.subsurface(rect)
    pygame.image.save(sub, "screenshot.jpg")

    image = cv2.imread("screenshot.jpg", 0)
    down_points = (28, 28)
    image_resized = cv2.resize(image, down_points, interpolation=cv2.INTER_AREA)
    image_final = abs(image_resized - [255])
    cv2.imwrite("resized.jpg", image_resized)

    image_vector = image_final.reshape(1, -1)
    digit = loaded_model.predict(image_vector)
    return my_font.render(f'{digit[0]}', False, (0, 0, 0))


if __name__ == "__main__":
    main()


