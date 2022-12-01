from flask import Flask, redirect, url_for, request, render_template
import query

app = Flask(__name__)

@app.route('/success/<name>')
def success(name):
    results = query.query(name)
    #results = ("test", "test", "time")
    return render_template("results.html", name=name, results=results)
    #return 'welcome %s' % name

@app.route('/search', methods=['POST', 'GET'])
def search():
    if request.method == 'POST':
        search_query = request.form['nm']
        return redirect(url_for('success', name=search_query))
    else:
        search_query = request.args.get('nm')
        return redirect(url_for('success', name=search_query))

if __name__ == '__main__':
    app.run(debug=True)