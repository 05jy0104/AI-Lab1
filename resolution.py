# resolution.py
from clause import Clause, Literal
from unification import Unifier
import copy


class ResolutionProver:
    """Two-Pointer Resolution定理证明器"""

    def __init__(self):
        self.clauses = []  # 子句集
        self.steps = 0  # 推理步数计数器
        self.history = []  # 推理历史记录
        self.max_steps = 1000  # 最大推理步数

    def add_clause(self, clause):
        """添加子句到子句集"""
        # 标准化变量后添加
        standardized_clause = clause.standardize_variables()
        self.clauses.append(standardized_clause)

    def resolve(self, clause1, clause2, literal1, literal2, substitution):
        """
        执行归结操作
        返回: 归结结果子句
        """
        # 应用替换到两个子句
        clause1_sub = Unifier.apply_substitution_to_clause(clause1, substitution)
        clause2_sub = Unifier.apply_substitution_to_clause(clause2, substitution)

        # 移除互补文字并合并子句
        new_literals = []

        # 添加 clause1 中除 literal1 外的所有文字
        for lit in clause1_sub.literals:
            if lit != literal1:
                new_literals.append(lit.copy())

        # 添加 clause2 中除 literal2 外的所有文字
        for lit in clause2_sub.literals:
            if lit != literal2:
                new_literals.append(lit.copy())

        # 去除重复文字
        unique_literals = []
        for lit in new_literals:
            if lit not in unique_literals:
                unique_literals.append(lit)

        # 创建归结子句并记录来源
        result_clause = Clause(unique_literals)
        result_clause.source = {
            'parent1': clause1.id,
            'parent2': clause2.id,
            'literal1': str(literal1),
            'literal2': str(literal2),
            'substitution': copy.deepcopy(substitution)
        }

        return result_clause

    def two_pointer_resolution(self):
        """
        Two-Pointer Resolution算法
        返回: 如果找到矛盾返回True，否则返回False
        """
        self.steps = 0
        self.history = []

        while self.steps < self.max_steps:
            new_clauses = []
            n = len(self.clauses)

            # 两两遍历子句对
            for i in range(n):
                for j in range(i + 1, n):
                    clause1 = self.clauses[i]
                    clause2 = self.clauses[j]

                    # 尝试归结两个子句中的每对文字
                    for literal1 in clause1.literals:
                        for literal2 in clause2.literals:
                            # 检查文字是否可能互补
                            if literal1.predicate == literal2.predicate and literal1.negated != literal2.negated:
                                # 尝试合一
                                substitution = Unifier.unify_literals(literal1, literal2)
                                if substitution is not None:
                                    # 执行归结
                                    resolvent = self.resolve(clause1, clause2, literal1, literal2, substitution)

                                    # 记录推理步骤
                                    step_info = {
                                        'step': self.steps + 1,
                                        'clause1': str(clause1),
                                        'clause2': str(clause2),
                                        'literal1': str(literal1),
                                        'literal2': str(literal2),
                                        'substitution': substitution,
                                        'resolvent': str(resolvent),
                                        'is_empty': resolvent.is_empty()
                                    }
                                    self.history.append(step_info)
                                    self.steps += 1

                                    # 如果得到空子句，返回成功
                                    if resolvent.is_empty():
                                        print(f"找到矛盾！在第 {self.steps} 步推导出空子句")
                                        return True

                                    # 如果新子句不在已知子句集中，添加它
                                    if not any(resolvent == existing for existing in self.clauses + new_clauses):
                                        new_clauses.append(resolvent)

            # 如果没有新子句产生，停止
            if not new_clauses:
                print(f"在 {self.steps} 步后未找到矛盾，无法证明")
                return False

            # 添加新子句到子句集
            self.clauses.extend(new_clauses)

        print(f"达到最大步数限制 {self.max_steps}，未找到证明")
        return False

    def print_resolution_history(self):
        """打印详细的推理历史"""
        print("\n=== 归结推理过程 ===")
        for step in self.history:
            print(f"步骤 {step['step']}:")
            print(f"  子句1: {step['clause1']}")
            print(f"  子句2: {step['clause2']}")
            print(f"  归结文字1: {step['literal1']}")
            print(f"  归结文字2: {step['literal2']}")
            if step['substitution']:
                subst_str = ", ".join(f"{var} → {val}" for var, val in step['substitution'].items())
                print(f"  替换: {subst_str}")
            print(f"  归结结果: {step['resolvent']}")
            if step['is_empty']:
                print("  ★ 推导出空子句！证明完成")
            print()

    def get_statistics(self):
        """获取推理统计信息"""
        return {
            'total_steps': self.steps,
            'total_clauses': len(self.clauses),
            'empty_clause_found': any(clause.is_empty() for clause in self.clauses),
            'history_length': len(self.history)
        }