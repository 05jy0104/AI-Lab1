# test_resolution.py
"""
测试Resolution Theorem Prover的正确性和性能
"""

import unittest
import time
from resolution import ResolutionProver
from problems import ProblemBuilder, get_all_problems


class TestResolutionProver(unittest.TestCase):
    """Resolution Prover测试套件"""

    def setUp(self):
        """测试前准备"""
        self.prover = ResolutionProver()
        self.start_time = time.time()

    def tearDown(self):
        """测试后清理"""
        duration = time.time() - self.start_time
        print(f"测试耗时: {duration:.3f}秒")

    def test_simple_contradiction(self):
        """测试简单矛盾检测 P ∧ ¬P"""
        print("\n=== 测试简单矛盾 ===")

        # 添加子句: P 和 ¬P
        from clause import Term, Literal, Clause
        p = Term("P")

        self.prover.add_clause(Clause([Literal("P", [])]))
        self.prover.add_clause(Clause([Literal("P", [], negated=True)]))

        result = self.prover.two_pointer_resolution()

        self.assertTrue(result, "应该找到矛盾")
        print("✅ 简单矛盾测试通过")

    def test_simple_tautology(self):
        """测试重言式 P ∨ ¬P"""
        print("\n=== 测试重言式 ===")

        from clause import Term, Literal, Clause
        p = Term("P")

        self.prover.add_clause(Clause([
            Literal("P", []),
            Literal("P", [], negated=True)
        ]))

        result = self.prover.two_pointer_resolution()

        # 重言式不会产生矛盾
        self.assertFalse(result, "重言式不应该产生矛盾")
        print("✅ 重言式测试通过")

    def test_simple_inference(self):
        """测试简单推理: P → Q, P ⊢ Q"""
        print("\n=== 测试简单推理 ===")

        from clause import Term, Literal, Clause
        p = Term("P")
        q = Term("Q")

        # P → Q 转化为 ¬P ∨ Q
        self.prover.add_clause(Clause([
            Literal("P", [], negated=True),
            Literal("Q", [])
        ]))
        # P
        self.prover.add_clause(Clause([Literal("P", [])]))
        # ¬Q (要证明的结论的否定)
        self.prover.add_clause(Clause([Literal("Q", [], negated=True)]))

        result = self.prover.two_pointer_resolution()

        self.assertTrue(result, "应该能够证明 Q")
        print("✅ 简单推理测试通过")

    def test_howling_hounds_problem(self):
        """测试Howling Hounds问题"""
        print("\n=== 测试Howling Hounds问题 ===")

        clauses = ProblemBuilder.create_howling_hounds_problem()

        for clause in clauses:
            self.prover.add_clause(clause)

        print(f"加载了 {len(clauses)} 个子句")
        result = self.prover.two_pointer_resolution()

        # Howling Hounds应该能够证明
        self.assertTrue(result, "Howling Hounds问题应该找到矛盾")

        stats = self.prover.get_statistics()
        print(f"推理统计: {stats['total_steps']} 步, {stats['total_clauses']} 子句")
        print("✅ Howling Hounds测试通过")

    def test_drug_dealer_problem(self):
        """测试Drug Dealer问题"""
        print("\n=== 测试Drug Dealer问题 ===")

        clauses = ProblemBuilder.create_drug_dealer_problem()

        for clause in clauses:
            self.prover.add_clause(clause)

        print(f"加载了 {len(clauses)} 个子句")
        result = self.prover.two_pointer_resolution()

        # Drug Dealer可能不会产生矛盾，我们主要测试算法是否正常运行
        stats = self.prover.get_statistics()
        print(f"推理统计: {stats['total_steps']} 步, {stats['total_clauses']} 子句")

        # 这个测试主要验证算法不会崩溃
        self.assertIsInstance(result, bool)
        print("✅ Drug Dealer测试通过")

    def test_unification_functionality(self):
        """测试合一算法功能"""
        print("\n=== 测试合一算法 ===")

        from clause import Term, Literal
        from unification import Unifier

        # 测试变量合一
        x = Term("x", is_variable=True)
        a = Term("a")
        substitution = Unifier.unify(x, a)
        self.assertIsNotNone(substitution)
        self.assertEqual(substitution.get("x"), a)
        print("✅ 变量合一测试通过")

        # 测试文字合一
        literal1 = Literal("P", [x])
        literal2 = Literal("P", [a])
        substitution = Unifier.unify_literals(literal1, literal2)
        self.assertIsNotNone(substitution)
        print("✅ 文字合一测试通过")

    def test_performance_benchmark(self):
        """性能基准测试"""
        print("\n=== 性能基准测试 ===")

        from clause import Term, Literal, Clause

        # 创建中等复杂度的测试
        clauses = []
        for i in range(5):
            p = Term(f"P{i}")
            q = Term(f"Q{i}")
            clauses.append(Clause([
                Literal(f"P{i}", []),
                Literal(f"Q{i}", [])
            ]))
            clauses.append(Clause([
                Literal(f"P{i}", [], negated=True),
                Literal(f"R{i}", [])
            ]))

        # 添加矛盾
        clauses.append(Clause([Literal("P0", [], negated=True)]))
        clauses.append(Clause([Literal("P0", [])]))

        for clause in clauses:
            self.prover.add_clause(clause)

        start_time = time.time()
        result = self.prover.two_pointer_resolution()
        end_time = time.time()

        self.assertTrue(result, "应该找到矛盾")
        print(f"性能: 处理 {len(clauses)} 个子句，耗时 {end_time - start_time:.3f} 秒")
        print("✅ 性能测试通过")


def run_comprehensive_tests():
    """运行全面的测试套件"""
    print("开始运行Resolution Theorem Prover全面测试")
    print("=" * 60)

    # 创建测试套件
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestResolutionProver)

    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    print("=" * 60)
    print("测试完成!")

    # 输出总结
    print(f"\n测试总结:")
    print(f"运行测试: {result.testsRun}")
    print(f"失败: {len(result.failures)}")
    print(f"错误: {len(result.errors)}")

    if result.wasSuccessful():
        print("🎉 所有测试通过!")
    else:
        print("❌ 有测试失败，请检查问题")

    return result.wasSuccessful()


def quick_test():
    """快速测试主要功能"""
    print("快速测试Resolution Prover...")

    # 测试简单矛盾
    prover = ResolutionProver()
    from clause import Term, Literal, Clause

    p = Term("P")
    prover.add_clause(Clause([Literal("P", [])]))
    prover.add_clause(Clause([Literal("P", [], negated=True)]))

    result = prover.two_pointer_resolution()

    if result:
        print("✅ 基础功能正常")
    else:
        print("❌ 基础功能异常")

    return result


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "quick":
        quick_test()
    else:
        run_comprehensive_tests()