from flask import Flask , render_template , jsonify , redirect , request
import pyodbc


app = Flask(__name__)



def get_connection():
    try:
        conn = pyodbc.connect('DRIVER={FreeTDS};SERVER=host.docker.internal;PORT=1433;DATABASE=family_tasks;UID=sa;PWD=12345678Aab')
        return conn
    except:
        return 'Connection failed'


def task_by_id(task_id):
    """
    Description: Returns tasks of specific user
    """
    try:
        with get_connection() as connection:
            cursor = connection.cursor()
            id = int(task_id)
            query = """select t.id, n.name, t.description, t.subject, t.due_date
                            from Tasks t join Names n on t.id = n.id
                            where t.id = (?)"""

            cursor.execute(query, id)
            query_result = cursor.fetchall()
            cursor.close

            return render_template('tasks.html', tasks = query_result)
        
    except Exception as e:
        return jsonify("message: " + str(e))


@app.route('/get_task' , methods = ['GET' , 'POST'])
def get_task():
    """
    Description: Enables user to select a name and returns associated tasks
    """
    try:
        with get_connection() as connection:
            cursor = connection.cursor()

            if request.method == 'POST':
                id = request.form.get('id')

                return task_by_id(id)
            else:
                query = """select * from Names"""
                cursor.execute(query)

                query_results = [{'name': name.name, 'id': name.id} for name in cursor.fetchall()]
                print (query_results) 
                return render_template('tasks.html' , my_names = query_results)
            
    except Exception as e:
        return jsonify("message: " + str(e))


@app.route('/create_task' , methods = ['GET' , 'POST'])
def create_task():
    """
    Description: Enables user to create a new task
    """
    try:
        with get_connection() as connection:
            cursor = connection.cursor()
            if request.method == 'POST':

                id = request.form.get('field4')
                description = request.form.get('description')
                subject = request.form.get('subject')
                due_date = request.form.get('due_date')

                query_tasks = """insert into [Tasks] values (?,?,?,?)"""
                cursor.execute(query_tasks, id, description , subject , due_date)
                cursor.commit()
                
                return get_tasks_from_db()
            else:
                query = """select * from Names"""
                cursor.execute(query)

                results = [{'name': name.name, 'id': name.id} for name in cursor.fetchall()]
                    
                return render_template('index.html' , names = results)
    
    except Exception as e:
        return jsonify("message: " + str(e))
        
        
@app.route('/' , methods = ['GET'])
def get_tasks_from_db():
    """
    Description: Function to display main web page containing a full list of tasks
    """
    try:
        with get_connection() as connection:
            cursor = connection.cursor()

            query = """select t.id, n.name, t.description, t.subject, t.due_date
            from Tasks t join Names n on t.id = n.id"""

            cursor.execute(query)
            query_result = cursor.fetchall()
            
            return render_template('tasks.html', tasks = query_result)
        
    except Exception as e:
        return jsonify("message: " + str(e))
        

@app.route('/delete_task/<int:task_id>' ,  methods = ['POST'])       
def delete_task(task_id):
    """
    Description: Enables user to delete a task from database
    """
    try:
        with get_connection() as connection:
            cursor = connection.cursor()
            
            query = """delete from Tasks where id = (?)"""

            cursor.execute(query, (task_id,))
            cursor.commit()

            return redirect('/')
        
    except Exception as e:
        return jsonify("message: " + str(e))
            

@app.route('/add_name' , methods = ['POST'])
def add_name():
    """
    Description: Enables user to add names to database
    """
    try:
        with get_connection() as connection:
            cursor = connection.cursor()

            name = request.form.get('user_name')
            query = """insert into Names values (?)"""

            cursor.execute(query, name)
            cursor.commit()

            return redirect('/')
        
    except Exception as e:
        return jsonify("message: " + str(e))






if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)