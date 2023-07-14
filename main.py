from operator import mod
from tkinter import Frame
import pygame, sys, json, random, math

clock = pygame.time.Clock()
finalscreen = pygame.display.set_mode((1500, 1000))
intermediatescreen = pygame.Surface((1500, 1000), pygame.SRCALPHA)

settingsTemp = json.loads(open("presets/control.json", "r").read())
class Blank:
    def __init__(self, information: dict):
        self.OutputFile = information["OutputFile"]
        self.PixelsPerUnit=information["PixelsPerUnit"]
        self.PlayerWidth = information["PlayerWidth"]
        self.PlayerHeight = information["PlayerHeight"]
        self.BackgroundGridSize=information["BackgroundGridSize"]
        self.FloorHeight=information["FloorHeight"]
        self.IndicatorUptime = information["IndicatorUptime"]
        self.SpeedAnimation=information["SpeedAnimation"]
        self.HorizontalAcceleration = information["HorizontalAcceleration"]
        self.HorizontalDragFlat = information["HorizontalDragFlat"]
        self.HorizontalMaxSpeed = information["HorizontalMaxSpeed"]
        self.CoyoteTime = information["CoyoteTime"]
        self.JumpVelocity = information["JumpVelocity"]
        self.Gravity=information["Gravity"]
        self.MinimumForgiveness = information["MinimumForgiveness"]
        self.MaximumForgiveness = information["MaximumForgiveness"]
        self.RespawnMultiplier = information["RespawnMultiplier"]
        self.SongName = information["SongName"]
Settings = Blank(settingsTemp)

PlayerCharacter = pygame.Surface((Settings.PlayerWidth*Settings.PixelsPerUnit, Settings.PlayerHeight*Settings.PixelsPerUnit), pygame.SRCALPHA)
PlayerCharacter.fill((0, 0, 0))
TotalTime = 0
Score = 0
pygame.display.set_caption("Score: 0")
Deaths = ""
PlayerCoordinates = [0, Settings.PlayerHeight]
Moving = [0, 0]
Momentum = [0, 0]
Platforms = [[Settings.HorizontalMaxSpeed**2/(2*(Settings.HorizontalAcceleration-Settings.HorizontalDragFlat))/-2, -0.5*Settings.FloorHeight, Settings.HorizontalMaxSpeed**2/(2*(Settings.HorizontalAcceleration-Settings.HorizontalDragFlat))], [Settings.HorizontalMaxSpeed**2/(2*(Settings.HorizontalAcceleration-Settings.HorizontalDragFlat))/-2, 0, Settings.HorizontalMaxSpeed**2/(2*(Settings.HorizontalAcceleration-Settings.HorizontalDragFlat))]]
OnGround = 0
IndicatorTime = 0
CoyoteTimer = 0

