from scheduling import app


worker = app.Worker(include=['scheduling.tasks'])

beat = app.Beat(loglevel='debug')


if __name__ == '__main__':
    worker.start()
    beat.run()
