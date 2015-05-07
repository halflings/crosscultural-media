import nltk

# Tokenize the text of the article into sentences using the standard nltk sentence tokenization and returns as list
# Input the text from an article
def extract_sentences(text):
    return [sent.replace("\n","") for sent in nltk.sent_tokenize(text)]

# Finds all sentences containing any of the query words and returns these sentences as elements in a list.
# Input the text from an article and the query word/words
def extract_context(text,query):
    res = [];
    sentences = extract_sentences(text)
    query_words = query.split(" ")
    for sent in sentences:
        if any(qw in sent for qw in query_words):
            res.append(sent)
    return res

# Finds all sentences containing any of the query words all well as all sentences preceding and following directly after
# such sentences.
# Input the text from an article and the query word/words
def extract_surrounded_context(text,query):
    res = [];
    sentences = extract_sentences(text)
    query_words = query.split(" ")
    first = False
    second = False
    ii = 0
    for sent in sentences:
        if any(qw in sent for qw in query_words):
            if ii > 0 and not first:
                res.append(sentences[ii-1])
            if not second:
                res.append(sent)
                first = True
            if ii < (len(sentences)-1):
                res.append(sentences[ii+1])
                second = True
        else:
            if second:
                first = True
            else:
                first = False
            second = False
        ii += 1
    return res

# Printing function for debugging
# def print_text(sentences):
#    for sent in sentences:
#        print(sent)




