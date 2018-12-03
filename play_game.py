import pygame
from util import displayText, button
import characters

QUIT = False
black = (0, 0, 0)
white = (255, 255, 255)
green = (100, 200, 100)
red = (200, 0, 0)
hoverred = (230, 0, 0)
yellow = (180, 180, 0)
hoveryellow = (200, 200, 0)
display_width, display_height = 2000, 1000
clock = pygame.time.Clock()
gameDisplay = pygame.display.set_mode((display_width, display_height))


background = pygame.image.load('images/game_background.jpg')
background = pygame.transform.scale(background, (2000, 1000))
arrow = pygame.image.load('images/arrow.png')
arrow = pygame.transform.scale(arrow, (150, 100))
stand = pygame.image.load('images/stand.png')
stand = pygame.transform.scale(stand, (500,500))
merchant = pygame.image.load('images/merchant.png')
merchant = pygame.transform.scale(merchant, (125, 200))


playerGroup = pygame.sprite.Group()
player = characters.Player()
playerGroup.add(player)
enemyGroup = pygame.sprite.Group()
bulletGroup = pygame.sprite.Group()
ledgeGroup = pygame.sprite.Group()
enemyBulletGroup = pygame.sprite.Group()
keys = pygame.key.get_pressed()


def playGame():
    play = True
    levelCounter = 1
    #transition = True
    while play:     
        menu_state = logic(background, False, levelCounter)

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    play = False
            if event.type == pygame.QUIT:
                return True
        # IF the level counter > 1 then add pick ups
        if (player.rect.x > display_width):
            if (levelCounter == 1):
                bulletGroup.empty()
                enemyBulletGroup.empty()
                level(1, levelCounter, 'images/light_background.png', False, 0)
            elif (levelCounter == 2):
                level(2, levelCounter, 'images/medium_background.png', False, 0)
            elif (levelCounter == 3):
                level(1, levelCounter, 'images/city_background.png', True, 1)
            elif (levelCounter == 4):
                level(1, levelCounter, 'images/misty_background.jpg', True, 1)
            elif (levelCounter == 5):
                level(1, levelCounter, 'images/game_background.jpg', True, 1)
            levelCounter += 1
            player.rect.x = 0
            bulletGroup.empty()
            ledgeGroup.empty()
            enemyBulletGroup.empty()
        if menu_state == True:
            play = False


def logic(bkgd, playing, level_count):
    gameDisplay.blit(bkgd, (0, 0))
    back2menu = False
    if playing:
        if player.shot == True:
            bullet = characters.Bullet(player.rect.x, player.rect.y, player.facing, player.location)
            bulletGroup.add(bullet)
            player.canShoot = False
            player.ammo -= 1
        pygame.sprite.groupcollide(bulletGroup, ledgeGroup, True, False)
        hitList = pygame.sprite.groupcollide(bulletGroup, enemyGroup, True, False)
        for bull in hitList:
            for enmy in hitList[bull]:
                enmy.health -= bull.damage
        for enemy in enemyGroup.sprites():
            if enemy.shot == True:
                enemyBullet = characters.enemyBullet(player.rect.x, player.rect.y, enemy.facing, enemy.rect.x, enemy.rect.y)
                enemyBulletGroup.add(enemyBullet)
                enemy.shot = False
            if enemy.alive == False:
                enemy.remove(enemyGroup)
        for bullet in bulletGroup.sprites():
            if bullet.alive == False:
                bulletGroup.remove(bullet)
        if pygame.sprite.groupcollide(enemyBulletGroup, playerGroup, True, False):
            player.health -= 10

    else:
        gameDisplay.blit(merchant, (3*display_width / 5, characters.floor))
        gameDisplay.blit(stand, (display_width / 3, characters.floor - 300))



    #UPDATE
    playerGroup.update()
    enemyGroup.update()
    bulletGroup.update()
    ledgeGroup.update()
    enemyBulletGroup.update()

    #DRAW
    playerGroup.draw(gameDisplay)
    enemyGroup.draw(gameDisplay)
    bulletGroup.draw(gameDisplay)
    ledgeGroup.draw(gameDisplay)
    enemyBulletGroup.draw(gameDisplay)

    pygame.draw.rect(gameDisplay, black, ((0, 0), (display_width, display_height / 15)))
    healthString = str("Health: " + str(player.health) + "/100")
    ammoString = str("Ammo: " + str(player.ammo) + "/100")
    displayText(healthString, 'fonts/Antonio-Regular.ttf', 30, 100, 30, white, 25)
    displayText(ammoString , 'fonts/Antonio-Regular.ttf', 30, 500, 30, white, 25)

    if playing:
        if (len(enemyGroup.sprites()) == 0):
            displayText("LEVEL COMPLETE", 'fonts/Antonio-Bold.ttf', 75, display_width / 2, display_height / 4, black, 50)
            displayText("Next stage", 'fonts/Antonio-Bold.ttf', 30, display_width - 75, characters.floor - 70, black, 15)
            gameDisplay.blit(arrow, (display_width - 150, characters.floor - 60))
        enemyString = str('Enemies remaining: ' + str(len(enemyGroup.sprites())))
        levelString = str('Level: ' + str(level_count))
        displayText(enemyString, 'fonts/Antonio-Regular.ttf', 30, 1850, 30, white, 20)
        displayText(levelString, 'fonts/Antonio-Regular.ttf', 40, display_width / 2, 30, white, 20)
    else:
        startString = str('Level ' + str(level_count))
        displayText(startString, 'fonts/Antonio-Bold.ttf', 30, display_width - 75, characters.floor - 70, black, 15)
        gameDisplay.blit(arrow, (display_width - 150, characters.floor - 60))
        back2menu = False
        back2menu = button("Main Menu (m)", 'fonts/Antonio-Regular.ttf', 40, white, red, hoverred, 1875, 970, 25, back2menu)


    pygame.display.update()

    if back2menu == False:
        return True



def level(num_enemy, level_num, background, isLedge, num_ledge_enemies):
    for i in range(num_enemy):
        enemy = characters.Enemy()
        enemyGroup.add(enemy)
    if isLedge:
        ledge = characters.Ledge()
        ledgeGroup.add(ledge)
    for j in range(num_ledge_enemies):
        ledge_enemy = characters.ledgeEnemy()
        enemyGroup.add(ledge_enemy)
    level_bkgd = pygame.image.load(background)
    level_bkgd = pygame.transform.scale(level_bkgd, (2000, 1000))
    player.rect.x = 0
    while True:
        logic(level_bkgd, True, level_num)
        #pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    play = False
            if event.type == pygame.QUIT:
                pygame.quit()
        if (player.rect.x >= display_width) and (len(enemyGroup.sprites()) == 0):
            break
        elif (player.rect.x >= (display_width - player.size)) and (len(enemyGroup.sprites()) > 0):
            player.rect.x = display_width - player.size
