import time
import random
import tkinter as tk
from tkinter import ttk
import sv_ttk
import json
import os
import sys
from PIL import Image, ImageTk, ImageDraw, ImageFont


# Card deck and upgrade system
base_suits = [
    'Hearts', 'Diamonds', 'Clubs', 'Spades', 'Stars', 'Moons', 'Crowns', 'Leaves', 'Suns', 'Waves',
    'Shields', 'Orbs', 'Axes', 'Spears', 'Rings', 'Cups', 'Scrolls', 'Keys', 'Masks', 'Fangs',
    'Eyes', 'Wings', 'Roots', 'Flames', 'Clouds', 'Stones', 'Webs', 'Beams', 'Echoes', 'Frost',
    'Petals', 'Coins', 'Swords', 'Helms', 'Lanterns', 'Talons', 'Scales', 'Spirals', 'Comets', 'Vines',
    'Crystals', 'Mirrors', 'Bells', 'Horns', 'Cogs', 'Rays', 'Dust', 'Mists', 'Roses', 'Thorns',
    'Paws', 'Hooves', 'Antlers', 'Shells', 'Fins', 'Roots', 'Stalks', 'Seeds', 'Pods'
]

# Suit color mapping for color-based combos (hex codes)
suit_colors = {
    'Hearts': '#FF0000', 'Diamonds': '#FF0000', 'Clubs': '#222222', 'Spades': '#222222',
    'Stars': '#FFFF00', 'Moons': '#1E90FF', 'Crowns': '#FFD700', 'Leaves': '#228B22', 'Suns': '#FFA500', 'Waves': '#1E90FF',
    'Shields': '#808080', 'Orbs': '#800080', 'Axes': '#8B4513', 'Spears': '#C0C0C0', 'Rings': '#FFD700', 'Cups': '#C0C0C0',
    'Scrolls': '#F5F5DC', 'Keys': '#CD7F32', 'Masks': '#FFFFFF', 'Fangs': '#FFFFFF', 'Eyes': '#1E90FF', 'Wings': '#FFFFFF',
    'Roots': '#8B4513', 'Flames': '#FFA500', 'Clouds': '#FFFFFF', 'Stones': '#808080', 'Webs': '#FFFFFF', 'Beams': '#FFFF00',
    'Echoes': '#1E90FF', 'Frost': '#00FFFF', 'Petals': '#FFC0CB', 'Coins': '#FFD700', 'Swords': '#C0C0C0', 'Helms': '#808080',
    'Lanterns': '#FFFF00', 'Talons': '#222222', 'Scales': '#228B22', 'Spirals': '#800080', 'Comets': '#FFFFFF', 'Vines': '#228B22',
    'Crystals': '#00FFFF', 'Mirrors': '#C0C0C0', 'Bells': '#FFD700', 'Horns': '#8B4513', 'Cogs': '#808080', 'Rays': '#FFFF00',
    'Dust': '#808080', 'Mists': '#FFFFFF', 'Roses': '#FF0000', 'Thorns': '#8B4513', 'Paws': '#8B4513', 'Hooves': '#808080',
    'Antlers': '#FFFFFF', 'Shells': '#FFFFFF', 'Fins': '#1E90FF', 'Stalks': '#228B22', 'Seeds': '#8B4513', 'Pods': '#228B22'
}
base_ranks = [
    '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A', 'Δ'
]

base_specials = {}

# Upgradeable lists
available_suits = base_suits.copy()
available_ranks = base_ranks.copy()
suits = [available_suits.pop(0)]  # Start with one suit
ranks = [available_ranks.pop(0)]  # Start with one rank
specials = base_specials.copy()

# Track total and draw count
total_count = 0
draw_count = 1  # Number of cards drawn per click
ace_multiplier = 1  # Multiplier for Ace effect

# Percentages for drawing normal vs special cards
NORMAL_CARD_CHANCE = 0.95  # 95% chance to draw a normal card
SPECIAL_CARD_CHANCE = 0.05  # 5% chance to draw a special card

# Percentages for each special card (must sum to 1.0)
special_card_weights = {
    'Joker': 0.10,
    'Double': 0.10,
    'Bonus': 0.10,
    'Triple': 0.10,
    'Half': 0.10,
    'Steal': 0.10,
    'Gift': 0.15,
    'Bland': 0.25
}

# Helper to pick a special card by weighted chance
def pick_special_card():
    names = list(special_card_weights.keys())
    weights = list(special_card_weights.values())
    return random.choices(names, weights=weights, k=1)[0]

def build_deck():
    deck = []
    for suit in suits:
        for rank in ranks:
            deck.append(f'{rank} of {suit}')
    # Add special cards with lower frequency
    for special in specials:
        # Add each special card only once for rarity
        deck.append(special)
    random.shuffle(deck)
    return deck

deck = build_deck()

# Card value lookup
rank_values = {str(i): i for i in range(2, 11)}
rank_values.update({'J': 11, 'Q': 12, 'K': 13, 'A': 14, '1': 1, 'Δ': 15})

# Special card abilities
special_card_pool = [
    ('Joker', lambda: joker_effect()),
    ('Double', lambda: double_effect()),
    ('Bonus', lambda: bonus_effect()),
    ('Triple', lambda: triple_effect()),
    ('Half', lambda: half_effect()),
    ('Steal', lambda: steal_effect()),
    ('Gift', lambda: gift_effect()),
    ('Bland', lambda: bland_effect())
]
special_abilities = {
    'Joker': lambda: joker_effect(),
    'Double': lambda: double_effect(),
    'Bonus': lambda: bonus_effect(),
    'Triple': lambda: triple_effect(),
    'Half': lambda: half_effect(),
    'Steal': lambda: steal_effect(),
    'Gift': lambda: gift_effect(),
    'Bland': lambda: bland_effect()
}

