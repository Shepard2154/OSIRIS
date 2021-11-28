from sentimental import Sentimental
import pymorphy2
sent = Sentimental()
morph = pymorphy2.MorphAnalyzer()

def get_sentiment(selectText):
    words = [morph.parse(word)[0].normal_form for word in re.findall(r'\w+', selectText)]
    #sentence_2 = {" ".join(words)}
    sentence = " ".join(words)
    result = sent.analyze(sentence)
    return(result)