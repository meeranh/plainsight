#!/usr/bin/env python3
"""Generate Gruvbox-themed SVG diagrams for the how-it-works page."""

import os

# Gruvbox colors
COLORS = {
    'bg': '#1d2021',
    'bg_card': '#3c3836',
    'fg': '#ebdbb2',
    'aqua': '#8ec07c',
    'yellow': '#fabd2f',
    'purple': '#d3869b',
    'green': '#b8bb26',
    'orange': '#fe8019',
}

counter = 0

def get_id():
    global counter
    counter += 1
    return f"arrow{counter}"

def box(x, y, text, color='aqua', width=120, height=50):
    """Create a rounded rectangle with text."""
    c = COLORS[color]
    return f'''<g>
    <rect x="{x}" y="{y}" width="{width}" height="{height}" rx="8" ry="8"
          fill="{COLORS['bg_card']}" stroke="{c}" stroke-width="2"/>
    <text x="{x + width/2}" y="{y + height/2 + 5}"
          fill="{COLORS['fg']}" text-anchor="middle" font-family="monospace" font-size="13">{text}</text>
  </g>'''

def arrow(x1, y1, x2, y2, dashed=False):
    """Create an arrow line."""
    dash = 'stroke-dasharray="6,4"' if dashed else ''
    aid = get_id()
    return f'''<g>
    <defs>
      <marker id="{aid}" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
        <polygon points="0 0, 10 3.5, 0 7" fill="{COLORS['yellow']}"/>
      </marker>
    </defs>
    <line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}"
          stroke="{COLORS['yellow']}" stroke-width="2" {dash} marker-end="url(#{aid})"/>
  </g>'''

def label(x, y, text, size=11):
    """Create a text label."""
    return f'<text x="{x}" y="{y}" fill="{COLORS["fg"]}" text-anchor="middle" font-family="monospace" font-size="{size}" opacity="0.6">{text}</text>'


def create_encryption_flow():
    """Main encryption pipeline."""
    global counter
    counter = 0
    svg = f'''<svg viewBox="0 0 660 100" xmlns="http://www.w3.org/2000/svg">
  {box(0, 25, "Message", "aqua", 100, 45)}
  {arrow(100, 48, 130, 48)}
  {box(140, 25, "ML-KEM", "green", 90, 45)}
  {arrow(230, 48, 260, 48)}
  {box(270, 25, "AES-256", "purple", 90, 45)}
  {arrow(360, 48, 390, 48)}
  {box(400, 25, "LSB Embed", "yellow", 100, 45)}
  {arrow(500, 48, 530, 48)}
  {box(540, 25, "Stego Image", "orange", 110, 45)}

  {label(185, 15, "public key")}
  {arrow(185, 18, 185, 25, dashed=True)}
</svg>'''
    return svg


def create_decryption_flow():
    """Main decryption pipeline."""
    global counter
    counter = 0
    svg = f'''<svg viewBox="0 0 660 100" xmlns="http://www.w3.org/2000/svg">
  {box(0, 25, "Stego Image", "orange", 110, 45)}
  {arrow(110, 48, 140, 48)}
  {box(150, 25, "LSB Extract", "yellow", 100, 45)}
  {arrow(250, 48, 280, 48)}
  {box(290, 25, "ML-KEM", "green", 90, 45)}
  {arrow(380, 48, 410, 48)}
  {box(420, 25, "AES-256", "purple", 90, 45)}
  {arrow(510, 48, 540, 48)}
  {box(550, 25, "Message", "aqua", 100, 45)}

  {label(335, 15, "private key")}
  {arrow(335, 18, 335, 25, dashed=True)}
</svg>'''
    return svg


def create_keygen():
    """Key generation diagram."""
    global counter
    counter = 0
    svg = f'''<svg viewBox="0 0 480 100" xmlns="http://www.w3.org/2000/svg">
  {box(0, 27, "RECEIVER", "aqua", 100, 45)}
  {arrow(100, 50, 130, 50)}
  {box(140, 27, "ML-KEM keygen", "green", 130, 45)}
  {arrow(270, 40, 320, 20)}
  {arrow(270, 60, 320, 80)}
  {box(330, 0, "Public Key", "yellow", 110, 40)}
  {box(330, 60, "Private Key", "purple", 110, 40)}
</svg>'''
    return svg


