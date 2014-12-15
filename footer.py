while True:
    for event in pygame.event.get():
        if event.type == QUIT:
             pygame.quit()
             sys.exit()
