from clause import Term, Literal, Clause
from resolution import ResolutionProver
from problems import ProblemBuilder, get_all_problems
from unification import Unifier


def run_optimized_problem(problem_name, clauses):
    """运行优化的问题证明过程"""
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

    # 执行优化的归结推理
    print(f"\n开始归结推理...")
    import time
    start_time = time.time()
    result = prover.two_pointer_resolution()
    end_time = time.time()

    # 输出结果
    print(f"\n{'=' * 30}")
    if result:
        print(f"✅ {problem_name}: 定理得证！")
    else:
        print(f"❌ {problem_name}: 无法证明定理")
    print(f"{'=' * 30}")

    # 显示统计信息
    stats = prover.get_statistics()
    duration = end_time - start_time
    print(f"\n推理统计:")
    print(f"总推理步数: {stats['total_steps']}")
    print(f"总生成子句数: {stats['total_clauses']}")
    print(f"推理耗时: {duration:.3f}秒")
    print(f"是否找到空子句: {stats['empty_clause_found']}")

    # 性能评估
    if stats['total_steps'] < 500:
        print("🎉 性能优秀：在500步内完成！")
    elif stats['total_steps'] < 1000:
        print("✅ 性能良好：在1000步内完成")
    else:
        print("⚠️  性能警告：超过1000步")

    # 显示详细的推理过程
    if result or stats['total_steps'] < 50:
        show_details = input("\n是否显示详细的推理过程？(y/n): ").lower().strip()
        if show_details == 'y':
            prover.print_resolution_history()

    return prover, result


def demo_optimized_unification():
    """演示优化的合一算法"""
    print("\n" + "=" * 60)
    print("优化的合一算法演示")
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
    print("        Resolution Theorem Prover - 优化版本")
    print("=" * 70)
    print("优化特性:")
    print("- 修复变量标准化问题")
    print("- 优化合一算法性能")
    print("- 减少最大推理步数到500")
    print("- 高度优化问题建模")
    print("=" * 70)

    while True:
        print("\n请选择要运行的问题:")
        print("1. Howling Hounds 问题 ")
        print("2. Drug Dealer 问题 ")
        print("3. 简单测试用例")
        print("4. 合一算法演示")
        print("5. 运行所有优化问题")
        print("6. 退出")

        choice = input("\n请输入选择 (1-6): ").strip()

        if choice == '1':
            clauses = ProblemBuilder.create_howling_hounds_optimized()
            run_optimized_problem("Howling Hounds ", clauses)

        elif choice == '2':
            clauses = ProblemBuilder.create_drug_dealer_optimized()
            run_optimized_problem("Drug Dealer ", clauses)

        elif choice == '3':
            clauses = ProblemBuilder.create_simple_test()
            run_optimized_problem("简单测试", clauses)

        elif choice == '4':
            demo_optimized_unification()

        elif choice == '5':
            # 运行所有优化问题
            problems = get_all_problems()
            results = []

            for problem_id, problem_info in problems.items():
                print(f"\n{'=' * 60}")
                print(f"运行: {problem_info['name']}")
                clauses = problem_info['builder']()
                prover, result = run_optimized_problem(problem_info['name'], clauses)
                results.append((problem_info['name'], result, prover.steps))

            # 显示总结
            print("\n" + "=" * 70)
            print("所有问题运行完成！")
            print("=" * 70)
            for name, result, steps in results:
                status = "✅ 证明成功" if result else "❌ 未证明"
                print(f"{name}: {status} (步数: {steps})")

        elif choice == '6':
            print("感谢使用 Resolution Theorem Prover！")
            break

        else:
            print("无效选择，请重新输入！")

        input("\n按Enter键继续...")


if __name__ == "__main__":
    main()