import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation

text= """ It’s important to note that the $842 billion proposed price tag for the Pentagon next year will 
only be the beginning of what taxpayers will be asked to shell out in the name of “defense.” If you add in nuclear weapons
 work at the Department of Energy and small amounts of military spending spread across other agencies, you’re already at a
   total military budget of $886 billion. And if last year is any guide, Congress will add tens of billions of dollars 
   extra to that sum, while yet more billions will go for emergency aid to Ukraine to help it fend off Russia’s brutal 
   invasion. In short, we’re talking about possible total spending of well over $950 billion on war and preparations for 
   more of it — within striking distance, in other words, of the $1 trillion mark that hawkish officials and pundits could
     only dream about a few short years ago."""

def summarizer(rawdocs):
    stopwords=list(STOP_WORDS)
    #print(stopwords)
    nlp=spacy.load('en_core_web_sm')
    doc=nlp(rawdocs)
    #print(doc)
    tokens=[token.text for token in doc]
    #print(tokens)
    word_freq= {}
    for word in doc:
        if word.text.lower() not in stopwords and word.text.lower() not in punctuation:
            if word.text not in word_freq.keys():
                word_freq[word.text]=1
            else:
                word_freq[word.text]+=1

    #print(word_freq)]
    max_freq=max(word_freq.values())
    #print(max_freq)

    for word in word_freq.keys():
        word_freq[word]=word_freq[word]/max_freq
    #print(word_freq)

    sent_tokens= [sent for sent in doc.sents]
    #print(sent_tokens)

    sent_scores={}
    for sent in sent_tokens:
        for word in sent:
            if word.text in word_freq.keys():
                if sent not in sent_scores.keys():
                    sent_scores[sent]=word_freq[word.text]
                else:
                    sent_scores[sent]+=word_freq[word.text]
    #print(sent_scores)

    select_len=int(len(sent_tokens) *0.3)
    #print(select_len)
    from heapq import nlargest
    summary=nlargest(select_len,sent_scores,key=sent_scores.get)
    #print(summary)

    final_summary=[word.text for word in summary]
    summary=' '.join(final_summary)
    # print(summary)
    # print('------------')
    # print(text)
    # print('------------')
    # print("Length of original text", len(text.split(' ')))
    # print("Length of summary text", len(summary.split(' ')))

    return summary, doc ,len(rawdocs.split(' ')),len(summary.split(' '))