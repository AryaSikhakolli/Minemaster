import random
import time

class Cell:
    def __init__(self):
        self.mine = False
        self.adjacent = 0
        self.open = False
        self.flagged = False
        self.flag_source = None  # 'player' or 'ai'

class MinesweeperGame:
    def __init__(self, rows, cols, mines):
        self.rows, self.cols, self.mine_count = rows, cols, mines
        self.board = [[Cell() for _ in range(cols)] for _ in range(rows)]
        self.started = False
        self.start_time = None
        self.finished = False
        self.won = False
        self.hints_used = 0
        self.moves = 0
        self.wrong_flags = 0
        self.safe_opens = 0
        self.ai_guesses = 0
        self._place_mines()
        self._calculate_numbers()

    def start(self):
        if not self.started and not self.finished:
            self.started = True
            self.start_time = time.time()
        return self.started

    def neighbors(self, r, c):
        for dr in (-1,0,1):
            for dc in (-1,0,1):
                if dr == dc == 0: continue
                nr, nc = r+dr, c+dc
                if 0 <= nr < self.rows and 0 <= nc < self.cols:
                    yield nr, nc

    def _place_mines(self):
        cells = [(r,c) for r in range(self.rows) for c in range(self.cols)]
        for r,c in random.sample(cells, self.mine_count):
            self.board[r][c].mine = True

    def _calculate_numbers(self):
        for r in range(self.rows):
            for c in range(self.cols):
                if not self.board[r][c].mine:
                    self.board[r][c].adjacent = sum(self.board[nr][nc].mine for nr,nc in self.neighbors(r,c))

    def elapsed(self):
        if not self.started or self.start_time is None: return 0.0
        end = time.time() if not self.finished else getattr(self, 'finish_time', time.time())
        return round(end-self.start_time,1)

    def open_cell(self,r,c, source='player'):
        if not self.started:
            return {'ok':False,'message':'Press Start Game before making moves.'}
        if self.finished or not (0 <= r < self.rows and 0 <= c < self.cols): return {'ok':False}
        cell=self.board[r][c]
        if cell.open or cell.flagged: return {'ok':False}
        self.moves += 1
        if cell.mine:
            cell.open=True; self.finished=True; self.won=False; self.finish_time=time.time()
            return {'ok':True,'mine':True,'message':'Boom! You hit a mine.'}
        stack=[(r,c)]
        while stack:
            cr,cc=stack.pop(); cur=self.board[cr][cc]
            if cur.open or cur.flagged: continue
            cur.open=True; self.safe_opens+=1
            if cur.adjacent==0:
                for nr,nc in self.neighbors(cr,cc):
                    n=self.board[nr][nc]
                    if not n.open and not n.mine and not n.flagged: stack.append((nr,nc))
        if self._check_win():
            self.finished=True; self.won=True; self.finish_time=time.time()
        return {'ok':True,'mine':False,'message':'Cell opened.'}

    def toggle_flag(self,r,c,source='player'):
        if not self.started: return {'ok':False,'message':'Press Start Game before making moves.'}
        if self.finished or not (0 <= r < self.rows and 0 <= c < self.cols): return {'ok':False}
        cell=self.board[r][c]
        if cell.open: return {'ok':False}
        if not cell.flagged:
            cell.flagged=True; cell.flag_source=source
            if source=='player' and not cell.mine: self.wrong_flags+=1
        else:
            cell.flagged=False; cell.flag_source=None
        return {'ok':True,'flagged':cell.flagged}

    def _check_win(self):
        return all(cell.mine or cell.open for row in self.board for cell in row)

    def efficiency(self):
        total_safe=self.rows*self.cols-self.mine_count
        progress=self.safe_opens/max(1,total_safe)
        time_penalty=min(1.0,self.elapsed()/(total_safe*4))
        mistake_penalty=min(0.35,self.wrong_flags*0.05)
        hint_penalty=self.hints_used*0.05
        guess_penalty=min(0.25,self.ai_guesses*0.01)
        score=100*(0.60*progress+0.40*(1-time_penalty))
        score*=max(0,1-mistake_penalty-hint_penalty-guess_penalty)
        return max(0,round(score))

    def public_state(self):
        cells=[]
        for r in range(self.rows):
            row=[]
            for c in range(self.cols):
                x=self.board[r][c]
                row.append({'open':x.open,'flagged':x.flagged,'value':x.adjacent if x.open else None,'mine':x.mine if self.finished else False,'ai_flag':x.flag_source=='ai'})
            cells.append(row)
        return {'rows':self.rows,'cols':self.cols,'mines':self.mine_count,'elapsed':self.elapsed(),'hints':3-self.hints_used,'moves':self.moves,'wrong_flags':self.wrong_flags,'ai_guesses':self.ai_guesses,'finished':self.finished,'won':self.won,'started':self.started,'efficiency':self.efficiency(),'cells':cells}
