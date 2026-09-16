"""Original celestial relief artwork; the host supplies the shared gold paints.

Both fragments use a 0,0 origin and remain inside a radius of 102 SVG units.
They deliberately contain no coin rims, lettering, or locally scoped IDs.
"""

from math import cos, pi, sin


def _ray(index: int) -> str:
    """A chased spear or flame, alternating around the central sun relief."""
    angle = index * 11.25
    if index % 2 == 0:
        outline = "M -4.6 -51 C -6 -64 -3.5 -81 0 -98 C 3.5 -81 6 -64 4.6 -51 Z"
        ridge = "M 0 -55 L 0 -93"
    else:
        outline = "M -3.4 -52 C -9 -63 1 -70 0 -82 C 8 -68 2 -65 3.4 -52 Z"
        ridge = "M -.2 -57 C -3 -65 3 -70 .8 -77"
    return (
        f'<g transform="rotate({angle:g})">'
        f'<path d="{outline}" fill="url(#relief)" stroke="#725021" stroke-width=".8"/>'
        f'<path d="{ridge}" fill="none" stroke="#fff0bd" stroke-width=".65" opacity=".78"/>'
        '</g>'
    )


SUN = (
    '<g stroke-linecap="round" stroke-linejoin="round">'
    '<g filter="url(#reliefShadow)">'
    + ''.join(_ray(index) for index in range(32))
    + '''
    <circle r="49.4" fill="url(#reliefDark)" stroke="#56391b" stroke-width="1.1"/>
    <circle r="47.8" fill="url(#relief)" stroke="#fff0bd" stroke-width=".85"/>
    <circle r="44.9" fill="none" stroke="#be8b40" stroke-width=".7"/>
    <path d="M -39 -21 A 44.1 44.1 0 0 1 27 -35" fill="none" stroke="#fff0bd" stroke-width=".7" opacity=".75"/>
    </g>
    <g fill="none">
      <!-- Chased brow ridges and closed, quietly smiling eyes. -->
      <path d="M -30 -11 C -23 -18 -14 -18 -8 -13 M 8 -13 C 14 -18 23 -18 30 -11"
        stroke="#725021" stroke-width="1.9"/>
      <path d="M -30 -12.5 C -22 -19 -14 -18.5 -8 -14.5 M 8 -14.5 C 14 -18.5 22 -19 30 -12.5"
        stroke="#fff0bd" stroke-width=".95"/>
      <path d="M -28 -5 Q -19 3 -10 -5 M 10 -5 Q 19 3 28 -5"
        stroke="#725021" stroke-width="1.7"/>
      <path d="M -27 -3.6 Q -19 3.8 -11 -3.6 M 11 -3.6 Q 19 3.8 27 -3.6"
        stroke="#fff0bd" stroke-width=".8"/>
      <path d="M -27 -4 L -29 -2 M 27 -4 L 29 -2" stroke="#725021" stroke-width="1"/>
      <!-- Paired highlights make the nose a raised metal ridge. -->
      <path d="M -2 -10 C -1 -3 -3 4 -5 9 Q 0 12 5 9"
        stroke="#725021" stroke-width="1.35"/>
      <path d="M 0 -9 C 1 -2 0 4 -1 7 Q 2 9 5 7.5"
        stroke="#fff0bd" stroke-width=".85"/>
      <path d="M -10 21 Q 0 17 10 21 Q 0 27 -10 21 Z"
        fill="#be8b40" stroke="#725021" stroke-width=".85"/>
      <path d="M -9 20.2 Q 0 16.9 9 20.2 M -5 27 Q 0 29 5 27"
        stroke="#fff0bd" stroke-width=".8"/>
      <path d="M -30 11 Q -25 19 -20 20 M 30 11 Q 25 19 20 20"
        stroke="#be8b40" stroke-width=".85"/>
      <path d="M -31 10 Q -27 18 -23 20 M 31 10 Q 27 18 23 20"
        stroke="#fff0bd" stroke-width=".6" opacity=".8"/>
      <path d="M -15 -33 Q 0 -39 15 -33" stroke="#fff0bd" stroke-width=".8" opacity=".7"/>
      <path d="M -4 -32 L 0 -37 L 4 -32 L 0 -27 Z" stroke="#be8b40" stroke-width=".7"/>
    </g>
    </g>
    '''
)


def _star(x: float, y: float, radius: float, rotation: float = 0) -> str:
    points = []
    for index in range(8):
        angle = (index * pi / 4) - pi / 2
        length = radius if index % 2 == 0 else radius * .23
        points.append(f'{cos(angle) * length:.3f},{sin(angle) * length:.3f}')
    return (
        f'<g transform="translate({x:g} {y:g}) rotate({rotation:g})">'
        f'<polygon points="{" ".join(points)}" fill="url(#fineGold)" '
        'stroke="#725021" stroke-width=".7"/>'
        f'<path d="M 0 {-radius + 1:g} L 0 0 L {radius - 1:g} 0" '
        'fill="none" stroke="#fff0bd" stroke-width=".65"/>'
        '<circle r="1.45" fill="#fff0bd" opacity=".8"/>'
        '</g>'
    )