pygame.mixer.init()
pygame.mixer.music.load("Songs/"+Settings.SongName)
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)
# TODO: Download music (First Steps, Elite Fight, First Steps)
try:
# if True:
    while True:
        FrameTime = clock.tick(60)
        TotalTime += FrameTime

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Logs results
                print(1/0)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    Moving[0] = 1
                elif event.key == pygame.K_RIGHT:
                    Moving[1] = 1
                elif event.key == pygame.K_UP:
                    if OnGround or CoyoteTimer > 0:
                        Momentum[1] = Settings.JumpVelocity
                        OnGround = 0
                        CoyoteTimer = 0
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    Moving[0] = 0
                elif event.key == pygame.K_RIGHT:
                    Moving[1] = 0
        
        # Accelerates player
        if Momentum[0] < 0:
            Momentum[0] = min((0, Momentum[0]+Settings.HorizontalDragFlat*FrameTime/1000))
        elif Momentum[0] > 0:
            Momentum[0] = max((0, Momentum[0]-Settings.HorizontalDragFlat*FrameTime/1000))
        if Moving[0]:
            Momentum[0] = max((Momentum[0]-Settings.HorizontalAcceleration*FrameTime/1000, Settings.HorizontalMaxSpeed*-1))
        if Moving[1]:
            Momentum[0] = min((Momentum[0]+Settings.HorizontalAcceleration*FrameTime/1000, Settings.HorizontalMaxSpeed))
        if not OnGround:
            Momentum[1] -= Settings.Gravity*FrameTime/1000

        # Lands on a platform
        if Momentum[1] < 0:
            if PlayerCoordinates[1] >= Platforms[0][1] and PlayerCoordinates[1]+Momentum[1]*FrameTime/1000 <= Platforms[0][1]:
                tempa = PlayerCoordinates[0]+Momentum[0]*(Platforms[0][1]-PlayerCoordinates[1])/(Momentum[1])
                if tempa >= Platforms[0][0] and tempa <= Platforms[0][0]+Platforms[0][2]:
                    OnGround = 1
                    PlayerCoordinates[1] = Platforms[0][1]
                    Momentum[1] = 0
            if PlayerCoordinates[1] > Platforms[1][1] and PlayerCoordinates[1]+Momentum[1]*FrameTime/1000 <= Platforms[1][1]:
                tempa = PlayerCoordinates[0]+Momentum[0]*(Platforms[1][1]-PlayerCoordinates[1])/(Momentum[1])
                if tempa >= Platforms[1][0] and tempa <= Platforms[1][0]+Platforms[1][2]:
                    OnGround = 1
                    PlayerCoordinates[1] = Platforms[1][1]
                    Momentum[1] = 0
                    # Moves the platform
                    pygame.display.set_caption("Score: "+str(Score))
                    Score += 1
                    temp3 = random.randint(math.floor(Settings.HorizontalMaxSpeed**2/(2*(Settings.HorizontalAcceleration-Settings.HorizontalDragFlat))+Settings.MinimumForgiveness), math.floor(Settings.HorizontalMaxSpeed**2/(2*(Settings.HorizontalAcceleration-Settings.HorizontalDragFlat))+Settings.MaximumForgiveness))
                    # Moves the platform
                    tempa = random.randint(1, math.floor(8*(Settings.JumpVelocity/Settings.Gravity)))/4
                    if tempa < Settings.JumpVelocity/Settings.Gravity:
                        temp1 = random.randint(math.ceil(Platforms[1][0]-temp3-tempa*Settings.HorizontalMaxSpeed), math.floor(Platforms[1][0]+Platforms[1][2]+tempa*Settings.HorizontalMaxSpeed))
                        temp2 = random.randint(math.floor(Platforms[1][1]+(Settings.JumpVelocity**2/Settings.Gravity)/4), math.floor(Platforms[1][1]+(Settings.JumpVelocity**2/Settings.Gravity)/2))
                    else:
                        temp2 = random.randint(math.floor(Platforms[1][1]+Settings.JumpVelocity*tempa-Settings.Gravity*(tempa**2)/2-Settings.MaximumForgiveness), math.floor(Platforms[1][1]+Settings.JumpVelocity*tempa-Settings.Gravity*(tempa**2)/2-Settings.MinimumForgiveness))
                        tempb = random.randint(0, 1)
                        if tempb == 0:
                            temp1 = random.randint(math.ceil(Platforms[1][0]-temp3-tempa*Settings.HorizontalMaxSpeed+Settings.MinimumForgiveness), math.ceil(Platforms[1][0]-temp3-tempa*Settings.HorizontalMaxSpeed+Settings.MaximumForgiveness))
                        else:
                            temp1 = random.randint(math.ceil(Platforms[1][0]+Platforms[1][2]+tempa*Settings.HorizontalMaxSpeed-Settings.MaximumForgiveness), math.ceil(Platforms[1][0]+Platforms[1][2]+tempa*Settings.HorizontalMaxSpeed-Settings.MinimumForgiveness))
                    Platforms.append((temp1, temp2, temp3))
                    Platforms.pop(0)
                    IndicatorTime = Settings.IndicatorUptime




        # Moves player
        PlayerCoordinates[0] += Momentum[0]*FrameTime/1000
        PlayerCoordinates[1] += Momentum[1]*FrameTime/1000

        # Makes player fall off of platform
        if OnGround:
            if Momentum[0] < 0:
                if PlayerCoordinates[0] < Platforms[0][0]:
                    OnGround = 0
                    CoyoteTimer = Settings.CoyoteTime
            elif Momentum[0] > 0:
                if PlayerCoordinates[0] > Platforms[0][0]+Platforms[0][2]:
                    OnGround = 0
                    CoyoteTimer = Settings.CoyoteTime
        # Makes player respawn
        if Momentum[1] <= -Settings.RespawnMultiplier*Settings.Gravity:
            Momentum = [0, 0]
            PlayerCoordinates = [Platforms[0][0]+Platforms[0][2]/2, Platforms[0][1]+Settings.PlayerHeight]
            if Deaths != "":
                Deaths += ";"
            Deaths += str(Score)

        if CoyoteTimer > 0:
            CoyoteTimer -= FrameTime/1000

        # Draws background grid
        intermediatescreen.fill((155, 155, 155))
        tempa = -2*Settings.BackgroundGridSize+mod(PlayerCoordinates[1], Settings.BackgroundGridSize*2)
        tempc = 0
        while tempa*Settings.PixelsPerUnit < 1000:
            if tempc:
                tempc = 0
                tempb = -2*Settings.BackgroundGridSize-mod(PlayerCoordinates[0], Settings.BackgroundGridSize*2)
            else:
                tempc = 1
                tempb = -3*Settings.BackgroundGridSize-mod(PlayerCoordinates[0], Settings.BackgroundGridSize*2)
            while tempb*Settings.PixelsPerUnit < 1500:
                pygame.draw.rect(intermediatescreen, (180, 180, 180), (tempb*Settings.PixelsPerUnit, tempa*Settings.PixelsPerUnit, Settings.BackgroundGridSize*Settings.PixelsPerUnit, Settings.BackgroundGridSize*Settings.PixelsPerUnit))
                tempb += Settings.BackgroundGridSize*2
            tempa += Settings.BackgroundGridSize

        # Draws indicator lines
        if IndicatorTime > 0:
            IndicatorTime -= FrameTime/1000
            pygame.draw.line(intermediatescreen, (60, 50, 50), ((Platforms[0][0]+Settings.PlayerWidth/2-PlayerCoordinates[0])*Settings.PixelsPerUnit+750, (PlayerCoordinates[1]-Platforms[0][1]+Settings.PlayerHeight/2)*Settings.PixelsPerUnit+500), ((Platforms[1][0]+Settings.PlayerWidth/2-PlayerCoordinates[0])*Settings.PixelsPerUnit+750, (PlayerCoordinates[1]-Platforms[1][1]+Settings.PlayerHeight/2)*Settings.PixelsPerUnit+500), Settings.PixelsPerUnit)
            pygame.draw.line(intermediatescreen, (60, 50, 50), ((Platforms[0][0]-Settings.PlayerWidth/2-PlayerCoordinates[0]+Platforms[0][2])*Settings.PixelsPerUnit+750, (PlayerCoordinates[1]-Platforms[0][1]+Settings.PlayerHeight/2)*Settings.PixelsPerUnit+500), ((Platforms[1][0]-Settings.PlayerWidth/2-PlayerCoordinates[0]+Platforms[1][2])*Settings.PixelsPerUnit+750, (PlayerCoordinates[1]-Platforms[1][1]+Settings.PlayerHeight/2)*Settings.PixelsPerUnit+500), Settings.PixelsPerUnit)
            pygame.draw.line(intermediatescreen, (60, 50, 50), ((Platforms[0][0]+Settings.PlayerWidth/2-PlayerCoordinates[0])*Settings.PixelsPerUnit+750, (PlayerCoordinates[1]-Platforms[0][1]+Settings.PlayerHeight/2+Settings.FloorHeight)*Settings.PixelsPerUnit+500), ((Platforms[1][0]+Settings.PlayerWidth/2-PlayerCoordinates[0])*Settings.PixelsPerUnit+750, (PlayerCoordinates[1]-Platforms[1][1]+Settings.PlayerHeight/2+Settings.FloorHeight)*Settings.PixelsPerUnit+500), Settings.PixelsPerUnit)
            pygame.draw.line(intermediatescreen, (60, 50, 50), ((Platforms[0][0]-Settings.PlayerWidth/2-PlayerCoordinates[0]+Platforms[0][2])*Settings.PixelsPerUnit+750, (PlayerCoordinates[1]-Platforms[0][1]+Settings.PlayerHeight/2+Settings.FloorHeight)*Settings.PixelsPerUnit+500), ((Platforms[1][0]-Settings.PlayerWidth/2-PlayerCoordinates[0]+Platforms[1][2])*Settings.PixelsPerUnit+750, (PlayerCoordinates[1]-Platforms[1][1]+Settings.PlayerHeight/2+Settings.FloorHeight)*Settings.PixelsPerUnit+500), Settings.PixelsPerUnit)

        # Draws platforms
        pygame.draw.rect(intermediatescreen, (60, 50, 50), ((Platforms[0][0]+Settings.PlayerWidth/2-PlayerCoordinates[0])*Settings.PixelsPerUnit+750, (PlayerCoordinates[1]-Platforms[0][1]+Settings.PlayerHeight/2)*Settings.PixelsPerUnit+500, (Platforms[0][2]-Settings.PlayerWidth)*Settings.PixelsPerUnit, Settings.FloorHeight*Settings.PixelsPerUnit))
        pygame.draw.rect(intermediatescreen, (50, 35, 35), ((Platforms[1][0]+Settings.PlayerWidth/2-PlayerCoordinates[0])*Settings.PixelsPerUnit+750, (PlayerCoordinates[1]-Platforms[1][1]+Settings.PlayerHeight/2)*Settings.PixelsPerUnit+500, (Platforms[1][2]-Settings.PlayerWidth)*Settings.PixelsPerUnit, Settings.FloorHeight*Settings.PixelsPerUnit))

        # Draws player
        if Settings.SpeedAnimation != 0:
            PlayerCharacter.set_alpha(40)
            intermediatescreen.blit(PlayerCharacter, (750-Settings.PlayerWidth*Settings.PixelsPerUnit/2-Momentum[0]*Settings.PixelsPerUnit*3*Settings.SpeedAnimation, 500-Settings.PlayerHeight*Settings.PixelsPerUnit/2+Momentum[1]*Settings.PixelsPerUnit*3*Settings.SpeedAnimation))
            PlayerCharacter.set_alpha(110)
            intermediatescreen.blit(PlayerCharacter, (750-Settings.PlayerWidth*Settings.PixelsPerUnit/2-Momentum[0]*Settings.PixelsPerUnit*2*Settings.SpeedAnimation, 500-Settings.PlayerHeight*Settings.PixelsPerUnit/2+Momentum[1]*Settings.PixelsPerUnit*2*Settings.SpeedAnimation))
            PlayerCharacter.set_alpha(190)
            intermediatescreen.blit(PlayerCharacter, (750-Settings.PlayerWidth*Settings.PixelsPerUnit/2-Momentum[0]*Settings.PixelsPerUnit*Settings.SpeedAnimation, 500-Settings.PlayerHeight*Settings.PixelsPerUnit/2+Momentum[1]*Settings.PixelsPerUnit*Settings.SpeedAnimation))
            PlayerCharacter.set_alpha(255)
        intermediatescreen.blit(PlayerCharacter, (750-Settings.PlayerWidth*Settings.PixelsPerUnit/2, 500-Settings.PlayerHeight*Settings.PixelsPerUnit/2))



        finalscreen.blit(intermediatescreen, (0, 0))
        pygame.display.update()
except:
    # print(vars(Settings).values())
    # print(1/0)
    try:
        open("Records/"+Settings.OutputFile, "x")
    except:
        pass
    tempa = str(vars(Settings).values())
    tempb = [TotalTime, Score, Deaths, tempa[13:len(tempa)-2]]
    tempb = str(tempb).replace("'", "").replace('"', "").replace(", ", ",")
    tempb = tempb[1:len(tempb)-1]
    open("Records/"+Settings.OutputFile, "a").write(str(tempb)+"\n")
