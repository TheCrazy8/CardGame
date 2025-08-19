import math
import time
import random
import tkinter as tk
from tkinter import ttk
import sv_ttk
import json
import os
import sys
from PIL import Image, ImageTk

# Card deck and upgrade system
base_suits = [
    'Hearts', 'Diamonds', 'Clubs', 'Spades', 'Stars', 'Moons', 'Crowns', 'Leaves', 'Suns', 'Waves',
    'Shields', 'Orbs', 'Axes', 'Spears', 'Rings', 'Cups', 'Scrolls', 'Keys', 'Masks', 'Fangs',
    'Eyes', 'Wings', 'Roots', 'Flames', 'Clouds', 'Stones', 'Webs', 'Beams', 'Echoes', 'Frost',
    'Petals', 'Coins', 'Swords', 'Helms', 'Lanterns', 'Talons', 'Scales', 'Spirals', 'Comets', 'Vines',
    'Crystals', 'Mirrors', 'Bells', 'Horns', 'Cogs', 'Rays', 'Dust', 'Mists', 'Roses', 'Thorns',
    'Paws', 'Hooves', 'Antlers', 'Shells', 'Fins', 'Roots', 'Stalks', 'Seeds', 'Pods', 'Stars2',
    'Moons2', 'Crowns2', 'Leaves2', 'Suns2', 'Waves2', 'Shields2', 'Orbs2', 'Axes2', 'Spears2', 'Rings2'
]
base_ranks = [
    '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A',
    'Z', 'X', 'M', 'P', 'R', 'S', 'T', 'U', 'V', 'W', 'Y', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'L', 'N', 'O',
    'AA', 'BB', 'CC', 'DD', 'EE', 'FF', 'GG', 'HH', 'II', 'JJ', 'KK', 'LL', 'MM', 'NN', 'OO', 'PP', 'QQ', 'RR', 'SS', 'TT',
    '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30'
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
shield_active = False

# Percentages for drawing normal vs special cards
NORMAL_CARD_CHANCE = 0.95  # 95% chance to draw a normal card
SPECIAL_CARD_CHANCE = 0.05  # 5% chance to draw a special card

# Percentages for each special card (must sum to 1.0)
special_card_weights = {
    'Joker': 0.10,
    'Double': 0.10,
    'Reset': 0.10,
    'Bonus': 0.10,
    'Triple': 0.05,
    'Half': 0.10,
    'Steal': 0.10,
    'Gift': 0.10,
    'Shield': 0.05,
    'Bland': 0.20
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
rank_values.update({'J': 11, 'Q': 12, 'K': 13, 'A': 14, '1': 1})

# Special card abilities
special_card_pool = [
    ('Joker', lambda: joker_effect()),
    ('Double', lambda: double_effect()),
    ('Reset', lambda: reset_effect()),
    ('Bonus', lambda: bonus_effect()),
    ('Triple', lambda: triple_effect()),
    ('Half', lambda: half_effect()),
    ('Steal', lambda: steal_effect()),
    ('Gift', lambda: gift_effect()),
    ('Shield', lambda: shield_effect()),
    ('Bland', lambda: bland_effect())
]
special_abilities = {
    'Joker': lambda: joker_effect(),
    'Double': lambda: double_effect(),
    'Reset': lambda: reset_effect(),
    'Bonus': lambda: bonus_effect(),
    'Triple': lambda: triple_effect(),
    'Half': lambda: half_effect(),
    'Steal': lambda: steal_effect(),
    'Gift': lambda: gift_effect(),
    'Shield': lambda: shield_effect(),
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

def reset_effect():
    global total_count, shield_active
    if shield_active:
        shield_active = False
        return 'Reset blocked by Shield!'
    total_count = 0
    return 'Reset! Total set to 0.'

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

def shield_effect():
    global shield_active
    shield_active = True
    return 'Shield! Next Reset blocked.'

def bland_effect():
    global total_count
    total_count -= 100
    return 'Bland! -100 from total.'

# Combo bonus tracking
combo_history = []
COMBO_SIZE = 3
COMBO_BONUS = 100

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
    global draw_count
    draw_count += 1
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
    'draw': 20
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
        result_label.config(text=f'Suit {new_suit} added!')
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
        except ValueError:
            # Use face card values or default to 15 for unknowns
            face_values = {'J': 11, 'Q': 12, 'K': 13, 'A': 14, 'Z': 15, 'X': 16, 'M': 17, 'P': 18, 'R': 19, 'S': 20}
            rank_values[new_rank] = face_values.get(new_rank, 15)
        rank_upgrade_level += 1
        rebuild_deck()
        result_label.config(text=f'Rank {new_rank} added!')
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
        # Find the effect function for the new special card
        for name, func in special_card_pool:
            if name == new_name:
                specials[new_name] = func
                special_abilities[new_name] = func
                break
        special_upgrade_level += 1
        rebuild_deck()
        result_label.config(text=f'Special card {new_name} added!')
        update_upgrade_buttons()
    elif not available_specials:
        result_label.config(text='No more special cards to unlock!')

def upgrade_draw_count():
    global draw_count, draw_upgrade_level
    cost = get_upgrade_cost('draw', draw_upgrade_level)
    if spend_total(cost):
        draw_count += 1
        draw_upgrade_level += 1
        draw_count_label.config(text=f'Cards per draw: {draw_count}')
        result_label.config(text='Draw count upgraded!')
        update_upgrade_buttons()

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
    card_name = card_name.replace(' ', '').replace('of', '_').replace('Hearts', 'heart').replace('Diamonds', 'diamond').replace('Clubs', 'club').replace('Spades', 'spade')
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
        # Fallback: blank image
        img = Image.new('RGBA', CARD_IMAGE_SIZE, (128,128,128,255))
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
    # Gather all unlocked cards
    unlocked_cards = [f'{rank} of {suit}' for suit in suits for rank in ranks] + list(specials.keys())
    # Display images in a grid
    cols = 5
    for idx, card in enumerate(unlocked_cards):
        img = load_card_image(card)
        lbl = ttk.Label(frame, image=img)
        lbl.image = img
        lbl.grid(row=idx//cols*2, column=idx%cols, padx=10, pady=10)
        ttk.Label(frame, text=card, font=('Arial', 10)).grid(row=idx//cols*2+1, column=idx%cols, padx=10)
    frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox('all'))

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
    combo_history.extend(drawn_cards)
    if len(combo_history) >= COMBO_SIZE:
        last_combo = combo_history[-COMBO_SIZE:]
        # Example: all same suit
        suits_in_combo = [c.split(' ')[-1] for c in last_combo if ' ' in c]
        if len(set(suits_in_combo)) == 1 and len(suits_in_combo) == COMBO_SIZE:
            bonus = COMBO_BONUS * skills['combo_multiplier']
            total_count += bonus
            special_messages.append(f'Combo! {COMBO_SIZE} {suits_in_combo[0]} cards: +{bonus}')
            combo_applied = True
        # Example: consecutive ranks (for numeric ranks only)
        ranks_in_combo = [c.split(' ')[0] for c in last_combo if c.split(' ')[0].isdigit()]
        if len(ranks_in_combo) == COMBO_SIZE:
            sorted_ranks = sorted(map(int, ranks_in_combo))
            if sorted_ranks == list(range(sorted_ranks[0], sorted_ranks[0] + COMBO_SIZE)):
                bonus = COMBO_BONUS * skills['combo_multiplier']
                total_count += bonus
                special_messages.append(f'Combo! {COMBO_SIZE} consecutive ranks: +{bonus}')
                combo_applied = True
        # Remove oldest if combo applied
        if combo_applied:
            combo_history = []
        else:
            combo_history = combo_history[-COMBO_SIZE:]
    result_text = f"Drawn cards: {', '.join(drawn_cards)}"
    if ace_count > 0:
        result_text += f"\n{ace_count} Ace(s) drawn! Total multiplied by {ace_multiplier}."
    if special_messages:
        result_text += "\n" + "\n".join(special_messages)
    result_label.config(text=result_text)
    total_label.config(text=f'Total: {total_count}')
    next_upgrade_discount = 1.0
    random.shuffle(deck)
    # Show image for last drawn card
    if last_drawn:
        img = load_card_image(last_drawn)
        card_image_label.config(image=img)
        card_image_label.image = img

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
        'shield_active': shield_active,
        'suit_upgrade_level': suit_upgrade_level,
        'rank_upgrade_level': rank_upgrade_level,
        'special_upgrade_level': special_upgrade_level,
        'draw_upgrade_level': draw_upgrade_level,
        'suits': suits,
        'ranks': ranks,
        'specials': list(specials.keys()),
        'skills': skills,
    }
    with open(get_save_path(), 'w') as f:
        json.dump(data, f)

def load_progress():
    global total_count, draw_count, ace_multiplier, shield_active
    global suit_upgrade_level, rank_upgrade_level, special_upgrade_level, draw_upgrade_level
    global suits, ranks, specials, skills
    path = get_save_path()
    if os.path.exists(path):
        with open(path, 'r') as f:
            data = json.load(f)
        total_count = data.get('total_count', 0)
        draw_count = data.get('draw_count', 1)
        ace_multiplier = data.get('ace_multiplier', 1)
        shield_active = data.get('shield_active', False)
        suit_upgrade_level = data.get('suit_upgrade_level', 0)
        rank_upgrade_level = data.get('rank_upgrade_level', 0)
        special_upgrade_level = data.get('special_upgrade_level', 0)
        draw_upgrade_level = data.get('draw_upgrade_level', 0)
        suits = data.get('suits', [base_suits[0]])
        ranks = data.get('ranks', [base_ranks[0]])
        specials = {name: special_abilities[name] for name in data.get('specials', []) if name in special_abilities}
        skills.update(data.get('skills', {}))
        rebuild_deck()

def reset_save():
    if os.path.exists(get_save_path()):
        os.remove(get_save_path())
    # Reset game state to defaults
    global total_count, draw_count, ace_multiplier, shield_active
    global suit_upgrade_level, rank_upgrade_level, special_upgrade_level, draw_upgrade_level
    global suits, ranks, specials, skills
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
        'combo_multiplier': 1,
        'upgrade_discount': 1.0,
        'special_chance': 0.05,
    }
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
gallery_btn.pack(side='right', padx=5)

# Clock label
clock_label = ttk.Label(title_bar, style='TitleBar.TLabel')
clock_label.pack(side='right', padx=10)

# Add skill tree button to title bar (move here to fix NameError)
skill_btn = ttk.Button(title_bar, text='Skill Tree', style='TitleBar.TButton', command=open_skill_tree)
skill_btn.pack(side='right', padx=5)

def update_clock():
    now = time.strftime('%H:%M:%S')
    clock_label.config(text=now)
    root.after(1000, update_clock)
update_clock()

# Minimize and close buttons
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

# Add save/load buttons to title bar
save_btn = ttk.Button(title_bar, text='Save', style='TitleBar.TButton', command=save_progress)
save_btn.pack(side='right', padx=5)
load_btn = ttk.Button(title_bar, text='Load', style='TitleBar.TButton', command=load_progress)
load_btn.pack(side='right', padx=5)

# Add reset button to title bar
reset_btn = ttk.Button(title_bar, text='Reset', style='TitleBar.TButton', command=reset_save)
reset_btn.pack(side='right', padx=5)

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