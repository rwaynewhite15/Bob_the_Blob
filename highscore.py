def load_high_score(filename):
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
            high_score = int(lines[0].strip())
            longest_time = float(lines[1].strip())
            return high_score, longest_time
    except FileNotFoundError:
        return 0, 0.0
    except ValueError:
        return 0, 0.0

def save_high_score(filename, score, time):
    with open(filename, 'w') as file:
        file.write(f"{score}\n")
        file.write(f"{time:.2f}\n")
