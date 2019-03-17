import re


def series_info(line):
    patterns = [
        r'''
        (?ix)(?:s|^)\s*(\d{1,3})\s*(?:e|ep|^)\s*(\d{1,3})
        ''',
        r'''
        (?ix)(\d{1,3})/(\d{1,3})
        ''',
        r'''
        (?ix)()ep(\d{1,3})
        '''
    ]

    season = 0
    episode = 0
    for pattern in patterns:
        matches = re.findall(pattern, line)

        for match in matches:
            if match[0]:
                season = int(match[0])
            episode = int(match[1])

    return {"season": season, "episode": episode}


print(series_info("Dawn of a New Era!: Dawn has her very first battle with Nando, a Pokémon bard who's torn between two possible " \
       "paths on his journey. (S10 Ep4)"))
print(series_info("9/10. Documentary series. Twins Imogen and Amelia, who were born with achondroplasia, a form of dwarfism, " \
       "prepare to dance in the prestigious Blackpool Tower Ballroom. [S,AD]"))
print(series_info("As Leah deals with the fallout of Adam's betrayal, some unexpected news further complicates matters. " \
       "The truth is finally exposed over the course of one explosive evening. Ep3	"))