MOON = (
    '''
    <g stroke-linecap="round" stroke-linejoin="round">
    <!-- Broken celestial circles are incised into the face, below the relief. -->
    <g fill="none" stroke-width=".65">
      <path d="M -89 -29 A 93.6 93.6 0 0 1 -31 -88 M 5 -94 A 94 94 0 0 1 83 -44 M 91 25 A 94.4 94.4 0 0 1 39 86 M 4 95 A 95 95 0 0 1 -69 65"
        stroke="#725021" opacity=".66"/>
      <path d="M -88 -30 A 93.6 93.6 0 0 1 -30 -89 M 6 -95 A 94 94 0 0 1 84 -45 M 92 24 A 94.4 94.4 0 0 1 40 85 M 5 94 A 95 95 0 0 1 -68 64"
        stroke="#fff0bd" opacity=".55"/>
      <path d="M -76 44 C -39 64 58 34 89 -28 M -77 41 C -30 58 56 27 86 -29"
        stroke="#be8b40" opacity=".63"/>
      <path d="M -50 -70 C 13 -80 69 -23 69 45" stroke="#725021" opacity=".44"/>
    </g>
    <g filter="url(#reliefShadow)">
      <path d="M 27 -71 C -12 -88 -72 -59 -77 -11 C -82 39 -42 81 9 73 C -20 58 -36 35 -38 9 C -41 -21 -15 -55 27 -71 Z"
        fill="url(#relief)" stroke="#725021" stroke-width="1.2"/>
      <path d="M 23 -70 C -16 -83 -69 -56 -74 -10 C -79 36 -44 76 3 73"
        fill="none" stroke="#fff0bd" stroke-width="1.05"/>
      <path d="M 16 -66 C -26 -47 -46 -17 -42 11 C -39 38 -25 57 0 70"
        fill="none" stroke="#725021" stroke-width="1.15"/>
      <path d="M 12 -67 C -30 -46 -49 -16 -45 12 C -42 37 -28 56 -8 67"
        fill="none" stroke="#fff0bd" stroke-width=".7" opacity=".76"/>
      <path d="M -4 -71 C -26 -69 -42 -61 -54 -46 M -66 -26 C -73 -1 -70 19 -60 35 M -45 55 Q -29 67 -14 69"
        fill="none" stroke="#be8b40" stroke-width=".75"/>
      <!-- Shallow elliptical craters keep the crescent visibly metallic. -->
      <ellipse cx="-49" cy="-36" rx="7.5" ry="9.3" transform="rotate(31 -49 -36)"
        fill="url(#recess)" stroke="#be8b40" stroke-width=".7" opacity=".75"/>
      <path d="M -52.8 -43.5 Q -59 -36 -51.3 -27.8" fill="none" stroke="#fff0bd" stroke-width=".8"/>
      <ellipse cx="-62" cy="2" rx="6.3" ry="8.1" transform="rotate(-8 -62 2)"
        fill="url(#recess)" stroke="#be8b40" stroke-width=".65" opacity=".65"/>
      <path d="M -64.2 -4.5 Q -69.8 2.5 -64 8.9" fill="none" stroke="#fff0bd" stroke-width=".75"/>
      <ellipse cx="-48" cy="35" rx="8.1" ry="5.7" transform="rotate(34 -48 35)"
        fill="url(#recess)" stroke="#be8b40" stroke-width=".65" opacity=".61"/>
      <path d="M -53.8 30.2 Q -59 34 -47 41" fill="none" stroke="#fff0bd" stroke-width=".65"/>
      <ellipse cx="-29" cy="-58" rx="3" ry="2.2" transform="rotate(-25 -29 -58)" fill="#be8b40" opacity=".65"/>
      <circle cx="-58.5" cy="-16" r="2.05" fill="#be8b40" opacity=".65"/>
      <ellipse cx="-28" cy="57" rx="3.8" ry="2.1" transform="rotate(26 -28 57)" fill="#be8b40" opacity=".65"/>
    </g>
    <g filter="url(#reliefShadow)">
    '''
    + _star(43, -42, 12)
    + _star(71, 9, 15)
    + _star(39, 48, 10)
    + _star(9, 2, 7)
    + _star(-13, -91, 4, 10)
    + '''
    </g>
    <g fill="#ecd18a" stroke="#725021" stroke-width=".35">
      <circle cx="38" cy="-12" r="1.6"/>
      <circle cx="16" cy="35" r="1.35"/>
      <circle cx="66" cy="-62" r="1.2"/>
      <circle cx="63" cy="67" r="1.3"/>
      <circle cx="-22" cy="86" r="1.3"/>
    </g>
    </g>
    '''
)
