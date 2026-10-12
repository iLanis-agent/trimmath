import json, math

def jsnum(x):
    return int(x) if isinstance(x, float) and x == int(x) else x
def plural(n, word, form=None): return str(jsnum(n)) + " " + (word if n == 1 else (form or word + "s"))
def fmt(x): return str(jsnum(x))
def round1(x): return jsnum(math.floor(x * 10 + 0.5) / 10)

def run_plan(lengthM, widthM, doors, doorM):
    if not (lengthM > 0) or not (widthM > 0) or not (doorM >= 0):
        return {"error": "length and width must be positive and the door width cannot be negative"}
    if not (doors >= 0) or math.floor(doors) != doors:
        return {"error": "doors must be a whole number, zero or more"}
    perimeter = 2 * (lengthM + widthM)
    run = perimeter - doors * doorM
    if not (run > 0):
        return {"error": "the doors take the whole wall"}
    if run < 8: verdict = "a short run"
    elif run < 16: verdict = "a typical room run"
    else: verdict = "a long run"
    return {"perimeter": round1(perimeter), "run": round1(run), "verdict": verdict}

def board_plan(runM, boardM, wastePct):
    if not (runM > 0) or not (boardM > 0) or not (wastePct >= 0):
        return {"error": "run and board length must be positive and the waste cannot be negative"}
    need = runM * (1 + wastePct / 100)
    boards = math.ceil(need / boardM)
    spare = round1(boards * boardM - runM)
    if boards <= 4: verdict = "one trip covers it"
    elif boards <= 10: verdict = "a car load"
    else: verdict = "order a delivery"
    return {"need": round1(need), "boards": boards, "spare": spare, "verdict": verdict}

def corner_plan(inside, outside, allowCm):
    if not (inside >= 0) or not (outside >= 0) or math.floor(inside) != inside or math.floor(outside) != outside:
        return {"error": "corner counts must be whole numbers, zero or more"}
    if not (allowCm >= 0):
        return {"error": "the allowance cannot be negative"}
    corners = inside + outside
    if corners == 0:
        return {"error": "a room with no corners needs no mitres"}
    cuts = corners * 2
    extra = round1(corners * allowCm / 100)
    if corners <= 4: verdict = "a plain room"
    elif corners <= 8: verdict = "a busy room"
    else: verdict = "a lot of mitres - cut a test corner first"
    return {"corners": corners, "cuts": cuts, "extra": extra, "verdict": verdict}

def render_run(r, l, w, doors, doorM):
    return ("A room " + fmt(l) + " m x " + fmt(w) + " m has " + fmt(r["perimeter"]) + " m of wall; "
            + plural(doors, "doorway") + " of " + fmt(doorM) + " m leave " + fmt(r["run"]) + " m to trim - " + r["verdict"] + ".")

def render_board(r, runM, boardM, wastePct):
    return (fmt(runM) + " m of trim with a labeled " + fmt(wastePct) + "% waste is " + fmt(r["need"]) + " m to buy: "
            + plural(r["boards"], "board") + " of " + fmt(boardM) + " m, " + fmt(r["spare"]) + " m left over - " + r["verdict"] + ".")

def render_corner(r, inside, outside, allowCm):
    return (plural(inside, "inside corner") + " and " + plural(outside, "outside corner") + " mean "
            + plural(r["cuts"], "mitre cut") + "; at a labeled " + fmt(allowCm) + " cm of extra length a corner, add "
            + fmt(r["extra"]) + " m - " + r["verdict"] + ".")

cases = []
def add(fn, f, rf, args):
    r = f(*args)
    c = {"fn": fn, "args": args, "result": r}
    if "error" not in r: c["render"] = rf(r, *args)
    cases.append(c)

for a in [[4,5,1,0.9],[3,3.5,2,0.9],[2,2.5,0,0.9],[6,8,3,0.8],[1,1,2,0.9],[0,3,1,0.9],[4,5,-1,0.9],[4,5,1.5,0.9],[4,5,1,-0.1],[3.3,4.7,1,0.85]]:
    add("runPlan", run_plan, render_run, a)
for a in [[14.2,2.4,10],[6,2.4,10],[20,2.4,10],[12,2.7,0],[7.6,2.4,15],[0,2.4,10],[10,2.4,-5],[10,0,10],[9.6,2.4,10],[30.5,2.4,12.5]]:
    add("boardPlan", board_plan, render_board, a)
for a in [[3,1,5],[4,0,5],[0,1,5],[6,4,5],[1,0,5],[0,0,5],[2.5,1,5],[2,2,-1],[2,2,0],[1,3,7.5]]:
    add("cornerPlan", corner_plan, render_corner, a)
json.dump(cases, open("expected.json", "w"), separators=(",", ":"))
print(len(cases), "cases")
