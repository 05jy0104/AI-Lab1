# check_basic.py
def test_basic_functionality():
    """测试基础功能"""
    print("=== 基础功能测试 ===")

    try:
        # 1. 测试导入
        from clause import Term, Literal, Clause
        from unification import Unifier
        from resolution import ResolutionProver
        print("✅ 所有模块导入成功")

        # 2. 测试数据结构
        x = Term("x", is_variable=True)
        john = Term("John")
        literal = Literal("Human", [x])
        clause = Clause([literal])
        print("✅ 数据结构创建成功")

        # 3. 测试合一算法
        substitution = Unifier.unify(x, john)
        print(f"✅ 合一算法测试: {substitution}")

        # 4. 测试归结器
        prover = ResolutionProver()
        prover.add_clause(clause)
        print("✅ 归结器实例化成功")

        # 5. 测试哈希功能
        term_set = {x, john}
        literal_set = {literal}
        print("✅ 哈希功能正常")

        print("\n🎉 所有基础功能测试通过！")
        return True

    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    test_basic_functionality()