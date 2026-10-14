from flask import Flask, render_template, request, jsonify
from game.game import MinesweeperGame
from ai.solver import MinesweeperSolver

app=Flask(__name__)
game=None
DIFFICULTIES={'easy':(9,9,10),'medium':(16,16,40),'hard':(16,30,99),'expert':(20,30,130)}

def snapshot(): return game.public_state() if game else None

@app.route('/')
def index(): return render_template('index.html')

@app.post('/api/new')
def new_game():
    global game
    data=request.get_json(silent=True) or {}
    difficulty=data.get('difficulty','easy')
    rows,cols,default_mines=DIFFICULTIES.get(difficulty,DIFFICULTIES['easy'])
    mines=int(data.get('mines',default_mines))
    mines=max(1,min(mines,rows*cols-1))
    game=MinesweeperGame(rows,cols,mines)
    return jsonify(snapshot())

@app.post('/api/start')
def start_game():
    if not game: return jsonify({'error':'Create a game first.'}),400
    game.start(); return jsonify(snapshot())

@app.post('/api/action')
def action():
    if not game: return jsonify({'error':'Create a game first.'}),400
    data=request.get_json() or {}; action=data.get('action'); r,c=data.get('row'),data.get('col')
    if action=='open': result=game.open_cell(r,c)
    elif action=='flag': result=game.toggle_flag(r,c)
    else: return jsonify({'error':'Unknown action.'}),400
    return jsonify({'state':snapshot(),'result':result})

@app.post('/api/hint')
def hint():
    if not game: return jsonify({'error':'Create a game first.'}),400
    if not game.started: game.start()
    if game.hints_used>=3: return jsonify({'error':'No hints remaining.'}),400
    result=MinesweeperSolver(game).best_move(allow_guess=True)
    game.hints_used+=1
    return jsonify({'state':snapshot(),'hint':result})

@app.post('/api/clean-flags')
def clean_flags():
    if not game: return jsonify({'error':'Create a game first.'}),400
    if not game.started: game.start()
    result=MinesweeperSolver(game).remove_incorrect_flags()
    return jsonify({'state':snapshot(),'result':result})

@app.post('/api/solve-step')
def solve_step():
    if not game: return jsonify({'error':'Create a game first.'}),400
    if not game.started: game.start()
    step=MinesweeperSolver(game).step(complete=True)
    return jsonify({'state':snapshot(),'step':step})

@app.post('/api/solve-all')
def solve_all():
    if not game: return jsonify({'error':'Create a game first.'}),400
    if not game.started: game.start()
    steps=MinesweeperSolver(game).solve_progressively(complete=True)
    return jsonify({'state':snapshot(),'steps':steps})

if __name__=='__main__': app.run(debug=True,host='127.0.0.1',port=5000)
