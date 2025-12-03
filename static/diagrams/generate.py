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
    svg = f'''<svg viewBox="0 0 660 120" xmlns="http://www.w3.org/2000/svg">
  {box(0, 50, "Message", "aqua", 100, 45)}
  {arrow(100, 73, 130, 73)}
  {box(140, 50, "ML-KEM", "green", 90, 45)}
  {arrow(230, 73, 260, 73)}
  {box(270, 50, "AES-256", "purple", 90, 45)}
  {arrow(360, 73, 390, 73)}
  {box(400, 50, "LSB Embed", "yellow", 100, 45)}
  {arrow(500, 73, 530, 73)}
  {box(540, 50, "Stego Image", "orange", 110, 45)}

  {label(185, 12, "public key")}
  {arrow(185, 18, 185, 50, dashed=True)}
</svg>'''
    return svg


def create_decryption_flow():
    """Main decryption pipeline."""
    global counter
    counter = 0
    svg = f'''<svg viewBox="0 0 660 120" xmlns="http://www.w3.org/2000/svg">
  {box(0, 50, "Stego Image", "orange", 110, 45)}
  {arrow(110, 73, 140, 73)}
  {box(150, 50, "LSB Extract", "yellow", 100, 45)}
  {arrow(250, 73, 280, 73)}
  {box(290, 50, "ML-KEM", "green", 90, 45)}
  {arrow(380, 73, 410, 73)}
  {box(420, 50, "AES-256", "purple", 90, 45)}
  {arrow(510, 73, 540, 73)}
  {box(550, 50, "Message", "aqua", 100, 45)}

  {label(335, 12, "private key")}
  {arrow(335, 18, 335, 50, dashed=True)}
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
    svg = f'''<svg viewBox="0 0 530 120" xmlns="http://www.w3.org/2000/svg">
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
    svg = f'''<svg viewBox="0 0 550 120" xmlns="http://www.w3.org/2000/svg">
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
    svg = f'''<svg viewBox="0 0 625 120" xmlns="http://www.w3.org/2000/svg">
  {box(0, 50, "Stego Image", "orange", 105, 45)}
  {arrow(105, 73, 130, 73)}
  {box(140, 50, "LSB Extract", "yellow", 95, 45)}
  {arrow(235, 73, 260, 73)}
  {box(270, 50, "ML-KEM", "green", 85, 45)}
  {arrow(355, 73, 380, 73)}
  {box(390, 50, "AES-256-GCM", "purple", 105, 45)}
  {arrow(495, 73, 520, 73)}
  {box(530, 50, "Message", "aqua", 85, 45)}

  {label(312, 12, "private key")}
  {arrow(312, 18, 312, 50, dashed=True)}
</svg>'''
    return svg


def create_mlkem_chart():
    """ML-KEM performance bar chart."""
    # Data: KeyGen, Encap, Decap for 512, 768, 1024
    data = {
        '512': (25, 24, 32),
        '768': (43, 40, 52),
        '1024': (69, 64, 77),
    }

    chart_width = 400
    chart_height = 200
    bar_width = 25
    group_gap = 60
    max_val = 80

    svg = f'''<svg viewBox="0 0 450 280" xmlns="http://www.w3.org/2000/svg">
  <!-- Title -->
  <text x="225" y="20" fill="{COLORS['fg']}" text-anchor="middle" font-family="monospace" font-size="14">ML-KEM Performance Comparison</text>

  <!-- Y axis -->
  <line x1="50" y1="40" x2="50" y2="240" stroke="{COLORS['fg']}" stroke-width="1" opacity="0.5"/>
  <text x="25" y="145" fill="{COLORS['fg']}" text-anchor="middle" font-family="monospace" font-size="10" transform="rotate(-90, 25, 145)">Time (μs)</text>

  <!-- Y axis labels -->
  <text x="45" y="244" fill="{COLORS['fg']}" text-anchor="end" font-family="monospace" font-size="9" opacity="0.7">0</text>
  <text x="45" y="194" fill="{COLORS['fg']}" text-anchor="end" font-family="monospace" font-size="9" opacity="0.7">20</text>
  <text x="45" y="144" fill="{COLORS['fg']}" text-anchor="end" font-family="monospace" font-size="9" opacity="0.7">40</text>
  <text x="45" y="94" fill="{COLORS['fg']}" text-anchor="end" font-family="monospace" font-size="9" opacity="0.7">60</text>
  <text x="45" y="44" fill="{COLORS['fg']}" text-anchor="end" font-family="monospace" font-size="9" opacity="0.7">80</text>

  <!-- Grid lines -->
  <line x1="50" y1="190" x2="420" y2="190" stroke="{COLORS['fg']}" stroke-width="0.5" opacity="0.2"/>
  <line x1="50" y1="140" x2="420" y2="140" stroke="{COLORS['fg']}" stroke-width="0.5" opacity="0.2"/>
  <line x1="50" y1="90" x2="420" y2="90" stroke="{COLORS['fg']}" stroke-width="0.5" opacity="0.2"/>

  <!-- X axis -->
  <line x1="50" y1="240" x2="420" y2="240" stroke="{COLORS['fg']}" stroke-width="1" opacity="0.5"/>