# Special card effect implementations
def joker_effect():
    global total_count
    total_count *= 2
    return 'Joker! Total doubled.'

def double_effect():
    global total_count
    total_count += 50
    return 'Double! +50 to total.'

def bonus_effect():
    global total_count
    total_count += 100
    return 'Bonus! +100 to total.'

def triple_effect():
    global total_count
    total_count *= 3
    return 'Triple! Total tripled.'

def half_effect():
    global total_count
    total_count = total_count // 2
    return 'Half! Total halved.'

def steal_effect():
    global total_count
    total_count += 200
    return 'Steal! +200 to total.'

def gift_effect():
    global total_count
    total_count += 500
    return 'Gift! +500 to total.'

def bland_effect():
    global total_count
    total_count -= 100
    return 'Bland! -100 from total.'

combo_history = []
COMBO_SIZE = 3
COMBO_BONUS = 30  # Nerfed combo bonus

# Color combo bonus
COLOR_COMBO_BONUS = 50  # Nerfed color combo bonus

# Suit effects
suit_effects = {
    'Flames': lambda: flames_effect(),
    'Frost': lambda: frost_effect(),
    'Waves': lambda: waves_effect(),
    'Stars': lambda: stars_effect(),
    'Moons': lambda: moons_effect(),
    'Crowns': lambda: crowns_effect(),
    'Roots': lambda: roots_effect(),
    'Echoes': lambda: echoes_effect(),
    'Rings': lambda: rings_effect(),
    'Masks': lambda: masks_effect(),
}

def flames_effect():
    global total_count
    total_count += 10
    return '+10 bonus from Flames!'

def frost_effect():
    global next_upgrade_discount
    next_upgrade_discount = 0.5
    return 'Next upgrade cost halved by Frost!'

def waves_effect():
    global extra_draw_next
    extra_draw_next = True
    return 'Waves! Next draw gives an extra card.'

def stars_effect():
    global total_count
    total_count += 25
    return '+25 bonus from Stars!'

def moons_effect():
    global extra_draw_next
    extra_draw_next = True
    return 'Moons! Draw +1 card next turn.'

def crowns_effect():
    global total_count
    total_count += 50
    return '+50 bonus from Crowns!'

def roots_effect():
    global total_count
    total_count = int(total_count * 1.1)
    return 'Roots! Total increased by 10%.'

def echoes_effect():
    global total_count
    total_count += 5 * draw_count
    return f'Echoes! +{5 * draw_count} bonus.'

def rings_effect():
    global total_count
    total_count += 100
    return '+100 bonus from Rings!'

def masks_effect():
    global total_count
    total_count -= 25
    return '-25 penalty from Masks!'

next_upgrade_discount = 1.0
extra_draw_next = False

# Skill tree
skills = {
    'combo_multiplier': 1,
    'upgrade_discount': 1.0,
    'special_chance': 0.05,
    # Add more skills as needed
}

# Prestige system variables
prestige_count = 0
prestige_bonus = 0.0  # e.g., permanent combo multiplier bonus
PRESTIGE_THRESHOLD = 10000  # Total required to prestige

def prestige():
    global total_count, draw_count, ace_multiplier, shield_active
    global suit_upgrade_level, rank_upgrade_level, special_upgrade_level, draw_upgrade_level
    global suits, ranks, specials, skills, prestige_count, prestige_bonus
    if total_count < PRESTIGE_THRESHOLD:
        result_label.config(text=f'Need {PRESTIGE_THRESHOLD} total to prestige!')
        return
    prestige_count += 1
    prestige_bonus += 0.1  # Each prestige adds +0.1 to combo multiplier
    # Reset game state to defaults
    total_count = 0
    draw_count = 1
    ace_multiplier = 1
    shield_active = False
    suit_upgrade_level = 0
    rank_upgrade_level = 0
    special_upgrade_level = 0
    draw_upgrade_level = 0
    suits = [base_suits[0]]
    ranks = [base_ranks[0]]
    specials = {}
    skills = {
        'combo_multiplier': 1 + prestige_bonus,
        'upgrade_discount': 1.0,
        'special_chance': 0.05,
    }
    rebuild_deck()
    update_upgrade_buttons()
    total_label.config(text='Total: 0')
    draw_count_label.config(text='Cards per draw: 1')
    result_label.config(text=f'Prestiged! Combo Multiplier bonus: +{prestige_bonus:.1f} (Prestige count: {prestige_count})')

