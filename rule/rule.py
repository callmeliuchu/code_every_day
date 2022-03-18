import csv
from collections import defaultdict


class Node:

    def __init__(self, val):
        self.value = val
        self.data = val
        self.left = None
        self.right = None

    def __str__(self):
        if self.left or self.right:
            return '{}({},{})'.format(self.data, self.left, self.right)
        else:
            return self.data


def parse_expression2tree(s):
    """
    此方法主要来解析表达式，转换成二叉树格式
    """
    s = s.strip()
    if s.startswith('('):
        i = 0
        n = len(s)
        count = 0
        while i < n:
            if s[i] == '(':
                count += 1
            if s[i] == ')':
                count -= 1
                if count == 0:
                    break
            i += 1
        left = s[1:i]
        j = i + 1
        while j < n and s[j] not in '&|':
            j += 1
        if j < n:
            op = s[j]
            right = s[j + 1:]
            node = Node(op)
            node.left = parse_expression2tree(left)
            node.right = parse_expression2tree(right)
            return node
        else:
            return parse_expression2tree(left)
    else:
        i = 0
        n = len(s)
        while i < n and s[i] not in '&|':
            i += 1
        if i < n:
            op = s[i]
            node = Node(op)
            node.left = parse_expression2tree(s[:i])
            node.right = parse_expression2tree(s[i + 1:])
            return node
        else:
            return Node(s)


def not_in_op(v1, v2):
    if not isinstance(v1, list):
        v1 = [v1]
    if not isinstance(v2, list):
        v2 = [v2]
    for x1 in v1:
        for x2 in v2:
            if x1 in x2:
                return False
    return True


def in_op(v1, v2):
    if not isinstance(v1, list):
        v1 = [v1]
    if not isinstance(v2, list):
        v2 = [v2]
    for x1 in v1:
        for x2 in v2:
            if x1 in x2:
                return True
    return False


def contains_op(v1, v2):
    return in_op(v2, v1)


def not_contains_op(v1, v2):
    return not_in_op(v2, v1)


def equal_op(v1, v2):
    if not isinstance(v1, list):
        v1 = [v1]
    if not isinstance(v2, list):
        v2 = [v2]
    v1.sort()
    v2.sort()
    return v1 == v2


def not_equal_op(v1, v2):
    return not equal_op(v1, v2)


class ExpressionHelper:

    def __init__(self, context):
        self.context = context
        self.op_mapping = {
            'in': in_op,
            'not in': not_in_op,
            'contains': contains_op,
            'not contains': not_contains_op,
            '=': equal_op,
            '!=': not_equal_op
        }

    @staticmethod
    def parse_right(right):
        right = right.strip()
        if right.startswith('['):
            right = right[1:len(right) - 1]
            right = right.strip()
            right_val = [v.strip() for v in right.split(',')]
        else:
            right_val = right.strip()
        return right_val

    @staticmethod
    def parse_left(left):
        return left.strip()

    @staticmethod
    def split(s):
        ops = ['!=', 'not in', 'not contains', 'contains', '=', 'in']
        op = ''
        left = ''
        right = ''
        for x in ops:
            if x in s:
                left, right = s.split(x)
                op = x
                break
        if not left and not right:
            raise Exception('{}不是一个基本表达式'.format(s))
        return left, op, right

    def is_true(self, s):
        left, op, right = self.split(s)
        left = self.parse_left(left)
        right = self.parse_right(right)
        if left not in self.context:
            return False
        if op in self.op_mapping:
            return self.op_mapping[op](self.context[left], right)
        return False


def is_expression_tree_true(tree, context):
    exp_helper = ExpressionHelper(context)

    def dfs(root):
        if not root:
            return False
        if root.data not in '&|':
            return exp_helper.is_true(root.data)
        elif root.data == '&':
            return dfs(root.left) and dfs(root.right)
        elif root.data == '|':
            return dfs(root.left) or dfs(root.right)
        else:
            raise Exception("非法表达式")

    return dfs(tree)


def exec_rule(rule_data, context):
    def dfs(rule):
        if isinstance(rule, dict):
            for key in rule:
                tree = parse_expression2tree(key)
                if is_expression_tree_true(tree, context):
                    v = dfs(rule[key])
                    if v is not None:
                        return v
            return None
        elif isinstance(rule, list):
            for o in rule:
                v = dfs(o)
                if v:
                    return v
            return None
        else:
            return rule

    r = dfs(rule_data)
    if r is None:
        return ''
    return r


def fetch_all_condition(data):
    if isinstance(data, dict):
        ans = []
        for key in data:
            ret = fetch_all_condition(data[key])
            for t in ret:
                ans.append([key] + t)
        return ans
    elif isinstance(data, list):
        ans = []
        for o in data:
            ans.extend(fetch_all_condition(o))
        return ans
    else:
        return [[]]


def flatten(data):
    if isinstance(data, list):
        ans = []
        for o in data:
            ans.extend(flatten(o))
        return ans
    else:
        return [data]


def get_tree_leaves(root):
    if not root:
        return []
    if not root.left and not root.right:
        return [root.data]
    return get_tree_leaves(root.left) + get_tree_leaves(root.right)


def put_x2y(x, y):
    if not isinstance(x, list):
        x = [x]
    y.extend(x)


def generate_context(expressions):
    tmp = []
    for exp in expressions:
        tree = parse_expression2tree(exp)
        tmp.extend(get_tree_leaves(tree))
    expressions = tmp
    ans = defaultdict(list)
    for exp in expressions:
        left, op, right = ExpressionHelper.split(exp)
        left = ExpressionHelper.parse_left(left)
        right = ExpressionHelper.parse_right(right)
        if not isinstance(right, list):
            right = [right]
        if op == '=':
            ans[left].extend(right)
        elif op == '!=':
            if isinstance(right, list):
                ans[left].extend([v + '（加一个字符串）' for v in right])
        elif op == 'in':
            ans[left].append(right[0])
        elif op == 'contains':
            ans[left].extend(right)
        elif op == 'not contains':
            ans[left].append('random')
        elif op == 'not in':
            ans[left].append('random')
    return dict(ans)


def get_tree_data_from_csv(file_path):
    """本方法从csv读取树形结构的if else 结构规则"""

    def parse(path):
        rows = []
        with open(path, 'r') as f:
            data = csv.reader(f)
            for row in data:
                r = [v.strip() for v in row]
                n = len(r)
                i = n - 1
                while i > 0:
                    if r[i] == '':
                        i -= 1
                    else:
                        break
                rows.append(r[:i + 1])
        return rows

    def parse_pieces(rows):
        n = len(rows)
        i = 0
        pieces = []
        while i < n:
            if rows[i][0] != '':
                tmp = []
                if rows[i][1:]:
                    tmp.append(rows[i][1:])
                j = i + 1
                while j < n and rows[j][0] == '':
                    if rows[j][1:]:
                        tmp.append(rows[j][1:])
                    j += 1
                pieces.append([rows[i][0], tmp])
                i = j
        return pieces

    def dfs(rows):
        pieces = parse_pieces(rows)
        ret = []
        for key, r in pieces:
            if len(r) == 0:
                ret.append(key)
            else:
                ret.append({key: dfs(r)})
        return ret

    all_rows = parse(file_path)
    return dfs(all_rows)
