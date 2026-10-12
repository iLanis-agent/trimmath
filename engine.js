(function (root) {
  "use strict";
  function plural(n, word, form) { return n + " " + (n === 1 ? word : (form || word + "s")); }
  function round1(x) { return Math.round(x * 10) / 10; }

  function runPlan(lengthM, widthM, doors, doorM) {
    if (!(lengthM > 0) || !(widthM > 0) || !(doorM >= 0)) return { error: "length and width must be positive and the door width cannot be negative" };
    if (!(doors >= 0) || Math.floor(doors) !== doors) return { error: "doors must be a whole number, zero or more" };
    var perimeter = 2 * (lengthM + widthM);
    var run = perimeter - doors * doorM;
    if (!(run > 0)) return { error: "the doors take the whole wall" };
    var verdict;
    if (run < 8) verdict = "a short run";
    else if (run < 16) verdict = "a typical room run";
    else verdict = "a long run";
    return { perimeter: round1(perimeter), run: round1(run), verdict: verdict };
  }

  function boardPlan(runM, boardM, wastePct) {
    if (!(runM > 0) || !(boardM > 0) || !(wastePct >= 0)) return { error: "run and board length must be positive and the waste cannot be negative" };
    var need = runM * (1 + wastePct / 100);
    var boards = Math.ceil(need / boardM);
    var spare = round1(boards * boardM - runM);
    var verdict;
    if (boards <= 4) verdict = "one trip covers it";
    else if (boards <= 10) verdict = "a car load";
    else verdict = "order a delivery";
    return { need: round1(need), boards: boards, spare: spare, verdict: verdict };
  }

  function cornerPlan(inside, outside, allowCm) {
    if (!(inside >= 0) || !(outside >= 0) || Math.floor(inside) !== inside || Math.floor(outside) !== outside) return { error: "corner counts must be whole numbers, zero or more" };
    if (!(allowCm >= 0)) return { error: "the allowance cannot be negative" };
    var corners = inside + outside;
    if (corners === 0) return { error: "a room with no corners needs no mitres" };
    var cuts = corners * 2;
    var extra = round1(corners * allowCm / 100);
    var verdict;
    if (corners <= 4) verdict = "a plain room";
    else if (corners <= 8) verdict = "a busy room";
    else verdict = "a lot of mitres - cut a test corner first";
    return { corners: corners, cuts: cuts, extra: extra, verdict: verdict };
  }

  function renderRun(r, lengthM, widthM, doors, doorM) {
    return "A room " + lengthM + " m x " + widthM + " m has " + r.perimeter + " m of wall; " + plural(doors, "doorway") + " of " + doorM + " m leave " + r.run + " m to trim - " + r.verdict + ".";
  }

  function renderBoard(r, runM, boardM, wastePct) {
    return runM + " m of trim with a labeled " + wastePct + "% waste is " + r.need + " m to buy: " + plural(r.boards, "board") + " of " + boardM + " m, " + r.spare + " m left over - " + r.verdict + ".";
  }

  function renderCorner(r, inside, outside, allowCm) {
    return plural(inside, "inside corner") + " and " + plural(outside, "outside corner") + " mean " + plural(r.cuts, "mitre cut") + "; at a labeled " + allowCm + " cm of extra length a corner, add " + r.extra + " m - " + r.verdict + ".";
  }

  var api = { runPlan: runPlan, boardPlan: boardPlan, cornerPlan: cornerPlan, renderRun: renderRun, renderBoard: renderBoard, renderCorner: renderCorner };
  if (typeof module !== "undefined" && module.exports) module.exports = api; else root.TrimMath = api;
})(this);