'''

    x_positions = [100, 210, 320]
    variants = ['512', '768', '1024']
    colors = [COLORS['aqua'], COLORS['green'], COLORS['purple']]

    for i, (variant, x_base) in enumerate(zip(variants, x_positions)):
        keygen, encap, decap = data[variant]

        # Calculate bar heights (scale to chart)
        h_keygen = (keygen / max_val) * 200
        h_encap = (encap / max_val) * 200
        h_decap = (decap / max_val) * 200

        # KeyGen bar
        svg += f'''  <rect x="{x_base}" y="{240 - h_keygen}" width="{bar_width}" height="{h_keygen}" fill="{COLORS['aqua']}" opacity="0.9"/>
  <text x="{x_base + bar_width/2}" y="{235 - h_keygen}" fill="{COLORS['fg']}" text-anchor="middle" font-family="monospace" font-size="8">{keygen}</text>
'''
        # Encap bar
        svg += f'''  <rect x="{x_base + 30}" y="{240 - h_encap}" width="{bar_width}" height="{h_encap}" fill="{COLORS['green']}" opacity="0.9"/>
  <text x="{x_base + 30 + bar_width/2}" y="{235 - h_encap}" fill="{COLORS['fg']}" text-anchor="middle" font-family="monospace" font-size="8">{encap}</text>
'''
        # Decap bar
        svg += f'''  <rect x="{x_base + 60}" y="{240 - h_decap}" width="{bar_width}" height="{h_decap}" fill="{COLORS['purple']}" opacity="0.9"/>
  <text x="{x_base + 60 + bar_width/2}" y="{235 - h_decap}" fill="{COLORS['fg']}" text-anchor="middle" font-family="monospace" font-size="8">{decap}</text>
'''
        # X label
        svg += f'''  <text x="{x_base + 45}" y="255" fill="{COLORS['fg']}" text-anchor="middle" font-family="monospace" font-size="10">ML-KEM-{variant}</text>
'''

    # Legend
    svg += f'''
  <rect x="120" y="265" width="12" height="12" fill="{COLORS['aqua']}" opacity="0.9"/>
  <text x="137" y="275" fill="{COLORS['fg']}" font-family="monospace" font-size="9">KeyGen</text>

  <rect x="195" y="265" width="12" height="12" fill="{COLORS['green']}" opacity="0.9"/>
  <text x="212" y="275" fill="{COLORS['fg']}" font-family="monospace" font-size="9">Encap</text>

  <rect x="265" y="265" width="12" height="12" fill="{COLORS['purple']}" opacity="0.9"/>
  <text x="282" y="275" fill="{COLORS['fg']}" font-family="monospace" font-size="9">Decap</text>
