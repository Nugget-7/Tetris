import pygame
from fentry_login import Fentry


def login_screen(screen):
    clock = pygame.time.Clock()
    font_title = pygame.font.SysFont('Arial', 32, bold=True)
    font_label = pygame.font.SysFont('Arial', 18)


    user_field = Fentry(150, 150, 400, 40, place_holder="Usuario", max_len=20)
    pass_field = Fentry(150, 230, 400, 40, place_holder="Contraseña", password=True)
    age_field = Fentry(150, 310, 400, 40, place_holder="Edad", numeric=True, max_len=3)

    fields = [user_field, pass_field, age_field]
    for f in fields:
        f.init()

    running = True
    while running:
        dt = clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            for f in fields:
                f.handle_event(event)

        for f in fields:
            f.update(dt)

        screen.fill((240, 240, 245))
        screen.blit(font_title.render("Iniciar sesión", True, (40, 40, 40)), (220, 70))
        screen.blit(font_label.render("Usuario:", True, (60, 60, 60)), (150, 128))
        screen.blit(font_label.render("Contraseña:", True, (60, 60, 60)), (150, 208))
        screen.blit(font_label.render("Edad:", True, (60, 60, 60)), (150, 288))

        for f in fields:
            f.draw(screen)

        pygame.display.flip()

    return user_field.get_value(), pass_field.get_value(), age_field.get_value()


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((700, 500))
    pygame.display.set_caption("Login")
    result = login_screen(screen)
    print("Resultado:", result)
    pygame.quit()