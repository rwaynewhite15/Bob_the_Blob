def load_high_score(filename):
    try:
        with open(filename, 'r') as file:
            return int(file.read().strip())
    except FileNotFoundError:
        return 0
    except ValueError:
        return 0

def save_high_score(filename, score):
    with open(filename, 'w') as file:
        file.write(str(score))