</svg>'''
    return svg


def create_lsb_diagram():
    """LSB embedding visualization."""
    svg = f'''<svg viewBox="0 0 500 180" xmlns="http://www.w3.org/2000/svg">
  <!-- Title -->
  <text x="250" y="20" fill="{COLORS['fg']}" text-anchor="middle" font-family="monospace" font-size="13">LSB Embedding Example</text>

  <!-- Original byte section -->
  <text x="20" y="55" fill="{COLORS['fg']}" font-family="monospace" font-size="11">original pixel (red = 180):</text>
'''
    # Original byte: 10110100 (180)
    original = [1, 0, 1, 1, 0, 1, 0, 0]
    for i, bit in enumerate(original):
        x = 230 + i * 30
        color = COLORS['aqua'] if i < 7 else COLORS['orange']
        svg += f'''  <rect x="{x}" y="40" width="26" height="26" rx="3" fill="{COLORS['bg_card']}" stroke="{color}" stroke-width="2"/>
  <text x="{x + 13}" y="58" fill="{COLORS['fg']}" text-anchor="middle" font-family="monospace" font-size="14">{bit}</text>
'''

    # LSB label
    svg += f'''  <text x="457" y="75" fill="{COLORS['orange']}" font-family="monospace" font-size="9">LSB</text>

  <!-- Arrow and secret bit -->
  <text x="20" y="100" fill="{COLORS['fg']}" font-family="monospace" font-size="11">secret bit to hide:</text>
  <rect x="230" y="85" width="26" height="26" rx="3" fill="{COLORS['yellow']}" stroke="{COLORS['yellow']}" stroke-width="2"/>
  <text x="243" y="103" fill="{COLORS['bg']}" text-anchor="middle" font-family="monospace" font-size="14" font-weight="bold">1</text>

  <!-- Arrow -->
  <path d="M 280 98 L 350 98" stroke="{COLORS['yellow']}" stroke-width="2" fill="none"/>
  <polygon points="350,98 340,93 340,103" fill="{COLORS['yellow']}"/>
  <text x="315" y="90" fill="{COLORS['fg']}" font-family="monospace" font-size="9" opacity="0.7">replace</text>

  <!-- Modified byte section -->
  <text x="20" y="145" fill="{COLORS['fg']}" font-family="monospace" font-size="11">modified pixel (red = 181):</text>
'''
    # Modified byte: 10110101 (181)
    modified = [1, 0, 1, 1, 0, 1, 0, 1]
    for i, bit in enumerate(modified):
        x = 230 + i * 30
        color = COLORS['yellow'] if i == 7 else COLORS['aqua']
        svg += f'''  <rect x="{x}" y="130" width="26" height="26" rx="3" fill="{COLORS['bg_card']}" stroke="{color}" stroke-width="2"/>
  <text x="{x + 13}" y="148" fill="{COLORS['fg']}" text-anchor="middle" font-family="monospace" font-size="14">{bit}</text>
'''

    svg += f'''  <text x="457" y="165" fill="{COLORS['yellow']}" font-family="monospace" font-size="9">modified</text>

  <!-- Explanation -->
  <text x="250" y="175" fill="{COLORS['fg']}" text-anchor="middle" font-family="monospace" font-size="10" opacity="0.6">changing 180 → 181 is invisible to the human eye</text>