def open_skill_tree():
    skill_win = tk.Toplevel(root)
    skill_win.title('Skill Tree')
    skill_win.geometry('400x300')
    ttk.Label(skill_win, text='Skill Tree', font=('Arial', 16)).pack(pady=10)
    # Combo Multiplier
    def upgrade_combo():
        if spend_total(200):
            skills['combo_multiplier'] += 1
            combo_label.config(text=f'Combo Multiplier: x{skills["combo_multiplier"]}')
    combo_label = ttk.Label(skill_win, text=f'Combo Multiplier: x{skills["combo_multiplier"]}')
    combo_label.pack(pady=5)
    ttk.Button(skill_win, text='Upgrade Combo Multiplier (200)', command=upgrade_combo).pack(pady=5)
    # Upgrade Discount
    def upgrade_discount():
        if spend_total(200):
            skills['upgrade_discount'] *= 0.9
            discount_label.config(text=f'Upgrade Discount: {skills["upgrade_discount"]:.2f}x')
    discount_label = ttk.Label(skill_win, text=f'Upgrade Discount: {skills["upgrade_discount"]:.2f}x')
    discount_label.pack(pady=5)
    ttk.Button(skill_win, text='Upgrade Discount (200)', command=upgrade_discount).pack(pady=5)
    # Special Chance
    def upgrade_special():
        if spend_total(200):
            skills['special_chance'] += 0.01
            special_label.config(text=f'Special Card Chance: {skills["special_chance"]:.2f}')
    special_label = ttk.Label(skill_win, text=f'Special Card Chance: {skills["special_chance"]:.2f}')
    special_label.pack(pady=5)
    ttk.Button(skill_win, text='Upgrade Special Chance (200)', command=upgrade_special).pack(pady=5)

    # Skill: Faster Autosave
    if 'autosave_speed' not in skills:
        skills['autosave_speed'] = 60000  # default 60s
    def upgrade_autosave():
        if spend_total(300) and skills['autosave_speed'] > 10000:
            skills['autosave_speed'] = max(10000, skills['autosave_speed'] - 10000)
            autosave_label.config(text=f'Autosave Interval: {skills["autosave_speed"]//1000}s')
    autosave_label = ttk.Label(skill_win, text=f'Autosave Interval: {skills["autosave_speed"]//1000}s')
    autosave_label.pack(pady=5)
    ttk.Button(skill_win, text='Upgrade Autosave Speed (300)', command=upgrade_autosave).pack(pady=5)

    # Skill: Increase Combo Size
    if 'combo_size' not in skills:
        skills['combo_size'] = 3
    def upgrade_combo_size():
        if spend_total(400):
            skills['combo_size'] += 1
            combo_size_label.config(text=f'Combo Size: {skills["combo_size"]}')
    combo_size_label = ttk.Label(skill_win, text=f'Combo Size: {skills["combo_size"]}')
    combo_size_label.pack(pady=5)
    ttk.Button(skill_win, text='Increase Combo Size (400)', command=upgrade_combo_size).pack(pady=5)

    # Skill: Suit Bonus (example for Hearts)
    if 'hearts_bonus' not in skills:
        skills['hearts_bonus'] = 0
    def upgrade_hearts_bonus():
        if spend_total(250):
            skills['hearts_bonus'] += 5
            hearts_bonus_label.config(text=f'Hearts Bonus: +{skills["hearts_bonus"]}')
    hearts_bonus_label = ttk.Label(skill_win, text=f'Hearts Bonus: +{skills["hearts_bonus"]}')
    hearts_bonus_label.pack(pady=5)
    ttk.Button(skill_win, text='Upgrade Hearts Bonus (250)', command=upgrade_hearts_bonus).pack(pady=5)

# Upgrade costs and levels
BASE_COSTS = {
    'suit': 10,
    'rank': 10,
    'special': 15,
    'draw': 50
}
suit_upgrade_level = 0
rank_upgrade_level = 0
special_upgrade_level = 0
draw_upgrade_level = 0

# Helper to calculate cost
def get_upgrade_cost(upgrade_type, level):
    base = BASE_COSTS[upgrade_type]
    # Exponential scaling: cost = base * (2 ** level) * discount
    return int(base * (2 ** level) * skills.get('upgrade_discount', 1.0) * next_upgrade_discount)

# Helper to update button text
def update_upgrade_buttons():
    add_suit_btn.config(text=f'Add Suit (Cost: {get_upgrade_cost("suit", suit_upgrade_level)}, Lv: {suit_upgrade_level})')
    add_rank_btn.config(text=f'Add Rank (Cost: {get_upgrade_cost("rank", rank_upgrade_level)}, Lv: {rank_upgrade_level})')
    add_special_btn.config(text=f'Add Special Card (Cost: {get_upgrade_cost("special", special_upgrade_level)}, Lv: {special_upgrade_level})')
    upgrade_draw_btn.config(text=f'Upgrade Draw Count (Cost: {get_upgrade_cost("draw", draw_upgrade_level)}, Lv: {draw_upgrade_level})')

# Upgrade functions
def spend_total(cost):
    global total_count
    if total_count >= cost:
        total_count -= cost
        total_label.config(text=f'Total: {total_count}')
        return True
    else:
        result_label.config(text=f'Not enough total! Need {cost}.')
        return False

def add_suit(_=None):
    global suit_upgrade_level
    cost = get_upgrade_cost('suit', suit_upgrade_level)
    if available_suits and spend_total(cost):
        new_suit = random.choice(available_suits)
        available_suits.remove(new_suit)
        suits.append(new_suit)
        suit_upgrade_level += 1
        rebuild_deck()
        result_label.config(text=f'Upgrade: Suit added!\nNew suit: {new_suit}\nTotal suits: {len(suits)}\nNext suit cost: {get_upgrade_cost("suit", suit_upgrade_level)}')
        update_upgrade_buttons()
    elif not available_suits:
        result_label.config(text='No more suits to unlock!')


def add_rank(_=None):
    global rank_upgrade_level
    cost = get_upgrade_cost('rank', rank_upgrade_level)
    if available_ranks and spend_total(cost):
        new_rank = random.choice(available_ranks)
        available_ranks.remove(new_rank)
        ranks.append(new_rank)
        # Assign a value for new ranks
        try:
            rank_values[new_rank] = int(new_rank)
            value_text = f"Value: {int(new_rank)}"
        except ValueError:
            face_values = {'J': 11, 'Q': 12, 'K': 13, 'A': 14, 'Δ': 15}
            rank_values[new_rank] = face_values.get(new_rank, 15)
            value_text = f"Value: {rank_values[new_rank]}"
        rank_upgrade_level += 1
        rebuild_deck()
        result_label.config(text=f'Upgrade: Rank added!\nNew rank: {new_rank} ({value_text})\nTotal ranks: {len(ranks)}\nNext rank cost: {get_upgrade_cost("rank", rank_upgrade_level)}')
        update_upgrade_buttons()
    elif not available_ranks:
        result_label.config(text='No more ranks to unlock!')

