from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QGroupBox, QRadioButton, \
							QButtonGroup, QFileDialog, QTableWidget, QHeaderView, QTableWidgetItem, QLabel, QComboBox
from PyQt5.QtCore import QDir, Qt
from PyQt5.QtGui import QPainter, QFont, QIcon
from survo_backtrack import *
from survo_sat import *
from light_sat import *
from light_backtrack import *

DUPLICITY = ["This is a unique solution.", "This is not a unique solution."]


class GUI:
	def __init__(self):
		self.app = QApplication([])
		self.window = QWidget()
		self.helpWindow = QWidget()
		self.painter = QPainter(self.window)
		self.buttons = [QPushButton("Load", self.window),
						QPushButton("Solve", self.window)]
		self.help = QPushButton("Help", self.window)
		self.helpLabel = QLabel(self.helpWindow)
		self.groupBox = QGroupBox("Solving Method")
		self.radioButtons = [QRadioButton("SAT", self.window),
							QRadioButton("Backtracking", self.window)]
		self.game = QComboBox(self.window)
		self.game.addItems(["survo", "light"])
		self.result = QLabel("")
		self.buttonGroup = QButtonGroup()
		self.boardToLoad = []
		self.gridWidth = 450
		self.gridHeight = 450
		self.table = QTableWidget(self.window)
		self.noBoardMessage = QLabel(self.window)
		self.unicityMessage = QLabel(self.window)
		self.table.setVisible(False)

		self.setup()

	def setup(self):
		self.window.setWindowTitle("Solver")
		self.window.setGeometry(300, 150, 500, 600)
		self.helpWindow.setWindowTitle("Solver")
		self.helpWindow.setGeometry(400, 150, 510, 300)
		self.window.setWindowIcon(QIcon("icon.png"))
		self.helpWindow.setWindowIcon(QIcon("icon.png"))

		self.setupButtons()
		self.setupGroupBox()
		self.setupTable()
		self.setupLabel()

		self.window.show()
		self.app.exec_()

	def setupLabel(self):
		self.noBoardMessage.setText("No board loaded, nothing to solve.")
		self.noBoardMessage.move(240, 10)
		self.unicityMessage.move(30, 10)
		self.noBoardMessage.setVisible(False)
		self.unicityMessage.setVisible(False)
		font = QFont("Arial")
		font.setPointSize(12)
		self.helpWindow.setFont(font)
		self.result.move(200, 10)

		self.helpLabel.setText(" How to use:\n1. Open a notepad or any similar program\n" +
							" 2. Write the board matrix you'd like to solve as follows:\n" +
							"       Every row has to be one line\n" +
							"       Start typing with the first cell directly\n" +
							"       If the first cell is an unnumbered cell, type in a zero\n" +
							"       To go to the next cell, type a coma, spaces do not matter\n" +
							" 3. Save your notepad wherever you want\n" +
							" 4. Change the extension of you file from .txt to .kur\n" +
							" 5. Decide if you'd like the program to solve your board with a SAT solver\n"
							"    or with the backtracking method\n" +
							"       NOTE: The backtracking method is faster with smaller boards\n" +
							"                    SAT solvers are faster with bigger boards\n" +
							" 6. Check the method you want under the solve button\n" +
							" 7. Click solve and enjoy the solution")

	def setupTable(self):
		self.table.verticalHeader().setVisible(False)
		self.table.horizontalHeader().setVisible(False)

	def setupButtons(self):
		# Setting buttons tooltips
		self.buttons[0].setToolTip("Load a Board from a file")
		self.buttons[1].setToolTip("This buttons solves the board\nPlease check what solving method" + "\
				you'd like to use")
		self.help.setToolTip("Open help window")
		# Setting buttons geometry
		self.buttons[0].setGeometry(280, 500, 100, 40)
		self.buttons[1].setGeometry(390, 500, 100, 40)
		self.help.setGeometry(390, 550, 100, 40)

		self.buttons[0].clicked.connect(self.onClickLoad)
		self.buttons[1].clicked.connect(self.onClickSolve)
		self.help.clicked.connect(self.onClickHelp)

	def setupGroupBox(self):
		self.game.move(10, 510)
		self.radioButtons[0].setChecked(True)
		for i in range(len(self.radioButtons)):
			self.buttonGroup.addButton(self.radioButtons[i])
			self.radioButtons[i].move(10, 550 + i * 25)


	def onClickSolve(self):
		if len(self.boardToLoad) == 0:
			self.noBoardMessage.setVisible(True)
		else:
			self.noBoardMessage.setVisible(False)
			if self.game.currentText() == "survo":
				self.performSurvo()
			elif self.game.currentText() == "light":
				self.performLight()
	
	def resultLabel(self, solution):
		if solution is not None:
			self.result.setText("This board is correct!")
			return True
		else:
			self.result.setText("This board is not solvable!")
			return False
			
	def performSurvo(self):
		if self.radioButtons[0].isChecked():
			solution = SurvoSat(self.boardToLoad)
		elif self.radioButtons[1].isChecked():
			solver = SurvoBacktrack()
			solution = solver.solve(self.boardToLoad)
		
		if(self.resultLabel(solution)):
			self.boardToLoad = solution
			self.setGraphicScene()
	
	def performLight(self):
		if self.radioButtons[0].isChecked():
			solution = LightSat(self.boardToLoad)
		elif self.radioButtons[1].isChecked():
			solver = LightBacktrack()
			solution = solver.solve(self.boardToLoad)
		
		if(self.resultLabel(solution)):
			self.boardToLoad = solution
			self.setGraphicScene()
	
	def onClickLoad(self):
		f, check = QFileDialog.getOpenFileName(None,
												"Load a board",
												QDir.homePath(),
												"Puzzle files (*.survo *.light)")
		if check:
			self.loadBoard(f)
			if(f[-5:] == "survo"):
				self.game.setCurrentIndex(0)
			elif(f[-5:] == "light"):
				self.game.setCurrentIndex(1)

	def onClickHelp(self):
		self.helpWindow.show()

	def loadBoard(self, file):
		self.boardToLoad = []
		with open(file, 'r') as file:
			lines = file.readlines()
			for line in lines:
				firstComa = -1
				row = []
				for i in range(len(line)):
					if line[i] == ',':
						row.append(int(line[firstComa+1: i]))
						firstComa = i
				row.append(int(line[firstComa+1: len(line)]))
				self.boardToLoad.append(row)
		self.setGraphicScene()

	def setGraphicScene(self):
		self.table.setRowCount(len(self.boardToLoad))
		self.table.setColumnCount(len(self.boardToLoad[0]))
		font = QFont()
		font.setPointSize(int(300/ (len(self.boardToLoad) + len(self.boardToLoad[0]))/2))
		self.table.setFont(font)

		self.table.setGeometry(25, 25, 450, 450)
		self.table.setVisible(True)

		for i in range(len(self.boardToLoad)):
			self.table.horizontalHeader().setSectionResizeMode(i, QHeaderView.Stretch)
			self.table.verticalHeader().setSectionResizeMode(i, QHeaderView.Stretch)
		for i in range(len(self.boardToLoad)):
			for j in range(len(self.boardToLoad[i])):
				# for survo there is no last element on the last line
				if(self.game.currentText() == "survo" and i == len(self.boardToLoad)-1 and j > len(self.boardToLoad[i])-1 ):
					break

				num = self.boardToLoad[i][j]
				#display the 0 for light
				if str(num) == "!" or num > 0 and self.game.currentText() == "survo" or num >= 0 and self.game.currentText() == "light":
					item = QTableWidgetItem(str(num))
					self.table.setItem(i, j, item)
					self.table.item(i, j).setTextAlignment(Qt.AlignCenter)
				else:
					item = QTableWidgetItem(str(''))
					self.table.setItem(i, j, item)


if __name__ == "__main__":
	gui = GUI()
