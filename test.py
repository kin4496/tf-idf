from concurrent.futures import process
from konlpy.tag import Okt
import math

okt = Okt()

docs=[]
tf_docs=[]
idf_terms={}
posting_lists={}

def read_docs(file):
    docs.append("지미 카터 제임스 얼 지미 카터 주니어는 민주당 출신 미국 39번째 대통령이다. 지미 카터는 조지아 주 한 마을에서 태어났다. 조지아 공과대학교를 졸업하였다. 그 후 해군에 들어가 전함·원자력·잠수함의 승무원으로 일하였다.");
    docs.append("체첸 공화국 체첸 공화국 또는 줄여서 체첸은 러시아의 공화국이다. 체첸에서 사용되는 언어는 체첸어와 러시아어이다. 체첸어는 캅카스제어 중, 북동 캅카스제어로 불리는 그룹에 속하는데 인구시어와 매우 밀접한 관계에 있다.")
    docs.append("백남준 백남준은 한국 태생의 미국 미술작가, 작곡가, 전위 예술가이다. 여러 가지 매체로 예술 활동을 하였고 특히 비디오 아트라는 새로운 예술을 창안하여 발전시켰다는 평가를 받는 예술가로서 '비디오 아트의 창시자'로 알려져 있다. ");

def parse_doc(idx,tool=Okt()):
    
    doc=docs[idx]
    term_count={}
    parsed_doc= tool.morphs(doc)
    for term in parsed_doc:
        if term in term_count:
            term_count[term]+=1
        else:
            term_count[term]=1
            process_postingList(idx,term)
    process_tf(term_count)

def parse_docs(file=""):
    
    read_docs(file)
    N=len(docs)
    for i in range(0,N):
        parse_doc(i)

def process_postingList(doc,term):
    if term in posting_lists:
        posting_lists[term].append(doc)
    else:
        posting_lists[term]=[doc]

def process_tf(term_count):
    tf_doc={}
    for term in term_count.keys():
        cnt=term_count[term]
        tf_doc[term]=1+math.log10(cnt)
    tf_docs.append(tf_doc)

def process_idf():
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

def search(q,k,tool=Okt()):
    ret=[]
    N=len(docs)
    score=[[0,i] for i in range(0,N)]
    parsed_q=tool.morphs(q)
    
    for term in parsed_q:
        posting_list=get_postingList(term)
        for doc in posting_list:
            score[doc][0]+=get_idf(term)*get_tf(doc,term)

    score.sort(key=lambda x:x[0],reverse=True)

    for i in range(0,k):
        ret.append(score[i][1])
    return ret;

def print_doc(doc):
    print("문서 번호: ",doc+1)
    print(docs[doc])
    
parse_docs()
q=input("검색어를 입력하세요 ")
result=search(q,1)
for i in result:
    print_doc(i)