</svg>'''
    return svg


def create_psnr_chart():
    """PSNR vs embedding rate chart."""
    # Data points: (capacity%, psnr)
    data = [(10, 61), (25, 57), (50, 54), (75, 52), (100, 51)]

    svg = f'''<svg viewBox="0 0 400 250" xmlns="http://www.w3.org/2000/svg">
  <!-- Title -->
  <text x="200" y="20" fill="{COLORS['fg']}" text-anchor="middle" font-family="monospace" font-size="14">Image Quality vs Embedding Rate</text>

  <!-- Y axis -->
  <line x1="50" y1="40" x2="50" y2="200" stroke="{COLORS['fg']}" stroke-width="1" opacity="0.5"/>
  <text x="20" y="125" fill="{COLORS['fg']}" text-anchor="middle" font-family="monospace" font-size="10" transform="rotate(-90, 20, 125)">PSNR (dB)</text>

  <!-- Y axis labels -->
  <text x="45" y="204" fill="{COLORS['fg']}" text-anchor="end" font-family="monospace" font-size="9" opacity="0.7">40</text>
  <text x="45" y="164" fill="{COLORS['fg']}" text-anchor="end" font-family="monospace" font-size="9" opacity="0.7">50</text>
  <text x="45" y="124" fill="{COLORS['fg']}" text-anchor="end" font-family="monospace" font-size="9" opacity="0.7">60</text>
  <text x="45" y="84" fill="{COLORS['fg']}" text-anchor="end" font-family="monospace" font-size="9" opacity="0.7">70</text>

  <!-- X axis -->
  <line x1="50" y1="200" x2="370" y2="200" stroke="{COLORS['fg']}" stroke-width="1" opacity="0.5"/>
  <text x="210" y="235" fill="{COLORS['fg']}" text-anchor="middle" font-family="monospace" font-size="10">Embedding Capacity (%)</text>

  <!-- X axis labels -->
  <text x="82" y="215" fill="{COLORS['fg']}" text-anchor="middle" font-family="monospace" font-size="9" opacity="0.7">10</text>
  <text x="130" y="215" fill="{COLORS['fg']}" text-anchor="middle" font-family="monospace" font-size="9" opacity="0.7">25</text>
  <text x="210" y="215" fill="{COLORS['fg']}" text-anchor="middle" font-family="monospace" font-size="9" opacity="0.7">50</text>
  <text x="290" y="215" fill="{COLORS['fg']}" text-anchor="middle" font-family="monospace" font-size="9" opacity="0.7">75</text>
  <text x="370" y="215" fill="{COLORS['fg']}" text-anchor="middle" font-family="monospace" font-size="9" opacity="0.7">100</text>

  <!-- Threshold line at 40dB -->
  <line x1="50" y1="200" x2="370" y2="200" stroke="{COLORS['orange']}" stroke-width="1" stroke-dasharray="5,5" opacity="0.7"/>
  <text x="375" y="204" fill="{COLORS['orange']}" font-family="monospace" font-size="8" opacity="0.7">40dB</text>

  <!-- Grid lines -->
  <line x1="50" y1="160" x2="370" y2="160" stroke="{COLORS['fg']}" stroke-width="0.5" opacity="0.2"/>
  <line x1="50" y1="120" x2="370" y2="120" stroke="{COLORS['fg']}" stroke-width="0.5" opacity="0.2"/>
  <line x1="50" y1="80" x2="370" y2="80" stroke="{COLORS['fg']}" stroke-width="0.5" opacity="0.2"/>
'''

    # Calculate points
    def x_pos(cap):
        return 50 + (cap / 100) * 320

    def y_pos(psnr):
        # Scale: 40dB = 200, 70dB = 80
        return 200 - ((psnr - 40) / 30) * 120

    # Draw line connecting points
    points = [(x_pos(cap), y_pos(psnr)) for cap, psnr in data]
    path = f"M {points[0][0]} {points[0][1]}"
    for x, y in points[1:]:
        path += f" L {x} {y}"

    svg += f'''  <path d="{path}" fill="none" stroke="{COLORS['aqua']}" stroke-width="2"/>
'''

    # Draw points
    for cap, psnr in data:
        x = x_pos(cap)
        y = y_pos(psnr)
        svg += f'''  <circle cx="{x}" cy="{y}" r="5" fill="{COLORS['aqua']}"/>
  <text x="{x}" y="{y - 10}" fill="{COLORS['fg']}" text-anchor="middle" font-family="monospace" font-size="9">{psnr}</text>
'''

    svg += '''</svg>'''
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
        'mlkem_chart.svg': create_mlkem_chart(),
        'lsb_diagram.svg': create_lsb_diagram(),
        'psnr_chart.svg': create_psnr_chart(),
    }

    for name, svg in diagrams.items():
        with open(name, 'w') as f:
            f.write(svg)
        print(f"Created: {name}")


if __name__ == '__main__':
    main()
