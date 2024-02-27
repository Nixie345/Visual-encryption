import pygame
from pygame.locals import *
import numpy as np
from PIL import Image
import csv
import os



# Turns image into an array of binary numbers  
def convert_image_to_binary(image_path):
    img = Image.open(image_path)
    img_rgba = img.convert('RGBA')
    data = np.array(img_rgba)
    red, green, blue, alpha = data[:,:,0], data[:,:,1], data[:,:,2], data[:,:,3]
    mask = (red != 255) | (green != 255) | (blue != 255)  # Pixels that are not white
    data[:,:,3] = np.where(mask, 255, 0)  # Set alpha channel to 0 for white pixels
    img_rgba = Image.fromarray(data)
    binary_matrix = np.array(img_rgba)[:,:,3] // 255  # Convert to binary matrix
    return binary_matrix

# Generates a random key 
def generate_key(binary_matrix):
    key = np.random.randint(2, size=binary_matrix.shape)
    return key

# Uses key to encrypt the given image
def encrypt_message(binary_matrix, key):
    encrypted_matrix = np.logical_xor(binary_matrix, key).astype(int)
    return encrypted_matrix

# Exports the CSV to the given folder 
def export_to_csv(matrix, folder_path, filename):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    
    file_path = os.path.join(folder_path, filename)
    
    with open(file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')  # Specify the delimiter as comma
        for row in matrix:
            writer.writerow(row)
    print(f"Matrix successfully exported to '{file_path}'.")
WATERMARK_TEXT = "nix made this"
WATERMARK_COLOR = (200, 200, 200)
# Creates an image from the binary files of the CSV
def create_image_from_csv(csv_file, output_file):
    with open(csv_file, 'r') as csvfile:
        reader = csv.reader(csvfile)
        matrix = []
        for row in reader:
            matrix.append([int(val) for val in row])

    # Convert matrix to numpy array
    matrix = np.array(matrix)

    # Create a new RGBA image with transparency
    img = Image.new("RGBA", (matrix.shape[1], matrix.shape[0]), (255, 255, 255, 0))
    
    # Iterate through each pixel in the image
    for y in range(img.height):
        for x in range(img.width):
            if matrix[y, x] == 1:
                img.putpixel((x, y), (0, 0, 0, 255))  # Set black color for value 1

    # Save the image as PNG file
    img.save(output_file, format='PNG')
    print(f"PNG image successfully created from '{csv_file}' and saved as '{output_file}'.")

def main():
    # Ask for locations of important files
    input_image_path = input("Enter the path to the input image: ").strip()
    export_folder = input("Enter the path to the folder where you want to export the files: ").strip()

    binary_matrix = convert_image_to_binary(input_image_path)
    key = generate_key(binary_matrix)
    encrypted_matrix = encrypt_message(binary_matrix, key)

    export_to_csv(encrypted_matrix, export_folder, 'encrypted_matrix.csv')
    export_to_csv(key, export_folder, 'encryption_key.csv')
    
    create_image_from_csv(os.path.join(export_folder, 'encrypted_matrix.csv'), os.path.join(export_folder, 'encrypted_matrix.png'))
    create_image_from_csv(os.path.join(export_folder, 'encryption_key.csv'), os.path.join(export_folder, 'encryption_key.png'))

    # Initialize Pygame
    pygame.init()

    # Set up the screen
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 800
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Player')

    # Load the images
    message_img = pygame.image.load(os.path.join(export_folder, 'encrypted_matrix.png'))
    key_img = pygame.image.load(os.path.join(export_folder, 'encryption_key.png'))

    # Resize images
    message_img = pygame.transform.scale(message_img, (500, 500))  # Resize message image
    key_img = pygame.transform.scale(key_img, (500, 500))  # Resize key image

    # Set initial positions closer to the center
    message_pos = np.array([200,200])
    key_pos = np.array([200, 00])
    font = pygame.font.SysFont('Arial', 10)

    # Main game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN:
                if event.key == K_UP:
                    message_pos[1] -= 10
                elif event.key == K_DOWN:
                    message_pos[1] += 10
                elif event.key == K_LEFT:
                    message_pos[0] -= 10
                elif event.key == K_RIGHT:
                    message_pos[0] += 10
                elif event.key == K_w:
                    key_pos[1] -= 10
                elif event.key == K_s:
                    key_pos[1] += 10
                elif event.key == K_a:
                    key_pos[0] -= 10
                elif event.key == K_d:
                    key_pos[0] += 10
                elif event.key == K_END:
                    pygame.quit()
                

        # Clear the screen
        screen.fill((255, 255, 255))

        # Blit the images onto the screen
        screen.blit(message_img, message_pos)
        screen.blit(key_img, key_pos)

        # Render and blit the watermark text
        text_surface = font.render(WATERMARK_TEXT, True, WATERMARK_COLOR)   
        screen.blit(text_surface, (20, 10))  # Adjust position as needed

        # Update the display
        pygame.display.flip()

if __name__ == "__main__":
    main()
