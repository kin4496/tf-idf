from konlpy.tag import Kkma
import math


docs=[]
tf_docs=[]
idf_terms={}
posting_lists={}

def isNumber(c):
    return c>='0' and c<='9'

def isDot(c):
    return c=='.'

def parse_text(text):
    text=text.lstrip('<title>')
    text=text.rstrip('</title>\n')
    return text

def debug():
    for i in range(0,len(docs)):
        print_doc(i)

def read_docs(file):
    f=open(file,'r',encoding='utf-8')
    isEmptyLine=False
    title=""
    for i in range(0,300):
        text=f.readline()
        if isEmptyLine:
            isEmptyLine=False
            continue
        if "<title>" in text:
            title=parse_text(text)
        else:
            docs.append(title+' '+text)
            isEmptyLine=True
def isMark(tag):
    return (tag=='SF' or tag=='SE' or tag=='SS' or tag=='SP' or tag=='SO');
def parse_doc(idx,tool=Kkma()):
    
    doc=docs[idx]
    term_count={}
    parsed_doc= tool.pos(doc)
    for term,tag in parsed_doc:
        if isMark(tag):
            continue
        if term in term_count:
            term_count[term]+=1
        else:
            term_count[term]=1
            calc_postingList(idx,term)
    calc_tf(term_count)

def parse_docs(file=""):
    
    read_docs(file)
    N=len(docs)
    for i in range(0,N):
        parse_doc(i)
    calc_idf()

def calc_postingList(doc,term):
    if term in posting_lists:
        posting_lists[term].append(doc)
    else:
        posting_lists[term]=[doc]

def calc_tf(term_count):
    tf_doc={}
    for term in term_count.keys():
        cnt=term_count[term]
        tf_doc[term]=1+math.log10(cnt)
    tf_docs.append(tf_doc)

def calc_idf():
    N=len(docs)
    
    for term in posting_lists.keys():
        cnt=len(posting_lists[term])
        idf_terms[term]=math.log10(N/cnt)

def get_tf(doc,term):
    if term not in tf_docs[doc]:
        return 0;
    return tf_docs[doc][term];

def get_idf(term):
    if term not in idf_terms:
        return math.log10(len(docs));
    return idf_terms[term];

def get_postingList(term):
    if term not in posting_lists:
        return [];
    return posting_lists[term];

def search(q,k,tool=Kkma()):
    ret=[]
    N=len(docs)
    score=[[0,i] for i in range(0,N)]
    parsed_q=tool.pos(q)
    
    for term,tag in parsed_q:
        if isMark(tag):
            continue
        w=1
        if tag == 'NNP' or tag=='NNG':
            w=10
        elif tag=='VV':
            w=5
        posting_list=get_postingList(term)
        for doc in posting_list:
            score[doc][0]+=w*get_idf(term)*get_tf(doc,term)

    score.sort(key=lambda x:x[0],reverse=True)

    for i in range(0,k):
        ret.append(score[i][1])
    return ret;

def print_doc(doc):
    print("문서 번호: ",doc+1)
    print(docs[doc])

def test():
    parse_docs('data.txt')
    q=input("검색어를 입력하세요 ")
    result=search(q,5)
    for i in result:
        print_doc(i)


parse_docs('data.txt')
while(True):
    q=input("검색어를 입력하세요 ")
    if q== 'q':
        break
    result=search(q,5)
    for i in result:
        print_doc(i)
    for i in result:
        print(i+1,end=' ')
    print()