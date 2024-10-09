class Config:
    default_council = "Nottingham City Council"
    primary_color = "#C0D731"
    secondary_color = "#4A4B4D"
    tab_style = {
        'idle': {
            'borderRadius': '10px',
            'padding': '5px',
            'margin': '5px',
            'marginInline': '5px',
            'display': 'flex',
            'alignItems': 'center',
            'justifyContent': 'center',
            'fontWeight': 'bold',
            'backgroundColor': primary_color,
            'border': 'none',
            'color': secondary_color
        },
        'active': {
            'borderRadius': '10px',
            'padding': '5px',
            'margin': '5px',
            'marginInline': '5px',
            'display': 'flex',
            'alignItems': 'center',
            'justifyContent': 'center',
            'fontWeight': 'bold',
            'border': 'none',
            'textDecoration': 'underline',
            'backgroundColor': primary_color,
            'color': secondary_color
        }
    }
