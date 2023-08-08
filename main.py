import random
import time
import numpy as np
import sys
from PyQt5 import QtWidgets, Qt, QtTest
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class Cell:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.visited = False
        self.walls = [True, True, True, True]


class Maze:
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.grid = []
        for row in range(height):
            arr = []
            for col in range(width):
                arr.append(Cell(row, col))
            self.grid.append(arr)

    def get_neighbours(self, row, col):
        # print(f"Current row and col: {row} {col}")
        neighbours = []
        if row > 0:
            if self.grid[row - 1][col].visited is False:
                neighbours.append(self.grid[row - 1][col])
        if row < self.height - 1:
            if self.grid[row + 1][col].visited is False:
                neighbours.append(self.grid[row + 1][col])
        if col > 0:
            if self.grid[row][col - 1].visited is False:
                neighbours.append(self.grid[row][col - 1])
        if col < self.width - 1:
            if self.grid[row][col + 1].visited is False:
                neighbours.append(self.grid[row][col + 1])
        # for neighbour in neighbours:
        #     print(neighbour.row, neighbour.col)
        return neighbours

    def get_visitable_neighbours(self, row, col):
        # print(f"Current row and col: {row} {col}")
        neighbours = []
        if row > 0:
            if self.grid[row - 1][col].visited is False and self.grid[row - 1][col].walls[2] is False:
                neighbours.append(self.grid[row - 1][col])
        if row < self.height - 1:
            if self.grid[row + 1][col].visited is False and self.grid[row + 1][col].walls[0] is False:
                neighbours.append(self.grid[row + 1][col])
        if col > 0:
            if self.grid[row][col - 1].visited is False and self.grid[row][col - 1].walls[1] is False:
                neighbours.append(self.grid[row][col - 1])
        if col < self.width - 1:
            if self.grid[row][col + 1].visited is False and self.grid[row][col + 1].walls[3] is False:
                neighbours.append(self.grid[row][col + 1])
        # for neighbour in neighbours:
        #     print(neighbour.row, neighbour.col)
        return neighbours

    def get_random_neighbour(self, row, col):
        neighbours = self.get_neighbours(row, col)
        if len(neighbours) > 0:
            return random.choice(neighbours)
        else:
            return None

    def reset_visited(self):
        for row in range(self.height):
            for col in range(self.width):
                self.grid[row][col].visited = False

    def reset_walls(self):
        for row in range(self.height):
            for col in range(self.width):
                self.grid[row][col].walls = [True, True, True, True]

    def reset_maze(self):
        self.reset_walls()
        self.reset_visited()


