from random import randint, random
from math import sqrt
from time import sleep
from win32api import GetSystemMetrics
from queue import Queue
from tkinter import DISABLED, NORMAL, Button, Canvas, Label, Tk
from numericUpDown import NumericUpDown


TIME_DELAY = 0.5
NUMBER_OF_NODES = 10
nodes = []
NODE_RADIUS = 20
matrix = [[0 for _ in range(NUMBER_OF_NODES)] for _ in range(NUMBER_OF_NODES)]


def distance(x1, y1, x2, y2):
    return sqrt((x1 - x2)**2 + (y1 - y2)**2)


def generate_node_coordinates():
    for i in range(100):
        x = randint(NODE_RADIUS, canvas_width-NODE_RADIUS)
        y = randint(NODE_RADIUS, canvas_height-NODE_RADIUS)
        is_far_enough = all(distance(x, y, canvas.coords(existing_node[0])[0]+NODE_RADIUS, canvas.coords(existing_node[0])[1]+NODE_RADIUS) > NODE_RADIUS*2 for existing_node in nodes)
        if is_far_enough:
            # Check if the node is too close to any existing links
            too_close = False
            for n1, l1, _ in nodes:
                for n2, l2, _ in nodes:
                    if n1 != n2:
                        x1, y1 = canvas.coords(n1)[0]+10, canvas.coords(n1)[1]+10
                        x2, y2 = canvas.coords(n2)[0]+10, canvas.coords(n2)[1]+10
                        if intersect(x1, y1, x2, y2, x, y, NODE_RADIUS):
                            too_close = True
                            break
                if too_close:
                    break
            if not too_close:
                return x, y
    return None  # Return None ifno valid coordinates are found


def intersect(x1, y1, x2, y2, cx, cy, r):
    dx = x2 - x1
    dy = y2 - y1
    a = dx**2 + dy**2
    b = 2*dx*(x1-cx) + 2*dy*(y1-cy)
    c = cx**2 + cy**2 + x1**2 + y1**2 - 2*(cx*x1 + cy*y1) - r**2
    discriminant = b**2 - 4*a*c
    if discriminant >= 0:
        # check if either endpoint is inside the circle
        if (x1-cx)**2 + (y1-cy)**2 <= r**2 or (x2-cx)**2 + (y2-cy)**2 <= r**2:
            return True
        # check if the line segment intersects the circle
        t = (-b - sqrt(discriminant)) / (2*a)
        if 0 <= t <= 1:
            ix = x1 + t*dx
            iy = y1 + t*dy
            if (ix-cx)**2 + (iy-cy)**2 <= r**2:
                return True
    return False


def add_node():
    button_clear.config(state=NORMAL)
    button_animate.config(state=NORMAL)
    button_find.config(state=NORMAL)
    button_print_matrix.config(state=NORMAL)
    numeric_up_down.update_value()
    for _ in range(numeric_up_down.get()):
        if len(nodes) < NUMBER_OF_NODES: # For cleaner Canvas
            node_coords = generate_node_coordinates()
            while node_coords is None:
                node_coords = generate_node_coordinates()
            x, y = node_coords
            node = canvas.create_oval(x-NODE_RADIUS, y-NODE_RADIUS, x+NODE_RADIUS, y+NODE_RADIUS, fill='lightblue')
            label = canvas.create_text(x,y, text=str(len(nodes) + 1))
            nodes.append((node, label, len(nodes) + 1))
            # Add random links between the new node and all existing nodes
            existing_nodes = nodes[:-1]  # all nodes except the new one
            for existing_node in existing_nodes:
                for i in range(randint(0, 3)):  # adjust the number of links as desired
                    if random() < 1.2:  # adjust the probability as desired
                        # Create the link
                        x1, y1 = canvas.coords(node)[0]+NODE_RADIUS, canvas.coords(node)[1]+NODE_RADIUS
                        x2, y2 = canvas.coords(existing_node[0])[0]+NODE_RADIUS, canvas.coords(existing_node[0])[1]+NODE_RADIUS
                        # Check if the link intersects with any other nodes
                        intersects = False
                        for n1, l1, _ in nodes[:-1]:
                            if n1 != node and n1 != existing_node[0]:
                                x3, y3 = canvas.coords(n1)[0]+10, canvas.coords(n1)[1]+10
                                if intersect(x1, y1, x2, y2, x3, y3, NODE_RADIUS + 10):
                                    intersects = True
                                    break
                        if not intersects:
                            link = canvas.create_line(x1, y1, x2, y2, fill='gray', width=2)
                            canvas.tag_lower(link)  # place the link behind the nodes
                            matrix[existing_node[2] - 1][len(nodes) - 1] = link
                            matrix[len(nodes) - 1][existing_node[2] - 1] = link
    update_nodes()