def create_encapsulation():
    """Key encapsulation diagram."""
    global counter
    counter = 0
    svg = f'''<svg viewBox="0 0 500 100" xmlns="http://www.w3.org/2000/svg">
  {box(0, 27, "Public Key", "yellow", 110, 45)}
  {arrow(110, 50, 140, 50)}
  {box(150, 27, "ML-KEM encap", "green", 125, 45)}
  {arrow(275, 40, 320, 18)}
  {arrow(275, 60, 320, 82)}
  {box(330, 0, "Shared Secret", "aqua", 120, 36)}
  {box(330, 62, "KEM Ciphertext", "purple", 120, 36)}
</svg>'''
    return svg


def create_symmetric_encryption():
    """Symmetric encryption diagram."""
    global counter
    counter = 0
    svg = f'''<svg viewBox="0 0 480 120" xmlns="http://www.w3.org/2000/svg">
  {box(0, 0, "Shared Secret", "aqua", 115, 40)}
  {arrow(115, 20, 145, 20)}
  {box(155, 0, "HKDF", "green", 70, 40)}
  {arrow(225, 20, 255, 50)}

  {box(0, 75, "Message", "yellow", 90, 40)}
  {arrow(90, 95, 255, 65)}

  {box(265, 40, "AES-256-GCM", "purple", 115, 45)}
  {arrow(380, 62, 410, 62)}
  {box(420, 42, "Ciphertext", "orange", 100, 40)}
</svg>'''
    return svg


def create_steganography():
    """Steganography embedding diagram."""
    global counter
    counter = 0
    svg = f'''<svg viewBox="0 0 500 120" xmlns="http://www.w3.org/2000/svg">
  {box(0, 0, "KEM Ciphertext", "purple", 120, 40)}
  {arrow(120, 20, 160, 50)}

  {box(0, 75, "Ciphertext", "orange", 100, 40)}
  {arrow(100, 95, 160, 65)}

  {box(170, 40, "Combine", "green", 85, 40)}
  {arrow(255, 60, 285, 60)}
  {box(295, 40, "LSB Embed", "yellow", 100, 40)}
  {arrow(395, 60, 425, 60)}
  {box(435, 40, "Stego Image", "aqua", 105, 40)}
</svg>'''
    return svg


def create_full_decryption():
    """Complete decryption process."""
    global counter
    counter = 0
    svg = f'''<svg viewBox="0 0 600 100" xmlns="http://www.w3.org/2000/svg">
  {box(0, 27, "Stego Image", "orange", 105, 45)}
  {arrow(105, 50, 130, 50)}
  {box(140, 27, "LSB Extract", "yellow", 95, 45)}
  {arrow(235, 50, 260, 50)}
  {box(270, 27, "ML-KEM", "green", 85, 45)}
  {arrow(355, 50, 380, 50)}
  {box(390, 27, "AES-256-GCM", "purple", 105, 45)}
  {arrow(495, 50, 520, 50)}
  {box(530, 27, "Message", "aqua", 85, 45)}

  {label(312, 15, "private key")}
  {arrow(312, 18, 312, 27, dashed=True)}
</svg>'''
    return svg


def main():
    diagrams = {
        'encryption_flow.svg': create_encryption_flow(),
        'decryption_flow.svg': create_decryption_flow(),
        'keygen.svg': create_keygen(),
        'encapsulation.svg': create_encapsulation(),
        'symmetric_encryption.svg': create_symmetric_encryption(),
        'steganography.svg': create_steganography(),
        'full_decryption.svg': create_full_decryption(),
    }

    for name, svg in diagrams.items():
        with open(name, 'w') as f:
            f.write(svg)
        print(f"Created: {name}")


if __name__ == '__main__':
    main()
