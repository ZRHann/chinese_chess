import random
import math
from ChessBoard import ChessBoard

class MCTSNode:
    def __init__(self, chessboard: ChessBoard, move=None, parent=None, side=None):
        self.chessboard = chessboard.copy()  # 假设ChessBoard有一个复制自身的方法
        self.move = move  # 导致此节点的移动
        self.parent = parent  # 父节点
        self.children = []  # 子节点
        self.wins = 0  # 赢的模拟次数
        self.visits = 0  # 访问次数
        self.side = side  # 当前节点代表的玩家
        if move:
            self.chessboard.move_piece_with_coords(move[0], move[1])
        self.untried_moves = self.chessboard.get_legal_moves(side)  # 尚未尝试的移动

    def select_child(self):
        """选择子节点, 使用UCT算法."""
        s = sorted(self.children, key=lambda c: c.wins / c.visits + math.sqrt(2 * math.log(self.visits) / c.visits))[-1]
        return s

    def expand(self):
        """扩展一个新的子节点."""
        move = self.untried_moves.pop()
        next_side = 'red' if self.side == 'black' else 'black'
        child_node = MCTSNode(self.chessboard, move, self, next_side)
        self.children.append(child_node)
        return child_node

    def update(self, result):
        """更新节点的信息."""
        self.visits += 1
        if self.side == result:
            self.wins += 1

    def is_terminal_node(self):
        """判断是否为终止节点，即游戏结束的节点."""
        return self.chessboard.winner is not None

class MCTSBot:
    def __init__(self, chessboard: ChessBoard, side: str, iteration_limit=10000):
        self.chessboard = chessboard
        self.side = side
        self.iteration_limit = iteration_limit

    def make_move(self):
        root = MCTSNode(chessboard=self.chessboard, side=self.side)

        for _ in range(self.iteration_limit):
            # 选择阶段
            node = root
            while node.untried_moves == [] and node.children != []:
                node = node.select_child()

            # 扩展阶段
            if node.untried_moves != []:
                node = node.expand()

            # 模拟阶段
            outcome = self.simulate_random_game(node.chessboard.copy(), node.side)

            # 回溯阶段
            while node is not None:
                node.update(outcome)
                node = node.parent

        best_move = sorted(root.children, key=lambda c: (c.visits - c.wins) / c.visits)[-1].move
        self.chessboard.move_piece_with_coords(best_move[0], best_move[1])
        return best_move

    def simulate_random_game(self, chessboard: ChessBoard, side: str):
        """随机模拟游戏至结束，返回胜者."""
        while chessboard.winner is None:
            pieces_positions = chessboard.get_pieces_positions(side)
            if not pieces_positions:
                break
            random_piece = random.choice(pieces_positions)
            possible_moves = chessboard.get_possible_moves_with_coords(random_piece)
            if not possible_moves:
                break
            random_move = random.choice(possible_moves)
            chessboard.move_piece_with_coords(random_piece, random_move)
            side = 'red' if side == 'black' else 'black'
        return chessboard.winner
