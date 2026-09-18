import pygame, math, random

pygame.init()
pygame.display.set_caption("F1 Cockpit Racer")
WIDTH, HEIGHT = 1100, 660
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

FONT_XS = pygame.font.SysFont("arial", 12, bold=True)
FONT_S  = pygame.font.SysFont("arial", 14, bold=True)
FONT    = pygame.font.SysFont("arial", 18, bold=True)
FONT_M  = pygame.font.SysFont("arial", 22, bold=True)
FONT_L  = pygame.font.SysFont("arial", 30, bold=True)
FONT_XL = pygame.font.SysFont("arial", 64, bold=True)
FONT_XXL= pygame.font.SysFont("arial", 92, bold=True)

# ===================== WORLD CONSTANTS =====================
SEGMENT_LENGTH = 200
RUMBLE_LENGTH = 3
ROAD_WIDTH = 2200
LANES = 3
DRAW_DISTANCE = 200
FIELD_OF_VIEW = 100
CAMERA_HEIGHT = 1200
FOG_DENSITY = 4.0
CENTRIFUGAL = 0.32

cameraDepth = 1.0 / math.tan((FIELD_OF_VIEW / 2) * math.pi / 180)
playerZ = CAMERA_HEIGHT * cameraDepth
maxSpeed = SEGMENT_LENGTH * 60
accel = maxSpeed / 5
breaking = -maxSpeed
decel = -maxSpeed / 5
offRoadDecel = -maxSpeed / 2
offRoadLimit = maxSpeed / 4
SPRITE_SCALE = 0.3 / 120.0

# ===================== RACE MODES =====================
RACE_MODES = [
    {'id':'quick',  'name':'Быстрая гонка', 'laps':3, 'opponents':19, 'special':None,
     'desc':'3 круга · 19 соперников · классика'},
    {'id':'sprint', 'name':'Спринт',        'laps':1, 'opponents':19, 'special':'aggressive',
     'desc':'1 круг · все атакуют без пощады'},
    {'id':'gp',     'name':'Гран-при',      'laps':5, 'opponents':19, 'special':'aggressive',
     'desc':'5 кругов · длинная гонка'},
    {'id':'elim',   'name':'На выбывание',  'laps':6, 'opponents':19, 'special':'elimination',
     'desc':'6 кругов · последний вылетает каждый круг'},
    {'id':'time',   'name':'Тайм-триал',    'laps':3, 'opponents':0,  'special':'timetrial',
     'desc':'3 круга · ты один · цель — лучший круг'},
    {'id':'champ',  'name':'Чемпионат',     'laps':3, 'opponents':19, 'special':'championship',
     'desc':'5 разных трасс · очки за позиции'},
]
CHAMP_POINTS = [25, 18, 15, 12, 10, 8, 6, 4, 2, 1]
CHAMP_ROUNDS = 5

# ===================== THEMES =====================
THEMES = {
    'grass': {
        'grass': (18, 122, 42), 'grass_dark': (14, 100, 34),
        'road': (112, 112, 118), 'road_dark': (98, 98, 104),
        'rumble': (238, 238, 240), 'rumble_dark': (198, 28, 28),
        'sky_top': (58, 106, 178), 'sky_bot': (196, 220, 238),
        'fog': (150, 185, 220),
        'leaf': (52, 142, 62), 'leaf_dark': (36, 112, 48),
        'ui': (80, 200, 120), 'badge': (60, 160, 80),
    },
    'desert': {
        'grass': (216, 186, 128), 'grass_dark': (196, 166, 108),
        'road': (120, 110, 100), 'road_dark': (105, 95, 85),
        'rumble': (240, 230, 200), 'rumble_dark': (180, 80, 60),
        'sky_top': (200, 140, 80), 'sky_bot': (250, 220, 160),
        'fog': (230, 200, 150),
        'leaf': (120, 130, 60), 'leaf_dark': (90, 100, 45),
        'ui': (230, 170, 70), 'badge': (210, 160, 70),
    },
    'snow': {
        'grass': (232, 238, 246), 'grass_dark': (210, 220, 235),
        'road': (100, 100, 110), 'road_dark': (88, 88, 98),
        'rumble': (255, 255, 255), 'rumble_dark': (180, 60, 60),
        'sky_top': (120, 150, 190), 'sky_bot': (222, 232, 246),
        'fog': (210, 220, 235),
        'leaf': (40, 80, 60), 'leaf_dark': (26, 60, 42),
        'ui': (140, 200, 255), 'badge': (150, 200, 240),
    },
    'night': {
        'grass': (18, 32, 24), 'grass_dark': (12, 24, 18),
        'road': (60, 60, 68), 'road_dark': (48, 48, 56),
        'rumble': (200, 200, 210), 'rumble_dark': (160, 20, 20),
        'sky_top': (6, 8, 24), 'sky_bot': (28, 32, 60),
        'fog': (30, 35, 55),
        'leaf': (18, 46, 26), 'leaf_dark': (10, 30, 16),
        'ui': (140, 140, 240), 'badge': (90, 90, 180),
    },
    'sunset': {
        'grass': (140, 100, 60), 'grass_dark': (118, 84, 50),
        'road': (105, 92, 82), 'road_dark': (90, 78, 70),
        'rumble': (240, 200, 180), 'rumble_dark': (180, 80, 60),
        'sky_top': (230, 100, 70), 'sky_bot': (252, 200, 130),
        'fog': (230, 165, 125),
        'leaf': (70, 44, 32), 'leaf_dark': (48, 30, 22),
        'ui': (255, 150, 70), 'badge': (220, 120, 70),
    },
    'city': {
        'grass': (100, 100, 105), 'grass_dark': (85, 85, 92),
        'road': (72, 72, 80), 'road_dark': (58, 58, 66),
        'rumble': (240, 240, 245), 'rumble_dark': (200, 40, 40),
        'sky_top': (80, 100, 140), 'sky_bot': (180, 190, 210),
        'fog': (155, 165, 190),
        'leaf': (60, 90, 60), 'leaf_dark': (40, 60, 40),
        'ui': (200, 210, 240), 'badge': (130, 140, 170),
    },
}
THEME_LABELS = {
    'grass': 'Трава', 'desert': 'Пустыня', 'snow': 'Снег',
    'night': 'Ночь', 'sunset': 'Закат', 'city': 'Город',
}

# ===================== TEAMS & DRIVERS =====================
TEAMS = [
    {'id':'rosso',  'name':'Rosso Corsa',    'short':'RSC',
     'primary':(220,30,40),   'secondary':(255,220,60),  'accent':(255,255,255), 'style':0,
     'drivers':[('К. Маркетти',16), ('Л. Бьянки',55)]},
    {'id':'silver', 'name':'Silver Arrows',  'short':'SLV',
     'primary':(200,205,215), 'secondary':(20,20,25),    'accent':(0,200,200),   'style':1,
     'drivers':[('К. Восс',44), ('Х. Хартманн',77)]},
    {'id':'energy', 'name':'Energy Racing',  'short':'ENR',
     'primary':(15,30,90),    'secondary':(220,40,40),   'accent':(255,220,60),  'style':2,
     'drivers':[('М. Янсен',1), ('П. Петерс',11)]},
    {'id':'papaya', 'name':'Papaya GP',      'short':'PAP',
     'primary':(255,120,20),  'secondary':(20,30,50),    'accent':(80,220,255),  'style':3,
     'drivers':[('Т. Блейк',4), ('Й. Соренсен',81)]},
    {'id':'azure',  'name':'Azure Racing',   'short':'AZR',
     'primary':(30,90,200),   'secondary':(240,80,160),  'accent':(255,255,255), 'style':0,
     'drivers':[('П. Дюбуа',31), ('А. Лоран',10)]},
    {'id':'emerald','name':'Emerald Works',  'short':'EMW',
     'primary':(15,90,60),    'secondary':(220,200,60),  'accent':(255,255,255), 'style':1,
     'drivers':[('Я. Новак',5), ('Р. Коста',24)]},
    {'id':'bee',    'name':'Yellow Bee',     'short':'BEE',
     'primary':(250,210,20),  'secondary':(30,30,35),    'accent':(30,30,35),    'style':2,
     'drivers':[('С. Руис',14), ('В. Чен',22)]},
    {'id':'wave',   'name':'Cyan Wave',      'short':'CYW',
     'primary':(20,190,210),  'secondary':(15,25,55),    'accent':(255,255,255), 'style':3,
     'drivers':[('Д. Иванов',23), ('Ю. Сато',47)]},
    {'id':'rose',   'name':'Rose Power',     'short':'RSW',
     'primary':(240,90,160),  'secondary':(255,255,255), 'accent':(30,30,35),    'style':0,
     'drivers':[('А. Мендес',18), ('К. Ковальски',99)]},
    {'id':'night',  'name':'Night Motorsport','short':'NGT',
     'primary':(25,25,30),    'secondary':(220,180,40),  'accent':(220,180,40),  'style':1,
     'drivers':[('Ф. Вагнер',7), ('О. Оконкво',63)]},
]

# ===================== HELPERS =====================
def lerp_color(c1, c2, t):
    return (int(c1[0]+(c2[0]-c1[0])*t),
            int(c1[1]+(c2[1]-c1[1])*t),
            int(c1[2]+(c2[2]-c1[2])*t))
