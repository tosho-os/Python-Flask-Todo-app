from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def todo():
    if request.method == 'POST':
        # Name of your form
        add_task = request.form['taskform'] 
        # database connection
        conn = sqlite3.connect('database.db')
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute('INSERT INTO todo (task, is_done) VALUES (?, 0)', (add_task,))
        conn.commit()
        conn.close()

    # Fetch tasks after possible insert
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('SELECT id, task, is_done FROM todo')
    tasks = c.fetchall()
    conn.close()

    return render_template('todo.html', 
            title='Do it',
            tasks=tasks)


@app.route('/delete', methods=['POST'])
def delete_task():
    del_task = request.form['del_task']  # get from form data
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('DELETE FROM todo WHERE id = ?', (del_task,))
    conn.commit()
    conn.close()
    return redirect(url_for('todo'))

@app.route('/mark_done', methods=['POST'])
def mark_done():
    mark_done = int(request.form['mark_done'])
    task_id = request.form['task_id']
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('UPDATE todo SET is_done = ? WHERE id = ?', (mark_done, task_id))
    conn.commit()
    conn.close()
    return redirect(url_for('todo'))


if __name__ == '__main__':
   app.run(debug=True)