from flask import Flask, request, redirect, render_template_string
import csv
import os
from datetime import datetime

app = Flask(__name__)

FOLDER = "TradingJournal"
FILE = "journal.csv"
PATH = os.path.join(FOLDER, FILE)

os.makedirs(FOLDER, exist_ok=True)

if not os.path.exists(PATH):
    with open(PATH, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "Date","Pair","Type","Lot","Entry","SL","TP",
            "Result","Pips","Profit","Risk %"
        ])

HTML = """
<!doctype html>
<title>Trading Journal</title>
<h2>📘 Trading Journal Web App</h2>

<form method="post">
Balance: <input name="balance" required><br><br>
Pair: <input name="pair" required><br>
Type: 
<select name="type">
  <option>buy</option>
  <option>sell</option>
</select><br>
Lot: <input name="lot" required><br>
Entry: <input name="entry" required><br>
SL: <input name="sl" required><br>
TP: <input name="tp" required><br>
Result:
<select name="result">
  <option>win</option>
  <option>loss</option>
</select><br><br>
<button type="submit">Save Trade</button>
</form>

<h3>📊 Trades</h3>
<table border="1">
<tr>
{% for h in headers %}<th>{{h}}</th>{% endfor %}
</tr>
{% for row in rows %}
<tr>{% for col in row %}<td>{{col}}</td>{% endfor %}</tr>
{% endfor %}
</table>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        balance = float(request.form["balance"])
        pair = request.form["pair"].upper()
        ttype = request.form["type"]
        lot = float(request.form["lot"])
        entry = float(request.form["entry"])
        sl = float(request.form["sl"])
        tp = float(request.form["tp"])
        result = request.form["result"]

        if ttype == "buy":
            pips = (tp-entry)/0.0001 if result=="win" else (entry-sl)/0.0001
        else:
            pips = (entry-tp)/0.0001 if result=="win" else (sl-entry)/0.0001

        profit = pips * lot * 10
        risk = abs(entry-sl)/0.0001 * lot * 10 / balance * 100

        with open(PATH, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                datetime.now().strftime("%Y-%m-%d %H:%M"),
                pair, ttype, lot, entry, sl, tp,
                result, round(pips,2), round(profit,2), round(risk,2)
            ])
        return redirect("/")

    with open(PATH) as f:
        rows = list(csv.reader(f))
    return render_template_string(
        HTML,
        headers=rows[0],
        rows=rows[1:]
    )

if __name__ == "__main__":
    app.run(debug=True)