def fog_color(color, fog): return lerp_color(CURRENT_FOG, color, fog)
def exponential_fog(d, density): return 1.0 / math.pow(math.e, d*d*density)
def interpolate(a,b,p): return a + (b-a)*p
def accelerate(v,a,dt): return v + a*dt
def ease_in(a,b,p): return a + (b-a)*p*p
def ease_in_out(a,b,p): return a + (b-a)*(-math.cos(p*math.pi)/2 + 0.5)
def clamp(v,lo,hi): return lo if v<lo else (hi if v>hi else v)
def format_time(t):
    m = int(t//60); s = t - m*60
    return f"{m}:{s:06.3f}"
def darken(c, d=70): return tuple(max(0, v-d) for v in c)

# ===================== CAR SPRITE =====================
def make_car_sprite(team, driver_num=None, style=None):
    if style is None: style = team['style']
    primary   = team['primary']
    secondary = team['secondary']
    accent    = team['accent']
    dark      = darken(primary, 75)
    w, h = 120, 90
    s = pygame.Surface((w, h), pygame.SRCALPHA)
    for tx in (4, 84):
        pygame.draw.rect(s, (28,28,30), (tx, 22, 32, 22), border_radius=6)
        pygame.draw.rect(s, (78,78,84), (tx, 22, 32, 22), 2, border_radius=6)
        pygame.draw.rect(s, (140,140,148), (tx+8, 26, 16, 8), border_radius=3)
    for tx in (0, 88):
        pygame.draw.rect(s, (28,28,30), (tx, 54, 32, 34), border_radius=8)
        pygame.draw.rect(s, (78,78,84), (tx, 54, 32, 34), 2, border_radius=8)
        pygame.draw.rect(s, (140,140,148), (tx+8, 62, 16, 12), border_radius=3)
    pygame.draw.rect(s, primary, (14, 4, 92, 13), border_radius=3)
    pygame.draw.rect(s, dark,   (14, 4, 92, 5), border_radius=3)
    pygame.draw.rect(s, accent, (14, 15, 92, 3))
    pygame.draw.rect(s, dark, (4, 0, 12, 26), border_radius=3)
    pygame.draw.rect(s, dark, (104, 0, 12, 26), border_radius=3)
    pygame.draw.polygon(s, primary, [(52,18),(68,18),(78,60),(42,60)])
    if style == 0:
        pygame.draw.polygon(s, secondary, [(57,18),(63,18),(66,60),(54,60)])
    elif style == 1:
        pygame.draw.polygon(s, secondary, [(52,18),(56,18),(48,60),(42,60)])
        pygame.draw.polygon(s, secondary, [(64,18),(68,18),(78,60),(72,60)])
    elif style == 2:
        pygame.draw.polygon(s, secondary, [(52,18),(60,18),(60,60),(42,60)])
    elif style == 3:
        pygame.draw.polygon(s, secondary, [(52,18),(57,18),(60,42),(42,60)])
        pygame.draw.polygon(s, secondary, [(63,18),(68,18),(78,60),(60,42)])
    pygame.draw.polygon(s, primary, [(44,55),(76,55),(84,88),(36,88)])
    pygame.draw.polygon(s, dark,    [(44,55),(52,55),(48,88),(36,88)])
    if style in (0, 3):
        pygame.draw.rect(s, secondary, (48, 64, 6, 20))
        pygame.draw.rect(s, secondary, (66, 64, 6, 20))
    if style == 2:
        pygame.draw.polygon(s, secondary, [(44,55),(60,55),(60,88),(36,88)])
    pygame.draw.circle(s, accent, (60, 42), 14)
    pygame.draw.circle(s, dark,   (60, 42), 14, 3)
    pygame.draw.ellipse(s, (25,25,60), (48, 35, 24, 13))
    pygame.draw.rect(s, primary, (22, 82, 76, 8), border_radius=2)
    pygame.draw.rect(s, dark,    (22, 84, 76, 4))
    pygame.draw.rect(s, accent,  (22, 82, 76, 2))
    if driver_num is not None:
        try:
            nf = pygame.font.SysFont("arial", 20, bold=True)
            ns = nf.render(str(driver_num), True, accent)
            s.blit(ns, (60 - ns.get_width()//2, 62))
        except Exception:
            pass
    return s

# ===================== ENVIRONMENT SPRITES =====================
def make_tree(kind, theme_key):
    t = THEMES[theme_key]
    w, h = 180, 260
    s = pygame.Surface((w, h), pygame.SRCALPHA)
    trunk = (78, 54, 34)
    if kind == 'conifer':
        pygame.draw.rect(s, trunk, (w//2-8, 190, 16, 70))
        for y, sz in [(30, 88), (90, 108), (150, 128)]:
            pygame.draw.polygon(s, t['leaf_dark'], [(w//2, y), (w//2-sz, y+80), (w//2+sz, y+80)])
            pygame.draw.polygon(s, t['leaf'],      [(w//2, y+10), (w//2-sz+10, y+80), (w//2+sz-10, y+80)])
    elif kind == 'round':
        pygame.draw.rect(s, trunk, (w//2-9, 150, 18, 110))
        pygame.draw.ellipse(s, t['leaf_dark'], (10, 15, w-20, 170))
        pygame.draw.ellipse(s, t['leaf'],      (30, 30, w-60, 140))
        bright = tuple(min(255, c+30) for c in t['leaf'])
        pygame.draw.ellipse(s, bright, (50, 45, w-100, 100))
    elif kind == 'poplar':
        pygame.draw.rect(s, trunk, (w//2-6, 200, 12, 60))
        pygame.draw.ellipse(s, t['leaf_dark'], (w//2-40, 10, 80, 220))
        pygame.draw.ellipse(s, t['leaf'],      (w//2-30, 20, 60, 200))
    elif kind == 'palm':
        pygame.draw.rect(s, (130, 95, 55), (w//2-7, 90, 14, 170))
        for ang in (-80, -55, -30, 0, 30, 55, 80, 110, 130):
            r = math.radians(ang - 90)
            ex = w//2 + int(95*math.cos(r))
            ey = 80 + int(80*math.sin(r))
            pygame.draw.polygon(s, t['leaf_dark'],
                [(w//2, 90), (ex-6, ey+4), (ex+6, ey+4)])
            pygame.draw.polygon(s, t['leaf'],
                [(w//2, 88), (ex-3, ey+2), (ex+3, ey+2)])
    elif kind == 'snowpine':
        pygame.draw.rect(s, (60, 45, 35), (w//2-7, 190, 14, 70))
        for y, sz in [(30, 88), (90, 108), (150, 128)]:
            pygame.draw.polygon(s, (40, 80, 60), [(w//2, y), (w//2-sz, y+80), (w//2+sz, y+80)])
            pygame.draw.polygon(s, (240, 248, 255),
                [(w//2, y+2), (w//2-sz//2, y+48), (w//2+sz//2, y+48)])
    elif kind == 'bush':
        pygame.draw.ellipse(s, t['leaf_dark'], (30, 160, 120, 90))
        pygame.draw.ellipse(s, t['leaf'],      (45, 170, 90, 70))
        bright = tuple(min(255, c+30) for c in t['leaf'])
        pygame.draw.ellipse(s, bright, (60, 180, 60, 50))
    return s

def make_billboard(variant, theme_key):
    w, h = 200, 280
    s = pygame.Surface((w, h), pygame.SRCALPHA)
    pygame.draw.rect(s, (90,90,96), (w//2-6, 130, 12, 150))
    palettes = [
        ((235,235,240), (200,30,30),   (40,40,55)),
        ((20,40,90),    (250,220,80),  (250,250,250)),
        ((250,240,200), (180,120,20),  (60,40,20)),
        ((230,60,60),   (255,255,255), (40,40,40)),
        ((20,20,25),    (250,200,40),  (250,250,250)),
        ((40,120,80),   (250,250,250), (250,250,240)),
    ]
    bg, fg, ink = palettes[variant % len(palettes)]
    pygame.draw.rect(s, bg, (0, 0, w, 140), border_radius=8)
    pygame.draw.rect(s, ink, (0, 0, w, 140), 8, border_radius=8)
    pygame.draw.rect(s, fg, (14, 14, w-28, 40), border_radius=4)
    pygame.draw.rect(s, ink, (24, 66, w-48, 18), border_radius=3)
    pygame.draw.rect(s, ink, (24, 96, w-100, 18), border_radius=3)
    return s

def make_grandstand():
    w, h = 400, 220
    s = pygame.Surface((w, h), pygame.SRCALPHA)
    pygame.draw.rect(s, (140,140,150), (0, 60, w, 160), border_radius=8)
    pygame.draw.rect(s, (90,90,100),   (0, 60, w, 160), 4, border_radius=8)
    pygame.draw.rect(s, (200,200,210), (0, 20, w, 50), border_radius=6)
    pygame.draw.polygon(s, (230,230,240), [(10,20),(w-10,20),(w-30,0),(30,0)])
    rng = random.Random(42)
    for _ in range(600):
        x = rng.randint(8, w-8); y = rng.randint(78, 200); r = rng.randint(2, 4)
        col = rng.choice([(240,180,60),(200,60,60),(60,140,220),
                          (240,240,240),(20,20,30),(100,220,100),
                          (250,90,160),(90,90,200)])
        pygame.draw.circle(s, col, (x, y), r)
    return s

def make_tire_barrier():
    w, h = 240, 60
    s = pygame.Surface((w, h), pygame.SRCALPHA)
    for i in range(4):
        col = (20,20,25) if i % 2 == 0 else (240,240,245)
        pygame.draw.rect(s, col, (i*60, 0, 60, 60), border_radius=8)
        pygame.draw.rect(s, (60,60,70), (i*60, 0, 60, 60), 2, border_radius=8)
    return s

def make_start_banner():
    w, h = 200, 280
    s = pygame.Surface((w, h), pygame.SRCALPHA)
    pygame.draw.rect(s, (60, 65, 78), (14, 60, 14, 220))
    pygame.draw.rect(s, (60, 65, 78), (w-28, 60, 14, 220))
    pygame.draw.rect(s, (90, 95, 110), (14, 60, 14, 220), 2)
    pygame.draw.rect(s, (90, 95, 110), (w-28, 60, 14, 220), 2)
    pygame.draw.rect(s, (30, 30, 38), (0, 10, w, 70), border_radius=6)
    pygame.draw.rect(s, (255, 210, 40), (0, 10, w, 70), 3, border_radius=6)
    cols_n = 10
    cw = w // cols_n
    for i in range(cols_n):
        col = (250, 250, 250) if i % 2 == 0 else (15, 15, 20)
        pygame.draw.rect(s, col, (i*cw, 14, cw-1, 8))
        pygame.draw.rect(s, col, (i*cw, 66, cw-1, 8))
    try:
        f = pygame.font.SysFont("arial", 18, bold=True)
        t1 = f.render("START", True, (255, 255, 255))
        t2 = f.render("FINISH", True, (255, 210, 40))
        s.blit(t1, (w//2 - t1.get_width() - 4, 32))
        s.blit(t2, (w//2 + 4, 32))
    except Exception:
        pass
    return s

def make_sky(top, bottom):
    sky = pygame.Surface((WIDTH, HEIGHT))
    mid = lerp_color(top, bottom, 0.55)
    for y in range(HEIGHT):
        t = y / HEIGHT
        c = lerp_color(top, mid, t/0.55) if t < 0.55 else lerp_color(mid, bottom, (t-0.55)/0.45)
        pygame.draw.line(sky, c, (0, y), (WIDTH, y))
    return sky

# ===================== COCKPIT / WHEEL =====================
def make_cockpit(team):
    surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    dash_h = 155
    pygame.draw.polygon(surf, (22,22,26), [
        (0, HEIGHT), (WIDTH, HEIGHT),
        (WIDTH, HEIGHT - dash_h + 55),
        (int(WIDTH*0.80), HEIGHT - dash_h),
        (int(WIDTH*0.20), HEIGHT - dash_h),
        (0, HEIGHT - dash_h + 55)])
    pygame.draw.polygon(surf, (40,40,48), [
        (int(WIDTH*0.20), HEIGHT - dash_h),
        (int(WIDTH*0.80), HEIGHT - dash_h),
        (int(WIDTH*0.78), HEIGHT - dash_h + 8),
        (int(WIDTH*0.22), HEIGHT - dash_h + 8)])
    pygame.draw.polygon(surf, (30,30,36), [
        (0, HEIGHT), (0, int(HEIGHT*0.55)),
        (int(WIDTH*0.07), int(HEIGHT*0.68)), (int(WIDTH*0.10), HEIGHT)])
    pygame.draw.polygon(surf, (30,30,36), [
        (WIDTH, HEIGHT), (WIDTH, int(HEIGHT*0.55)),
        (WIDTH - int(WIDTH*0.07), int(HEIGHT*0.68)),
        (WIDTH - int(WIDTH*0.10), HEIGHT)])
    halo_col = (18,18,22,235)
    pygame.draw.rect(surf, halo_col, (WIDTH//2-15, 0, 30, 96), border_radius=8)
    pygame.draw.arc(surf, halo_col,
                    (int(-WIDTH*0.10), -int(HEIGHT*0.55),
                     int(WIDTH*1.20), int(HEIGHT*1.10)),
                    math.radians(52), math.radians(128), 22)
    pygame.draw.rect(surf, (60,60,70), (WIDTH//2-15, 0, 30, 6))
    if team:
        pygame.draw.rect(surf, team['primary'], (WIDTH//2-14, 6, 28, 12))
        pygame.draw.rect(surf, team['secondary'], (WIDTH//2-14, 18, 28, 4))
        pygame.draw.rect(surf, team['primary'],
                         (int(WIDTH*0.22), HEIGHT - dash_h + 10,
                          int(WIDTH*0.56), 4))
        pygame.draw.rect(surf, team['secondary'],
                         (int(WIDTH*0.22), HEIGHT - dash_h + 16,
                          int(WIDTH*0.56), 2))
    for mx in (int(WIDTH*0.115), int(WIDTH*0.885)):
        pygame.draw.rect(surf, (20,20,24), (mx-62, 58, 124, 74), border_radius=14)
        pygame.draw.rect(surf, (52,58,70), (mx-54, 66, 108, 58), border_radius=10)
        pygame.draw.rect(surf, (86,100,120), (mx-54, 66, 108, 20), border_radius=10)
        pygame.draw.rect(surf, (35,35,42), (mx-8, 128, 16, 26))
    return surf

def make_wheel(team):
    size = 460
    s = pygame.Surface((size, size), pygame.SRCALPHA)
    c = size // 2
    R = 200
    pygame.draw.circle(s, (32,32,38), (c,c), R, 30)
    pygame.draw.circle(s, (62,62,74), (c,c), R+16, 4)
    pygame.draw.circle(s, (18,18,22), (c,c), R-15, 4)
    if team:
        pygame.draw.arc(s, team['primary'],
                        (c-R, c-R, R*2, R*2),
                        math.radians(72), math.radians(108), 30)
        pygame.draw.arc(s, team['secondary'],
                        (c-R+6, c-R+6, R*2-12, R*2-12),
                        math.radians(80), math.radians(100), 6)
    else:
        pygame.draw.arc(s, (225,42,42), (c-R, c-R, R*2, R*2),
                        math.radians(72), math.radians(108), 30)
    pygame.draw.rect(s, (44,44,54), (c-175, c-20, 350, 40), border_radius=12)
    pygame.draw.rect(s, (58,58,70), (c-80, c-52, 160, 104), border_radius=22)
    pygame.draw.rect(s, (30,30,38), (c-62, c-34, 124, 68), border_radius=16)
    pygame.draw.circle(s, (215,190,60), (c-62, c+4), 13)
    pygame.draw.circle(s, (200,60,60),  (c+62, c+4), 13)
    pygame.draw.circle(s, (70,200,110), (c-62, c-30), 9)
    pygame.draw.circle(s, (90,150,230), (c+62, c-30), 9)
    return s

# ===================== TRACK META =====================
TRACK_META = [
    ("Монца",           "ИТ",  "grass",  1, 101),
    ("Монако",          "МК",  "city",   5, 202),
    ("Сильверстоун",    "ВБ",  "grass",  3, 303),
    ("Спа",             "БЕ",  "grass",  3, 404),
    ("Сузука",          "ЯП",  "grass",  3, 505),
    ("Интерлагос",      "БР",  "grass",  3, 606),
    ("Шанхай",          "КН",  "grass",  3, 707),
    ("Сочи",            "РФ",  "grass",  2, 808),
    ("Бахрейн",         "БХ",  "desert", 2, 909),
    ("Яс Марина",       "ОАЭ", "sunset", 2, 1010),
    ("Марина Бэй",      "СГ",  "city",   4, 1111),
    ("Барселона",       "ИС",  "grass",  3, 1212),
    ("Хунгароринг",     "ВГ",  "grass",  3, 1313),
    ("Ред Булл Ринг",   "АВ",  "grass",  2, 1414),
    ("Зандворт",        "НИ",  "grass",  3, 1515),
    ("Портиман",        "ПТ",  "sunset", 3, 1616),
    ("Имола",           "ИТ",  "grass",  3, 1717),
    ("Муджелло",        "ИТ",  "grass",  4, 1818),
    ("Ле-Кастелле",     "ФР",  "grass",  2, 1919),
    ("Поль Рикар",      "ФР",  "grass",  3, 2020),
    ("Хоккенхайм",      "ГЕ",  "grass",  2, 2121),
    ("Нюрбургринг",     "ГЕ",  "grass",  3, 2222),
    ("Брэндс-Хэтч",     "ВБ",  "grass",  4, 2323),
    ("Донингтон",       "ВБ",  "grass",  3, 2424),
    ("Уоткинс-Глен",    "США", "sunset", 3, 2525),
    ("Лагуна Сека",     "США", "desert", 4, 2626),
    ("Индианаполис",    "США", "grass",  2, 2727),
    ("Кота",            "США", "desert", 3, 2828),
    ("Мехико",          "МХ",  "sunset", 3, 2929),
    ("Жакарепагуа",     "БР",  "grass",  4, 3030),
    ("Буэнос-Айрес",    "АР",  "grass",  2, 3131),
    ("Киалами",         "ЮА",  "sunset", 3, 3232),
    ("Фудзи",           "ЯП",  "snow",   2, 3333),
    ("Сепанг",          "МЗ",  "grass",  3, 3434),
    ("Йеонгам",         "КР",  "night",  3, 3535),
    ("Будда",           "ИН",  "desert", 2, 3636),
]

def make_track_layout(seed, difficulty):
    rng = random.Random(seed)
    layout = [(45, 45, 45, 0, 0)]
    sections = 4 + difficulty * 2
    curve_amp = 2.0 + difficulty * 0.6
    y_amp = 12 + difficulty * 6
    total_y = 0.0
    for _ in range(sections):
        curve = rng.choice([-1, 1]) * rng.uniform(1.5, curve_amp)
        y = rng.uniform(-y_amp, y_amp) if rng.random() < 0.55 else 0
        enter = rng.randint(30, 45)
        hold  = rng.randint(45, 80)
        leave = rng.randint(30, 45)
        layout.append((enter, hold, leave, curve, y))
        total_y += y
        if rng.random() < 0.6:
            y2 = rng.uniform(-y_amp/2, y_amp/2)
            layout.append((20, 30, 20, 0, y2))
            total_y += y2
    if abs(total_y) > 0.01:
        layout.append((50, 50, 50, 0, -total_y))
    layout.append((45, 45, 45, 0, 0))
    return layout

TRACKS = []
for _name, _ctry, _theme, _diff, _seed in TRACK_META:
    TRACKS.append({
        'name': _name, 'country': _ctry, 'theme': _theme,
        'difficulty': _diff, 'layout': make_track_layout(_seed, _diff),
    })

# ===================== SEGMENT =====================
class Segment:
    __slots__ = ('index','curve','y1','y2','z1','z2','color',
                 'sprites','cars','clip','fog',
                 'p1sx','p1sy','p1sw','p1scale','p1cz',
                 'p2sx','p2sy','p2sw','p2scale','p2cz','looped',
                 'is_finish')
    def __init__(self, index, curve, y1, y2):
        self.index = index; self.curve = curve
        self.y1 = y1; self.y2 = y2
        self.z1 = index * SEGMENT_LENGTH
        self.z2 = (index + 1) * SEGMENT_LENGTH
        self.color = None; self.sprites = []; self.cars = []
        self.clip = HEIGHT; self.fog = 1.0; self.looped = False
        self.is_finish = False

segments = []
def last_y(): return segments[-1].y2 if segments else 0.0

def add_segment(curve, y):
    n = len(segments)
    segments.append(Segment(n, curve, last_y(), y))

def add_road(enter, hold, leave, curve, y):
    start_y = last_y()
    end_y = start_y + y * SEGMENT_LENGTH
    total = enter + hold + leave
    for n in range(enter):
        add_segment(ease_in(0, curve, n/enter),
                    ease_in_out(start_y, end_y, n/total))
    for n in range(hold):
        add_segment(curve, ease_in_out(start_y, end_y, (enter+n)/total))
    for n in range(leave):
        add_segment(ease_in_out(curve, 0, n/leave),
                    ease_in_out(start_y, end_y, (enter+hold+n)/total))

def find_segment(z):
    return segments[int(z // SEGMENT_LENGTH) % len(segments)]

# ===================== TRACK LOADING =====================
CURRENT_FOG = (150, 185, 220)
sky_surf = None
current_track_idx = 0
track_length = 0
current_theme_key = 'grass'

def build_segments(layout):
    segments.clear()
    for (en, ho, le, cu, y) in layout:
        add_road(en, ho, le, cu, y)

def apply_theme(theme_key):
    t = THEMES[theme_key]
    for n, seg in enumerate(segments):
        seg.is_finish = (n == 0)
        if (n // RUMBLE_LENGTH) % 2:
            seg.color = {'road': t['road'], 'grass': t['grass'],
                         'rumble': t['rumble'], 'lane': (250,250,250)}
        else:
            seg.color = {'road': t['road_dark'], 'grass': t['grass_dark'],
                         'rumble': t['rumble_dark'], 'lane': (250,250,250)}
    if segments:
        segments[0].color['rumble'] = (28, 28, 32)

def add_track_sprites(theme_key):
    rng = random.Random(current_track_idx * 9973 + 42)
    if theme_key == 'desert':
        tree_kinds = ['palm', 'palm', 'bush']
    elif theme_key == 'snow':
        tree_kinds = ['snowpine', 'snowpine', 'conifer']
    elif theme_key == 'city':
        tree_kinds = ['round', 'poplar']
    elif theme_key == 'night':
        tree_kinds = ['conifer', 'round', 'bush']
    else:
        tree_kinds = ['round', 'conifer', 'poplar', 'bush']
    trees = {k: make_tree(k, theme_key) for k in set(tree_kinds)}
    billboards = [make_billboard(i, theme_key) for i in range(6)]
    grandstand = make_grandstand()
    barrier = make_tire_barrier()
    start_banner = make_start_banner()
    if len(segments) > 3:
        segments[3].sprites.append((start_banner, -1.5))
        segments[3].sprites.append((start_banner, 1.5))
    n_segs = len(segments)
    bb_count = 0
    for n in range(15, n_segs - 15):
        seg = segments[n]
        if n % 18 == 7:
            bb = billboards[bb_count % len(billboards)]
            side = -1.6 if bb_count % 2 == 0 else 1.6
            bb_count += 1
            seg.sprites.append((bb, side))
        if n % 4 == 0:
            if rng.random() < 0.7:
                k = rng.choice(tree_kinds)
                seg.sprites.append((trees[k], rng.uniform(-2.8, -2.0)))
            if rng.random() < 0.7:
                k = rng.choice(tree_kinds)
                seg.sprites.append((trees[k], rng.uniform(2.0, 2.8)))
        if n % 90 == 30:
            seg.sprites.append((grandstand, rng.choice([-1.78, 1.78])))
        if abs(seg.curve) > 3.5 and n % 5 == 0:
            side = -1.35 if seg.curve > 0 else 1.35
            seg.sprites.append((barrier, side))

def load_track(idx):
    global CURRENT_FOG, sky_surf, track_length, current_track_idx, current_theme_key
    current_track_idx = idx
    trk = TRACKS[idx]
    theme_key = trk['theme']
    current_theme_key = theme_key
    theme = THEMES[theme_key]
    CURRENT_FOG = theme['fog']
    build_segments(trk['layout'])
    apply_theme(theme_key)
    add_track_sprites(theme_key)
    sky_surf = make_sky(theme['sky_top'], theme['sky_bot'])
    track_length = len(segments) * SEGMENT_LENGTH

# ===================== ENTITIES =====================
class Player:
    def __init__(self):
        self.total = 0.0; self.playerX = 0.0; self.speed = 0.0
        self.steer = 0.0; self.lap = 1; self.lap_time = 0.0
        self.best_lap = None

class Opponent:
    def __init__(self, total, offset, team, driver_name, driver_num, skill):
        self.total = total
        self.offset = offset; self.target = offset
        self.skill = skill; self.speed = 0.0
        self.team = team; self.driver_name = driver_name; self.driver_num = driver_num
        self.color = team['primary']
        self.sprite = make_car_sprite(team, driver_num)
        self.retarget = random.uniform(2.0, 5.0)
        self.eliminated = False       # для elimination режима
        self.points = 0               # для чемпионата

# ===================== GAME STATE =====================
state = 'menu'
menu_sel = 0
track_sel = 0
team_sel = 0
driver_sel = 0
mode_sel = 0
pause_sel = 0
countdown = 4.0
race_time = 0.0
final_pos = 0
shake = 0.0

player_team_idx = 0
player_driver_idx = 0

player = Player()
opponents = []
cockpit_surf = None
wheel_surf = None

# Параметры текущего режима
current_mode_idx = 0
current_laps = 3
current_opponent_count = 19
current_special = None

# Чемпионат
champ_round = 0
champ_tracks = []
champ_player_points = 0
champ_player_history = []      # список (позиция, очки, имя трассы)

# Баннер круга
lap_banner_timer = 0.0
lap_banner_text  = ""

def trigger_lap_banner(text):
    global lap_banner_timer, lap_banner_text
    lap_banner_timer = 2.0
    lap_banner_text = text

def refresh_cockpit():
    global cockpit_surf, wheel_surf
    team = TEAMS[player_team_idx]
    cockpit_surf = make_cockpit(team)
    wheel_surf = make_wheel(team)

def apply_mode(mode_idx):
    global current_mode_idx, current_laps, current_opponent_count, current_special
    current_mode_idx = mode_idx
    m = RACE_MODES[mode_idx]
    current_laps = m['laps']
    current_opponent_count = m['opponents']
    current_special = m['special']

def spawn_opponents(count=19, aggressive=False):
    global opponents
    opponents = []
    player_key = (player_team_idx, player_driver_idx)
    pool = []
    for ti, team in enumerate(TEAMS):
        for di, (name, num) in enumerate(team['drivers']):
            if (ti, di) != player_key:
                pool.append((ti, di, name, num))
    rng = random.Random()
    rng.shuffle(pool)
    count = min(count, len(pool))
    lo, hi = (0.78, 0.96) if aggressive else (0.62, 0.88)
    for i in range(count):
        ti, di, name, num = pool[i]
        team = TEAMS[ti]
        row = i // 2; col = i % 2
        opponents.append(Opponent(
            1500.0 + row * 1150.0,
            -0.35 if col == 0 else 0.35,
            team, name, num,
            rng.uniform(lo, hi)))
    opponents.sort(key=lambda o: -o.total)

def reset_race():
    global player, countdown, race_time, final_pos, shake, state
    global lap_banner_timer, lap_banner_text
    player = Player()
    spawn_opponents(current_opponent_count, aggressive=(current_special == 'aggressive'))
    refresh_cockpit()
    countdown = 4.0
    race_time = 0.0
    final_pos = 0
    shake = 0.0
    lap_banner_timer = 0.0
    lap_banner_text = ""
    state = 'countdown'

def start_race_from_menu():
    load_track(current_track_idx)
    reset_race()

# ---- Championship ----
def start_championship():
    global champ_round, champ_tracks, champ_player_points, champ_player_history
    champ_round = 0
    champ_player_points = 0
    champ_player_history = []
    all_tracks = list(range(len(TRACKS)))
    random.shuffle(all_tracks)
    champ_tracks = all_tracks[:CHAMP_ROUNDS]
    load_track(champ_tracks[0])
    reset_race()

def award_champ_points():
    """Награждает игрока и ИИ очками по финишной позиции."""
    global champ_player_points, final_pos
    standings = get_standings()
    player_pos = [s[0] for s in standings].index('player') + 1
    final_pos = player_pos
    pts = CHAMP_POINTS[player_pos - 1] if player_pos <= len(CHAMP_POINTS) else 0
    champ_player_points += pts
    champ_player_history.append((player_pos, pts, TRACKS[current_track_idx]['name']))
    # Очки ИИ
    for i, (who, _) in enumerate(standings):
        if who == 'player': continue
        pos = i + 1
        ai_pts = CHAMP_POINTS[pos - 1] if pos <= len(CHAMP_POINTS) else 0
        opponents[who].points += ai_pts

def advance_championship():
    """Переходит к следующему раунду или завершает чемпионат."""
    global champ_round, state
    champ_round += 1
    if champ_round >= CHAMP_ROUNDS:
        state = 'champ_final'
    else:
        load_track(champ_tracks[champ_round])
        reset_race()

# ===================== INITIAL LOAD =====================
apply_mode(0)
load_track(0)
refresh_cockpit()
spawn_opponents(19)

# ===================== FINISH LINE =====================
def draw_checkered(x1, y1, w1, x2, y2, w2, fog, cols=8, rows=4):
    col_light = fog_color((250, 250, 250), fog)
    col_dark  = fog_color((15, 15, 20),   fog)
    for r in range(rows):
        tr1 = r / rows; tr2 = (r + 1) / rows
        ya = y1 + (y2 - y1) * tr1
        yb = y1 + (y2 - y1) * tr2
        xa = x1 + (x2 - x1) * tr1
        xb = x1 + (x2 - x1) * tr2
        wa = w1 + (w2 - w1) * tr1
        wb = w1 + (w2 - w1) * tr2
        for c in range(cols):
            tc1 = c / cols; tc2 = (c + 1) / cols
            pa1 = xa - wa + 2 * wa * tc1
            pb1 = xa - wa + 2 * wa * tc2
            pa2 = xb - wb + 2 * wb * tc1
            pb2 = xb - wb + 2 * wb * tc2
            col = col_light if (r + c) % 2 == 0 else col_dark
            pygame.draw.polygon(screen, col,
                [(pa1, ya), (pb1, ya), (pb2, yb), (pa2, yb)])

# ===================== RENDER HELPERS =====================
def draw_segment(seg, fog):
    y1, y2 = seg.p1sy, seg.p2sy
    x1, x2 = seg.p1sx, seg.p2sx
    w1, w2 = seg.p1sw, seg.p2sw
    col = seg.color
    grass  = fog_color(col['grass'], fog)
    rumble = fog_color(col['rumble'], fog)
    road   = fog_color(col['road'], fog)
    lane   = fog_color(col['lane'], fog) if 'lane' in col else None
    r1, r2 = w1/6.0, w2/6.0
    l1, l2 = w1/32.0, w2/32.0
    y2d = y2 + 1
    pygame.draw.rect(screen, grass, (0, int(y2), WIDTH, int(y1-y2)+2))
    pygame.draw.polygon(screen, rumble, [(x1-w1-r1,y1),(x1-w1,y1),(x2-w2,y2d),(x2-w2-r2,y2d)])
    pygame.draw.polygon(screen, rumble, [(x1+w1+r1,y1),(x1+w1,y1),(x2+w2,y2d),(x2+w2+r2,y2d)])
    pygame.draw.polygon(screen, road,   [(x1-w1,y1),(x1+w1,y1),(x2+w2,y2d),(x2-w2,y2d)])
    if seg.is_finish:
        draw_checkered(x1, y1, w1, x2, y2d, w2, fog)
    elif lane:
        lanew1 = w1 * 2 / LANES; lanew2 = w2 * 2 / LANES
        lx1 = x1 - w1 + lanew1; lx2 = x2 - w2 + lanew2
        for _ in range(1, LANES):
            pygame.draw.polygon(screen, lane, [
                (lx1-l1/2,y1),(lx1+l1/2,y1),(lx2+l2/2,y2d),(lx2-l2/2,y2d)])
            lx1 += lanew1; lx2 += lanew2

def render_sprite(surf, scale, destX, destY, offsetX, offsetY, clipY):
    destW = surf.get_width() * scale * WIDTH/2 * SPRITE_SCALE * ROAD_WIDTH
    destH = surf.get_height() * scale * WIDTH/2 * SPRITE_SCALE * ROAD_WIDTH
    if destW < 1.0 or destH < 1.0: return
    if destW > WIDTH * 3: return
    destX += destW * offsetX
    destY += destH * offsetY
    dW, dH = int(destW), int(destH)
    dX, dY = int(destX), int(destY)
    if dX > WIDTH or dX + dW < 0 or dH < 1: return
    clipH = max(0, dY + dH - clipY) if clipY else 0
    if clipH >= dH: return
    scaled = pygame.transform.scale(surf, (dW, dH))
    if clipH > 0:
        scaled = scaled.subsurface(pygame.Rect(0, 0, dW, dH - clipH))
    screen.blit(scaled, (dX, dY))

def get_standings():
    entries = [('player', player.total + playerZ)]
    for i, op in enumerate(opponents):
        if op.eliminated:
            entries.append((i, -1e9))   # выбывшие — в самом конце
        else:
            entries.append((i, op.total))
    entries.sort(key=lambda e: -e[1])
    return entries

# ===================== ELIMINATION =====================
def do_elimination():
    """Каждый круг — снимаем с гонки последнего (кроме игрока)."""
    standings = get_standings()
    # убираем player из списка кандидатов
    opp_entries = [(w, v) for (w, v) in standings if w != 'player']
    if not opp_entries:
        return
    last_who, _ = opp_entries[-1]
    if last_who == 'player':
        return
    op = opponents[last_who]
    if not op.eliminated:
        op.eliminated = True
        op.speed = 0.0
        trigger_lap_banner(f"ВЫБЫЛ #{op.driver_num} {op.driver_name[:10]}")

# ===================== UPDATE =====================
def update_race(dt):
    global state, race_time, shake, final_pos
    global lap_banner_timer

    race_time += dt
    player.lap_time += dt
    if lap_banner_timer > 0:
        lap_banner_timer = max(0.0, lap_banner_timer - dt)

    player_segment = find_segment(player.total + playerZ)
    speed_percent = player.speed / maxSpeed
    dx = dt * 2.2 * speed_percent

    keys = pygame.key.get_pressed()
    steer_input = 0
    if keys[pygame.K_LEFT]  or keys[pygame.K_a]: steer_input -= 1
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]: steer_input += 1
    throttle = keys[pygame.K_UP]   or keys[pygame.K_w]
    brake    = keys[pygame.K_DOWN] or keys[pygame.K_s]

    player.playerX += steer_input * dx
    player.playerX -= dx * speed_percent * player_segment.curve * CENTRIFUGAL
    player.playerX = clamp(player.playerX, -2.2, 2.2)

    if throttle:  player.speed = accelerate(player.speed, accel, dt)
    elif brake:   player.speed = accelerate(player.speed, breaking, dt)
    else:         player.speed = accelerate(player.speed, decel, dt)

    if (player.playerX < -1.0 or player.playerX > 1.0) and player.speed > offRoadLimit:
        player.speed = accelerate(player.speed, offRoadDecel, dt)
        shake = min(6.0, shake + 40*dt)
    player.speed = clamp(player.speed, 0.0, maxSpeed)
    player.total += player.speed * dt

    # Столкновения
    pcz = player.total + playerZ
    for op in opponents:
        if op.eliminated: continue
        dz = op.total - pcz
        if dz > track_length/2: dz -= track_length
        if dz < -track_length/2: dz += track_length
        if abs(dz) < 340 and abs(op.offset - player.playerX) < 0.36:
            player.speed *= 0.90
            push = 1 if op.offset > player.playerX else -1
            player.playerX -= push * dt * 2.4
            shake = min(9.0, shake + 90*dt)

    # ИИ
    for i, op in enumerate(opponents):
        if op.eliminated:
            op.speed = 0.0
            continue
        seg = find_segment(op.total)
        curve = seg.curve
        target_speed = maxSpeed * op.skill * (1.0 - min(0.5, abs(curve)*0.07))
        for j, other in enumerate(opponents):
            if i == j or other.eliminated: continue
            gap = other.total - op.total
            if 0 < gap < 950 and abs(other.offset - op.offset) < 0.26:
                target_speed = min(target_speed, other.speed * 0.94)
                op.target = op.offset + (0.55 if other.offset > op.offset else -0.55)
                break
        op.target = clamp(op.target, -0.86, 0.86)
        op.speed += (target_speed - op.speed) * min(1.0, dt * 1.4)
        op.total += op.speed * dt
        op.offset += (op.target - op.offset) * min(1.0, dt * 2.2)
        op.retarget -= dt
        if op.retarget <= 0:
            op.retarget = random.uniform(2.5, 6.0)
            op.target = random.uniform(-0.78, 0.78)

    # Логика кругов
    next_boundary = player.lap * track_length
    if player.lap <= current_laps and player.total >= next_boundary:
        lap_done = player.lap_time
        if player.best_lap is None or lap_done < player.best_lap:
            player.best_lap = lap_done
        completed_lap = player.lap
        player.lap += 1
        player.lap_time = 0.0

        # Elimination
        if current_special == 'elimination':
            do_elimination()

        if player.lap > current_laps:
            # Гонка завершена
            if current_special == 'championship':
                award_champ_points()
                state = 'champ_standings'
            else:
                standings = get_standings()
                final_pos = [s[0] for s in standings].index('player') + 1
                state = 'finished'
        else:
            if current_special != 'elimination':
                trigger_lap_banner(f"КРУГ {completed_lap} / {current_laps}")

    player.steer += (steer_input - player.steer) * min(1.0, dt * 9.0)
    shake = max(0.0, shake - 22*dt)

# ===================== RACE RENDER =====================
def render_race():
    global shake
    screen.blit(sky_surf, (0, 0))
    position = player.total % track_length
    base_segment = find_segment(position)
    base_percent = (position % SEGMENT_LENGTH) / SEGMENT_LENGTH
    player_segment = find_segment(position + playerZ)
    player_percent = ((position + playerZ) % SEGMENT_LENGTH) / SEGMENT_LENGTH
    player_y = interpolate(player_segment.y1, player_segment.y2, player_percent)

    for s in segments: s.cars.clear()
    pcz = player.total + playerZ
    for op in opponents:
        if op.eliminated: continue
        rel = op.total - pcz
        if 0 <= rel < DRAW_DISTANCE * SEGMENT_LENGTH:
            si = int(op.total // SEGMENT_LENGTH) % len(segments)
            pct = (op.total % SEGMENT_LENGTH) / SEGMENT_LENGTH
            segments[si].cars.append((op, pct))

    maxy = HEIGHT
    x = 0.0
    dx = -(base_segment.curve * base_percent)

    for n in range(DRAW_DISTANCE):
        seg = segments[(base_segment.index + n) % len(segments)]
        seg.looped = seg.index < base_segment.index
        seg.fog = exponential_fog(n / DRAW_DISTANCE, FOG_DENSITY)
        seg.clip = maxy

        cam_z_base = position - (track_length if seg.looped else 0)
        cam_y = player_y + CAMERA_HEIGHT
        cam_x1 = player.playerX * ROAD_WIDTH - x
        cam_x2 = player.playerX * ROAD_WIDTH - x - dx

        cz1_raw = seg.z1 - cam_z_base
        cz2_raw = seg.z2 - cam_z_base
        cz1 = max(1.0, cz1_raw)
        cz2 = max(1.0, cz2_raw)
        s1 = cameraDepth / cz1
        s2 = cameraDepth / cz2

        seg.p1cz = cz1_raw; seg.p2cz = cz2_raw
        seg.p1scale = s1;   seg.p2scale = s2
        seg.p1sx = WIDTH/2 + s1 * (0 - cam_x1) * WIDTH/2
        seg.p1sy = HEIGHT/2 - s1 * (seg.y1 - cam_y) * HEIGHT/2
        seg.p1sw = s1 * ROAD_WIDTH * WIDTH/2
        seg.p2sx = WIDTH/2 + s2 * (0 - cam_x2) * WIDTH/2
        seg.p2sy = HEIGHT/2 - s2 * (seg.y2 - cam_y) * HEIGHT/2
        seg.p2sw = s2 * ROAD_WIDTH * WIDTH/2

        x += dx
        dx += seg.curve

        if cz1_raw <= 0.5:              continue
        if seg.p2sy >= seg.p1sy:        continue
        if seg.p2sy >= maxy:            continue

        draw_segment(seg, seg.fog)
        maxy = seg.p2sy

    for n in range(DRAW_DISTANCE - 1, 0, -1):
        seg = segments[(base_segment.index + n) % len(segments)]
        for (spr, off) in seg.sprites:
            sc = seg.p1scale
            sx = seg.p1sx + sc * off * ROAD_WIDTH * WIDTH/2
            sy = seg.p1sy
            render_sprite(spr, sc, sx, sy, -0.5, -1.0, seg.clip)
        for (car, pct) in seg.cars:
            sc = interpolate(seg.p1scale, seg.p2scale, pct)
            sx = interpolate(seg.p1sx, seg.p2sx, pct) + \
                 sc * car.offset * ROAD_WIDTH * WIDTH/2
            sy = interpolate(seg.p1sy, seg.p2sy, pct)
            render_sprite(car.sprite, sc, sx, sy, -0.5, -1.0, seg.clip)

    if shake > 0.5:
        ox = random.randint(-int(shake), int(shake))
        oy = random.randint(-int(shake), int(shake))
    else:
        ox = oy = 0

    screen.blit(cockpit_surf, (ox, oy))
    angle = -player.steer * 95.0
    rotated = pygame.transform.rotate(wheel_surf, angle)
    wc_x = WIDTH//2 + ox - rotated.get_width()//2
    wc_y = HEIGHT - 10 + oy - rotated.get_height()//2
    screen.blit(rotated, (wc_x, wc_y))

    draw_race_hud()
    draw_lap_banner()

# ===================== LAP BANNER =====================
def draw_lap_banner():
    if lap_banner_timer <= 0 or not lap_banner_text:
        return
    t = lap_banner_timer / 2.0
    if t > 0.85:
        alpha = int(255 * (1.0 - (t - 0.85) / 0.15))
    elif t < 0.25:
        alpha = int(255 * (t / 0.25))
    else:
        alpha = 255
    rise = int((1.0 - t) * 25)
    try:
        txt = FONT_XL.render(lap_banner_text, True, (255, 220, 60))
        sh  = FONT_XL.render(lap_banner_text, True, (0, 0, 0))
    except Exception:
        return
    cx = WIDTH // 2 - txt.get_width() // 2
    cy = 130 - rise
    pad_x, pad_y = 40, 18
    plate_w = txt.get_width() + pad_x * 2
    plate_h = txt.get_height() + pad_y * 2
    plate = pygame.Surface((plate_w, plate_h), pygame.SRCALPHA)
    pygame.draw.rect(plate, (0, 0, 0, int(alpha * 0.55)),
                     (0, 0, plate_w, plate_h), border_radius=18)
    team = TEAMS[player_team_idx]
    pygame.draw.rect(plate, (*team['primary'], alpha),
                     (0, 0, plate_w, plate_h), 4, border_radius=18)
    plate.set_alpha(alpha)
    sh.set_alpha(alpha)
    txt.set_alpha(alpha)
    screen.blit(plate, (cx - pad_x, cy - pad_y))
    screen.blit(sh, (cx + 4, cy + 4))
    screen.blit(txt, (cx, cy))

# ===================== RACE HUD =====================
def draw_race_hud():
    kmh = int(player.speed / maxSpeed * 342)
    gear = max(1, min(8, int(player.speed / maxSpeed * 7.9) + 1))
    standings = get_standings()
    pos = [s[0] for s in standings].index('player') + 1
    total_drivers = 1 + current_opponent_count

    hud = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    team = TEAMS[player_team_idx]
    driver_name, driver_num = team['drivers'][player_driver_idx]
    mode = RACE_MODES[current_mode_idx]

    panel = pygame.Surface((320, 118), pygame.SRCALPHA)
    pygame.draw.rect(panel, (0, 0, 0, 155), (0, 0, 320, 118), border_radius=12)
    pygame.draw.rect(panel, team['primary'], (0, 0, 320, 118), 3, border_radius=12)
    hud.blit(panel, (18, 18))
    hud.blit(FONT_L.render(f"P {pos}/{total_drivers}", True, (255, 255, 255)), (34, 26))
    cur_lap_show = min(player.lap, current_laps)
    hud.blit(FONT.render(f"LAP {cur_lap_show}/{current_laps}",
                         True, (255, 220, 60)), (36, 74))
    mini_car = pygame.transform.scale(make_car_sprite(team, driver_num), (46, 34))
    hud.blit(mini_car, (270, 40))

    # Название трассы и режима
    trk = TRACKS[current_track_idx]
    if current_special == 'championship':
        top_text = f"{trk['name']}  ·  РАУНД {champ_round + 1}/{CHAMP_ROUNDS}  ·  ОЧКИ {champ_player_points}"
    else:
        top_text = f"{mode['name']}  ·  {trk['name']}"
    name = FONT.render(top_text, True, (255, 255, 255))
    bg = pygame.Surface((name.get_width() + 28, 32), pygame.SRCALPHA)
    pygame.draw.rect(bg, (0, 0, 0, 150), (0, 0, bg.get_width(), 32), border_radius=8)
    screen.blit(bg, (WIDTH//2 - bg.get_width()//2, 18))
    hud.blit(name, (WIDTH//2 - name.get_width()//2, 24))

    panel2 = pygame.Surface((320, 118), pygame.SRCALPHA)
    pygame.draw.rect(panel2, (0, 0, 0, 155), (0, 0, 320, 118), border_radius=12)
    pygame.draw.rect(panel2, (60, 160, 255), (0, 0, 320, 118), 3, border_radius=12)
    hud.blit(panel2, (WIDTH - 338, 18))
    hud.blit(FONT.render("TIME  " + format_time(race_time), True, (255, 255, 255)),
             (WIDTH - 320, 30))
    bl = format_time(player.best_lap) if player.best_lap else "--:--.---"
    hud.blit(FONT.render("BEST  " + bl, True, (120, 255, 160)), (WIDTH - 320, 58))
    hud.blit(FONT.render("LAST  " + format_time(player.lap_time), True, (230, 230, 230)),
             (WIDTH - 320, 86))

    sp_panel = pygame.Surface((250, 130), pygame.SRCALPHA)
    pygame.draw.rect(sp_panel, (0, 0, 0, 168), (0, 0, 250, 130), border_radius=14)
    pygame.draw.rect(sp_panel, team['primary'], (0, 0, 250, 130), 3, border_radius=14)
    hud.blit(sp_panel, (30, HEIGHT - 190))
    hud.blit(FONT_XL.render(str(gear), True, (255, 210, 40)), (46, HEIGHT - 186))
    hud.blit(FONT_S.render("GEAR", True, (170, 170, 180)), (60, HEIGHT - 88))
    hud.blit(FONT_L.render(f"{kmh}", True, (255, 255, 255)), (135, HEIGHT - 168))
    hud.blit(FONT_S.render("KM/H", True, (170, 170, 180)), (140, HEIGHT - 132))

    # Мини-таблица (только если есть соперники)
    if current_opponent_count > 0:
        mini = pygame.Surface((260, 250), pygame.SRCALPHA)
        pygame.draw.rect(mini, (0, 0, 0, 140), (0, 0, 260, 250), border_radius=10)
        hud.blit(mini, (WIDTH - 278, HEIGHT - 320))
        shown = 0
        for i, (who, _) in enumerate(standings):
            if shown >= 10: break
            if who == 'player':
                col = team['primary']
                if col[0] > 220 and col[1] > 220 and col[2] > 220:
                    col = (255, 255, 255)
                label = f"{i+1:2d} ВЫ · {driver_num}"
                name_col = (255, 220, 60)
            else:
                op = opponents[who]
                col = op.color
                if col[0] > 220 and col[1] > 220 and col[2] > 220:
                    col = (210, 210, 210)
                if op.eliminated:
                    label = f"{i+1:2d} #{op.driver_num:2d} ВЫБЫЛ"
                    name_col = (150, 150, 155)
                    col = (100, 100, 105)
                else:
                    label = f"{i+1:2d} #{op.driver_num:2d} {op.driver_name[:10]}"
                    name_col = (235, 235, 240)
            pygame.draw.rect(hud, col, (WIDTH - 270, HEIGHT - 312 + shown*23, 4, 18))
            hud.blit(FONT_S.render(label, True, name_col),
                     (WIDTH - 262, HEIGHT - 312 + shown*23))
            shown += 1

    screen.blit(hud, (0, 0))

# ===================== MENUS =====================
def draw_main_menu():
    screen.blit(sky_surf, (0, 0))
    ov = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    ov.fill((5, 8, 18, 205))
    screen.blit(ov, (0, 0))
    pygame.draw.rect(screen, (220, 30, 40), (0, 200, WIDTH, 6))

    title = FONT_XXL.render("F1 RACER", True, (255, 255, 255))
    screen.blit(title, title.get_rect(center=(WIDTH // 2, 100)))
    sub = FONT_L.render("COCKPIT CHAMPIONSHIP", True, (230, 60, 60))
    screen.blit(sub, sub.get_rect(center=(WIDTH // 2, 165)))

    items = ["Начать гонку", "Выбрать режим", "Выбрать пилота",
             "Выбрать трассу", "Выход"]
    for i, txt in enumerate(items):
        rect = pygame.Rect(WIDTH//2 - 240, 230 + i*64, 480, 54)
        sel = (i == menu_sel)
        if sel:
            pygame.draw.rect(screen, (200, 30, 40), rect, border_radius=12)
            pygame.draw.rect(screen, (255, 255, 255), rect, 2, border_radius=12)
        else:
            pygame.draw.rect(screen, (18, 22, 34), rect, border_radius=12)
            pygame.draw.rect(screen, (70, 80, 110), rect, 2, border_radius=12)
        col = (255, 255, 255) if sel else (200, 210, 230)
        t = FONT_M.render(txt, True, col)
        screen.blit(t, t.get_rect(center=rect.center))

    team = TEAMS[player_team_idx]
    dname, dnum = team['drivers'][player_driver_idx]
    trk = TRACKS[current_track_idx]
    mode = RACE_MODES[current_mode_idx]
    info = FONT.render(f"{dname} · {team['name']}   |   {trk['name']}   |   {mode['name']}",
                       True, (180, 190, 210))
    screen.blit(info, info.get_rect(center=(WIDTH // 2, 600)))
    hint = FONT_S.render("↑/↓ — выбор   Enter — подтвердить   ESC — выход",
                         True, (130, 140, 160))
    screen.blit(hint, hint.get_rect(center=(WIDTH // 2, 632)))

def draw_mode_select():
    screen.blit(sky_surf, (0, 0))
    ov = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    ov.fill((5, 8, 18, 215))
    screen.blit(ov, (0, 0))

    title = FONT_L.render("ВЫБОР РЕЖИМА ГОНКИ", True, (255, 255, 255))
    screen.blit(title, title.get_rect(center=(WIDTH // 2, 46)))

    card_w = 500
    card_h = 74
    gap = 10
    total_h = len(RACE_MODES) * card_h + (len(RACE_MODES) - 1) * gap
    y0 = (HEIGHT - total_h) // 2 - 10
    x0 = (WIDTH - card_w) // 2

    for i, m in enumerate(RACE_MODES):
        rect = pygame.Rect(x0, y0 + i*(card_h+gap), card_w, card_h)
        sel = (i == mode_sel)
        # фон
        bg_col = (60, 90, 140) if sel else (25, 30, 45)
        pygame.draw.rect(screen, bg_col, rect, border_radius=12)
        # цветная полоска слева — от цвета команды
        team = TEAMS[player_team_idx]
        pygame.draw.rect(screen, team['primary'], (rect.x, rect.y, 6, rect.h),
                         border_top_left_radius=12, border_bottom_left_radius=12)
        # обводка
        border = (255, 230, 90) if sel else (60, 70, 100)
        pygame.draw.rect(screen, border, rect, 3 if sel else 2, border_radius=12)
        # название
        t = FONT_M.render(m['name'], True,
                          (255, 255, 255) if sel else (200, 210, 230))
        screen.blit(t, (rect.x + 24, rect.y + 12))
        # описание
        d = FONT_S.render(m['desc'], True,
                          (220, 230, 245) if sel else (140, 150, 175))
        screen.blit(d, (rect.x + 24, rect.y + 44))
        # иконка сложности
        if m['special'] == 'championship':
            ic = "🏆"
        elif m['special'] == 'elimination':
            ic = "💀"
        elif m['special'] == 'timetrial':
            ic = "⏱"
        elif m['special'] == 'aggressive':
            ic = "🔥"
        else:
            ic = "🏁"
        try:
            ic_s = FONT_L.render(ic, True, (255, 220, 60))
            screen.blit(ic_s, (rect.right - 60, rect.y + 18))
        except Exception:
            pass

    hint = FONT_S.render("↑/↓ — выбор   Enter — начать   ESC — назад",
                         True, (150, 160, 180))
    screen.blit(hint, hint.get_rect(center=(WIDTH // 2, HEIGHT - 18)))

def draw_driver_select():
    screen.blit(sky_surf, (0, 0))
    ov = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    ov.fill((5, 8, 18, 215))
    screen.blit(ov, (0, 0))

    title = FONT_L.render("ВЫБОР ПИЛОТА И БОЛИДА", True, (255, 255, 255))
    screen.blit(title, title.get_rect(center=(WIDTH // 2, 44)))

    list_x, list_y = 30, 90
    list_w = 340
    row_h = 50
    for i, team in enumerate(TEAMS):
        rect = pygame.Rect(list_x, list_y + i*row_h, list_w, row_h - 5)
        sel = (i == team_sel)
        if sel:
            pygame.draw.rect(screen, (60, 90, 140), rect, border_radius=8)
            pygame.draw.rect(screen, (255, 230, 90), rect, 2, border_radius=8)
        else:
            pygame.draw.rect(screen, (25, 30, 45), rect, border_radius=8)
            pygame.draw.rect(screen, (60, 70, 100), rect, 1, border_radius=8)
        pygame.draw.rect(screen, team['primary'],   (rect.x+8,  rect.y+8, 20, rect.h-16), border_radius=4)
        pygame.draw.rect(screen, team['secondary'], (rect.x+32, rect.y+8, 8,  rect.h-16), border_radius=2)
        col = (255, 255, 255) if sel else (200, 210, 230)
        t = FONT.render(team['name'], True, col)
        screen.blit(t, (rect.x + 52, rect.y + 14))

    drv_x = list_x + list_w + 25
    drv_y = 90
    drv_w = WIDTH - drv_x - 30
    drv_h = 96
    team = TEAMS[team_sel]

    for di, (dname, dnum) in enumerate(team['drivers']):
        rect = pygame.Rect(drv_x, drv_y + di*(drv_h+8), drv_w, drv_h)
        sel = (di == driver_sel)
        if sel:
            pygame.draw.rect(screen, (200, 30, 40), rect, border_radius=12)
            pygame.draw.rect(screen, (255, 255, 255), rect, 3, border_radius=12)
        else:
            pygame.draw.rect(screen, (25, 30, 45), rect, border_radius=12)
            pygame.draw.rect(screen, (70, 80, 110), rect, 2, border_radius=12)
        num_bg = pygame.Rect(rect.x+14, rect.y+14, 68, 68)
        pygame.draw.rect(screen, (250, 250, 250), num_bg, border_radius=10)
        pygame.draw.rect(screen, team['primary'], num_bg, 4, border_radius=10)
        nt = FONT_L.render(str(dnum), True, (20, 20, 25))
        screen.blit(nt, nt.get_rect(center=num_bg.center))
        ncol = (255, 255, 255) if sel else (220, 225, 235)
        screen.blit(FONT_M.render(dname, True, ncol), (rect.x + 100, rect.y + 22))
        screen.blit(FONT_S.render(team['name'], True, (200, 210, 230)),
                    (rect.x + 100, rect.y + 60))

    prev_y = drv_y + 2*(drv_h+8) + 8
    prev_rect = pygame.Rect(drv_x, prev_y, drv_w, HEIGHT - prev_y - 55)
    pygame.draw.rect(screen, (12, 16, 28), prev_rect, border_radius=14)
    pygame.draw.rect(screen, team['primary'], prev_rect, 3, border_radius=14)
    lbl = FONT_S.render("БОЛИД · ВИД СВЕРХУ", True, (180, 190, 210))
    screen.blit(lbl, (prev_rect.x + 16, prev_rect.y + 10))
    preview = make_car_sprite(team, team['drivers'][driver_sel][1])
    scale = 2.6
    big = pygame.transform.scale(preview,
        (int(preview.get_width()*scale), int(preview.get_height()*scale)))
    screen.blit(big, big.get_rect(center=(prev_rect.centerx, prev_rect.centery + 14)))

    hint = FONT_S.render("↑/↓ — команда   ←/→ — пилот   Enter — сохранить   ESC — назад",
                         True, (150, 160, 180))
    screen.blit(hint, hint.get_rect(center=(WIDTH // 2, HEIGHT - 18)))

GRID_COLS = 6
GRID_ROWS = 6
CELL_W = 170
CELL_H = 78
CELL_PAD = 3
GRID_W = GRID_COLS*CELL_W + (GRID_COLS-1)*CELL_PAD
GRID_H = GRID_ROWS*CELL_H + (GRID_ROWS-1)*CELL_PAD
GRID_X = (WIDTH - GRID_W) // 2
GRID_Y = 96

def draw_track_select():
    screen.blit(sky_surf, (0, 0))
    ov = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    ov.fill((5, 8, 18, 215))
    screen.blit(ov, (0, 0))

    title = FONT_L.render("ВЫБОР ТРАССЫ", True, (255, 255, 255))
    screen.blit(title, title.get_rect(center=(WIDTH // 2, 50)))

    for i in range(len(TRACKS)):
        col = i % GRID_COLS; row = i // GRID_COLS
        x = GRID_X + col * (CELL_W + CELL_PAD)
        y = GRID_Y + row * (CELL_H + CELL_PAD)
        rect = pygame.Rect(x, y, CELL_W, CELL_H)
        trk = TRACKS[i]; theme = THEMES[trk['theme']]
        sel = (i == track_sel)
        bg = (30, 34, 48) if not sel else (60, 90, 140)
        pygame.draw.rect(screen, bg, rect, border_radius=8)
        stripe = pygame.Rect(x+4, y+4, CELL_W-8, 5)
        pygame.draw.rect(screen, theme['badge'], stripe, border_radius=3)
        screen.blit(FONT_S.render(trk['name'], True, (255, 255, 255)), (x+8, y+16))
        screen.blit(FONT_XS.render(trk['country'], True, (200, 210, 230)), (x+8, y+38))
        st = FONT_XS.render("★" * trk['difficulty'], True, (255, 210, 60))
        screen.blit(st, (x+8, y+55))
        lbl = FONT_XS.render(THEME_LABELS[trk['theme']], True, theme['ui'])
        screen.blit(lbl, (x + CELL_W - lbl.get_width() - 8, y + 55))
        if sel:
            pygame.draw.rect(screen, (255, 230, 90), rect, 3, border_radius=8)
            pygame.draw.rect(screen, (255, 255, 255), rect.inflate(-6, -6),
                             1, border_radius=6)

    trk = TRACKS[track_sel]; theme = THEMES[trk['theme']]
    info_h = 100
    info_rect = pygame.Rect(30, HEIGHT - info_h - 10, WIDTH - 60, info_h)
    pygame.draw.rect(screen, (15, 20, 32), info_rect, border_radius=10)
    pygame.draw.rect(screen, theme['badge'], info_rect, 2, border_radius=10)
    screen.blit(FONT_L.render(trk['name'], True, (255, 255, 255)),
                (info_rect.x + 20, info_rect.y + 12))
    screen.blit(FONT.render(f"Страна: {trk['country']}", True, (200, 210, 230)),
                (info_rect.x + 20, info_rect.y + 54))
    screen.blit(FONT.render("Сложность: " + "★"*trk['difficulty'] + "☆"*(5-trk['difficulty']),
                            True, (255, 210, 60)),
                (info_rect.x + 260, info_rect.y + 54))
    screen.blit(FONT.render(f"Тема: {THEME_LABELS[trk['theme']]}", True, theme['ui']),
                (info_rect.x + 640, info_rect.y + 54))
    hint = FONT_S.render("Стрелки — навигация   Enter — начать гонку   ESC — назад",
                         True, (150, 160, 180))
    screen.blit(hint, hint.get_rect(center=(WIDTH // 2, HEIGHT - 18)))

def draw_pause_menu():
    ov = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    ov.fill((5, 8, 18, 190))
    screen.blit(ov, (0, 0))
    panel = pygame.Rect(WIDTH//2 - 250, 130, 500, 420)
    pygame.draw.rect(screen, (15, 20, 32), panel, border_radius=16)
    pygame.draw.rect(screen, (200, 30, 40), panel, 3, border_radius=16)
    t = FONT_XL.render("ПАУЗА", True, (255, 255, 255))
    screen.blit(t, t.get_rect(center=(WIDTH // 2, 190)))
    items = ["Продолжить", "Заново", "Выбрать трассу",
             "Главное меню", "Выход"]
    for i, txt in enumerate(items):
        rect = pygame.Rect(WIDTH//2 - 200, 260 + i*58, 400, 46)
        sel = (i == pause_sel)
        if sel:
            pygame.draw.rect(screen, (200, 30, 40), rect, border_radius=10)
            pygame.draw.rect(screen, (255, 255, 255), rect, 2, border_radius=10)
        else:
            pygame.draw.rect(screen, (25, 30, 45), rect, border_radius=10)
            pygame.draw.rect(screen, (70, 80, 110), rect, 2, border_radius=10)
        col = (255, 255, 255) if sel else (200, 210, 230)
        t = FONT_M.render(txt, True, col)
        screen.blit(t, t.get_rect(center=rect.center))

def draw_finish_overlay():
    ov = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    ov.fill((0, 0, 0, 180))
    screen.blit(ov, (0, 0))
    panel = pygame.Rect(WIDTH//2 - 340, 100, 680, 460)
    pygame.draw.rect(screen, (15, 20, 32), panel, border_radius=18)
    pygame.draw.rect(screen, (255, 210, 40), panel, 3, border_radius=18)
    t1 = FONT_XL.render("ФИНИШ", True, (255, 210, 40))
    screen.blit(t1, t1.get_rect(center=(WIDTH // 2, 160)))
    t2 = FONT_L.render(f"Ваша позиция: {final_pos} / {1 + current_opponent_count}",
                       True, (255, 255, 255))
    screen.blit(t2, t2.get_rect(center=(WIDTH // 2, 240)))
    if player.best_lap:
        t3 = FONT.render(f"Лучший круг: {format_time(player.best_lap)}",
                         True, (120, 255, 160))
        screen.blit(t3, t3.get_rect(center=(WIDTH // 2, 290)))
    t4 = FONT.render(f"Общее время: {format_time(race_time)}",
                     True, (230, 230, 230))
    screen.blit(t4, t4.get_rect(center=(WIDTH // 2, 330)))
    mode = RACE_MODES[current_mode_idx]
    t5 = FONT_S.render(f"Режим: {mode['name']}", True, (180, 190, 210))
    screen.blit(t5, t5.get_rect(center=(WIDTH // 2, 370)))
    hint = FONT.render("R — новая гонка   T — выбор трассы   ESC — главное меню",
                       True, (200, 210, 230))
    screen.blit(hint, hint.get_rect(center=(WIDTH // 2, 440)))

def draw_countdown_overlay():
    num = int(math.ceil(countdown))
    txt = str(num) if num >= 1 else "GO!"
    col = (255, 60, 60) if num >= 1 else (80, 255, 120)
    t = FONT_XXL.render(txt, True, col)
    sh = FONT_XXL.render(txt, True, (0, 0, 0))
    r = t.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 40))
    screen.blit(sh, (r.x + 5, r.y + 5))
    screen.blit(t, r)

# ===================== CHAMPIONSHIP STANDINGS SCREEN =====================
def draw_champ_standings():
    """Показывается между гонками чемпионата."""
    # Пробегаем трек в фоне
    render_race()
    ov = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    ov.fill((5, 8, 18, 210))
    screen.blit(ov, (0, 0))

    panel = pygame.Rect(120, 60, WIDTH - 240, HEIGHT - 120)
    pygame.draw.rect(screen, (15, 20, 32), panel, border_radius=18)
    pygame.draw.rect(screen, (255, 210, 40), panel, 3, border_radius=18)

    title = FONT_L.render(f"ЧЕМПИОНАТ · РАУНД {champ_round + 1} / {CHAMP_ROUNDS}",
                          True, (255, 255, 255))
    screen.blit(title, title.get_rect(center=(WIDTH // 2, 100)))

    last_pos, last_pts, last_track = champ_player_history[-1]
    info = FONT_M.render(f"{last_track}:  P{last_pos}   +{last_pts} очков",
                         True, (120, 255, 160))
    screen.blit(info, info.get_rect(center=(WIDTH // 2, 148)))

    # Текущие очки игрока
    tot = FONT_L.render(f"Всего: {champ_player_points} очков",
                        True, (255, 220, 60))
    screen.blit(tot, tot.get_rect(center=(WIDTH // 2, 200)))

    # Список гонок чемпионата
    y = 260
    hdr = FONT.render("Раунд  Трасса                Позиция  Очки",
                      True, (180, 190, 210))
    screen.blit(hdr, (WIDTH // 2 - 280, y))
    y += 30
    for i in range(CHAMP_ROUNDS):
        track_name = TRACKS[champ_tracks[i]]['name']
        if i < len(champ_player_history):
            pos, pts, _ = champ_player_history[i]
            line = f"  {i+1}     {track_name:<20}  P{pos:<3}   +{pts}"
            col = (230, 240, 255)
        else:
            line = f"  {i+1}     {track_name:<20}  —"
            col = (140, 150, 175)
        txt = FONT.render(line, True, col)
        screen.blit(txt, (WIDTH // 2 - 280, y))
        y += 28

    hint = FONT.render("Enter — следующий раунд   ESC — выйти в меню",
                       True, (200, 210, 230))
    screen.blit(hint, hint.get_rect(center=(WIDTH // 2, HEIGHT - 90)))

def draw_champ_final():
    """Финальный экран чемпионата."""
    ov = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    ov.fill((0, 0, 0, 200))
    screen.blit(ov, (0, 0))
    panel = pygame.Rect(WIDTH//2 - 400, 60, 800, HEIGHT - 120)
    pygame.draw.rect(screen, (15, 20, 32), panel, border_radius=18)
    pygame.draw.rect(screen, (255, 210, 40), panel, 3, border_radius=18)

    t1 = FONT_XL.render("ЧЕМПИОНАТ ЗАВЕРШЁН", True, (255, 210, 40))
    screen.blit(t1, t1.get_rect(center=(WIDTH // 2, 110)))

    # Итоговые очки
    t2 = FONT_L.render(f"Ваш результат: {champ_player_points} очков",
                       True, (255, 255, 255))
    screen.blit(t2, t2.get_rect(center=(WIDTH // 2, 175)))

    # Каждая гонка
    y = 220
    hdr = FONT.render("Раунд  Трасса                Позиция  Очки",
                      True, (180, 190, 210))
    screen.blit(hdr, (WIDTH // 2 - 320, y))
    y += 32
    for i, (pos, pts, name) in enumerate(champ_player_history):
        line = f"  {i+1}     {name:<20}  P{pos:<3}   +{pts}"
        col = (230, 240, 255) if pts > 0 else (200, 200, 210)
        if pts >= 18:
            col = (255, 220, 60)
        elif pts >= 10:
            col = (140, 255, 180)
        txt = FONT.render(line, True, col)
        screen.blit(txt, (WIDTH // 2 - 320, y))
        y += 26

    hint = FONT.render("Enter — в главное меню   R — новый чемпионат",
                       True, (200, 210, 230))
    screen.blit(hint, hint.get_rect(center=(WIDTH // 2, HEIGHT - 70)))

# ===================== MAIN LOOP =====================
running = True
while running:
    dt = 1.0 / 60.0
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if state == 'menu':
                if event.key == pygame.K_UP:    menu_sel = (menu_sel - 1) % 5
                elif event.key == pygame.K_DOWN: menu_sel = (menu_sel + 1) % 5
                elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    if menu_sel == 0:
                        # Начать гонку в текущем режиме
                        if current_special == 'championship':
                            start_championship()
                        else:
                            start_race_from_menu()
                    elif menu_sel == 1:
                        state = 'mode_select'
                        mode_sel = current_mode_idx
                    elif menu_sel == 2:
                        state = 'driver_select'
                        team_sel = player_team_idx
                        driver_sel = player_driver_idx
                    elif menu_sel == 3:
                        state = 'track_select'
                        track_sel = current_track_idx
                    else:
                        running = False
                elif event.key == pygame.K_ESCAPE:
                    running = False

            elif state == 'mode_select':
                if event.key == pygame.K_ESCAPE:
                    state = 'menu'
                elif event.key == pygame.K_UP:
                    mode_sel = (mode_sel - 1) % len(RACE_MODES)
                elif event.key == pygame.K_DOWN:
                    mode_sel = (mode_sel + 1) % len(RACE_MODES)
                elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    apply_mode(mode_sel)
                    state = 'menu'

            elif state == 'driver_select':
                if event.key == pygame.K_ESCAPE:
                    state = 'menu'
                elif event.key == pygame.K_UP:
                    team_sel = (team_sel - 1) % len(TEAMS)
                    driver_sel = min(driver_sel, len(TEAMS[team_sel]['drivers'])-1)
                elif event.key == pygame.K_DOWN:
                    team_sel = (team_sel + 1) % len(TEAMS)
                    driver_sel = min(driver_sel, len(TEAMS[team_sel]['drivers'])-1)
                elif event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                    driver_sel = (driver_sel + 1) % len(TEAMS[team_sel]['drivers'])
                elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    player_team_idx = team_sel
                    player_driver_idx = driver_sel
                    state = 'menu'

            elif state == 'track_select':
                if event.key == pygame.K_ESCAPE:
                    state = 'menu'
                elif event.key == pygame.K_LEFT:  track_sel = (track_sel - 1) % len(TRACKS)
                elif event.key == pygame.K_RIGHT: track_sel = (track_sel + 1) % len(TRACKS)
                elif event.key == pygame.K_UP:    track_sel = (track_sel - GRID_COLS) % len(TRACKS)
                elif event.key == pygame.K_DOWN:  track_sel = (track_sel + GRID_COLS) % len(TRACKS)
                elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    current_track_idx = track_sel
                    state = 'menu'

            elif state == 'countdown':
                if event.key == pygame.K_ESCAPE:
                    state = 'paused'; pause_sel = 0

            elif state == 'racing':
                if event.key in (pygame.K_ESCAPE, pygame.K_p):
                    state = 'paused'; pause_sel = 0

            elif state == 'champ_standings':
                if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    advance_championship()
                elif event.key == pygame.K_ESCAPE:
                    state = 'menu'; menu_sel = 0

            elif state == 'champ_final':
                if event.key in (pygame.K_RETURN, pygame.K_SPACE, pygame.K_ESCAPE):
                    state = 'menu'; menu_sel = 0
                elif event.key == pygame.K_r:
                    start_championship()

            elif state == 'paused':
                if event.key == pygame.K_ESCAPE:
                    state = 'racing'
                elif event.key == pygame.K_UP:   pause_sel = (pause_sel - 1) % 5
                elif event.key == pygame.K_DOWN: pause_sel = (pause_sel + 1) % 5
                elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    if pause_sel == 0:   state = 'racing'
                    elif pause_sel == 1:
                        if current_special == 'championship':
                            # Перезапуск текущего раунда
                            load_track(champ_tracks[champ_round])
                            reset_race()
                        else:
                            reset_race()
                    elif pause_sel == 2:
                        state = 'track_select'; track_sel = current_track_idx
                    elif pause_sel == 3:
                        state = 'menu'; menu_sel = 0
                    else: running = False

            elif state == 'finished':
                if event.key == pygame.K_r:
                    reset_race()
                elif event.key == pygame.K_t:
                    state = 'track_select'; track_sel = current_track_idx
                elif event.key == pygame.K_ESCAPE:
                    state = 'menu'; menu_sel = 0

    if state == 'countdown':
        countdown -= dt
        if countdown <= 0:
            state = 'racing'
    elif state == 'racing':
        update_race(dt)
    elif state == 'finished':
        if lap_banner_timer > 0:
            lap_banner_timer = max(0.0, lap_banner_timer - dt)

    # ---- RENDER ----
    if state == 'menu':
        draw_main_menu()
    elif state == 'mode_select':
        draw_mode_select()
    elif state == 'driver_select':
        draw_driver_select()
    elif state == 'track_select':
        draw_track_select()
    elif state == 'champ_standings':
        draw_champ_standings()
    elif state == 'champ_final':
        draw_champ_final()
    elif state in ('countdown', 'racing', 'paused', 'finished'):
        render_race()
        if state == 'countdown':
            draw_countdown_overlay()
        elif state == 'paused':
            draw_pause_menu()
        elif state == 'finished':
            draw_finish_overlay()

    pygame.display.flip()

pygame.quit()