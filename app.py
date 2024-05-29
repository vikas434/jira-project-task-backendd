from flask import Flask, jsonify, request

app = Flask(__name__)

# Hardcoded data
projects = [
    {
        "projectName": "P1",
        "createdDate": "2010-10-27",
        "projectId": "FM_SN1_Planning_PRJ2",
        "manager": "snadmin, snadmin",
        "start": "2010-01-01",
        "currencyCode": "EUR",
        "budget": 0.2
    },
    {
        "projectName": "P2",
        "createdDate": "2010-10-27",
        "projectId": "FM_SN1_Planning_PRJ3",
        "manager": "snadmin, snadmin",
        "start": "2010-01-01",
        "currencyCode": "EUR",
        "budget": 2
    },
    {
        "projectName": "P3",
        "createdDate": "2011-06-01",
        "projectId": "FM_SN1_Planning_PRJ5",
        "manager": "snadmin, snadmin",
        "start": "2011-06-01",
        "currencyCode": "EUR",
        "budget": 0.2
    },
    {
        "projectName": "P4",
        "createdDate": "2023-07-03",
        "projectId": "20448",
        "manager": "Amos, Cheryl",
        "start": "2023-06-01",
        "currencyCode": "EUR",
        "budget": 0.365136
    },
    {
        "projectName": "P5",
        "createdDate": "2013-07-04",
        "projectId": "csk.infrastructure",
        "manager": "Martin, Paul",
        "start": "2023-07-31",
        "currencyCode": "USD",
        "budget": 3.92
    }
]

# Hardcoded task data
tasks = [
    {
        "taskId": 1,
        "projectId": "P1",
        "status": "Completed",
        "owner": "Joe",
        "description": "Random task 1",
        "startDate": "2023-01-01",
        "endDate": "2023-06-01"
    },
    {
        "taskId": 2,
        "projectId": "P2",
        "status": "Started",
        "owner": "Jenny",
        "description": "Random task 2",
        "startDate": "2023-01-08",
        "endDate": "2023-06-08"
    },
    {
        "taskId": 3,
        "projectId": "P3",
        "status": "Not Started",
        "owner": "Sam",
        "description": "Random task 3",
        "startDate": "2023-01-15",
        "endDate": "2023-06-15"
    },
    {
        "taskId": 4,
        "projectId": "P4",
        "status": "Blocked",
        "owner": "Alex",
        "description": "Random task 4",
        "startDate": "2023-01-22",
        "endDate": "2023-06-22"
    },
    {
        "taskId": 5,
        "projectId": "P5",
        "status": "Completed",
        "owner": "Taylor",
        "description": "Random task 5",
        "startDate": "2023-01-29",
        "endDate": "2023-06-29"
    },
    {
        "taskId": 6,
        "projectId": "P6",
        "status": "Started",
        "owner": "Joe",
        "description": "Random task 6",
        "startDate": "2023-02-05",
        "endDate": "2023-07-05"
    },
    {
        "taskId": 7,
        "projectId": "P1",
        "status": "Not Started",
        "owner": "Jenny",
        "description": "Random task 7",
        "startDate": "2023-02-12",
        "endDate": "2023-07-12"
    },
    {
        "taskId": 8,
        "projectId": "P2",
        "status": "Completed",
        "owner": "Sam",
        "description": "Random task 8",
        "startDate": "2023-02-19",
        "endDate": "2023-07-19"
    },
    {
        "taskId": 9,
        "projectId": "P2",
        "status": "Blocked",
        "owner": "Alex",
        "description": "Random task 9",
        "startDate": "2023-02-26",
        "endDate": "2023-07-26"
    },
    {
        "taskId": 10,
        "projectId": "PR1022",
        "status": "Started",
        "owner": "Taylor",
        "description": "Random task 10",
        "startDate": "2023-03-05",
        "endDate": "2023-08-05"
    }
]

@app.route('/projects', methods=['GET'])
def get_projects():
    filters = request.args
    filtered_projects = projects

    for key, value in filters.items():
        filtered_projects = [project for project in filtered_projects if str(project.get(key)) == value]

    return jsonify(filtered_projects)

@app.route('/projects', methods=['POST'])
def create_project():
    new_project = request.json
    projects.append(new_project)
    return jsonify(new_project), 201

@app.route('/projects/<projectId>', methods=['GET'])
def get_project(projectId):
    project = next((p for p in projects if p['projectId'] == projectId), None)
    if project:
        return jsonify(project)
    return jsonify({"error": "Project not found"}), 404

@app.route('/projects/<projectId>', methods=['PUT'])
def update_project(projectId):
    project = next((p for p in projects if p['projectId'] == projectId), None)
    if project:
        data = request.json
        project.update(data)
        return jsonify(project)
    return jsonify({"error": "Project not found"}), 404

@app.route('/projects/<projectId>', methods=['DELETE'])
def delete_project(projectId):
    global projects
    projects = [p for p in projects if p['projectId'] != projectId]
    return '', 204

@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify(tasks)

@app.route('/tasks', methods=['POST'])
def create_task():
    new_task = request.json
    tasks.append(new_task)
    return jsonify(new_task), 201

@app.route('/tasks/<int:taskId>', methods=['GET'])
def get_task(taskId):
    task = next((t for t in tasks if t['taskId'] == taskId), None)
    if task:
        return jsonify(task)
    return jsonify({"error": "Task not found"}), 404

@app.route('/tasks/<int:taskId>', methods=['PUT'])
def update_task(taskId):
    task = next((t for t in tasks if t['taskId'] == taskId), None)
    if task:
        data = request.json
        task.update(data)
        return jsonify(task)
    return jsonify({"error": "Task not found"}), 404

@app.route('/tasks/<int:taskId>', methods=['DELETE'])
def delete_task(taskId):
    global tasks
    tasks = [t for t in tasks if t['taskId'] != taskId]
    return '', 204

if __name__ == '__main__':
    app.run(debug=True)
