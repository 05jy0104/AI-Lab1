class Term:
    """表示逻辑项（常量、变量或函数）"""

    def __init__(self, name, is_variable=False, args=None):
        self.name = name
        self.is_variable = is_variable
        self.args = args if args is not None else []  # 函数参数

    def __str__(self):
        if self.args:
            return f"{self.name}({', '.join(str(arg) for arg in self.args)})"
        return self.name

    def __eq__(self, other):
        if not isinstance(other, Term):
            return False
        return (self.name == other.name and
                self.is_variable == other.is_variable and
                self.args == other.args)

    def __hash__(self):
        """添加hash方法，使Term可哈希"""
        return hash((
            self.name,
            self.is_variable,
            tuple(self.args)  # 将args列表转换为元组
        ))

    def copy(self):
        """创建项的深拷贝"""
        return Term(self.name, self.is_variable, [arg.copy() for arg in self.args])

    def contains_variable(self, var_name):
        """检查是否包含指定变量"""
        if self.is_variable and self.name == var_name:
            return True
        for arg in self.args:
            if arg.contains_variable(var_name):
                return True
        return False


class Literal:
    """表示文字（带符号的原子公式）"""

    def __init__(self, predicate, terms, negated=False):
        self.predicate = predicate  # 谓词名称
        self.terms = terms  # 参数列表
        self.negated = negated  # 是否为否定

    def __str__(self):
        sign = "¬" if self.negated else ""
        terms_str = ", ".join(str(term) for term in self.terms)
        return f"{sign}{self.predicate}({terms_str})"

    def __eq__(self, other):
        if not isinstance(other, Literal):
            return False
        return (self.predicate == other.predicate and
                self.terms == other.terms and
                self.negated == other.negated)

    def __hash__(self):
        """添加hash方法，使Literal可哈希"""
        return hash((
            self.predicate,
            tuple(self.terms),  # 将terms列表转换为元组
            self.negated
        ))

    def copy(self):
        """创建文字的深拷贝"""
        return Literal(self.predicate, [term.copy() for term in self.terms], self.negated)

    def is_complement(self, other):
        """检查两个文字是否互补"""
        return (self.predicate == other.predicate and
                self.terms == other.terms and
                self.negated != other.negated)


class Clause:
    """表示子句（文字的析取）"""

    def __init__(self, literals=None, source=None):
        self.literals = literals if literals is not None else []
        self.source = source  # 记录来源，用于追踪推理过程
        self.id = id(self)  # 唯一标识符

    def __str__(self):
        if not self.literals:
            return "□"  # 空子句
        return " ∨ ".join(str(literal) for literal in self.literals)

    def __eq__(self, other):
        if not isinstance(other, Clause):
            return False
        # 使用set比较，现在Literal是可哈希的
        return set(self.literals) == set(other.literals)

    def copy(self):
        """创建子句的深拷贝"""
        return Clause([literal.copy() for literal in self.literals], self.source)

    def is_empty(self):
        """检查是否为空子句"""
        return len(self.literals) == 0

    def standardize_variables(self, counter=None):
        """标准化变量（修复版本）- 自动保留常量"""
        if counter is None:
            counter = {'x': 0}

        # 创建变量映射表
        var_mapping = {}
        new_literals = []

        for literal in self.literals:
            new_terms = []
            for term in literal.terms:
                new_terms.append(self._standardize_term(term, var_mapping, counter))
            new_literals.append(Literal(literal.predicate, new_terms, literal.negated))

        return Clause(new_literals, self.source)

    def _standardize_term(self, term, var_mapping, counter):
        """标准化单个项 - 自动保留常量"""
        if term.is_variable:
            # 相同的变量名映射到相同的新名称
            if term.name not in var_mapping:
                new_name = f"v{counter['x']}"
                counter['x'] += 1
                var_mapping[term.name] = Term(new_name, is_variable=True)
            return var_mapping[term.name]
        elif term.args:
            # 递归处理函数参数
            new_args = [self._standardize_term(arg, var_mapping, counter) for arg in term.args]
            return Term(term.name, False, new_args)
        else:
            # 常量和函数符号保持不变
            return term.copy()