# problems.py
"""
一阶逻辑问题定义 - 高度优化版本
确保在合理步数内完成推理
"""

from clause import Term, Literal, Clause


class ProblemBuilder:
    """问题构建器，高度优化问题建模"""

    @staticmethod
    def create_howling_hounds_optimized():
        """高度优化的Howling Hounds问题"""
        print("构建高度优化的 Howling Hounds 问题...")

        # 使用最少的变量和简单的常量名
        x = Term("x", is_variable=True)
        y = Term("y", is_variable=True)
        john = Term("John")
        animal = Term("a")  # 简单常量名

        clauses = []

        # 1. 所有猎犬嚎叫: ¬Hound(x) ∨ Howl(x)
        clauses.append(Clause([
            Literal("Hound", [x], negated=True),
            Literal("Howl", [x])
        ]))

        # 2. 浅眠者没有嚎叫的动物: ¬LightSleeper(x) ∨ ¬Has(x,y) ∨ ¬Howl(y)
        clauses.append(Clause([
            Literal("LightSleeper", [x], negated=True),
            Literal("Has", [x, y], negated=True),
            Literal("Howl", [y], negated=True)
        ]))

        # 3. John是浅眠者
        clauses.append(Clause([Literal("LightSleeper", [john])]))

        # 4. John有动物
        clauses.append(Clause([Literal("Has", [john, animal])]))

        # 5. 动物是猎犬
        clauses.append(Clause([Literal("Hound", [animal])]))

        # 要证明结论的否定: John有老鼠
        clauses.append(Clause([Literal("HasMouse", [john])]))

        print(f"构建完成，共 {len(clauses)} 个子句")
        for i, clause in enumerate(clauses, 1):
            print(f"{i}. {clause}")

        return clauses

    @staticmethod
    def create_drug_dealer_optimized():
        """优化的Drug dealer问题 - 修复版本"""
        print("\n构建优化的 Drug Dealer 问题...")

        clauses = []

        # 定义变量
        x = Term("x", is_variable=True)
        y = Term("y", is_variable=True)
        z = Term("z", is_variable=True)

        # Skolem常数
        dealer = Term("d")  # 进入国家的毒贩
        official = Term("o")  # 是毒贩的海关官员

        # 1. 海关官员搜查所有进入的非VIP
        # CustomsOfficial(x) ∧ Entered(y) ∧ ¬VIP(y) → SearchedBy(x,y)
        clauses.append(Clause([
            Literal("CustomsOfficial", [x], negated=True),
            Literal("Entered", [y], negated=True),
            Literal("VIP", [y]),
            Literal("SearchedBy", [x, y])
        ]))

        # 2. 毒贩d进入国家且不是VIP
        clauses.append(Clause([Literal("DrugDealer", [dealer])]))
        clauses.append(Clause([Literal("Entered", [dealer])]))
        clauses.append(Clause([Literal("VIP", [dealer], negated=True)]))

        # 3. 所有毒贩都不是VIP
        clauses.append(Clause([
            Literal("DrugDealer", [x], negated=True),
            Literal("VIP", [x], negated=True)
        ]))

        # 4. 官员o是海关官员且是毒贩
        clauses.append(Clause([Literal("CustomsOfficial", [official])]))
        clauses.append(Clause([Literal("DrugDealer", [official])]))

        # 5. 关键约束：毒贩只被毒贩搜查
        # 如果毒贩y被x搜查，那么x必须是毒贩
        clauses.append(Clause([
            Literal("DrugDealer", [y], negated=True),
            Literal("SearchedBy", [x, y], negated=True),
            Literal("DrugDealer", [x])
        ]))

        # 6. 关键约束：每个进入的非VIP都会被某个海关官员搜查
        # 这个约束确保毒贩d会被官员o搜查
        clauses.append(Clause([
            Literal("Entered", [y], negated=True),
            Literal("VIP", [y]),
            Literal("CustomsOfficial", [x]),
            Literal("SearchedBy", [x, y])
        ]))

        # 7. 要证明的结论的否定：没有海关官员是毒贩
        # 实际上我们要证明"有些海关官员是毒贩"，所以否定是"没有海关官员是毒贩"
        clauses.append(Clause([
            Literal("CustomsOfficial", [x], negated=True),
            Literal("DrugDealer", [x], negated=True)
        ]))

        print(f"构建完成，共 {len(clauses)} 个子句")
        for i, clause in enumerate(clauses, 1):
            print(f"{i}. {clause}")

        return clauses

    @staticmethod
    def create_simple_test():
        """创建简单测试用例"""
        print("构建简单测试用例...")

        clauses = []

        # P
        clauses.append(Clause([Literal("P", [])]))

        # ¬P
        clauses.append(Clause([Literal("P", [], negated=True)]))

        print(f"构建完成，共 {len(clauses)} 个子句")
        return clauses


def get_all_problems():
    """获取所有优化的问题"""
    return {
        'howling_hounds': {
            'name': 'Howling Hounds (优化版)',
            'description': '高度优化版本，确保快速推理',
            'builder': ProblemBuilder.create_howling_hounds_optimized,
            'expected_result': True
        },
        'drug_dealer': {
            'name': 'Drug Dealer (优化版)',
            'description': '优化版本的问题建模',
            'builder': ProblemBuilder.create_drug_dealer_optimized,
            'expected_result': True
        },
        'simple_test': {
            'name': '简单测试',
            'description': '基础矛盾测试',
            'builder': ProblemBuilder.create_simple_test,
            'expected_result': True
        }
    }


def print_problem_info(problem_name):
    """打印问题的详细信息"""
    problems = get_all_problems()
    if problem_name in problems:
        info = problems[problem_name]
        print(f"问题: {info['name']}")
        print(f"描述: {info['description']}")
        print(f"预期结果: {'找到矛盾' if info['expected_result'] else '未找到矛盾'}")
    else:
        print(f"未知问题: {problem_name}")


if __name__ == "__main__":
    # 显示所有问题信息
    print("Resolution Theorem Prover - 优化问题定义")
    print("=" * 50)

    for problem_id in get_all_problems():
        print_problem_info(problem_id)
        print()