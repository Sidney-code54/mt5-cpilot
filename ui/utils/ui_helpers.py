def format_strategy(response_text):
    # You can improve this to parse structured GPT output
    return {
        'description': response_text,
        'risk': '1%',
        'sl': '1.09450',
        'tp': '1.09800',
        'lot': '0.05'
    }
