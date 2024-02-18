class ChessPiece:
    def __init__(self, name, side, position):
        self.name = name  # 棋子名称
        self.side = side  # 所属方，'red' 或 'black'
        self.position = position  # 棋子位置，例如 'a1'

    def __str__(self):
        # 返回带有颜色的字符串，这里仅为示例，需要根据实际环境调整
        if self.side == 'red':
            return f"\033[91m{self.name}\033[0m"
        else:
            return f"\033[94m{self.name}\033[0m"

class ChessBoard:
    def __init__(self):
        # 初始化棋盘，使用二维数组表示，None表示空位
        self.board = [[None for _ in range(9)] for _ in range(10)]
        self.winner = None
        # 初始化棋子，这里省略了棋子的放置代码，参考之前的初始化方法

    def set_initial_pieces(self):
        """设置初始棋子。
        """
        pieces = [
            ChessPiece('车', 'red', 'a0'), ChessPiece('马', 'red', 'b0'),
            ChessPiece('象', 'red', 'c0'), ChessPiece('士', 'red', 'd0'),
            ChessPiece('帅', 'red', 'e0'), ChessPiece('士', 'red', 'f0'),
            ChessPiece('象', 'red', 'g0'), ChessPiece('马', 'red', 'h0'),
            ChessPiece('车', 'red', 'i0'), ChessPiece('炮', 'red', 'b2'),
            ChessPiece('炮', 'red', 'h2'), ChessPiece('兵', 'red', 'a3'),
            ChessPiece('兵', 'red', 'c3'), ChessPiece('兵', 'red', 'e3'),
            ChessPiece('兵', 'red', 'g3'), ChessPiece('兵', 'red', 'i3'),

            ChessPiece('车', 'black', 'a9'), ChessPiece('马', 'black', 'b9'),
            ChessPiece('象', 'black', 'c9'), ChessPiece('士', 'black', 'd9'),
            ChessPiece('将', 'black', 'e9'), ChessPiece('士', 'black', 'f9'),
            ChessPiece('象', 'black', 'g9'), ChessPiece('马', 'black', 'h9'),
            ChessPiece('车', 'black', 'i9'), ChessPiece('炮', 'black', 'b7'),
            ChessPiece('炮', 'black', 'h7'), ChessPiece('卒', 'black', 'a6'),
            ChessPiece('卒', 'black', 'c6'), ChessPiece('卒', 'black', 'e6'),
            ChessPiece('卒', 'black', 'g6'), ChessPiece('卒', 'black', 'i6'),
        ]
        self.place_pieces(pieces)
    
    def place_pieces(self, pieces : list):
        """将棋子放置到棋盘上。
        Args:
            pieces (list): 棋子列表。
        """
        for piece in pieces:
            col, row = ord(piece.position[0]) - ord('a'), int(piece.position[1])
            self.board[row][col] = piece
            
    def print_board(self):
        """打印棋盘状态。
        """
        # 打印列坐标
        col_labels = '  '.join(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i'])
        print(f"\033[92m  {col_labels}\033[0m")  # 绿色
        for idx, row in enumerate(self.board):
            row_label = f"\033[92m{idx}\033[0m"  # 行号，绿色
            print(row_label, end=' ')
            for cell in row:
                if cell is None:
                    print('＋', end=' ')
                else:
                    print(cell, end=' ')
            print()  # 新的一行
            if idx == 4:  # 在第五行后打印楚河汉界分界线
                print('' + '============================')
        # 打印列坐标
        print(f"\033[92m  {col_labels}\033[0m")  # 绿色   

    def get_possible_moves(self, position: str) -> list:
        """获取指定位置的棋子的可能移动位置。

        Args:
            position (str): 棋子的位置，例如 'a1'。

        Returns:
            _type_: 可能移动位置的列表，每个位置为 (row, col) 形式的元组。
        """
        if self.winner is not None:
            return []
        col, row = ord(position[0]) - ord('a'), int(position[1])
        piece = self.board[row][col]
        if piece is None:
            return []  # 如果指定位置没有棋子，则返回空列表

        # 根据棋子类型调用对应的移动逻辑
        if piece.name == '车':
            return self._get_rook_moves(row, col)
        elif piece.name == '马':
            return self._get_knight_moves(row, col)
        elif piece.name == '象' or piece.name == '相':
            return self._get_elephant_moves(row, col)
        elif piece.name == '士' or piece.name == '仕':
            return self._get_guard_moves(row, col)
        elif piece.name == '将' or piece.name == '帅':
            return self._get_king_moves(row, col)
        elif piece.name == '炮':
            return self._get_cannon_moves(row, col)
        elif piece.name == '兵' or piece.name == '卒':
            return self._get_pawn_moves(row, col)
        else:
            return []

    def get_possible_moves_with_coords(self, position: tuple) -> list:
        """根据行列坐标获取指定位置的棋子的可能移动位置。该函数是 get_possible_moves 方法的包装。

        Args:
            position (tuple): 棋子的行列坐标，例如 (0, 0)。

        Returns:
            _type_: 可能移动位置的列表，每个位置为 (row, col) 形式的元组。
        """
        position_str = self.coords_to_alphanumeric([position])[0]
        return self.get_possible_moves(position_str)
    
    def _get_rook_moves(self, row, col):
        possible_moves = []
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # 右、下、左、上
        for dr, dc in directions:
            r, c = row + dr, col + dc
            while 0 <= r < 10 and 0 <= c < 9:
                if self.board[r][c] is None:
                    possible_moves.append((r, c))  # 添加空位置
                else:
                    if self.board[r][c].side != self.board[row][col].side:
                        possible_moves.append((r, c))  # 可以吃掉对方棋子
                    break  # 遇到任何棋子停止检查这个方向
                r += dr
                c += dc
        return possible_moves

    def _get_knight_moves(self, row, col):
        possible_moves = []
        current_piece = self.board[row][col]
        # 马的移动向量和对应的马脚位置
        move_vectors = [(-2, -1), (-2, 1), (2, -1), (2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2)]
        leg_positions = [(-1, 0), (-1, 0), (1, 0), (1, 0), (0, -1), (0, 1), (0, -1), (0, 1)]

        for i, (dr, dc) in enumerate(move_vectors):
            leg_row, leg_col = row + leg_positions[i][0], col + leg_positions[i][1]
            new_row, new_col = row + dr, col + dc
            
            # print(row, col, leg_row, leg_col, new_row, new_col)
            # 检查马脚位置和目标位置是否合法：马脚位置不能有棋子，目标位置不能越界、不能有己方棋子
            if 0 <= new_row < 10 and 0 <= new_col < 9 and self.board[leg_row][leg_col] is None:
                target_piece = self.board[new_row][new_col]
                if target_piece is None or target_piece.side != current_piece.side:
                    possible_moves.append((new_row, new_col))

        return possible_moves

    def _get_elephant_moves(self, row, col):
        possible_moves = []
        current_piece = self.board[row][col]
        directions = [(2, 2), (2, -2), (-2, 2), (-2, -2)]  # 定义“相”或“象”移动的四个方向
        river_boundary = 4 if current_piece.side == 'red' else 5  # 定义楚河汉界

        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            middle_row, middle_col = row + dr // 2, col + dc // 2  # 计算“田”字中心的位置
            # 检查目标位置和“田”字中心的位置是否合法
            if 0 <= new_row < 10 and 0 <= new_col < 9 and self.board[middle_row][middle_col] is None:
                if current_piece.side == 'red' and new_row <= river_boundary or \
                current_piece.side == 'black' and new_row >= river_boundary:
                    target_piece = self.board[new_row][new_col]
                    if target_piece is None or target_piece.side != current_piece.side:
                        possible_moves.append((new_row, new_col))

        return possible_moves

    def _get_guard_moves(self, row, col):
        side = self.board[row][col].side
        moves = []
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]  # 斜线移动的四个方向
        # 红方和黑方的九宫格范围
        palace_bounds = {
            'red': ((0, 2), (3, 5)),
            'black': ((7, 9), (3, 5))
        }
        row_bounds, col_bounds = palace_bounds[side]

        for drow, dcol in directions:
            new_row, new_col = row + drow, col + dcol
            # 检查是否在九宫内以及是否有己方棋子
            if row_bounds[0] <= new_row <= row_bounds[1] and col_bounds[0] <= new_col <= col_bounds[1]:
                target_piece = self.board[new_row][new_col]
                if target_piece is None or target_piece.side != side:
                    moves.append((new_row, new_col))
        
        return moves

    def _get_king_moves(self, row, col):
        possible_moves = []
        current_piece = self.board[row][col]
        # 定义移动方向：上、下、左、右
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        # 定义九宫格范围
        king_zone = {
            'red': (0, 2, 3, 5),
            'black': (7, 9, 3, 5)
        }
        # 获取当前棋子的九宫格范围
        zone = king_zone[current_piece.side]

        # 检查水平和垂直方向移动一格的合法性
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if zone[0] <= new_row <= zone[1] and zone[2] <= new_col <= zone[3]:
                target_piece = self.board[new_row][new_col]
                if target_piece is None or target_piece.side != current_piece.side:
                    possible_moves.append((new_row, new_col))

        # 检查垂直方向上是否直接对面对方的“将”或“帅”
        direction_to_check = 1 if current_piece.side == 'red' else -1  # 红方向下检查，黑方向上检查
        for i in range(1, 10):  # 最多检查棋盘的高度
            check_row = row + i * direction_to_check
            if check_row < 0 or check_row > 9:  # 超出棋盘范围
                break
            target_piece = self.board[check_row][col]
            if target_piece is not None:
                if target_piece.name in ['帅', '将'] and target_piece.side != current_piece.side:
                    possible_moves.append((check_row, col))  # 直接对面对方的“将”或“帅”，可以移动
                break  # 遇到任何棋子都停止检查

        return possible_moves

    def _get_cannon_moves(self, row, col):
        possible_moves = []
        current_piece = self.board[row][col]

        # 检查横向和纵向的移动
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # 右、左、下、上
        for dr, dc in directions:
            obstacle_found = False  # 标记是否找到跳板（障碍）
            for step in range(1, 10):  # 假设棋盘最大不超过10步
                new_row, new_col = row + step * dr, col + step * dc
                # 检查新位置是否超出棋盘
                if not (0 <= new_row < 10 and 0 <= new_col < 9):
                    break  # 超出棋盘范围

                target_piece = self.board[new_row][new_col]
                if target_piece is None:
                    if not obstacle_found:  # 如果还没有找到障碍，可以移动
                        possible_moves.append((new_row, new_col))
                else:
                    if not obstacle_found:
                        obstacle_found = True  # 找到第一个障碍
                    else:  # 如果已经找到障碍，检查这个位置的棋子是否为敌方棋子
                        if target_piece.side != current_piece.side:
                            possible_moves.append((new_row, new_col))  # 可以跳吃
                        break  # 无论是否跳吃成功，之后的位置都不再考虑

        return possible_moves

    def _get_pawn_moves(self, row, col):
        possible_moves = []
        current_piece = self.board[row][col]
        move_direction = 1 if current_piece.side == 'red' else -1  # 红方向下，黑方向上

        # 楚河汉界的定义：红方的楚河汉界是第5行（从0开始计数），黑方的是第4行
        river_boundary = 4 if current_piece.side == 'red' else 5

        # 前进一步的移动
        forward_row = row + move_direction
        if 0 <= forward_row < 10:
            if self.board[forward_row][col] is None or self.board[forward_row][col].side != current_piece.side:
                possible_moves.append((forward_row, col))

        # 楚河汉界后的左右移动
        if (current_piece.side == 'red' and row > river_boundary) or (current_piece.side == 'black' and row < river_boundary):
            for side_step in [-1, 1]:  # 左移和右移
                side_col = col + side_step
                if 0 <= side_col < 9:
                    if self.board[row][side_col] is None or self.board[row][side_col].side != current_piece.side:
                        possible_moves.append((row, side_col))

        return possible_moves
    
    def move_piece(self, src: str, dest: str) -> bool:
        """移动棋子。

        Args:
            src (str): 源位置，例如 'a1'。
            dest (str): 目标位置，例如 'a2'。

        Returns:
            bool: 移动是否成功。
        """
        src_col, src_row = ord(src[0]) - ord('a'), int(src[1])
        dest_col, dest_row = ord(dest[0]) - ord('a'), int(dest[1])
        
        # 检查源位置和目标位置是否合法
        if not (0 <= src_row < 10 and 0 <= src_col < 9) or not (0 <= dest_row < 10 and 0 <= dest_col < 9):
            # print("Invalid move: Out of bounds")
            return False
        
        moving_piece = self.board[src_row][src_col]
        if moving_piece is None:
            # print("Invalid move: No piece at source")
            return False
        
        # 获取棋子的可能移动位置
        possible_moves = self.get_possible_moves(src)
        if (dest_row, dest_col) not in possible_moves:
            # print("Invalid move: Not a legal move for this piece")
            return False
        
        # 执行移动
        target_piece = self.board[dest_row][dest_col]
        self.board[dest_row][dest_col] = moving_piece
        self.board[src_row][src_col] = None
        # print(f"Moved {moving_piece.name} from {src} to {dest}")
        
        # 检查是否吃掉了对方的将/帅
        if target_piece is not None:
            if target_piece.name == '将' or target_piece.name == '帅':
                self.winner = 'black' if target_piece.side == 'red' else 'red'
                # print(f"{self.winner} wins!")
        return True
    
    def move_piece_with_coords(self, src_coords: tuple, dest_coords: tuple) -> bool:
        """根据行列坐标移动棋子。该函数是 move_piece 方法的包装。
            Args:
                src_coords (tuple): 源位置的行列坐标，例如 (0, 0)。
                dest_coords (tuple): 目标位置的行列坐标，例如 (0, 1)。
            Returns:
                bool: 移动是否成功。
        """
        src_str = self.coords_to_alphanumeric([src_coords])[0]
        dest_str = self.coords_to_alphanumeric([dest_coords])[0]
        return self.move_piece(src_str, dest_str)
    
    def get_pieces_positions(self, side: str) -> list:
        """获取指定颜色方的所有棋子的坐标。

        Args:
            side (str): 棋子的颜色，"black" 或 "red"。

        Returns:
            list: 该颜色方的所有棋子的坐标元组列表，每个元组为(row, col)。
        """
        positions = []
        len_row = len(self.board)
        len_col = len(self.board[0])
        for row in range(len_row):
            for col in range(len_col):
                piece = self.board[row][col]
                if piece is not None and piece.side == side:
                    positions.append((row, col))
        return positions
    
    def get_legal_moves(self, side: str) -> list:
        """获取指定颜色方的所有合法移动。

        Args:
            side (str): 棋子的颜色，"black" 或 "red"。

        Returns:
            list: 所有合法移动的列表，每个移动为 (src, dest) 形式的元组。
        """
        if self.winner is not None:
            return []
        positions = self.get_pieces_positions(side)
        legal_moves = []
        for position in positions:
            possible_moves = self.get_possible_moves_with_coords(position)
            for move in possible_moves:
                legal_moves.append((position, move))
        return legal_moves
    
    def copy(self):
        """复制棋盘。

        Returns:
            ChessBoard: 复制的棋盘。
        """
        new_board = ChessBoard()
        new_board.board = [row[:] for row in self.board]
        new_board.winner = self.winner
        return new_board
    @classmethod
    def coords_to_alphanumeric(cls, coords: list) -> list:
        """
        将行列坐标列表转换为字母+数字格式的列表。
        :param coords: 坐标列表，每个坐标为(row, col)形式的元组。
        :return: 转换后的坐标列表，每个坐标为字母+数字形式的字符串。
        """
        result = []
        for row, col in coords:
            # 将列数字转换为字母，a对应列0，以此类推
            col_letter = chr(col + ord('a'))
            # 将行数字转换为字符串，直接使用行号
            row_number = str(row)
            # 拼接字母和数字形成坐标
            result.append(col_letter + row_number)
        return result
        

