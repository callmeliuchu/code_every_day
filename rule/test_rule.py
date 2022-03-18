from rule import *
from settings import post_surgery_total_stage_rule, \
    after_neoadjuvant_total_stage_rule, t_stage_rule


def test_post_surgery_total_stage_rule():
    source = [[{'A': 'yp', 'C': 'T4b', 'D': 'N3'}, 'IVA'],
              [{'A': 'yp', 'C': 'T4a', 'D': 'N0（加一个字符串）'}, 'IVA'],
              [{'A': 'yp', 'C': 'T4a', 'D': 'N0'}, 'IIIB'],
              [{'A': 'yp', 'D': 'N2'}, 'IIIB'],
              [{'A': 'yp', 'C': 'T3', 'D': 'N1'}, 'IIIB'],
              [{'A': 'yp', 'D': 'N1'}, 'IIIA'],
              [{'A': 'yp', 'C': 'T3', 'D': 'N0'}, 'II'], [{'A': 'yp', 'D': 'N0'}, 'I'],
              [{'A': 'p', 'B': ['腺癌（加一个字符串）'], 'C': 'T4b', 'D': 'N3'}, 'IVA'],
              [{'A': 'p', 'B': ['腺癌（加一个字符串）'], 'C': 'T4a', 'D': 'N2'}, 'IVA'],
              [{'A': 'p', 'B': ['腺癌（加一个字符串）'], 'C': 'T4a', 'D': 'N1'}, 'IIIB'],
              [{'A': 'p', 'B': ['腺癌（加一个字符串）'], 'C': 'T3', 'D': 'N2'}, 'IIIB'],
              [{'A': 'p', 'B': ['腺癌（加一个字符串）'], 'C': 'T2', 'D': 'N2'}, 'IIIB'],
              [{'A': 'p', 'B': ['腺癌（加一个字符串）'], 'C': 'T2', 'D': 'N1'}, 'IIIA'],
              [{'A': 'p', 'B': ['腺癌（加一个字符串）'], 'C': 'T1', 'D': 'N2'}, 'IIIA'],
              [{'A': 'p', 'B': ['腺癌（加一个字符串）'], 'C': 'T1', 'D': 'N1'}, 'IIB'],
              [{'A': 'p', 'B': ['腺癌（加一个字符串）'], 'C': 'T3', 'D': 'N0', 'F': '食管胸下段', 'E': '分化不能评估（Gx）（加一个字符串）'},
               'IIA'], [{'A': 'p', 'B': ['腺癌（加一个字符串）'], 'C': 'T3', 'D': 'N0', 'F': '颈段', 'E': '高分化（G1）'}, 'IIA'],
              [{'A': 'p', 'B': ['腺癌（加一个字符串）'], 'C': 'T3', 'D': 'N0'}, 'IIB'],
              [{'A': 'p', 'B': ['腺癌（加一个字符串）'], 'C': 'T2', 'D': 'N0', 'E': '高分化（G1）'}, 'IB'],
              [{'A': 'p', 'B': ['腺癌（加一个字符串）'], 'C': 'T2', 'D': 'N0'}, 'IIA'],
              [{'A': 'p', 'B': ['腺癌（加一个字符串）'], 'C': 'T1b', 'D': 'N0'}, 'IB'],
              [{'A': 'p', 'B': ['腺癌（加一个字符串）'], 'C': 'T1a', 'D': 'N0', 'E': '高-中分化（G1-G2）'}, 'IB'],
              [{'A': 'p', 'B': ['腺癌（加一个字符串）'], 'C': 'T1a', 'D': 'N0'}, 'IA'],
              [{'A': 'p', 'B': ['腺癌（加一个字符串）'], 'C': 'Tis', 'D': 'N0'}, '0'],
              [{'A': 'p', 'B': ['腺癌'], 'F': '胃食管交界', 'C': 'T4b', 'D': 'N3'}, 'IVA'],
              [{'A': 'p', 'B': ['腺癌'], 'F': '胃食管交界', 'C': 'T4a', 'D': 'N2'}, 'IVA'],
              [{'A': 'p', 'B': ['腺癌'], 'F': '胃食管交界', 'C': 'T4a', 'D': 'N1'}, 'IIIB'],
              [{'A': 'p', 'B': ['腺癌'], 'F': '胃食管交界', 'C': 'T3', 'D': 'N2'}, 'IIIB'],
              [{'A': 'p', 'B': ['腺癌'], 'F': '胃食管交界', 'C': 'T2', 'D': 'N2'}, 'IIIB'],
              [{'A': 'p', 'B': ['腺癌'], 'F': '胃食管交界', 'C': 'T2', 'D': 'N1'}, 'IIIA'],
              [{'A': 'p', 'B': ['腺癌'], 'F': '胃食管交界', 'C': 'T1', 'D': 'N2'}, 'IIIA'],
              [{'A': 'p', 'B': ['腺癌'], 'F': '胃食管交界', 'C': 'T1', 'D': 'N1'}, 'IIB'],
              [{'A': 'p', 'B': ['腺癌'], 'F': '胃食管交界', 'C': 'T3', 'D': 'N0'}, 'IIB'],
              [{'A': 'p', 'B': ['腺癌'], 'F': '胃食管交界', 'C': 'T2', 'D': 'N0', 'E': '高分化（G1）'}, 'IC'],
              [{'A': 'p', 'B': ['腺癌'], 'F': '胃食管交界', 'C': 'T2', 'D': 'N0'}, 'IIA'],
              [{'A': 'p', 'B': ['腺癌'], 'F': '胃食管交界', 'C': 'T1b', 'D': 'N0', 'E': '中-低分化（G2-G3）'}, 'IC'],
              [{'A': 'p', 'B': ['腺癌'], 'F': '胃食管交界', 'C': 'T1b'}, 'IB'],
              [{'A': 'p', 'B': ['腺癌'], 'F': '胃食管交界', 'C': 'T1a', 'E': '高-中分化（G1-G2）'}, 'IB'],
              [{'A': 'p', 'B': ['腺癌'], 'F': '胃食管交界', 'C': 'T1a'}, 'IA'],
              [{'A': 'p', 'B': ['腺癌'], 'F': '胃食管交界', 'C': 'Tis', 'D': 'N0'}, '0']]

    for context, expected in source:
        print(context)
        ans = exec_rule(post_surgery_total_stage_rule, context)
        print(ans)
        print('-' * 40)


