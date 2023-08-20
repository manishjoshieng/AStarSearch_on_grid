import heapq
import enum

class CellType(enum.Enum):
    EMPTY = 0
    FIRE = 1
    BUSH_PLANT = 2

class Direction(enum.Enum):
    LEFT = 0
    RIGHT = 1
    TOP = 2
    BOTTOM = 3

class Position():
    @staticmethod
    def add(a, b):
        c = Position(0,0)
        c.x = a.x + b.x
        c.y = a.y + b.y
        return c

    def __init__(self,x,y) -> None:
        self.x = x
        self.y = y
    
    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, __value: object) -> bool:
        return (self.x==__value.x and self.y==__value.y)
        
    def __str__(self):
        return "("+str(self.x)+", "+str(self.y)+")"
    
    def distance(self,other):
        return abs(self.x - other.x) + abs(self.y - other.y)
    
    def getLeft(self):
        return Position(self.x, self.y-1)
    def getRight(self):
        return Position(self.x, self.y+1)
    def getBottom(self):
        return Position(self.x+1, self.y)
    def getTop(self):
        return Position(self.x-1, self.y)
    
    def getNext(self,dir : Direction):
        if dir == Direction.LEFT:
            return self.getLeft()
        elif dir == Direction.RIGHT:
            return self.getRight()
        elif dir == Direction.BOTTOM:
            return self.getBottom()
        else:
            return self.getTop()

class Move():
    def __init__(self,pos : Position, dir : Direction) -> None:
        self.position = pos
        self.direction = dir

class Priority_Queue():
    def __init__(self):
        self.elements = []

    def is_empty(self):
        return len(self.elements) == 0

    def push(self, item, priority):
        heapq.heappush(self.elements, (priority, item))

    def pop(self):
        if not self.is_empty():
            priority, item = heapq.heappop(self.elements)
            return item
        else:
            raise IndexError("Priority queue is empty.")
        
class Cell():
    def __init__(self, position , parent = None, type = CellType.EMPTY) -> None:
        self.position = position
        self.type = type
        self.parent = parent
        self.walls = [False] * 4
        self.cost = 0
        self.huristic = 0
        self.final = 0

    def __eq__(self, __value: object) -> bool:
        return self.position == __value.position
    
    def __lt__(self, other):
        return self.final < other.final
    
    def getCost(self):
        if self.type == CellType.EMPTY:
            return 3
        elif self.type == CellType.BUSH_PLANT:
            return 4
        else:
            return 8
        
    def setWall(self, dir, value = True):
        self.walls[int(dir.value)] = value
        
    def getChildCells(self):
        childs = []
        if not self.walls[Direction.LEFT.value]:
            childs.append(self.position.getLeft())
        if not self.walls[Direction.RIGHT.value]:
            childs.append(self.position.getRight())
        if not self.walls[Direction.TOP.value]:
            childs.append(self.position.getTop())
        if not self.walls[Direction.BOTTOM.value]:
            childs.append(self.position.getBottom())
        return childs
    
class Grid():
    def __init__(self,noOfRow,noOfCol,listOfFire,listOfBushplant,listOfRestrictedMove) -> None:
        self.maxRow = noOfRow
        self.maxCol = noOfCol
        self.grid = []

        for i in range(noOfRow):
            row = []
            for j in range(noOfCol):
                cellPos = Position(i,j)
                cell = Cell(cellPos)

                if cellPos in listOfFire:
                    cell.type = CellType.FIRE
                elif cellPos in listOfBushplant:
                    cell.type = CellType.BUSH_PLANT
                
                if cellPos.x == 0:
                    cell.setWall(Direction.TOP)
                if cellPos.x==self.maxRow - 1:
                    cell.setWall(Direction.BOTTOM)
                if cellPos.y == 0:
                    cell.setWall(Direction.LEFT)
                if cellPos.y == self.maxCol - 1:
                    cell.setWall(Direction.RIGHT)

                row.append(cell)
            self.grid.append(row)
        
        for move in listOfRestrictedMove:
            pos = move.position
            dir = move.direction

            cell = self.grid[pos.x][pos.y]
            cell.setWall(dir)
            otherCellPos = pos.getNext(dir)
            if otherCellPos.x>=0 and otherCellPos.y >= 0 and otherCellPos.x < self.maxRow and otherCellPos.y < self.maxCol:
                otherCell = self.grid[otherCellPos.x][otherCellPos.y]
                if dir== Direction.LEFT:
                    otherCell.setWall(Direction.RIGHT)
                elif dir==Direction.RIGHT:
                    otherCell.setWall(Direction.LEFT)
                elif dir==Direction.TOP:
                    otherCell.setWall(Direction.BOTTOM)
                else:
                    otherCell.setWall(Direction.TOP)

