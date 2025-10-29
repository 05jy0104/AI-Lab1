# resolution.py
from clause import Clause, Literal
from unification import Unifier
import copy
import time


class ResolutionProver:
    """Two-Pointer Resolution定理证明器"""

    def __init__(self):
        self.clauses = []  # 子句集
        self.steps = 0  # 推理步数计数器
        self.history = []  # 推理历史记录
        self.max_steps = 500  # 减少最大推理步数

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

    def has_complementary_predicates(self, clause1, clause2):
        """快速检查两个子句是否有互补的谓词"""
        preds1 = set((lit.predicate, lit.negated) for lit in clause1.literals)
        preds2 = set((lit.predicate, not lit.negated) for lit in clause2.literals)
        return bool(preds1 & preds2)

    def two_pointer_resolution(self):
        """
        优化的two-pointer resolution算法
        返回: 如果找到矛盾返回True，否则返回False
        """
        self.steps = 0
        self.history = []
        start_time = time.time()

        # 使用集合来快速检查重复子句
        clause_set = set(str(clause) for clause in self.clauses)

        print(f"开始推理，初始子句数: {len(self.clauses)}")

        while self.steps < self.max_steps:
            new_clauses = []
            n = len(self.clauses)
            found_contradiction = False

            # 两两遍历子句对
            for i in range(n):
                for j in range(i + 1, n):
                    clause1 = self.clauses[i]
                    clause2 = self.clauses[j]

                    # 快速检查：如果子句没有互补谓词，跳过
                    if not self.has_complementary_predicates(clause1, clause2):
                        continue

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

                                    # 性能监控
                                    if self.steps % 100 == 0:
                                        current_time = time.time()
                                        elapsed = current_time - start_time
                                        print(
                                            f"进度: {self.steps}步, 耗时: {elapsed:.2f}秒, 子句数: {len(self.clauses)}")

                                    # 如果得到空子句，返回成功
                                    if resolvent.is_empty():
                                        print(f"🎉 找到矛盾！在第 {self.steps} 步推导出空子句")
                                        return True

                                    # 如果新子句不在已知子句集中，添加它
                                    resolvent_str = str(resolvent)
                                    if resolvent_str not in clause_set:
                                        clause_set.add(resolvent_str)
                                        new_clauses.append(resolvent)

                                    # 检查步数限制
                                    if self.steps >= self.max_steps:
                                        print(f"达到最大步数限制 {self.max_steps}")
                                        return False

            # 如果没有新子句产生，停止
            if not new_clauses:
                print(f"在 {self.steps} 步后未产生新子句，无法证明")
                return False

            # 添加新子句到子句集
            self.clauses.extend(new_clauses)
            print(f"生成 {len(new_clauses)} 个新子句，总子句数: {len(self.clauses)}")

        print(f"达到最大步数限制 {self.max_steps}，未找到证明")
        return False

    def print_resolution_history(self):
        """打印详细的推理历史"""
        print("\n=== 归结推理过程 ===")
        for step in self.history[-20:]:  # 只显示最后20步
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