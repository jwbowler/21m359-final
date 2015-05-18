together_we_are_structure = {
    'bpm': 128,
    'bar0_frame': 2430,
    'sections': (
        (4 * 32, 'Intro'),
        (4 * 4, 'Pre-verse'),

        (4 * 16, 'Verse 1'),
        (4 * 4, 'Build 1'),
        (4 * 24, 'Drop 1'),

        (4 * 4, 'Pre-breakdown'),
        (4 * 24, 'Breakdown'),

        (4 * 8, 'Verse 2'),
        (4 * 8, 'Build 2'),
        (4 * 24, 'Drop 2'),

        (4 * 32, 'Outro'),
        (4 * 8, 'Trail')
    )
}

lionhearted_structure = {
    'bpm': 128,
    'bar0_frame': 10900,
    'sections': (
        (4 * 16, 'Verse 1a'),
        (4 * 16, 'Verse 1b'),
        (4 * 8, 'Build 1'),
        (4 * 16, 'Drop 1'),

        (4 * 16, 'Verse 2a'),
        (4 * 16, 'Verse 2b'),
        (4 * 8, 'Build 2'),
        (4 * 16, 'Drop 2'),

        (4 * 4, 'Trail')
    )
}

days_with_you_structure = {
    'bpm': 90,
    'bar0_frame': 994268 - 29400 * 32,
    'sections': (
        (4 * 8, '1'),
        (4 * 8, '2'),
        (4 * 8, '3'),
        (4 * 8, '4'),
        (4 * 8, '5'),
        (4 * 8, '6'),
        (4 * 8, '7'),
        (4 * 8, '8'),
    )
}

inertia_structure = {
    'bpm': 90,
    'bar0_frame': 0,
    'sections': (
        (4 * 8, '1'),
        (4 * 4, '2'),
        (4 * 4, '3'),
        (4 * 8, '4'),
        (4 * 8, '5'),

        (4 * 8, '6'),
        (4 * 8, '7'),
        (4 * 4, '8'),
        (4 * 8, '9'),
        (4 * 8, '10'),

        (4 * 2, '11'),
        (4 * 8, '12'),
        (4 * 8, '13'),
        (4 * 8, '14'),
        (4 * 8, '15')
    )
}

instant_need_structure = {
    'bpm': 90,
    'bar0_frame': 0,
    'sections': (
        (4 * 4, ''),
        (4 * 2, ''),
        (4 * 2, ''),
        (4 * 2, ''),

        (4 * 4, ''),
        (4 * 2, ''),
        (4 * 2, ''),
        (4 * 2, ''),

        (4 * 4, ''),

        (4 * 8, ''),
        (4 * 8, ''),
        (4 * 8, ''),

        (4 * 4, ''),
        (4 * 2, ''),
        (4 * 2, ''),
        (4 * 2, ''),

        (4 * 4, ''),
        (4 * 2, ''),
        (4 * 2, ''),
        (4 * 2, ''),

        (4 * 4, ''),
        (4 * 2, ''),
        (4 * 2, ''),
        (4 * 2, ''),

        (4 * 4, ''),
        (4 * 2, ''),
        (4 * 2, ''),
        (4 * 2, ''),

        (4 * 8, ''),
        (4 * 8, ''),

        (4 * 1, '')
    )
}

poison_structure = {
    'bpm': 90,
    'bar0_frame': 8816,
    'sections': (
        (4 * 8, ''),
        (4 * 8, ''),
        (4 * 8, ''),
        (4 * 2, ''),

        (4 * 8, ''),
        (4 * 4, ''),

        (4 * 8, ''),
        (4 * 8, ''),
        (4 * 8, ''),

        (4 * 8, ''),
    )
}

together_structure = {
    'bpm': 90,
    'bar0_frame': 816,
    'sections': (
        (4 * 1, ''),
        (4 * 4, ''),
        (4 * 8, ''),
        (4 * 8, ''),
        (4 * 8, ''),
        (4 * 8, ''),
        (4 * 4, ''),
        (4 * 2, ''),
        (4 * 8, ''),
    )
}

forever_structure = {
    'bpm': 90,
    'bar0_frame': 20286,
    'sections': (
        (4 * 4, ''),
        (4 * 4, ''),
        (4 * 8, ''),
        (4 * 8, ''),
        (4 * 8, ''),
        (4 * 4, ''),
        (4 * 8, ''),
        (4 * 8, ''),
        (4 * 8, ''),
        (4 * 8, ''),
        (4 * 8, ''),
        (4 * 8, ''),
        (4 * 8, ''),
    )
}

structures = {
    'together-we-are': together_we_are_structure,
    'lionhearted': lionhearted_structure,
    'days-with-you': days_with_you_structure,
    'inertia': inertia_structure,
    'instant-need': instant_need_structure,
    'poison': poison_structure,
    'together': together_structure,
    'forever': forever_structure
}
