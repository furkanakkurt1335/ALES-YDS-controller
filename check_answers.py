import os
import argparse
import re
parser = argparse.ArgumentParser()
parser.add_argument('--exam-type', action='store', required=True)
parser.add_argument('--exam-name', action='store', required=True)
args = parser.parse_args()
THIS_DIR = os.path.realpath(os.path.dirname(__file__))
exam_type = args.exam_type
exam_name = args.exam_name
gold_path = os.path.join(
    THIS_DIR, '{type}/Answers/Gold/{name}.txt'.format(type=exam_type, name=exam_name))
my_answers_path = os.path.join(
    THIS_DIR, '{type}/Answers/Mine/{name}.txt'.format(type=exam_type, name=exam_name))
with open(gold_path, 'r') as f:
    gold_lines = f.readlines()
with open(my_answers_path, 'r') as f:
    my_answers_lines = f.readlines()
answer_pattern = r'(\d+) ([a-e])'
if exam_type == 'YDS':
    correct, wrong, empty = 0, 0, 0
    wrong_l = []
    for i in range(len(gold_lines)):
        answer_found = re.search(answer_pattern, my_answers_lines[i])
        if not answer_found:
            empty += 1
            continue
        my_answer_t = answer_found.group(2)
        gold_answer_t = re.search(answer_pattern, gold_lines[i]).group(2)
        if my_answer_t == gold_answer_t:
            correct += 1
        else:
            wrong += 1
            wrong_l.append(i+1)
    y_all = correct + wrong + empty
    print(
        'Correct: {c}; Wrong: {w}; Empty: {e}; All: {a}; Score: {score}'.format(c=correct, w=wrong, e=empty, a=y_all, score=correct*1.25))
    print('Wrongs: ', end='')
    for i in wrong_l:
        print(i, end=' ')
elif exam_type == 'ALES':
    science_d, verbal_d = {'correct': 0, 'wrong': 0, 'empty': 0}, {
        'correct': 0, 'wrong': 0, 'empty': 0}
    science_wrong_l, verbal_wrong_l = [], []
    question_count = len(gold_lines)
    half_way = question_count//2
    for i in range(question_count):
        answer_found = re.search(answer_pattern, my_answers_lines[i])
        if not answer_found:
            if i < half_way:
                science_d['empty'] += 1
            else:
                verbal_d['empty'] += 1
            continue
        my_answer_t = answer_found.group(2)
        gold_answer_t = re.search(answer_pattern, gold_lines[i]).group(2)
        if my_answer_t == gold_answer_t:
            if i < half_way:
                science_d['correct'] += 1
            else:
                verbal_d['correct'] += 1
        else:
            if i < half_way:
                science_d['wrong'] += 1
                science_wrong_l.append(i+1)
            else:
                verbal_d['wrong'] += 1
                verbal_wrong_l.append(i+1-half_way)
    s_all = science_d['correct'] + science_d['wrong'] + science_d['empty']
    v_all = verbal_d['correct'] + verbal_d['wrong'] + verbal_d['empty']
    s_score = ((science_d['correct']-(science_d['wrong']/4))
               * .75 + (verbal_d['correct']-(verbal_d['wrong']/4))*.25)*2
    print(
        '# Science\n\tCorrect: {sc}; Wrong: {sw}; Empty: {se}; All: {sa}; Q Score: {q_score}'.format(sc=science_d['correct'], sw=science_d['wrong'], se=science_d['empty'], sa=s_all, q_score=s_score))
    print('\tWrongs: ', end='')
    for i in science_wrong_l:
        print(i, end=' ')
    print()
    print()
    print(
        '# Verbal\n\tCorrect: {vc}; Wrong: {vw}; Empty: {ve}; All: {va}'.format(vc=verbal_d['correct'], vw=verbal_d['wrong'], ve=verbal_d['empty'], va=v_all))
    print('\tWrongs: ', end='')
    for i in verbal_wrong_l:
        print(i, end=' ')
