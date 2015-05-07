import nltk

# Tokenize the text of the article into sentences using the standard nltk sentence tokenization and returns as list
# Input the text from an article
def extract_sentences(text):
    text_No_Newline = text.replace("\n","")
    return nltk.sent_tokenize(text_No_Newline)

# Finds all sentences containing the query and returns these sentences as elements in a list.
# Input the text from an article and the query word/words
def extract_context(text,query):
    res = [];
    sentences = extract_sentences(text)
    for sent in sentences:
        if query in sent:
            res.append(sent)
    return res


# Finds all sentences containing the query. Returns a list where each element is a string. Apart from the sentence
# containing the query, each element also contains the sentence before and after the sentence containing the query
# (if applicable). This may lead to multiple elements being identical or almost identical.
# Input the text from an article and the query word/words
def extract_surrounded_context(text,query):
    res = [];
    sentences = extract_sentences(text)
    ii = 0
    for sent in sentences:
        tmp = []
        if query in sent:
            if ii > 0:
                tmp.append(sentences[ii-1])
                tmp.append(" ")
            tmp.append(sent)
            if ii < (len(sentences)-1):
                tmp.append(" ")
                tmp.append(sentences[ii+1])
        res.append("".join(tmp))
        ii += 1
    return res






