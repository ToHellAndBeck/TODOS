import random

def generate_pattern(width, height):
    pattern_chars = ['\\', '/']
    for _ in range(height):
        line = ''.join(random.choice(pattern_chars) for _ in range(width))
        print(line)

if __name__ == "__main__":
    width, height = 80, 20  # Adjust the width and height as needed
    generate_pattern(width, height)

