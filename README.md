# Trim math

Trim math plans the baseboard run before the shopping trip: the room's size
and doorways become the meters of wall to cover, the run becomes a board count
with a labeled waste allowance, and the corners become mitre cuts and the
extra length they eat.

Live site: https://ilanis-agent.github.io/trimmath/

## The three tools

- **Run plan** - `2 x (length + width) - doorways x doorway width`, in meters.
  Verdicts run short / typical / long.
- **Board plan** - `ceil(run x (1 + waste%) / board length)` boards and the
  length left over; labeled 10% waste by default.
- **Corner plan** - two cuts per corner (inside plus outside) and a labeled
  extra length per corner, 5 cm by default.

## Limits

Every default is labeled and illustrative. Walls are never perfectly square,
and real rooms have bays, cupboards and uneven floors. This is arithmetic,
not a measured quote: measure the real walls and buy a spare board.

## Files

- `index.html` - landing page with the labeled norms
- `app.html` - the three calculators
- `engine.js` - shared calculation and render logic (browser + node)
- `oracle.py` - python mirror of the engine, writes `expected.json`
- `test.js` - runs the engine against `expected.json` (30 cases, 154 checks)

Run the tests: `python3 oracle.py && node test.js`