if __name__ == '__main__':
    pieces_initial = [
        ChessPiece('车', 'red', 'a0'), ChessPiece('马', 'red', 'b0'),
        ChessPiece('象', 'red', 'c0'), ChessPiece('士', 'red', 'd0'),
        ChessPiece('帅', 'red', 'e0'), ChessPiece('士', 'red', 'f0'),
        ChessPiece('象', 'red', 'g0'), ChessPiece('马', 'red', 'h0'),
        ChessPiece('车', 'red', 'i0'), ChessPiece('炮', 'red', 'b2'),
        ChessPiece('炮', 'red', 'h2'), ChessPiece('兵', 'red', 'a3'),
        ChessPiece('兵', 'red', 'c3'), ChessPiece('兵', 'red', 'e3'),
        ChessPiece('兵', 'red', 'g3'), ChessPiece('兵', 'red', 'i3'),

        ChessPiece('车', 'black', 'a9'), ChessPiece('马', 'black', 'b9'),
        ChessPiece('象', 'black', 'c9'), ChessPiece('士', 'black', 'd9'),
        ChessPiece('将', 'black', 'e9'), ChessPiece('士', 'black', 'f9'),
        ChessPiece('象', 'black', 'g9'), ChessPiece('马', 'black', 'h9'),
        ChessPiece('车', 'black', 'i9'), ChessPiece('炮', 'black', 'b7'),
        ChessPiece('炮', 'black', 'h7'), ChessPiece('卒', 'black', 'a6'),
        ChessPiece('卒', 'black', 'c6'), ChessPiece('卒', 'black', 'e6'),
        ChessPiece('卒', 'black', 'g6'), ChessPiece('卒', 'black', 'i6'),
    ]
    pieces_test1 = [
        ChessPiece('马', 'black', 'g5'), 
        ChessPiece('马', 'black', 'g6'), 
        ChessPiece('马', 'red', 'e3'), 
    ]
    chess_board = ChessBoard()
    chess_board.place_pieces(pieces_initial)
    chess_board.print_board()