def add_special_card():
    global special_upgrade_level
    cost = get_upgrade_cost('special', special_upgrade_level)
    # Find available special cards not yet added
    available_specials = [name for name, _ in special_card_pool if name not in specials]
    if available_specials and spend_total(cost):
        new_name = random.choice(available_specials)
        for name, func in special_card_pool:
            if name == new_name:
                specials[new_name] = func
                special_abilities[new_name] = func
                break
        special_upgrade_level += 1
        rebuild_deck()
        result_label.config(text=f'Upgrade: Special card added!\nNew special: {new_name}\nTotal specials: {len(specials)}\nNext special cost: {get_upgrade_cost("special", special_upgrade_level)}')
        update_upgrade_buttons()
    elif not available_specials:
        result_label.config(text='No more special cards to unlock!')

def upgrade_draw_count():
    global draw_count, draw_upgrade_level
    cost = get_upgrade_cost('draw', draw_upgrade_level)
    if spend_total(cost) and draw_upgrade_level < 4:  # Limit max draw limit to 4
        prev_draw = draw_count
        draw_count += 1
        draw_upgrade_level += 1
        draw_count_label.config(text=f'Cards per draw: {draw_count}')
        result_label.config(text=f'Upgrade: Draw count increased!\nPrevious: {prev_draw}\nNow: {draw_count}\nNext draw cost: {get_upgrade_cost("draw", draw_upgrade_level)}')
        update_upgrade_buttons()
    else:
        result_label.config(text='Max draw count reached!')

def rebuild_deck():
    global deck
    deck = build_deck()

# Card image cache
card_images = {}
IMAGE_DIR = os.path.join(os.path.dirname(__file__), 'images')
CARD_IMAGE_SIZE = (120, 180)

# Helper to get image directory compatible with PyInstaller
def get_image_dir():
    if hasattr(sys, '_MEIPASS'):
        # PyInstaller: images bundled in _MEIPASS/images
        return os.path.join(sys._MEIPASS, 'images')
    else:
        # Normal: images in script directory
        return os.path.join(os.path.dirname(__file__), 'images')

IMAGE_DIR = get_image_dir()

# Helper to get image filename for a card
def get_card_image_filename(card_name):
    card_name = card_name.replace(' ', '').replace('of', '_').replace('Hearts', 'hearts').replace('Diamonds', 'diamonds').replace('Clubs', 'clubs').replace('Spades', 'spades')
    card_name = card_name.lower()
    return os.path.join(IMAGE_DIR, f'{card_name}.png')

