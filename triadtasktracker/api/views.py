from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

import json

from api.models import Task

def index(request):
    response = json.dumps([{ 'Supported Queries': [
            { 'Get Task': [
                { 'Method': 'GET'},
                { 'Required Parameters': 'task_id' },
                { 'Optional Parameters': '' },
                { 'Parameter Details': [
                    { 'task_id': [
                        { 'type': 'integer' },
                        { 'description': 'Unique ID for task' }
                    ]},
                ]},
                { 'Response': 'text/json' },
                { 'Description': 'Returns task information' },
            ]},
            { 'Add Task': [
                { 'Method': 'POST'},
                { 'Required Parameters': 'task_name' },
                { 'Optional Parameters': '' },
                { 'Parameter Details': [
                    { 'task_name': [
                        { 'type': 'string/varchar/char[]' },
                        { 'description': 'The name of the task' },
                    ]},
                ]},
                { 'Response': 'text/json' },
                { 'Description': 'Returns task information' },
            ]}
        ]}]);
    return HttpResponse(response, content_type='text/json')

def get_task(request, task_id):
    if request.method == 'GET':
        try:
            task = Task.objects.get(id=task_id)
            response = json.dumps([{ 'Task': task.name, 'Completed': task.completed}])
            #response = json.dumps([{'temp':'temp'}])
        except:
            response = json.dumps([{ 'Error': 'No task with that id'}])
    return HttpResponse(response, content_type='text/json')

@csrf_exempt
def tasks(request):
    print('method: ', request.method)
    if request.method == 'GET':
        print('GET test')
        return get_tasks(request)
    elif request.method == 'DELETE':
        return delete_task(request)
    elif request.method == 'PATCH':
        return update_task(request)
    elif request.method == 'POST':
        print('POST test')
        return add_task(request)
    else:
        response = json.dumps([{ 'Error': 'Unsupported HTTP Method for endpoint' }])
        return HttpResponse(response, content_type='text/json')

def get_tasks(request):
    print('pre-trying to get tasks')
    try:
        
        print('Trying to get tasks')
        tasks = Task.objects.all()
        print('all tasks: ', tasks)
        arr_dict_response = []
        for t in tasks:
            dict_response = {}
            dict_response['name'] = t.name
            dict_response['completed'] = t.completed
            dict_response['id'] = t.id

            arr_dict_response.append(dict_response)
        response = json.dumps(arr_dict_response)
        #response = json.dumps([{'temp':'temp'}])
    except:
        print('error trying to get tasks')
        response = json.dumps([{ 'Error': 'Issue retrieving tasks' }])
    return HttpResponse(response, content_type='text/json')

def delete_task(request):
    payload = json.loads(request.body)
    task_id = payload['id']
    try:
        Task.objects.filter(id=task_id).delete()
        response = json.dumps([{ 'Success': 'Task deleted successfully'}])
    except:
        response = json.dumps([{ 'Error': 'Task with specified id could not be found/deleted'}])
    return HttpResponse(response, content_type='text/json')

def update_task(request):
    payload = json.loads(request.body)
    task_id = payload['id']
    try:
        task = Task.objects.get(id=task_id)
        print("TESTING COMPLETION OF TASK:",task.completed)
        if task.completed == 1:
            Task.objects.filter(id=task_id).update(completed=0)
        elif task.completed == 0:
            Task.objects.filter(id=task_id).update(completed=1)
        response = json.dumps([{ 'Success': 'Task updated successfully'}])
    except:
        response = json.dumps([{ 'Error': 'Task with specified id could not be found/updated'}])
    return HttpResponse(response, content_type='text/json')

def add_task(request):
    print('pre-trying to add tasks')
    payload = json.loads(request.body)
    task_name = payload['name']
    task = Task(name=task_name, completed=False)
    try:
        print('trying to add task')
        task.save()
        response = json.dumps([{ 'Success': 'Task added successfully'}])
    except:
        print('error trying to add task')
        response = json.dumps([{ 'Error': 'Task could not be added'}])
    return HttpResponse(response, content_type='text/json')

