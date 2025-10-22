from clause import Term, Literal, Clause
from resolution import ResolutionProver


def create_howling_hounds_problem():
    """
    创建Howling Hounds问题的子句集

    已知条件：
    a) All hounds howl at night
    b) Anyone who has any cats will not have any mice
    c) Light sleepers do not have anything which howls at night
    d) John has either a cat or a hound

    要证明：If John is a light sleeper, then John does not have any mice
    """
    print("=== Howling Hounds 问题 ===")

    clauses = []

    # 定义变量和常量
    x = Term("X", is_variable=True)
    y = Term("Y", is_variable=True)
    z = Term("Z", is_variable=True)
    john = Term("John")

    print("将自然语言转化为一阶逻辑公式...")

    # a) All hounds howl at night: ∀x (Hound(x) → Howl(x))
    # 转化为子句: ¬Hound(x) ∨ Howl(x)
    clause_a = Clause([
        Literal("Hound", [x], negated=True),
        Literal("Howl", [x])
    ])
    clauses.append(clause_a)
    print(f"a) {clause_a}")

    # b) Anyone who has any cats will not have any mice:
    # ∀x [∃y (Has(x,y) ∧ Cat(y)) → ¬∃z (Has(x,z) ∧ Mouse(z))]
    # 转化为: ¬Has(x,y) ∨ ¬Cat(y) ∨ ¬Has(x,z) ∨ ¬Mouse(z)
    clause_b = Clause([
        Literal("Has", [x, y], negated=True),
        Literal("Cat", [y], negated=True),
        Literal("Has", [x, z], negated=True),
        Literal("Mouse", [z], negated=True)
    ])
    clauses.append(clause_b)
    print(f"b) {clause_b}")

    # c) Light sleepers do not have anything which howls at night:
    # ∀x∀y (LightSleeper(x) ∧ Has(x,y) ∧ Howl(y) → False)
    # 转化为: ¬LightSleeper(x) ∨ ¬Has(x,y) ∨ ¬Howl(y)
    clause_c = Clause([
        Literal("LightSleeper", [x], negated=True),
        Literal("Has", [x, y], negated=True),
        Literal("Howl", [y], negated=True)
    ])
    clauses.append(clause_c)
    print(f"c) {clause_c}")

    # d) John has either a cat or a hound:
    # ∃y (Has(John,y) ∧ (Cat(y) ∨ Hound(y)))
    # 转化为两个子句: Has(John, A) 和 Cat(A) ∨ Hound(A)
    a = Term("A")  # Skolem常数
    clause_d1 = Clause([Literal("Has", [john, a])])
    clause_d2 = Clause([Literal("Cat", [a]), Literal("Hound", [a])])
    clauses.append(clause_d1)
    clauses.append(clause_d2)
    print(f"d1) {clause_d1}")
    print(f"d2) {clause_d2}")

    # 要证明的结论: If John is a light sleeper, then John does not have any mice
    # 转化为反驳: LightSleeper(John) ∧ ∃z (Has(John,z) ∧ Mouse(z))
    # 需要转化为子句形式添加到知识库中进行反驳
    clause_neg1 = Clause([Literal("LightSleeper", [john])])  # 假设John是浅眠者
    b = Term("B")  # Skolem常数
    clause_neg2 = Clause([Literal("Has", [john, b])])  # 假设John有某物B
    clause_neg3 = Clause([Literal("Mouse", [b])])  # 假设B是老鼠

    clauses.append(clause_neg1)
    clauses.append(clause_neg2)
    clauses.append(clause_neg3)
    print("要反驳的结论:")
    print(f"¬结论1) {clause_neg1}")
    print(f"¬结论2) {clause_neg2}")
    print(f"¬结论3) {clause_neg3}")

    return clauses, "Howling Hounds"


def create_drug_dealer_problem():
    """
    创建Drug dealer and customs official问题的子句集

    已知条件：
    a) The customs officials searched everyone who entered the country who was not a VIP
    b) Some of the drug dealers entered the country, and they were only searched by drug dealers
    c) No drug dealer was a VIP
    d) Some of the customs officials were drug dealers
    """
    print("\n=== Drug Dealer 问题 ===")

    clauses = []

    # 定义变量和常量
    x = Term("X", is_variable=True)
    y = Term("Y", is_variable=True)
    z = Term("Z", is_variable=True)

    print("将自然语言转化为一阶逻辑公式...")

    # a) The customs officials searched everyone who entered the country who was not a VIP
    # ∀x∀y (CustomsOfficial(x) ∧ EnteredCountry(y) ∧ ¬VIP(y) → SearchedBy(x,y))
    # 转化为: ¬CustomsOfficial(x) ∨ ¬EnteredCountry(y) ∨ VIP(y) ∨ SearchedBy(x,y)
    clause_a = Clause([
        Literal("CustomsOfficial", [x], negated=True),
        Literal("EnteredCountry", [y], negated=True),
        Literal("VIP", [y]),
        Literal("SearchedBy", [x, y])
    ])
    clauses.append(clause_a)
    print(f"a) {clause_a}")

    # b) Some of the drug dealers entered the country, and they were only searched by drug dealers
    # ∃x (DrugDealer(x) ∧ EnteredCountry(x) ∧ ∀y (SearchedBy(y,x) → DrugDealer(y)))
    # 转化为两个子句:
    # 1. DrugDealer(A) ∧ EnteredCountry(A)  [存在量词实例化]
    # 2. ¬SearchedBy(y,A) ∨ DrugDealer(y)   [全称量词转化为子句]
    a = Term("A")  # Skolem常数
    clause_b1 = Clause([
        Literal("DrugDealer", [a]),
        Literal("EnteredCountry", [a])
    ])
    clause_b2 = Clause([
        Literal("SearchedBy", [y, a], negated=True),
        Literal("DrugDealer", [y])
    ])
    clauses.append(clause_b1)
    clauses.append(clause_b2)
    print(f"b1) {clause_b1}")
    print(f"b2) {clause_b2}")

    # c) No drug dealer was a VIP: ∀x (DrugDealer(x) → ¬VIP(x))
    # 转化为: ¬DrugDealer(x) ∨ ¬VIP(x)
    clause_c = Clause([
        Literal("DrugDealer", [x], negated=True),
        Literal("VIP", [x], negated=True)
    ])
    clauses.append(clause_c)
    print(f"c) {clause_c}")

    # d) Some of the customs officials were drug dealers: ∃x (CustomsOfficial(x) ∧ DrugDealer(x))
    # 转化为: CustomsOfficial(B) ∧ DrugDealer(B)
    b = Term("B")  # Skolem常数
    clause_d = Clause([
        Literal("CustomsOfficial", [b]),
        Literal("DrugDealer", [b])
    ])
    clauses.append(clause_d)
    print(f"d) {clause_d}")

    # 这个问题通常是要找出隐含矛盾，不需要额外添加否定结论
    return clauses, "Drug Dealer"


