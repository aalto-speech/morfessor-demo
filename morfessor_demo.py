from bottle import Bottle, run, static_file

demo = Bottle()


@demo.route('/')
def htmlpage():
    return static_file('index.html', root='./static')


@demo.route('/static/<filename>')
def staticfiles(filename):
    return static_file(filename, root='./static')


@demo.route()
def get_models():
    return dict(models=[('Estonian', 'est', '3.908.820 word forms'),
                        ('Finnish', 'fin', '2.206.719 word forms'),
                        ('Turkish', 'tur', '617.298 word forms'),
                        ('English', 'eng', '384.903 word forms'),
                        ])


if __name__ == "__main__":
    run(demo, host='localhost', port=8080)