# check_algorithms.py
def test_algorithms():
    """测试算法逻辑"""
    print("=== 算法逻辑测试 ===")

    from clause import Term, Literal, Clause
    from unification import Unifier
    from resolution import ResolutionProver

    try:
        # 测试1: 简单的矛盾检测
        print("测试1: 简单矛盾检测")
        prover = ResolutionProver()
        prover.add_clause(Clause([Literal("P", [])]))  # P
        prover.add_clause(Clause([Literal("P", [], negated=True)]))  # ¬P
        result = prover.two_pointer_resolution()
        print(f"简单矛盾检测: {'✅ 成功' if result else '❌ 失败'}")

        # 测试2: 合一功能
        print("\n测试2: 合一功能")
        x = Term("x", is_variable=True)
        a = Term("a")
        literal1 = Literal("Q", [x])
        literal2 = Literal("Q", [a])
        substitution = Unifier.unify_literals(literal1, literal2)
        print(f"合一测试: {substitution}")

        # 测试3: 变量标准化
        print("\n测试3: 变量标准化")
        clause = Clause([Literal("R", [x])])
        standardized = clause.standardize_variables()
        print(f"标准化前: {clause}")
        print(f"标准化后: {standardized}")

        print("\n🎉 算法逻辑测试完成！")
        return True

    except Exception as e:
        print(f"❌ 算法测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    test_algorithms()