def run_problem(problem_name, clauses):
    """运行单个问题的证明过程"""
    print(f"\n{'=' * 50}")
    print(f"开始解决 {problem_name} 问题")
    print(f"{'=' * 50}")

    prover = ResolutionProver()

    # 添加子句到证明器
    for i, clause in enumerate(clauses):
        prover.add_clause(clause)

    print(f"\n初始子句集 ({len(prover.clauses)} 个子句):")
    for i, clause in enumerate(prover.clauses):
        print(f"{i + 1:2d}. {clause}")

    # 执行归结推理
    print(f"\n开始归结推理...")
    result = prover.two_pointer_resolution()

    # 输出结果
    print(f"\n{'=' * 30}")
    if result:
        print(f"✅ {problem_name}: 定理得证！")
    else:
        print(f"❌ {problem_name}: 无法证明定理")
    print(f"{'=' * 30}")

    # 显示统计信息
    stats = prover.get_statistics()
    print(f"\n推理统计:")
    print(f"总推理步数: {stats['total_steps']}")
    print(f"总生成子句数: {stats['total_clauses']}")
    print(f"是否找到空子句: {stats['empty_clause_found']}")

    # 显示详细的推理过程
    show_details = input("\n是否显示详细的推理过程？(y/n): ").lower().strip()
    if show_details == 'y':
        prover.print_resolution_history()

    return prover, result


def demo_unification():
    """演示合一算法的功能"""
    print("\n" + "=" * 60)
    print("合一算法演示")
    print("=" * 60)

    # 测试用例1: 简单的变量合一
    print("测试1: 简单变量合一")
    term1 = Term("X", is_variable=True)
    term2 = Term("john")
    substitution = Unifier.unify(term1, term2)
    print(f"合一 {term1} 和 {term2}: {substitution}")

    # 测试用例2: 函数项合一
    print("\n测试2: 函数项合一")
    term1 = Term("f", False, [Term("X", is_variable=True), Term("a")])
    term2 = Term("f", False, [Term("b"), Term("Y", is_variable=True)])
    substitution = Unifier.unify(term1, term2)
    print(f"合一 {term1} 和 {term2}: {substitution}")

    # 测试用例3: 文字合一
    print("\n测试3: 文字合一")
    literal1 = Literal("P", [Term("X", is_variable=True), Term("a")])
    literal2 = Literal("P", [Term("b"), Term("Y", is_variable=True)])
    substitution = Unifier.unify_literals(literal1, literal2)
    print(f"合一 {literal1} 和 {literal2}: {substitution}")


def main():
    """主函数"""
    print("=" * 70)
    print("        Resolution Theorem Prover - 一阶逻辑推理系统")
    print("=" * 70)
    print("作者: [成员A姓名] [学号]")
    print("      [成员B姓名] [学号]")
    print("日期: 2025-10-XX")
    print("=" * 70)

    while True:
        print("\n请选择要运行的问题:")
        print("1. Howling Hounds 问题")
        print("2. Drug Dealer 问题")
        print("3. 合一算法演示")
        print("4. 运行所有问题")
        print("5. 退出")

        choice = input("\n请输入选择 (1-5): ").strip()

        if choice == '1':
            clauses, name = create_howling_hounds_problem()
            run_problem(name, clauses)

        elif choice == '2':
            clauses, name = create_drug_dealer_problem()
            run_problem(name, clauses)

        elif choice == '3':
            from unification import Unifier
            demo_unification()

        elif choice == '4':
            # 运行Howling Hounds问题
            clauses1, name1 = create_howling_hounds_problem()
            prover1, result1 = run_problem(name1, clauses1)

            # 运行Drug Dealer问题
            clauses2, name2 = create_drug_dealer_problem()
            prover2, result2 = run_problem(name2, clauses2)

            print("\n" + "=" * 70)
            print("所有问题运行完成！")
            print("=" * 70)

        elif choice == '5':
            print("感谢使用 Resolution Theorem Prover！")
            break

        else:
            print("无效选择，请重新输入！")

        input("\n按Enter键继续...")


if __name__ == "__main__":
    # 导入Unifier用于演示
    from unification import Unifier

    main()