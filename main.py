
import json
import pdfplumber


pdf = pdfplumber.open('financial_markets_1.pdf')
bold_text = ""
text = ""
for i in range(6, 88):
    t = pdf.pages[i]
    text += (pdf.pages[i]).extract_text()
    b_text = t.filter(lambda obj: obj["object_type"] == "char" and "Bold" in obj["fontname"])
    bold_text += b_text.extract_text()

    
file = open("new_file", "w")
alphabets = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
            'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'
            'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
            'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
nums = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']


def subheaders(bold_text):
    que = []
    ind = []
    for i in range(len(bold_text)-2):
        if (bold_text[i] in nums) & (bold_text[i+2] in nums) & (bold_text[i+1]=='.'):
            if (i-2) not in ind:
                question = ''
                ind.append(i)
                for j in range(i+3, len(bold_text)):
                    if bold_text[j] in alphabets:
                        question += bold_text[j]
                    elif (bold_text[j] == ' '):
                        if (bold_text[j+1] in alphabets):
                            question += bold_text[j]
                    elif bold_text[j] == '?' or bold_text[j] == ' ' or bold_text[j] == ':':
                        question += bold_text[j]
                        que.append(question)
                        break
    return que


def que_format(text, index):
    if text[index] in nums:
        if (text[index+1] == '.') & (text[index+3] == '.'):
            if (text[index+2] in nums) & (text[index+4] in nums):
                 return True


def subh_format(text, index):
    if text[index] in nums:
        if (text[index+1] == '.') & (text[index+2] in nums) & (text[index+3] != '.'):
                 return True


def function(page_text):
    que_index = []
    que_end_index = []
    num_index = []
    ans_end_index = []
    lst_subheaders = subheaders(bold_text)

    for i in range(len(page_text)-4):
        if que_format(page_text, i):               
            num_index.append(i)
            for j in range(i+5, len(page_text)):
                if ((page_text[j] in alphabets) & (j not in que_index)):
                    if len(num_index)-1 == len(que_index):
                        que_index.append(j)        
                if (page_text[j] == '?') or (page_text[j] == ':'):
                    que_end_index.append(j)
                    break
        if (i-2) not in num_index:
            if subh_format(page_text, i):
                string = ""
                for j in range(i+3, len(page_text)):
                    if page_text[j] in alphabets:
                        string += page_text[j]
                    elif (page_text[j] == ' ') & (page_text[j+1] in alphabets):
                        string += page_text[j]
                    elif page_text[j] == '?' or page_text[j] == ' ' or page_text[j] == ':':
                        string += page_text[j]
                        break
                for l in lst_subheaders:
                    if string in l:
                        if i not in ans_end_index:
                            ans_end_index.append(i)            
    return que_index, que_end_index, num_index, ans_end_index


def lst_questions(que_index, que_end_index, page_text):
    que = []
    for i in range(len(que_index)):
        que_start = que_index[i]
        que_end = que_end_index[i]
        question = page_text[que_start:que_end+1]
        que.append(question)
    return que


def lst_answers(num_index, que_end_index, ans_end_index, page_text):
    ans = []
    num_index.append(len(page_text))
    for i in range (len(que_end_index)):
        ans_start = que_end_index[i]
        ans_end = num_index[i+1]
        for j in ans_end_index:
            if (ans_start<j<ans_end):
                ans_end = j
                ans_end_index.remove(j)
        answer = page_text[ans_start+1:ans_end]
        ans.append(answer)
    return ans

    

def JSON(que_lst, ans_lst):    
    for i in range(len(que_lst)):
        w = {}
        w["question"] = que_lst[i]
        w["answer"] = ans_lst[i]
        js_format = json.dumps(w)
        file.write(f"{js_format}\n")


a, b, c, d = function(text)
JSON(lst_questions(a, b, text), lst_answers(c, b, d, text))

        


