# experiment_log.py
"""
实验过程记录系统
记录详细的推理过程并生成报告
"""

import datetime
import json
import time
from resolution import ResolutionProver
from problems import ProblemBuilder, get_all_problems


class ExperimentLogger:
    """实验记录器"""

    def __init__(self, verbose=True):
        self.verbose = verbose
        self.experiments = []
        self.current_experiment = None

    def start_experiment(self, problem_name, problem_description):
        """开始新的实验"""
        self.current_experiment = {
            'problem_name': problem_name,
            'problem_description': problem_description,
            'start_time': datetime.datetime.now().isoformat(),
            'clauses': [],
            'resolution_steps': [],
            'statistics': {},
            'result': None,
            'duration': 0
        }

        if self.verbose:
            print(f"\n🔬 开始实验: {problem_name}")
            print(f"描述: {problem_description}")

    def log_clauses(self, clauses):
        """记录初始子句集"""
        clause_strs = [str(clause) for clause in clauses]
        self.current_experiment['clauses'] = clause_strs

        if self.verbose:
            print(f"📋 加载 {len(clauses)} 个子句:")
            for i, clause in enumerate(clause_strs, 1):
                print(f"  {i:2d}. {clause}")

    def log_resolution_step(self, step_info):
        """记录每一步归结过程"""
        self.current_experiment['resolution_steps'].append(step_info)

        if self.verbose and step_info.get('is_empty', False):
            print(f"🎉 步骤 {step_info['step']}: 推导出空子句!")

    def end_experiment(self, result, statistics, prover=None):
        """结束实验并记录结果"""
        end_time = datetime.datetime.now()
        start_time = datetime.datetime.fromisoformat(self.current_experiment['start_time'])
        duration = (end_time - start_time).total_seconds()

        self.current_experiment.update({
            'end_time': end_time.isoformat(),
            'result': result,
            'statistics': statistics,
            'duration': duration
        })

        # 如果提供了prover，记录完整历史
        if prover and hasattr(prover, 'history'):
            self.current_experiment['full_history'] = prover.history

        self.experiments.append(self.current_experiment)

        if self.verbose:
            status = "✅ 证明成功" if result else "❌ 未找到证明"
            print(f"\n实验结束: {status}")
            print(f"耗时: {duration:.3f} 秒")
            print(f"推理步数: {statistics['total_steps']}")
            print(f"生成子句数: {statistics['total_clauses']}")

        return self.current_experiment

    def run_problem_experiment(self, problem_id):
        """运行单个问题的完整实验"""
        problems = get_all_problems()
        if problem_id not in problems:
            print(f"❌ 未知问题: {problem_id}")
            return None

        problem_info = problems[problem_id]

        # 开始实验
        self.start_experiment(
            problem_info['name'],
            problem_info['description']
        )

        # 构建问题
        clauses = problem_info['builder']()
        self.log_clauses(clauses)

        # 创建证明器并设置回调
        prover = ResolutionProver()

        # 重写历史记录方法以捕获每一步
        original_resolve = prover.resolve

        def logged_resolve(clause1, clause2, literal1, literal2, substitution):
            result = original_resolve(clause1, clause2, literal1, literal2, substitution)

            step_info = {
                'step': prover.steps,
                'clause1': str(clause1),
                'clause2': str(clause2),
                'literal1': str(literal1),
                'literal2': str(literal2),
                'substitution': {k: str(v) for k, v in substitution.items()} if substitution else {},
                'resolvent': str(result),
                'is_empty': result.is_empty()
            }

            self.log_resolution_step(step_info)
            return result

        prover.resolve = logged_resolve

        # 添加子句并运行推理
        for clause in clauses:
            prover.add_clause(clause)

        # 运行推理
        start_time = time.time()
        result = prover.two_pointer_resolution()
        end_time = time.time()

        statistics = prover.get_statistics()
        statistics['actual_duration'] = end_time - start_time

        # 结束实验
        experiment = self.end_experiment(result, statistics, prover)

        return experiment

    def generate_text_report(self, filename=None):
        """生成文本格式的实验报告"""
        report = []
        report.append("Resolution Theorem Prover 实验报告")
        report.append("=" * 60)
        report.append(f"生成时间: {datetime.datetime.now()}")
        report.append(f"总实验数: {len(self.experiments)}")
        report.append("")

        for i, exp in enumerate(self.experiments, 1):
            report.append(f"实验 {i}: {exp['problem_name']}")
            report.append(f"描述: {exp['problem_description']}")
            report.append(f"开始时间: {exp['start_time']}")
            report.append(f"持续时间: {exp['duration']:.3f} 秒")
            report.append(f"结果: {'找到矛盾' if exp['result'] else '未找到矛盾'}")
            report.append(f"推理步数: {exp['statistics']['total_steps']}")
            report.append(f"总子句数: {exp['statistics']['total_clauses']}")

            report.append("\n初始子句:")
            for j, clause in enumerate(exp['clauses'], 1):
                report.append(f"  {j:2d}. {clause}")

            # 显示关键推理步骤（最后10步）
            steps = exp['resolution_steps']
            if steps:
                report.append(f"\n关键推理步骤 (共 {len(steps)} 步):")
                for step in steps[-10:]:  # 显示最后10步
                    status = "★" if step['is_empty'] else " "
                    report.append(f"  步骤 {step['step']}: {status} {step['resolvent']}")
                    if step['substitution']:
                        subst_str = ", ".join(f"{k}→{v}" for k, v in step['substitution'].items())
                        report.append(f"        替换: {subst_str}")

            report.append("\n" + "-" * 60)

        report_text = "\n".join(report)

        if filename:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(report_text)
            print(f"📄 文本报告已保存: {filename}")

        return report_text

    def generate_json_report(self, filename=None):
        """生成JSON格式的详细报告"""
        report = {
            'metadata': {
                'generated_at': datetime.datetime.now().isoformat(),
                'total_experiments': len(self.experiments),
                'system': 'Resolution Theorem Prover'
            },
            'experiments': self.experiments
        }

        if filename:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            print(f"📊 JSON报告已保存: {filename}")

        return report

    def print_summary(self):
        """打印实验摘要"""
        print("\n" + "=" * 60)
        print("实验摘要")
        print("=" * 60)

        for i, exp in enumerate(self.experiments, 1):
            status = "✅ 证明成功" if exp['result'] else "❌ 未证明"
            print(f"{i}. {exp['problem_name']}: {status}")
            print(f"   步数: {exp['statistics']['total_steps']}, "
                  f"子句: {exp['statistics']['total_clauses']}, "
                  f"耗时: {exp['duration']:.3f}s")


def run_complete_experiment_suite():
    """运行完整的实验套件"""
    print("开始运行完整实验套件")
    print("=" * 60)

    logger = ExperimentLogger(verbose=True)

    # 运行所有定义的问题
    problems = get_all_problems()

    for problem_id in problems:
        try:
            logger.run_problem_experiment(problem_id)
            print("\n" + "-" * 50)
        except Exception as e:
            print(f"❌ 运行问题 {problem_id} 时出错: {e}")
            import traceback
            traceback.print_exc()

    # 生成报告
    print("\n生成实验报告...")
    logger.generate_text_report("experiment_report.txt")
    logger.generate_json_report("experiment_report.json")

    # 显示摘要
    logger.print_summary()

    print(f"\n🎉 实验完成! 共运行 {len(logger.experiments)} 个问题")
    return logger


if __name__ == "__main__":
    # 运行完整实验
    logger = run_complete_experiment_suite()

    # 提示用户查看详细结果
    print("\n📁 生成的文件:")
    print("  - experiment_report.txt (可读报告)")
    print("  - experiment_report.json (详细数据)")
    print("\n要查看详细推理过程，请运行 main.py 并选择相应问题")