# Helper to load image (with cache)
def load_card_image(card_name):
    filename = get_card_image_filename(card_name)
    if filename in card_images:
        return card_images[filename]
    try:
        img = Image.open(filename).resize(CARD_IMAGE_SIZE)
        photo = ImageTk.PhotoImage(img)
        card_images[filename] = photo
        return photo
    except Exception:
        # Procedurally generate card image
        img = Image.new('RGBA', CARD_IMAGE_SIZE, (255,255,255,255))
        draw = ImageDraw.Draw(img)
        # Parse rank and suit
        rank, suit = None, None
        if ' of ' in card_name:
            parts = card_name.split(' of ')
            rank, suit = parts[0], parts[1]
        else:
            rank, suit = card_name, None
        # Get color
        color = suit_colors.get(suit, '#CCCCCC') if suit else '#FFD700'
        # Draw border
        draw.rectangle([0,0,CARD_IMAGE_SIZE[0]-1,CARD_IMAGE_SIZE[1]-1], outline=color, width=4)
        # Draw suit name and symbol
        font_size = 32
        try:
            font = ImageFont.truetype('arial.ttf', font_size)
        except Exception:
            font = ImageFont.load_default()
        # Suit symbol mapping (only Unicode symbols, no emoji)
        suit_symbols = {
            'Hearts': '♥', 'Diamonds': '♦', 'Clubs': '♣', 'Spades': '♠',
            'Stars': '★', 'Moons': '☾', 'Crowns': '♛', 'Leaves': '♣', 'Suns': '☼', 'Waves': '≈',
            'Shields': '⛨', 'Orbs': '◉', 'Axes': '⛏', 'Spears': '⚔', 'Rings': '◯', 'Cups': '☕',
            'Scrolls': '✉', 'Keys': '⚿', 'Masks': '☻', 'Fangs': '∇', 'Eyes': '◉', 'Wings': '⚚',
            'Roots': '♣', 'Flames': '♨', 'Clouds': '☁', 'Stones': '⬥', 'Webs': '⌘', 'Beams': '≡',
            'Echoes': '♪', 'Frost': '❄', 'Petals': '✿', 'Coins': '◉', 'Swords': '⚔', 'Helms': '⛑',
            'Lanterns': '☼', 'Talons': '⚡', 'Scales': '⚖', 'Spirals': '➰', 'Comets': '☄', 'Vines': '♣',
            'Crystals': '♦', 'Mirrors': '◊', 'Bells': '🔔', 'Horns': '♯', 'Cogs': '⚙', 'Rays': '☀',
            'Dust': '⋱', 'Mists': '〰', 'Roses': '✾', 'Thorns': '†', 'Paws': '☸', 'Hooves': '∩',
            'Antlers': '∩', 'Shells': '◗', 'Fins': '∫', 'Stalks': '∣', 'Seeds': '•', 'Pods': '◉'
        }
        # Draw suit symbol top left, then rank next to it
        if suit:
            symbol = suit_symbols.get(suit, '?')
            draw.text((10, 10), symbol, font=font, fill=color)
            draw.text((10 + font_size + 5, 10), str(rank), font=font, fill=color)
            # Optionally, draw suit name below symbol (smaller font)
            try:
                small_font = ImageFont.truetype('arial.ttf', 16)
            except Exception:
                small_font = ImageFont.load_default()
            draw.text((10, 10 + font_size + 2), suit, font=small_font, fill=color)
        else:
            # For specials, just draw rank top left
            draw.text((10, 10), str(rank), font=font, fill=color)
        # Center delta symbol if rank is delta
        if rank == 'Δ':
            draw.text((CARD_IMAGE_SIZE[0]//2-10, CARD_IMAGE_SIZE[1]//2-10), 'Δ', font=font, fill=color)
        # Optionally, add special card background
        if card_name in specials:
            draw.rectangle([0,0,CARD_IMAGE_SIZE[0],CARD_IMAGE_SIZE[1]], outline='#FFD700', width=8)
            draw.text((CARD_IMAGE_SIZE[0]//2-40, CARD_IMAGE_SIZE[1]//2-20), card_name, font=font, fill='#FFD700')
        photo = ImageTk.PhotoImage(img)
        card_images[filename] = photo
        return photo

# Tkinter GUI setup
root = tk.Tk()
root.title('Card Game')
root.attributes('-fullscreen', True)
root.overrideredirect(True)  # Remove default title bar

# Add card image label to GUI (move after root is defined)
card_image_label = ttk.Label(root)
card_image_label.pack(pady=10)

# Card Art Gallery window
def open_card_gallery():
    gallery_win = tk.Toplevel(root)
    gallery_win.title('Card Art Gallery')
    gallery_win.geometry('800x600')
    ttk.Label(gallery_win, text='Card Art Gallery', font=('Arial', 16)).pack(pady=10)
    canvas = tk.Canvas(gallery_win, width=760, height=500)
    canvas.pack()
    scrollbar = ttk.Scrollbar(gallery_win, orient='vertical', command=canvas.yview)
    scrollbar.pack(side='right', fill='y')
    canvas.configure(yscrollcommand=scrollbar.set)
    frame = ttk.Frame(canvas)
    canvas.create_window((0,0), window=frame, anchor='nw')
    # Gather all unlocked cards and sort by suit then rank
    def rank_sort_key(rank):
        # Try to sort numerically, fallback to string
        try:
            return int(rank) if rank.isdigit() else base_ranks.index(rank)
        except Exception:
            return 9999
    sorted_cards = []
    for suit in sorted(suits, key=lambda s: base_suits.index(s) if s in base_suits else s):
        suit_ranks = sorted(ranks, key=rank_sort_key)
        for rank in suit_ranks:
            sorted_cards.append(f'{rank} of {suit}')
    # Add specials at the end
    sorted_cards += sorted(list(specials.keys()))
    # Display images in a grid
    cols = 5
    for idx, card in enumerate(sorted_cards):
        img = load_card_image(card)
        lbl = ttk.Label(frame, image=img)
        lbl.image = img
        lbl.grid(row=idx//cols*2, column=idx%cols, padx=10, pady=10)
        ttk.Label(frame, text=card, font=('Arial', 10)).grid(row=idx//cols*2+1, column=idx%cols, padx=10)
    frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox('all'))


# Helper to get leaderboard file path compatible with PyInstaller
def get_leaderboard_path():
    if hasattr(sys, '_MEIPASS'):
        # PyInstaller: save in user home directory
        return os.path.join(os.path.expanduser('~'), 'card_game_leaderboard.json')
    else:
        # Normal: save in current directory
        return 'card_game_leaderboard.json'


# Helper to load leaderboard
def load_leaderboard():
    path = get_leaderboard_path()
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

# Helper to save leaderboard
def save_leaderboard(scores):
    path = get_leaderboard_path()
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(scores, f)

# Add score to leaderboard
def add_score_to_leaderboard(name, score):
    scores = load_leaderboard()
    scores.append({'name': name, 'score': score, 'date': time.strftime('%Y-%m-%d %H:%M')})
    scores = sorted(scores, key=lambda x: x['score'], reverse=True)[:10]
    save_leaderboard(scores)

# Leaderboard window
def open_leaderboard():
    win = tk.Toplevel(root)
    win.title('Leaderboard')
    win.geometry('400x400')
    ttk.Label(win, text='Leaderboard', font=('Arial', 16)).pack(pady=10)
    local_scores = load_leaderboard()
    ttk.Label(win, text='Local Scores', font=('Arial', 12)).pack(pady=5)
    for entry in local_scores:
        ttk.Label(win, text=f"{entry['name']}: {entry['score']} ({entry['date']})", font=('Arial', 10)).pack()
    ttk.Label(win, text='Cloud Scores', font=('Arial', 12)).pack(pady=5)

# Move draw_card definition above GUI creation
def draw_card():
    global total_count, ace_multiplier, combo_history, next_upgrade_discount, extra_draw_next
    drawn_cards = []
    ace_count = 0
    value_sum = 0
    special_messages = []
    combo_applied = False
    draw_times = draw_count + (1 if extra_draw_next else 0)
    extra_draw_next = False
    last_drawn = None
    for _ in range(draw_times):
        if random.random() < (skills.get('special_chance', SPECIAL_CARD_CHANCE)) and specials:
            # Draw a special card by weighted chance
            special_name = pick_special_card()
            if special_name in specials:
                drawn_cards.append(special_name)
                msg = special_abilities[special_name]()
                special_messages.append(msg)
                last_drawn = special_name
            else:
                card = random.choice([f'{rank} of {suit}' for suit in suits for rank in ranks])
                drawn_cards.append(card)
                rank = card.split(' ')[0]
                if rank == 'A':
                    ace_count += 1
                if rank in rank_values:
                    value_sum += rank_values[rank]
                last_drawn = card
        elif deck:
            card = random.choice([f'{rank} of {suit}' for suit in suits for rank in ranks])
            drawn_cards.append(card)
            rank = card.split(' ')[0]
            suit = card.split(' ')[-1]
            if rank == 'A':
                ace_count += 1
            if rank in rank_values:
                value_sum += rank_values[rank]
            # Suit effects
            if suit in suit_effects:
                msg = suit_effects[suit]()
                special_messages.append(msg)
            # Skill: Hearts bonus
            if suit == 'Hearts' and skills.get('hearts_bonus', 0) > 0:
                total_count += skills['hearts_bonus']
                special_messages.append(f'Hearts bonus! +{skills["hearts_bonus"]}')
            last_drawn = card
        else:
            break
    ace_multiplier = 2 ** ace_count if ace_count > 0 else 1
    total_count += value_sum * ace_multiplier
    # Combo bonus check
    COMBO_SIZE = skills.get('combo_size', 3)
    # Only keep up to COMBO_SIZE-1 cards in history before this draw
    combo_history = combo_history[-(COMBO_SIZE-1):] + drawn_cards
    # Check for combos only if combo_history has exactly COMBO_SIZE cards
    combo_messages = []
    if len(combo_history) == COMBO_SIZE:
        last_combo = combo_history[:COMBO_SIZE]
        suits_in_combo = [c.split(' ')[-1] for c in last_combo if ' ' in c]
        combo_applied = False
        if len(set(suits_in_combo)) == 1 and len(suits_in_combo) == COMBO_SIZE:
            bonus = COMBO_BONUS * skills['combo_multiplier']
            total_count += bonus
            combo_messages.append(f'Combo! {COMBO_SIZE} {suits_in_combo[0]} cards: +{bonus}')
            combo_applied = True
        colors_in_combo = [suit_colors.get(suit, None) for suit in suits_in_combo]
        def hex_to_name(hex_code):
            color_map = {
                '#FF0000': 'Red', '#222222': 'Black', '#FFFF00': 'Yellow', '#1E90FF': 'Blue', '#FFD700': 'Gold',
                '#228B22': 'Green', '#FFA500': 'Orange', '#808080': 'Gray', '#800080': 'Purple', '#8B4513': 'Brown',
                '#C0C0C0': 'Silver', '#F5F5DC': 'Beige', '#CD7F32': 'Bronze', '#FFFFFF': 'White', '#00FFFF': 'Cyan',
                '#FFC0CB': 'Pink'
            }
            return color_map.get(hex_code, hex_code)
        if len(set(colors_in_combo)) == 1 and None not in colors_in_combo and len(colors_in_combo) == COMBO_SIZE:
            color_bonus = COLOR_COMBO_BONUS * skills['combo_multiplier']
            total_count += color_bonus
            color_name = hex_to_name(colors_in_combo[0])
            combo_messages.append(f'Color Combo! {COMBO_SIZE} {color_name} cards: +{color_bonus}')
            combo_applied = True
        ranks_in_combo = [c.split(' ')[0] for c in last_combo if c.split(' ')[0].isdigit()]
        if len(ranks_in_combo) == COMBO_SIZE:
            sorted_ranks = sorted(map(int, ranks_in_combo))
            if sorted_ranks == list(range(sorted_ranks[0], sorted_ranks[0] + COMBO_SIZE)):
                bonus = COMBO_BONUS * skills['combo_multiplier']
                total_count += bonus
                combo_messages.append(f'Combo! {COMBO_SIZE} consecutive ranks: +{bonus}')
                combo_applied = True
        # Remove the combo cards from history if combo applied, else shift window by one
        if combo_applied:
            combo_history = []
        else:
            combo_history = combo_history[1:]
        # Show all combo messages immediately
        for msg in combo_messages:
            special_messages.append(msg)
    # Build colored text for drawn cards
    def get_card_color(card):
        if card in specials:
            return '#FFD700'  # Special cards: gold
        if suit in suit_colors:
            color = suit_colors.get(suit)
            if color:
                return color
            else:
                return '#CCCCCC'  # fallback for unknown suit
        return '#CCCCCC'  # fallback for unknown card

    drawn_cards_colored = []
    for card in drawn_cards:
        if card in specials:
            suit = None
            color = '#FFD700'  # Special cards: gold
        else:
            suit = None
            # Extract suit by splitting from the right
            parts = card.rsplit(' of ', 1)
            if len(parts) == 2:
                possible_suit = parts[1]
                if possible_suit in suit_colors:
                    suit = possible_suit
                    color = suit_colors[suit]
                else:
                    color = '#CCCCCC'
            else:
                color = '#CCCCCC'
        drawn_cards_colored.append((card, suit, color))

    # Build a string with each card on a new line
    result_text = "Drawn cards:\n" + "\n".join([f"{card}" for card in drawn_cards])
    # Use Canvas for true outlined text
    if hasattr(root, 'result_text_widget'):
        root.result_text_widget.destroy()
    root.result_text_widget = tk.Canvas(root, width=700, height=220, bg=root.cget('bg'), highlightthickness=0, bd=0)
    root.result_text_widget.pack(pady=10)
    result_label.pack_forget()
    canvas = root.result_text_widget
    y = 10
    canvas.create_text(10, y, text="Drawn cards:", anchor='nw', font=('Arial', 14, 'bold'), fill='#FFFFFF')
    y += 28
    def get_outline_color(hex_color):
        hex_color = hex_color.lstrip('#')
        if len(hex_color) == 3:
            hex_color = ''.join([c*2 for c in hex_color])
        r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        brightness = (r*299 + g*587 + b*114) / 1000
        return '#FFFFFF' if brightness < 128 else '#000000'
    for idx, (card, suit, color) in enumerate(drawn_cards_colored):
        outline_color = get_outline_color(color)
        # Draw outline by drawing text at offsets
        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1),(-1,-1),(1,1),(-1,1),(1,-1)]:
            canvas.create_text(20+dx, y+dy, text=card, anchor='nw', font=('Arial', 14, 'bold'), fill=outline_color)
        canvas.create_text(20, y, text=card, anchor='nw', font=('Arial', 14, 'bold'), fill=color)
        y += 28
    # Add ace message
    if ace_count > 0:
        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1),(-1,-1),(1,1),(-1,1),(1,-1)]:
            canvas.create_text(20+dx, y+dy, text=f"{ace_count} Ace(s) drawn! Total multiplied by {ace_multiplier}.", anchor='nw', font=('Arial', 14, 'bold'), fill='#000000')
        canvas.create_text(20, y, text=f"{ace_count} Ace(s) drawn! Total multiplied by {ace_multiplier}.", anchor='nw', font=('Arial', 14, 'bold'), fill='#FFD700')
        y += 28
    # Add each special message on its own line
    for msg in special_messages:
        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1),(-1,-1),(1,1),(-1,1),(1,-1)]:
            canvas.create_text(20+dx, y+dy, text=msg, anchor='nw', font=('Arial', 14, 'bold'), fill='#000000')
        canvas.create_text(20, y, text=msg, anchor='nw', font=('Arial', 14, 'bold'), fill='#FFFFFF')
        y += 28

    total_label.config(text=f'Total: {total_count}')
    next_upgrade_discount = 1.0
    random.shuffle(deck)
    # Show images for all drawn cards (multiple images for upgraded draw counts)
    # Remove previous images if any
    if hasattr(root, 'card_image_frame'):
        root.card_image_frame.destroy()
    root.card_image_frame = ttk.Frame(root)
    root.card_image_frame.pack(pady=10)
    def fade_in_multi(images, labels, step=0):
        alpha = int(255 * (step / 10))
        if alpha > 255:
            alpha = 255
        for idx, card in enumerate(drawn_cards):
            try:
                pil_img = Image.open(get_card_image_filename(card)).resize(CARD_IMAGE_SIZE).convert('RGBA')
                pil_img.putalpha(alpha)
                tk_img = ImageTk.PhotoImage(pil_img)
                labels[idx].config(image=tk_img)
                labels[idx].image = tk_img
            except Exception:
                pass
        if step < 10:
            root.after(30, lambda: fade_in_multi(images, labels, step+1))
    images = []
    labels = []
    for idx, card in enumerate(drawn_cards):
        img = load_card_image(card)
        lbl = ttk.Label(root.card_image_frame, image=img)
        lbl.image = img
        lbl.grid(row=0, column=idx, padx=5)
        images.append(img)
        labels.append(lbl)
    if drawn_cards:
        fade_in_multi(images, labels, 0)
    # Optionally, add score to leaderboard
    add_score_to_leaderboard('Player', total_count)