def test_parse_expression(self):
    expressions = ['C=T1 & D=N1', 'C=T4b | D=N3',
                   'E in [中-低分化（G2-G3）,低分化或未分化（G3）]',
                   'A=yp', 'C=T4a & (D=N0 | D=N1)',
                   '(C=T1a | C=T1b) & D=N0',
                   'E in [高分化（G1）,高-中分化（G1-G2）,中分化（G2）]',
                   'A=p & B!=[腺癌]',
                   'D=N0',
                   'C=T3 & (D=N1 | D=N2)',
                   'D=N1', 'A=p & (B=[腺癌] | F=胃食管交界)',
                   'E in [高-中分化（G1-G2）,中分化（G2）,中-低分化（G2-G3）,低分化或未分化（G3）]',
                   'C=T2 & D=N2',
                   'D=N2',
                   'C=T1a & D=N0',
                   'C=T3 & D=N1',
                   'C=T1b & D=N0',
                   'C=Tis & D=N0',
                   'C=T1a', 'C=T1b', 'C=T4a & D!=N0', 'C=T4a & D=N2',
                   'F=食管胸下段 & E!=分化不能评估（Gx）',
                   'C=T1a & E in [高-中分化（G1-G2）,中分化（G2）]',
                   'F in [颈段,食管胸上段,食管胸中段] & E=高分化（G1）',
                   'C=T1 & D=N2', 'C=T2 & D=N1', 'C=T3 & D=N0',
                   'C=T4a & D=N0',
                   'E=高分化（G1）', 'C=T2 & D=N0']
    for exp in expressions:
        print(exp)
        print(parse_expression2tree(exp))
        print('-' * 40)


def test_is_expression_true(self):
    context = {'A': 'yp', 'C': 'T3', 'D': 'N1'}
    expression = '((A=yp & C=T | (D=N)) | ((D=N & C=T3) | (D=N1 & C=T3)))'
    tree = parse_expression2tree(expression)
    print(tree)
    print(is_expression_tree_true(tree, context))


def test_after_neoadjuvant_total_stage_rule():
    contexts = [[{'A': ['（加一个字符串）'], 'D': 'M1'}, 'IVB'],
                [{'A': ['（加一个字符串）'], 'D': 'M0', 'B': 'T4a'}, 'IVA'],
                [{'A': ['（加一个字符串）'], 'B': 'T3', 'C': 'N1'}, 'III'],
                [{'A': ['（加一个字符串）'], 'B': 'T3', 'C': 'N0'}, 'II'],
                [{'A': ['（加一个字符串）'], 'B': 'T2'}, 'II'],
                [{'A': ['（加一个字符串）'], 'B': 'T1'}, 'I'],
                [{'A': ['腺癌'], 'E': ['胃食管交界'], 'D': 'M1'}, 'IVB'],
                [{'A': ['腺癌'], 'E': ['胃食管交界'], 'D': 'M0', 'B': 'T4b'}, 'IVA'],
                [{'A': ['腺癌'], 'E': ['胃食管交界'], 'D': 'M0', 'B': 'T4a'}, 'III'],
                [{'A': ['腺癌'], 'E': ['胃食管交界'], 'D': 'M0', 'B': 'T2', 'C': 'N1'}, 'III'],
                [{'A': ['腺癌'], 'E': ['胃食管交界'], 'D': 'M0', 'B': 'T2', 'C': 'N0'}, 'IIB'],
                [{'A': ['腺癌'], 'E': ['胃食管交界'], 'D': 'M0', 'B': 'T1', 'C': 'N1'}, 'IIA'],
                [{'A': ['腺癌'], 'E': ['胃食管交界'], 'D': 'M0', 'B': 'T1', 'C': 'N'}, '']]
    for context, expected in contexts:
        print(context)
        ans = exec_rule(after_neoadjuvant_total_stage_rule, context)
        print('-' * 40)


def test_t_stage_rule():
    source = [[{'B': ['主动脉', '椎体', '气管', '隆凸', '左主支气管', '右主支气管',
                      '下肺静脉', '肺组织', '腹腔动脉干', '下腔静脉', '乳糜池']}, 'T4b'],
              [{'B': ['胸膜', '心包', '膈肌', '腹膜', '胸导管', '迷走神经', '左侧喉返神经',
                      '右侧喉返神经', '奇静脉', '胃体', '胃小弯', '胃大弯', '胃底']}, 'T4a'],
              [{'C': ['外膜层', '全层', '周围组织']}, 'T3'], [{'C': ['肌层', '固有肌层', '浅肌层', '深肌层']}, 'T2'],
              [{'C': ['粘膜下层']}, 'T1b'], [{'C': ['粘膜固有层', '粘膜肌层']}, 'T2'],
              [{'E': ['random'], 'D': ['胃镜', 'random']}, 'T3']]
    for context, expected in source:
        print(context)
        ans = exec_rule(t_stage_rule, context)
        print(ans)
        print('-' * 40)
