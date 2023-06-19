import pygame
import heapq

# Inicializar Pygame
pygame.init()

# Configuración de la ventana
window_size = (800, 600)
window = pygame.display.set_mode(window_size)
pygame.display.set_caption("Dijkstra Visualization")

# Colores
color_white = (255, 255, 255)
color_black = (0, 0, 0)
color_gray = (128, 128, 128)
color_blue = (0, 0, 255)
color_green = (0, 255, 0)
color_red = (255, 0, 0)

# Fuente
font = pygame.font.Font(None, 24)

# Gráfico y posición de los nodos
graph = {}
node_positions = {}

# Variables para la animación
start_node = None
end_node = None
distances = {}
visited = set()
previous = {}
path = []

# Función para dibujar el gráfico
def draw_graph():
    window.fill(color_white)
    for node, neighbors in graph.items():
        pygame.draw.circle(window, color_black, node_positions[node], 20)
        text = font.render(node, True, color_black)
        text_rect = text.get_rect(center=node_positions[node])
        window.blit(text, text_rect)

        for neighbor, cost in neighbors:
            pygame.draw.line(window, color_gray, node_positions[node], node_positions[neighbor], 2)
            text = font.render(str(cost), True, color_gray)
            text_rect = text.get_rect(center=(node_positions[node][0] + node_positions[neighbor][0]) // 2,
                                      center_y=(node_positions[node][1] + node_positions[neighbor][1]) // 2)
            window.blit(text, text_rect)

    if start_node:
        pygame.draw.circle(window, color_green, node_positions[start_node], 20)
    if end_node:
        pygame.draw.circle(window, color_red, node_positions[end_node], 20)

    for node in visited:
        pygame.draw.circle(window, color_blue, node_positions[node], 20)

    for i in range(len(path) - 1):
        pygame.draw.line(window, color_red, node_positions[path[i]], node_positions[path[i + 1]], 4)

    pygame.display.flip()

# Función para el algoritmo de Dijkstra
def dijkstra():
    global distances, visited, previous, path
    distances = {node: float('inf') for node in graph}
    distances[start_node] = 0
    visited = set()
    previous = {}
    path = []

    queue = [(0, start_node)]

    while queue:
        current_distance, current_node = heapq.heappop(queue)

        if current_node == end_node:
            node = end_node
            while node != start_node:
                path.insert(0, node)
                node = previous[node]
            path.insert(0, start_node)
            return

        if current_node in visited:
            continue

        visited.add(current_node)

        for neighbor, weight in graph[current_node]:
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous[neighbor] = current_node
                heapq.heappush(queue, (distance, neighbor))

# Función principal
def main():
    global start_node, end_node

    running = True
    creating_graph = True
    selecting_start = False
    selecting_end = False
    assigning_cost = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                if creating_graph:
                    node_name = "Node" + str(len(graph) + 1)
                    graph[node_name] = []
                    node_positions[node_name] = pos
                elif selecting_start or selecting_end:
                    for node, position in node_positions.items():
                        if (pos[0] - position[0]) ** 2 + (pos[1] - position[1]) ** 2 <= 400:
                            if selecting_start:
                                start_node = node
                            elif selecting_end:
                                end_node = node
                            selecting_start = False
                            selecting_end = False
                elif assigning_cost:
                    for node, position in node_positions.items():
                        if (pos[0] - position[0]) ** 2 + (pos[1] - position[1]) ** 2 <= 400:
                            if node != assigning_cost:
                                cost_str = input("Enter the cost between {} and {}: ".format(assigning_cost, node))
                                try:
                                    cost = int(cost_str)
                                    graph[assigning_cost].append((node, cost))
                                    graph[node].append((assigning_cost, cost))
                                except ValueError:
                                    print("Invalid input. Cost should be an integer.")
                            assigning_cost = False

        if creating_graph:
            draw_graph()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_s]:
                selecting_start = True
            elif keys[pygame.K_e]:
                selecting_end = True
            elif keys[pygame.K_c]:
                assigning_cost = True
            elif keys[pygame.K_RETURN]:
                creating_graph = False

        elif start_node and end_node:
            dijkstra()
            draw_graph()

    pygame.quit()


# Ejecutar la función principal
main()