# Helper to get save path compatible with PyInstaller
def get_save_path():
    if hasattr(sys, '_MEIPASS'):
        # PyInstaller: save in user home directory
        return os.path.join(os.path.expanduser('~'), 'card_game_save.json')
    else:
        # Normal: save in current directory
        return SAVE_FILE

SAVE_FILE = 'card_game_save.json'

# Update save/load functions to use get_save_path()
def save_progress():
    data = {
        'total_count': total_count,
        'draw_count': draw_count,
        'ace_multiplier': ace_multiplier,
        'suit_upgrade_level': suit_upgrade_level,
        'rank_upgrade_level': rank_upgrade_level,
        'special_upgrade_level': special_upgrade_level,
        'draw_upgrade_level': draw_upgrade_level,
        'suits': suits,
        'ranks': ranks,
        'specials': list(specials.keys()),
        'skills': skills,
        'prestige_count': prestige_count,
        'prestige_bonus': prestige_bonus,
    }
    with open(get_save_path(), 'w') as f:
        json.dump(data, f)

def load_progress():
    global total_count, draw_count, ace_multiplier
    global suit_upgrade_level, rank_upgrade_level, special_upgrade_level, draw_upgrade_level
    global suits, ranks, specials, skills, prestige_count, prestige_bonus
    path = get_save_path()
    if os.path.exists(path):
        with open(path, 'r') as f:
            data = json.load(f)
        total_count = data.get('total_count', 0)
        draw_count = data.get('draw_count', 1)
        ace_multiplier = data.get('ace_multiplier', 1)
        suit_upgrade_level = data.get('suit_upgrade_level', 0)
        rank_upgrade_level = data.get('rank_upgrade_level', 0)
        special_upgrade_level = data.get('special_upgrade_level', 0)
        draw_upgrade_level = data.get('draw_upgrade_level', 0)
        suits = data.get('suits', [base_suits[0]])
        ranks = data.get('ranks', [base_ranks[0]])
        specials = {name: special_abilities[name] for name in data.get('specials', []) if name in special_abilities}
        skills.update(data.get('skills', {}))
        prestige_count = data.get('prestige_count', 0)
        prestige_bonus = data.get('prestige_bonus', 0.0)
    # Ensure combo_multiplier includes prestige bonus
    skills['combo_multiplier'] = 1 + prestige_bonus
    rebuild_deck()