def clear_graph():
    global matrix
    numeric_up_down.update_value()
    global nodes
    canvas.delete('all')
    nodes = []
    matrix = [[0 for _ in range(NUMBER_OF_NODES)] for _ in range(NUMBER_OF_NODES)]
    lable_bfs_out.config(text='')
    button_clear.config(state=DISABLED)
    button_animate.config(state=DISABLED)
    button_find.config(state=DISABLED)
    button_print_matrix.config(state=DISABLED)


def is_entry_empty(entry): 
    return entry.get().strip() == ""


def find_traversal():
    numeric_up_down.update_value()
    start_node = 0
    text = ''
    n = len(matrix)
    visited = [False]*n
    queue = Queue()

    visited[start_node] = True
    queue.put(start_node)

    while not queue.empty():
        node = queue.get()
        text += str(node + 1) + ' '

        for i in range(n):
            if matrix[node][i] and not visited[i]:
                visited[i] = True
                queue.put(i)
    
    print('Breadth-first search: ' + text)
    lable_bfs_out.config(text = text)


def find_traversal_animation():
    update_nodes()
    numeric_up_down.up_button.config(state=DISABLED)
    numeric_up_down.down_button.config(state=DISABLED)
    button_clear.config(state=DISABLED)
    button_add_node.config(state=DISABLED)
    button_find.config(state=DISABLED)
    button_print_matrix.config(state=DISABLED)
    button_animate.config(state=DISABLED)
    numeric_up_down.update_value()
    start_node = 0 
    text = '' 
    n = len(matrix)
    visited = [False]*n
    queue = Queue()
    
    visited[start_node] = True
    queue.put(start_node)
    sleep(TIME_DELAY)
    
    while not queue.empty():
        node = queue.get()
        text += str(node + 1) + ' '
        canvas.itemconfig(nodes[node][0], fill='lightgreen')
        root.update()
        sleep(TIME_DELAY)
        
        for i in range(n):
            if matrix[node][i] and not visited[i]:
                canvas.itemconfig(matrix[node][i], width=4, fill='black')
                root.update()
                sleep(TIME_DELAY)
                visited[i] = True
                queue.put(i)
                canvas.itemconfig(nodes[i][0], fill='yellow')
                root.update()
                sleep(TIME_DELAY)
                
        lable_bfs_out.config(text=text)
    
    numeric_up_down.up_button.config(state=NORMAL)
    numeric_up_down.down_button.config(state=NORMAL)
    button_clear.config(state=NORMAL)
    button_add_node.config(state=NORMAL)
    button_find.config(state=NORMAL)
    button_print_matrix.config(state=NORMAL)
    button_animate.config(state=NORMAL)


def update_nodes():
    for node in nodes:
        canvas.itemconfig(node[0], fill='lightblue')        
    for row in matrix:
        for element in row:
            if element:
                canvas.itemconfig(element, width=2, fill='gray')


def print_matrix():
    numeric_up_down.update_value()
    print('Adjacency matrix:')
    for row in matrix:
    # iterate over each column in the row and print the value
        for column in row:
            if column != 0:
                print(1, end='\t')
            else:
                print(0, end='\t')
        print()  # print a newline after each row


def create_window():
    global root, canvas, canvas_width, canvas_height, lable_bfs_out, numeric_up_down, button_animate, button_clear, button_print_matrix, button_find, button_add_node

    root=Tk()

    root.title('Random Graph')
    root.config(bg='gray80')
    
    window_width = 660
    window_height = 520
    screen_width = GetSystemMetrics(0)
    screen_height = GetSystemMetrics(1)

    root.geometry(f'{window_width}x{window_height}+{int((screen_width - window_width) / 2)}+{int((screen_height - window_height) / 2)}')
    root.resizable(width=False, height=False)

    canvas_width = 500
    canvas_height = 500
    canvas=Canvas(root,width=canvas_width,height=canvas_height,bg='white')
    canvas.place(x=10,y=10)

    label_add_node=Label(root,text='Add node or clear graph', bg='gray80')
    label_add_node.place(x=520,y=10)

    lable_bfs_out = Label(root, text='', bg='gray80')
    lable_bfs_out.place(x=520, y=90)

    numeric_up_down = NumericUpDown(root, min_value=1, max_value=10, initial_value=1, entry_width=10)
    numeric_up_down.place(x=520, y=30)
    
    button_add_node=Button(root, text='add', command=add_node)
    button_add_node.place(x=520, y=60)

    button_clear = Button(root, text='clear', command=clear_graph, state=DISABLED)
    button_clear.place(x=554, y=60)

    button_find=Button(root, text='Breadth-first search', command=find_traversal, state=DISABLED)
    button_find.place(x=520,y=120)
    
    button_print_matrix = Button(root, text='print adjacency matrix', command=print_matrix, state=DISABLED)
    button_print_matrix.place(x=520, y=150)
    
    button_animate = Button(root, text='animate', command=find_traversal_animation, state=DISABLED)
    button_animate.place(x=520, y=180)

    root.mainloop()


if __name__ == '__main__':
    create_window()