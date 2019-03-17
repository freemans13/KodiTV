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