def recunstructPath(current_cell):
    current = current_cell
    path = []
    while current is not None:
       path.append(current.position)
       current = current.parent
    return path[::-1]

def AStarSearch(grid : Grid, start : Position, end : Position):
    start_cell = grid[start.x][start.y]
    end_cell = grid[end.x][end.y]

    openList = Priority_Queue()
    closeList = {}

    openList.push(start_cell,start_cell.final)

    while openList.is_empty() == False:
        current_cell = openList.pop()
        closeList[current_cell.position] = True

        if (current_cell == end_cell):
            path = recunstructPath(current_cell)
            cost = current_cell.cost
            return (cost, path)
        
        childs = current_cell.getChildCells()
        for child in childs:
            if child in closeList:
                continue

            childCell = grid[child.x][child.y]
            childCell.cost = current_cell.cost + childCell.getCost()
            childCell.huristic = child.distance(end)
            childCell.final = childCell.cost + childCell.huristic
            childCell.parent = current_cell
            openList.push(childCell,childCell.final)

if __name__ == '__main__':
    start = Position(0,2)
    end = Position(6,4)

    maxRow = 7
    maxCol = 6
    listOfFire = [
        Position(0,5),
        Position(2,3),
        Position(3,1)
        ]
    listOfBushPlant = [
        Position(0,0),
        Position(1,4),
        Position(4,1),
        Position(4,5)
        ]
    listOfWalls = [
        Move(Position(0,2),Direction.RIGHT),
        Move(Position(1,0),Direction.RIGHT),
        Move(Position(1,1),Direction.TOP),
        Move(Position(1,1),Direction.RIGHT),
        Move(Position(1,3),Direction.TOP),
        Move(Position(1,4),Direction.TOP),
        Move(Position(1,4),Direction.RIGHT),
        Move(Position(2,0),Direction.RIGHT),
        Move(Position(2,2),Direction.RIGHT),
        Move(Position(2,3),Direction.TOP),
        Move(Position(3,1),Direction.TOP),
        Move(Position(3,1),Direction.RIGHT),
        Move(Position(3,2),Direction.RIGHT),
        Move(Position(3,3),Direction.TOP),
        Move(Position(3,4),Direction.TOP),
        Move(Position(4,0),Direction.RIGHT),
        Move(Position(4,1),Direction.TOP),
        Move(Position(4,4),Direction.TOP),
        Move(Position(4,5),Direction.TOP),
        Move(Position(5,0),Direction.RIGHT),
        Move(Position(5,2),Direction.TOP),
        Move(Position(5,3),Direction.TOP),
        Move(Position(5,3),Direction.RIGHT),
        Move(Position(5,4),Direction.RIGHT),
        Move(Position(6,0),Direction.TOP),
        Move(Position(6,1),Direction.RIGHT),
        Move(Position(6,2),Direction.TOP),
        Move(Position(6,4),Direction.RIGHT)
    ]

    grid = Grid(maxRow,maxCol,listOfFire=listOfFire,listOfBushplant=listOfBushPlant,listOfRestrictedMove=listOfWalls)
    cost , path = AStarSearch(grid.grid,start,end)

    print("Cost: ",cost)
    print("Path:",end=" ")
    for p in path:
        print(p,end=" ")





        