def reset_save():
    if os.path.exists(get_save_path()):
        os.remove(get_save_path())
    # Reset game state to defaults
    global total_count, draw_count, ace_multiplier
    global suit_upgrade_level, rank_upgrade_level, special_upgrade_level, draw_upgrade_level
    global suits, ranks, specials, skills, prestige_count, prestige_bonus
    total_count = 0
    draw_count = 1
    ace_multiplier = 1
    suit_upgrade_level = 0
    rank_upgrade_level = 0
    special_upgrade_level = 0
    draw_upgrade_level = 0
    suits = [base_suits[0]]
    ranks = [base_ranks[0]]
    specials = {}
    skills = {
        'combo_multiplier': 1,
        'upgrade_discount': 1.0,
        'special_chance': 0.05,
    }
    prestige_count = 0
    prestige_bonus = 0.0
    rebuild_deck()
    update_upgrade_buttons()
    total_label.config(text='Total: 0')
    draw_count_label.config(text='Cards per draw: 1')
    result_label.config(text='Progress reset!')

# Custom title bar
bar_height = 40
bar_bg = '#222'
bar_fg = '#fff'
title_bar = ttk.Frame(root, height=bar_height)
title_bar.place(x=0, y=0, relwidth=1)
title_bar.configure(style='TitleBar.TFrame')

