import pygame
import random
import matplotlib.pyplot as plt


#MODIFY
GRID_SIZE = 400 #SIZE (may lag)
WINDOW_SIZE = (960, 960)
POPULATION_SIZE = 40  #Anzahl der Pixel auf dem "Land"
TIME_SPEED = 50  #Geschwindigkeit der Simulation (kleinere Werte = schneller)
DAYS = 1000
reproduction_probability = 0.001 #0.2 / 1
death_probability = 0.3  #0.3 / 1

pygame.init()
window = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Pixel life simulation")

num_occupied = min(POPULATION_SIZE, GRID_SIZE * GRID_SIZE)

grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
population = []
dna = []
dna_frequencies = []
day = 0

occupied_positions = random.sample([(x, y) for x in range(GRID_SIZE) for y in range(GRID_SIZE)], num_occupied)
for x, y in occupied_positions:
    population.append((x, y))
    dna.append(random.choice(['RED', 'GREEN', 'BLUE', "WHITE"]))
    grid[x][y] = 1

running = True
clock = pygame.time.Clock()
while running:
    clock.tick(TIME_SPEED) 
    day += 1
    if(day >= DAYS):
        running = False
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    new_population = []
    new_dna = []
    for i in range(len(population)):
        x, y = population[i]
        
        directions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        random.shuffle(directions)
        for direction in directions:
            if direction == 'UP' and y > 0 and grid[x][y - 1] == 0:
                new_x, new_y = x, y - 1
                break
            elif direction == 'DOWN' and y < GRID_SIZE - 1 and grid[x][y + 1] == 0:
                new_x, new_y = x, y + 1
                break
            elif direction == 'LEFT' and x > 0 and grid[x - 1][y] == 0:
                new_x, new_y = x - 1, y
                break
            elif direction == 'RIGHT' and x < GRID_SIZE - 1 and grid[x + 1][y] == 0:
                new_x, new_y = x + 1, y
                break
        else:
            new_x, new_y = x, y 

        if (new_x, new_y) not in new_population:
            new_population.append((new_x, new_y))
            new_dna.append(dna[i])

        if (new_x, new_y) != (x, y):
            if random.random() < reproduction_probability:
                child_positions = []
                for _ in range(2):
                    child_x, child_y = new_x, new_y
                    while (child_x, child_y) in new_population or grid[child_x][child_y] == 1:
                        directions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
                        random.shuffle(directions)
                        for direction in directions:
                            if direction == 'UP' and child_y > 0:
                                child_y -= 1
                                break
                            elif direction == 'DOWN' and child_y < GRID_SIZE - 1:
                                child_y += 1
                                break
                            elif direction == 'LEFT' and child_x > 0:
                                child_x -= 1
                                break
                            elif direction == 'RIGHT' and child_x < GRID_SIZE - 1:
                                child_x += 1
                                break
                        else:
                            break

                    child_positions.append((child_x, child_y))

                new_population.extend(child_positions)
                parent_dna = dna[i]
                child_dna = random.choice([parent_dna, dna[i]])

                new_dna.extend([child_dna] * 2)

    if len(new_population) == 0:
        print("Die Simulation ist beendet.")
        break

    grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    for x, y in new_population:
        grid[x][y] = 1

    window.fill((0, 0, 0))  
    for x, y in new_population:
        pixel_x = x * (WINDOW_SIZE[0] // GRID_SIZE)
        pixel_y = y * (WINDOW_SIZE[1] // GRID_SIZE)

        index = new_population.index((x, y))
        if new_dna[index] == 'RED':
            color = (255, 0, 0)  #Rot
        elif new_dna[index] == 'GREEN':
            color = (0, 255, 0)  #Grün
        elif new_dna[index] == 'BLUE':
            color = (0, 0, 255)  #Blau
        elif new_dna[index] == "WHITE":
            color = (255,255,255) #Weiß

        pygame.draw.rect(window, color, (pixel_x, pixel_y, WINDOW_SIZE[0] // GRID_SIZE, WINDOW_SIZE[1] // GRID_SIZE))

    pygame.display.update()

    print("Population: ", len(new_population))
    counter = {}
    for d in new_dna:
        counter[d] = counter.get(d, 0) + 1
        
    dna_frequencies.append(counter.copy())

    sorted_dna = sorted(counter, key=counter.get, reverse=True)

    for dna in sorted_dna:
        print("DNA:", dna, "Frequency:", counter[dna])

    print("---")
    population = new_population
    dna = new_dna


plt.figure()
for dna in sorted_dna:
    frequencies = [freq[dna] for freq in dna_frequencies]
    plt.plot(frequencies, label=dna)

plt.xlabel("Time")
plt.ylabel("Frequency")
plt.legend()
plt.show()
pygame.quit()
