from ConfigParser import SafeConfigParser
from bottle import Bottle, run, static_file
import morfessor

demo = Bottle()


def load_models():
    io = morfessor.MorfessorIO()
    scp = SafeConfigParser()
    scp.read('config')

    metadata = []
    models = {}

    for section in scp.sections():
        key = section
        lang = scp.get(key, 'lang')
        desc = scp.get(key, 'desc')

        metadata.append((key, lang, desc))

        models[key] = io.read_binary_model_file('models/{}'.format(scp.get(key, 'model')))
        if scp.has_option(key, 'annomodel'):
            models["{}anno".format(key)] = io.read_binary_model_file('models/{}'.format(scp.get(key, 'annomodel')))

    return metadata, models

metadata, models = load_models()


@demo.route('/')
def htmlpage():
    return static_file('index.html', root='./static')


@demo.route('/static/<filename>')
def staticfiles(filename):
    return static_file(filename, root='./static/static')


@demo.route('/models')
def get_models():
    return dict(models=[('Estonian', 'est', '3.908.820 word forms'),
                        ('Finnish', 'fin', '2.206.719 word forms'),
                        ('Turkish', 'tur', '617.298 word forms'),
                        ('English', 'eng', '384.903 word forms'),
                        ])


def format_nbest(nbest):
    costs = [n[1] for n in nbest]
    mc = max(costs)
    rels = [mc/c for c in costs]
    fonts = [r / sum(rels) for r in rels]

    return [{'segm': n[0], 'cost': n[1], 'fsize': f}
            for n, f in zip(nbest, fonts)]


@demo.route('/segment/<model>/<word>')
def segment_word(model, word):
    result = {}
    result['standard'] = format_nbest(models[model].viterbi_nbest(word, 5))
    anno_model = "{}anno".format(model)
    if anno_model in models:
        result['anno'] = format_nbest(models[anno_model].viterbi_nbest(word, 5))

    return result


if __name__ == "__main__":
    run(demo, host='localhost', port=8080)