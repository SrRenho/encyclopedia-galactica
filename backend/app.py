from flask import Flask, request, render_template_string

import query

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head><title>Enciclopedia Galáctica</title></head>
<body>
  <h1>Consultá la Enciclopedia Galáctica de Isaac Asimov</h1>
  <form method="POST">
    <input type="text" name="user_input" style="width:300px;" autofocus autocomplete="off" />
    <input type="submit" value="Send" />
  </form>
  {% if response %}
    <p><b>Enciclopedia Galáctica:</b> <pre>{{ response }}</pre></p>
  {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def chat():
    response = None
    if request.method == "POST":
        user_input = request.form["user_input"]
        # call your llm here with user_input
        response = query.generate_response(user_input)  # or your actual function
    return render_template_string(HTML, response=response)

if __name__ == "__main__":
    query.__init__()
    app.run(debug=True)