class Grid(QWidget):
    def __init__(self, height, width):
        super().__init__()
        self.maze = Maze(height, width)
        self.maze.grid[0][0].visited = True
        self.initUI()
        self.start = self.maze.grid[0][0]
        self.exit = self.maze.grid[height - 1][width - 1]
        self.maze_generated = False

    def initUI(self):
        self.setWindowTitle('Maze Generator')
        self.setGeometry(300, 50, 1300, 900)
        # Create the main layout
        main_layout = QHBoxLayout(self)

        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(0)  # Set spacing to 0

        rows = self.maze.height
        cols = self.maze.width
        for row in range(rows):
            for col in range(cols):
                label = QLabel()
                # Set different border styles for cells
                label.setStyleSheet('border: 1px solid black;background-color: #FFFFFF')  # Orange color

                self.grid_layout.addWidget(label, row, col)

        side_layout = QVBoxLayout()

        self.generate_maze_btn = QPushButton('Generate Maze', self)
        self.generate_maze_btn.setFont(QFont('Times', 15))
        self.generate_maze_btn.setFixedSize(250, 200)
        self.generate_maze_btn.clicked.connect(self.generate_maze)
        side_layout.addWidget(self.generate_maze_btn)

        vertical_layout_start = QVBoxLayout()
        start_lbl = QLabel('Move Starting Point', self)
        start_lbl.setFont(QFont('Times', 15))
        start_lbl.setAlignment(Qt.AlignCenter)
        start_lbl.setFixedHeight(50)
        vertical_layout_start.addWidget(start_lbl)
        horizontal_layout_start = QHBoxLayout()
        row_lbl = QLabel('Row:', self)
        row_lbl.setFixedWidth(45)
        row_lbl.setFont(QFont('Times', 12))
        horizontal_layout_start.addWidget(row_lbl)
        self.start_row_tf = QLineEdit()
        self.start_row_tf.setFont(QFont('Times', 12))
        self.start_row_tf.setFixedWidth(50)
        self.start_row_tf.setText('0')
        self.start_row_tf.setContentsMargins(0, 0, 10, 0)
        self.start_row_tf.textChanged.connect(self.change_start_exit)
        horizontal_layout_start.addWidget(self.start_row_tf)
        col_lbl = QLabel('Col:', self)
        col_lbl.setFixedWidth(35)
        col_lbl.setFont(QFont('Times', 12))
        horizontal_layout_start.addWidget(col_lbl)
        self.start_col_tf = QLineEdit()
        self.start_col_tf.setFont(QFont('Times', 12))
        self.start_col_tf.setFixedWidth(50)
        self.start_col_tf.setText('0')
        self.start_col_tf.textChanged.connect(self.change_start_exit)
        horizontal_layout_start.addWidget(self.start_col_tf)
        vertical_layout_start.addLayout(horizontal_layout_start)
        side_layout.addLayout(vertical_layout_start)

        vertical_layout_exit = QVBoxLayout()
        exit_lbl = QLabel('Move Exit', self)
        exit_lbl.setFont(QFont('Times', 15))
        exit_lbl.setAlignment(Qt.AlignCenter)
        exit_lbl.setFixedHeight(50)
        vertical_layout_exit.addWidget(exit_lbl)
        horizontal_layout_exit = QHBoxLayout()
        row_lbl = QLabel('Row:', self)
        row_lbl.setFixedWidth(50)
        row_lbl.setFont(QFont('Times', 12))
        horizontal_layout_exit.addWidget(row_lbl)
        self.exit_row_tf = QLineEdit()
        self.exit_row_tf.setFont(QFont('Times', 12))
        self.exit_row_tf.setFixedWidth(50)
        self.exit_row_tf.setText(str(self.maze.width - 1))
        self.exit_row_tf.setContentsMargins(0, 0, 10, 0)
        self.exit_row_tf.textChanged.connect(self.change_start_exit)
        horizontal_layout_exit.addWidget(self.exit_row_tf)
        col_lbl = QLabel('Col:', self)
        col_lbl.setFixedWidth(35)
        col_lbl.setFont(QFont('Times', 12))
        horizontal_layout_exit.addWidget(col_lbl)
        self.exit_col_tf = QLineEdit()
        self.exit_col_tf.setFont(QFont('Times', 12))
        self.exit_col_tf.setFixedWidth(50)
        self.exit_col_tf.setText(str(self.maze.width - 1))
        self.exit_col_tf.textChanged.connect(self.change_start_exit)
        horizontal_layout_exit.addWidget(self.exit_col_tf)
        vertical_layout_exit.addLayout(horizontal_layout_exit)
        side_layout.addLayout(vertical_layout_exit)

        self.find_path_btn = QPushButton('Find Path', self)
        self.find_path_btn.setMaximumSize(300, 200)
        self.find_path_btn.setFont(QFont('Times', 15))
        self.find_path_btn.clicked.connect(self.display_path)
        self.find_path_btn.setFixedSize(250, 200)
        side_layout.addWidget(self.find_path_btn)
        self.find_path_btn.setEnabled(False)

        # Add the grid layout and buttons layout to the main layout
        main_layout.addLayout(self.grid_layout, 2)
        main_layout.addLayout(side_layout, 1)
        self.setLayout(main_layout)

    def change_start_exit(self):
        # if self.start_row_tf.text() and self.start_col_tf.text():
        self.clear_color()
        self.find_path_btn.setEnabled(False)
        try:
            self.update_cell(self.start, 'grey')
            self.update_cell(self.exit, 'grey')
            if 0 <= int(self.start_row_tf.text()) < self.maze.height and 0 <= int(self.start_row_tf.text()) < self.maze.width and \
                    0 <= int(self.exit_row_tf.text()) < self.maze.height and 0 <= int(self.exit_row_tf.text()) < self.maze.width:
                self.start = self.maze.grid[int(self.start_row_tf.text())][int(self.start_col_tf.text())]
                self.update_cell(self.start, 'red')
                self.exit = self.maze.grid[int(self.exit_row_tf.text())][int(self.exit_col_tf.text())]
                self.update_cell(self.exit, 'green')
                self.find_path_btn.setEnabled(True)
        except Exception:
            pass

    def change_cell_color(self, row, col, color):
        # Find the existing widget at the specified row and column
        widget = self.grid_layout.itemAtPosition(row, col).widget()

        # Update the background color of the widget (cell)
        widget.setStyleSheet(f'background-color: {color};')

    def remove_walls(self, current, neighbour):
        if current.row - neighbour.row == 1:
            current.walls[0] = False
            neighbour.walls[2] = False
        elif current.row - neighbour.row == -1:
            current.walls[2] = False
            neighbour.walls[0] = False
        elif current.col - neighbour.col == 1:
            current.walls[3] = False
            neighbour.walls[1] = False
        elif current.col - neighbour.col == -1:
            current.walls[1] = False
            neighbour.walls[3] = False

    def update_cell(self, current, color):
        current_widget = self.grid_layout.itemAtPosition(current.row, current.col).widget()
        border_style = f'border: 3px solid black; background-color: {color};'
        if current.walls[0] is False:
            border_style += 'border-top: none;'
        if current.walls[1] is False:
            border_style += 'border-right: none;'
        if current.walls[2] is False:
            border_style += 'border-bottom: none;'
        if current.walls[3] is False:
            border_style += 'border-left: none;'
        current_widget.setStyleSheet(border_style)

    def clear_color(self):
        rows = self.maze.height
        cols = self.maze.width
        for row in range(rows):
            for col in range(cols):
                self.update_cell(self.maze.grid[row][col], 'grey')

    def generate_maze(self):
        self.find_path_btn.setEnabled(False)
        self.clear_color()
        self.maze.reset_maze()
        stack = [self.maze.grid[0][0]]
        current = self.maze.grid[0][0]
        self.change_cell_color(current.row, current.col, 'red')
        while stack:
            QtTest.QTest.qWait(0)
            if self.maze.get_random_neighbour(current.row, current.col):
                neighbour = self.maze.get_random_neighbour(current.row, current.col)
                self.remove_walls(current, neighbour)
                self.update_cell(current, 'grey')
                current = neighbour
                stack.append(current)
                self.change_cell_color(current.row, current.col, 'red')
                neighbour.visited = True
            else:
                self.update_cell(current, 'grey')
                current = stack.pop()
        self.update_cell(self.maze.grid[self.start.row][self.start.col], 'red')
        self.update_cell(self.maze.grid[self.exit.row][self.exit.col], 'green')
        self.find_path_btn.setEnabled(True)

    def return_path(self):
        # print(self.start, self.exit)
        self.maze.reset_visited()

        # Queue of paths:
        queue = []
        queue.append([self.start])
        self.start.visited = True
        while queue:
            path = queue.pop(0)
            # print(f"Row: {neighbour.row}, Col: {neighbour.col}", end="")

            # for node in path:
            #     print(node.row, node.col, end=" - ")
            # print()

            # print("Current path: ", path)
            last_node = path[-1]
            # print(f"Row: {last_node.row}, Col: {last_node.col}")

            if last_node.row == self.exit.row and last_node.col == self.exit.col:
                path.pop(0)
                path.pop(-1)
                return path

            neighbours = self.maze.get_visitable_neighbours(last_node.row, last_node.col)
            # print("Neighbours: ", neighbours)
            for neighbour in neighbours:
                new_path = path.copy()
                new_path.append(neighbour)
                # for node in new_path:
                #     print(node.row, node.col, end=" - ")
                # print()
                queue.append(new_path)
                neighbour.visited = True
            # print("Queue: ", queue)
        return None

    def display_path(self):
        for node in self.return_path():
            # node_widget = self.grid_layout.itemAtPosition(node.row, node.col).widget()
            self.update_cell(node, 'blue')
            QtTest.QTest.qWait(10)


class InputDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.resize(400, 200)
        self.setWindowTitle('Maze Generator')
        self.layout = QVBoxLayout(self)
        self.dimension_layout = QHBoxLayout(self)
        self.label1 = QLabel('Input Maze Size:')
        self.label1.setAlignment(Qt.AlignCenter)
        self.label1.setFont(QFont('Times', 15))
        self.layout.addWidget(self.label1)
        self.line_edit1 = QLineEdit(self)
        self.line_edit1.setText('15')
        self.line_edit1.setFont(QFont('Times', 12))
        self.dimension_layout.addWidget(self.line_edit1)
        self.line_edit1.setFixedWidth(40)
        self.line_edit1.setFixedHeight(40)
        self.label2 = QLabel('x', self)
        self.label2.setFont(QFont('Times', 12))
        self.label2.setFixedWidth(12)
        self.dimension_layout.addWidget(self.label2)
        self.line_edit2 = QLineEdit(self)
        self.line_edit2.setText('15')
        self.line_edit2.setFont(QFont('Times', 12))
        self.line_edit2.setFixedWidth(40)
        self.line_edit2.setFixedWidth(40)
        self.dimension_layout.addWidget(self.line_edit2)
        self.layout.addLayout(self.dimension_layout)


        # Add OK and Cancel buttons
        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok, self)
        self.button_box.setFixedSize(230, 80)
        self.button_box.setFont(QFont('Times', 12))
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        self.layout.addWidget(self.button_box)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    height = -1
    width = -1
    input_dialog = InputDialog()
    try:
        if input_dialog.exec_() == QDialog.Accepted:
            # Retrieve the user input
            height = int(input_dialog.line_edit1.text())
            width = int(input_dialog.line_edit2.text())
            if height < 0 or width < 0:
                raise Exception()

    except Exception as e:
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Invalid Maze Size!")
        msg.setFont(QFont('Times', 15))
        msg.setWindowTitle("Error!")
        msg.exec_()
        exit(-1)

    window = Grid(height, width)
    window.generate_maze()
    window.show()    # window.display_path(maze.grid[0][0], maze.grid[19][19])

    sys.exit(app.exec_())

