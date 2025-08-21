import os
from PIL import Image, ImageDraw, ImageFont

CARD_IMAGE_SIZE = (120, 180)
border_width = 8
rank_font_size = 56
suit_font_size = 36
images_dir = os.path.join(os.path.dirname(__file__), 'images')

base_suits = [
    'Hearts', 'Diamonds', 'Clubs', 'Spades', 'Stars', 'Moons', 'Crowns', 'Leaves', 'Suns', 'Waves',
    'Shields', 'Orbs', 'Axes', 'Spears', 'Rings', 'Cups', 'Scrolls', 'Keys', 'Masks', 'Fangs',
    'Eyes', 'Wings', 'Roots', 'Flames', 'Clouds', 'Stones', 'Webs', 'Beams', 'Echoes', 'Frost',
    'Petals', 'Coins', 'Swords', 'Helms', 'Lanterns', 'Talons', 'Scales', 'Spirals', 'Comets', 'Vines',
    'Crystals', 'Mirrors', 'Bells', 'Horns', 'Cogs', 'Rays', 'Dust', 'Mists', 'Roses', 'Thorns',
    'Paws', 'Hooves', 'Antlers', 'Shells', 'Fins', 'Roots', 'Stalks', 'Seeds', 'Pods'
]
base_ranks = [
    '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A', 'Δ'
]
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

def generate_card_image(rank, suit):
    img = Image.new('RGBA', CARD_IMAGE_SIZE, (255,255,255,255))
    draw = ImageDraw.Draw(img)
    color = suit_colors.get(suit, '#CCCCCC')
    # Draw border
    for i in range(border_width):
        draw.rectangle([i,i,CARD_IMAGE_SIZE[0]-1-i,CARD_IMAGE_SIZE[1]-1-i], outline=color)
    # Fonts
    try:
        rank_font = ImageFont.truetype('arialbd.ttf', rank_font_size)
    except Exception:
        rank_font = ImageFont.load_default()
    try:
        suit_font = ImageFont.truetype('arial.ttf', suit_font_size)
    except Exception:
        suit_font = ImageFont.load_default()
    # Draw rank top left
    draw.text((18, 10), str(rank), font=rank_font, fill=color)
    # Draw suit symbol bottom right
    symbol = suit_symbols.get(suit, '?')
    w, h = draw.textsize(symbol, font=suit_font)
    draw.text((CARD_IMAGE_SIZE[0]-w-18, CARD_IMAGE_SIZE[1]-h-18), symbol, font=suit_font, fill=color)
    # Center delta symbol if rank is delta
    if rank == 'Δ':
        w, h = draw.textsize('Δ', font=rank_font)
        draw.text(((CARD_IMAGE_SIZE[0]-w)//2, (CARD_IMAGE_SIZE[1]-h)//2), 'Δ', font=rank_font, fill=color)
    return img

def main():
    if not os.path.exists(images_dir):
        os.makedirs(images_dir)
    for suit in base_suits:
        for rank in base_ranks:
            fname = f"{rank}_{suit.lower()}.png"
            path = os.path.join(images_dir, fname)
            img = generate_card_image(rank, suit)
            img.save(path)
            print(f"Saved {path}")

if __name__ == "__main__":
    main()