style = ttk.Style()
style.configure('TitleBar.TFrame', background=bar_bg)
style.configure('TitleBar.TLabel', background=bar_bg, foreground=bar_fg, font=('Arial', 14, 'bold'))
style.configure('TitleBar.TButton', background=bar_bg, foreground=bar_fg)

# Title label
title_label = ttk.Label(title_bar, text='Card Game', style='TitleBar.TLabel')
title_label.pack(side='left', padx=10)

# Add Card Gallery button to title bar
gallery_btn = ttk.Button(title_bar, text='Card Gallery', style='TitleBar.TButton', command=open_card_gallery)
gallery_btn.pack(side='left', padx=5)

# Leaderboard button
leaderboard_btn = ttk.Button(title_bar, text='Leaderboard', style='TitleBar.TButton', command=open_leaderboard)
leaderboard_btn.pack(side='left', padx=5)

# Add skill tree button to title bar
skill_btn = ttk.Button(title_bar, text='Skill Tree', style='TitleBar.TButton', command=open_skill_tree)
skill_btn.pack(side='left', padx=5)

# Add save/load/reset buttons to title bar
save_btn = ttk.Button(title_bar, text='Save', style='TitleBar.TButton', command=save_progress)
save_btn.pack(side='left', padx=5)
load_btn = ttk.Button(title_bar, text='Load', style='TitleBar.TButton', command=load_progress)
load_btn.pack(side='left', padx=5)
reset_btn = ttk.Button(title_bar, text='Reset', style='TitleBar.TButton', command=reset_save)
reset_btn.pack(side='left', padx=5)

# Prestige button
def show_prestige_info():
    result_label.config(text=f'Prestige: {prestige_count} | Combo Multiplier Bonus: +{prestige_bonus:.1f}')
prestige_btn = ttk.Button(title_bar, text='Prestige', style='TitleBar.TButton', command=prestige)
prestige_btn.pack(side='left', padx=5)
prestige_info_btn = ttk.Button(title_bar, text='Prestige Info', style='TitleBar.TButton', command=show_prestige_info)
prestige_info_btn.pack(side='left', padx=5)

# Clock label (rightmost)
clock_label = ttk.Label(title_bar, style='TitleBar.TLabel')
clock_label.pack(side='right', padx=10)

def update_clock():
    now = time.strftime('%H:%M:%S')
    clock_label.config(text=now)
    root.after(1000, update_clock)
update_clock()

# Minimize and close buttons (rightmost)
btn_frame = ttk.Frame(title_bar, style='TitleBar.TFrame')
btn_frame.pack(side='right', padx=5)

def minimize():
    root.iconify()

def close():
    root.destroy()

min_btn = ttk.Button(btn_frame, text='_', width=3, command=minimize, style='TitleBar.TButton')
min_btn.pack(side='left', padx=2)
close_btn = ttk.Button(btn_frame, text='X', width=3, command=close, style='TitleBar.TButton')
close_btn.pack(side='left', padx=2)

# Move window by dragging title bar
_drag_data = {'x': 0, 'y': 0}
def start_move(event):
    _drag_data['x'] = event.x
    _drag_data['y'] = event.y
def do_move(event):
    x = root.winfo_x() + event.x - _drag_data['x']
    y = root.winfo_y() + event.y - _drag_data['y']
    root.geometry(f'+{x}+{y}')
title_bar.bind('<Button-1>', start_move)
title_bar.bind('<B1-Motion>', do_move)

result_label = ttk.Label(root, text='Click to draw a card', font=('Arial', 14))
result_label.pack(pady=10)

total_label = ttk.Label(root, text='Total: 0', font=('Arial', 12))
total_label.pack(pady=5)

draw_count_label = ttk.Label(root, text=f'Cards per draw: {draw_count}', font=('Arial', 12))
draw_count_label.pack(pady=5)

draw_button = ttk.Button(root, text='Draw Card(s)', command=draw_card)
draw_button.pack(pady=10)

# Example upgrade buttons (add more as needed)
upgrade_frame = ttk.Frame(root)
upgrade_frame.pack(pady=10)

add_suit_btn = ttk.Button(upgrade_frame, command=add_suit)
add_suit_btn.pack(side='left', padx=5)

add_rank_btn = ttk.Button(upgrade_frame, command=add_rank)
add_rank_btn.pack(side='left', padx=5)

add_special_btn = ttk.Button(upgrade_frame, command=add_special_card)
add_special_btn.pack(side='left', padx=5)

upgrade_draw_btn = ttk.Button(upgrade_frame, command=upgrade_draw_count)
upgrade_draw_btn.pack(side='left', padx=5)

update_upgrade_buttons()

sv_ttk.set_theme("dark")

# Load progress on startup
load_progress()

# Autosave interval in milliseconds

# Use skill for autosave interval
AUTOSAVE_INTERVAL = skills.get('autosave_speed', 60000)

def autosave():
    save_progress()
    result_label.config(text='Autosave successful!')
    # Update interval from skill
    interval = skills.get('autosave_speed', 60000)
    root.after(interval, autosave)

# Start autosave loop after GUI is initialized
root.after(AUTOSAVE_INTERVAL, autosave)

SPACEBAR_COOLDOWN = 1000  # milliseconds
spacebar_ready = True

def spacebar_cooldown():
    global spacebar_ready
    spacebar_ready = True
    result_label.config(text='Spacebar ready!')

def on_spacebar(event):
    global spacebar_ready
    if spacebar_ready:
        draw_card()
        spacebar_ready = False
        root.after(SPACEBAR_COOLDOWN, spacebar_cooldown)
    else:
        result_label.config(text='Spacebar on cooldown!')

root.bind('<space>', on_spacebar)

root.mainloop()