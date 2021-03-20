#!coding=utf-8

from celery import Celery

app = Celery('tasks', backend='redis://redis', broker='redis://redis')


@app.task
def add(x, y):
    return x + y
