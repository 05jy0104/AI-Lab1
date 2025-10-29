from clause import Term, Literal, Clause


class Unifier:
    """合一算法实现"""

    @staticmethod
    def unify(term1, term2, substitution=None, depth=0):
        """
        合一两个项，返回最一般合一子
        返回: 如果可合一返回 substitution dict，否则返回 None
        """
        if depth > 50:  # 防止无限递归
            return None

        if substitution is None:
            substitution = {}

        # 如果两个项在当前替换下相等，直接返回
        term1 = Unifier.apply_substitution(term1, substitution)
        term2 = Unifier.apply_substitution(term2, substitution)

        if term1 == term2:
            return substitution

        # 快速检查：如果都是常量且不同，直接返回None
        if not term1.is_variable and not term2.is_variable:
            if term1.name != term2.name or len(term1.args) != len(term2.args):
                return None

        # 如果 term1 是变量
        if term1.is_variable:
            if Unifier.occurs_check(term1, term2):
                return None  # 出现循环
            substitution[term1.name] = term2
            return substitution

        # 如果 term2 是变量
        if term2.is_variable:
            if Unifier.occurs_check(term2, term1):
                return None  # 出现循环
            substitution[term2.name] = term1
            return substitution

        # 如果两个都是常量或函数，检查名称和参数
        if term1.name != term2.name or len(term1.args) != len(term2.args):
            return None

        # 递归合一参数
        for arg1, arg2 in zip(term1.args, term2.args):
            substitution = Unifier.unify(arg1, arg2, substitution, depth + 1)
            if substitution is None:
                return None

        return substitution

    @staticmethod
    def occurs_check(var, term):
        """检查变量是否出现在项中"""
        if var == term:
            return True
        if term.args:
            return any(Unifier.occurs_check(var, arg) for arg in term.args)
        return False

    @staticmethod
    def unify_literals(literal1, literal2):
        """
        合一两个文字
        返回: 如果可合一返回 substitution dict，否则返回 None
        """
        if literal1.predicate != literal2.predicate:
            return None

        if len(literal1.terms) != len(literal2.terms):
            return None

        substitution = {}
        for term1, term2 in zip(literal1.terms, literal2.terms):
            substitution = Unifier.unify(term1, term2, substitution)
            if substitution is None:
                return None

        return substitution

    @staticmethod
    def apply_substitution(term, substitution):
        """应用替换到项上"""
        if not substitution:
            return term

        # 如果是变量且在替换中有定义
        if term.is_variable and term.name in substitution:
            return Unifier.apply_substitution(substitution[term.name], substitution)

        # 如果是函数，递归应用到参数
        if term.args:
            new_args = [Unifier.apply_substitution(arg, substitution) for arg in term.args]
            return Term(term.name, term.is_variable, new_args)

        return term

    @staticmethod
    def apply_substitution_to_literal(literal, substitution):
        """应用替换到文字上"""
        new_terms = [Unifier.apply_substitution(term, substitution) for term in literal.terms]
        return Literal(literal.predicate, new_terms, literal.negated)

    @staticmethod
    def apply_substitution_to_clause(clause, substitution):
        """应用替换到子句上"""
        new_literals = [Unifier.apply_substitution_to_literal(literal, substitution)
                        for literal in clause.literals]
        return Clause(new_literals, clause.source)