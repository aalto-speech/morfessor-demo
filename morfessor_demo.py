from ConfigParser import SafeConfigParser
import string
import random

from bottle import Bottle, run, static_file

import morfessor

import logging
logging.basicConfig(level=logging.INFO)

demo = Bottle()


def load_models():
    io = morfessor.MorfessorIO(encoding='utf-8')
    scp = SafeConfigParser()
    scp.read('config')

    metadata = []
    models = {}
    wordlists = {}

    for section in scp.sections():
        key = section
        lang = scp.get(key, 'lang')
        desc = scp.get(key, 'desc')

        metadata.append((lang, key, desc))

        models[key] = io.read_binary_model_file('models/{}'.format(scp.get(key, 'model')))
        if scp.has_option(key, 'annomodel'):
            models["{}anno".format(key)] = io.read_binary_model_file('models/{}'.format(scp.get(key, 'annomodel')))

        if scp.has_option(key, 'evalset'):
            wordlists["{}eval".format(key)] = io.read_annotations_file('models/{}'.format(scp.get(key,'evalset')))


    return metadata, models, wordlists


def find_special_chars(model):
    all_chars = set(k for k,v in model._lexicon_coding.atoms.items() if v > 10)
    return list(all_chars - set(string.ascii_lowercase) - set(string.punctuation))

metadata, models, wordlists = load_models()


@demo.route('/')
def htmlpage():
    return static_file('index.html', root='./static')


@demo.route('/static/<filename>')
def staticfiles(filename):
    return static_file(filename, root='./static/static')


@demo.route('/models')
def get_models():
    return dict(models=metadata)


def format_nbest(nbest, correct):
    costs = [n[1] for n in nbest]
    mc = max(costs)
    rels = [mc/c for c in costs]
    fonts = [r / sum(rels) for r in rels]

    return [{'segm': tuple(n[0]), 'cost': n[1], 'fsize': f, 'correct': tuple(n[0]) in correct}
            for n, f in zip(nbest, fonts)]


@demo.route('/segment/<model>/<word>')
def segment_word(model, word):

    word = word.decode("utf-8")
    result = {}
    correct = set()
    evalset = "{}eval".format(model)
    if evalset in wordlists:
        if word in wordlists[evalset]:
            correct = set(tuple(x) for x in wordlists[evalset][word])
            result['correct'] = list(correct)


    result['standard'] = format_nbest(models[model].viterbi_nbest(word, 5), correct)
    anno_model = "{}anno".format(model)
    if anno_model in models:
        result['anno'] = format_nbest(models[anno_model].viterbi_nbest(word, 5), correct)


    return result

@demo.route("/info/<modelname>")
def model_info(modelname):
    model = models[modelname]
    anno_modelname = "{}anno".format(modelname)
    eval_name = "{}eval".format(modelname)

    result = {}
    result['num_compounds'] = model._num_compounds if model._segment_only else len(model.get_compounds())
    result['corpus_weight'] = model._corpus_coding.weight
    result['num_morphs'] = len(model.get_constructions())

    result['special_chars'] = find_special_chars(model)

    result['supervised'] = False
    if anno_modelname in models:
        anno_model = models[anno_modelname]
        result['supervised'] = True
        result['num_annotations'] = len(anno_model.annotations)
        result['annotation_weight'] = anno_model._annot_coding.weight

    if eval_name in wordlists:
        result['evalwords'] = random.sample(wordlists[eval_name].keys(), 100)
    return result

if __name__ == "__main__":
    run(demo, host="0.0.0.0", port=8080)